# airJET Progress

## 2026-06-15 Natural-language CAD modeling discussion

Context:
- Existing prototype is a Fusion 360 Python script generated through vibe coding.
- The script builds a CAD-native 4028 guide-vane solid from explicit engineering equations.
- The next goal is to explore a friendlier and more efficient natural-language engineering 3D modeling workflow.

Current script observations:
- Geometry intent is encoded as parameter functions: duct radius transition, hub radius, NACA 0012 thickness, vane angle, wall thickness, and vane count.
- Fusion 360 API work is mostly mechanical: sketch creation, offset planes, fitted splines, revolve, loft, boolean join, and UI messaging.
- Main complexity is not the math itself, but robust CAD API orchestration and Fusion-specific runtime constraints.

Initial direction:
- Prefer a build123d-first pipeline for model generation, validation, and export.
- Keep Fusion 360 as an optional downstream viewer/editor/export target rather than the primary generation runtime.
- Separate natural-language interpretation from deterministic model construction.
- Build reusable parametric templates for common engineering parts instead of asking the model to write full CAD scripts from scratch every time.

Open product-shape options:
- Codex skill: best for repeatable local workflows, prompt rules, validation steps, and template libraries.
- Agent workflow: best when requirements clarification, iterative repair, rendering, and file export need multiple stages.
- Small app or CLI: best if the desired output is an end-user tool with forms, previews, and versioned model files.

Assembly modeling note:
- The proposed build123d-first route can support assemblies.
- Use individual parametric part generators for parts, then compose them into labeled Compound assembly trees.
- Use joints and named connection points for placement intent, such as fixed, hinge, slider, cylindrical, or ball-like relationships.
- Treat assembly constraints as deterministic metadata in the structured spec, rather than asking the model to freehand all transforms.

Interaction model note:
- Natural-language CAD should not assume the user can fully specify the model up front.
- The workflow should support progressive modeling: describe intent, generate a rough first version, inspect, revise, and lock decisions incrementally.
- Some later requirements only become describable after earlier reference geometry exists, so the system needs named features, faces, edges, joints, and construction references that users and agents can point back to.
- Preserve model history and structured specs after each iteration so design state is recoverable across sessions.

Parameter template note:
- Maintain a parameter template for each model family so users can quickly adjust dimensions without rewriting natural-language requirements.
- Parameters should include labels, units, defaults, allowed ranges, dependency rules, manufacturing hints, and user-facing descriptions.
- Separate user-facing parameters from derived engineering parameters so common edits stay simple while the generator still has exact geometry inputs.
- Version parameter templates alongside model specs and generated outputs to preserve reproducibility.

Product-shape decision:
- Current preferred output is a Codex skill for natural-language engineering CAD modeling.
- The skill should encode the workflow, state files, parameter-template rules, validation loop, and build123d-first modeling conventions.
- The first version should stay workflow-oriented and template-driven rather than becoming a full CAD application.
- Candidate skill name: `engineering-cad-modeler`.

Documentation planning note:
- Need a project documentation structure before implementing the skill.
- Documentation should preserve current conclusions, target outcomes, solution design, project progress, decision logs, and global operating principles.
- Keep docs lightweight enough to maintain during rapid exploration, but structured enough that future sessions can recover context without reading conversation history.
- Documentation is primarily for future Codex sessions, not external readers.
- Optimize file names and contents for fast context recovery, current-state awareness, and consistent adherence to project principles.
- Prefer fewer, high-signal files over a comprehensive documentation hierarchy.
- The documentation scheme should use a small universal core plus project-specific operational files when needed.
- Cross-device environment configuration, multi-session work division, and git/GitHub operating rules are important operational context and should be documented explicitly when they affect execution.
- The documentation system is intended to be an agent-facing context recovery and operating memory layer, not conventional external-facing project documentation.
- Its primary success metric is whether future Codex sessions can quickly understand the current state, follow project principles, avoid repeated decisions, and continue work safely across devices, branches, and sessions.
- New candidate meta-skill: initialize an agent-facing project documentation system from a user's business domain and technical project type.
- The meta-skill should generate a small universal documentation core, add project-specific operational docs only when needed, and include clear planning for `COORDINATION.md` when work is split across sessions, branches, devices, or agents.
- Generated documentation should include self-maintenance instructions so future Codex sessions know each file's purpose, update triggers, and expected content shape.
- `AGENTS.md` should act as the top-level operating rulebook that tells future sessions which docs to read first and when to update status, logs, decisions, environment, repository, and coordination notes.
- Further optimization direction: make the documentation system optimized for agent execution, not human completeness.
- Prefer explicit reading order, update triggers, stale markers, source-of-truth ownership, and handoff fields so future sessions can decide what to read and what to update quickly.
- `init-project-memory` should support ongoing maintenance workflows, not only initialization.
- Maintenance workflows should include context-budget compaction, documentation health diagnosis, stale-state detection, handoff preparation, and repository/environment consistency checks.
- Prefer audit-first and preserve-first maintenance: diagnose and propose/perform scoped updates while preserving durable conclusions and moving obsolete details to logs or archive sections instead of deleting them silently.
- Maintenance actions are developer-triggered and agent-assisted, not automatic background updates.
- Compaction requires presenting the proposed strategy and getting developer confirmation before applying changes, especially when moving, summarizing, archiving, or deleting information.

## 2026-06-16 `init-project-memory` skill implementation

Implemented skill source in the repository:
- Path: `skills/init-project-memory`
- Current path after rename: `skills/project-memory`
- Purpose: initialize and maintain lightweight, agent-facing project memory docs for coding projects.
- Product boundary: developer-triggered, agent-assisted workflows; no automatic background maintenance.

Implemented resources:
- `SKILL.md` with initialize, resume, checkpoint, diagnose, compact, handoff, coordination, and safety workflows.
- `agents/openai.yaml` with display metadata and default prompt.
- Core templates for `AGENTS.md`, `PROJECT_STATUS.md`, and `docs/` memory files.
- Addon templates for skill, CAD/modeling, iOS, web, and data projects.
- `scripts/init_docs.py` for safe initialization from templates.
- `scripts/diagnose_memory.py` for read-only project memory health checks.
- `scripts/compact_memory.py` for read-only compaction strategy generation.
- `references/maintenance-policy.md` for source-of-truth and compaction policy.

Validation:
- Python syntax check passed for all scripts using `/private/tmp` pycache.
- `init_docs.py` tested in `/private/tmp` for generic, skill+CAD, and iOS projects.
- Re-running initialization against an existing generated project created 0 files and skipped existing files as intended.
- `diagnose_memory.py` successfully reported placeholder environment notes.
- `compact_memory.py` produced a conservative read-only plan and did not modify files.
- Official `quick_validate.py` could not run because available Python environments lack the `yaml` module.

Next suggested step:
- Dogfood the new skill by using it to initialize this repository's own project memory docs, then refine templates based on actual friction.

## 2026-06-16 Addon abstraction refinement

New conclusion:
- `cad` is not a good addon category for `init-project-memory`.
- Addons should represent project artifact type or engineering organization shape, not business/domain subject matter.
- This project is a Codex skill about engineering 3D modeling, so it should use a `skill` project-type addon plus domain context, not a `cad` addon.

Recommended direction:
- Replace domain-specific addons such as `cad` with a generic `DOMAIN.md` mechanism.
- Consider addon axes such as project shape (`skill`, `app`, `system`, `library`, `docs`, `data-ai`) and platform/runtime (`web`, `ios`, `cli`, `cloud`) rather than one-off business domains.
- Keep business-specific knowledge in `docs/DOMAIN.md`, `docs/CONTEXT.md`, `docs/PLAN.md`, and project-type docs.

Further agent-facing optimization direction:
- Improve generated content for agent consumption, not just generality.
- Add explicit task-based read paths, source-of-truth ownership, stale markers, max-size budgets, and fact/decision/hypothesis separation.
- Consider lightweight machine-readable metadata in generated docs so future sessions can quickly decide what to read, trust, update, or compact.
- Context growth is a core risk for mid/late project stages.
- The documentation system should optimize for selective loading: short status index, task-based read paths, per-file context budgets, archive/summary layers, and diagnosis for docs that exceed their intended size or mix stale history with current state.

## 2026-06-16 `init-project-memory` optimization

Implemented refinements:
- Reworked addon abstraction around project shape, platform/runtime, and domain context.
- Removed `cad` as a project addon category; CAD/3D modeling now belongs in generic `docs/DOMAIN.md` for this project.
- Added project-shape addons: `skill`, `app`, `system`, `library`, `docs`, `data-ai`.
- Added platform/runtime addons: `web`, `ios`, `cli`, `cloud`.
- Added context addon: `domain`.
- Added `Memory Metadata` to generated templates with owner, read triggers, update triggers, context budget, and stale conditions.
- Added task-based read paths, source-of-truth ownership, context-budget warnings, and handoff fields to core templates.
- Updated `init_docs.py` inference so an engineering 3D modeling Codex skill generates `skill + domain`, not `cad`.
- Updated `diagnose_memory.py` to detect context-budget overages and recommend compact without applying changes.
- Updated `compact_memory.py` to generate read-only, source-of-truth-aware compaction plans.
- Cleaned macOS `.DS_Store` files from the skill source tree.

Validation:
- Python syntax check passed for all scripts.
- `--list-addons` now works without `--target`.
- Temporary project tests passed for:
  - engineering 3D modeling Codex skill: generated `skill + domain`.
  - iOS app: generated `app + ios + domain`.
  - web system with analytics: generated `data-ai + system + web + domain`.
- Repeated initialization still skips existing files by default.
- Over-budget status-file test caused `diagnose_memory.py` to recommend compact and `compact_memory.py` to produce a read-only trim strategy.
- Official `quick_validate.py` still cannot run because available Python environments lack the `yaml` module.

Follow-up validation:
- Temporarily installed `PyYAML` into `/private/tmp/airjet-pyyaml` without changing project files or global Python.
- Ran official `quick_validate.py` with `PYTHONPATH=/private/tmp/airjet-pyyaml`.
- Result: `Skill is valid!`

## 2026-06-16 Vibe coding readiness review

Reviewed external vibe-coding checklist:
- One-sentence product goal
- Locked technical stack and runtime versions
- Directory structure and coding conventions
- Core data structures
- Development red lines
- AI permission boundaries

Assessment:
- The checklist is directionally correct for preventing "AI generated a lot of code but not what I wanted."
- It should be adapted as a project readiness gate, not a rigid requirement that every detail must be complete before any exploration.
- Current `init-project-memory` partially covers product context, environment, repository, principles, API/data docs, and workflows.
- Missing explicit support for AI/developer responsibility boundaries and a consolidated vibe-coding readiness checklist.

Recommended skill refinement:
- Add an explicit `VIBE_READINESS.md` or equivalent section in core docs.
- Add readiness checks to diagnosis so future sessions can warn when product goal, stack, data structures, red lines, or AI review boundaries are missing.

## 2026-06-16 `AGENTS.md` merge strategy discussion

New conclusion:
- `AGENTS.md` should remain short because it may be automatically loaded by future Codex sessions.
- A long "ideal header plus legacy content below" is less optimal, even if it says the lower content usually does not need to be read, because the lower content may still consume context.
- Existing `AGENTS.md` content should be classified and migrated into the project memory docs when the developer approves.
- Keep only always-on operating rules in `AGENTS.md`; move detailed project context, environment, repository, decisions, logs, and domain notes into `docs/`.
- A snippet file is useful as a conservative non-overwrite fallback, but the preferred confirmed workflow is an `AGENTS.md` refactor/merge with old content redistributed to source-of-truth docs.

## 2026-06-16 Skill rename

Decision:
- Renamed the skill from `init-project-memory` to `project-memory`.

Rationale:
- The skill now covers initialization, diagnosis, context-budget warnings, compaction planning, Vibe Coding readiness, and AGENTS.md migration planning.
- The old name over-emphasized initialization and no longer represented the full lifecycle.

Current path:
- `skills/project-memory`

## 2026-06-16 Local skill installation

Installed the current `project-memory` skill into the local Codex skills directory:
- Source: `skills/project-memory`
- Destination: `/Users/bytedance/.codex/skills/project-memory`

Validation:
- Installed `SKILL.md` has `name: project-memory`.
- Official `quick_validate.py` passed for `/Users/bytedance/.codex/skills/project-memory`.

Usage note:
- Restart Codex to pick up the newly installed skill.

## 2026-06-16 Vibe readiness and AGENTS migration implementation

Implemented refinements:
- Added core `docs/VIBE_READINESS.md` template as the AI-assisted development readiness gate.
- Updated `AGENTS.md`, `PROJECT_STATUS.md`, and `PRINCIPLES.md` templates to reference vibe readiness before broad code generation or large refactors.
- Added readiness fields for product goal, stack/runtime versions, project structure/conventions, core models/contracts, development red lines, and AI permission boundaries.
- Updated `SKILL.md` with Vibe Readiness and AGENTS.md Migration workflows.
- Added `scripts/migrate_agents.py`, a read-only AGENTS.md migration planner.
- Updated `diagnose_memory.py` to:
  - require `docs/VIBE_READINESS.md` as a core memory file.
  - warn when readiness placeholders remain.
  - recommend `migrate-agents` when `AGENTS.md` exceeds budget.
- Updated `compact_memory.py` so overlong `AGENTS.md` produces a `migrate-agents` action rather than ordinary compaction.
- Updated `init_docs.py` post-generation guidance to fill `docs/VIBE_READINESS.md` before broad code generation.
- Updated `references/maintenance-policy.md` with AGENTS migration policy and vibe readiness rules.

Validation:
- Python syntax check passed for all scripts, including `migrate_agents.py`.
- Template metadata check passed for all core and addon templates.
- Official `quick_validate.py` passed with temporary `PyYAML` from `/private/tmp/airjet-pyyaml`.
- Temporary project test confirmed:
  - `docs/VIBE_READINESS.md` is generated.
  - engineering 3D modeling skill still selects `skill + domain`.
  - diagnosis reports missing readiness fields.
  - overlong `AGENTS.md` triggers `agents-migration-recommended`.
  - `migrate_agents.py` outputs a read-only migration plan.
  - `compact_memory.py` recommends `migrate-agents` for overlong `AGENTS.md`.
