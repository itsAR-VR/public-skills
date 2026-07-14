---
name: skill-consolidation
description: "Audit and consolidate installed agent skills by archiving generated mirror homes, reporting duplicate content/name groups, and preserving as many canonical skills as necessary without arbitrary caps."
origin: the project
---

# Skill Consolidation

Use this when the installed skill trees are noisy, duplicated, or bloated across Codex, Claude, Hermes, and OpenClaw.

## Principle

Do not force a fixed number of active skills. Keep as many as necessary, but remove accidental duplication:

- Keep canonical skills.
- Keep distinct variants with real behavioral differences.
- Preserve aliases for compatibility.
- Archive generated mirror homes and exact nested copies.
- Report same-name/different-content groups for human review.

## Safe cleanup command

Preview first:

```bash
node skills/skill-consolidation/scripts/consolidate-skill-mirrors.mjs
```

Apply reversible archive cleanup:

```bash
node skills/skill-consolidation/scripts/consolidate-skill-mirrors.mjs --apply
```

The script archives embedded agent-home mirrors such as `.hermes/skills`, `.codex/skills`, `.claude/skills`, `.openclaw/skills`, `.cursor/skills`, `.opencode/skills`, `.kiro/skills`, `.slate/skills`, `.factory/skills`, and `.agents/skills` when those directories appear inside another skill pack.

It does not delete canonical top-level skills. It moves generated mirrors into a timestamped archive under `~/.skill-consolidation-archive/`.

## Report output

The script writes a JSON report with:

- root skill counts before and after
- archived mirror directories
- duplicate exact-content groups
- same-name variant groups
- duplicate description groups

Use this report to decide second-pass merges, aliases, and retirements.

## Second-pass review

After mirror cleanup, review:

1. Same name + different content: choose canonical or rename collision.
2. Same description + different content: merge useful deltas or alias.
3. Exact duplicates across top-level roots: leave if each agent needs a local copy; otherwise convert to symlinks/manifest-managed mirrors if supported.
4. Deprecated aliases: keep alias metadata until no project docs reference them.

## Safety

- Never remove `.env`, auth, sessions, OAuth state, history, caches, or raw transcripts.
- Never delete canonical source files in `public-skills/skills` from this script.
- Archive first; delete archives only after a follow-up review.
- Run skill frontmatter/security validation after changes.
