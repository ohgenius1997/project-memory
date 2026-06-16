# Agent Operating Rules

## Memory Metadata
- owner: agent-operating-rules
- read_when: every new session, uncertain project memory behavior
- update_when: read order, update triggers, source-of-truth ownership, or coordination rules change
- max_lines: 140
- stale_if: documentation structure or project memory workflow changes

## Maintenance Rules
- This file is the top-level operating rulebook for Codex/agent sessions in this project.
- Read `PROJECT_STATUS.md` and `docs/PRINCIPLES.md` before making project changes.
- Update project memory during the task when state, decisions, setup, repository rules, or handoff context changes.
- Do not put long project history here. Use `docs/LOG.md`.
- Do not put detailed background, environment, repository rules, decisions, or logs here; route to `docs/`.

## Default Read Order
1. `PROJECT_STATUS.md`
2. `docs/PRINCIPLES.md`
3. `docs/PLAN.md`
4. `docs/VIBE_READINESS.md` before substantial code generation or large refactors
5. `docs/DECISIONS.md` when changing direction or explaining previous choices
6. `docs/ENVIRONMENT.md` when setup/build/runtime/cross-device details matter
7. `docs/REPOSITORY.md` when git/GitHub/branch/release details matter
8. `docs/COORDINATION.md` when parallel work or handoff exists
9. `docs/TRACKS.md` when feature tracks or larger work units are active
10. `docs/LOG.md` only when historical detail is needed

## Task-Based Read Paths
- Continue implementation: `PROJECT_STATUS.md`, `docs/PRINCIPLES.md`, `docs/PLAN.md`
- Start substantial code generation or refactor: add `docs/VIBE_READINESS.md`
- Change architecture or direction: add `docs/DECISIONS.md`
- Work on setup/build/runtime/devices: add `docs/ENVIRONMENT.md`
- Work on git/GitHub/branches/releases: add `docs/REPOSITORY.md`
- Handle handoff/parallel work/long tasks: add `docs/COORDINATION.md`
- Work on active feature tracks or multi-step milestones: add `docs/TRACKS.md` if present
- Need domain terminology or business rules: add `docs/DOMAIN.md` if present
- Need historical reasoning: read `docs/LOG.md` selectively
- Diagnose or compact project memory: read all project memory docs first

## Source Of Truth
- Current phase, next action, blockers: `PROJECT_STATUS.md`
- Global rules: `docs/PRINCIPLES.md`
- Current approach and roadmap: `docs/PLAN.md`
- Vibe coding readiness, red lines, AI permissions: `docs/VIBE_READINESS.md`
- Durable decisions and alternatives: `docs/DECISIONS.md`
- Domain concepts and terminology: `docs/DOMAIN.md`
- Setup and cross-device configuration: `docs/ENVIRONMENT.md`
- Git/GitHub/release rules: `docs/REPOSITORY.md`
- Parallel work and handoff state: `docs/COORDINATION.md`
- Feature track status and local work-unit links: `docs/TRACKS.md`
- Chronological history: `docs/LOG.md`

## External Memory Modes
- If `.projectmem/` exists, treat projectmem as dynamic event memory for issues, attempts, fixes, file-level gotchas, and precheck hints. Do not read or edit raw event logs unless explicitly asked.
- Prefer `memory_bridge.py detect|summary|precheck` when the project-memory skill scripts are available.
- If `conductor/` exists, treat it as an external static context directory and conflict signal. Do not parse, migrate, or synchronize Conductor-specific files by default.
- Precheck warnings are risk inputs, not refusal criteria. Use them to adjust the plan and explain mitigation.

## Context Gate
- Before broad implementation, large refactors, or new feature work, check `docs/VIBE_READINESS.md`, `PROJECT_STATUS.md`, and relevant decisions.
- Prefer `diagnose_memory.py --context-gate` when the project-memory skill scripts are available.
- If `.projectmem/` exists, use recent events or precheck output to verify the current plan is not repeating known failures.
- If `conductor/` exists, confirm whether to proceed with project-memory despite the external static context directory.

## Update Triggers
- Update `PROJECT_STATUS.md` after meaningful progress, blockers, or next-step changes.
- Add to `docs/DECISIONS.md` when a durable technical, product, workflow, or operational decision is made.
- Add to `docs/LOG.md` for chronological progress details.
- Update `docs/ENVIRONMENT.md` when setup, dependencies, versions, paths, or cross-device assumptions change.
- Update `docs/REPOSITORY.md` when git/GitHub rules, remotes, branches, generated-file policy, or release process changes.
- Activate or update `docs/COORDINATION.md` when work splits across sessions, branches, agents, devices, or long-running tasks.
- Update `docs/TRACKS.md` when active feature track state, owner/session, last updated date, or next step changes.
- Update `docs/VIBE_READINESS.md` when product goal, stack/runtime, conventions, core contracts, red lines, or AI permission boundaries change.

## Context Budget Warnings
- If `AGENTS.md` exceeds 140 lines, recommend `$project-memory migrate-agents`.
- If `PROJECT_STATUS.md` exceeds 150 lines, recommend `$project-memory compact`.
- If `docs/LOG.md` exceeds 500 lines, recommend `$project-memory compact`.
- If any memory doc mixes current state with stale history, recommend diagnosis or compaction.
- If two static context systems appear to own the same fact, recommend diagnosis and source-of-truth cleanup.
- Do not compact, archive, or delete content without developer confirmation.

## Project Context
- Project: {{PROJECT_NAME}}
- Kind: {{PROJECT_KIND}}
- Domain: {{DOMAIN}}
- Initialized: {{DATE}}
- Addons: {{ADDONS}}
