---
name: matt-pocock-skills-pack
description: >
  Install, update, and route to the Matt Pocock Skills marketplace pack
  (engineering-focused: TDD, debugging, refactoring, code review, triage,
  pre-commit setup, skill authoring helpers, domain modeling, and more).
  Use when the user says "install matt pocock skills", "update matt pocock
  skills", or invokes any of the bundled commands — engineering: /tdd,
  /diagnose, /triage, /github-triage, /to-issues, /to-prd,
  /improve-codebase-architecture, /migrate-to-shoehorn, /setup-pre-commit,
  /git-guardrails-claude-code; misc: /grill-with-docs, /grill-me, /caveman;
  personal: /write-a-skill, /scaffold-exercises, /edit-article,
  /obsidian-vault; productivity: /setup-matt-pocock-skills, /triage-issue,
  /zoom-out; or any of the deprecated-but-retained /domain-model, /qa,
  /request-refactor-plan, /design-an-interface, /ubiquitous-language.
  Wraps `npx skills add mattpocock/skills` with idempotent install / update /
  verify scripts. Stays current via the sync-skills refresh hook.
metadata:
  author: podhi
  version: 1.1.0
  source: mattpocock/skills
related_skills: [sync-skills, marketing-skills-pack, skill-creator]
---

# matt-pocock-skills-pack

Meta-skill that installs and keeps current the **Matt Pocock Skills**
marketplace pack — an engineering-focused library distributed via the
`skills` CLI.

## What's in the Pack

Upstream now organizes skills into four category folders plus a `deprecated/` bucket for retired skills. We mirror upstream's grouping below. **20 active** + **5 deprecated-but-retained** = **25 manifest entries**.

### Engineering (10)

| Skill | Purpose |
|-------|---------|
| `tdd` | Test-driven development workflow |
| `diagnose` | Disciplined diagnosis loop for hard bugs and perf regressions |
| `triage` | State-machine triage with category + state roles |
| `github-triage` | Bulk GitHub issue triage |
| `to-issues` | Break a plan / spec into issue-tracker tickets |
| `to-prd` | Turn the current conversation into a PRD |
| `improve-codebase-architecture` | Find deepening architectural opportunities |
| `migrate-to-shoehorn` | Migrate test files to shoehorn |
| `setup-pre-commit` | Set up Husky pre-commit hooks |
| `git-guardrails-claude-code` | Set up Claude Code git guardrails |

### Misc (3)

| Skill | Purpose |
|-------|---------|
| `grill-with-docs` | Grill the user with domain-model + ADR docs as supporting info (renamed from `domain-model`) |
| `grill-me` | Interview the user rigorously |
| `caveman` | Ultra-compressed communication |

### Personal (4)

| Skill | Purpose |
|-------|---------|
| `write-a-skill` | Create new agent skills |
| `scaffold-exercises` | Create exercise directory structures |
| `edit-article` | Edit and improve articles |
| `obsidian-vault` | Search, create, manage Obsidian vault |

### Productivity (3)

| Skill | Purpose |
|-------|---------|
| `setup-matt-pocock-skills` | Bootstrap the per-repo `## Agent skills` config block |
| `triage-issue` | Triage a single bug or issue end-to-end |
| `zoom-out` | Step back and reconsider scope |

### Deprecated upstream (retained locally)

These five skills were moved into upstream's `deprecated/` folder in 2026-05 and `npx skills add` no longer installs them. We retain them in this repo as the source-of-truth so prior installations continue to work; consider migrating to the listed successor.

| Skill | Successor / Notes |
|-------|-------------------|
| `domain-model` | Renamed upstream to `grill-with-docs` (XML-wrapped + auto-invocable) |
| `qa` | Folded into the broader `triage` + `tdd` flow |
| `request-refactor-plan` | Folded into `improve-codebase-architecture` |
| `design-an-interface` | Variant generation handled ad-hoc; no direct successor |
| `ubiquitous-language` | Methodology folded into `grill-with-docs` |

**Source of truth:** `https://github.com/mattpocock/skills`
**Install command (canonical):** `npx skills add mattpocock/skills`

## When to Use

- User says "install matt pocock skills", "set up matt pocock pack"
- User says "update matt pocock skills" or "refresh matt pocock pack"
- User invokes any of the bundled commands listed above and they aren't installed
- A first-time bootstrap of an engineering-focused workspace

## Workflow

### Install (first time)
```bash
bash "$HOME/.claude/skills/matt-pocock-skills-pack/scripts/install.sh"
```
Wraps `npx -y skills@latest add mattpocock/skills -g -y --copy`.

### Update
```bash
bash "$HOME/.claude/skills/matt-pocock-skills-pack/scripts/update.sh"
```
Called automatically by `sync-skills` Step 1.5 on every sync.

### Verify
```bash
bash "$HOME/.claude/skills/matt-pocock-skills-pack/scripts/verify.sh"
```

## Integration with sync-skills

Listed in `sync-skills/SKILL.md` Step 1.5 alongside `marketing-skills-pack`.
The 25 marketplace-managed names (20 active + 5 deprecated-but-retained) are
enumerated in `manifest.txt` so Step 1.6 adopts upstream replacements for those
names after saving diffs.

## Troubleshooting

### `npx: command not found`
- **Cause:** Node.js is not installed.
- **Fix:** Install Node 20+ (`brew install node`). Re-run install.

### `/tdd` doesn't trigger after install
- **Cause:** Skill landed at project scope, not global.
- **Fix:** Re-run install (always uses `-g`). Verify with `npx skills list -g`.

### Update reports "package not found"
- **Cause:** Pack was never installed at the targeted scope.
- **Fix:** `update.sh` auto-falls-back to `add`.

## Related Skills

- **sync-skills** — bidirectional sync; calls this skill's `update.sh` every run.
- **marketing-skills-pack** — sibling marketplace pack (Corey Haines marketing).
- **skill-creator** — write your own skills from scratch (`write-a-skill` is the marketplace version).
