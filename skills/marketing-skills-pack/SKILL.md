---
name: marketing-skills-pack
description: >
  Install, update, and route to the Corey Haines Marketing Skills marketplace
  pack. Use when the user says "install marketing skills", "update marketing
  skills", "marketing skills pack", mentions Corey Haines marketing skills, or
  invokes bundled commands such as /image, /video, /social, or legacy
  /social-content. Also use for marketing requests involving ChatGPT Images,
  GPT Image, Gemini, Flux, Midjourney, Veo, Sora, Runway, Kling, Pika,
  Seedance, HeyGen, Hyperframes, or Synthesia integrations. Wraps `npx skills
  add coreyhaines31/marketingskills` with idempotent install, update, and verify
  scripts. Stays current via the sync-skills refresh hook.
metadata:
  author: podhi
  version: 1.0.0
  source: coreyhaines31/marketingskills
related_skills: [sync-skills, setup-skill-packs, social-content, ad-creative, copywriting]
---

# marketing-skills-pack

Meta-skill that installs and keeps current the **Corey Haines Marketing Skills**
marketplace pack — a free, open-source marketing-skill library distributed via
the `skills` CLI.

Before quoting the current version, skill count, tool count, or image/video
model lineup, check the upstream source of truth and date the claim.

## Source Snapshot (checked 2026-06-10)

Latest checked upstream release: v2.3.0 (43 skills). The image/video model
lineup was last explicitly refreshed upstream in v2.0.1 on 2026-05-19. Re-check
the source of truth before presenting these as current.

| Command / Skill | Purpose |
|----------------|---------|
| `/image` | AI image generation (Gemini Image, Flux, Ideogram, ChatGPT Images / GPT Image, Midjourney, Recraft, Stable Diffusion) for blog heroes, social graphics, product mockups |
| `/video` | AI video production via Hyperframes & Remotion pipelines, HeyGen / Synthesia avatars, Veo, Sora, Runway, Kling, Seedance, Hailuo / MiniMax, Pika, Hunyuan / Wan |
| `/social` (formerly `/social-content`) | Short-form video frameworks (TikTok, Reels, Shorts) with hooks and scripting |
| HeyGen integration | API setup, MCP server, avatar workflows |
| Hyperframes integration | HTML/CSS programmatic video rendering |

**Source of truth:** `https://github.com/coreyhaines31/marketingskills`
**Release notes:** `https://github.com/coreyhaines31/marketingskills/releases`
**Install command (canonical):** `npx skills add coreyhaines31/marketingskills`

## When to Use

- User says "install marketing skills", "set up marketing skills", "add marketing skills pack"
- User says "update marketing skills" or "refresh marketing skills"
- User mentions Corey Haines marketing pack, Hyperframes, HeyGen, Veo, Sora, Runway, Kling, Pika
- User invokes `/image`, `/video`, `/social`, or legacy `/social-content` and the skills are not yet installed
- A first-time bootstrap of a marketing-focused workspace

## Workflow

### Install (first time)

```bash
bash "$HOME/.claude/skills/marketing-skills-pack/scripts/install.sh"
```

The script runs:
```bash
npx -y skills@latest add coreyhaines31/marketingskills -g -y
```

`-g` installs at the user (global) level so all projects can invoke `/image`
and `/video`. `-y` skips confirmation prompts so the script is non-interactive.

### Update

```bash
bash "$HOME/.claude/skills/marketing-skills-pack/scripts/update.sh"
```

The script runs:
```bash
npx -y skills@latest update -g -y coreyhaines31/marketingskills
```

If `update` fails (e.g., not yet installed), the script falls back to `add`,
which is also idempotent.

### Verify

```bash
bash "$HOME/.claude/skills/marketing-skills-pack/scripts/verify.sh"
```

Verify checks:
1. `npx skills list -g` shows the package present.
2. The marquee skills (`image`, `video`, and `social` or legacy `social-content`)
   resolves under `~/.claude/skills/`.
3. Reports the installed version line for the pack.

## Integration with sync-skills

`sync-skills` calls this skill's `update.sh` as part of its workflow so the
marketplace pack stays current on every sync. See
[sync-skills/SKILL.md](../sync-skills/SKILL.md) — the marketplace refresh
runs **before** the rsync push, so any newly-installed marketplace files
get distributed to the public-skills repo and downstream consumers
(`~/.codex/skills/`, `~/.agents/skills/`) in the same pass.

If the marketplace `npx skills` CLI is unavailable (e.g., offline), the
refresh step logs a warning and continues — sync-skills does not fail.

## Examples

### Example 1: First-time install

**User says:** "install marketing skills"

**Actions:**
1. Run `bash scripts/install.sh`.
2. Confirm via `scripts/verify.sh` that `image`, `video`, and `social` or legacy `social-content` are present.
3. Surface the canonical command: "Try `/image generate a hero for my blog post about pricing strategy`."

**Result:** Marketing skills installed at user-global level, invokable in any project.

### Example 2: User invokes /image but it's missing

**User says:** "/image hero for landing page"

**Actions:**
1. Detect that `image` skill is not installed (or routing fails).
2. Offer: "I can install the marketing skills pack — that includes `/image` and 39 others. Run install?"
3. On confirmation, run `scripts/install.sh` then re-route to `/image`.

**Result:** Skill installed and the original request fulfilled.

### Example 3: Refresh as part of weekly sync

**User says:** "sync skills"

**Actions:** `sync-skills` runs and includes the marketplace refresh step, which
calls this skill's `update.sh`. New skills shipped upstream land in
`~/.claude/skills/` and propagate via the rsync push.

**Result:** Marketplace pack stays current with zero extra effort.

## Troubleshooting

### `npx: command not found`
- **Cause:** Node.js is not installed.
- **Fix:** Install Node 20+ (`brew install node` on macOS, `apt install nodejs npm` on Linux). Re-run install.

### `skills: command not found` after install
- **Cause:** The marketplace CLI is installed per-project by default, not globally.
- **Fix:** Always invoke via `npx -y skills@latest …` (the install/update scripts already do this).

### `/image` doesn't trigger after install
- **Cause:** The skill landed at project scope rather than global.
- **Fix:** Re-run install with explicit `-g`: `npx -y skills@latest add coreyhaines31/marketingskills -g -y`. Verify with `npx skills list -g`.

### Symlink mode breaks the public-skills rsync push
- **Cause:** Default install mode is symlink. Some rsync invocations may not follow symlinks across filesystems.
- **Fix:** Re-install with `--copy` to materialize real files: `npx -y skills@latest add coreyhaines31/marketingskills -g -y --copy`. Then sync-skills push will succeed.

### Update reports "package not found"
- **Cause:** Pack was never installed at the targeted scope.
- **Fix:** The `update.sh` script auto-falls-back to `add`. If still failing, run install manually.

### Marketplace CLI offline
- **Cause:** No internet connection or registry blocked.
- **Fix:** Skip update on this sync. The pack continues to work from the last cached install.

## Related Skills

- **sync-skills** — bidirectional sync between local skill dirs and public-skills repo; calls this skill's `update.sh` on every run.
- **setup-skill-packs** — full first-boot bootstrap for the AI coding environment; can be extended to call this skill's `install.sh`.
- **social-content** — local short-form video skill in public-skills; complements (does not replace) the marketplace `/social-content`.
- **ad-creative**, **copywriting** — adjacent marketing skills already in public-skills.
