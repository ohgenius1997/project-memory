# project-memory

`project-memory` is a Codex skill for creating and maintaining lightweight, agent-facing project memory docs.

It helps long-running AI-assisted coding projects preserve the context that future sessions need: current status, durable decisions, operating rules, environment notes, repository rules, coordination state, Vibe Coding readiness, and safe maintenance workflows.

## What It Provides

- Project memory initialization from templates
- Task-based read paths for future agent sessions
- Vibe Coding readiness checks
- Context-budget diagnostics
- Read-only compaction plans
- Read-only `AGENTS.md` migration plans
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
    diagnose_memory.py
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

Diagnose project memory health:

```bash
python3 skills/project-memory/scripts/diagnose_memory.py --target /path/to/project
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
- `diagnose_memory.py` is read-only.
- `compact_memory.py` is read-only and only proposes a strategy.
- `migrate_agents.py` is read-only and only proposes a migration plan.

Risky changes such as compaction, archival, deletion, or `AGENTS.md` rewrites should be reviewed and confirmed by the developer before an agent applies patches.

## Validation

Run script syntax checks:

```bash
PYTHONPYCACHEPREFIX=/tmp/project-memory-pycache \
python3 -m py_compile skills/project-memory/scripts/*.py
```

If the Codex skill validator and `PyYAML` are available:

```bash
python3 /path/to/quick_validate.py skills/project-memory
```

## License

MIT
