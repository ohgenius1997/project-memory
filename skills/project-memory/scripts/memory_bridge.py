#!/usr/bin/env python3
"""Read-only bridge for optional dynamic project memory systems."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


DISTILLED_PATTERNS = [
    "**/summary*.md",
    "**/SUMMARY*.md",
    "**/PROJECT_MAP.md",
    "**/AI_INSTRUCTIONS.md",
    "**/project_map*.md",
    "**/README.md",
]

RAW_EVENT_NAMES = {
    "events.jsonl",
    "events.json",
    "log.jsonl",
    "memory.jsonl",
}


def read(path: Path, max_chars: int) -> str:
    try:
        return path.read_text(encoding="utf-8")[:max_chars]
    except (FileNotFoundError, UnicodeDecodeError):
        return ""


def distilled_files(target: Path) -> list[Path]:
    root = target / ".projectmem"
    if not root.exists():
        return []
    files: list[Path] = []
    for pattern in DISTILLED_PATTERNS:
        files.extend(path for path in root.glob(pattern) if path.is_file())
    return sorted(
        {
            path
            for path in files
            if path.name not in RAW_EVENT_NAMES and path.suffix.lower() in {".md", ".txt"}
        }
    )


def run_pjm(target: Path, commands: list[list[str]]) -> dict[str, object] | None:
    pjm = shutil.which("pjm")
    if not pjm:
        return None

    for command in commands:
        try:
            proc = subprocess.run(
                [pjm, *command],
                cwd=target,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=12,
                check=False,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
        output = proc.stdout.strip() or proc.stderr.strip()
        if proc.returncode == 0 and output:
            return {
                "available": True,
                "source": "pjm",
                "command": " ".join(["pjm", *command]),
                "output": output,
            }
    return {
        "available": False,
        "source": "pjm",
        "message": "pjm is installed, but no supported read-only command returned output.",
    }


def detect(target: Path) -> dict[str, object]:
    files = distilled_files(target)
    return {
        "target": str(target),
        "projectmem_dir": (target / ".projectmem").exists(),
        "pjm_cli": shutil.which("pjm"),
        "distilled_files": [str(path.relative_to(target)) for path in files[:12]],
        "mode": "read-only",
        "raw_event_policy": "Do not read or edit raw projectmem event logs by default.",
    }


def summary(target: Path, max_chars: int) -> dict[str, object]:
    files = distilled_files(target)
    if files:
        items = []
        per_file = max(400, max_chars // max(len(files[:4]), 1))
        for path in files[:4]:
            items.append(
                {
                    "path": str(path.relative_to(target)),
                    "content": read(path, per_file),
                }
            )
        return {
            "available": True,
            "source": "distilled-files",
            "items": items,
            "policy": "Distilled summaries are preferred over raw event logs.",
        }

    pjm_result = run_pjm(
        target,
        [
            ["summary"],
            ["show"],
            ["get-summary"],
        ],
    )
    if pjm_result:
        return pjm_result
    return {
        "available": False,
        "source": "none",
        "message": "No .projectmem distilled summary or pjm CLI summary command is available.",
    }


def recent(target: Path) -> dict[str, object]:
    pjm_result = run_pjm(
        target,
        [
            ["recent"],
            ["log", "--recent"],
            ["show", "--recent"],
        ],
    )
    if pjm_result:
        return pjm_result
    return {
        "available": False,
        "source": "none",
        "message": "Recent dynamic memory is unavailable without a supported pjm CLI command.",
    }


def precheck(target: Path, file_path: str) -> dict[str, object]:
    pjm_result = run_pjm(
        target,
        [
            ["precheck", file_path],
            ["precheck", "--file", file_path],
        ],
    )
    if pjm_result:
        pjm_result["policy"] = (
            "Treat precheck output as advisory risk input; do not refuse work solely because "
            "historical failures exist."
        )
        return pjm_result
    return {
        "available": False,
        "source": "none",
        "file": file_path,
        "message": "Precheck is unavailable without a supported pjm CLI command.",
        "policy": "Continue with normal project-memory docs and local code inspection.",
    }


def print_markdown(command: str, result: dict[str, object]) -> None:
    print("# Memory Bridge\n")
    print(f"- Command: `{command}`")
    print("- Mode: read-only")

    if command == "detect":
        print(f"- Projectmem dir: `{result['projectmem_dir']}`")
        print(f"- pjm CLI: `{result['pjm_cli'] or 'not found'}`")
        files = result["distilled_files"]
        assert isinstance(files, list)
        if files:
            print("\n## Distilled Files")
            for item in files:
                print(f"- `{item}`")
        print(f"\nPolicy: {result['raw_event_policy']}")
        return

    if result.get("available"):
        print(f"- Source: `{result.get('source')}`")
        if "command" in result:
            print(f"- Tool command: `{result['command']}`")
        if "items" in result:
            print("\n## Summary Files")
            items = result["items"]
            assert isinstance(items, list)
            for item in items:
                assert isinstance(item, dict)
                print(f"\n### `{item['path']}`\n")
                print(item["content"])
        elif "output" in result:
            print("\n## Output\n")
            print(result["output"])
        if "policy" in result:
            print(f"\nPolicy: {result['policy']}")
        return

    print(f"- Source: `{result.get('source')}`")
    print(f"- Message: {result.get('message')}")
    if "policy" in result:
        print(f"- Policy: {result['policy']}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only bridge for optional dynamic memory.")
    parser.add_argument(
        "command",
        choices=["detect", "summary", "recent", "precheck"],
        help="Bridge command to run.",
    )
    parser.add_argument("file", nargs="?", help="File path for precheck.")
    parser.add_argument("--target", default=".", help="Project directory to inspect.")
    parser.add_argument("--max-chars", type=int, default=6000, help="Maximum summary characters.")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    args = parser.parse_args()

    target = Path(args.target).expanduser().resolve()
    if args.command == "detect":
        result = detect(target)
    elif args.command == "summary":
        result = summary(target, max(1000, args.max_chars))
    elif args.command == "recent":
        result = recent(target)
    else:
        if not args.file:
            parser.error("precheck requires a file path")
        result = precheck(target, args.file)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_markdown(args.command, result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
