#!/usr/bin/env python3
"""Small shared helpers for project-memory scripts."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11 fallback.
    tomllib = None  # type: ignore[assignment]


def safe_read_text(path: Path, default: str = "") -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (FileNotFoundError, IsADirectoryError, PermissionError, UnicodeDecodeError, OSError):
        return default


def safe_read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, IsADirectoryError, PermissionError, UnicodeDecodeError, json.JSONDecodeError, OSError):
        return {}
    return value if isinstance(value, dict) else {}


def safe_read_toml(path: Path) -> dict[str, Any]:
    if tomllib is None:
        return {}
    try:
        with path.open("rb") as handle:
            value = tomllib.load(handle)
    except (FileNotFoundError, IsADirectoryError, PermissionError, tomllib.TOMLDecodeError, OSError):
        return {}
    return value if isinstance(value, dict) else {}


def git_lines(target: Path, args: list[str], timeout: int = 8) -> list[str]:
    if not target.exists() or not target.is_dir():
        return []
    try:
        proc = subprocess.run(
            ["git", *args],
            cwd=target,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=timeout,
        )
    except (FileNotFoundError, NotADirectoryError, PermissionError, subprocess.TimeoutExpired, OSError):
        return []
    if proc.returncode != 0:
        return []
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def git_pointer_issue(target: Path) -> str | None:
    git_file = target / ".git"
    if not git_file.is_file():
        return None

    text = safe_read_text(git_file).strip()
    if not text.startswith("gitdir:"):
        return None

    raw = text.split(":", 1)[1].strip()
    if not raw:
        return ".git file contains an empty gitdir pointer."

    pointed = Path(raw)
    if not pointed.is_absolute():
        pointed = (target / pointed).resolve()

    if not pointed.exists():
        return f".git file points to missing gitdir: {pointed}"
    return None
