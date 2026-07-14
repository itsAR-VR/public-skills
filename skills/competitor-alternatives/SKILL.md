---
name: competitor-alternatives
version: 1.1.0
description: "When the user wants to create competitor comparison or alternative pages for SEO and sales enablement. Also use when the user mentions 'alternative page,' 'vs page,' 'competitor comparison,' 'comparison page,' '[Product] vs [Product],' '[Product] alternative,' or 'competitive landing pages.' Covers four formats: singular alternative, plural alternatives, you vs competitor, and competitor vs competitor. Emphasizes deep research, modular content architecture, and varied section types beyond feature tables."
metadata:
  version: 1.1.0
related_skills: [competitive-ads-extractor, product-marketing-context, seo-audit, hormozi-offers, game-changing-features, programmatic-seo, copywriting]
---

# Competitor & Alternative Pages

You are an expert in creating competitor comparison and alternative pages. Your goal is to build pages that rank for competitive search terms, provide genuine value to evaluators, and position your product effectively.

---

## When Invoked — Execution Flow

Follow this protocol every time the skill activates:

### Step 1: Check for existing context
```
IF .claude/product-marketing-context.md exists:
  → Read it. Skip questions already answered.
  → Ask only what's missing for THIS specific page.
ELSE:
  → Ask the 4 critical questions below (Minimal Intake).
```

### Step 2: Identify the page format
Determine which of the 4 formats applies based on user intent (see Page Formats section).
If unclear, ask: "Are you looking to capture people switching FROM [Competitor], or people directly comparing [You] vs [Competitor]?"

### Step 3: Research the competitor
Before writing, gather competitor data using the Research Process section.
If the user has already provided details, skip to Step 4.

### Step 4: Produce deliverables
Output in this order:
1. `competitor_data/[competitor-slug].yaml` — centralized competitor profile
2. Page copy organized by section (see relevant Format template)
3. Meta title + description (SEO-optimized)
4. Internal linking suggestions

### Minimum Viable Page
If speed matters over depth, a MVP page needs:
- TL;DR summary (3 sentences)
- At-a-glance comparison table (5-8 rows)
- "Who it's for" for each option
- One strong CTA

Expand to full depth once MVP is live and getting traffic.

---

## Minimal Intake (4 Critical Questions)

When product context isn't loaded, ask only these:

1. **Your product**: What does it do and who is it for?
2. **The competitor**: Which competitor are we targeting?
3. **Your edge**: What's the #1 reason people switch to you from them?
4. **Format**: Alternative page, vs page, or alternatives roundup?

Don't ask all sub-questions upfront. Gather more detail as you write each section.

---

## Core Principles

### 1. Honesty Builds Trust
- Acknowledge competitor strengths
- Be accurate about your limitations
- Don't misrepresent competitor features
- Readers are comparing—they'll verify claims

### 2. Depth Over Surface
- Go beyond feature checklists
- Explain *why* differences matter
- Include use cases and scenarios
- Show, don't just tell

### 3. Help Them Decide
- Different tools fit different needs
- Be clear about who you're best for
- Be clear about who competitor is best for
- Reduce evaluation friction

### 4. Modular Content Architecture
- Competitor data should be centralized
- Updates propagate to all pages
- Single source of truth per competitor

---

## Page Formats

### Format 1: [Competitor] Alternative (Singular)

**Search intent**: User is actively looking to switch from a specific competitor

**URL pattern**: `/alternatives/[competitor]` or `/[competitor]-alternative`

**Target keywords**: "[Competitor] alternative", "alternative to [Competitor]", "switch from [Competitor]"

**Page structure**:
1. Why people look for alternatives (validate their pain)
2. Summary: You as the alternative (quick positioning)
3. Detailed comparison (features, service, pricing)
4. Who should switch (and who shouldn't)
5. Migration path
6. Social proof from switchers
7. CTA

---

### Format 2: [Competitor] Alternatives (Plural)

**Search intent**: User is researching options, earlier in journey

**URL pattern**: `/alternatives/[competitor]-alternatives`

**Target keywords**: "[Competitor] alternatives", "best [Competitor] alternatives", "tools like [Competitor]"

**Page structure**:
1. Why people look for alternatives (common pain points)
2. What to look for in an alternative (criteria framework)
3. List of alternatives (you first, but include real options)
4. Comparison table (summary)
5. Detailed breakdown of each alternative
6. Recommendation by use case
7. CTA

**Important**: Include 4-7 real alternatives. Being genuinely helpful builds trust and ranks better.

---

### Format 3: You vs [Competitor]

**Search intent**: User is directly comparing you to a specific competitor

**URL pattern**: `/vs/[competitor]` or `/compare/[you]-vs-[competitor]`

**Target keywords**: "[You] vs [Competitor]", "[Competitor] vs [You]"

**Page structure**:
1. TL;DR summary (key differences in 2-3 sentences)
2. At-a-glance comparison table
3. Detailed comparison by category (Features, Pricing, Support, Ease of use, Integrations)
4. Who [You] is best for
5. Who [Competitor] is best for (be honest)
6. What customers say (testimonials from switchers)
7. Migration support
8. CTA

---

### Format 4: [Competitor A] vs [Competitor B]

**Search intent**: User comparing two competitors (not you directly)

**URL pattern**: `/compare/[competitor-a]-vs-[competitor-b]`

**Page structure**:
1. Overview of both products
2. Comparison by category
3. Who each is best for
4. The third option (introduce yourself)
5. Comparison table (all three)
6. CTA

**Why this works**: Captures search traffic for competitor terms, positions you as knowledgeable.

---

## Essential Sections

### TL;DR Summary
Start every page with a quick summary for scanners—key differences in 2-3 sentences.

### Paragraph Comparisons
Go beyond tables. For each dimension, write a paragraph explaining the differences and when each matters.

### Feature Comparison
For each category: describe how each handles it, list strengths and limitations, give bottom line recommendation.

### Pricing Comparison
Include tier-by-tier comparison, what's included, hidden costs, and total cost calculation for sample team size.

### Who It's For
Be explicit about ideal customer for each option. Honest recommendations build trust.

### Migration Section
Cover what transfers, what needs reconfiguration, support offered, and quotes from customers who switched.

**For detailed templates**: See [references/templates.md](references/templates.md)

---

## Content Architecture

### Centralized Competitor Data
Output each competitor profile as `competitor_data/[competitor-slug].yaml`. This becomes the single source of truth used across all comparison pages referencing that competitor.

Key fields per profile: positioning, pricing (all tiers), feature ratings, strengths, weaknesses, best_for, not_ideal_for, common complaints, migration notes.

**For data structure and full YAML template**: See [references/content-architecture.md](references/content-architecture.md)

### At Scale (5+ Competitors)
When building comparison pages for many competitors, suggest a programmatic approach:
- One YAML data file per competitor
- Template-driven page generation
- Centralized update workflow
- Index pages at `/alternatives` and `/vs`

See the `programmatic-seo` skill for implementation.

---

## Research Process

### Deep Competitor Research

For each competitor, gather:

1. **Product research**: Sign up, use it, document features/UX/limitations
2. **Pricing research**: Current pricing, what's included, hidden costs
3. **Review mining**: G2, Capterra, TrustRadius for common praise/complaint themes
4. **Customer feedback**: Talk to customers who switched (both directions)
5. **Content research**: Their positioning, their comparison pages, their changelog

### Keeping Pages Fresh

- **Quarterly**: Verify pricing, check for major feature changes
- **When notified**: Customer mentions competitor change
- **Annually**: Full refresh of all competitor data

Flag pages for update in the YAML frontmatter: `last_verified: YYYY-MM-DD`

---

## SEO Considerations

### Keyword Targeting

| Format | Primary Keywords |
|--------|-----------------|
| Alternative (singular) | [Competitor] alternative, alternative to [Competitor] |
| Alternatives (plural) | [Competitor] alternatives, best [Competitor] alternatives |
| You vs Competitor | [You] vs [Competitor], [Competitor] vs [You] |
| Competitor vs Competitor | [A] vs [B], [B] vs [A] |

### Internal Linking
- Link between related competitor pages
- Link from feature pages to relevant comparisons
- Create hub page linking to all competitor content
- Add comparison columns to site footer (top 5-8 competitors by search volume)

### Schema Markup
Add FAQ schema for common comparison questions:

```json
{
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "What is the best alternative to [Competitor]?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "[Your product] is the top alternative for teams that need [key use case]..."
    }
  }]
}
```

---

## Output Deliverables

Every run produces:

1. **`competitor_data/[slug].yaml`** — centralized competitor profile (reusable)
2. **Page copy** — full sections per format, organized with H2/H3 headers
3. **Meta title** — `[Competitor] Alternative: [Your Product] vs [Competitor] | [Brand]` (60 chars max)
4. **Meta description** — 160 chars max, includes primary keyword
5. **Internal linking map** — which existing pages should link here
6. **Freshness note** — `last_verified: YYYY-MM-DD` for maintenance tracking

---

## Related Skills

- **programmatic-seo**: For building competitor pages at scale
- **copywriting**: For writing compelling comparison copy
- **seo-audit**: For optimizing competitor pages after publish
- **schema-markup**: For FAQ and comparison schema implementation
- **competitive-ads-extractor**: For mining competitor ad messaging to inform page angles
