#!/usr/bin/env python3
"""Read-only project shape inspection for project-memory initialization."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11 fallback.
    tomllib = None  # type: ignore[assignment]


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


def read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def read_toml(path: Path) -> dict[str, Any]:
    if tomllib is None:
        return {}
    try:
        with path.open("rb") as handle:
            return tomllib.load(handle)
    except (FileNotFoundError, tomllib.TOMLDecodeError):
        return {}


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (FileNotFoundError, UnicodeDecodeError):
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
            timeout=8,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return []
    if proc.returncode != 0:
        return []
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def files_matching(target: Path, patterns: list[str]) -> list[str]:
    result: list[str] = []
    for pattern in patterns:
        result.extend(str(path.relative_to(target)) for path in target.glob(pattern) if path.is_file())
    return sorted(set(result))


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
    if (target / "docs").exists() or files_matching(target, ["**/*.md"]):
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
    if not addons:
        addons.add("system")
    return sorted(addons)


def project_name(target: Path) -> str:
    status = read_text(target / "PROJECT_STATUS.md")
    match = re.search(r"^-\s*Project:\s*`?([^`\n]+)`?\s*$", status, re.MULTILINE)
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
    return target.name


def inspect(target: Path) -> dict[str, object]:
    languages = detect_languages(target)
    interesting = [file for file in INTERESTING_FILES if (target / file).exists()]
    workflows = files_matching(target, [".github/workflows/*.yml", ".github/workflows/*.yaml"])
    scripts = {
        "package_json": package_scripts(target),
        "pyproject": python_scripts(target),
    }
    existing_memory = {
        "project_memory": (target / "PROJECT_STATUS.md").exists() or (target / "docs" / "PLAN.md").exists(),
        "projectmem": (target / ".projectmem").exists(),
        "conductor": (target / "conductor").exists(),
    }
    recommendations: list[str] = []
    repository_doc = read_text(target / "docs" / "REPOSITORY.md").lower()
    if existing_memory["conductor"] and not existing_memory["project_memory"]:
        recommendations.append(
            "Target contains conductor/. Confirm whether to keep Conductor as the static context source before initializing project-memory."
        )
    if not existing_memory["project_memory"]:
        recommendations.append("Initialize project-memory core docs, then fill current status and Vibe readiness.")
    if workflows and not any(marker in repository_doc for marker in ["ci:", "github actions", "workflow"]):
        recommendations.append("Record CI and release rules in docs/REPOSITORY.md.")
    if languages:
        recommendations.append("Record required/tested runtime versions in docs/VIBE_READINESS.md and docs/ENVIRONMENT.md.")

    return {
        "target": str(target),
        "project_name": project_name(target),
        "git": {
            "branch": "\n".join(git_lines(target, ["branch", "--show-current"])) or None,
            "remotes": git_lines(target, ["remote", "-v"]),
        },
        "languages": languages,
        "interesting_files": interesting,
        "workflows": workflows,
        "scripts": scripts,
        "existing_memory": existing_memory,
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

    for title, key in [
        ("Languages", "languages"),
        ("Interesting Files", "interesting_files"),
        ("GitHub Workflows", "workflows"),
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
