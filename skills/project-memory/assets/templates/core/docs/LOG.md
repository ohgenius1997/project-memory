# Checkpoint Log

## Memory Metadata
- owner: sparse-checkpoint-fallback
- read_when: dynamic memory is unavailable and sparse project checkpoints are needed
- update_when: meaningful milestone checkpoints occur and agentmemory is unavailable
- max_lines: 220
- stale_if: log contains durable decisions not copied to DECISIONS.md or current state not copied to PROJECT_STATUS.md

## Maintenance Rules
- Use this file only as a lightweight fallback when agentmemory is unavailable.
- Do not record full session transcripts, ordinary attempts, transient failures, or debug traces.
- Append only high-signal milestone checkpoints.
- Append concise entries by date.
- Move durable decisions to `DECISIONS.md`.
- Move current status to `PROJECT_STATUS.md`.
- If this file becomes too long, compact old routine entries into summaries.

## {{DATE}}
- Initialized AGENTS-first project context routing for {{PROJECT_NAME}}.
