# Project Memory Maintenance Policy

Use this reference when diagnosing, compacting, or repairing generated project memory docs.

## Source Of Truth

- Current state and next action: `PROJECT_STATUS.md`
- Global operating rules: `docs/PRINCIPLES.md`
- Current approach and roadmap: `docs/PLAN.md`
- Vibe coding readiness, development red lines, AI permissions: `docs/VIBE_READINESS.md`
- Durable decisions and rationale: `docs/DECISIONS.md`
- Domain terms and business/professional rules: `docs/DOMAIN.md`
- Setup and cross-device configuration: `docs/ENVIRONMENT.md`
- Git/GitHub/release rules: `docs/REPOSITORY.md`
- Parallel work and handoff state: `docs/COORDINATION.md`
- Feature tracks and larger work-unit state: `docs/TRACKS.md`
- Chronological narrative: `docs/LOG.md`

## Selective Loading

Prefer task-based read paths over reading all docs. Read all memory docs only when diagnosing, compacting, preparing a major handoff, or resolving cross-document conflicts.

Use `scripts/brief_memory.py` at session start when present. It provides a short current-state summary, recommended read set, and external-memory warnings without loading every project document.

## Addon Abstraction

Addons describe project shape and platform/runtime, not business domains:
- Project shape: `skill`, `app`, `system`, `library`, `docs`, `data-ai`
- Platform/runtime: `web`, `ios`, `cli`, `cloud`
- Context: `domain`, `tracks`

Do not create one-off business-domain addons such as billing, medical, or inventory. Put those facts in `docs/DOMAIN.md` and project-specific specs.

Use `tracks` only when the project has multi-session, multi-branch, or multi-day work units. Do not create tracks for every small task.

## External Memory Interop

Projectmem is a dynamic event memory layer. Use it for issues, attempts, fixes, file-level gotchas, and precheck hints. Do not hand-edit raw projectmem event logs. At session end, use recent projectmem events to check whether `PROJECT_STATUS.md` is stale, but do not mechanically copy every event into project-memory docs.

When available, prefer `scripts/memory_bridge.py detect|summary|precheck` for projectmem-style memory. The bridge is read-only and best-effort; if it cannot read a summary or precheck result, continue with project-memory docs and local code inspection.

Precheck output is risk evidence. It can require mitigation, extra testing, or plan changes, but it must not be the only reason to refuse a user request.

`conductor/` from context-driven-development is an external static context directory. Treat it as a conflict signal, not a compatibility target. If `conductor/` exists:

1. Do not create overlapping project-memory docs by default.
2. Do not parse, migrate, synchronize, or adapt Conductor-specific files.
3. Ask whether the developer wants to proceed with project-memory despite the external static context directory.
4. If proceeding, keep any migration generic: classify existing `AGENTS.md`, README, old docs, roadmaps, changelogs, handoff notes, or developer-specified files into project-memory docs.

Avoid long-term dual ownership of the same product, technical, workflow, or work-unit facts.

## Update Policy

Update project memory during the task when a conclusion, state, or operational assumption changes. Keep updates scoped. Prefer appending concise entries to logs and decisions over rewriting history.

Warn the developer when a project memory doc exceeds its `max_lines` budget or mixes stale history with current state. Recommend compact, but do not run compaction changes without confirmation.

Before broad AI implementation, check `docs/VIBE_READINESS.md`. If product goal, stack/runtime, conventions, core contracts, development red lines, or AI permission boundaries are missing, warn the developer and either clarify or record the unknowns explicitly.

Before broad implementation or large refactors, also run a context gate:
- `PROJECT_STATUS.md` next step should match the intended task.
- Active `docs/TRACKS.md` entries should have concrete next steps and recent `Last Updated` dates.
- Relevant durable decisions should be reviewed.
- Environment and repository docs should be current when tooling, dependency, CI, release, branch, or cross-device work is involved.
- If projectmem exists, recent failures and precheck hints should be considered.
- If Conductor exists, the developer should explicitly choose whether to proceed despite the external static context directory.

Common anti-patterns:
- Stale context: docs no longer match code or current plan.
- Context sprawl: multiple docs own the same fact.
- Implicit context: repeatedly used knowledge is not captured anywhere.
- Over-specification: docs become too detailed to maintain.

## AGENTS.md Policy

`AGENTS.md` is always-on context. Keep it short and limited to read routing, maintenance triggers, and hard operating rules.

If an existing `AGENTS.md` is long or contains detailed project memory, prefer developer-confirmed migration:

1. Run `scripts/migrate_agents.py` to produce a read-only migration plan.
2. Present what stays in `AGENTS.md`, what moves to docs, and what needs review.
3. After developer confirmation, apply patches manually as the agent.
4. Run diagnosis and record the migration in `docs/LOG.md` and, if durable, `docs/DECISIONS.md`.

Snippet files are a fallback only when the developer does not allow modifying existing `AGENTS.md`.

## Existing Context Migration

Existing-context migration is for brownfield projects with useful context scattered across `AGENTS.md`, README, old docs, TODO files, roadmaps, changelogs, handoff notes, or developer-specified files.

Start with `scripts/migrate_context.py --target <project>` when available. It is read-only and classifies legacy sources into suggested project-memory targets.

Migration should classify facts by project-memory ownership:
- Always-on operating rules: `AGENTS.md`
- Current state: `PROJECT_STATUS.md`
- Current approach and roadmap: `docs/PLAN.md`
- Durable decisions and rationale: `docs/DECISIONS.md`
- Setup and cross-device facts: `docs/ENVIRONMENT.md`
- Git, GitHub, CI, release facts: `docs/REPOSITORY.md`
- Handoff and parallel-work facts: `docs/COORDINATION.md`
- Chronological history: `docs/LOG.md`
- Domain terminology and rules: `docs/DOMAIN.md`

This workflow is not compatibility with a third-party context framework. Conductor remains a detected conflict signal only.

## Compaction Policy

Compaction is developer-triggered and confirmation-gated. First produce a plan.

Keep:
- Current conclusions, accepted decisions, current plan, principles, environment/repository rules, unresolved risks.

Summarize:
- Repeated discussion, completed routine progress, obsolete intermediate plans, long exploratory logs.

Archive:
- Non-adopted alternatives that may still explain future context.

Trim:
- Duplicated facts outside their source-of-truth file and stale `PROJECT_STATUS.md` history.

Never silently delete:
- Decision rationale, active constraints, unresolved blockers, setup details, repository rules, or handoff state.

Compaction should produce layers:
- Current state: `PROJECT_STATUS.md`
- Durable why: `docs/DECISIONS.md`
- Recent history: `docs/LOG.md`
- Old history: `docs/archive/`
- Domain facts: `docs/DOMAIN.md`
- Operational facts: `docs/ENVIRONMENT.md`, `docs/REPOSITORY.md`, `docs/COORDINATION.md`
- AI readiness and red lines: `docs/VIBE_READINESS.md`
