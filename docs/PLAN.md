# Plan

## Memory Metadata
- owner: current-plan-and-roadmap
- read_when: planning, implementation, scope decisions, milestone changes
- update_when: current approach, milestones, scope, next actions, or roadmap changes
- max_lines: 200
- stale_if: current phase, project output type, or accepted architecture changes

## Maintenance Rules
- Use this file for the current approach, roadmap, milestones, and scope boundaries.
- Update when the project plan or phase changes.
- Keep historical plans only if they explain current choices; otherwise move history to `LOG.md` or `DECISIONS.md`.
- Do not record environment setup here; use `ENVIRONMENT.md`.

## Known Facts
- The skill source lives under `skills/project-memory`.
- The repository has been pushed to public GitHub after docs cleanup and validation.
- The skill has already been installed locally once for dogfooding.
- Current optimization direction: add read-only brief, projectmem interop rules, conductor detection, and stronger diagnosis without turning the skill into a runtime framework.

## Decisions
- Publish this repository as the `project-memory` skill project.
- Use MIT license for broad reuse.
- Keep helper scripts dependency-light and runnable with Python standard library.
- Treat projectmem as an optional dynamic event layer.
- Treat context-driven-development/Conductor as an alternate static context system, not a default companion.

## Assumptions
- Initial public users will copy or install the skill manually rather than via a package manager.
- Public users will initially install by copying the skill source.

## Open Questions
- Whether to add CI for `py_compile` and skill validation.
- Whether to add examples or screenshots after the first public push.

## Risks
- The public repository may imply stable API guarantees before the skill has real external usage.

## Current Approach
- Keep the repository small and focused.
- Treat `README.md` as the public entrypoint.
- Treat `PROJECT_STATUS.md` and `docs/` as agent-facing project memory.
- Implement improvements in phases: rules first, diagnosis/brief next, optional tracks and bridges later.

## Milestones
- [x] Build `project-memory` skill.
- [x] Rename from `init-project-memory`.
- [x] Install locally for dogfooding.
- [x] Archive obsolete origin context.
- [x] Add public repository metadata files.
- [x] Push to GitHub.
- [x] Add Phase 0/1/2/3 improvements: CI, interop rules, diagnosis checks, and brief script.
- [ ] Sync local installed skill and push updated release.
- [ ] Add optional tracks addon and context gate diagnostics.
- [ ] Add read-only projectmem bridge.
- [ ] Add brownfield inspect light mode.

## In Scope
- Skill templates and scripts.
- Project-memory documentation workflows.
- Vibe readiness and AGENTS migration planning.
- Read-only brief, diagnosis, interop routing, and source-of-truth checks.
- Public README, license, and repository hygiene.

## Out Of Scope
- Unrelated domain-specific skill development.
- Package registry release.
- Automatic background document maintenance.
- MCP server, daemon, watcher, git hooks, or automatic projectmem writes.

## Next Actions
- Validate current Phase 0-3 implementation.
- Sync local installed skill after validation.
- Commit and push.
