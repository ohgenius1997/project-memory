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
- Current phase: Phase 7/8 PDY_2 dogfood fixes validated
- Current branch: `main`
- Latest conclusion: PDY_2 dogfood confirmed the key brownfield case: legacy docs should be classified as Existing Context Migration sources, not treated as malformed project-memory docs.
- Next step: push the Phase 7/8 dogfood fixes.
- Blockers: none
- Active risks: `migrate_context.py` uses heuristic classification; output should remain advisory and developer-confirmed.

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
- Began Phase 7/8: accepted `PDY_2` as the intended real-project dogfood target and clarified migration scope as generic existing-context migration.
- Searched common local paths for `PDY_2`; it was not found yet.
- Found `PDY_2` at `/Users/bytedance/.codex/worktrees/8211/PDY_2` and ran read-only dogfood checks.
- Updated diagnosis to treat old docs as legacy context sources instead of warning per old doc.
- Updated inspection to detect legacy context sources, detached HEAD, Xcode project names, and tracks addon cues.
- Added read-only `migrate_context.py` for generic existing-context migration plans.

## Read Next
- Continue implementation: `docs/PRINCIPLES.md`, `docs/PLAN.md`
- Broad code generation or refactor: `docs/VIBE_READINESS.md`
- GitHub publishing: `docs/REPOSITORY.md`
- Skill behavior: `docs/SKILL_SPEC.md`, `docs/WORKFLOWS.md`
- Optional dynamic memory: `memory_bridge.py` workflow in `docs/WORKFLOWS.md`
- Historical origin only if explicitly needed: `docs/archive/origin-scope-pivot.md`

## Handoff
- Last completed: tracks/context-gate/bridge/inspect implementation, validation, local install sync, commit, and push.
- In progress: push dogfood fixes.
- Validation done: `py_compile`, official `quick_validate.py`, fresh init smoke, smoke `brief_memory.py`, `diagnose_memory.py --context-gate`, `inspect_project.py`, `memory_bridge.py detect`, `migrate_context.py`; PDY_2 read-only `inspect_project.py`, `diagnose_memory.py --context-gate`, `migrate_agents.py`, `migrate_context.py`; whitespace check.
- Known risks: new bridge command compatibility is best-effort because projectmem CLI shapes may vary; migration classification is heuristic.
