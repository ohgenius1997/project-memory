# Repository

## Memory Metadata
- owner: git-github-release-rules
- read_when: git, GitHub, branching, PR, release, or generated-file policy work
- update_when: remotes, branch strategy, commit policy, PR policy, release flow, or generated-file policy changes
- max_lines: 220
- stale_if: remote URL, default branch, branch strategy, release flow, or generated-file policy changes

## Maintenance Rules
- Update when git/GitHub rules, remotes, default branches, branch naming, release process, or generated-file policy changes.
- Do not use this file for daily progress.
- Keep command examples safe and non-destructive.

## Last Reviewed
- Date: 2026-06-16
- Status: active
- Stale if: repository remote, branch strategy, release flow, or generated-file policy changes.

## Git
- Default branch: `main`
- Branch naming: use `codex/` prefix for agent-created branches unless the user asks otherwise.
- Commit policy: commit focused, validated changes with concise messages.

## GitHub
- Intended repository name: `project-memory`
- Remote URL: `https://github.com/ohgenius1997/project-memory.git`
- Visibility: public
- PR policy: direct push to `main` is acceptable until collaborators or CI are added.
- Issue/project usage: optional after public release.
- CI: GitHub Actions validates script syntax, skill metadata, initialization smoke test, brief, diagnosis, context gate, project inspection, and memory bridge detection.

## Branch State
- Current active branch: `main` tracking `origin/main`
- Active work branches: none

## Generated Files
- Commit: source templates, scripts, README, license, and project-memory docs.
- Ignore: Python caches, OS metadata, virtualenvs, temporary build/cache files.
