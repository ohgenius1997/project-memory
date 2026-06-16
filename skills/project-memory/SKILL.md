---
name: project-memory
description: Initialize, diagnose, migrate, compact-plan, and maintain lightweight agent-facing project memory docs for coding projects. Use when the user asks to initialize project documentation, manage project memory, recover context, create agent runbooks, record project principles, progress logs, environment notes, repository rules, coordination docs, handoff notes, Vibe Coding readiness checks, AGENTS.md migration plans, context-budget compaction planning, or cross-device/project-state sync checks for software, skill, app, data, docs, system, or agent projects.
---

# Project Memory

## Core Contract

Create and maintain a project memory layer for future Codex sessions. Optimize for selective loading, fast context recovery, consistent project rules, safe cross-session execution, and low-maintenance progress tracking. Do not optimize for public-facing completeness.

Use this skill in developer-triggered workflows only. Do not silently rewrite project memory, archive content, delete historical context, or change durable decisions without explicit developer confirmation.

## Default Read Order

When resuming a project with this documentation system, read:

1. `PROJECT_STATUS.md`
2. `docs/PRINCIPLES.md`
3. `docs/PLAN.md`
4. `docs/VIBE_READINESS.md` before substantial code generation or large refactors
5. `docs/DECISIONS.md` when changing direction or explaining prior choices
6. `docs/ENVIRONMENT.md` when setup, build, runtime, or cross-device work is involved
7. `docs/REPOSITORY.md` when git, GitHub, branches, releases, or remotes are involved
8. `docs/COORDINATION.md` when parallel sessions, branches, agents, devices, or handoffs are involved
9. `docs/LOG.md` only when historical detail is needed

When available, run `scripts/brief_memory.py --target /path/to/project` first to get a short current-state brief and task-based read recommendations.

## Task-Based Read Paths

Use the smallest read set that can safely answer the task:

- Continue implementation: `PROJECT_STATUS.md`, `docs/PRINCIPLES.md`, `docs/PLAN.md`
- Start broad code generation or large refactor: add `docs/VIBE_READINESS.md`
- Change direction or architecture: add `docs/DECISIONS.md`
- Work on setup, build, dependencies, or devices: add `docs/ENVIRONMENT.md`
- Work on git, GitHub, release, or branches: add `docs/REPOSITORY.md`
- Handle parallel work, handoff, or long-running tasks: add `docs/COORDINATION.md`
- Need business/domain terms or user mental model: add `docs/DOMAIN.md` if present
- Need historical reasoning: read `docs/LOG.md` selectively
- Project has `.projectmem/`: treat projectmem as dynamic event memory; use summaries/precheck results, not raw event logs
- Project has `conductor/`: treat it as an alternate static context system; do not create duplicate project-memory docs without confirming source-of-truth ownership
- Diagnose or compact project memory: read all memory docs, then report findings before patching

## Workflows

### Brief

Use `scripts/brief_memory.py --target /path/to/project` at the start of a session or before a handoff. It is read-only and prints current phase, latest conclusion, next step, blockers, risks, recommended files to read, and detected external memory systems.

### Initialize

Use `scripts/init_docs.py` to generate a small core plus selected addons:

```bash
python3 scripts/init_docs.py --target /path/to/project --project-name "Project Name" --project-kind "ios app" --domain "pin bead pattern generation"
```

Default behavior never overwrites existing files. Use `--force` only when the developer explicitly asks to regenerate or replace docs.

If the user gives only natural language, infer addons conservatively from project shape and platform/runtime:

- Project shape addons: `skill`, `app`, `system`, `library`, `docs`, `data-ai`
- Platform/runtime addons: `web`, `ios`, `cli`, `cloud`
- Domain context addon: `domain`

Do not create domain-specific addons such as `billing`, `medical`, or `inventory`. Business or technical domain knowledge belongs in `docs/DOMAIN.md`, `docs/CONTEXT.md`, `docs/PLAN.md`, or project-shape docs.

Always include core docs. Add only relevant addons; do not generate comprehensive docs for hypothetical future needs.

If a target already contains `conductor/`, `init_docs.py` stops by default. Ask the developer whether to keep Conductor as the static context source, migrate to project-memory, or explicitly mix both with a source-of-truth table. Use `--allow-conductor` only after that decision.

### Resume

Read the default files in order. Summarize current phase, durable decisions, active constraints, next action, and any stale or missing context before doing project work.

If `.projectmem/` exists, also consult projectmem summary/recent/precheck through its available CLI or MCP tools. Do not read raw event logs unless the developer explicitly asks for forensic detail.

If `conductor/` exists, read its index and relevant artifacts only after confirming whether Conductor or project-memory owns the static project context.

### Checkpoint

Update docs during normal work when the current state changes:

- `PROJECT_STATUS.md`: current phase, latest conclusion, next step, blockers
- `docs/LOG.md`: chronological progress details
- `docs/DECISIONS.md`: durable product, architecture, workflow, or operational decisions
- `docs/VIBE_READINESS.md`: product goal, stack/runtime, conventions, core contracts, red lines, AI permission boundaries
- `docs/ENVIRONMENT.md`: dependency, setup, version, path, or cross-device changes
- `docs/REPOSITORY.md`: branch, remote, GitHub, release, or generated-file rules
- `docs/COORDINATION.md`: active workstreams, handoffs, collision zones

Keep `PROJECT_STATUS.md` short. Move history into `docs/LOG.md`.

### Diagnose

Use `scripts/diagnose_memory.py --target /path/to/project` for a read-only health check. Diagnose missing files, stale dates, missing maintenance rules, oversized status files, inactive coordination with multiple branches, and incomplete environment/repository notes.

Report findings first. Apply patches only when the fix is routine and clearly implied, or after developer confirmation when meaning is ambiguous.

If any doc exceeds its context budget, explicitly recommend running compact. Do not compact automatically.

If `AGENTS.md` exceeds its context budget, recommend `migrate-agents` instead of ordinary compaction because `AGENTS.md` is always-on context.

If `.projectmem/` exists but the routing rules do not mention projectmem, recommend documenting the split: project-memory owns stable governance, projectmem owns dynamic events and precheck hints.

If both `conductor/` and project-memory docs exist, warn about static-context source-of-truth conflicts unless an explicit ownership table says which system owns product, technical, workflow, and work-unit facts.

### Vibe Readiness

Use `docs/VIBE_READINESS.md` as the readiness gate before large AI-assisted implementation. It should capture:

- One-sentence product goal: user, problem, success standard
- Stack/runtime: required, tested, preferred, and unknown versions
- Project structure and coding conventions
- Core models and contracts: domain model, API, config/schema, state model, file formats
- Development red lines: security, performance, error handling, privacy, compatibility
- AI permission boundaries: direct edits, plan-first areas, confirmation gates, forbidden actions, human review areas

This is not a requirement that every detail be finalized before exploration. Unknowns must be explicit so future sessions do not treat guesses as facts.

### Context Gate

Before broad implementation, large refactors, or work on a new feature track, verify:

- Product goal, success standard, stack/runtime, core contracts, red lines, and AI boundaries are current in `docs/VIBE_READINESS.md`
- `PROJECT_STATUS.md` next step matches the intended work
- Relevant durable decisions have been read from `docs/DECISIONS.md`
- Environment and repository rules are current when tooling, dependencies, CI, release, or branches are involved
- If `.projectmem/` exists, recent failures and precheck results have been considered
- If `conductor/` exists, static-context source-of-truth ownership is explicit

Context Gate produces warnings and update recommendations. It should not block the developer's request by itself.

### Projectmem Interop

Use projectmem as an optional dynamic event layer, not a replacement for project-memory docs.

- project-memory owns stable project governance: current status, principles, plans, durable decisions, environment, repository, coordination, and AI boundaries
- projectmem owns dynamic events: issues, attempts, fixes, file-level gotchas, and precheck hints
- Treat projectmem precheck as risk input. It may require explaining mitigation or changing approach, but it must not be the sole reason to refuse a user request
- At session end, use recent projectmem events to check whether `PROJECT_STATUS.md` is stale; summarize only durable current state, not every event
- Do not hand-edit projectmem raw event logs

### Conductor Detection

Treat `conductor/` from context-driven-development as an alternate static context system, not a default companion layer.

When `conductor/` exists:

1. Do not generate overlapping project-memory docs by default.
2. Ask whether to keep Conductor, migrate to project-memory, or explicitly mix them.
3. If mixing, record a source-of-truth table in `AGENTS.md` or project docs before continuing.
4. Prefer migration plans over automatic rewrites.

### Compact

Use `scripts/compact_memory.py --target /path/to/project` to produce a compaction plan. The script must not modify files.

Compaction is always two-step:

1. Present strategy: keep, summarize, archive, trim, do-not-change, risk.
2. Apply changes only after developer confirmation.

Preserve durable conclusions, accepted decisions, current plan, global principles, environment rules, repository rules, unresolved risks, and rationale for major decisions. Prefer moving historical detail to logs or archive notes over deletion.

Compact by information ownership, not just length:

- Always-on operating rules belong in `AGENTS.md`
- Current state belongs in `PROJECT_STATUS.md`
- Durable rules belong in `docs/PRINCIPLES.md`
- AI readiness, red lines, and AI permission boundaries belong in `docs/VIBE_READINESS.md`
- Current plan belongs in `docs/PLAN.md`
- Accepted decisions and alternatives belong in `docs/DECISIONS.md`
- Domain knowledge belongs in `docs/DOMAIN.md`
- Recent history belongs in `docs/LOG.md`
- Old history belongs in `docs/archive/`

### Handoff And Coordination

`docs/COORDINATION.md` is created by default with `Status: not active`. Activate it when work splits across sessions, branches, agents, devices, or long-running tasks.

Record workstreams, owners/sessions, branches, touched areas, dependencies, handoff status, and collision zones. Use it to prevent two sessions from editing the same project surface blindly.

### AGENTS.md Migration

Use `scripts/migrate_agents.py --target /path/to/project` when an existing `AGENTS.md` is long or contains project context that belongs in `docs/`.

The script is read-only. It produces a migration plan with:

- Keep in `AGENTS.md`: always-on operating rules and routing
- Move to docs: principles, environment, repository, coordination, decisions, logs, domain/context, vibe readiness
- Needs review: ambiguous or high-risk content

After developer confirmation, the agent may apply patches according to the plan, then run diagnosis. The preferred final state is a short `AGENTS.md` plus detailed source-of-truth docs. Snippet files are only a fallback when the developer does not allow editing the existing `AGENTS.md`.

## Safety Rules

- Do not store secrets in generated docs.
- Do not replace existing docs unless `--force` or explicit developer confirmation is present.
- Do not delete, archive, or compact durable decisions without confirmation.
- Do not make `PROJECT_STATUS.md` a long history log.
- Do not make `AGENTS.md` a project memory warehouse; keep it as a short always-on router.
- Prefer fewer high-signal files over comprehensive documentation hierarchies.
- Treat generated docs as source-of-truth ownership boundaries: put each fact in the file whose maintenance rules own it.
- Keep docs within their context budgets. Warn the developer and recommend compact when docs exceed budget or mix stale history with current state.
- Separate known facts, decisions, assumptions, open questions, and risks when recording non-trivial context.
- Do not maintain two static context systems without explicit source-of-truth ownership.
- Do not let external memory warnings become automatic refusal criteria.

## Resources

- `assets/templates/`: core and addon documentation templates.
- `scripts/init_docs.py`: initialize docs from templates.
- `scripts/brief_memory.py`: read-only current-state brief and read-path recommendation.
- `scripts/diagnose_memory.py`: read-only documentation health diagnosis.
- `scripts/compact_memory.py`: read-only compaction strategy generator.
- `scripts/migrate_agents.py`: read-only AGENTS.md migration planner.
- `references/maintenance-policy.md`: detailed maintenance and compaction policy.
