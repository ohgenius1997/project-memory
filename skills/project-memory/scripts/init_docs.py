#!/usr/bin/env python3
"""Initialize agent-facing project memory docs from bundled templates."""

from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = SKILL_ROOT / "assets" / "templates"
CORE_TEMPLATE = TEMPLATE_ROOT / "core"
ADDONS_ROOT = TEMPLATE_ROOT / "addons"

ADDON_GROUPS = {
    "project shape": ["skill", "app", "system", "library", "docs", "data-ai"],
    "platform/runtime": ["web", "ios", "cli", "cloud"],
    "context": ["domain"],
}
KNOWN_ADDONS = {addon for addons in ADDON_GROUPS.values() for addon in addons}

ADDON_ALIASES = {
    "agent": "skill",
    "plugin": "skill",
    "documentation": "docs",
    "doc": "docs",
    "data": "data-ai",
    "ai": "data-ai",
    "ml": "data-ai",
    # Domain-specific requests intentionally collapse to generic domain context.
    "cad": "domain",
    "3d": "domain",
    "modeling": "domain",
    "modelling": "domain",
}

ADDON_KEYWORDS = {
    "skill": [
        "skill",
        "plugin",
        "agent capability",
        "codex",
        "mcp",
    ],
    "app": [
        "app",
        "application",
        "mobile app",
        "desktop app",
        "product app",
    ],
    "system": [
        "system",
        "service",
        "backend",
        "platform",
        "automation",
        "infrastructure",
    ],
    "library": [
        "library",
        "sdk",
        "package",
        "framework",
        "module",
    ],
    "docs": [
        "docs",
        "documentation",
        "knowledge base",
        "guide",
        "manual",
    ],
    "data-ai": [
        "data",
        "dataset",
        "analytics",
        "machine learning",
        "ml",
        "ai",
        "evaluation",
        "benchmark",
    ],
    "web": [
        "web",
        "frontend",
        "react",
        "next.js",
        "nextjs",
        "browser",
        "dashboard",
    ],
    "ios": [
        "ios",
        "swift",
        "swiftui",
        "xcode",
        "iphone",
        "ipad",
    ],
    "cli": [
        "cli",
        "command line",
        "terminal",
        "shell",
    ],
    "cloud": [
        "cloud",
        "aws",
        "gcp",
        "azure",
        "deployment",
        "kubernetes",
        "serverless",
    ],
}

GENERIC_DOMAINS = {
    "",
    "unspecified",
    "general",
    "general coding",
    "software",
    "coding",
    "n/a",
    "none",
    "tbd",
}


def normalize_addon(value: str) -> str:
    item = value.strip().lower()
    return ADDON_ALIASES.get(item, item)


def split_addons(values: list[str] | None) -> list[str]:
    if not values:
        return []
    result: list[str] = []
    for value in values:
        for item in value.split(","):
            normalized = normalize_addon(item)
            if normalized:
                result.append(normalized)
    return result


def domain_is_specific(domain: str) -> bool:
    normalized = " ".join(domain.strip().lower().split())
    return normalized not in GENERIC_DOMAINS


def infer_addons(project_kind: str, domain: str) -> list[str]:
    text = f"{project_kind} {domain}".lower()
    addons: list[str] = []
    for addon, keywords in ADDON_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            addons.append(addon)

    # Most user-facing platform projects are also apps.
    if any(platform in addons for platform in ["web", "ios"]) and "app" not in addons:
        if "app" in text or "application" in text or "product" in text:
            addons.append("app")

    # Business/professional subject matter belongs in DOMAIN.md, not in custom addons.
    if domain_is_specific(domain):
        addons.append("domain")

    return sorted(set(addons), key=addon_sort_key)


def addon_sort_key(addon: str) -> tuple[int, str]:
    for index, addons in enumerate(ADDON_GROUPS.values()):
        if addon in addons:
            return index, addon
    return 99, addon


def render(content: str, variables: dict[str, str]) -> str:
    for key, value in variables.items():
        content = content.replace("{{" + key + "}}", value)
    return content


def copy_templates(
    template_dir: Path,
    target: Path,
    variables: dict[str, str],
    *,
    force: bool,
    dry_run: bool,
) -> tuple[list[Path], list[Path]]:
    created: list[Path] = []
    skipped: list[Path] = []

    for source in sorted(template_dir.rglob("*")):
        if not source.is_file():
            continue
        relative = source.relative_to(template_dir)
        if any(part.startswith(".") for part in relative.parts):
            continue
        destination = target / relative
        if destination.exists() and not force:
            skipped.append(destination)
            continue
        if not dry_run:
            destination.parent.mkdir(parents=True, exist_ok=True)
            rendered = render(source.read_text(encoding="utf-8"), variables)
            destination.write_text(rendered, encoding="utf-8")
        created.append(destination)

    return created, skipped


def print_addons() -> None:
    for group, addons in ADDON_GROUPS.items():
        print(f"{group}:")
        for addon in addons:
            print(f"  - {addon}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Initialize agent-facing project memory docs."
    )
    parser.add_argument("--target", help="Project directory to initialize.")
    parser.add_argument("--project-name", default="", help="Project display name.")
    parser.add_argument("--project-kind", default="software project", help="Project type.")
    parser.add_argument("--domain", default="", help="Business or product domain.")
    parser.add_argument(
        "--addons",
        nargs="*",
        help=(
            "Optional addons. Known: skill,app,system,library,docs,data-ai,"
            "web,ios,cli,cloud,domain. Commas are accepted."
        ),
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files. Use only with explicit developer confirmation.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print actions without writing.")
    parser.add_argument(
        "--list-addons",
        action="store_true",
        help="List known addons and exit.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.list_addons:
        print_addons()
        return 0

    if not args.target:
        print("--target is required unless --list-addons is used.", file=sys.stderr)
        return 2

    target = Path(args.target).expanduser().resolve()
    project_name = args.project_name.strip() or target.name
    project_kind = args.project_kind.strip() or "software project"
    domain = args.domain.strip() or "unspecified"

    requested_addons = split_addons(args.addons)
    addons = requested_addons or infer_addons(project_kind, domain)
    unknown = sorted(set(addons) - KNOWN_ADDONS)
    if unknown:
        print(f"Unknown addon(s): {', '.join(unknown)}", file=sys.stderr)
        print("Known addon(s):", file=sys.stderr)
        for group, group_addons in ADDON_GROUPS.items():
            print(f"  {group}: {', '.join(group_addons)}", file=sys.stderr)
        return 2
    addons = sorted(set(addons), key=addon_sort_key)

    variables = {
        "PROJECT_NAME": project_name,
        "PROJECT_KIND": project_kind,
        "DOMAIN": domain,
        "DATE": dt.date.today().isoformat(),
        "ADDONS": ", ".join(addons) if addons else "none",
    }

    if not CORE_TEMPLATE.exists():
        print(f"Missing core template directory: {CORE_TEMPLATE}", file=sys.stderr)
        return 2

    all_created: list[Path] = []
    all_skipped: list[Path] = []

    created, skipped = copy_templates(
        CORE_TEMPLATE, target, variables, force=args.force, dry_run=args.dry_run
    )
    all_created.extend(created)
    all_skipped.extend(skipped)

    for addon in addons:
        addon_dir = ADDONS_ROOT / addon
        if not addon_dir.exists():
            print(f"Missing addon template directory: {addon_dir}", file=sys.stderr)
            return 2
        created, skipped = copy_templates(
            addon_dir, target, variables, force=args.force, dry_run=args.dry_run
        )
        all_created.extend(created)
        all_skipped.extend(skipped)

    action = "Would create/update" if args.dry_run else "Created/updated"
    print(f"{action}: {len(all_created)} file(s)")
    for path in all_created:
        print(f"  + {path}")

    if all_skipped:
        print(f"Skipped existing: {len(all_skipped)} file(s)")
        for path in all_skipped:
            print(f"  = {path}")

    print(f"Selected addons: {', '.join(addons) if addons else 'none'}")
    if args.force:
        print("Force mode was enabled; existing files may have been replaced.")

    print("\nNext:")
    print("- Fill `PROJECT_STATUS.md` current phase, branch, next action, and risks.")
    print("- Fill `docs/CONTEXT.md` known facts and assumptions.")
    print("- Fill `docs/PLAN.md` current approach and next actions.")
    print("- Fill `docs/VIBE_READINESS.md` product goal, stack/runtime, core contracts, red lines, and AI permission boundaries before broad code generation.")
    print("- Fill `docs/REPOSITORY.md` before git/GitHub work.")
    print("- Keep `docs/COORDINATION.md` inactive until work splits.")
    if "domain" in addons:
        print("- Fill `docs/DOMAIN.md` with domain terms, rules, and risks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
