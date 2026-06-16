#!/usr/bin/env python3
"""Print a short, read-only project memory brief."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


FIELD_PATTERNS = {
    "project": r"^- Project:\s*(.+)$",
    "kind": r"^- Kind:\s*(.+)$",
    "domain": r"^- Domain:\s*(.+)$",
    "phase": r"^- Current phase:\s*(.+)$",
    "branch": r"^- Current branch:\s*(.+)$",
    "latest": r"^- Latest conclusion:\s*(.+)$",
    "next": r"^- Next step:\s*(.+)$",
    "blockers": r"^- Blockers:\s*(.+)$",
    "risks": r"^- Active risks:\s*(.+)$",
}


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def extract_fields(status_text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for key, pattern in FIELD_PATTERNS.items():
        match = re.search(pattern, status_text, re.MULTILINE)
        if match:
            fields[key] = match.group(1).strip()
    return fields


def file_exists(target: Path, relative: str) -> bool:
    return (target / relative).exists()


def recommended_reads(target: Path, fields: dict[str, str]) -> list[str]:
    reads = ["PROJECT_STATUS.md", "docs/PRINCIPLES.md", "docs/PLAN.md"]
    text = " ".join(fields.values()).lower()

    if any(word in text for word in ["implement", "refactor", "broad", "feature", "code"]):
        reads.append("docs/VIBE_READINESS.md")
    if any(word in text for word in ["decision", "architecture", "direction", "rationale"]):
        reads.append("docs/DECISIONS.md")
    if any(word in text for word in ["setup", "dependency", "runtime", "environment", "build", "test"]):
        reads.append("docs/ENVIRONMENT.md")
    if any(word in text for word in ["git", "github", "branch", "remote", "release", "push", "pr"]):
        reads.append("docs/REPOSITORY.md")
    if file_exists(target, "docs/COORDINATION.md"):
        coordination = read(target / "docs/COORDINATION.md")
        if "Status: active" in coordination:
            reads.append("docs/COORDINATION.md")
    if file_exists(target, "docs/DOMAIN.md"):
        reads.append("docs/DOMAIN.md")

    result: list[str] = []
    for item in reads:
        if item not in result and file_exists(target, item):
            result.append(item)
    return result


def projectmem_distilled_files(target: Path) -> list[str]:
    root = target / ".projectmem"
    if not root.exists():
        return []
    candidates: list[Path] = []
    for pattern in ["**/summary*.md", "**/PROJECT_MAP.md", "**/AI_INSTRUCTIONS.md", "**/project_map*.md"]:
        candidates.extend(path for path in root.glob(pattern) if path.is_file())
    return sorted({str(path.relative_to(target)) for path in candidates})[:8]


def external_memory(target: Path) -> list[str]:
    notes: list[str] = []
    if (target / ".projectmem").exists():
        distilled = projectmem_distilled_files(target)
        if distilled:
            notes.append(
                "projectmem detected: use dynamic event summaries/precheck; distilled files: "
                + ", ".join(distilled)
            )
        else:
            notes.append(
                "projectmem detected: use its CLI/MCP summary and precheck; do not read raw event logs by default"
            )
    if (target / "conductor").exists():
        notes.append(
            "conductor detected: confirm whether Conductor or project-memory owns static context before editing overlapping docs"
        )
    return notes


def build_brief(target: Path) -> dict[str, object]:
    status_text = read(target / "PROJECT_STATUS.md")
    fields = extract_fields(status_text)
    return {
        "target": str(target),
        "status": fields,
        "recommended_reads": recommended_reads(target, fields),
        "external_memory": external_memory(target),
    }


def print_markdown(brief: dict[str, object]) -> None:
    status = brief["status"]
    assert isinstance(status, dict)
    print("# Project Memory Brief\n")
    if not status:
        print("No `PROJECT_STATUS.md` snapshot found.\n")
    else:
        for label, key in [
            ("Project", "project"),
            ("Kind", "kind"),
            ("Phase", "phase"),
            ("Branch", "branch"),
            ("Latest", "latest"),
            ("Next", "next"),
            ("Blockers", "blockers"),
            ("Risks", "risks"),
        ]:
            value = status.get(key)
            if value:
                print(f"- {label}: {value}")

    print("\n## Recommended Reads")
    reads = brief["recommended_reads"]
    assert isinstance(reads, list)
    if reads:
        for item in reads:
            print(f"- `{item}`")
    else:
        print("- No project-memory files found.")

    notes = brief["external_memory"]
    assert isinstance(notes, list)
    if notes:
        print("\n## External Memory")
        for note in notes:
            print(f"- {note}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Print a short project memory brief.")
    parser.add_argument("--target", default=".", help="Project directory to inspect.")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    args = parser.parse_args()

    target = Path(args.target).expanduser().resolve()
    brief = build_brief(target)
    if args.json:
        print(json.dumps(brief, indent=2))
    else:
        print_markdown(brief)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
