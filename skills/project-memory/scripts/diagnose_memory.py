#!/usr/bin/env python3
"""Read-only health diagnosis for AGENTS-first project memory routing."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path


PROFILE_FILES = {
    "minimal": [
        "AGENTS.md",
    ],
    "standard": [
        "AGENTS.md",
        "PROJECT_STATUS.md",
        "docs/DECISIONS.md",
    ],
    "governed": [
        "AGENTS.md",
        "PROJECT_STATUS.md",
        "docs/DECISIONS.md",
        "docs/ENVIRONMENT.md",
        "docs/COORDINATION.md",
    ],
}

CORE_FILES = sorted({item for files in PROFILE_FILES.values() for item in files} | {"docs/LOG.md"})

DEFAULT_BUDGETS = {
    "AGENTS.md": 90,
    "PROJECT_STATUS.md": 90,
    "docs/TRACKS.md": 260,
    "docs/DECISIONS.md": 350,
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

DEPENDENCY_AND_SETUP_FILES = [
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "bun.lockb",
    "pyproject.toml",
    "requirements.txt",
    "poetry.lock",
    "uv.lock",
    "Cargo.toml",
    "Cargo.lock",
    "Package.swift",
    "go.mod",
    "go.sum",
    "Gemfile",
    "Gemfile.lock",
    "composer.json",
    "Dockerfile",
    "docker-compose.yml",
]


@dataclass
class Finding:
    severity: str
    code: str
    path: str
    message: str
    recommendation: str


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


def git_date_for_path(target: Path, relative: str) -> dt.date | None:
    lines = git_lines(target, ["log", "-1", "--format=%cs", "--", relative])
    if not lines:
        return None
    try:
        return dt.date.fromisoformat(lines[0])
    except ValueError:
        return None


def add(
    findings: list[Finding],
    severity: str,
    code: str,
    path: str,
    message: str,
    recommendation: str,
) -> None:
    findings.append(Finding(severity, code, path, message, recommendation))


def memory_files(target: Path) -> list[Path]:
    files: list[Path] = []
    for relative in ["AGENTS.md", "PROJECT_STATUS.md"]:
        path = target / relative
        if path.exists():
            files.append(path)
    docs = target / "docs"
    if docs.exists():
        for path in sorted(docs.glob("*.md")):
            if not path.is_file():
                continue
            relative = str(path.relative_to(target))
            text = read(path)
            if (
                relative in CORE_FILES
                or relative in OPTIONAL_PROJECT_MEMORY_FILES
                or "Memory Metadata" in text
                or "Maintenance Rules" in text
            ):
                files.append(path)
    return files


def legacy_context_files(target: Path) -> list[str]:
    docs = target / "docs"
    if not docs.exists():
        return []
    memory = {relative_to_target(path, target) for path in memory_files(target)}
    legacy: list[str] = []
    for path in sorted(docs.glob("*.md")):
        if not path.is_file():
            continue
        relative = relative_to_target(path, target)
        if relative not in memory:
            legacy.append(relative)
    return legacy


def relative_to_target(path: Path, target: Path) -> str:
    return str(path.relative_to(target))


def max_lines_for(relative: str, text: str) -> int | None:
    match = re.search(r"^\s*-\s*max_lines:\s*(\d+)\s*$", text, re.MULTILINE)
    if match:
        return int(match.group(1))
    return DEFAULT_BUDGETS.get(relative)


def review_dates(text: str) -> list[dt.date]:
    matches = re.findall(
        r"Date:\s*(\d{4}-\d{2}-\d{2})|Last reviewed:\s*(\d{4}-\d{2}-\d{2})",
        text,
        re.I,
    )
    dates: list[dt.date] = []
    for first, second in matches:
        value = first or second
        if not value:
            continue
        try:
            dates.append(dt.date.fromisoformat(value))
        except ValueError:
            continue
    return dates


def status_field(status_text: str, name: str) -> str:
    match = re.search(rf"^-\s*{re.escape(name)}:\s*(.+)$", status_text, re.MULTILINE)
    return match.group(1).strip() if match else ""


def detect_profile(target: Path) -> str:
    agents = read(target / "AGENTS.md")
    match = re.search(r"^-\s*Profile:\s*(minimal|standard|governed)\s*$", agents, re.MULTILINE)
    if match:
        return match.group(1)
    if (target / "docs/ENVIRONMENT.md").exists() or (target / "docs/COORDINATION.md").exists():
        return "governed"
    if (target / "PROJECT_STATUS.md").exists() or (target / "docs/DECISIONS.md").exists():
        return "standard"
    return "minimal"


def dynamic_memory_mode(target: Path) -> str:
    agents = read(target / "AGENTS.md")
    match = re.search(r"^-\s*Dynamic memory:\s*(agentmemory|none)\s*$", agents, re.MULTILINE)
    if match:
        return match.group(1)
    lowered = agents.lower()
    if "agentmemory" in lowered:
        return "agentmemory"
    if "dynamic memory: none" in lowered:
        return "none"
    return "unknown"


def is_placeholder(value: str) -> bool:
    normalized = value.strip().strip("`").lower()
    return normalized in {
        "",
        "tbd",
        "todo",
        "unknown",
        "none",
        "none recorded",
        "not recorded",
        "n/a",
        "-",
    }


def parse_date(value: str) -> dt.date | None:
    try:
        return dt.date.fromisoformat(value.strip())
    except ValueError:
        return None


def markdown_table_rows(text: str, headers: list[str]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    expected = [header.lower() for header in headers]
    lines = text.splitlines()
    for index, line in enumerate(lines):
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if [cell.lower() for cell in cells] != expected:
            continue
        for row_line in lines[index + 2 :]:
            if not row_line.strip().startswith("|"):
                break
            row_cells = [cell.strip() for cell in row_line.strip().strip("|").split("|")]
            if len(row_cells) != len(headers):
                continue
            rows.append(dict(zip(expected, row_cells)))
        break
    return rows


def track_rows(tracks_text: str) -> list[dict[str, str]]:
    return markdown_table_rows(
        tracks_text,
        [
            "ID",
            "Status",
            "Priority",
            "Owner",
            "Scope",
            "Spec",
            "Plan",
            "Last Updated",
            "Next Step",
        ],
    )


def tracked_dependency_files(target: Path) -> list[str]:
    files: set[str] = set()
    for relative in DEPENDENCY_AND_SETUP_FILES:
        if (target / relative).exists():
            files.add(relative)
    workflows = target / ".github" / "workflows"
    if workflows.exists():
        for path in workflows.glob("*.y*ml"):
            if path.is_file():
                files.add(str(path.relative_to(target)))
    return sorted(files)


def diagnose(target: Path, *, context_gate: bool = False) -> list[Finding]:
    findings: list[Finding] = []
    over_budget = False
    profile = detect_profile(target)
    dynamic_memory = dynamic_memory_mode(target)

    for relative in PROFILE_FILES[profile]:
        path = target / relative
        if not path.exists():
            add(
                findings,
                "error",
                "missing-core-file",
                relative,
                f"Required `{profile}` profile file is missing.",
                f"Run init_docs.py --profile {profile} or restore the file from templates.",
            )

    legacy_docs = legacy_context_files(target)
    if legacy_docs:
        add(
            findings,
            "info",
            "legacy-context-docs-detected",
            "docs",
            f"Found {len(legacy_docs)} existing Markdown doc(s) that are not project-memory docs.",
            "Treat them as Existing Context Migration sources instead of adding Memory Metadata to every legacy file: "
            + ", ".join(legacy_docs[:6]),
        )

    for path in memory_files(target):
        relative = relative_to_target(path, target)
        text = read(path)
        if "Memory Metadata" not in text:
            add(
                findings,
                "warning",
                "missing-memory-metadata",
                relative,
                "Project memory file lacks a Memory Metadata section.",
                "Add owner, read_when, update_when, max_lines, and stale_if metadata.",
            )
        has_maintenance = "Maintenance Rules" in text or (
            relative == "AGENTS.md"
            and "Memory Ownership" in text
            and "Checkpoint Rules" in text
        )
        if not has_maintenance:
            add(
                findings,
                "warning",
                "missing-maintenance-rules",
                relative,
                "Markdown file lacks a Maintenance Rules section.",
                "Add update triggers, source-of-truth scope, and exclusions.",
            )
        budget = max_lines_for(relative, text)
        line_count = len(text.splitlines())
        if budget and line_count > budget:
            over_budget = True
            if relative == "AGENTS.md":
                add(
                    findings,
                    "warning",
                    "agents-migration-recommended",
                    relative,
                    f"{relative} has {line_count} lines; budget is {budget}.",
                    "Recommend trimming AGENTS.md into a short router or upgrading profile; do not turn it into a project memory warehouse.",
                )
                continue
            add(
                findings,
                "warning",
                "context-budget-exceeded",
                relative,
                f"{relative} has {line_count} lines; budget is {budget}.",
                "Recommend running compact to generate a developer-confirmed compaction plan.",
            )

    agents_text = read(target / "AGENTS.md")
    lowered_agents = agents_text.lower()
    if agents_text:
        if "critical:" not in lowered_agents or "context routing" not in lowered_agents:
            add(
                findings,
                "warning",
                "agents-router-contract-missing",
                "AGENTS.md",
                "AGENTS.md does not clearly present the always-on router contract.",
                "Keep a first-screen context acknowledgement and task-based routing section in AGENTS.md.",
            )
        if dynamic_memory == "unknown":
            add(
                findings,
                "warning",
                "dynamic-memory-routing-missing",
                "AGENTS.md",
                "AGENTS.md does not declare whether agentmemory or no dynamic memory is used.",
                "Record `Dynamic memory: agentmemory` or `Dynamic memory: none` and the ownership split.",
            )
        if dynamic_memory == "agentmemory" and "attempts" not in lowered_agents:
            add(
                findings,
                "warning",
                "agentmemory-ownership-incomplete",
                "AGENTS.md",
                "agentmemory is named but its ownership boundary is not explicit.",
                "Document that agentmemory owns attempts, failures, debug traces, file-level gotchas, and session continuity.",
            )
        if re.search(r"^##\s+\d{4}-\d{2}-\d{2}", agents_text, re.MULTILINE):
            add(
                findings,
                "warning",
                "agents-contains-history",
                "AGENTS.md",
                "AGENTS.md appears to contain dated historical sections.",
                "Move history to agentmemory or sparse fallback LOG; keep AGENTS.md as the always-on router.",
            )

    agents_line_count = len(agents_text.splitlines())
    if profile == "minimal" and (
        agents_line_count > DEFAULT_BUDGETS["AGENTS.md"]
        or re.search(r"Current phase:|Next step:|Decision:", agents_text)
    ):
        add(
            findings,
            "action",
            "profile-upgrade-recommended",
            "AGENTS.md",
            "Minimal profile appears to be carrying current status or durable decision content.",
            "Recommend upgrading to standard after developer confirmation: add PROJECT_STATUS.md and docs/DECISIONS.md.",
        )

    status_text = read(target / "PROJECT_STATUS.md")
    if re.search(r"^##\s+\d{4}-\d{2}-\d{2}", status_text, re.MULTILINE):
        add(
            findings,
            "warning",
            "status-contains-history",
            "PROJECT_STATUS.md",
            "PROJECT_STATUS.md appears to contain dated historical sections.",
            "Keep current state here and move historical detail to docs/LOG.md.",
        )
    if context_gate and (profile != "minimal" or status_text):
        for field in ["Current phase", "Latest conclusion", "Next step"]:
            value = status_field(status_text, field)
            if is_placeholder(value):
                add(
                    findings,
                    "warning",
                    "gate-status-field-missing",
                    "PROJECT_STATUS.md",
                    f"Context Gate requires a current `{field}` value.",
                    "Update PROJECT_STATUS.md before broad implementation so future sessions have a clear starting point.",
                )

    log_text = read(target / "docs/LOG.md")
    if re.search(r"^\s*-\s*Decision:", log_text, re.MULTILINE | re.IGNORECASE):
        add(
            findings,
            "warning",
            "decision-in-log",
            "docs/LOG.md",
            "LOG.md appears to contain a durable decision entry.",
            "Copy durable decisions and rationale into docs/DECISIONS.md.",
        )
    if log_text and dynamic_memory == "agentmemory" and len(log_text.splitlines()) > 80:
        add(
            findings,
            "warning",
            "log-overused-with-agentmemory",
            "docs/LOG.md",
            "LOG.md is sizable even though agentmemory is the declared dynamic memory tool.",
            "Keep LOG as sparse fallback only; move ordinary process history to agentmemory.",
        )

    tracks_text = read(target / "docs/TRACKS.md")
    if tracks_text:
        today = dt.date.today()
        for row in track_rows(tracks_text):
            track_id = row.get("id", "")
            status = row.get("status", "").strip().lower()
            if track_id.strip().lower() == "tbd":
                add(
                    findings,
                    "info",
                    "tracks-placeholder",
                    "docs/TRACKS.md",
                    "TRACKS.md still contains the template placeholder row.",
                    "Replace the placeholder with real feature tracks or remove the row until tracks are needed.",
                )
                continue
            if status not in {"active", "blocked"}:
                continue
            updated = parse_date(row.get("last updated", ""))
            if not updated:
                add(
                    findings,
                    "warning",
                    "track-date-invalid",
                    "docs/TRACKS.md",
                    f"Active track `{track_id}` lacks a valid ISO Last Updated date.",
                    "Use YYYY-MM-DD so stale track detection remains reliable.",
                )
            elif (today - updated).days > 30:
                add(
                    findings,
                    "warning",
                    "track-stale",
                    "docs/TRACKS.md",
                    f"Active track `{track_id}` was last updated {(today - updated).days} days ago.",
                    "Review the track plan or mark it paused/done if it is no longer active.",
                )
            if context_gate and is_placeholder(row.get("next step", "")):
                add(
                    findings,
                    "warning",
                    "gate-track-next-step-missing",
                    "docs/TRACKS.md",
                    f"Active track `{track_id}` has no concrete next step.",
                    "Fill the next step before starting broad work on this track.",
                )

    for relative in ["docs/ENVIRONMENT.md", "docs/COORDINATION.md"]:
        path = target / relative
        text = read(path)
        dates = review_dates(text)
        if dates:
            latest = max(dates)
            age = (dt.date.today() - latest).days
            if age > 60:
                add(
                    findings,
                    "warning",
                    "stale-review-date",
                    relative,
                    f"Last review date appears {age} days old.",
                    "Review this file if setup, repository, or coordination context may have changed.",
                )

    env = read(target / "docs/ENVIRONMENT.md")
    if env and "TBD" in env:
        add(
            findings,
            "info",
            "environment-placeholders",
            "docs/ENVIRONMENT.md",
            "Environment doc still contains TBD placeholders.",
            "Fill required tools, dependencies, and machine-specific notes when setup work begins.",
        )

    env_dates = review_dates(env)
    env_latest = max(env_dates) if env_dates else None
    changed_setup_files: list[str] = []
    for relative in tracked_dependency_files(target):
        changed = git_date_for_path(target, relative)
        if changed and env_latest and changed > env_latest:
            changed_setup_files.append(relative)
    if changed_setup_files:
        add(
            findings,
            "warning",
            "environment-may-be-stale",
            "docs/ENVIRONMENT.md",
            "Setup or dependency files changed after the last recorded environment review.",
            "Review environment notes for: " + ", ".join(changed_setup_files[:6]),
        )

    branch = "\n".join(git_lines(target, ["branch", "--show-current"]))
    if branch and "Current branch: TBD" in status_text:
        add(
            findings,
            "info",
            "status-branch-placeholder",
            "PROJECT_STATUS.md",
            "Git branch is available but PROJECT_STATUS.md still lists current branch as TBD.",
            "Record the active branch when branch context matters.",
        )

    branches = git_lines(target, ["branch", "--format=%(refname:short)"])
    coordination = read(target / "docs/COORDINATION.md")
    if len(branches) > 1 and "Status: not active" in coordination:
        add(
            findings,
            "warning",
            "coordination-may-need-activation",
            "docs/COORDINATION.md",
            f"Repository has {len(branches)} local branches but coordination is not active.",
            "Activate coordination if branches represent parallel workstreams.",
        )

    if dynamic_memory == "agentmemory" and not shutil.which("agentmemory"):
        add(
            findings,
            "info",
            "agentmemory-not-on-path",
            "AGENTS.md",
            "AGENTS.md recommends agentmemory but the `agentmemory` CLI is not on PATH.",
            "Install/connect agentmemory separately, or set Dynamic memory to none and use sparse LOG fallback.",
        )

    if profile == "standard":
        upgrade_reasons: list[str] = []
        if len(branches) > 1:
            upgrade_reasons.append(f"{len(branches)} local branches")
        if tracked_dependency_files(target) and not (target / "docs/ENVIRONMENT.md").exists():
            upgrade_reasons.append("setup/dependency files exist")
        if upgrade_reasons:
            add(
                findings,
                "action",
                "profile-upgrade-recommended",
                "project-memory",
                "Standard profile may need governed coordination/environment docs: " + ", ".join(upgrade_reasons),
                "Recommend upgrading to governed after developer confirmation if these signals represent ongoing complexity.",
            )

    porcelain = git_lines(target, ["status", "--short"])
    if porcelain and (target / "PROJECT_STATUS.md").exists():
        add(
            findings,
            "info",
            "working-tree-has-changes",
            "PROJECT_STATUS.md",
            "Working tree has uncommitted changes.",
            "Ensure project memory reflects meaningful in-progress work before handoff.",
        )

    if over_budget:
        add(
            findings,
            "action",
            "compact-recommended",
            "project-memory",
            "One or more project memory docs exceed their context budget.",
            "Ask the developer whether to run compact or migrate-agents; do not modify memory automatically.",
        )

    return findings


def print_markdown(findings: list[Finding]) -> None:
    if not findings:
        print("# Project Memory Diagnosis\n\nNo issues found.")
        return
    print("# Project Memory Diagnosis\n")
    for finding in findings:
        print(f"## [{finding.severity.upper()}] {finding.code}")
        print(f"- Path: `{finding.path}`")
        print(f"- Finding: {finding.message}")
        print(f"- Recommendation: {finding.recommendation}\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Diagnose project memory docs.")
    parser.add_argument("--target", default=".", help="Project directory to diagnose.")
    parser.add_argument(
        "--context-gate",
        action="store_true",
        help="Add stricter readiness checks for broad implementation or feature-track work.",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    args = parser.parse_args()

    target = Path(args.target).expanduser().resolve()
    findings = diagnose(target, context_gate=args.context_gate)

    if args.json:
        print(json.dumps([asdict(item) for item in findings], indent=2))
    else:
        print_markdown(findings)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
