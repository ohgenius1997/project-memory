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
- Date: {{DATE}}
- Status: initial
- Stale if: dependencies, toolchains, paths, or supported devices change.

## Required Tools
- TBD

## Dependencies
- TBD

## Setup Commands
- TBD

## Machine-Specific Notes
- TBD

## Secrets Policy
- Do not commit secrets.
- Document required secret names or setup steps without values.
