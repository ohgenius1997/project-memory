---
name: project-memory
description: AGENTS-first project context router and lightweight governance bootstrap for AI-assisted coding projects. Use when the user asks to initialize or maintain AGENTS.md project context, create a project memory/router, set up agent-facing rules, diagnose context bloat, recommend minimal/standard/governed profile upgrades, coordinate with agentmemory, migrate long AGENTS/CLAUDE/README/docs context, propose PROJECT_STATUS.md syncs, or manage current-state/decision/environment/coordination docs for Codex or other coding agents.
---

# Project Memory

## Core Contract

Create a lightweight AGENTS-first router, not a full memory runtime.

Optimize for:
- little always-on context
- strong task-based routing
- weak ceremony
- dynamic/episodic memory outsourced to agentmemory

Do not build or maintain a large Markdown documentation system by default. Do not install agentmemory, run global hooks, create MCP servers, or implement vector/episodic memory. Recommend agentmemory as the single dynamic-memory companion and document the ownership split.

## Profiles

Use the smallest profile that fits the project.

- `minimal` (default): `AGENTS.md` only. Use for small projects, exploration, or projects with agentmemory.
- `standard`: `AGENTS.md`, `PROJECT_STATUS.md`, `docs/DECISIONS.md`. Use when current state and durable decisions must survive sessions.
- `governed`: standard plus `docs/ENVIRONMENT.md`, `docs/COORDINATION.md`. Use only for cross-device setup, multiple branches, multiple sessions, or handoff.

Never auto-upgrade profiles. Diagnose complexity and recommend an upgrade with rationale, added files, and maintenance cost. Apply the upgrade only after developer confirmation.

## Git Tracking Policy

Do not decide globally that all memory files must be committed or ignored. Git tracking is a target-project policy.

Default guidance:
- `AGENTS.md` is usually committed when repository rules should travel across branches, devices, and contributors.
- `PROJECT_STATUS.md` and `docs/DECISIONS.md` are usually committed when current state and durable decisions need branch/cross-device continuity.
- `docs/ENVIRONMENT.md` is committed only for non-secret, stable setup facts.
- `docs/COORDINATION.md`, sparse `docs/LOG.md`, and dynamic-memory exports are project-specific; follow the developer's policy and `.gitignore`.
- Never commit secrets, private tokens, credentials, large raw session transcripts, or raw dynamic-memory dumps.

When initializing or diagnosing, describe the tradeoff instead of forcing a repo-wide answer.

## Read Rules

Start with `AGENTS.md`. It is the always-on router.

Then use the smallest task-specific context:
- Ordinary development: `AGENTS.md` plus agentmemory relevant memory if available.
- Continue long-running work: add `PROJECT_STATUS.md` if present.
- Change architecture, product direction, or workflow policy: add `docs/DECISIONS.md` if present.
- Work on dependencies, setup, CI, build, runtime, or cross-device assumptions: add `docs/ENVIRONMENT.md` if present.
- Handle multi-session, multi-branch, owner, collision, or handoff state: add `docs/COORDINATION.md` if present.
- Need historical process context: use agentmemory; read `docs/LOG.md` only as sparse fallback if present.

Before mutating repository files, consult `AGENTS.md` and identify the context sources used in a progress update or final response. Keep this acknowledgement concise.

## Initialize

Use `scripts/init_docs.py`.

```bash
python3 scripts/init_docs.py \
  --target /path/to/project \
  --project-name "My Project" \
  --project-kind "ios app" \
  --domain "pin bead pattern generation"
```

Defaults:
- `--profile minimal`
- `--dynamic-memory agentmemory`
- no addons
- no overwrite of existing files

Useful variants:

```bash
python3 scripts/init_docs.py --target /path/to/project --profile standard
python3 scripts/init_docs.py --target /path/to/project --profile governed
python3 scripts/init_docs.py --target /path/to/project --dynamic-memory none --profile standard
```

Use `--fallback-log` only when the developer wants sparse checkpoint history without agentmemory. Use `--force` only after explicit confirmation.

## Checkpoint

Update project-memory docs only when stable facts change.

- `AGENTS.md`: routing, stable operating rules, AI boundaries, and dynamic-memory ownership.
- `PROJECT_STATUS.md`: current phase, latest conclusion, next step, blockers, branch, and active risks.
- `docs/DECISIONS.md`: durable decisions, rationale, alternatives, and consequences.
- `docs/ENVIRONMENT.md`: stable setup, dependencies, CI, device, runtime, or cross-machine facts.
- `docs/COORDINATION.md`: active multi-session or multi-branch handoff/collision state.
- `docs/LOG.md`: sparse checkpoint fallback only when agentmemory is unavailable.

Do not write ordinary attempts, transient failures, debugging traces, file-level gotchas, or session transcripts into project-memory docs. Those belong in agentmemory.

## Diagnose

Use `scripts/diagnose_memory.py --target /path/to/project` for read-only health checks.

It should report:
- missing required files for the detected profile
- oversized or history-heavy `AGENTS.md`
- missing agentmemory ownership split
- `PROJECT_STATUS.md` acting like a log
- `docs/LOG.md` overuse when agentmemory is declared
- minimal-to-standard or standard-to-governed upgrade signals
- coordination state that may need activation

Use `--context-gate` before broad implementation or handoff. Context Gate warns; it does not block the developer's request by itself.

## Status Sync Proposal

Use `scripts/status_sync_proposal.py` to propose, not apply, `PROJECT_STATUS.md` updates.

```bash
python3 scripts/status_sync_proposal.py --target /path/to/project
python3 scripts/status_sync_proposal.py --target /path/to/project --agentmemory-summary summary.md
```

If agentmemory output is available, pass a summary file or `--agentmemory-summary -` via stdin. If not, the script falls back to git state and sparse `docs/LOG.md`. Apply the suggested status fields only after developer confirmation.

Do not hard-code agentmemory CLI/API calls unless the developer confirms a stable local command. Prefer stdin or an explicitly supplied summary file for now.

## Migration

Use read-only planners first.

- `scripts/migrate_agents.py`: classify long `AGENTS.md` content into keep/move/review buckets.
- `scripts/migrate_context.py`: classify README, CLAUDE.md, old docs, TODOs, roadmaps, and handoff notes.
- `scripts/compact_memory.py`: propose compaction; never compact automatically.

Migration target:
- keep `AGENTS.md` short as the router
- move current state to `PROJECT_STATUS.md`
- move durable decisions to `docs/DECISIONS.md`
- move setup/coordination facts only when governed profile is justified
- route process history to agentmemory or sparse fallback `docs/LOG.md`

## Coordination Boundary

In `docs/COORDINATION.md`, an agent may update only its own session/workstream state unless the developer asks otherwise. Do not assign owners, lock or unlock another session's work, remove another session's handoff, or declare another session complete without confirmation.

## Resources

- `assets/templates/`: AGENTS-first profile templates and optional legacy addons.
- `scripts/init_docs.py`: initialize minimal, standard, or governed profile files.
- `scripts/brief_memory.py`: read-only context brief and recommended read path.
- `scripts/diagnose_memory.py`: read-only profile and context health diagnosis.
- `scripts/status_sync_proposal.py`: read-only current-status sync proposal.
- `scripts/migrate_agents.py`: read-only AGENTS.md migration planner.
- `scripts/migrate_context.py`: read-only brownfield context classifier.
- `scripts/compact_memory.py`: read-only compaction strategy generator.
