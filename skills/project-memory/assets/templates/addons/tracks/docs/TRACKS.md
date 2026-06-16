# Tracks

## Memory Metadata
- owner: work-unit-registry
- read_when: feature work, parallel work, milestone tracking, acceptance criteria, or handoff requires work-unit state
- update_when: tracks are created, status changes, blockers change, acceptance criteria change, or tracks complete
- max_lines: 260
- stale_if: active track status, next step, owner, dependencies, or acceptance criteria changes

## Maintenance Rules
- Use this file as the registry for larger work units, not as a daily log.
- Keep detailed specs and plans in `docs/tracks/<track-id>/`.
- Keep current global next step in `PROJECT_STATUS.md`.
- Keep durable decisions in `docs/DECISIONS.md`.
- Close or archive stale tracks instead of leaving them ambiguous.

## Track Status Values
- proposed: candidate work not yet accepted
- active: currently being implemented
- blocked: cannot proceed without dependency or decision
- paused: intentionally deferred
- done: completed and validated
- archived: historical only

## Track Registry
| ID | Status | Priority | Owner | Scope | Spec | Plan | Last Updated | Next Step |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TBD | proposed | TBD | TBD | TBD | `docs/tracks/TBD/SPEC.md` | `docs/tracks/TBD/PLAN.md` | {{DATE}} | TBD |

## Cross-Track Dependencies
- TBD

## Risks
- TBD
