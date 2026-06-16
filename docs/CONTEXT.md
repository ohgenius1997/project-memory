# Context

## Memory Metadata
- owner: stable-project-context
- read_when: project purpose, users, product shape, or domain background is unclear
- update_when: project purpose, audience, product shape, constraints, or non-goals change
- max_lines: 220
- stale_if: product type, target audience, or domain assumptions change

## Maintenance Rules
- Use this file for stable project background and intent.
- Update when the project's purpose, audience, product shape, or core constraints change.
- Do not use this file for daily progress; use `LOG.md`.
- Do not duplicate current next steps; use `PROJECT_STATUS.md`.

## Project Background
- Project: `project-memory`
- Kind: Codex skill
- Domain: agent-facing project memory management

## Known Facts
- The repository contains a Codex skill at `skills/project-memory`.
- The skill initializes and maintains lightweight project memory docs for coding projects.
- The skill is developer-triggered and agent-assisted; it does not run background automation.
- Obsolete origin context has been archived and is no longer active project context.

## Decisions
- The project output is a Codex skill named `project-memory`.
- Active project memory should serve future agent sessions, not external marketing docs.
- Open-source repository files should be clean, generic, and free of local machine paths.

## Assumptions
- The public repository name will be `project-memory`.
- The GitHub owner will be the user's account.
- The first public release will focus on documentation workflows and bundled scripts, not package-manager distribution.

## Open Questions
- Whether to publish through a package registry or keep installation as a source-copy workflow.
- Whether to add automated CI after the initial public push.

## Risks
- Existing local install copies can drift from repository source unless updates are synced deliberately.
- Public users may expect automatic document rewrites; README and skill docs must keep the read-only/confirmation-gated boundary clear.

## Audience And Users
- Primary user: developers using Codex across long-running coding projects.
- Secondary users: agent workflow builders who need reusable project-memory conventions.
- Agent users: future Codex sessions that must recover project state quickly.

## Problem Being Solved
Long-running AI-assisted projects lose context across sessions, devices, branches, and agent handoffs. This skill provides a small, structured project memory system with explicit read paths, update triggers, readiness checks, and conservative maintenance tools.

## Current Product Shape
A local Codex skill with templates, references, and Python helper scripts.

## Non-Goals
- Replacing full project management systems.
- Automatically rewriting project memory without developer confirmation.
- Building unrelated domain-specific skills in this repository.
