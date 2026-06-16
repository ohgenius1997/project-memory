# Domain

## Memory Metadata
- owner: domain-knowledge
- read_when: domain terminology, user mental model, business rules, professional constraints, or success criteria matter
- update_when: domain facts, terminology, constraints, workflows, or assumptions change
- max_lines: 240
- stale_if: target domain, user type, regulatory/manufacturing/business constraints, or accepted domain assumptions change

## Maintenance Rules
- Use this file for business or technical domain knowledge, not generic project management.
- Keep project shape and implementation roadmap in `PLAN.md` or project-specific addon docs.
- Separate known facts, decisions, assumptions, open questions, and risks.
- Do not create one-off domain addons; use this file for domain-specific context.

## Domain Summary
- Domain: agent-facing project memory management

## Known Facts
- Agent-facing memory is different from external documentation.
- The most valuable docs are short, stable, and routed by task.
- Context budget is a first-class constraint.
- `AGENTS.md` may be always-on context and should stay short.

## Terms
- Project memory: persistent files that let future agent sessions recover state and rules.
- Source of truth: the single document that owns a class of information.
- Vibe readiness: a gate that checks whether AI-assisted implementation has enough product, technical, safety, and permission context.
- Compaction plan: a read-only proposal for summarizing, moving, or archiving project memory.
- AGENTS migration: moving detailed context out of a long `AGENTS.md` into source-of-truth docs.

## User Mental Model
- Users want less repeated explanation across sessions.
- Users should trigger maintenance workflows explicitly.
- Users should review risky memory rewrites before they happen.

## Business Or Technical Rules
- Diagnose freely, but modify cautiously.
- Prefer read-only scripts for analysis and plans.
- Apply patches only after developer confirmation for risky memory operations.

## Decisions
- Domain-specific subject matter belongs in `docs/DOMAIN.md`, not one-off addon categories.

## Assumptions
- Users are comfortable with Markdown project docs.
- Codex sessions can read local project files and run helper scripts.

## Open Questions
- Whether future public users will prefer an installer script.

## Risks
- Too many docs can become the same context burden the skill is meant to solve.
