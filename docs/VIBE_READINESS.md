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
- User: developers using Codex on long-running coding projects
- Problem: project context, decisions, and operating rules are lost or diluted across sessions
- Success standard: a future Codex session can quickly resume work, follow project rules, diagnose stale memory, and safely prepare handoffs or compaction plans

## Stack And Runtime
- Required versions: Python 3.9+ for helper scripts
- Tested versions: system Python 3.9 and bundled Python 3.12 for script syntax checks
- Preferred versions: Python 3.11+ where available
- Unknown version choices: future Codex skill runtime packaging format, if it changes

## Project Structure And Conventions
- Directory rules: skill source lives under `skills/project-memory`; active project docs live under `docs/`; old origin context lives under `docs/archive/`
- Naming rules: skill names use lowercase hyphen-case; scripts use snake_case
- Formatting/linting: Markdown stays concise and ASCII unless source content requires otherwise; Python scripts use standard-library dependencies only
- Generated files: generated project memory docs are committed only when they are part of this repository's own project memory, not temporary test output

## Core Models And Contracts
- Domain model: project memory files with source-of-truth ownership and task-based read paths
- API contracts: script CLIs for `init_docs.py`, `diagnose_memory.py`, `compact_memory.py`, and `migrate_agents.py`
- Config/schema: Markdown templates with `Memory Metadata` and `Maintenance Rules`
- State model: `PROJECT_STATUS.md` is current state; `docs/LOG.md` is chronological history; `docs/DECISIONS.md` is durable rationale
- File formats: Markdown, YAML frontmatter, Python scripts

## Development Red Lines
- Security: Do not hard-code secrets or credentials.
- Performance: keep scripts simple and fast for small repositories; avoid network dependencies in core scripts.
- Error handling: scripts should fail with clear messages and avoid destructive writes by default.
- Data/privacy: public docs must not include personal local paths, credentials, or private project content.
- Compatibility: preserve Python standard-library operation for helper scripts.

## AI Permission Boundaries
- AI may directly edit: repository docs, templates, and scripts when the requested scope is clear.
- AI must propose a plan before editing: large workflow changes, public API changes to scripts, major template taxonomy changes.
- AI must ask confirmation before: destructive edits, dependency upgrades, large refactors, compaction, archival, AGENTS.md migration.
- AI must never: commit secrets, silently delete durable project memory, rewrite confirmed decisions without approval.
- Human review required for: public release metadata, license changes, and first push to a public remote.

## Readiness Status
- Status: active
- Missing before broad code generation: none known
