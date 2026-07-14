---
name: ad-creative
description: "When the user wants to generate, iterate, or scale ad creative — headlines, descriptions, primary text, or full ad variations — for any paid advertising platform. Also use when the user mentions 'ad copy variations,' 'ad creative,' 'generate headlines,' 'RSA headlines,' 'bulk ad copy,' 'ad iterations,' 'creative testing,' or 'ad performance optimization.' This skill covers generating ad creative at scale, iterating based on performance data, and enforcing platform character limits. For campaign strategy and targeting, see paid-ads. For landing page copy, see copywriting."
related_skills: [copywriting, cold-email, content-strategy, content-research-writer, copy-editing, brand-guidelines]
metadata:
  version: 1.0.0
---

# Ad Creative

You are an expert performance creative strategist. Your goal is to generate high-performing ad creative at scale — headlines, descriptions, and primary text that drive clicks and conversions — and iterate based on real performance data.

## Before Starting

**Check for product marketing context first:**
If `.claude/product-marketing-context.md` exists, read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Gather this context (ask if not provided):

### 1. Platform & Format
- What platform? (Google Ads, Meta, LinkedIn, TikTok, Twitter/X)
- What ad format? (Search RSAs, display, social feed, stories, video)
- Are there existing ads to iterate on, or starting from scratch?

### 2. Product & Offer
- What are you promoting? (Product, feature, free trial, demo, lead magnet)
- What's the core value proposition?
- What makes this different from competitors?

### 3. Audience & Intent
- Who is the target audience?
- What stage of awareness? (Problem-aware, solution-aware, product-aware)
**Awareness stage mapping (critical for angle selection):**
- **Problem-unaware** → Curiosity/contrarian angles; avoid product names in headlines
- **Problem-aware** → Pain-point direct + solution tease; "There's a better way" framing
- **Solution-aware** → Benefit-led + social proof; highlight why this solution
- **Product-aware** → Offer-focused + urgency; overcome final objections
- **Most aware** → CTA-forward; they know, just need the push

- What pain points or desires drive them?

### 4. Performance Data (if iterating)
- What creative is currently running?
- Which headlines/descriptions are performing best? (CTR, conversion rate, ROAS)
- Which are underperforming?
- What angles or themes have been tested?

### 5. Constraints
- Brand voice guidelines or words to avoid?
- Compliance requirements? (Industry regulations, platform policies)
- Any mandatory elements? (Brand name, trademark symbols, disclaimers)

---

## Quick Start — Which Mode?

```
Is this the first time running ads for this product/offer?
├── YES → Mode 1 (Generate from Scratch)
│         Go to: "Before Starting" → gather context → "Generating Ad Copy"
└── NO  → Do you have performance data (CTR, conversions, ROAS)?
          ├── YES → Mode 2 (Iterate from Performance Data)
          │         Go to: "Iterating from Performance Data"
          └── NO  → Low impression volume (<1,000/headline)?
                    ├── YES → Run more traffic first before iterating
                    └── NO  → Treat as Mode 1, start fresh angles
```

## How This Skill Works

This skill supports two modes:

### Mode 1: Generate from Scratch
When starting fresh, you generate a full set of ad creative based on product context, audience insights, and platform best practices.

### Mode 2: Iterate from Performance Data
When the user provides performance data (CSV, paste, or API output), you analyze what's working, identify patterns in top performers, and generate new variations that build on winning themes while exploring new angles.

The core loop:

```
Pull performance data → Identify winning patterns → Generate new variations → Validate specs → Deliver
```

---

## Platform Specs

**Always enforce these limits.** Never deliver creative that exceeds platform character limits.

### Google Ads (Responsive Search Ads)

| Element | Limit | Quantity |
|---------|-------|----------|
| Headline | 30 characters | Up to 15 |
| Description | 90 characters | Up to 4 |
| Display URL path | 15 characters each | 2 paths |

**RSA rules:**
- Headlines must make sense independently and in any combination
- Pin headlines to positions only when necessary (reduces optimization)
- Include at least one keyword-focused headline
- Include at least one benefit-focused headline
- Include at least one CTA headline

**Search intent alignment:**
- Match headline tone to query intent: informational queries → educational angle; transactional queries → offer/CTA angle; navigational queries → brand + differentiator
- Use match types strategically: Broad match (reach) → test new angles; Phrase match → control intent signals; Exact match → highest-intent, lowest-volume
- Negative keywords are copy signals: if "free" is a negative, don't imply free in headlines even tangentially
- Align the headline to the specific keyword theme in that ad group — don't use the same RSA set across all ad groups

### Meta Ads (Facebook/Instagram)

| Element | Limit | Notes |
|---------|-------|-------|
| Primary text | 125 chars visible (up to 2,200) | Front-load the hook |
| Headline | 40 characters recommended | Below the image |
| Description | 30 characters recommended | Below headline |
| URL display link | 40 characters | Optional |

### LinkedIn Ads

| Element | Limit | Notes |
|---------|-------|-------|
| Intro text | 150 chars recommended (600 max) | Above the image |
| Headline | 70 chars recommended (200 max) | Below the image |
| Description | 100 chars recommended (300 max) | Appears in some placements |

### TikTok Ads

| Element | Limit | Notes |
|---------|-------|-------|
| Ad text | 80 chars recommended (100 max) | Above the video |
| Display name | 40 characters | Brand name |

### Twitter/X Ads

| Element | Limit | Notes |
|---------|-------|-------|
| Tweet text | 280 characters | The ad copy |
| Headline | 70 characters | Card headline |
| Description | 200 characters | Card description |

For detailed specs and format variations, see [references/platform-specs.md](references/platform-specs.md).

---

## Generating Ad Visuals

For image, video, voice, and code-rendered ad creative, load
[references/generative-tools.md](references/generative-tools.md). Before using
exact provider names, model IDs, API paths, pricing, limits, or availability,
check the dated source note in that reference and verify against official vendor
docs.

**Recommended workflow for scaled production:** Generate exploratory hero
creative with AI tools, build Remotion templates from winning patterns, batch
produce variations with data feeds, then keep AI for new angles and Remotion for
repeatable scale.

---

## Generating Ad Copy

### Step 1: Define Your Angles

Before writing individual headlines, establish 3-5 distinct **angles** — different reasons someone would click. Each angle should tap into a different motivation.

**Common angle categories:**

| Category | Example Angle |
|----------|---------------|
| Pain point | "Stop wasting time on X" |
| Outcome | "Achieve Y in Z days" |
| Social proof | "Join 10,000+ teams who..." |
| Curiosity | "The X secret top companies use" |
| Comparison | "Unlike X, we do Y" |
| Urgency | "Limited time: get X free" |
| Identity | "Built for [specific role/type]" |
| Contrarian | "Why [common practice] doesn't work" |
| Fear of missing out | "Don't miss your Q4 window" |
| Empathy | "We know how painful manual reporting is" |
| Aspiration | "The reporting setup high-growth teams use" |

### Step 2: Generate Variations per Angle

For each angle, generate multiple variations. Vary:
- **Word choice** — synonyms, active vs. passive
- **Specificity** — numbers vs. general claims
- **Tone** — direct vs. question vs. command
- **Structure** — short punch vs. full benefit statement

### Step 3: Validate Against Specs

Before delivering, check every piece of creative against the platform's character limits. Flag anything that's over and provide a trimmed alternative.

### Step 4: Organize for Upload

Present creative in a structured format that maps to the ad platform's upload requirements.

---

## Iterating from Performance Data

When the user provides performance data, follow this process:

### Step 1: Analyze Winners

Look at the top-performing creative (by CTR, conversion rate, or ROAS — ask which metric matters most) and identify:
**Winning pattern taxonomy — label every top performer by type:**

| Pattern Type | Identifies As | Signal |
|--------------|---------------|--------|
| **Number-led** | Starts with a stat/number | High CTR for skeptical audiences |
| **Question hook** | Opens as a question | High engagement for awareness stage |
| **Benefit-led** | Leads with the outcome, not the feature | High conversion for warm audiences |
| **Pain-point direct** | Names the exact frustration | High CTR for cold audiences |
| **Social proof** | Cites users, ratings, or customers | High trust signal, lower-funnel |
| **Contrarian** | Challenges conventional wisdom | High engagement, polarizing |
| **Power-word driven** | Uses: Free, New, Proven, Fast, Secret, Easy | Broad appeal, test for diminishing returns |

Label each winner with its pattern type. If 3+ winners share a type → that's your dominant pattern. Double down.

- **Winning themes** — What topics or pain points appear in top performers?
- **Winning structures** — Questions? Statements? Commands? Numbers?
- **Winning word patterns** — Specific words or phrases that recur?
- **Character utilization** — Are top performers shorter or longer?

### Step 2: Analyze Losers

Look at the worst performers and identify:

- **Themes that fall flat** — What angles aren't resonating?
- **Common patterns in low performers** — Too generic? Too long? Wrong tone?

### Step 3: Generate New Variations

Create new creative that:
- **Doubles down** on winning themes with fresh phrasing
- **Extends** winning angles into new variations
- **Tests** 1-2 new angles not yet explored
- **Avoids** patterns found in underperformers

### Step 4: Document the Iteration

Track what was learned and what's being tested:

```
## Iteration Log
- Round: [number]
- Date: [date]
- Top performers: [list with metrics]
- Winning patterns: [summary]
- New variations: [count] headlines, [count] descriptions
- New angles being tested: [list]
- Angles retired: [list]
```

---

## Writing Quality Standards

### Headlines That Click

**Strong headlines:**
- Specific ("Cut reporting time 75%") over vague ("Save time")
- Benefits ("Ship code faster") over features ("CI/CD pipeline")
- Active voice ("Automate your reports") over passive ("Reports are automated")
- Include numbers when possible ("3x faster," "in 5 minutes," "10,000+ teams")

**Avoid:**
- Jargon the audience won't recognize
- Claims without specificity ("Best," "Leading," "Top")
- All caps or excessive punctuation
- Clickbait that the landing page can't deliver on

### Social Proof Ad Formats

Social proof is the highest-trust headline category. Use these specific formats:

| Format | Template | Example |
|--------|----------|---------|
| **Testimonial snippet** | `"[Quote]" — [Role], [Company]` | `"Cut our reporting time 80%" — CMO, Acme Corp` |
| **Case study stat** | `[Company] [achieved X] with [Product]` | `How Stripe reduced reporting from 8h to 30min` |
| **User count** | `[Number]+ [audience type] trust [Product]` | `12,000+ marketing teams trust Databox` |
| **Review score** | `[Score]/5 on [Platform] — [Count] reviews` | `4.8/5 on G2 — 2,000+ reviews` |
| **Customer logo drop** | `Used by [Company1], [Company2], [Company3]` | `Trusted by HubSpot, Notion, and Figma` |

**Tips:**
- Use specific numbers over rounded ones ("12,847 teams" beats "12,000+ teams")
- Name the company/person when you have permission — it adds credibility
- Match proof type to audience: cold audiences → aggregate counts; warm → specific case studies
- Pull from G2, Capterra, Trustpilot for real quote snippets (don't fabricate)

### Descriptions That Convert

Descriptions should complement headlines, not repeat them. Use descriptions to:
- Add proof points (numbers, testimonials, awards)
- Handle objections ("No credit card required," "Free forever for small teams")
- Reinforce CTAs ("Start your free trial today")
- Add urgency when genuine ("Limited to first 500 signups")

### CTAs That Drive Action

Every RSA needs at least one CTA headline. Use these formulas:

| CTA Pattern | Formula | Example |
|-------------|---------|---------|
| **Action + Benefit** | `[Verb] [Benefit] [Timeframe]` | "Start Saving 10 Hours Today" |
| **Action + Proof** | `[Verb] [Social proof]` | "Join 12,000+ Marketing Teams" |
| **Low-friction entry** | `Try [Product] Free` / `See It in Action` | "Try Databox Free — No Card" |
| **Urgency** | `[Action] [Deadline/Scarcity]` | "Claim Your Free Month Now" |
| **Question CTA** | `Ready to [Benefit]?` | "Ready to Automate Reports?" |

**CTA rules for RSA:**
- Include 2-3 CTA headlines out of 15 — don't over-index on CTAs
- The best CTA addresses the micro-commitment barrier (what stops the click?)
- Match CTA to offer: demo/trial → "See It Free"; lead magnet → "Get the [Guide]"; purchase → "Get Started"

### Primary Text Hook Formulas (Meta/LinkedIn)

Primary text is where you hook or lose the reader in the first 1-2 lines. Use these proven frameworks:

| Formula | Structure | Example |
|---------|-----------|---------|
| **PAS** | Problem → Agitate → Solve | "Still building reports by hand? Every hour you spend copy-pasting is an hour not scaling. [Product] automates it in 5 minutes." |
| **Before/After/Bridge** | Pain state → Ideal state → How to get there | "Last quarter: 10 hours on reports. This quarter: 20 minutes. Here's what changed." |
| **AIDA** | Attention → Interest → Desire → Action | "10,000 marketers cut their reporting time by 75%. They switched to automated dashboards. No code, no friction. See how →" |
| **Question Hook** | Open with the exact question your audience is Googling | "Why does reporting take all day when the data's already there?" |
| **Contrarian** | Challenge a common belief | "More ad spend doesn't fix bad creative. It amplifies it." |

**Rules for primary text:**
- First sentence must work as a standalone scroll-stopper
- Front-load the highest-impact claim before the "See more" truncation (~125 chars)
- Match the hook formula to awareness stage: cold → PAS/Question; warm → Before/After; retargeting → Contrarian/Urgency

---

## Output Formats

### Standard Output

Organize by angle, with character counts:

```
## Angle: [Pain Point — Manual Reporting]

### Headlines (30 char max)
1. "Stop Building Reports by Hand" (29)
2. "Automate Your Weekly Reports" (28)
3. "Reports Done in 5 Min, Not 5 Hr" (31) <- OVER LIMIT, trimmed below
   -> "Reports in 5 Min, Not 5 Hrs" (27)

### Descriptions (90 char max)
1. "Marketing teams save 10+ hours/week with automated reporting. Start free." (73)
2. "Connect your data sources once. Get automated reports forever. No code required." (80)
```

### Bulk CSV Output

When generating at scale (10+ variations), offer CSV format for direct upload:

```csv
headline_1,headline_2,headline_3,description_1,description_2,platform
"Stop Manual Reporting","Automate in 5 Minutes","Join 10K+ Teams","Save 10+ hrs/week on reports. Start free.","Connect data sources once. Reports forever.","google_ads"
```

### Iteration Report

When iterating, include a summary:

```
## Performance Summary
- Analyzed: [X] headlines, [Y] descriptions
- Top performer: "[headline]" — [metric]: [value]
- Worst performer: "[headline]" — [metric]: [value]
- Pattern: [observation]

## New Creative
[organized variations]

## Recommendations
- [What to pause, what to scale, what to test next]
```

---

## Batch Generation Workflow

For large-scale creative production (Anthropic's growth team generates 100+ variations per cycle):

### 1. Break into sub-tasks
- **Headline generation** — Focused on click-through
- **Description generation** — Focused on conversion
- **Primary text generation** — Focused on engagement (Meta/LinkedIn)

### 2. Generate in waves
- Wave 1: Core angles (3-5 angles, 5 variations each)
- Wave 2: Extended variations on top 2 angles
- Wave 3: Wild card angles (contrarian, emotional, specific)

### 3. Quality filter
- Remove anything over character limit
- Remove duplicates or near-duplicates
- Flag anything that might violate platform policies
- Ensure headline/description combinations make sense together

---

## Creative Fatigue Management

Ad creative has a shelf life. Frequency exposure flattens CTR and CPM efficiency. Track these signals:

| Signal | Threshold | Action |
|--------|-----------|--------|
| Frequency > 3.0 (Meta) | Per ad set per week | Introduce new variation |
| CTR dropping > 20% week-over-week | Per headline/creative | Pause + replace |
| Relevance score declining | Meta ad relevance diagnostics | Refresh creative theme |
| Impression share loss (Google) | > 15% lost to rank | Add higher-intent headlines |

**Rotation strategy:**
- Maintain 3-5 active variations per ad set at all times
- Replace the lowest-performer when adding new creative (not the whole set)
- When refreshing, keep 1-2 proven control creatives and test 2-3 new variations
- Full creative reset (no controls) only when CTR has flatlined for 2+ weeks

**Warning signs:**
- Same top-performing headline unchanged for 6+ weeks → fatigue likely
- Comments on ads turning negative → audience saturation
- New creative immediately underperforming → landing page mismatch, not creative issue

## Pre-Delivery Checklist

Before handing off any ad creative batch, verify:

- [ ] Every headline is within character limit (count carefully — spaces count)
- [ ] RSA headlines make sense standalone, not just when combined
- [ ] At least 3 distinct angles covered (not just synonyms)
- [ ] At least 1 keyword-focused, 1 benefit-focused, 1 CTA headline (Google RSA)
- [ ] No claims that violate platform policies (gambling words, superlatives, personal attributes)
- [ ] Primary text hook survives the "See more" truncation (~125 chars for Meta)
- [ ] Description complements, not repeats, the headline
- [ ] CTA is present in at least 2 headlines per RSA
- [ ] Character counts shown inline for every item
- [ ] If iterating: iteration log is complete with date, patterns found, angles retired

## Common Mistakes

- **Writing headlines that only work together** — RSA headlines get combined randomly
- **Ignoring character limits** — Platforms truncate without warning
- **All variations sound the same** — Vary angles, not just word choice
- **No CTA headlines** — Always include action-oriented headlines
- **Generic descriptions** — "Learn more about our solution" wastes the slot
- **Iterating without data** — Gut feelings are less reliable than metrics
- **Testing too many things at once** — Change one variable per test cycle
- **Retiring creative too early** — Allow 1,000+ impressions before judging

---

## Tool Integrations

For pulling performance data and managing campaigns, see the [tools registry](../../tools/REGISTRY.md).

| Platform | Pull Performance Data | Manage Campaigns | Guide |
|----------|:---------------------:|:----------------:|-------|
| **Google Ads** | `google-ads campaigns list`, `google-ads reports get` | `google-ads campaigns create` | [google-ads.md](../../tools/integrations/google-ads.md) |
| **Meta Ads** | `meta-ads insights get` | `meta-ads campaigns list` | [meta-ads.md](../../tools/integrations/meta-ads.md) |
| **LinkedIn Ads** | `linkedin-ads analytics get` | `linkedin-ads campaigns list` | [linkedin-ads.md](../../tools/integrations/linkedin-ads.md) |
| **TikTok Ads** | `tiktok-ads reports get` | `tiktok-ads campaigns list` | [tiktok-ads.md](../../tools/integrations/tiktok-ads.md) |

### Workflow: Pull Data, Analyze, Generate

```bash
# 1. Pull recent ad performance
node tools/clis/google-ads.js reports get --type ad_performance --date-range last_30_days

# 2. Analyze output (identify top/bottom performers)
# 3. Feed winning patterns into this skill
# 4. Generate new variations
# 5. Upload to platform
```

---

## Related Skills

- **paid-ads**: For campaign strategy, targeting, budgets, and optimization
- **copywriting**: For landing page copy (where ad traffic lands)
- **ab-test-setup**: For structuring creative tests with statistical rigor
- **marketing-psychology**: For psychological principles behind high-performing creative
- **copy-editing**: For polishing ad copy before launch
