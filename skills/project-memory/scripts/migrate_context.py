#!/usr/bin/env python3
"""Read-only existing-context migration planner for brownfield projects."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


PROJECT_MEMORY_FILES = {
    "AGENTS.md",
    "PROJECT_STATUS.md",
    "docs/DECISIONS.md",
    "docs/ENVIRONMENT.md",
    "docs/LOG.md",
    "docs/COORDINATION.md",
    "docs/TRACKS.md",
}

ROOT_CANDIDATES = [
    "AGENTS.md",
    "README.md",
    "TODO.md",
    "ROADMAP.md",
    "CHANGELOG.md",
]

FILENAME_HINTS = [
    (re.compile(r"agents?", re.I), ["AGENTS.md"], "agent operating rules"),
    (re.compile(r"handoff|coordination", re.I), ["PROJECT_STATUS.md", "docs/COORDINATION.md"], "handoff/current coordination"),
    (re.compile(r"roadmap|plan|todo", re.I), ["PROJECT_STATUS.md"], "roadmap or planned work"),
    (re.compile(r"context|background|overview", re.I), ["AGENTS.md", "docs/DECISIONS.md"], "project context and rationale"),
    (re.compile(r"decision|adr|rationale", re.I), ["docs/DECISIONS.md"], "durable decisions"),
    (re.compile(r"setup|environment|device|xcode|build", re.I), ["docs/ENVIRONMENT.md"], "setup/build/device context"),
    (re.compile(r"repository|github|git|release|ci", re.I), ["docs/COORDINATION.md", "docs/ENVIRONMENT.md"], "repository workflow"),
    (re.compile(r"validation|test|qa|checklist", re.I), ["AGENTS.md", "PROJECT_STATUS.md"], "validation and readiness"),
    (re.compile(r"domain|algorithm|color|palette|mard|business|terminology", re.I), ["docs/DOMAIN.md", "docs/DECISIONS.md"], "domain or algorithm facts"),
    (re.compile(r"changelog|history|log", re.I), ["docs/LOG.md"], "chronological history"),
]

CONTENT_HINTS = [
    ("PROJECT_STATUS.md", ["current state", "current baseline", "active branch", "next step", "blocker", "当前"]),
    ("AGENTS.md", ["goal", "problem", "background", "overview", "product goal", "known facts", "red line", "validation", "security", "privacy", "目标", "背景"]),
    ("PROJECT_STATUS.md", ["roadmap", "milestone", "phase", "planned order", "next priority", "scope", "current state", "next step", "计划", "路线"]),
    ("docs/DECISIONS.md", ["decision", "accepted", "rejected", "rationale", "alternative", "tradeoff", "决定", "拒绝"]),
    ("docs/ENVIRONMENT.md", ["setup", "xcode", "install", "device", "simulator", "dependency", "path", "环境"]),
    ("docs/COORDINATION.md", ["git", "github", "branch", "commit", "push", "release", "ci", "handoff", "coordination", "仓库", "分支"]),
    ("docs/COORDINATION.md", ["handoff", "coordination", "specialist", "parallel", "owner", "交接", "并行"]),
    ("docs/LOG.md", ["updated", "last updated", "completed", "merged", "history", "progress", "记录"]),
    ("docs/DOMAIN.md", ["domain", "algorithm", "palette", "mard", "user workflow", "terminology", "业务", "算法"]),
]


@dataclass
class MigrationItem:
    source: str
    line_count: int
    suggested_targets: list[str]
    action: str
    rationale: str
    excerpt: str


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (FileNotFoundError, UnicodeDecodeError):
        return ""


def relative(path: Path, target: Path) -> str:
    return str(path.relative_to(target))


def is_project_memory_doc(path: Path, target: Path) -> bool:
    rel = relative(path, target)
    text = read(path)
    if rel == "AGENTS.md":
        return "Memory Metadata" in text or "Maintenance Rules" in text
    return (
        rel in PROJECT_MEMORY_FILES
        or "Memory Metadata" in text
        or "Maintenance Rules" in text
    )


def default_sources(target: Path) -> list[Path]:
    sources: list[Path] = []
    for candidate in ROOT_CANDIDATES:
        path = target / candidate
        if path.is_file() and not is_project_memory_doc(path, target):
            sources.append(path)

    docs = target / "docs"
    if docs.exists():
        for path in sorted(docs.glob("*.md")):
            if path.is_file() and not is_project_memory_doc(path, target):
                sources.append(path)

    return sorted({path.resolve() for path in sources})


def explicit_sources(target: Path, includes: list[str]) -> list[Path]:
    result: list[Path] = []
    for item in includes:
        path = (target / item).resolve() if not Path(item).is_absolute() else Path(item).resolve()
        if path.is_file():
            result.append(path)
    return sorted({path for path in result})


def score_targets(text: str) -> dict[str, int]:
    lowered = text.lower()
    scores: dict[str, int] = {}
    for target, keywords in CONTENT_HINTS:
        score = sum(1 for keyword in keywords if keyword.lower() in lowered)
        if score:
            scores[target] = score
    return scores


def classify(path: Path, target: Path, max_excerpt: int) -> MigrationItem:
    rel = relative(path, target)
    text = read(path)
    line_count = len(text.splitlines())
    excerpt = " ".join(text.split())[:max_excerpt]
    if len(" ".join(text.split())) > max_excerpt:
        excerpt += "..."

    if rel == "AGENTS.md" and line_count <= 140:
        return MigrationItem(
            source=rel,
            line_count=line_count,
            suggested_targets=["AGENTS.md"],
            action="keep-or-trim",
            rationale="short AGENTS.md should remain always-on operating context",
            excerpt=excerpt,
        )

    suggested: list[str] = []
    rationale_parts: list[str] = []

    for pattern, targets, rationale in FILENAME_HINTS:
        if pattern.search(path.name):
            for item in targets:
                if item not in suggested:
                    suggested.append(item)
            rationale_parts.append(f"filename suggests {rationale}")

    scores = score_targets(text)
    for item, _score in sorted(scores.items(), key=lambda pair: (-pair[1], pair[0]))[:4]:
        if item not in suggested:
            suggested.append(item)
    if scores:
        rationale_parts.append("content keywords suggest " + ", ".join(sorted(scores)[:4]))

    if rel == "AGENTS.md" and "AGENTS.md" not in suggested:
        suggested.insert(0, "AGENTS.md")
    if not suggested:
        suggested = ["developer-review"]
        action = "review"
        rationale_parts.append("no confident target")
    elif rel == "AGENTS.md":
        action = "keep-or-trim"
    elif len(suggested) == 1:
        action = "migrate-summary"
    else:
        action = "split-summary"

    return MigrationItem(
        source=rel,
        line_count=line_count,
        suggested_targets=suggested,
        action=action,
        rationale="; ".join(rationale_parts),
        excerpt=excerpt,
    )


def plan(target: Path, includes: list[str], max_excerpt: int) -> list[MigrationItem]:
    sources = explicit_sources(target, includes) if includes else default_sources(target)
    return [classify(path, target, max_excerpt) for path in sources]


def print_markdown(items: list[MigrationItem]) -> None:
    print("# Existing Context Migration Plan\n")
    print("- Mode: read-only strategy; no files were modified")
    print("- Scope: generic brownfield context classification into AGENTS-first profile files")
    print("- Non-goal: no dynamic memory import, full history preservation, or third-party context compatibility")
    print("- Requirement: developer confirmation is required before applying migration\n")

    if not items:
        print("No legacy context sources found.")
        return

    for item in items:
        print(f"## `{item.source}`")
        print(f"- Lines: {item.line_count}")
        print(f"- Action: `{item.action}`")
        print("- Suggested targets: " + ", ".join(f"`{target}`" for target in item.suggested_targets))
        print(f"- Rationale: {item.rationale}")
        print(f"- Excerpt: {item.excerpt}\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a read-only existing-context migration plan.")
    parser.add_argument("--target", default=".", help="Project directory to inspect.")
    parser.add_argument(
        "--include",
        nargs="*",
        default=[],
        help="Optional explicit files to classify. Defaults to root context docs and legacy docs/*.md.",
    )
    parser.add_argument("--max-excerpt", type=int, default=220, help="Maximum excerpt characters per source.")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    args = parser.parse_args()

    target = Path(args.target).expanduser().resolve()
    items = plan(target, args.include, max(80, args.max_excerpt))
    if args.json:
        print(json.dumps([asdict(item) for item in items], indent=2))
    else:
        print_markdown(items)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
