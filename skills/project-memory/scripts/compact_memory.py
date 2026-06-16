#!/usr/bin/env python3
"""Read-only compaction strategy generator for project memory docs."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


DEFAULT_BUDGETS = {
    "AGENTS.md": 160,
    "PROJECT_STATUS.md": 150,
    "docs/CONTEXT.md": 220,
    "docs/PRINCIPLES.md": 100,
    "docs/PLAN.md": 200,
    "docs/TRACKS.md": 260,
    "docs/VIBE_READINESS.md": 260,
    "docs/DECISIONS.md": 350,
    "docs/DOMAIN.md": 240,
    "docs/ENVIRONMENT.md": 220,
    "docs/REPOSITORY.md": 220,
    "docs/LOG.md": 500,
    "docs/COORDINATION.md": 220,
}

PROFILE_MULTIPLIERS = {
    "conservative": 1.0,
    "normal": 0.85,
}

OPERATIONAL_FILES = {
    "docs/ENVIRONMENT.md",
    "docs/REPOSITORY.md",
    "docs/COORDINATION.md",
}


@dataclass
class CompactionItem:
    action: str
    path: str
    reason: str
    recommendation: str
    risk: str


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def memory_files(target: Path) -> list[Path]:
    files: list[Path] = []
    for relative in ["AGENTS.md", "PROJECT_STATUS.md"]:
        path = target / relative
        if path.exists():
            files.append(path)
    docs = target / "docs"
    if docs.exists():
        files.extend(path for path in sorted(docs.glob("*.md")) if path.is_file())
    return files


def relative_to_target(path: Path, target: Path) -> str:
    return str(path.relative_to(target))


def max_lines_for(relative: str, text: str, profile: str) -> int | None:
    match = re.search(r"^\s*-\s*max_lines:\s*(\d+)\s*$", text, re.MULTILINE)
    base = int(match.group(1)) if match else DEFAULT_BUDGETS.get(relative)
    if not base:
        return None
    return max(40, int(base * PROFILE_MULTIPLIERS[profile]))


def add(
    items: list[CompactionItem],
    action: str,
    path: str,
    reason: str,
    recommendation: str,
    risk: str,
) -> None:
    items.append(CompactionItem(action, path, reason, recommendation, risk))


def plan(target: Path, profile: str) -> list[CompactionItem]:
    items: list[CompactionItem] = []

    for path in memory_files(target):
        relative = relative_to_target(path, target)
        text = read(path)
        budget = max_lines_for(relative, text, profile)
        count = len(text.splitlines())

        if budget and count > budget:
            if relative == "AGENTS.md":
                add(
                    items,
                    "migrate-agents",
                    relative,
                    f"{relative} has {count} lines; budget is {budget}.",
                    "Run migrate_agents.py to classify existing content and move detailed project memory to docs/. Keep only always-on routing rules in AGENTS.md.",
                    "high",
                )
            elif relative == "PROJECT_STATUS.md":
                add(
                    items,
                    "trim",
                    relative,
                    f"{relative} has {count} lines; budget is {budget}.",
                    "Keep current phase, latest conclusion, next action, blockers, active risks, handoff, and read-next links. Move history to docs/LOG.md.",
                    "medium",
                )
            elif relative == "docs/LOG.md":
                add(
                    items,
                    "summarize-or-archive",
                    relative,
                    f"{relative} has {count} lines; budget is {budget}.",
                    "Summarize routine completed history by month. Move old detail to docs/archive/ after developer confirmation.",
                    "medium",
                )
            elif relative == "docs/DECISIONS.md":
                add(
                    items,
                    "keep-with-index",
                    relative,
                    f"{relative} has {count} lines; budget is {budget}.",
                    "Do not delete decision rationale. Add or refresh a decision index and mark superseded decisions instead.",
                    "high",
                )
            elif relative in OPERATIONAL_FILES:
                add(
                    items,
                    "manual-review",
                    relative,
                    f"{relative} has {count} lines; budget is {budget}.",
                    "Operational context can be dangerous if over-compressed. Preserve current setup, branch, remote, and handoff details.",
                    "high",
                )
            else:
                add(
                    items,
                    "summarize",
                    relative,
                    f"{relative} has {count} lines; budget is {budget}.",
                    "Preserve current facts, decisions, assumptions, open questions, and risks. Move stale detail to the correct source-of-truth file.",
                    "medium",
                )

        if relative == "PROJECT_STATUS.md" and re.search(
            r"^##\s+\d{4}-\d{2}-\d{2}", text, re.MULTILINE
        ):
            add(
                items,
                "source-of-truth-fix",
                relative,
                "Status file appears to contain dated history.",
                "Move dated history to docs/LOG.md and keep PROJECT_STATUS.md as a current-state index.",
                "low",
            )

        if relative == "docs/LOG.md" and re.search(
            r"^\s*-\s*Decision:", text, re.MULTILINE | re.IGNORECASE
        ):
            add(
                items,
                "source-of-truth-fix",
                relative,
                "LOG.md appears to contain durable decisions.",
                "Copy durable decisions and rationale to docs/DECISIONS.md before summarizing log entries.",
                "medium",
            )

    for relative in sorted(OPERATIONAL_FILES):
        if (target / relative).exists():
            add(
                items,
                "do-not-change-by-default",
                relative,
                "Operational context can become dangerous if compressed blindly.",
                "Review manually. Preserve active setup, repository, branch, remote, and handoff state.",
                "high",
            )

    return items


def print_markdown(items: list[CompactionItem], profile: str) -> None:
    print("# Project Memory Compaction Plan\n")
    print(f"- Profile: `{profile}`")
    print("- Mode: read-only strategy; no files were modified")
    print("- Requirement: developer confirmation is required before applying changes")
    print("- Principle: compact by source-of-truth ownership, not just by length\n")

    if not items:
        print("No compaction actions recommended.")
        return

    sections = [
        "trim",
        "migrate-agents",
        "summarize",
        "summarize-or-archive",
        "keep-with-index",
        "manual-review",
        "source-of-truth-fix",
        "do-not-change-by-default",
    ]
    for section in sections:
        matching = [item for item in items if item.action == section]
        if not matching:
            continue
        print(f"## {section}")
        for item in matching:
            print(f"- Path: `{item.path}`")
            print(f"  Reason: {item.reason}")
            print(f"  Recommendation: {item.recommendation}")
            print(f"  Risk: {item.risk}")
        print()


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a read-only compaction plan.")
    parser.add_argument("--target", default=".", help="Project directory to inspect.")
    parser.add_argument(
        "--budget-profile",
        choices=sorted(PROFILE_MULTIPLIERS),
        default="conservative",
        help="Compaction threshold profile.",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    args = parser.parse_args()

    target = Path(args.target).expanduser().resolve()
    items = plan(target, args.budget_profile)

    if args.json:
        print(json.dumps([asdict(item) for item in items], indent=2))
    else:
        print_markdown(items, args.budget_profile)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
