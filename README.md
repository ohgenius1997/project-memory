# project-memory

`project-memory` is a Codex skill for creating a lightweight, AGENTS-first project context router for AI-assisted development.

It follows four constraints:

- little always-on context
- strong task-based routing
- weak ceremony
- dynamic/episodic memory outsourced to agentmemory

It is not an MCP server, vector memory engine, automatic session recorder, or documentation management system.

## What It Provides

- Minimal `AGENTS.md` router generation by default
- Optional `standard` and `governed` profiles for projects that need stable state, decisions, environment, or coordination docs
- Agent-facing context routing and source-of-truth ownership rules
- agentmemory collaboration guidance without installing or wrapping agentmemory
- Read-only profile/context diagnosis
- Read-only status sync proposals for `PROJECT_STATUS.md`
- Read-only migration and compaction planners

## Recommended Pairing

Use `project-memory` for stable project governance:

- `AGENTS.md`: always-on routing, stable rules, and AI boundaries
- `PROJECT_STATUS.md`: current phase, latest conclusion, next step, blockers, risks
- `docs/DECISIONS.md`: durable decisions and rationale
- `docs/ENVIRONMENT.md`: stable setup/cross-device facts when needed
- `docs/COORDINATION.md`: active multi-session or multi-branch coordination when needed

Use [agentmemory](https://github.com/rohitg00/agentmemory) for dynamic memory:

- attempts
- failures
- debugging traces
- file-level gotchas
- session continuity
- episodic recall

`project-memory` does not install agentmemory. It only writes the routing contract that tells future agents how the two layers should cooperate.

## Repository Files vs Generated Files

This repository uses `AGENTS.md` for its own contributor/agent instructions.

The template used for target projects lives at `skills/project-memory/assets/templates/core/AGENTS.md`. When `init_docs.py` initializes another project, it writes that template into the target project's `AGENTS.md`.

Root-level local project-memory files such as `PROJECT_STATUS.md` or `docs/` may exist while developing this repository, but they are not part of the public skill package.

## Profiles

| Profile | Files | Use when |
| --- | --- | --- |
| `minimal` | `AGENTS.md` | Default. Small projects, exploration, or projects with agentmemory. |
| `standard` | `AGENTS.md`, `PROJECT_STATUS.md`, `docs/DECISIONS.md` | Continuous development needs current state and durable decisions. |
| `governed` | standard + `docs/ENVIRONMENT.md`, `docs/COORDINATION.md` | Cross-device setup, multiple branches, multiple sessions, or handoff. |

Profiles never upgrade automatically. Diagnosis can recommend an upgrade, but file creation or migration should happen only after developer confirmation.

## Git Tracking Policy

`project-memory` does not decide whether every memory file belongs in git. That is a project policy.

General guidance:

- Commit `AGENTS.md` when the rules should follow the repository across branches, machines, or contributors.
- Commit `PROJECT_STATUS.md` and `docs/DECISIONS.md` when current state and durable decisions should survive branch switches and cross-device work.
- Treat `docs/COORDINATION.md`, sparse `docs/LOG.md`, and any dynamic-memory export as project-specific: commit them only when the team wants those facts reviewed, merged, and shared.
- Never commit secrets, credentials, private tokens, or large raw episodic memory dumps.

Agents should follow the target project's `.gitignore`, repository policy, and developer instructions instead of assuming all generated memory files are either public or private.

## Install

Copy the skill folder into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R skills/project-memory ~/.codex/skills/project-memory
```

Restart Codex after installation so the skill can be discovered.

`pyproject.toml` exists for repository metadata and Python development tooling. Installing this repository with pip does not install the Codex skill into `~/.codex/skills/`.

## Usage

Initialize the default minimal router:

```bash
python3 skills/project-memory/scripts/init_docs.py \
  --target /path/to/project \
  --project-name "My Project" \
  --project-kind "Codex skill" \
  --domain "agent-facing project context"
```

Initialize a project that needs stable current state and decisions:

```bash
python3 skills/project-memory/scripts/init_docs.py \
  --target /path/to/project \
  --profile standard \
  --project-name "My Project"
```

Initialize a governed project:

```bash
python3 skills/project-memory/scripts/init_docs.py \
  --target /path/to/project \
  --profile governed \
  --project-name "My Project"
```

Use no dynamic memory and add a sparse checkpoint log fallback:

```bash
python3 skills/project-memory/scripts/init_docs.py \
  --target /path/to/project \
  --profile standard \
  --dynamic-memory none \
  --fallback-log
```

Diagnose context health:

```bash
python3 skills/project-memory/scripts/brief_memory.py --target /path/to/project
python3 skills/project-memory/scripts/diagnose_memory.py --target /path/to/project
python3 skills/project-memory/scripts/diagnose_memory.py --target /path/to/project --context-gate
```

Generate a read-only status sync proposal:

```bash
python3 skills/project-memory/scripts/status_sync_proposal.py --target /path/to/project
python3 skills/project-memory/scripts/status_sync_proposal.py \
  --target /path/to/project \
  --agentmemory-summary summary.md
```

If a dynamic-memory tool can print a concise project summary, pass it through stdin:

```bash
your-summary-command | \
  python3 skills/project-memory/scripts/status_sync_proposal.py \
    --target /path/to/project \
    --agentmemory-summary -
```

The stdin form is the preferred integration point for dynamic-memory tools. `project-memory` intentionally does not hard-code an agentmemory CLI/API until a stable command contract is confirmed.

Generate read-only migration or compaction plans:

```bash
python3 skills/project-memory/scripts/migrate_agents.py --target /path/to/project
python3 skills/project-memory/scripts/migrate_context.py --target /path/to/project
python3 skills/project-memory/scripts/compact_memory.py --target /path/to/project
```

## Safety Model

- `init_docs.py` does not overwrite existing files unless `--force` is used.
- Diagnosis, migration, compaction, and status sync scripts are read-only.
- Profile upgrades are recommendations, not automatic mutations.
- `AGENTS.md` should stay short and should not become a project encyclopedia.
- `docs/LOG.md` is only a sparse fallback when agentmemory is unavailable.
- Git tracking for generated memory files is a target-project policy; this skill documents guidance but does not force all memory files into or out of git.
- In `docs/COORDINATION.md`, agents may update only their own session state unless the developer asks otherwise.

## Validation

Run script syntax checks:

```bash
PYTHONPYCACHEPREFIX=/tmp/project-memory-pycache \
python3 -m py_compile skills/project-memory/scripts/*.py
```

Run smoke checks:

```bash
rm -rf /tmp/project-memory-smoke
python3 skills/project-memory/scripts/init_docs.py \
  --target /tmp/project-memory-smoke \
  --project-name "Smoke"

python3 skills/project-memory/scripts/init_docs.py \
  --target /tmp/project-memory-smoke-standard \
  --project-name "Smoke Standard" \
  --profile standard

python3 skills/project-memory/scripts/init_docs.py \
  --target /tmp/project-memory-smoke-governed \
  --project-name "Smoke Governed" \
  --profile governed

python3 skills/project-memory/scripts/brief_memory.py --target /tmp/project-memory-smoke
python3 skills/project-memory/scripts/diagnose_memory.py --target /tmp/project-memory-smoke
python3 skills/project-memory/scripts/status_sync_proposal.py --target /tmp/project-memory-smoke-standard
python3 skills/project-memory/scripts/migrate_agents.py --target /tmp/project-memory-smoke
python3 skills/project-memory/scripts/migrate_context.py --target /tmp/project-memory-smoke
```

If the Codex skill validator and `PyYAML` are available:

```bash
python3 /path/to/quick_validate.py skills/project-memory
```

## License

MIT
