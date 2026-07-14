---
name: tiktok-app-marketing
description: Automate TikTok slideshow marketing for any app or product. Researches competitors, generates AI images, adds text overlays, posts via Postiz, tracks analytics, and iterates on what works. Use when setting up TikTok marketing automation, creating slideshow posts, analyzing post performance, optimizing app marketing funnels, or when a user mentions TikTok growth, slideshow ads, or social media marketing for their app. Covers competitor research (browser-based), image generation, text overlays, TikTok posting (Postiz API), cross-posting to Instagram/YouTube/Threads, analytics tracking, hook testing, CTA optimization, conversion tracking with RevenueCat, and a full feedback loop that adjusts hooks and CTAs based on views vs conversions.
related_skills:
  - social-content
  - hormozi-goated-ads
  - paid-ads
  - ad-creative
  - ai-video-scroll-animation
---

# TikTok App Marketing

Automate your entire TikTok slideshow marketing pipeline: generate → overlay → post → track → iterate.

Proven results: 7 million views on the viral X article, 1M+ TikTok views, $670/month MRR — all from an AI agent running on an old gaming PC.

## Prerequisites

This skill does NOT bundle any dependencies. Your AI agent will need to research and install the following based on your setup. Tell your agent what you're working with and it will figure out the rest.

### Required

**Node.js (v18+)** — all scripts run on Node. Your agent should verify this is installed and install it if not.

**node-canvas** (`npm install canvas`) — used for adding text overlays to slide images. This is a native module that may need build tools (Python, make, C++ compiler) on some systems. Your agent should research the install requirements for your OS.

**Postiz** — this is the backbone of the whole system. Postiz handles posting to TikTok (and 28+ other platforms), but more importantly, it provides the analytics API that powers the daily feedback loop. Without Postiz, the agent can post but can't track what's working — and the feedback loop is what makes this skill actually grow your account instead of just posting blindly. Sign up at postiz.pro/oliverhenry.

### Image Generation (pick one)

You choose what generates your images. Your agent should research the API docs for whichever you pick. OpenAI image model/source check: official OpenAI image-generation docs checked 2026-06-11 list `gpt-image-2` as latest; re-check those docs before changing OpenAI model IDs, pricing, latency, or Batch API assumptions.

- **OpenAI** — `gpt-image-2` by default, unless a current test shows `gpt-image-1.5` converts better for the app. Needs an OpenAI API key. Best for realistic photo-style images. This is what Larry uses and what we strongly recommend.
- **Stability AI** — Stable Diffusion XL and newer. Needs a Stability AI API key. Good for stylized/artistic images.
- **Replicate** — run any open-source model (Flux, SDXL, etc.). Needs a Replicate API token. Most flexible.
- **Local** — bring your own images. No API needed. Place images in the output directory and the script skips generation.

### Conversion Tracking (optional but recommended for mobile apps)

**RevenueCat** — this is what completes the intelligence loop. Postiz tells you which posts get views. RevenueCat tells you which posts drive paying users. Combined, the agent can distinguish between a viral post that makes no money and a modest post that actually converts — and optimize accordingly. Install the RevenueCat skill from ClaWHub (`clawhub install revenuecat`) for full API access to subscribers, MRR, trials, churn, and revenue. There's also a RevenueCat MCP for programmatic control over products and offerings from your agent/IDE.

### Cross-Posting (optional, recommended)

Postiz supports cross-posting to Instagram Reels, YouTube Shorts, Threads, Facebook, LinkedIn, and 20+ more platforms simultaneously. Your agent should research which platforms fit your audience and connect them in Postiz. Same content, different algorithms, more reach.

## First Run — Onboarding

When this skill is first loaded, IMMEDIATELY start a conversation with the user. Don't dump a checklist — talk to them like a human marketing partner would. The flow below is a guide, not a script. Be natural. Ask one or two things at a time. React to what they say. Build on their answers.

**Important:** Use `scripts/onboarding.js --validate` at the end to confirm the config is complete.

See [references/onboarding-phases.md](references/onboarding-phases.md) for the full 8-phase onboarding flow covering:

- **Phase 0:** TikTok Account Warmup (CRITICAL for new accounts)
- **Phase 1:** Get to Know Their App (conversational)
- **Phase 2:** Competitor Research (browser-based)
- **Phase 3:** Content Format & Image Generation setup
- **Phase 4:** Postiz Setup (powers the feedback loop)
- **Phase 5:** Conversion Tracking with RevenueCat
- **Phase 6:** Content Strategy (built from research)
- **Phase 7:** Daily Analytics Cron setup
- **Phase 8:** Save Config & First Test Post

## Core Workflow

### 1. Generate Slideshow Images

```bash
node scripts/generate-slides.js --config tiktok-marketing/config.json \
  --output tiktok-marketing/posts/YYYY-MM-DD-HHmm/ --prompts prompts.json
```

The script auto-routes to the correct provider based on `config.imageGen.provider`. Supports OpenAI, Stability AI, Replicate, or local images.

⚠️ **Timeout warning:** Generating 6 images can take several minutes, and OpenAI documents that complex GPT Image prompts may take up to 2 minutes per image. Set your exec timeout to at least 600 seconds (10 minutes). If you get `spawnSync ETIMEDOUT`, the exec timeout is too short. The script supports resume — if it fails partway, re-run it and completed slides will be skipped.

**Critical image rules (all providers):**
- ALWAYS portrait aspect ratio (1024x1536 or 9:16 equivalent) — fills TikTok screen
- Include "iPhone photo" and "realistic lighting" in prompts (for AI providers)
- ALL 6 slides share the EXACT same base description (only style/feature changes)
- Lock key elements across all slides (architecture, face shape, camera angle)
- See [references/slide-structure.md](references/slide-structure.md) for the 6-slide formula

### 2. Add Text Overlays

Uses node-canvas to render text directly onto slide images. See [references/text-overlay.md](references/text-overlay.md) for the exact code, font sizing rules, and positioning details that Larry uses for viral slides.

```bash
node scripts/add-overlay.js --dir tiktok-marketing/posts/YYYY-MM-DD-HHmm/ \
  --texts texts.json
```

**Key rules:**
- Dynamic font sizing — short text gets bigger (75px), long text gets smaller (51px)
- Positioned at ~28% from top (safe zone)
- White fill with thick black outline (readable on any background)
- 4-6 words per line, use `\n` for manual line breaks
- REACTIONS not labels — "Wait... this is actually nice??" not "Modern minimalist"
- No emoji — canvas can't render them reliably

### 3. Post to TikTok

```bash
node scripts/post-to-tiktok.js --config tiktok-marketing/config.json \
  --dir tiktok-marketing/posts/YYYY-MM-DD-HHmm/ --caption "caption" --title "title"
```

Posts go to TikTok inbox as **drafts** (SELF_ONLY), NOT published directly. User adds trending music manually before publishing. This is intentional — music is the single biggest factor in TikTok reach. Cross-posts to connected platforms automatically via Postiz.

**Caption rules:** Long storytelling captions (3x more views). Structure: Hook → Problem → Discovery → What it does → Result → max 5 hashtags. Conversational tone.

### 4. Connect Post Analytics

After user publishes from their TikTok inbox, connect posts to TikTok video IDs:

```bash
node scripts/check-analytics.js --config tiktok-marketing/config.json \
  --days 3 --connect
```

⚠️ **Wait at least 2 hours** after publishing before connecting. TikTok's API has an indexing delay. See [references/analytics-loop.md](references/analytics-loop.md) for full details.

⚠️ **Release ID cannot be overwritten** — once connected to wrong video, it's permanent. Always verify before connecting.

## The Feedback Loop (CRITICAL)

This is what separates "posting TikToks" from "running a marketing machine." See [references/feedback-loop.md](references/feedback-loop.md) for the full diagnostic framework.

### Diagnostic Framework

| Views | Conversions | Diagnosis | Action |
|-------|-------------|-----------|--------|
| High | High | 🟢 SCALE IT | Make 3 variations, test posting times |
| High | Low | 🟡 FIX THE CTA | Rotate CTAs, check app landing page |
| Low | High | 🟡 FIX THE HOOKS | Test radically different hooks |
| Low | Low | 🔴 FULL RESET | New format, new audience angle |
| High views + High downloads + Low subscribers | | 🔴 APP ISSUE | Fix onboarding/paywall/pricing |

### Hook Performance Tracking

Track in `tiktok-marketing/hook-performance.json`. Decision rules:
- 50K+ views → DOUBLE DOWN — make 3 variations immediately
- 10K-50K → Good — keep in rotation
- 1K-10K → Try 1 more variation
- <1K twice → DROP — try something radically different

### CTA Testing

When views are good but conversions are low, cycle through CTAs:
- "Download [App] — link in bio"
- "[App] is free to try — link in bio"
- "I used [App] for this — link in bio"
- "Search [App] on the App Store"
- No explicit CTA (just app name visible)

Track which CTAs convert best per hook category.

## Posting Schedule

Optimal times (adjust for audience timezone):
- **7:30 AM** — catch early scrollers
- **4:30 PM** — afternoon break
- **9:00 PM** — evening wind-down

3x/day minimum. Consistency beats sporadic viral hits. 100 posts beats 1 viral.

## Cross-Posting

Postiz supports cross-posting the same content to multiple platforms simultaneously. Recommend:
- **Instagram Reels** — especially strong for beauty/lifestyle/home
- **YouTube Shorts** — long-tail discovery
- **Threads** — lightweight engagement driver

Same slides, different algorithms, more surface area. Each platform's algo evaluates content independently.

## App Category Templates

See [references/app-categories.md](references/app-categories.md) for category-specific slide prompts and hook formulas.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| 1536x1024 (landscape) | Use 1024x1536 (portrait) |
| Font at 5% | Use 6.5% of width |
| Text at bottom | Position at 30% from top |
| Different rooms per slide | Lock architecture in EVERY prompt |
| Labels not reactions | "Wait this is nice??" not "Modern style" |
| Only tracking views | Track conversions — views without revenue = vanity |
| Same hooks forever | Iterate based on data, test new formats weekly |
| No cross-posting | Use Postiz to post everywhere simultaneously |
| Connecting release ID too soon | Wait 2+ hours — TikTok API indexing delay |
| Wrong video connected | Can't overwrite — always verify before connecting |
| spawnSync ETIMEDOUT | Exec timeout too short — image gen takes 3-9 min for 6 slides. Use 10-minute timeout or generate one at a time |
