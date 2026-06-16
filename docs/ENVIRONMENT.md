# Environment

## Memory Metadata
- owner: setup-runtime-cross-device
- read_when: setup, build, run, test, dependency, runtime, or cross-device work
- update_when: tool versions, setup steps, dependencies, paths, secrets policy, or supported devices change
- max_lines: 220
- stale_if: dependencies, toolchains, paths, devices, or runtime assumptions change

## Maintenance Rules
- Update when setup steps, dependencies, versions, paths, credentials policy, or cross-device assumptions change.
- Mark machine-specific values clearly.
- Do not store secrets, tokens, passwords, or private credentials.
- Keep installation commands reproducible when possible.

## Last Reviewed
- Date: 2026-06-16
- Status: active
- Stale if: Python runtime, Codex skill format, or repository layout changes.

## Required Tools
- Git
- Python 3.9+ for helper scripts
- Codex skill runtime for actual skill usage
- GitHub Actions for public repository validation

## Dependencies
- Runtime scripts use only the Python standard library.
- Official skill validation script requires `PyYAML`; this can be installed temporarily or supplied by the local environment.

## Setup Commands
- Validate scripts: `PYTHONPYCACHEPREFIX=/tmp/project-memory-pycache python3 -m py_compile skills/project-memory/scripts/*.py`
- Generate brief: `python3 skills/project-memory/scripts/brief_memory.py --target .`
- Run context gate: `python3 skills/project-memory/scripts/diagnose_memory.py --target . --context-gate`
- Inspect project shape: `python3 skills/project-memory/scripts/inspect_project.py --target .`
- Detect dynamic memory bridge state: `python3 skills/project-memory/scripts/memory_bridge.py detect --target .`
- Plan existing-context migration: `python3 skills/project-memory/scripts/migrate_context.py --target .`
- Validate skill when PyYAML is available: `python3 /path/to/quick_validate.py skills/project-memory`

## Machine-Specific Notes
- Do not commit local install paths.
- Local skill installation lives outside the repository and should be treated as a copy of `skills/project-memory`.

## Secrets Policy
- Do not commit secrets.
- Document required secret names or setup steps without values.
