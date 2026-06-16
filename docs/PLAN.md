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
- Current optimization direction: add small, read-only workflow helpers without turning the skill into a runtime framework.

## Decisions
- Publish this repository as the `project-memory` skill project.
- Use MIT license for broad reuse.
- Keep helper scripts dependency-light and runnable with Python standard library.
- Treat projectmem as an optional dynamic event layer.
- Treat `conductor/` as an external static context directory and conflict signal, not a compatibility or migration target.
- Keep feature tracks optional and lightweight; they are an index for larger work units, not a replacement for `PROJECT_STATUS.md` or `docs/PLAN.md`.
- Define migration as Existing Context Migration: classify useful historical context from `AGENTS.md`, README, old docs, TODOs, roadmaps, changelogs, handoff notes, or user-specified files into project-memory docs.

## Assumptions
- Initial public users will copy or install the skill manually rather than via a package manager.
- Public users will initially install by copying the skill source.

## Open Questions
- Whether to add examples or screenshots after more dogfooding.
- Whether projectmem CLI support needs a stable adapter after observing real-world usage.
- Whether `migrate_context.py` should eventually produce patch-ready drafts after more dogfooding.

## Risks
- The public repository may imply stable API guarantees before the skill has real external usage.
- Existing-context migration classification is heuristic and must remain advisory until more real projects are tested.

## Current Approach
- Keep the repository small and focused.
- Treat `README.md` as the public entrypoint.
- Treat `PROJECT_STATUS.md` and `docs/` as agent-facing project memory.
- Implement improvements in phases: rules first, diagnosis/brief next, optional tracks and read-only bridges, then real-project dogfood and generic migration.

## Milestones
- [x] Build `project-memory` skill.
- [x] Rename from `init-project-memory`.
- [x] Install locally for dogfooding.
- [x] Archive obsolete origin context.
- [x] Add public repository metadata files.
- [x] Push to GitHub.
- [x] Add Phase 0/1/2/3 improvements: CI, interop rules, diagnosis checks, and brief script.
- [x] Sync local installed skill and push Phase 0/1/2/3 release.
- [x] Add optional tracks addon and context gate diagnostics.
- [x] Add read-only projectmem bridge.
- [x] Add brownfield inspect light mode.
- [x] Validate, sync local installed skill, commit, and push current iteration.
- [x] Phase 7: dogfood on `PDY_2` or another real project.
- [x] Phase 8: implement generic Existing Context Migration improvements; do not adapt Conductor.
- [ ] Validate, sync local installed skill, commit, and push Phase 7/8 dogfood fixes.

## In Scope
- Skill templates and scripts.
- Project-memory documentation workflows.
- Vibe readiness and AGENTS migration planning.
- Read-only brief, diagnosis, interop routing, and source-of-truth checks.
- Optional feature-track templates for larger work units.
- Read-only dynamic-memory bridge and existing-project inspection.
- Generic existing-context migration design and diagnostics.
- Public README, license, and repository hygiene.

## Out Of Scope
- Unrelated domain-specific skill development.
- Package registry release.
- Automatic background document maintenance.
- MCP server, daemon, watcher, git hooks, or automatic projectmem writes.
- Conductor compatibility, Conductor parsing, Conductor migration, or Conductor synchronization.

## Next Actions
- Run full validation for dogfood fixes.
- Sync local installed skill.
- Commit and push.
