---
name: ponytail-skills-pack
description: >
  Install, update, and route to Dietrich Gebert's Ponytail skill pack: a
  minimal-code senior engineer style plus over-engineering review, repo audit,
  debt ledger, and help commands. Use when the user says "install ponytail", "update
  ponytail", "ponytail skill", "lazy senior dev", "review for
  over-engineering", "/ponytail", "/ponytail-review", "/ponytail-audit",
  "/ponytail-debt", or "/ponytail-help". Wraps `npx skills add
  DietrichGebert/ponytail` with idempotent install, update, and verify scripts.
  Stays current via the sync-skills marketplace refresh hook.
metadata:
  author: podhi
  version: 1.0.0
  source: DietrichGebert/ponytail
related_skills: [sync-skills, ponytail, ponytail-review, ponytail-audit, ponytail-debt, ponytail-help]
---

# ponytail-skills-pack

Meta-skill that installs and keeps current the **Ponytail** skill pack, an
open-source set of agent skills for choosing the smallest working solution and
reviewing code for avoidable complexity.

## Source Snapshot

Checked 2026-06-16 from `https://github.com/DietrichGebert/ponytail`.

| Skill | Purpose |
|-------|---------|
| `ponytail` | Minimal-code senior engineer style: YAGNI, stdlib/native first, minimal code. |
| `ponytail-review` | Diff review focused only on over-engineering and deletable complexity. |
| `ponytail-audit` | Whole-repo audit for bloat, speculative abstractions, and hand-rolled stdlib. |
| `ponytail-debt` | Collects `ponytail:` shortcut comments into a debt ledger. |
| `ponytail-help` | Quick reference for the Ponytail modes and commands. |

Source of truth: `https://github.com/DietrichGebert/ponytail`
Install command: `npx skills add DietrichGebert/ponytail`

## Workflow

### Install

```bash
bash "$HOME/.claude/skills/ponytail-skills-pack/scripts/install.sh"
```

The script runs:

```bash
npx -y skills@latest add DietrichGebert/ponytail -g -y --copy --full-depth --skill '*'
```

`--copy` materializes files into the local skill directory so the public-skills
sync path can mirror them without depending on symlinks.

### Update

```bash
bash "$HOME/.claude/skills/ponytail-skills-pack/scripts/update.sh"
```

Called automatically by `sync-skills` Step 1.5. If `update` is unsupported or
the pack is not installed yet, the script falls back to `add`.

### Verify

```bash
bash "$HOME/.claude/skills/ponytail-skills-pack/scripts/verify.sh"
```

Verify checks that all five Ponytail `SKILL.md` files exist under the
loader-facing skills directory.

## Integration With sync-skills

`sync-skills` auto-discovers any meta-skill that has both `manifest.txt` and an
executable `scripts/update.sh`. This pack's manifest lists the five upstream
skill names so Step 1.6 can adopt upstream replacements for only those skills
after saving a diff snapshot.

## Troubleshooting

### `npx: command not found`

Install Node.js 20+ and re-run the install script.

### Skills do not appear after install

Run:

```bash
bash "$HOME/.claude/skills/ponytail-skills-pack/scripts/verify.sh"
```

If the verifier reports missing files, rerun install with the canonical command
shown above. On this shared setup, `~/.claude/skills`, `~/.codex/skills`, and
`~/.agents/skills` may resolve to the same real directory.

## Related Skills

- `ponytail` - minimal implementation mode.
- `ponytail-review` - over-engineering diff review.
- `ponytail-audit` - whole-repo complexity audit.
- `ponytail-debt` - deferred shortcut ledger.
- `sync-skills` - keeps this pack current and mirrored into public-skills.
