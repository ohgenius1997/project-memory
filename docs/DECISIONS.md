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
- 2026-06-16 - Keep projectmem optional and advisory
- 2026-06-16 - Treat conductor as external context signal
- 2026-06-16 - Add optional tracks and read-only helper adapters
- 2026-06-16 - Define migration as generic Existing Context Migration

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

### 2026-06-16 - Keep projectmem optional and advisory
- Decision: `project-memory` will detect and route around projectmem but will not require it.
- Rationale: projectmem is useful as a dynamic event layer, while `project-memory` should remain a lightweight Codex skill.
- Consequences: projectmem warnings can influence plans and testing, but they cannot be the sole reason to refuse a user request.

### 2026-06-16 - Treat conductor as external context signal
- Decision: `conductor/` from context-driven-development is an external static context directory and conflict signal, not a compatibility target or default companion layer.
- Rationale: Conductor-style files and project-memory docs can both describe static project context, so silently maintaining both risks duplicate or conflicting facts.
- Consequences: detection should stop default initialization and warn about an external static context directory. project-memory does not parse, migrate, or synchronize Conductor-specific files.

### 2026-06-16 - Add optional tracks and read-only helper adapters
- Decision: Add optional `tracks` templates, Context Gate diagnostics, `inspect_project.py`, and read-only `memory_bridge.py`.
- Rationale: These features borrow the useful parts of richer context systems without making project-memory a daemon, MCP server, or runtime dependency.
- Consequences: The skill can guide larger and existing projects better while preserving the core safety model: diagnose and suggest first, patch only after clear intent or confirmation.
- Alternatives considered: make projectmem/Conductor hard dependencies; rejected because that would narrow usage and increase maintenance risk.

### 2026-06-16 - Define migration as generic Existing Context Migration
- Decision: Migration means classifying useful historical project context from `AGENTS.md`, README, old docs, TODOs, roadmaps, changelogs, handoff notes, or developer-specified files into project-memory docs.
- Rationale: A generic migration model serves ordinary brownfield projects without coupling project-memory to any third-party context framework.
- Consequences: `conductor/` remains a conflict signal only. It is not a compatibility target, migration source format, or synchronization partner. The read-only `migrate_context.py` planner implements this as advisory classification, not automatic rewriting.
- Alternatives considered: adapt context-driven-development/Conductor outputs directly; rejected because the project intentionally borrows ideas without inheriting another system's file semantics.
