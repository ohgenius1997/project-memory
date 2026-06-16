# Build Runbook

## Memory Metadata
- owner: ios-build-run-test
- read_when: building, running, testing, signing, or debugging iOS app targets
- update_when: Xcode version, schemes, bundle IDs, simulators, signing, or dependencies change
- max_lines: 240
- stale_if: Xcode, scheme, simulator, bundle ID, signing, or test workflow changes

## Maintenance Rules
- Use this file for build, run, test, simulator, signing, and release commands.
- Update when schemes, bundle IDs, simulator targets, dependencies, or build tooling changes.
- Keep commands safe and reproducible.
- Do not store secrets or signing credentials.

## Project Setup
- Xcode version: TBD
- Scheme: TBD
- Bundle ID: TBD
- Minimum OS: TBD

## Build And Run
- TBD

## Test
- TBD

## Simulator Notes
- TBD
