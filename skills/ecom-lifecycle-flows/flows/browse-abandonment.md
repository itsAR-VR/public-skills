# Browse Abandonment

## Overview

**Purpose:** Re-capture interest from visitors who viewed a product but didn't add to cart. This is low-commitment behavior — they were curious, not ready. Messaging should match that intent level.

**Trigger:** Viewed a product page (or category page) → session ended without cart add → no purchase in last X days

**Goal:** Bring them back to the product page and nudge toward cart add. Do not over-pressure — they weren't ready to buy.

**Length:** 2-3 emails over 48 hours

**Exit condition:** Cart add or purchase → move to cart flow or post-purchase. Any conversion exits the browse flow.

**CVR target:** 2-5% of browse abandoners → purchase

---

## Email Sequence

### Email 1 — 1 hour after browse session ends
**Subject angle:** Gentle reminder / "you were looking at this"
**Preview text:** Product name or benefit teaser

**Copy angle:**
- Low-pressure, conversational tone — "Noticed you checking this out"
- Show the specific product they viewed (dynamic product block)
- Lead with one benefit or use case — give them a reason to care
- No urgency yet — they weren't ready; don't push
- Answer one likely question (what does it do / why is it different)

**CTA:** Take another look / See [Product Name] again

---

### Email 2 — 24 hours later
**Subject angle:** Social proof / "others are loving this"
**Preview text:** Specific review or star rating

**Copy angle:**
- Lead with customer reviews for the specific product they viewed
- 2-3 outcome-based quotes ("I used to X, now Y because of this product")
- Introduce scarcity if genuine (low stock, limited batch)
- Light urgency: "Others have been looking at this too"
- Objection handling: returns, guarantee, shipping

**CTA:** Read more reviews / See what others are saying / Shop [Product]

---

### Email 3 — 48 hours later (optional — higher-intent visitors only)
**Subject angle:** Last nudge / small offer to break hesitation
**Preview text:** "Still thinking about it? Here's a little help."

**Copy angle:**
- Acknowledge the hesitation without pressure
- Offer a small incentive if margin allows (free shipping, small discount, bonus gift)
- If no discount available: re-lead with the strongest use case or bundle angle
- Create soft close: "If it's not right for you, no worries — we're here when you're ready"

**CTA:** Get [X]% off your first order / Try it risk-free

---

## Suppression Logic

- Suppress if customer purchased in the last 30 days (don't browse-abandon someone who just bought)
- Suppress if they're currently in an active cart abandonment flow
- Suppress VIP customers from Email 3 discount offers (they don't need incentivization)
- Suppress if they've gone through browse abandonment in the last 7 days for the same product

---

## Segmentation Notes

- **First-time visitor** → Full 3-email sequence, lean on brand trust in Email 1
- **Previous customer** → Skip Email 1 brand trust copy, lead with product benefit and loyalty acknowledgment
- **High-intent page** (best-seller, limited edition) → Add urgency earlier in the sequence

---

## A/B Test Priorities

1. Email 1 delay: 1 hour vs. 3 hours vs. same-day EOD
2. Email 1 subject: Curiosity ("Still thinking about it?") vs. direct ("You left [Product] behind")
3. Email 3: Discount offer vs. free shipping vs. value-add (how-to content, recipe, usage guide)

---

## Success Metrics

| Metric | Benchmark | Good |
|--------|-----------|------|
| Flow CVR | 2% | 4-5%+ |
| Email 1 open rate | 35-45% | 50%+ |
| Email 1 CTR | 5-8% | 10-12%+ |
| Email 2 open rate | 25-35% | 40%+ |
