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
- 2026-06-16 - Pivot repository to `project-memory`
- 2026-06-16 - Keep AGENTS.md short and route detail to docs
- 2026-06-16 - Use project-shape/platform/domain addon model
- 2026-06-16 - Add Vibe readiness gate
- 2026-06-16 - Use MIT license for open source release

## Decision Log

### 2026-06-16 - Pivot repository to `project-memory`
- Decision: The repository is now scoped to the `project-memory` Codex skill.
- Rationale: The project evolved from an initial domain-specific skill discussion into a reusable project memory system.
- Consequences: obsolete origin context is archived and no longer part of active project memory.
- Alternatives considered: continue as the initial domain-specific skill project; rejected because the implemented artifact is project-memory infrastructure.

### 2026-06-16 - Keep AGENTS.md short and route detail to docs
- Decision: `AGENTS.md` should contain only always-on operating rules and read routing.
- Rationale: `AGENTS.md` may be automatically loaded, so long historical or domain content wastes context.
- Consequences: Detailed content belongs in source-of-truth docs, and `migrate_agents.py` plans migrations for overlong AGENTS files.

### 2026-06-16 - Use project-shape/platform/domain addon model
- Decision: Addons represent project shape, platform/runtime, and generic domain context.
- Rationale: Business-domain-specific addons do not generalize.
- Consequences: Domain-specific project knowledge belongs in `docs/DOMAIN.md`.

### 2026-06-16 - Add Vibe readiness gate
- Decision: Generated project memory includes `docs/VIBE_READINESS.md`.
- Rationale: AI-assisted implementation needs clear product goals, stack/runtime, core contracts, red lines, and AI permission boundaries.
- Consequences: Diagnosis warns when readiness placeholders remain before broad code generation.

### 2026-06-16 - Use MIT license for open source release
- Decision: Publish under MIT license.
- Rationale: The project is a lightweight developer tool where broad reuse and modification are desirable.
- Consequences: Users can reuse and adapt the skill with minimal restrictions.
