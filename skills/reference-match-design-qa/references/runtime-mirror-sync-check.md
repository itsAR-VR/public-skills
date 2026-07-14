# Runtime Mirror Sync Check

Research date: 2026-05-18

Purpose: keep the authored skill and the runnable Codex/Claude copies from
drifting.

Canonical authoring source (in the `public-skills` repo):

- `skills/design-intelligence`
- `skills/reference-match-design-qa`
- `skills/vibe-design-reference-libraries`

Runtime mirrors (created by `sync-skills`):

- `$HOME/.codex/skills/design-intelligence`
- `$HOME/.codex/skills/reference-match-design-qa`
- `$HOME/.codex/skills/vibe-design-reference-libraries`
- `$HOME/.claude/skills/<same>` — on most setups this is a symlink that
  resolves to the same realpath as `$HOME/.codex/skills/`.

## Check

Run from the `public-skills` repo root:

```bash
bash scripts/check-design-intelligence-mirror-drift.sh
```

The check is read-only. It fails if the source skill and Codex runtime mirror
differ. If a Claude skills path exists, it also fails when any expected Claude
skill mirror is missing or different.

Override env vars when running from a non-standard layout:

```bash
SOURCE_ROOT=/path/to/public-skills \
CODEX_SKILLS=/path/to/.codex/skills \
CLAUDE_SKILLS=/path/to/.claude/skills \
  bash scripts/check-design-intelligence-mirror-drift.sh
```

## Sync

After editing the source skills, prefer the `sync-skills` skill — it handles
the full repo, all upstream packs, validation, and security scanning in one
pass. For a quick local sync of just these three skills:

```bash
rsync -a skills/design-intelligence/ "$HOME/.codex/skills/design-intelligence/"
rsync -a skills/reference-match-design-qa/ "$HOME/.codex/skills/reference-match-design-qa/"
rsync -a skills/vibe-design-reference-libraries/ "$HOME/.codex/skills/vibe-design-reference-libraries/"
```

Then run the drift check again.
