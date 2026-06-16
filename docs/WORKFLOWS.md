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
- Generate project memory brief
- Initialize project memory
- Diagnose project memory
- Generate compaction plan
- Plan AGENTS.md migration
- Prepare public repository release

## Generate Project Memory Brief
1. Run `scripts/brief_memory.py --target <project>`.
2. Use the recommended read set instead of loading all docs.
3. If projectmem is detected, use summaries/precheck rather than raw logs.
4. If Conductor is detected, confirm static context ownership before editing overlapping docs.

## Initialize Project Memory
1. Run `scripts/init_docs.py` with project name, kind, domain, and addons.
2. Do not overwrite existing files unless explicitly approved.
3. Fill `PROJECT_STATUS.md`, `docs/CONTEXT.md`, `docs/PLAN.md`, `docs/VIBE_READINESS.md`, and `docs/REPOSITORY.md`.
4. Run diagnosis and address important warnings.

## Diagnose Project Memory
1. Run `scripts/diagnose_memory.py --target <project>`.
2. Report findings before applying changes.
3. Check for context-budget issues, stale setup/repository notes, projectmem routing, and Conductor source-of-truth conflicts.
4. Recommend compact or migrate-agents when budgets are exceeded.
5. Patch only routine, clear updates unless the developer confirms larger changes.

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

## Prepare Public Repository Release
1. Confirm README, license, ignore rules, and project status are public-safe.
2. Run script syntax checks and skill validation.
3. Confirm git status is clean after committing.
4. Add remote and push to the empty GitHub repository.
