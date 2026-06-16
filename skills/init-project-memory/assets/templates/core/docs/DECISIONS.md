# Decisions

## Memory Metadata
- owner: durable-decisions-and-rationale
- read_when: changing direction, explaining why, resolving conflicts, compacting history
- update_when: durable technical, product, workflow, or operational decisions are made
- max_lines: 350
- stale_if: major decisions are superseded without being marked superseded

## Maintenance Rules
- Add an entry for durable technical, product, workflow, or operational decisions.
- Each entry should include date, decision, rationale, and consequences.
- Include alternatives considered when they may matter later.
- Do not use this file for daily progress logs.

## Decision Index
- {{DATE}} - Initialize agent-facing project memory

## Decision Log

### {{DATE}} - Initialize agent-facing project memory
- Decision: Use a lightweight project memory system for future Codex sessions.
- Rationale: Future sessions need fast context recovery and consistent operating rules.
- Consequences: Keep current state in `PROJECT_STATUS.md`, durable decisions here, and chronological detail in `LOG.md`.
- Alternatives considered: conventional external-facing docs; rejected because this system optimizes for agent context recovery.
