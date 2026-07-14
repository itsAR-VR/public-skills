# Replenishment

## Overview

**Purpose:** Bring customers back to reorder at exactly the right moment — when they're running low, before they forget or go to a competitor. Timing is the entire game for this flow.

**Trigger:** Time-based (calculated from purchase date + average usage cycle) OR behavior-based (product page revisit after X days)

**Goal:** Drive a reorder before the customer runs out and makes a decision about an alternative brand.

**Length:** 2-3 emails over 7-10 days (centered around the predicted depletion date)

**Exit condition:** Repeat purchase exits immediately. If they subscribe (subscribe-and-save), exit and move to subscriber segment.

**CVR target:** 20-35% of replenishment-eligible customers → reorder

---

## Timing Logic

### For Consumables

Calculate depletion date from:
- **Average usage cycle** for your product category (e.g., 30-day supplement, 60-day cleaning product)
- **Quantity purchased** (single unit vs. multi-pack)
- **Subscription vs. one-time** purchase

**Send timing:**
- Email 1: 7 days before predicted depletion
- Email 2: 2-3 days before predicted depletion
- Email 3: Day of / 1-2 days after predicted depletion

### For Non-Consumables

Use complementary product introduction instead (see Post-Purchase Email 4). Replenishment flow is primarily for consumables. If your product is non-consumable, consider a replenishment flow for accessories, refills, or consumable components.

### Klaviyo Implementation Note

Use a "Placed Order" metric trigger + date-based delay. Calculate the predicted depletion date as a profile property. Filter by product SKU/category to target only replenishment-eligible products.

---

## Email Sequence

### Email 1 — 7 days before predicted depletion
**Subject angle:** Anticipatory reminder / "You might be getting low"
**Preview text:** "Based on typical use, you're probably running low on [product]"

**Copy angle:**
- Open with the usage-cycle logic: "If you've been using [product] daily, you're likely about a week away from running out"
- Make it feel like a helpful reminder from a friend, not a promotional push
- Lead with the benefit of not running out (maintain the routine, don't lose progress)
- One-click reorder link to exact SKU
- Introduce subscribe-and-save if you have it: "Never run out again — save [X]% on auto-ship"

**CTA:** Reorder [product] / Set up auto-ship and save

---

### Email 2 — 2-3 days before predicted depletion
**Subject angle:** Urgency — "You're almost out"
**Preview text:** "Don't lose your streak / progress / results"

**Copy angle:**
- Direct and brief: "You're probably a few days away from finishing your [product]"
- Loss-framing: what happens when they run out (lose progress, break routine, restart from scratch)
- Reinforce results they've already seen or should be seeing by now
- Subscribe-and-save push: "Most customers switch to auto-ship after their second order — never run out again"
- Shipping timeline: order today, receive before you run out

**CTA:** Reorder now — ships in [X] days / Subscribe and save [X]%

---

### Email 3 — Day of depletion / 1-2 days after
**Subject angle:** "Are you out yet?" / Last call
**Preview text:** "This is the last nudge — we promise"

**Copy angle:**
- Acknowledge you've sent a couple of reminders
- Brief and honest: "If you've run out, we're ready to ship today"
- If they're trying a competitor: "Give us one more shot — here's [incentive]"
- Offer a reorder incentive if margin allows (loyalty discount, free shipping, bonus product)
- This email is also a retention play — reactivate before the competitor's product makes them forget you

**CTA:** Get back on track / Reorder with [X]% off

---

## Suppression Logic

- Suppress anyone on an active subscription / auto-ship for this product
- Suppress if they've already placed a repeat order for this product
- Suppress if they've been in this sequence in the last 90 days (avoid over-triggering)
- Suppress if they've also entered winback flow (prioritize winback for dormant customers)

---

## Subscribe-and-Save Integration

Replenishment flow is the highest-converting moment to convert one-time buyers to subscribers. In every email:
- Show the subscribe-and-save option with clear savings percentage
- Emphasize convenience over savings (outcome: never run out > save money)
- Make subscription easy to cancel (remove the fear)

---

## A/B Test Priorities

1. Email 1 timing: 10 days before vs. 7 days before (more runway vs. more urgency)
2. Email 2 framing: Loss ("don't lose your progress") vs. Gain ("keep your results going")
3. Email 3: Discount offer vs. free shipping vs. bonus product incentive
4. Subscribe-and-save CTA prominence: primary CTA vs. secondary CTA

---

## Success Metrics

| Metric | Benchmark | Good |
|--------|-----------|------|
| Flow CVR | 20% | 30-35%+ |
| Subscribe-and-save conversion | 5-10% | 15%+ |
| Time-to-next-order vs. baseline | Baseline | Shortening |
| Email 1 open rate | 40-50% | 55%+ |
| Revenue per replenishment flow | Track monthly | Increasing |
