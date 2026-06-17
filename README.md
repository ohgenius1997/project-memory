# project-memory

AGENTS-first project context router for AI-assisted development.

`project-memory` keeps the always-on context small. It creates a short
`AGENTS.md` that tells coding agents what matters, where to read next, and what
not to load by default.

It is designed around one practical split:

- Stable rules and read paths belong in `AGENTS.md`.
- Current state and durable decisions get a few optional Markdown files.
- Messy session history belongs in a dynamic memory tool, preferably
  [agentmemory](https://github.com/rohitg00/agentmemory).

The goal is not "more docs". The goal is that a future agent can restart work
without rereading the whole repository or asking you to repeat the same context.

## Why This Exists

AI coding projects often drift into one of two bad states:

- The agent starts every session cold and forgets the project constraints.
- `AGENTS.md`, `CLAUDE.md`, README, TODOs, logs, and handoff notes become one
  giant pile of context.

`project-memory` avoids both by making `AGENTS.md` a router instead of a
project encyclopedia.

```text
AGENTS.md
  -> stable rules
  -> task-based read path
  -> source-of-truth ownership
  -> dynamic-memory handoff
```

For small projects, that may be the only file you need. For larger projects,
you can add only the stable files that justify their maintenance cost.

## The Recommended Stack

Use `project-memory` and `agentmemory` together:

| Layer | Tool | What it stores |
| --- | --- | --- |
| Always-on router | `project-memory` | `AGENTS.md`: rules, boundaries, task-based read paths |
| Stable project state | `project-memory` | `PROJECT_STATUS.md`, `docs/DECISIONS.md`, optional environment/coordination docs |
| Dynamic session memory | `agentmemory` | Attempts, failures, debugging traces, file-level gotchas, session continuity |

The direct rule is:

> Put instructions that should constrain every future agent in `AGENTS.md`.
> Put experiences that should be remembered but not always loaded in
> agentmemory.

`project-memory` does not install agentmemory, run hooks, create an MCP server,
or wrap a memory runtime. It writes the contract that tells agents how to use
the project files and agentmemory together.

## How agentmemory Fits

With agentmemory enabled, the intended workflow is simple:

1. At the start of a session, the agent reads `AGENTS.md`.
2. `AGENTS.md` tells the agent which project files are relevant for the task.
3. The agent asks agentmemory for related prior work, failures, and file-level
   warnings.
4. During implementation, ordinary debugging history stays in agentmemory.
5. When a conclusion becomes stable, the agent proposes a small update to
   `PROJECT_STATUS.md` or `docs/DECISIONS.md`.

That keeps permanent project files clean:

| Information | Where it should go |
| --- | --- |
| "Never hardcode API keys in frontend code." | `AGENTS.md` |
| "We use Swift 6.2 and Xcode 26 for this app." | `docs/ENVIRONMENT.md` when governed profile is justified |
| "The current milestone is palette import QA." | `PROJECT_STATUS.md` |
| "We chose build123d over Fusion scripts because..." | `docs/DECISIONS.md` |
| "Tried changing `ColorMatcher.swift`; test X failed because..." | agentmemory |
| "This file had a weird edge case last session." | agentmemory |

If agentmemory can print a concise project summary, pass it into the status sync
proposal command:

```bash
agentmemory-summary-command | \
  python3 skills/project-memory/scripts/status_sync_proposal.py \
    --target /path/to/project \
    --agentmemory-summary -
```

The command above is intentionally a generic stdin bridge. `project-memory` does
not hard-code an agentmemory CLI or API until agentmemory has a stable command
contract that should be depended on.

If you do not use agentmemory, start with `minimal`. Only add `docs/LOG.md` as a
sparse checkpoint fallback when the project has real long-running state that
would otherwise be lost.

## What It Generates

`project-memory` has three profiles. It never upgrades a project
automatically.

| Profile | Files | Use when |
| --- | --- | --- |
| `minimal` | `AGENTS.md` | Default. Small projects, exploration, or projects with agentmemory. |
| `standard` | `AGENTS.md`, `PROJECT_STATUS.md`, `docs/DECISIONS.md` | Continuous development needs current state and durable decisions. |
| `governed` | standard + `docs/ENVIRONMENT.md`, `docs/COORDINATION.md` | Cross-device setup, multiple branches, multiple sessions, or handoff. |

The profile choice is about maintenance cost. If a file will not be used to
route future agents, do not create it yet.

## Quick Start

Install the Codex skill:

```bash
mkdir -p ~/.codex/skills
cp -R skills/project-memory ~/.codex/skills/project-memory
```

Restart Codex so the skill can be discovered.

Initialize the smallest useful router:

```bash
python3 skills/project-memory/scripts/init_docs.py \
  --target /path/to/project \
  --project-name "My Project" \
  --project-kind "iOS app" \
  --domain "pin bead pattern generation"
```

That creates only `AGENTS.md` by default.

Use `standard` when the project needs stable current state and durable
decisions:

```bash
python3 skills/project-memory/scripts/init_docs.py \
  --target /path/to/project \
  --profile standard \
  --project-name "My Project"
```

Use `governed` only when environment or coordination facts need to survive
across devices, branches, sessions, or contributors:

```bash
python3 skills/project-memory/scripts/init_docs.py \
  --target /path/to/project \
  --profile governed \
  --project-name "My Project"
```

`pyproject.toml` is repository metadata for development and validation. Installing
this repository with pip does not install the Codex skill into
`~/.codex/skills/`.

## Which Tool Should I Run?

Start with the smallest workflow that matches the project state.

| Situation | Run | Why |
| --- | --- | --- |
| New or small project | `init_docs.py --profile minimal` | Create only `AGENTS.md`, the always-on router. |
| Continuous development needs current state | `init_docs.py --profile standard` | Add current status and durable decisions. |
| Cross-device, multi-branch, or handoff work | `init_docs.py --profile governed` | Add environment and coordination context. |
| Existing project, unsure what context exists | `inspect_project.py --target ...` | Inventory likely project-memory files, legacy docs, stack, git state, and upgrade signals. |
| Starting a new session or handoff | `brief_memory.py --target ...` | Get a short recommended read path without loading everything. |
| Before broad implementation or after context drift | `diagnose_memory.py --target ... --context-gate` | Check bloat, missing files, stale status, and profile-upgrade signals. |
| Current state changed | `status_sync_proposal.py --target ...` | Generate a read-only `PROJECT_STATUS.md` update proposal. |
| Long `AGENTS.md` or `CLAUDE.md` needs cleanup | `migrate_agents.py --target ...` | Classify what stays in the router versus what should move elsewhere. |
| Existing README/docs/TODOs/roadmaps need routing | `migrate_context.py --target ...` | Classify old context into status, decisions, environment, coordination, or archive buckets. |
| Memory or legacy docs are too long | `compact_memory.py --target ...` | Produce a read-only compaction, migration, and archive review plan. |

Typical flow for a new project:

1. Initialize `minimal`.
2. Add only stable rules and success criteria to `AGENTS.md`.
3. Use agentmemory for attempts, failures, and session history.
4. Upgrade to `standard` only when current status or durable decisions are being
   repeatedly re-explained.

Typical flow for an existing project:

1. Run `inspect_project.py`.
2. Run migration planners if old context is scattered across README, TODOs,
   `CLAUDE.md`, or docs.
3. Review the plan.
4. Patch only the files that will make future agent sessions shorter and more
   reliable.

## Usage Examples

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

Generate read-only migration or compaction plans:

```bash
python3 skills/project-memory/scripts/migrate_agents.py --target /path/to/project
python3 skills/project-memory/scripts/migrate_context.py --target /path/to/project
python3 skills/project-memory/scripts/compact_memory.py --target /path/to/project
```

`compact_memory.py` does not edit files. It flags oversized project-memory docs,
long legacy docs, source-of-truth drift, suggested target files, and the
recommended execution order for an agent-assisted cleanup after developer
confirmation.

## Safety Model

- `init_docs.py` does not overwrite existing files unless `--force` is used.
- Diagnosis, migration, compaction, and status sync scripts are read-only.
- Profile upgrades are recommendations, not automatic mutations.
- `AGENTS.md` should stay short and should not become a project encyclopedia.
- `docs/LOG.md` is only a sparse fallback when agentmemory is unavailable.
- Git tracking for generated memory files is a target-project policy.
- In `docs/COORDINATION.md`, agents may update only their own session state
  unless the developer asks otherwise.

## Git Tracking Policy

`project-memory` does not decide whether every memory file belongs in git. That
is a project policy.

General guidance:

- Commit `AGENTS.md` when the rules should follow the repository across
  branches, machines, or contributors.
- Commit `PROJECT_STATUS.md` and `docs/DECISIONS.md` when current state and
  durable decisions should survive branch switches and cross-device work.
- Treat `docs/COORDINATION.md`, sparse `docs/LOG.md`, and any dynamic-memory
  export as project-specific. Commit them only when the team wants those facts
  reviewed, merged, and shared.
- Never commit secrets, credentials, private tokens, or large raw episodic
  memory dumps.

Agents should follow the target project's `.gitignore`, repository policy, and
developer instructions instead of assuming all generated memory files are either
public or private.

## Cross-Agent Use

The skill package itself is for Codex. The files it generates are plain
Markdown and can be reused by other coding agents when that tool reads
repository instructions.

Practical guidance:

- Keep `AGENTS.md` as the repository source of truth for shared agent rules.
- If another tool does not read `AGENTS.md`, copy or link the relevant content
  into that tool's native instruction file.
- Do not assume Codex skill triggers, hooks, or installation paths exist in
  Claude Code, Cursor, GitHub Copilot, Windsurf, or other agents.
- Keep cross-agent instructions short and stable. Route detailed state through
  project-memory files or agentmemory instead of duplicating everything into
  every agent-specific file.

For Claude Code projects, a common lightweight option is:

```bash
ln -s AGENTS.md CLAUDE.md
```

Use a real copy instead of a symlink when the tool, operating system, or
repository policy does not handle symlinks well.

## Repository Files vs Generated Files

This repository uses root `AGENTS.md` for its own contributor/agent
instructions.

The template used for target projects lives at
`skills/project-memory/assets/templates/core/AGENTS.md`. When `init_docs.py`
initializes another project, it writes that template into the target project's
`AGENTS.md`.

Root-level local project-memory files such as `PROJECT_STATUS.md` or `docs/` may
exist while developing this repository, but they are not part of the public skill
package.

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
