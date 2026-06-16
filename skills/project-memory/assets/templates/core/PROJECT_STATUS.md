# Project Status

## Memory Metadata
- owner: current-state-index
- read_when: every new session, before project work, before handoff
- update_when: phase, next action, blocker, risk, branch, or latest conclusion changes
- max_lines: 150
- stale_if: next action is completed, branch changes, blocker state changes, or major decision changes

## Maintenance Rules
- Read this file first in every new session.
- Keep this file short; target under 150 lines.
- Update when current phase, latest conclusion, next step, or blocker changes.
- Move historical detail to `docs/LOG.md`.
- Source of truth for current state only; do not store long rationale here.

## Current Snapshot
- Project: {{PROJECT_NAME}}
- Kind: {{PROJECT_KIND}}
- Domain: {{DOMAIN}}
- Initialized: {{DATE}}
- Current phase: initialization
- Latest conclusion: Project memory docs have been initialized for agent-facing context recovery.
- Next step: Replace placeholders with project-specific details and begin project work.
- Blockers: none recorded
- Current branch: TBD
- Active risks: none recorded

## Changed Since Last Checkpoint
- Initialized project memory docs.

## Read Next
- Continue implementation: `docs/PRINCIPLES.md`, `docs/PLAN.md`
- Change direction: `docs/DECISIONS.md`
- Setup/build work: `docs/ENVIRONMENT.md`
- Substantial code generation: `docs/VIBE_READINESS.md`
- Git/GitHub work: `docs/REPOSITORY.md`
- Domain context: `docs/DOMAIN.md` if present
- Feature tracks: `docs/TRACKS.md` if present

## Handoff
- Last completed: initialized project memory docs
- In progress: fill project-specific placeholders
- Validation done: initial files generated
- Known risks: placeholders still need project-specific content

## Important Links
- Principles: `docs/PRINCIPLES.md`
- Plan: `docs/PLAN.md`
- Decisions: `docs/DECISIONS.md`
- Environment: `docs/ENVIRONMENT.md`
- Repository: `docs/REPOSITORY.md`
- Coordination: `docs/COORDINATION.md`
- Tracks: `docs/TRACKS.md` if present
- Log: `docs/LOG.md`
