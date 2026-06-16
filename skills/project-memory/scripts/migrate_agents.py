#!/usr/bin/env python3
"""Read-only AGENTS.md migration planner."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


AGENTS_BUDGET = 140

TARGET_RULES = [
    (
        "docs/VIBE_READINESS.md",
        [
            "permission",
            "boundary",
            "red line",
            "forbidden",
            "must ask",
            "confirm",
            "review required",
            "security",
            "performance",
            "privacy",
            "api key",
            "api keys",
            "secret",
            "secrets",
            "credential",
            "credentials",
            "hard-code",
            "hardcode",
            "ai may",
            "ai must",
            "权限",
            "红线",
            "确认",
            "审核",
            "禁止",
        ],
    ),
    (
        "docs/ENVIRONMENT.md",
        [
            "environment",
            "setup",
            "install",
            "dependency",
            "version",
            "python",
            "node",
            "xcode",
            "path",
            "env var",
            "环境",
            "依赖",
            "版本",
            "路径",
        ],
    ),
    (
        "docs/REPOSITORY.md",
        [
            "git",
            "github",
            "branch",
            "commit",
            "pr",
            "pull request",
            "remote",
            "release",
            "tag",
            "仓库",
            "分支",
            "提交",
        ],
    ),
    (
        "docs/COORDINATION.md",
        [
            "handoff",
            "coordination",
            "workstream",
            "parallel",
            "session",
            "agent",
            "owner",
            "交接",
            "分工",
            "并行",
            "会话",
        ],
    ),
    (
        "docs/DECISIONS.md",
        [
            "decision",
            "decided",
            "rationale",
            "alternative",
            "tradeoff",
            "choose",
            "选择",
            "决策",
            "取舍",
            "原因",
        ],
    ),
    (
        "docs/DOMAIN.md",
        [
            "domain",
            "business",
            "terminology",
            "user mental",
            "workflow",
            "业务",
            "领域",
            "术语",
            "用户",
        ],
    ),
    (
        "docs/PLAN.md",
        [
            "plan",
            "roadmap",
            "milestone",
            "scope",
            "next",
            "todo",
            "计划",
            "路线",
            "范围",
            "下一步",
        ],
    ),
    (
        "docs/PRINCIPLES.md",
        [
            "principle",
            "rule",
            "always",
            "never",
            "prefer",
            "avoid",
            "准则",
            "规则",
            "必须",
            "不要",
        ],
    ),
    (
        "docs/LOG.md",
        [
            "log",
            "progress",
            "history",
            "completed",
            "记录",
            "进展",
            "历史",
            "完成",
        ],
    ),
    (
        "docs/CONTEXT.md",
        [
            "context",
            "background",
            "goal",
            "problem",
            "audience",
            "背景",
            "目标",
            "问题",
        ],
    ),
]

KEEP_KEYWORDS = [
    "default read order",
    "task-based read paths",
    "source of truth",
    "update triggers",
    "context budget warnings",
    "project context",
    "read ",
    "read `",
    "before starting",
    "operating rules",
    "update project memory",
    "do not compact",
    "do not delete",
    "source of truth",
    "maintenance rules",
    "开始工作",
    "先读",
    "更新",
    "不要压缩",
    "不要删除",
]

KEEP_HEADINGS = {
    "# agent operating rules",
    "## memory metadata",
    "## maintenance rules",
    "## default read order",
    "## task-based read paths",
    "## source of truth",
    "## update triggers",
    "## context budget warnings",
    "## project context",
}

STANDARD_SECTION_MAX_LINES = {
    "# agent operating rules": 3,
    "## memory metadata": 7,
    "## maintenance rules": 7,
    "## default read order": 12,
    "## task-based read paths": 12,
    "## source of truth": 14,
    "## update triggers": 10,
    "## context budget warnings": 8,
    "## project context": 8,
}


@dataclass
class MigrationItem:
    action: str
    target: str
    reason: str
    excerpt: str


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def chunks(text: str) -> list[str]:
    lines = text.splitlines()
    result: list[list[str]] = []
    current: list[str] = []

    for line in lines:
        if line.startswith("#") and current:
            result.append(current)
            current = [line]
        elif not line.strip() and current and len(current) > 8:
            result.append(current)
            current = []
        else:
            current.append(line)

    if current:
        result.append(current)

    expanded: list[str] = []
    for chunk in result:
        first_line = chunk[0].strip().lower() if chunk else ""
        max_lines = STANDARD_SECTION_MAX_LINES.get(first_line)
        if max_lines and len(chunk) > max_lines:
            expanded.append("\n".join(chunk[:max_lines]).strip())
            tail = chunk[max_lines:]
            for index in range(0, len(tail), 12):
                expanded.append("\n".join(tail[index : index + 12]).strip())
        else:
            expanded.append("\n".join(chunk).strip())

    return [chunk for chunk in expanded if chunk]


def score(text: str, keywords: list[str]) -> int:
    lowered = text.lower()
    return sum(1 for keyword in keywords if keyword in lowered)


def classify(chunk: str) -> MigrationItem:
    cleaned = " ".join(chunk.split())
    excerpt = cleaned[:180] + ("..." if len(cleaned) > 180 else "")
    lines = chunk.splitlines()
    first_line = lines[0].strip().lower() if lines else ""

    if first_line in KEEP_HEADINGS:
        return MigrationItem(
            "keep",
            "AGENTS.md",
            "Standard AGENTS.md router section.",
            excerpt,
        )

    if (
        first_line.startswith("#")
        and len(lines) <= AGENTS_BUDGET
        and any(marker in first_line for marker in ["agent", "codex", "instruction", "instructions"])
    ):
        return MigrationItem(
            "keep",
            "AGENTS.md",
            "Short agent operating instruction block should remain always-on context.",
            excerpt,
        )

    keep_score = score(chunk, KEEP_KEYWORDS)
    target_scores = [(target, score(chunk, keywords)) for target, keywords in TARGET_RULES]
    target, target_score = max(target_scores, key=lambda item: item[1])

    if keep_score >= 2 and target_score <= keep_score:
        return MigrationItem(
            "keep",
            "AGENTS.md",
            "Looks like always-on routing or operating rules.",
            excerpt,
        )

    if target_score > 0:
        return MigrationItem(
            "move",
            target,
            "Content appears to belong to a source-of-truth project memory doc.",
            excerpt,
        )

    if chunk.startswith("#"):
        return MigrationItem(
            "keep",
            "AGENTS.md",
            "Top-level heading or short operating context.",
            excerpt,
        )

    return MigrationItem(
        "review",
        "developer-review",
        "Could not confidently classify this content.",
        excerpt,
    )


def plan(target: Path) -> list[MigrationItem]:
    agents = target / "AGENTS.md"
    text = read(agents)
    if not text:
        return [
            MigrationItem(
                "missing",
                "AGENTS.md",
                "No AGENTS.md file was found.",
                "Run init_docs.py to create one or skip migration.",
            )
        ]

    items = [classify(chunk) for chunk in chunks(text)]
    line_count = len(text.splitlines())
    if line_count > AGENTS_BUDGET:
        items.insert(
            0,
            MigrationItem(
                "migrate-recommended",
                "AGENTS.md",
                f"AGENTS.md has {line_count} lines; budget is {AGENTS_BUDGET}.",
                "Prefer a short AGENTS.md router and move detailed context into docs/.",
            ),
        )
    return items


def print_markdown(items: list[MigrationItem]) -> None:
    print("# AGENTS.md Migration Plan\n")
    print("- Mode: read-only strategy; no files were modified")
    print("- Requirement: developer confirmation is required before applying migration")
    print("- Goal: keep AGENTS.md short and move detailed project memory to docs/\n")

    order = ["migrate-recommended", "keep", "move", "review", "missing"]
    for action in order:
        matching = [item for item in items if item.action == action]
        if not matching:
            continue
        print(f"## {action}")
        for item in matching:
            print(f"- Target: `{item.target}`")
            print(f"  Reason: {item.reason}")
            print(f"  Excerpt: {item.excerpt}")
        print()


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a read-only AGENTS.md migration plan.")
    parser.add_argument("--target", default=".", help="Project directory to inspect.")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    args = parser.parse_args()

    target = Path(args.target).expanduser().resolve()
    items = plan(target)

    if args.json:
        print(json.dumps([asdict(item) for item in items], indent=2))
    else:
        print_markdown(items)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
