# Skill Spec

## Memory Metadata
- owner: skill-product-spec
- read_when: developing, changing, validating, or packaging a Codex skill/plugin/agent capability
- update_when: trigger rules, workflow, bundled resources, validation, or installation behavior changes
- max_lines: 220
- stale_if: skill scope, resources, or trigger behavior changes

## Maintenance Rules
- Use this file for Codex skill product shape, trigger behavior, workflows, bundled resources, and validation expectations.
- Update when skill scope, resources, scripts, templates, or invocation semantics change.
- Do not use this file for generic project planning; use `PLAN.md`.

## Skill Identity
- Name: `project-memory`
- Purpose: initialize, diagnose, and maintain lightweight agent-facing project memory docs.
- Primary users: Codex sessions and developers working across long-running coding projects.

## Known Facts
- Skill source lives in `skills/project-memory`.
- The skill uses templates, references, and Python scripts.
- The skill is intended to be installed into a Codex skills directory or copied as source.

## Decisions
- Keep helper scripts standard-library only.
- Keep maintenance actions developer-triggered.
- Use read-only planning for diagnosis, compaction, and AGENTS migration.
- Keep projectmem integration optional and advisory.
- Detect `conductor/` as an external static context directory and conflict signal; do not parse, migrate, synchronize, or adapt Conductor-specific files.
- Treat migration as generic Existing Context Migration from `AGENTS.md`, README, old docs, TODOs, roadmaps, changelogs, handoff notes, or developer-specified files into project-memory docs.
- Keep projectmem bridge commands read-only and best-effort so the skill does not hard-depend on a specific projectmem CLI version.
- Keep tracks optional for larger work units only; avoid creating a parallel project plan for small tasks.

## Assumptions
- Future users will restart Codex after installation.
- A repository can use generated docs without installing the skill globally.

## Open Questions
- Whether to add a one-command local installer.

## Trigger Scenarios
- Initialize project memory docs.
- Inspect an existing project before initialization and recommend addons.
- Generate a short current-state brief for a new session or handoff.
- Diagnose stale or missing project memory.
- Run a stricter Context Gate before broad implementation or active track work.
- Create optional track templates for feature/milestone state.
- Consult projectmem-style dynamic memory through a read-only bridge.
- Generate a context-budget compaction plan.
- Plan an AGENTS.md migration.
- Plan generic existing-context migration for brownfield projects.
- Check Vibe Coding readiness.
- Prepare handoff or coordination docs.
- Detect projectmem or external static context overlap and recommend safe routing.
- Stop initialization on `conductor/` by default unless `--allow-conductor` is explicitly used.

## Core Workflows
- Initialize: `scripts/init_docs.py`
- Inspect: `scripts/inspect_project.py`
- Brief: `scripts/brief_memory.py`
- Diagnose: `scripts/diagnose_memory.py`
- Context Gate: `scripts/diagnose_memory.py --context-gate`
- Dynamic memory bridge: `scripts/memory_bridge.py`
- Compact plan: `scripts/compact_memory.py`
- AGENTS migration plan: `scripts/migrate_agents.py`

## Bundled Resources
- `scripts/`: helper CLIs.
- `references/`: policy docs.
- `assets/templates/`: core and addon Markdown templates.

## Validation
- Python syntax check for scripts.
- Official skill validator when `PyYAML` is available.
- Temporary project generation tests for key addon combinations.
- Smoke tests for brief, diagnosis, context gate, project inspection, and memory bridge detection.
