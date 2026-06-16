# Decisions

## Memory Metadata
- owner: durable-decisions-and-rationale
- read_when: changing architecture, product direction, workflow policy, or explaining why
- update_when: durable technical, product, workflow, or operational decisions are made
- max_lines: 260
- stale_if: accepted decisions are superseded without a new entry

## Maintenance Rules
- Record only durable decisions future sessions must honor.
- Include decision, rationale, alternatives, and consequences.
- Do not record ordinary attempts, transient failures, or daily progress.
- Prefer agentmemory for episodic process history.

## Decision Index
- {{DATE}} - Use AGENTS-first project context routing

## Decision Log

### {{DATE}} - Use AGENTS-first project context routing
- Decision: Keep stable operating rules in `AGENTS.md` and use project-memory docs only for stable facts that should be audited or resumed across sessions.
- Rationale: Agents need a short always-on router more than a large documentation tree.
- Alternatives considered: full multi-document project memory by default; rejected because it increases context and maintenance cost for lightweight projects.
- Consequences: Dynamic attempts and session history should be handled by agentmemory; only current state and durable decisions belong in project-memory docs.
