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

## Cross-Agent Use

The skill package itself is for Codex. The files it generates are plain Markdown and can be reused by other coding agents when that tool reads repository instructions.

Practical guidance:

- Keep `AGENTS.md` as the repository source of truth for shared agent rules.
- If another tool does not read `AGENTS.md`, copy or link the relevant content into that tool's native instruction file.
- Do not assume Codex skill triggers, hooks, or installation paths exist in Claude Code, Cursor, GitHub Copilot, Windsurf, or other agents.
- Keep cross-agent instructions short and stable; route detailed state through the project-memory files or the dynamic-memory tool instead of duplicating everything into every agent-specific file.

For Claude Code projects, a common lightweight option is:

```bash
ln -s AGENTS.md CLAUDE.md
```

Use a real copy instead of a symlink when the tool, operating system, or repository policy does not handle symlinks well.

## Which Tool Should I Run?

Start with the smallest workflow that matches the project state.

| Situation | Run | Why |
| --- | --- | --- |
| New or small project | `init_docs.py --profile minimal` | Create only `AGENTS.md`, the always-on router. |
| Continuous development needs current state | `init_docs.py --profile standard` | Add `PROJECT_STATUS.md` and durable decisions. |
| Cross-device, multi-branch, or handoff work | `init_docs.py --profile governed` | Add environment and coordination context. |
| Existing project, unsure what context exists | `inspect_project.py --target ...` | Inventory likely project-memory, legacy docs, stack, git state, and upgrade signals. |
| Long `AGENTS.md` or `CLAUDE.md` needs cleanup | `migrate_agents.py --target ...` | Classify what stays in the router versus what should move elsewhere. |
| Existing README/docs/TODOs/roadmaps need routing | `migrate_context.py --target ...` | Classify old context into status, decisions, environment, coordination, or archive buckets. |
| Starting a new session or handoff | `brief_memory.py --target ...` | Get a short recommended read path without loading everything. |
| Before broad implementation or after context drift | `diagnose_memory.py --target ... --context-gate` | Check bloat, missing files, stale status, and profile-upgrade signals. |
| Current state changed | `status_sync_proposal.py --target ...` | Generate a read-only `PROJECT_STATUS.md` update proposal. |
| Memory or legacy docs are too long | `compact_memory.py --target ...` | Produce a read-only compaction, migration, and archive review plan. |

Typical flow:

1. New project: initialize the smallest profile, then fill only the stable facts.
2. Existing project: inspect first, then initialize or migrate only after reviewing the plan.
3. During development: read `AGENTS.md`, use `brief_memory.py` for the minimal read path, and rely on agentmemory for episodic history.
4. Before handoff: run diagnosis and status sync proposal, then patch stable state only after confirmation.

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

`compact_memory.py` does not edit files. It flags oversized project-memory docs, long legacy docs, source-of-truth drift, suggested target files, and the recommended execution order for an agent-assisted cleanup after developer confirmation.

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
python3 -m compileall -q skills/project-memory/scripts tests
```

Run behavior tests:

```bash
python3 -m unittest discover -s tests
```

GitHub Actions runs these checks on Linux, macOS, and Windows.

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
