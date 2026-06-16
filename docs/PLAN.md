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
- The repository is ready for public GitHub setup after docs cleanup and validation.
- The skill has already been installed locally once for dogfooding.

## Decisions
- Publish this repository as the `project-memory` skill project.
- Use MIT license for broad reuse.
- Keep helper scripts dependency-light and runnable with Python standard library.

## Assumptions
- Initial public users will copy or install the skill manually rather than via a package manager.
- The GitHub repository will be created empty, then local history will be pushed.

## Open Questions
- Whether to add CI for `py_compile` and skill validation.
- Whether to add examples or screenshots after the first public push.

## Risks
- The public repository may imply stable API guarantees before the skill has real external usage.

## Current Approach
- Keep the repository small and focused.
- Treat `README.md` as the public entrypoint.
- Treat `PROJECT_STATUS.md` and `docs/` as agent-facing project memory.

## Milestones
- [x] Build `project-memory` skill.
- [x] Rename from `init-project-memory`.
- [x] Install locally for dogfooding.
- [x] Archive obsolete origin context.
- [x] Add public repository metadata files.
- [ ] Push to GitHub.
- [ ] Verify GitHub rendering and repository metadata.

## In Scope
- Skill templates and scripts.
- Project-memory documentation workflows.
- Vibe readiness and AGENTS migration planning.
- Public README, license, and repository hygiene.

## Out Of Scope
- Unrelated domain-specific skill development.
- Package registry release.
- Automatic background document maintenance.

## Next Actions
- Create empty GitHub repository if not already created.
- Add remote.
- Push `main`.
- Review public README and topics.
