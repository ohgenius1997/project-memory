# Vibe Readiness

## Memory Metadata
- owner: ai-development-readiness
- read_when: before substantial code generation, large refactors, architecture changes, or delegating broad implementation to AI
- update_when: product goal, success criteria, stack/runtime, conventions, core contracts, red lines, or AI permission boundaries change
- max_lines: 260
- stale_if: project goal, runtime, core data model, safety constraints, or AI review boundaries change

## Maintenance Rules
- Use this file as the readiness gate for AI-assisted development.
- Keep it concise and operational; detailed background belongs in `CONTEXT.md` or `DOMAIN.md`.
- Record unknowns explicitly instead of inventing certainty.
- Do not store secrets.
- Before large implementation work, check that required fields are filled or consciously marked `Unknown`.

## One-Sentence Product Goal
- User: TBD
- Problem: TBD
- Success standard: TBD

## Stack And Runtime
- Required versions: TBD
- Tested versions: TBD
- Preferred versions: TBD
- Unknown version choices: TBD

## Project Structure And Conventions
- Directory rules: TBD
- Naming rules: TBD
- Formatting/linting: TBD
- Generated files: TBD

## Core Models And Contracts
- Domain model: TBD
- API contracts: TBD
- Config/schema: TBD
- State model: TBD
- File formats: TBD

## Development Red Lines
- Security: Do not hard-code secrets or credentials.
- Performance: TBD
- Error handling: TBD
- Data/privacy: TBD
- Compatibility: TBD

## AI Permission Boundaries
- AI may directly edit: TBD
- AI must propose a plan before editing: TBD
- AI must ask confirmation before: destructive edits, dependency upgrades, large refactors, compaction, archival, AGENTS.md migration
- AI must never: commit secrets, silently delete durable project memory, rewrite confirmed decisions without approval
- Human review required for: TBD

## Readiness Status
- Status: draft
- Missing before broad code generation: product goal, stack/runtime, conventions, core contracts, development red lines, AI permission boundaries
