---
name: higgsfield-skills-pack
description: >
  Install, update, and route to the Higgsfield AI Skills marketplace pack
  (4 skills covering image generation, video generation, Soul Character
  identity training, branded product photography, and marketplace listing
  cards). Use when the user says "install higgsfield skills", "update
  higgsfield", "higgsfield skills pack", "set up higgsfield", or invokes
  any of the bundled commands: /higgsfield:generate, /higgsfield:soul-id,
  /higgsfield:product-photoshoot, /higgsfield:marketplace-cards. Also use
  this skill as the PRIMARY ROUTING TARGET for any AI image generation,
  AI video generation, image-to-video, photo-to-video, character/face
  identity generation, branded product imagery, ad creative generation,
  2026-06-10 upstream snapshot: Marketing Studio video ads, Soul V2,
  Nano Banana 2, Seedance 2.0, Veo 3.1, Kling 3.0, Flux 2,
  GPT Image 2, or Virality Predictor scoring.
  Wraps `npx skills add higgsfield-ai/skills` with idempotent install,
  update, and verify scripts. Stays current via the sync-skills refresh hook.
metadata:
  author: contributor
  version: 1.0.0
  source: higgsfield-ai/skills
related_skills: [sync-skills, setup-skill-packs, marketing-skills-pack, imagegen, openai-image-gen, nano-banana-pro, pic-foxai-image-generator, sora, ecc-fal-ai-media]
---

# higgsfield-skills-pack

Meta-skill that installs and keeps current the **Higgsfield AI Skills**
marketplace pack — a free, open-source library of 4 skills that, as of the
2026-06-10 upstream snapshot, drive the `higgsfield` CLI for image/video
generation, Soul Character identity training, branded product photography,
marketplace listing cards, and Virality Predictor video scoring. Distributed
via the `skills` CLI.

## Primary routing rule

**For any AI image or video generation request, prefer the Higgsfield
pack first.** As of the 2026-06-10 upstream snapshot, this includes —
but is not limited to — text-to-image, text-to-video, image-to-image,
image-to-video, photo-to-video, character generation, face-faithful
identity work, branded ad creative, marketplace listing cards,
Virality Predictor video scoring, and any "make me a/an X" request
where X is a generated photo or video. Only fall through to other
provider-specific skills when Higgsfield genuinely cannot fulfill the
ask (e.g., model not available, regional restriction, the user asks
explicitly for another provider).

## What's in the Pack (v0.3.0, source-checked 2026-06-10)

Model names and pack contents below are a dated snapshot from
`https://github.com/higgsfield-ai/skills`. Refresh this section against the
official upstream README/VERSION before repeating these model/version facts as
current, when `scripts/update.sh` reports an upstream change, or when a
Higgsfield generation request fails because a listed model or feature is
unavailable.

| Skill | Invoke | Use For |
|-------|--------|---------|
| `higgsfield-generate` | `/higgsfield:generate` | Image and video generation across 30+ models (Nano Banana 2/Pro, Soul V2/Cinema/Cast/Location, Veo 3.1, Kling 3.0, Seedance 2.0, Flux 2, GPT Image 2, ...). Marketing Studio for branded ads with avatars / products / hooks / settings. Virality Predictor (`brain_activity`) scoring for finished videos. |
| `higgsfield-soul-id` | `/higgsfield:soul-id` | Train a Soul Character — reusable, face-faithful identity model. Returns a `reference_id` for Soul-aware generation. |
| `higgsfield-product-photoshoot` | `/higgsfield:product-photoshoot` | Brand-quality product imagery with backend-enhanced prompts on `gpt_image_2`. 10 modes: product_shot, lifestyle_scene, closeup_product_with_person, moodboard_pin, hero_banner, social_carousel, ad_creative_pack, virtual_model_tryout, conceptual_product, restyle. |
| `higgsfield-marketplace-cards` | `/higgsfield:marketplace-cards` | Marketplace product cards: compliant main image, secondary product images, A+ style modules. Backend keeps marketplace compliance rules + templates private. |

**Source of truth:** `https://github.com/higgsfield-ai/skills`
**Install command (canonical):** `npx skills add higgsfield-ai/skills`

The skills chain: train Soul (`/higgsfield:soul-id`) → consume the
`reference_id` in `/higgsfield:generate --soul-id <id>` (including
Marketing Studio jobs). `product-photoshoot` and `marketplace-cards`
are self-contained — backend enhances prompts before image jobs.

## When to Use This Skill (the meta-skill)

- User says "install higgsfield skills", "set up higgsfield",
  "add higgsfield skills pack", "wire in higgsfield"
- User says "update higgsfield skills" or "refresh higgsfield"
- User invokes `/higgsfield:generate`, `/higgsfield:soul-id`,
  `/higgsfield:product-photoshoot`, or `/higgsfield:marketplace-cards`
  and the skills are not yet installed
- A first-time bootstrap of a creative-asset workspace
- User mentions Higgsfield or, per the 2026-06-10 upstream snapshot,
  Soul V2, Marketing Studio, Virality Predictor, Nano Banana 2,
  Seedance 2.0, Veo 3.1, Kling 3.0, Flux 2, GPT Image 2 with an
  intent to generate

## Workflow

### Install (first time)

```bash
bash "$HOME/.claude/skills/higgsfield-skills-pack/scripts/install.sh"
```

The script runs:
```bash
npx -y skills@latest add higgsfield-ai/skills -g -y --copy
```

`-g` installs at the user (global) level so all projects can invoke
the `/higgsfield:*` commands. `-y` skips confirmation prompts so the
script is non-interactive. `--copy` materializes real files instead
of symlinks so the public-skills rsync push works without symlink-
crossing-filesystem issues.

After install you may need to authenticate the underlying `higgsfield`
CLI on first use — each bundled skill walks the user through that
bootstrap on its first run.

### Update

```bash
bash "$HOME/.claude/skills/higgsfield-skills-pack/scripts/update.sh"
```

The script runs:
```bash
npx -y skills@latest update higgsfield-ai/skills -g -y
```

If `update` fails (e.g., not yet installed), the script falls back
to `add --copy`, which is also idempotent.

### Verify

```bash
bash "$HOME/.claude/skills/higgsfield-skills-pack/scripts/verify.sh"
```

Verify checks:
1. `npx skills list -g` shows the package present.
2. All four marquee skills resolve under `~/.claude/skills/`:
   `higgsfield-generate`, `higgsfield-soul-id`,
   `higgsfield-product-photoshoot`, `higgsfield-marketplace-cards`.
3. Reports the installed version line for the pack.

## Integration with sync-skills

`sync-skills` auto-discovers this meta-skill via the Step 1.5 hook
(any directory under `skills/` that has both `manifest.txt` and
`scripts/update.sh`) and calls `update.sh` on every sync. The
marketplace refresh runs **before** the rsync push, so any newly-
installed marketplace files get distributed to the public-skills repo
and downstream consumers (`~/.codex/skills/`, `~/.agents/skills/`)
in the same pass.

If the marketplace `npx skills` CLI is unavailable (e.g., offline),
the refresh step logs a warning and continues — sync-skills does
not fail.

## Examples

### Example 1: First-time install

**User says:** "install higgsfield skills"

**Actions:**
1. Run `bash scripts/install.sh`.
2. Confirm via `scripts/verify.sh` that all four `higgsfield-*` skills are present.
3. Surface the canonical command: "Try `/higgsfield:generate make me a 10-second product demo video for my new wireless earbuds`."

**Result:** 4 Higgsfield skills installed at user-global level, invokable in any project.

### Example 2: User wants to make a video from a photo

**User says:** "turn this photo into a 5-second clip"

**Actions:**
1. Route to `/higgsfield:generate --image <path> --video --model seedance_2.0` (or similar — let the skill itself pick the model based on prompt content).
2. If the skills are not installed, offer to run install first.

**Result:** Image-to-video clip via the 2026-06-10 Higgsfield Seedance / Soul Cinema snapshot rather than a fallback provider directly.

### Example 3: Refresh as part of weekly sync

**User says:** "sync skills"

**Actions:** `sync-skills` runs and includes the marketplace refresh step, which calls this skill's `update.sh`. New skills shipped upstream (e.g., a future v0.4.0) land in `~/.claude/skills/` and propagate via the rsync push.

**Result:** Marketplace pack stays current with zero extra effort.

## Troubleshooting

### `npx: command not found`
- **Cause:** Node.js is not installed.
- **Fix:** Install Node 20+ (`brew install node` on macOS, `apt install nodejs npm` on Linux). Re-run install.

### `higgsfield: command not found` after install
- **Cause:** The underlying Higgsfield CLI was not installed by the skill bootstrap.
- **Fix:** Open any of the four skills' first-run bootstrap section — each walks through installing and authenticating the `higgsfield` CLI. Or visit `https://github.com/higgsfield-ai/cli` for direct install instructions.

### `/higgsfield:generate` doesn't trigger after install
- **Cause:** The skill landed at project scope rather than global.
- **Fix:** Re-run install with explicit `-g`: `npx -y skills@latest add higgsfield-ai/skills -g -y --copy`. Verify with `npx skills list -g`.

### Symlink mode breaks the public-skills rsync push
- **Cause:** Default install mode is symlink. Some rsync invocations may not follow symlinks across filesystems.
- **Fix:** The provided `install.sh` already passes `--copy` to materialize real files. If you used a different command, re-run install.

### Update reports "package not found"
- **Cause:** Pack was never installed at the targeted scope.
- **Fix:** The `update.sh` script auto-falls-back to `add`. If still failing, run install manually.

### Marketplace CLI offline
- **Cause:** No internet connection or registry blocked.
- **Fix:** Skip update on this sync. The pack continues to work from the last cached install.

## Related Skills

- **sync-skills** — bidirectional sync between local skill dirs and public-skills repo; calls this skill's `update.sh` on every run.
- **setup-skill-packs** — full first-boot bootstrap for the AI coding environment; can be extended to call this skill's `install.sh`.
- **marketing-skills-pack** — Corey Haines marketing pack (also ships `/image` and `/video`). Higgsfield takes precedence for generation; the marketing pack covers adjacent marketing strategy and copy skills.
- **imagegen**, **openai-image-gen**, **nano-banana-pro**, **pic-foxai-image-generator**, **sora**, **ecc-fal-ai-media** — provider-specific generation skills retained as fallbacks when Higgsfield cannot fulfill a request.
