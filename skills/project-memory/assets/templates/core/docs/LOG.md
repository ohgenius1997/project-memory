# Log

## Memory Metadata
- owner: chronological-history
- read_when: historical detail, prior experiments, or task narrative is needed
- update_when: meaningful progress, exploration, validation, or handoff-relevant events occur
- max_lines: 500
- stale_if: log contains durable decisions not copied to DECISIONS.md or current state not copied to PROJECT_STATUS.md

## Maintenance Rules
- Use this file for chronological project progress, exploration notes, and task history.
- Append concise entries by date.
- Move durable decisions to `DECISIONS.md`.
- Move current status to `PROJECT_STATUS.md`.
- If this file becomes too long, compact old routine entries into `docs/archive/`.

## {{DATE}}
- Initialized agent-facing project memory docs for {{PROJECT_NAME}}.
