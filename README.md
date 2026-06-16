# project-memory

`project-memory` is a Codex skill for creating and maintaining lightweight, agent-facing project memory docs.

It helps long-running AI-assisted coding projects preserve the context that future sessions need: current status, durable decisions, operating rules, environment notes, repository rules, coordination state, Vibe Coding readiness, and safe maintenance workflows.

## What It Provides

- Project memory initialization from templates
- Existing-project inspection and addon recommendations
- Short current-state briefs for new sessions
- Task-based read paths for future agent sessions
- Vibe Coding readiness checks
- Context Gate and context-budget diagnostics
- Optional feature-track templates for larger work units
- Read-only bridge for projectmem-style dynamic memory
- Read-only compaction plans
- Read-only `AGENTS.md` migration plans
- Optional projectmem/conductor detection rules
- Source-of-truth conventions for project docs

## Repository Layout

```text
skills/project-memory/
  SKILL.md
  agents/openai.yaml
  assets/templates/
  references/maintenance-policy.md
  scripts/
    init_docs.py
    inspect_project.py
    brief_memory.py
    diagnose_memory.py
    memory_bridge.py
    compact_memory.py
    migrate_agents.py
```

The root `docs/` directory is this repository's own project memory, used to dogfood the skill.

## Install

Copy the skill folder into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R skills/project-memory ~/.codex/skills/project-memory
```

Restart Codex after installation so the skill can be discovered.

## Basic Usage

Initialize project memory docs in another repository:

```bash
python3 skills/project-memory/scripts/init_docs.py \
  --target /path/to/project \
  --project-name "My Project" \
  --project-kind "Codex skill" \
  --domain "agent-facing project memory"
```

If the target already contains `conductor/`, initialization stops by default to avoid duplicate static context systems. `project-memory` treats `conductor/` as an external context directory and does not parse, migrate, or synchronize it by default. Rerun with `--allow-conductor` only after explicitly choosing to proceed.

Inspect an existing repository before initialization:

```bash
python3 skills/project-memory/scripts/inspect_project.py --target /path/to/project
```

Diagnose project memory health:

```bash
python3 skills/project-memory/scripts/brief_memory.py --target /path/to/project
python3 skills/project-memory/scripts/diagnose_memory.py --target /path/to/project
python3 skills/project-memory/scripts/diagnose_memory.py --target /path/to/project --context-gate
```

Use optional feature tracks for multi-session or multi-day work:

```bash
python3 skills/project-memory/scripts/init_docs.py \
  --target /path/to/project \
  --project-name "My Project" \
  --project-kind "Codex skill" \
  --domain "agent-facing project memory" \
  --addons skill,docs,domain,tracks
```

Consult optional dynamic memory without binding to projectmem internals:

```bash
python3 skills/project-memory/scripts/memory_bridge.py detect --target /path/to/project
python3 skills/project-memory/scripts/memory_bridge.py summary --target /path/to/project
python3 skills/project-memory/scripts/memory_bridge.py precheck path/to/file --target /path/to/project
```

Generate a read-only compaction plan:

```bash
python3 skills/project-memory/scripts/compact_memory.py --target /path/to/project
```

Generate a read-only `AGENTS.md` migration plan:

```bash
python3 skills/project-memory/scripts/migrate_agents.py --target /path/to/project
```

## Safety Model

The helper scripts are intentionally conservative:

- `init_docs.py` does not overwrite existing files unless `--force` is used.
- `inspect_project.py` is read-only.
- `diagnose_memory.py` is read-only.
- `memory_bridge.py` is read-only and treats external memory output as advisory.
- `compact_memory.py` is read-only and only proposes a strategy.
- `migrate_agents.py` is read-only and only proposes a migration plan.

Risky changes such as compaction, archival, deletion, or `AGENTS.md` rewrites should be reviewed and confirmed by the developer before an agent applies patches.

## Interop Guidance

`project-memory` can coexist with other memory tools when ownership is explicit:

- Use `project-memory` for stable project governance: current status, principles, plans, durable decisions, environment, repository, coordination, and AI permission boundaries.
- Use projectmem, when installed, for dynamic events: issues, attempts, fixes, file-level gotchas, and precheck hints.
- Treat `conductor/` from context-driven-development as an external static context directory and conflict signal. Do not parse, migrate, or synchronize Conductor-specific files by default.

For most projects, commit generated project-memory docs to git so context travels across devices and sessions. Do not commit secrets, private customer details, or machine-specific credentials.

## Validation

Run script syntax checks:

```bash
PYTHONPYCACHEPREFIX=/tmp/project-memory-pycache \
python3 -m py_compile skills/project-memory/scripts/*.py
```

Run the built-in smoke checks:

```bash
python3 skills/project-memory/scripts/init_docs.py \
  --target /tmp/project-memory-smoke \
  --project-name "Smoke" \
  --project-kind "Codex skill" \
  --domain "agent-facing project memory" \
  --addons skill,docs,domain,tracks

python3 skills/project-memory/scripts/brief_memory.py --target /tmp/project-memory-smoke
python3 skills/project-memory/scripts/diagnose_memory.py --target /tmp/project-memory-smoke
python3 skills/project-memory/scripts/diagnose_memory.py --target /tmp/project-memory-smoke --context-gate
python3 skills/project-memory/scripts/inspect_project.py --target /tmp/project-memory-smoke
python3 skills/project-memory/scripts/memory_bridge.py detect --target /tmp/project-memory-smoke
```

If the Codex skill validator and `PyYAML` are available:

```bash
python3 /path/to/quick_validate.py skills/project-memory
```

## License

MIT
