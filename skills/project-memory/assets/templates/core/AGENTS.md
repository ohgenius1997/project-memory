# Agent Context Router

CRITICAL: Before mutating repository files, read this `AGENTS.md`, choose the smallest task-specific context below, and state the context sources used in a progress update or final response.

## Memory Metadata
- owner: always-on-agent-router
- read_when: every new session, before repository mutation, before handoff
- update_when: stable rules, routing, dynamic-memory ownership, or AI permission boundaries change
- max_lines: 90
- stale_if: project profile, dynamic-memory tool, or source-of-truth ownership changes

## Project
- Name: {{PROJECT_NAME}}
- Kind: {{PROJECT_KIND}}
- Domain: {{DOMAIN}}
- Profile: {{PROFILE}}
- Dynamic memory: {{DYNAMIC_MEMORY}}
- Initialized: {{DATE}}

## Goal
- User: TBD
- Problem: TBD
- Success standard: TBD

## Context Routing
- Ordinary development: read this file, then use agentmemory relevant memory if available.
- Continue a long-running task: add `PROJECT_STATUS.md` if present.
- Change architecture, product direction, or workflow policy: add `docs/DECISIONS.md` if present.
- Change dependencies, setup, CI, build, runtime, or cross-device assumptions: add `docs/ENVIRONMENT.md` if present.
- Coordinate parallel sessions, branches, owners, or handoff: add `docs/COORDINATION.md` if present.
- Need historical reasoning: prefer agentmemory; use `docs/LOG.md` only as a lightweight checkpoint fallback if present.

## Memory Ownership
- `AGENTS.md`: stable operating rules, routing, and source-of-truth ownership.
- agentmemory: attempts, failures, debugging traces, file-level gotchas, session continuity, and episodic recall.
- `PROJECT_STATUS.md`: current phase, latest conclusion, next step, blockers, and active risks.
- `docs/DECISIONS.md`: durable decisions, rationale, alternatives, and consequences.
- `docs/ENVIRONMENT.md`: stable setup, dependency, CI, device, or cross-machine facts.
- `docs/COORDINATION.md`: active multi-session or multi-branch handoff and collision state.

## Checkpoint Rules
- Update `PROJECT_STATUS.md` only when the current phase, next step, blocker, or risk changes.
- Add `docs/DECISIONS.md` entries only for durable decisions that future sessions must honor.
- Do not write ordinary attempts, transient failures, or debug traces into project-memory docs; use agentmemory.
- If dynamic memory is unavailable, keep `docs/LOG.md` to sparse checkpoint summaries only.

## AI Boundaries
- Do not store secrets, credentials, or private tokens in project-memory docs.
- Do not overwrite existing context files without explicit developer confirmation.
- Do not compact, archive, delete, or migrate durable context without confirmation.
- In `docs/COORDINATION.md`, update only this session's status unless the developer asks otherwise; do not assign owners, lock or unlock others' work, or declare another session complete.

## Upgrade Signals
- Recommend `standard` when this file starts carrying current status or durable decisions.
- Recommend `governed` when cross-device setup, multiple branches, multiple sessions, or handoff state becomes active.
