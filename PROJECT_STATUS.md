# project-memory Status

## Memory Metadata
- owner: current-state-index
- read_when: every new session, before project work, before handoff
- update_when: phase, next action, blocker, risk, branch, or latest conclusion changes
- max_lines: 150
- stale_if: next action is completed, branch changes, blocker state changes, or major decision changes

## Maintenance Rules
- Read this file first in every new session.
- Keep this file short; target under 150 lines.
- Update when current phase, latest conclusion, next step, blocker, or release state changes.
- Move historical detail to `docs/LOG.md`.
- Keep obsolete origin context out of active project memory; it is archived at `docs/archive/origin-scope-pivot.md`.

## Current Snapshot
- Project: `project-memory`
- Kind: Codex skill
- Domain: agent-facing project memory management
- Current phase: Phase 0-3 improvements implemented
- Current branch: `main`
- Latest conclusion: keep `project-memory` lightweight while adding read-only brief, interop routing, and context-risk diagnosis.
- Next step: commit and push Phase 0-3 improvements, then plan optional tracks/context-gate diagnostics.
- Blockers: none
- Active risks: new projectmem/conductor rules must stay advisory and not turn into heavy runtime coupling.

## Changed Since Last Checkpoint
- Initialized project memory docs for this repository.
- Archived obsolete origin context to `docs/archive/origin-scope-pivot.md`.
- Rewrote active project context around the `project-memory` skill.
- Added open-source repository files: `README.md`, `LICENSE`, `.gitignore`.
- Validated script syntax, skill metadata, initialization dry-run, and project memory diagnosis.
- Added `origin` remote and pushed `main` to GitHub.
- Added projectmem interop rules, conductor detection rules, context gate guidance, brief workflow, and CI validation.
- Synced updated skill source to local Codex skills install.

## Read Next
- Continue implementation: `docs/PRINCIPLES.md`, `docs/PLAN.md`
- Broad code generation or refactor: `docs/VIBE_READINESS.md`
- GitHub publishing: `docs/REPOSITORY.md`
- Skill behavior: `docs/SKILL_SPEC.md`, `docs/WORKFLOWS.md`
- Historical origin only if explicitly needed: `docs/archive/origin-scope-pivot.md`

## Handoff
- Last completed: Phase 0-3 implementation and local install sync.
- In progress: commit and push.
- Validation done: `py_compile`, `brief_memory.py`, `diagnose_memory.py`, init smoke test, CI YAML parse, official `quick_validate.py` for repo and installed skill.
- Known risks: optional tracks/context-gate diagnostics are not implemented yet.
