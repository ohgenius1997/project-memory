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
- Current phase: tracks/context-gate/bridge/inspect iteration implemented
- Current branch: `main`
- Latest conclusion: next-step improvements should stay low-complexity: optional tracks, stricter diagnostics, read-only dynamic-memory bridge, and brownfield inspection.
- Next step: monitor GitHub Actions after push and dogfood tracks/context-gate/bridge/inspect workflows in a real project.
- Blockers: none
- Active risks: projectmem bridge is best-effort across possible CLI variants and must remain advisory/read-only.

## Changed Since Last Checkpoint
- Initialized project memory docs for this repository.
- Archived obsolete origin context to `docs/archive/origin-scope-pivot.md`.
- Rewrote active project context around the `project-memory` skill.
- Added open-source repository files: `README.md`, `LICENSE`, `.gitignore`.
- Validated script syntax, skill metadata, initialization dry-run, and project memory diagnosis.
- Added `origin` remote and pushed `main` to GitHub.
- Added projectmem interop rules, conductor detection rules, context gate guidance, brief workflow, and CI validation.
- Synced updated skill source to local Codex skills install.
- Added optional tracks addon templates, `diagnose_memory.py --context-gate`, read-only `memory_bridge.py`, and read-only `inspect_project.py`.
- Extended README, skill instructions, templates, and CI smoke coverage for the new workflows.
- Validated repository source and installed skill copy with script syntax checks, smoke tests, and official skill validation.

## Read Next
- Continue implementation: `docs/PRINCIPLES.md`, `docs/PLAN.md`
- Broad code generation or refactor: `docs/VIBE_READINESS.md`
- GitHub publishing: `docs/REPOSITORY.md`
- Skill behavior: `docs/SKILL_SPEC.md`, `docs/WORKFLOWS.md`
- Optional dynamic memory: `memory_bridge.py` workflow in `docs/WORKFLOWS.md`
- Historical origin only if explicitly needed: `docs/archive/origin-scope-pivot.md`

## Handoff
- Last completed: tracks/context-gate/bridge/inspect implementation, validation, local install sync, commit, and push.
- In progress: none
- Validation done: `py_compile`, init smoke with tracks, brief, diagnosis with `--context-gate`, inspect, memory bridge detect/summary/precheck fallback, conductor guard, official `quick_validate.py` for repo and installed skill.
- Known risks: new bridge command compatibility is best-effort because projectmem CLI shapes may vary.
