#!/usr/bin/env python3
"""Generate a read-only PROJECT_STATUS.md sync proposal."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


FIELD_PATTERNS = {
    "Current phase": r"^- Current phase:\s*(.+)$",
    "Current branch": r"^- Current branch:\s*(.+)$",
    "Latest conclusion": r"^- Latest conclusion:\s*(.+)$",
    "Next step": r"^- Next step:\s*(.+)$",
    "Blockers": r"^- Blockers:\s*(.+)$",
    "Active risks": r"^- Active risks:\s*(.+)$",
}


@dataclass
class Proposal:
    target: str
    sources: list[str]
    current: dict[str, str]
    suggested: dict[str, str]
    notes: list[str]


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def git_lines(target: Path, args: list[str]) -> list[str]:
    try:
        proc = subprocess.run(
            ["git", *args],
            cwd=target,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except FileNotFoundError:
        return []
    if proc.returncode != 0:
        return []
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def status_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for key, pattern in FIELD_PATTERNS.items():
        match = re.search(pattern, text, re.MULTILINE)
        if match:
            fields[key] = match.group(1).strip()
    return fields


def is_placeholder(value: str) -> bool:
    return value.strip().strip("`").lower() in {"", "tbd", "todo", "unknown", "none recorded", "not recorded", "n/a", "-"}


def clean_summary(text: str, limit: int = 180) -> str:
    compact = " ".join(text.split())
    if not compact:
        return ""
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3].rstrip() + "..."


def read_summary_arg(value: str | None) -> tuple[str, str | None]:
    if not value:
        return "", None
    if value == "-":
        return sys.stdin.read(), "stdin"
    path = Path(value).expanduser()
    if path.exists():
        return read(path), str(path)
    return value, "literal"


def latest_log_checkpoint(target: Path) -> str:
    text = read(target / "docs" / "LOG.md")
    if not text:
        return ""
    sections = re.split(r"^##\s+", text, flags=re.MULTILINE)
    if len(sections) <= 1:
        return clean_summary(text, 220)
    return clean_summary("## " + sections[-1], 220)


def build_proposal(target: Path, agentmemory_summary: str = "", summary_source: str | None = None) -> Proposal:
    status_text = read(target / "PROJECT_STATUS.md")
    current = status_fields(status_text)
    branch = "\n".join(git_lines(target, ["branch", "--show-current"]))
    recent_commits = git_lines(target, ["log", "-3", "--oneline"])
    dirty = git_lines(target, ["status", "--short"])
    log_checkpoint = latest_log_checkpoint(target)

    sources: list[str] = []
    notes: list[str] = []
    if agentmemory_summary:
        sources.append(f"agentmemory summary ({summary_source or 'provided'})")
    else:
        notes.append("No agentmemory summary was provided; using git state and sparse LOG fallback only.")
    if log_checkpoint:
        sources.append("docs/LOG.md fallback checkpoint")
    if recent_commits:
        sources.append("git recent commits")
    if dirty:
        sources.append("git working tree")

    suggested = dict(current)
    if branch:
        suggested["Current branch"] = branch

    summary_basis = clean_summary(agentmemory_summary, 220) or log_checkpoint
    if summary_basis:
        suggested["Latest conclusion"] = summary_basis
    elif is_placeholder(suggested.get("Latest conclusion", "")):
        suggested["Latest conclusion"] = "No durable latest conclusion detected from available read-only inputs."

    if dirty:
        suggested["Current phase"] = suggested.get("Current phase") or "active development"
        suggested["Active risks"] = suggested.get("Active risks") or "working tree has uncommitted changes"
        notes.append(f"Working tree has {len(dirty)} changed file(s); verify status before handoff.")

    if recent_commits and is_placeholder(suggested.get("Next step", "")):
        suggested["Next step"] = "Review recent commits and define the next concrete implementation or validation step."

    for key in FIELD_PATTERNS:
        suggested.setdefault(key, current.get(key, "TBD"))

    return Proposal(
        target=str(target),
        sources=sources,
        current=current,
        suggested=suggested,
        notes=notes,
    )


def print_markdown(proposal: Proposal) -> None:
    print("# Status Sync Proposal\n")
    print("- Mode: read-only; no files were modified")
    print("- Target: `" + proposal.target + "`")
    if proposal.sources:
        print("- Sources: " + ", ".join(proposal.sources))
    else:
        print("- Sources: none detected")
    print("\n## Suggested PROJECT_STATUS.md Fields")
    for key in FIELD_PATTERNS:
        value = proposal.suggested.get(key, "TBD")
        print(f"- {key}: {value}")
    if proposal.notes:
        print("\n## Notes")
        for note in proposal.notes:
            print(f"- {note}")
    print("\n## Apply")
    print("Review the suggested fields. Patch `PROJECT_STATUS.md` only after developer confirmation.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a read-only PROJECT_STATUS.md sync proposal.")
    parser.add_argument("--target", default=".", help="Project directory to inspect.")
    parser.add_argument(
        "--agentmemory-summary",
        default="",
        help="Agentmemory summary text, path to a summary file, or '-' to read from stdin.",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    args = parser.parse_args()

    target = Path(args.target).expanduser().resolve()
    summary, summary_source = read_summary_arg(args.agentmemory_summary)
    proposal = build_proposal(target, summary, summary_source)
    if args.json:
        print(json.dumps(asdict(proposal), indent=2))
    else:
        print_markdown(proposal)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
