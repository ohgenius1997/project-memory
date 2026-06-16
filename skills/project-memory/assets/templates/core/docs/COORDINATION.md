# Coordination

## Memory Metadata
- owner: coordination-handoff-workstreams
- read_when: parallel sessions, parallel branches, cross-device work, long-running tasks, or handoff
- update_when: work splits, branches diverge, ownership changes, touched areas change, or handoff state changes
- max_lines: 220
- stale_if: active branches, workstreams, devices, or handoff state changes

## Maintenance Rules
- This file is the source of truth for multi-session, multi-branch, multi-agent, cross-device, or long-running task coordination.
- Keep `Status: not active` for single-stream work.
- Activate this file when work splits or handoff state matters.
- Record collision zones before parallel editing begins.

## Status
- Status: not active
- Mode: single-stream
- Source of truth: `PROJECT_STATUS.md`
- Last reviewed: {{DATE}}

## Enable When
- Multiple Codex sessions work in parallel.
- Multiple branches represent separate scopes.
- Work moves across devices and local state may diverge.
- A task needs handoff between a human and an agent.
- A long-running experiment or background task needs tracking.

## Workstreams
| ID | Owner/Session | Branch | Scope | Status | Dependencies | Touches | Handoff |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Collision Zones
- TBD

## Handoffs
- TBD

## Sync Rules
- Update after branch changes that affect active work.
- Update before ending a session with incomplete work.
- Update when ownership or dependencies change.
