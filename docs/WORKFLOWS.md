# Workflows

## Memory Metadata
- owner: repeatable-agent-workflows
- read_when: executing or modifying repeatable project workflows
- update_when: workflow steps, safety checks, validation, or handoff behavior changes
- max_lines: 260
- stale_if: implemented workflow differs from documented workflow

## Maintenance Rules
- Use this file for repeatable agent workflows that the project must preserve.
- Update when the sequence of work, safety checks, or handoff behavior changes.
- Keep examples concise and realistic.
- Do not duplicate current roadmap details from `PLAN.md`.

## Workflow Index
- Inspect existing project
- Generate project memory brief
- Initialize project memory
- Diagnose project memory
- Run Context Gate
- Use dynamic memory bridge
- Generate compaction plan
- Plan AGENTS.md migration
- Plan existing-context migration
- Prepare public repository release

## Inspect Existing Project
1. Run `scripts/inspect_project.py --target <project>`.
2. Use detected languages, config files, existing memory systems, and recommended addons as input.
3. Confirm before initializing if external static context directories such as `conductor/`, existing docs, or long `AGENTS.md` already exist.
4. Do not treat inspection output as a full architecture analysis.

## Generate Project Memory Brief
1. Run `scripts/brief_memory.py --target <project>`.
2. Use the recommended read set instead of loading all docs.
3. If projectmem is detected, use summaries/precheck rather than raw logs.
4. If `conductor/` is detected, treat it as an external static context directory and do not parse or migrate it by default.

## Initialize Project Memory
1. Run `scripts/init_docs.py` with project name, kind, domain, and addons.
2. Do not overwrite existing files unless explicitly approved.
3. Fill `PROJECT_STATUS.md`, `docs/CONTEXT.md`, `docs/PLAN.md`, `docs/VIBE_READINESS.md`, and `docs/REPOSITORY.md`.
4. Run diagnosis and address important warnings.

## Diagnose Project Memory
1. Run `scripts/diagnose_memory.py --target <project>`.
2. Report findings before applying changes.
3. Check for context-budget issues, stale setup/repository notes, projectmem routing, and external static context conflicts.
4. Recommend compact or migrate-agents when budgets are exceeded.
5. Patch only routine, clear updates unless the developer confirms larger changes.

## Run Context Gate
1. Run `scripts/diagnose_memory.py --target <project> --context-gate`.
2. Check whether current status fields and active track next steps are concrete.
3. Treat warnings as update recommendations, not automatic blockers.
4. If warnings expose ambiguous product, stack, contract, or permission facts, ask the developer before broad implementation.

## Use Dynamic Memory Bridge
1. Run `scripts/memory_bridge.py detect --target <project>`.
2. If projectmem-style memory exists, run `summary` or `precheck <file>` as needed.
3. Treat returned output as advisory risk input.
4. Do not read or edit raw event logs unless the developer explicitly asks for forensic detail.

## Generate Compaction Plan
1. Run `scripts/compact_memory.py --target <project>`.
2. Present keep/summarize/archive/trim/do-not-change recommendations.
3. Ask for developer confirmation before applying any compaction.
4. Preserve durable decisions and active operational context.

## Plan AGENTS.md Migration
1. Run `scripts/migrate_agents.py --target <project>`.
2. Present keep/move/review classifications.
3. Ask for developer confirmation before rewriting `AGENTS.md`.
4. After migration, run diagnosis and log the migration.

## Plan Existing-Context Migration
1. Run `scripts/migrate_context.py --target <project>`.
2. Review suggested sources such as `AGENTS.md`, README, old docs, TODOs, roadmaps, changelogs, handoff notes, and developer-specified files.
3. Classify content into project-memory targets: `AGENTS.md`, `PROJECT_STATUS.md`, `docs/PLAN.md`, `docs/DECISIONS.md`, `docs/ENVIRONMENT.md`, `docs/REPOSITORY.md`, `docs/COORDINATION.md`, `docs/LOG.md`, and `docs/DOMAIN.md` when present.
4. Present the read-only migration plan before applying patches.
5. Do not special-case `conductor/`; it is an external static context conflict signal, not a supported migration format.

## Prepare Public Repository Release
1. Confirm README, license, ignore rules, and project status are public-safe.
2. Run script syntax checks and skill validation.
3. Confirm git status is clean after committing.
4. Add remote and push to the empty GitHub repository.
