# Agent Context Router

CRITICAL: Before mutating repository files, read this `AGENTS.md`, inspect the relevant source files, and state the context sources used in a progress update or final response.

## Project
- Name: project-memory
- Kind: Codex skill
- Purpose: lightweight AGENTS-first project context router for AI-assisted coding projects

## Public Repo Rules
- Keep the public repository focused on the reusable skill: `skills/project-memory/`, `README.md`, license, CI, and this `AGENTS.md`.
- Do not commit local project-management memory such as root `docs/` or `PROJECT_STATUS.md`.
- Keep generated target-project templates under `skills/project-memory/assets/templates/`.
- Keep helper scripts dependency-light and runnable with Python standard library.
- Do not add MCP servers, daemons, global hooks, vector stores, or automatic dynamic-memory writes.
- Recommend agentmemory as the dynamic-memory companion, but do not install or wrap it.

## Task Routing
- Skill instructions: `skills/project-memory/SKILL.md`
- Public docs: `README.md`
- Scripts: `skills/project-memory/scripts/`
- Templates: `skills/project-memory/assets/templates/`
- CI: `.github/workflows/validate.yml`

## Validation
- Run script syntax checks after script edits:
  `PYTHONPYCACHEPREFIX=/tmp/project-memory-pycache python3 -m py_compile skills/project-memory/scripts/*.py`
- Smoke minimal, standard, governed, and dynamic-memory-none initialization when changing templates or `init_docs.py`.
- Run status sync, diagnosis, brief, inspect, compact, and migration planner smoke tests after workflow changes.
