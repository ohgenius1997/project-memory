# Principles

## Memory Metadata
- owner: global-operating-principles
- read_when: every new session, before making project changes
- update_when: durable project-wide principles change
- max_lines: 100
- stale_if: project memory workflow or fundamental project constraints change

## Maintenance Rules
- Use this file for durable rules that future Codex sessions must follow.
- Update only when a project-wide operating principle changes.
- Keep this file concise; target under 100 lines.
- Do not put transient plans or daily progress here.

## Global Principles
- Maintain project memory as work progresses.
- Prefer small, high-signal docs over comprehensive documentation.
- Keep `PROJECT_STATUS.md` short and current.
- Record durable decisions in `DECISIONS.md`.
- Preserve source-of-truth ownership: each fact should live in the file that owns it.
- Do not store secrets in project docs.
- Ask for confirmation before deleting, archiving, compacting, or rewriting durable project memory.
- Prefer selective loading over reading all project docs.
- Warn the developer when docs exceed context budget; do not compact automatically.
- Do not generate substantial code when product goal, success standard, core contracts, or AI permission boundaries are unclear.
- Record uncertainties as assumptions or open questions instead of treating them as facts.
- Confirm before dependency upgrades, destructive edits, large refactors, memory compaction, archival, or AGENTS.md migration.

## Project-Specific Principles
- This repository is for the `project-memory` skill only.
- Keep obsolete origin history archived and out of active project context.
- Scripts should default to read-only analysis unless a workflow explicitly initializes files.
- Public docs should not include local personal paths or machine-specific state.
