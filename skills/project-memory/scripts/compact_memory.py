#!/usr/bin/env python3
"""Read-only compaction strategy generator for project memory docs."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path


DEFAULT_BUDGETS = {
    "AGENTS.md": 90,
    "PROJECT_STATUS.md": 90,
    "docs/TRACKS.md": 260,
    "docs/DECISIONS.md": 350,
    "docs/DOMAIN.md": 240,
    "docs/ENVIRONMENT.md": 220,
    "docs/LOG.md": 220,
    "docs/COORDINATION.md": 220,
}

OPTIONAL_PROJECT_MEMORY_FILES = {
    "docs/API.md",
    "docs/APP_SPEC.md",
    "docs/BUILD_RUNBOOK.md",
    "docs/CLI_RUNBOOK.md",
    "docs/CLOUD_RUNBOOK.md",
    "docs/DATA.md",
    "docs/DESIGN_SYSTEM.md",
    "docs/DOCS_SPEC.md",
    "docs/DOMAIN.md",
    "docs/EVALUATION.md",
    "docs/LIBRARY_SPEC.md",
    "docs/SYSTEM_ARCHITECTURE.md",
    "docs/TRACKS.md",
    "docs/USER_FLOWS.md",
    "docs/WORKFLOWS.md",
}

PROFILE_MULTIPLIERS = {
    "conservative": 1.0,
    "normal": 0.85,
}

LEGACY_DOC_BUDGET = 220

OPERATIONAL_FILES = {
    "docs/ENVIRONMENT.md",
    "docs/COORDINATION.md",
}

FILENAME_TARGET_HINTS = [
    (re.compile(r"handoff|coordination", re.I), ["PROJECT_STATUS.md", "docs/COORDINATION.md"]),
    (re.compile(r"roadmap|plan|todo", re.I), ["PROJECT_STATUS.md"]),
    (re.compile(r"context|background|overview", re.I), ["AGENTS.md", "docs/DECISIONS.md"]),
    (re.compile(r"decision|adr|rationale", re.I), ["docs/DECISIONS.md"]),
    (re.compile(r"setup|environment|device|xcode|build", re.I), ["docs/ENVIRONMENT.md"]),
    (re.compile(r"repository|github|git|release|ci", re.I), ["docs/COORDINATION.md", "docs/ENVIRONMENT.md"]),
    (re.compile(r"validation|test|qa|checklist", re.I), ["PROJECT_STATUS.md", "docs/ENVIRONMENT.md"]),
    (re.compile(r"domain|algorithm|color|palette|mard|business|terminology", re.I), ["docs/DOMAIN.md", "docs/DECISIONS.md"]),
    (re.compile(r"changelog|history|log", re.I), ["docs/LOG.md"]),
]

CONTENT_TARGET_HINTS = [
    ("PROJECT_STATUS.md", ["current state", "active branch", "next step", "blocker", "roadmap", "milestone", "phase"]),
    ("AGENTS.md", ["red line", "must", "never", "validation", "security", "privacy"]),
    ("docs/DECISIONS.md", ["decision", "accepted", "rejected", "rationale", "alternative", "tradeoff"]),
    ("docs/ENVIRONMENT.md", ["setup", "xcode", "install", "device", "simulator", "dependency", "path"]),
    ("docs/COORDINATION.md", ["git", "github", "branch", "commit", "push", "release", "ci", "handoff", "coordination"]),
    ("docs/LOG.md", ["updated", "last updated", "completed", "merged", "history", "progress"]),
    ("docs/DOMAIN.md", ["domain", "algorithm", "palette", "mard", "user workflow", "terminology"]),
]


@dataclass
class CompactionItem:
    action: str
    path: str
    reason: str
    recommendation: str
    risk: str
    suggested_targets: list[str] = field(default_factory=list)
    confirmation: str = "Developer confirmation required before applying changes."


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


def legacy_budget(profile: str) -> int:
    return max(80, int(LEGACY_DOC_BUDGET * PROFILE_MULTIPLIERS[profile]))


def is_project_memory_doc(relative: str, text: str) -> bool:
    return (
        relative in DEFAULT_BUDGETS
        or relative in OPTIONAL_PROJECT_MEMORY_FILES
        or "Memory Metadata" in text
        or "Maintenance Rules" in text
    )


def suggested_targets(relative: str, text: str) -> list[str]:
    targets: list[str] = []
    name = Path(relative).name

    for pattern, pattern_targets in FILENAME_TARGET_HINTS:
        if pattern.search(name):
            for target in pattern_targets:
                if target not in targets:
                    targets.append(target)

    lowered = text.lower()
    scored: list[tuple[str, int]] = []
    for target, keywords in CONTENT_TARGET_HINTS:
        score = sum(1 for keyword in keywords if keyword in lowered)
        if score:
            scored.append((target, score))
    for target, _score in sorted(scored, key=lambda item: (-item[1], item[0]))[:4]:
        if target not in targets:
            targets.append(target)

    return targets or ["developer-review"]


def add(
    items: list[CompactionItem],
    action: str,
    path: str,
    reason: str,
    recommendation: str,
    risk: str,
    suggested_targets: list[str] | None = None,
    confirmation: str = "Developer confirmation required before applying changes.",
) -> None:
    items.append(
        CompactionItem(
            action=action,
            path=path,
            reason=reason,
            recommendation=recommendation,
            risk=risk,
            suggested_targets=suggested_targets or [],
            confirmation=confirmation,
        )
    )


def plan(target: Path, profile: str) -> list[CompactionItem]:
    items: list[CompactionItem] = []

    for path in memory_files(target):
        relative = relative_to_target(path, target)
        text = read(path)
        budget = max_lines_for(relative, text, profile)
        count = len(text.splitlines())
        is_legacy = relative.startswith("docs/") and not is_project_memory_doc(relative, text)

        if budget and count > budget:
            if relative == "AGENTS.md":
                add(
                    items,
                    "migrate-agents",
                    relative,
                    f"{relative} has {count} lines; budget is {budget}.",
                    "Run migrate_agents.py to classify existing content. Keep AGENTS.md as a short router; move only stable current state or durable decisions into profile docs.",
                    "high",
                    ["AGENTS.md", "PROJECT_STATUS.md", "docs/DECISIONS.md"],
                )
            elif relative == "PROJECT_STATUS.md":
                add(
                    items,
                    "trim",
                    relative,
                    f"{relative} has {count} lines; budget is {budget}.",
                    "Keep current phase, latest conclusion, next action, blockers, active risks, and handoff. Move process history to agentmemory or sparse fallback LOG.",
                    "medium",
                    ["PROJECT_STATUS.md", "docs/LOG.md", "agentmemory"],
                )
            elif relative == "docs/LOG.md":
                add(
                    items,
                    "summarize-or-archive",
                    relative,
                    f"{relative} has {count} lines; budget is {budget}.",
                    "Summarize routine completed history. Prefer agentmemory for detailed process recall; keep only sparse checkpoints here.",
                    "medium",
                    ["docs/LOG.md", "agentmemory"],
                )
            elif relative == "docs/DECISIONS.md":
                add(
                    items,
                    "keep-with-index",
                    relative,
                    f"{relative} has {count} lines; budget is {budget}.",
                    "Do not delete decision rationale. Add or refresh a decision index and mark superseded decisions instead.",
                    "high",
                    ["docs/DECISIONS.md"],
                )
            elif relative in OPERATIONAL_FILES:
                add(
                    items,
                    "manual-review",
                    relative,
                    f"{relative} has {count} lines; budget is {budget}.",
                    "Operational context can be dangerous if over-compressed. Preserve current setup, branch, remote, and handoff details.",
                    "high",
                    [relative],
                    "Developer must confirm which operational details are stale before an agent patches this file.",
                )
            else:
                add(
                    items,
                    "summarize",
                    relative,
                    f"{relative} has {count} lines; budget is {budget}.",
                    "Preserve current facts, decisions, assumptions, open questions, and risks. Move stale detail to the correct source-of-truth file.",
                    "medium",
                    suggested_targets(relative, text),
                )
        elif is_legacy and count > legacy_budget(profile):
            targets = suggested_targets(relative, text)
            add(
                items,
                "legacy-migrate-or-archive",
                relative,
                f"{relative} has {count} lines; legacy doc budget is {legacy_budget(profile)}.",
                "Run migrate_context.py for this file, copy only stable summaries into the suggested target files, then archive or keep the original as a deep-reference document outside the default read path.",
                "medium",
                targets,
                "Developer must confirm whether to archive the original, keep it as deep reference, or leave it untouched.",
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
                ["PROJECT_STATUS.md", "docs/LOG.md"],
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
                ["docs/LOG.md", "docs/DECISIONS.md"],
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
                [relative],
                "Developer must confirm this file is safe to edit before an agent applies any compaction.",
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

    print("## Suggested Execution Order")
    print("1. Review `migrate-agents` and `source-of-truth-fix` items first; they affect always-on routing and ownership.")
    print("2. For `legacy-migrate-or-archive`, run `migrate_context.py --include <path>` and confirm which summaries should move.")
    print("3. Patch target project-memory files with stable summaries only after confirmation.")
    print("4. Archive or keep original legacy docs as deep references; do not delete originals without explicit confirmation.")
    print("5. Treat operational files as manual-review items even when they are long.\n")

    sections = [
        "trim",
        "migrate-agents",
        "legacy-migrate-or-archive",
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
            if item.suggested_targets:
                print("  Suggested targets: " + ", ".join(f"`{target}`" for target in item.suggested_targets))
            print(f"  Confirmation: {item.confirmation}")
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
