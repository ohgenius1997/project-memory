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
- Chronological narrative: `docs/LOG.md`

## Selective Loading

Prefer task-based read paths over reading all docs. Read all memory docs only when diagnosing, compacting, preparing a major handoff, or resolving cross-document conflicts.

## Addon Abstraction

Addons describe project shape and platform/runtime, not business domains:
- Project shape: `skill`, `app`, `system`, `library`, `docs`, `data-ai`
- Platform/runtime: `web`, `ios`, `cli`, `cloud`
- Domain knowledge: `domain`

Do not create one-off business-domain addons such as billing, medical, or inventory. Put those facts in `docs/DOMAIN.md` and project-specific specs.

## Update Policy

Update project memory during the task when a conclusion, state, or operational assumption changes. Keep updates scoped. Prefer appending concise entries to logs and decisions over rewriting history.

Warn the developer when a project memory doc exceeds its `max_lines` budget or mixes stale history with current state. Recommend compact, but do not run compaction changes without confirmation.

Before broad AI implementation, check `docs/VIBE_READINESS.md`. If product goal, stack/runtime, conventions, core contracts, development red lines, or AI permission boundaries are missing, warn the developer and either clarify or record the unknowns explicitly.

## AGENTS.md Policy

`AGENTS.md` is always-on context. Keep it short and limited to read routing, maintenance triggers, and hard operating rules.

If an existing `AGENTS.md` is long or contains detailed project memory, prefer developer-confirmed migration:

1. Run `scripts/migrate_agents.py` to produce a read-only migration plan.
2. Present what stays in `AGENTS.md`, what moves to docs, and what needs review.
3. After developer confirmation, apply patches manually as the agent.
4. Run diagnosis and record the migration in `docs/LOG.md` and, if durable, `docs/DECISIONS.md`.

Snippet files are a fallback only when the developer does not allow modifying existing `AGENTS.md`.

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
