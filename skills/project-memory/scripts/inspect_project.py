#!/usr/bin/env python3
"""Read-only project shape inspection for AGENTS-first project-memory initialization."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from project_memory_lib import git_lines, git_pointer_issue, safe_read_json, safe_read_text, safe_read_toml


INTERESTING_FILES = [
    "README.md",
    "AGENTS.md",
    "SKILL.md",
    "package.json",
    "pyproject.toml",
    "requirements.txt",
    "Package.swift",
    "go.mod",
    "Cargo.toml",
    "Gemfile",
    "composer.json",
    "Dockerfile",
    "docker-compose.yml",
]

PROJECT_MEMORY_FILES = {
    "AGENTS.md",
    "PROJECT_STATUS.md",
    "docs/DECISIONS.md",
    "docs/ENVIRONMENT.md",
    "docs/LOG.md",
    "docs/COORDINATION.md",
}


def read_json(path: Path) -> dict[str, Any]:
    return safe_read_json(path)


def read_toml(path: Path) -> dict[str, Any]:
    return safe_read_toml(path)


def read_text(path: Path) -> str:
    return safe_read_text(path)


def files_matching(target: Path, patterns: list[str]) -> list[str]:
    result: list[str] = []
    for pattern in patterns:
        result.extend(str(path.relative_to(target)) for path in target.glob(pattern) if path.is_file())
    return sorted(set(result))


def legacy_context_sources(target: Path) -> list[str]:
    sources: list[str] = []
    for relative in ["AGENTS.md", "README.md", "TODO.md", "ROADMAP.md", "CHANGELOG.md"]:
        path = target / relative
        text = read_text(path)
        if (
            path.exists()
            and not (
                relative == "AGENTS.md"
                and ("Memory Metadata" in text or "Maintenance Rules" in text)
            )
        ):
            sources.append(relative)
    docs = target / "docs"
    if docs.exists():
        for path in sorted(docs.glob("*.md")):
            if not path.is_file():
                continue
            relative = str(path.relative_to(target))
            text = read_text(path)
            if (
                relative not in PROJECT_MEMORY_FILES
                and "Memory Metadata" not in text
                and "Maintenance Rules" not in text
            ):
                sources.append(relative)
    return sorted(set(sources))


def detect_languages(target: Path) -> list[str]:
    languages: set[str] = set()
    checks = {
        "python": ["pyproject.toml", "requirements.txt", "setup.py", "setup.cfg"],
        "node": ["package.json", "pnpm-lock.yaml", "package-lock.json", "yarn.lock", "bun.lockb"],
        "swift": ["Package.swift"],
        "go": ["go.mod"],
        "rust": ["Cargo.toml"],
        "ruby": ["Gemfile"],
        "php": ["composer.json"],
        "docker": ["Dockerfile", "docker-compose.yml"],
    }
    for language, files in checks.items():
        if any((target / file).exists() for file in files):
            languages.add(language)

    if files_matching(target, ["*.xcodeproj/project.pbxproj", "*.xcworkspace/contents.xcworkspacedata"]):
        languages.add("ios")
        languages.add("swift")
    if files_matching(target, ["**/*.ipynb"]):
        languages.add("data-ai")
    return sorted(languages)


def package_scripts(target: Path) -> dict[str, str]:
    package = read_json(target / "package.json")
    scripts = package.get("scripts", {})
    return scripts if isinstance(scripts, dict) else {}


def python_scripts(target: Path) -> dict[str, str]:
    pyproject = read_toml(target / "pyproject.toml")
    project = pyproject.get("project", {}) if isinstance(pyproject, dict) else {}
    scripts = project.get("scripts", {}) if isinstance(project, dict) else {}
    return scripts if isinstance(scripts, dict) else {}


def recommended_addons(target: Path, languages: list[str]) -> list[str]:
    addons: set[str] = set()
    package = read_json(target / "package.json")
    dependencies = {
        **package.get("dependencies", {}),
        **package.get("devDependencies", {}),
    } if package else {}
    dependency_text = " ".join(dependencies.keys()).lower()

    if (target / "SKILL.md").exists() or (target / "skills").exists():
        addons.add("skill")
    if (target / "docs").exists():
        addons.add("docs")
    if "node" in languages and any(name in dependency_text for name in ["react", "next", "vite", "vue", "svelte"]):
        addons.add("web")
        addons.add("app")
    if "ios" in languages:
        addons.add("ios")
        addons.add("app")
    if "python" in languages and (
        (target / "requirements.txt").exists()
        or "data-ai" in languages
        or any(name in dependency_text for name in ["tensorflow", "torch", "scikit"])
    ):
        if files_matching(target, ["**/*.ipynb", "**/notebooks/*.py"]):
            addons.add("data-ai")
    if python_scripts(target) or package.get("bin") or files_matching(target, ["bin/*"]):
        addons.add("cli")
    if (target / "Dockerfile").exists() or (target / ".github" / "workflows").exists():
        addons.add("cloud")
    if any((target / relative).exists() for relative in ["docs/HANDOFF.md", "docs/ROADMAP.md"]):
        addons.add("tracks")
    return sorted(addons)


def recommended_profile(target: Path) -> str:
    if (target / "docs" / "COORDINATION.md").exists() or (target / "docs" / "ENVIRONMENT.md").exists():
        return "governed"
    if (target / "PROJECT_STATUS.md").exists() or (target / "docs" / "DECISIONS.md").exists():
        return "standard"
    branch_count = len(git_lines(target, ["branch", "--format=%(refname:short)"]))
    has_setup = any((target / relative).exists() for relative in [
        "package.json",
        "pyproject.toml",
        "requirements.txt",
        "Package.swift",
        "go.mod",
        "Cargo.toml",
        "Dockerfile",
    ])
    if branch_count > 1 or has_setup and (target / ".github" / "workflows").exists():
        return "governed"
    if legacy_context_sources(target):
        return "standard"
    return "minimal"


def project_name(target: Path) -> str:
    status = read_text(target / "PROJECT_STATUS.md")
    match = re.search(r"^-\s*Project:\s*`?([^`\n]+)`?\s*$", status, re.MULTILINE)
    if match:
        return match.group(1).strip()
    agents = read_text(target / "AGENTS.md")
    match = re.search(r"^-\s*Name:\s*`?([^`\n]+)`?\s*$", agents, re.MULTILINE)
    if match:
        return match.group(1).strip()
    readme = read_text(target / "README.md")
    match = re.search(r"^#\s+(.+)$", readme, re.MULTILINE)
    if match:
        return match.group(1).strip()
    package = read_json(target / "package.json")
    if isinstance(package.get("name"), str):
        return package["name"]
    pyproject = read_toml(target / "pyproject.toml")
    project = pyproject.get("project", {}) if isinstance(pyproject, dict) else {}
    if isinstance(project, dict) and isinstance(project.get("name"), str):
        return project["name"]
    xcode_projects = sorted(target.glob("*.xcodeproj"))
    if len(xcode_projects) == 1:
        return xcode_projects[0].stem
    return target.name


def branch_name(target: Path) -> str | None:
    branch = "\n".join(git_lines(target, ["branch", "--show-current"]))
    if branch:
        return branch
    commit = "\n".join(git_lines(target, ["rev-parse", "--short", "HEAD"]))
    if commit:
        return f"detached:{commit}"
    return None


def inspect(target: Path) -> dict[str, object]:
    languages = detect_languages(target)
    interesting = [file for file in INTERESTING_FILES if (target / file).exists()]
    workflows = files_matching(target, [".github/workflows/*.yml", ".github/workflows/*.yaml"])
    legacy_sources = legacy_context_sources(target)
    scripts = {
        "package_json": package_scripts(target),
        "pyproject": python_scripts(target),
    }
    existing_memory = {
        "agents_router": (target / "AGENTS.md").exists(),
        "project_status": (target / "PROJECT_STATUS.md").exists(),
        "decisions": (target / "docs" / "DECISIONS.md").exists(),
        "legacy_context": bool(legacy_sources),
    }
    recommendations: list[str] = []
    profile = recommended_profile(target)
    if not existing_memory["agents_router"]:
        recommendations.append(f"Initialize project-memory with --profile {profile}; default minimal creates only AGENTS.md.")
    if legacy_sources:
        recommendations.append("Plan Existing Context Migration before copying stable rules/current state into AGENTS.md or standard docs.")
    if workflows:
        recommendations.append("Use governed profile if CI/release workflow needs stable environment or coordination notes.")
    if languages:
        recommendations.append("Keep runtime/version facts in AGENTS.md only if short; use governed ENVIRONMENT.md when setup becomes cross-device or fragile.")
    git_issue = git_pointer_issue(target)
    if git_issue:
        recommendations.append("Git metadata looks inconsistent: " + git_issue)

    return {
        "target": str(target),
        "project_name": project_name(target),
        "git": {
            "branch": branch_name(target),
            "remotes": git_lines(target, ["remote", "-v"]),
            "health": "warning: " + git_issue if git_issue else "ok",
        },
        "languages": languages,
        "interesting_files": interesting,
        "workflows": workflows,
        "legacy_context_sources": legacy_sources,
        "scripts": scripts,
        "existing_memory": existing_memory,
        "recommended_profile": profile,
        "recommended_addons": recommended_addons(target, languages),
        "recommendations": recommendations,
    }


def print_markdown(result: dict[str, object]) -> None:
    print("# Project Inspection\n")
    print(f"- Target: `{result['target']}`")
    print(f"- Project name: `{result['project_name']}`")

    git = result["git"]
    assert isinstance(git, dict)
    print(f"- Git branch: `{git.get('branch') or 'unknown'}`")
    print(f"- Git health: `{git.get('health') or 'unknown'}`")
    print(f"- Recommended profile: `{result['recommended_profile']}`")

    for title, key in [
        ("Languages", "languages"),
        ("Interesting Files", "interesting_files"),
        ("GitHub Workflows", "workflows"),
        ("Legacy Context Sources", "legacy_context_sources"),
        ("Recommended Addons", "recommended_addons"),
    ]:
        values = result[key]
        assert isinstance(values, list)
        if not values:
            continue
        print(f"\n## {title}")
        for value in values:
            print(f"- `{value}`")

    scripts = result["scripts"]
    assert isinstance(scripts, dict)
    if any(scripts.values()):
        print("\n## Candidate Commands")
        for group, commands in scripts.items():
            if not commands:
                continue
            assert isinstance(commands, dict)
            for name, command in commands.items():
                print(f"- `{group}:{name}`: `{command}`")

    memory = result["existing_memory"]
    assert isinstance(memory, dict)
    print("\n## Existing Memory Systems")
    for name, present in memory.items():
        print(f"- `{name}`: `{present}`")

    recommendations = result["recommendations"]
    assert isinstance(recommendations, list)
    if recommendations:
        print("\n## Recommendations")
        for item in recommendations:
            print(f"- {item}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect project shape before initializing memory docs.")
    parser.add_argument("--target", default=".", help="Project directory to inspect.")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    args = parser.parse_args()

    target = Path(args.target).expanduser().resolve()
    result = inspect(target)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_markdown(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
