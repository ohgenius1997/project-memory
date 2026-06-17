# Agent Context Router

CRITICAL: Before mutating repository files, read this `AGENTS.md`, choose the smallest task-specific context below, and state the context sources used in a progress update or final response.

## Memory Metadata
- owner: always-on-agent-router
- read_when: every new session, before repository mutation, before handoff
- update_when: stable rules, routing, dynamic-memory ownership, public repo boundaries, or AI permission boundaries change
- max_lines: 120
- stale_if: project profile, dynamic-memory tool, source-of-truth ownership, or public release policy changes

## Maintenance Rules
- Keep this file short; it is the always-on router, not a project encyclopedia.
- Update only for stable rules, read paths, boundaries, validation policy, or source-of-truth ownership.
- Keep generated target-project templates under `skills/project-memory/assets/templates/`.
- Do not put local project-management history, session logs, or raw dynamic-memory exports here.

## Project
- Name: project-memory
- Kind: Codex skill
- Domain: AGENTS-first project context routing for AI-assisted coding projects
- Profile: governed
- Dynamic memory: agentmemory recommended, not installed or wrapped by this project

## Goal
- User: developers using coding agents across sessions.
- Problem: agents lose stable project context or over-load every session with too much history.
- Success standard: a future agent can start from `AGENTS.md`, choose the smallest useful context, and avoid mixing stable rules with episodic memory.

## Public Repo Rules
- Keep the public repository focused on the reusable skill: `skills/project-memory/`, `README.md`, license, CI, tests, `pyproject.toml`, and this `AGENTS.md`.
- Do not commit local project-management memory such as root `docs/` or `PROJECT_STATUS.md`.
- Keep helper scripts dependency-light and runnable with the Python standard library.
- Do not add MCP servers, daemons, global hooks, vector stores, or automatic dynamic-memory writes.
- Recommend agentmemory as the dynamic-memory companion, but do not install, wrap, or hard-code calls to it.

## Context Routing
- Ordinary development: read this file, then use agentmemory relevant memory if available.
- Continue long-running project work: add `PROJECT_STATUS.md` if present.
- Change architecture, product direction, workflow policy, or public positioning: add `docs/DECISIONS.md` if present.
- Change dependencies, setup, CI, validation, runtime, release, or cross-device assumptions: add `docs/ENVIRONMENT.md` if present.
- Coordinate parallel sessions, branches, owners, or handoff: add `docs/COORDINATION.md` if present.
- Need historical reasoning: prefer agentmemory; read `docs/LOG.md` only as a sparse checkpoint fallback.

## Memory Ownership
- `AGENTS.md`: stable operating rules, context routing, public repo boundaries, and source-of-truth ownership.
- agentmemory: attempts, failures, debugging traces, file-level gotchas, session continuity, and episodic recall.
- `PROJECT_STATUS.md`: current phase, latest conclusion, next step, blockers, and active risks.
- `docs/DECISIONS.md`: durable decisions, rationale, alternatives, and consequences.
- `docs/ENVIRONMENT.md`: stable setup, dependency, CI, device, or cross-machine facts.
- `docs/COORDINATION.md`: active multi-session or multi-branch handoff and collision state.

## Checkpoint Rules
- Update `PROJECT_STATUS.md` only when the current phase, next step, blocker, or risk changes.
- Add `docs/DECISIONS.md` entries only for durable decisions that future sessions must honor.
- Do not write ordinary attempts, transient failures, debug traces, or file-level gotchas into project-memory docs; use agentmemory.
- If agentmemory is unavailable, keep `docs/LOG.md` to sparse checkpoint summaries only.

## Git Tracking Policy
- Follow this repository's `.gitignore` and developer instructions for which memory files are committed.
- Commit this `AGENTS.md` because repository rules should travel across branches, machines, and contributors.
- Do not commit root `PROJECT_STATUS.md` or root `docs/` for this public skill repository unless the public repo policy changes.
- Never commit secrets, private tokens, credentials, large raw session transcripts, or raw dynamic-memory dumps.

## AI Boundaries
- Do not overwrite existing context files without explicit developer confirmation.
- Do not compact, archive, delete, or migrate durable context without confirmation.
- In `docs/COORDINATION.md`, update only this session's status unless the developer asks otherwise; do not assign owners, lock or unlock others' work, or declare another session complete.
- Treat PDY_2 as a detached non-git dogfood folder unless it is deliberately reinitialized as an independent repo.

## Task Routing
- Skill instructions: `skills/project-memory/SKILL.md`
- Public docs: `README.md`
- Scripts: `skills/project-memory/scripts/`
- Templates: `skills/project-memory/assets/templates/`
- Tests: `tests/`
- CI: `.github/workflows/validate.yml`

## Validation
- After script edits: `PYTHONPYCACHEPREFIX=/tmp/project-memory-pycache python3 -m compileall -q skills/project-memory/scripts tests`
- After behavior changes: `python3 -m unittest discover -s tests`
- After template or init changes: smoke minimal, standard, governed, and dynamic-memory-none initialization.
- After workflow changes: smoke status sync, diagnosis, brief, inspect, compact, and migration planner commands.
