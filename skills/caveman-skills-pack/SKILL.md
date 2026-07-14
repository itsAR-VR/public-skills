---
name: caveman-skills-pack
description: >
  Install and update the caveman ecosystem (JuliusBrussee/caveman) as a managed
  marketplace pack. Provides 5 skills — caveman (terse mode), caveman-commit
  (terse commit messages), caveman-help (mode reference), caveman-review (terse
  PR review comments), and caveman-compress (compress memory files into caveman
  format). Auto-refreshed every sync via Step 1.5 of sync-skills. Use when the
  user says "install caveman", "update caveman skills", or "set up caveman".
metadata:
  author: contributor
  version: 1.0.0
  source_repo: https://github.com/JuliusBrussee/caveman
  source_commit: tracked-on-update
related_skills:
  - sync-skills
  - marketing-skills-pack
  - matt-pocock-skills-pack
---

# caveman-skills-pack

Marketplace meta-skill that installs and keeps the caveman ecosystem in sync
with `JuliusBrussee/caveman`. Follows the same convention as
`marketing-skills-pack` and `matt-pocock-skills-pack` so `sync-skills` Step 1.5
auto-discovers it (presence of `manifest.txt` + executable `scripts/update.sh`)
and refreshes upstream changes on every sync.

## What this provides

| Skill | Trigger | Purpose |
|---|---|---|
| `caveman` | `/caveman [lite\|full\|ultra\|wenyan-*]` | Persistent terse output mode (~75% token cut) |
| `caveman-commit` | `/commit`, "write a commit" | Conventional Commits with no fluff |
| `caveman-help` | `/caveman-help` | One-shot reference card for caveman modes |
| `caveman-review` | `/review`, "code review" | One-line PR comments: location → problem → fix |
| `caveman-compress` | `/caveman:compress <file>` | Compress memory files (CLAUDE.md, todos) into caveman speak; backup to `<file>.original.md` |

## Why a meta-skill instead of a direct copy

If the upstream repo ships a fix or new mode, the meta-skill's `update.sh` runs
on the next `sync-skills` invocation and pulls it in automatically — no manual
re-clone. The managed-upstream rule in sync-skills Step 1.6 means updates to
caveman skills replace the old repo copies after diff snapshots are written.

## Manifest

`manifest.txt` lists the 5 skill names this pack manages. The managed
replacement in sync-skills Step 1.6 is scoped to these names — non-marketplace
skills are never touched by upstream refreshes.

## Scripts

- `scripts/install.sh` — clone or update upstream, copy the 5 skills into
  `~/.claude/skills/` (renaming `compress` → `caveman-compress`)
- `scripts/update.sh` — same flow as install (idempotent), called by
  sync-skills Step 1.5 every sync
- `scripts/verify.sh` — confirm all 5 skill directories exist with valid
  frontmatter

## When to invoke directly

- Fresh machine setup before first sync: `bash scripts/install.sh`
- Verify after a sync: `bash scripts/verify.sh`
- `update.sh` runs automatically; no manual call needed in normal use.

## Source

- Upstream repo: https://github.com/JuliusBrussee/caveman
- License: see upstream `LICENSE` file
- Updated from upstream HEAD on each `update.sh` run; the installer prints the
  resolved commit for traceability.

## Reviewing upstream changes

Every managed replacement writes a diff under
`~/.codex/skill-sync-diffs/<timestamp>/marketplace/` before the repo copy is
replaced.

## Anti-patterns

- Don't edit upstream-mirrored files in `~/.claude/skills/caveman*/` or
  `public-skills/skills/caveman*/` directly unless you expect the next sync to
  replace them. Fork or rename the skill for durable local changes.
- Don't rename skills inside this pack without updating `manifest.txt` AND
  the `name:` frontmatter — Step 1.6 restoration matches by directory name.
