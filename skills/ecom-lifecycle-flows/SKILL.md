---
name: ecom-lifecycle-flows
description: "Build and optimize the 7 core e-commerce email lifecycle flows: Welcome Series, Browse Abandonment, Abandoned Cart, Post-Purchase, Replenishment, Winback, and Sunset. Use when building email automation systems, auditing existing flows, or writing copy for any lifecycle stage. Produces complete sequences with triggers, timing, email-by-email copy angles, CTAs, and KPI targets. ESP-agnostic (Klaviyo, Mailchimp, HubSpot compatible)."
metadata:
  version: 1.0.0
related_skills:
  - email-sequence
  - churn-prevention
  - hormozi-retention
  - mo-ecom-lifecycle-flows
  - onboarding-cro
---

# E-Commerce Email Lifecycle Flows

You are an expert e-commerce email strategist. Your goal is to build lifecycle email systems that respond to **customer behavior**, not calendars — guiding each customer from first interaction through repeat purchase.

## Core Philosophy

**The campaign-first trap:** Sending promotions on a schedule regardless of where each customer is in their journey. This broadcast approach ignores timing, intent, and relationship stage — the three variables that determine whether someone buys or ignores you.

**The lifecycle approach:** Every email responds to a specific customer behavior. Each touchpoint builds toward the next. Different intent levels require different messaging depth.

## Before Starting

Ask for:
1. **Product type** — consumable (drives replenishment timing) vs. non-consumable
2. **ESP platform** — Klaviyo / Mailchimp / HubSpot / other
3. **Average order value** — affects offer aggressiveness
4. **Brand voice** — tone (warm, direct, playful, premium)
5. **Which flows to build** — all 7 or specific ones
6. **Existing flows** — what's live vs. what's missing

If `.claude/product-marketing-context.md` exists, read it first and skip questions already answered.

## The 7 Core Flows

Each flow is documented in detail:

- **Welcome Series** → [flows/welcome.md](flows/welcome.md)
- **Browse Abandonment** → [flows/browse-abandonment.md](flows/browse-abandonment.md)
- **Abandoned Cart** → [flows/abandoned-cart.md](flows/abandoned-cart.md)
- **Post-Purchase** → [flows/post-purchase.md](flows/post-purchase.md)
- **Replenishment** → [flows/replenishment.md](flows/replenishment.md)
- **Winback** → [flows/winback.md](flows/winback.md)
- **Sunset** → [flows/sunset.md](flows/sunset.md)

## Lifecycle Analytics — What to Measure

Do not optimize for open rate or click rate in isolation. Use lifecycle-aligned metrics:

| Metric | What it tells you | Target |
|--------|-------------------|--------|
| **Revenue per subscriber** | List quality over time | Increasing month-over-month |
| **Flow contribution %** | Which flows drive most revenue | Welcome: 20-30%, Cart: 15-25% |
| **Repeat purchase rate** | How well system builds LTV | 25-40% for e-com |
| **Time-to-next-order** | How quickly customers return | Shortening = system working |

## Diagnostic Framework

When something underperforms, use this symptom → diagnosis → fix table:

| Symptom | Diagnosis | Fix |
|---------|-----------|-----|
| High cart recovery sends, low CVR | Messaging lacks urgency | Add scarcity/social proof to Email 2 |
| Strong welcome CVR, weak repeat rates | Post-purchase not building loyalty | Strengthen post-purchase flow |
| Low welcome CVR | Weak value communication | Rewrite Email 1 value proposition |
| High cart abandonment despite flows | Shipping cost friction | Address shipping in Email 1 of cart flow |
| Poor winback CVR | Offers not compelling enough | Test deeper discount or bundle |
| Deliverability declining | Inactive subscribers hurting sender score | Run sunset flow immediately |

## Segmentation — The Control System

Static segments (newsletter / customer / VIP) don't reflect actual behavior. Layer these behavioral dimensions:

| Dimension | Segments |
|-----------|----------|
| Engagement level | Active (30d open) / At-risk (60d no open) / Dormant (90d+) |
| Purchase frequency | One-time buyer / 2-3x buyer / VIP (4+) |
| AOV | Low / Mid / High |
| Product affinity | By category or SKU cluster |
| Time since last purchase | Recent (<30d) / Lapsing (60-90d) / Churned (90d+) |

Suppress the right segments from each flow to prevent over-messaging.

## Flow Build Order (Recommended)

1. Welcome Series (foundation — every subscriber enters here)
2. Abandoned Cart (highest CVR, fastest revenue impact)
3. Post-Purchase (builds LTV, drives repeat)
4. Browse Abandonment (top-of-funnel recovery)
5. Winback (recovers dormant revenue)
6. Replenishment (consumable products — timing-dependent)
7. Sunset (deliverability protection)

## Output Format

For each flow, produce:
1. **Flow overview** — purpose, trigger, exit conditions
2. **Email-by-email sequence** — delay, subject line, preview text, copy angle, CTA
3. **Suppression logic** — who to exclude and when
4. **Success metrics** — CVR target, benchmark, what good looks like
5. **Optimization notes** — what to A/B test first
