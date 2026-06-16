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
9. `docs/LOG.md` only when historical detail is needed

## Task-Based Read Paths
- Continue implementation: `PROJECT_STATUS.md`, `docs/PRINCIPLES.md`, `docs/PLAN.md`
- Start substantial code generation or refactor: add `docs/VIBE_READINESS.md`
- Change architecture or direction: add `docs/DECISIONS.md`
- Work on setup/build/runtime/devices: add `docs/ENVIRONMENT.md`
- Work on git/GitHub/branches/releases: add `docs/REPOSITORY.md`
- Handle handoff/parallel work/long tasks: add `docs/COORDINATION.md`
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
- Chronological history: `docs/LOG.md`

## Update Triggers
- Update `PROJECT_STATUS.md` after meaningful progress, blockers, or next-step changes.
- Add to `docs/DECISIONS.md` when a durable technical, product, workflow, or operational decision is made.
- Add to `docs/LOG.md` for chronological progress details.
- Update `docs/ENVIRONMENT.md` when setup, dependencies, versions, paths, or cross-device assumptions change.
- Update `docs/REPOSITORY.md` when git/GitHub rules, remotes, branches, generated-file policy, or release process changes.
- Activate or update `docs/COORDINATION.md` when work splits across sessions, branches, agents, devices, or long-running tasks.
- Update `docs/VIBE_READINESS.md` when product goal, stack/runtime, conventions, core contracts, red lines, or AI permission boundaries change.

## Context Budget Warnings
- If `AGENTS.md` exceeds 140 lines, recommend `$init-project-memory migrate-agents`.
- If `PROJECT_STATUS.md` exceeds 150 lines, recommend `$init-project-memory compact`.
- If `docs/LOG.md` exceeds 500 lines, recommend `$init-project-memory compact`.
- If any memory doc mixes current state with stale history, recommend diagnosis or compaction.
- Do not compact, archive, or delete content without developer confirmation.

## Project Context
- Project: {{PROJECT_NAME}}
- Kind: {{PROJECT_KIND}}
- Domain: {{DOMAIN}}
- Initialized: {{DATE}}
- Addons: {{ADDONS}}
