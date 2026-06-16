# Docs Spec

## Memory Metadata
- owner: documentation-product-spec
- read_when: creating or maintaining docs, knowledge bases, guides, or content products
- update_when: audience, information architecture, publication target, or content rules change
- max_lines: 240
- stale_if: audience, content structure, or publication workflow changes

## Maintenance Rules
- Use this file for docs/content product strategy and structure.
- Keep project progress in `LOG.md`.
- Keep durable decisions in `DECISIONS.md`.

## Audience
- Public readers evaluating or installing the skill.
- Future Codex sessions maintaining the repository.

## Information Architecture
- `README.md`: public introduction and usage.
- `skills/project-memory/SKILL.md`: skill instructions loaded by Codex.
- `skills/project-memory/assets/templates/`: generated project memory docs.
- `skills/project-memory/scripts/`: helper CLIs.
- `docs/`: this repository's own agent-facing project memory.
- `docs/archive/`: non-active historical context.

## Content Rules
- Keep README practical and concise.
- Keep active docs free of obsolete origin context.
- Keep local paths and machine-specific details out of public docs.
- Prefer examples that show read-only planning before risky changes.

## Publication Workflow
- Update docs locally.
- Validate scripts and skill metadata.
- Commit.
- Push to public GitHub repository.
