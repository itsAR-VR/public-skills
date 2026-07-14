# Abandoned Cart

## Overview

**Purpose:** Recover purchases from shoppers who added to cart (or started checkout) but didn't complete. This is the highest-intent behavior outside of a purchase — messaging should match that urgency.

**Trigger:** Item added to cart (or checkout started) → no purchase within 1 hour

**Goal:** Complete the purchase. This is not a nurture flow — it's a recovery flow. Be direct.

**Length:** 3 emails over 48-72 hours

**Exit condition:** Purchase at any point exits the flow immediately.

**CVR target:** 10-15% of cart abandoners → purchase

---

## Email Sequence

### Email 1 — 1 hour after abandonment
**Subject angle:** Simple, direct cart reminder — no tricks
**Preview text:** Product name + cart reminder

**Copy angle:**
- Immediately show their cart (dynamic product block with image, name, price)
- One-line opener: "You left something behind" or "Your cart is waiting"
- Address the most common abandonment reason upfront: shipping costs, trust, hesitation
  - State your shipping policy clearly
  - Include guarantee / free returns
  - Include security/trust signals (secure checkout badge)
- No urgency yet — keep it simple and easy
- Make completing checkout the path of least resistance

**CTA:** Complete your order / Return to cart / Finish checkout

---

### Email 2 — 24 hours later
**Subject angle:** Social proof + light urgency
**Preview text:** "X people bought this today" or review snippet

**Copy angle:**
- Reinforce the decision they were about to make
- Lead with outcome: what life looks like after buying this product
- Customer reviews for the specific cart item (2-3 quotes)
- Introduce genuine scarcity if applicable: "Only X left in stock"
- Address the #1 objection for your product category specifically
- Offer free shipping if not already offered (if margin allows)

**CTA:** Get it before it sells out / Complete your purchase

---

### Email 3 — 48-72 hours later
**Subject angle:** Final nudge — offer or last call
**Preview text:** Discount code or expiration signal

**Copy angle:**
- This is your last email in the sequence — say so briefly
- Offer your best incentive: percentage discount, free gift, free shipping
- Create real urgency: the offer expires in 24 hours
- Brief, no fluff — they've seen two emails already; respect their time
- One final objection handler (risk reversal: money-back guarantee, easy returns)
- If you don't want to offer a discount: use a story-driven last push or highest-impact review

**CTA:** Claim your [X]% off / Use code [CODE] at checkout

---

## Suppression Logic

- Exit flow immediately on purchase (at any email)
- Suppress customers who purchase a different item during the sequence (don't recover a cart if they already bought something else)
- Suppress if customer has received a cart abandonment email in the last 14 days (don't double-trigger)
- Suppress VIP segment from Email 3 discount (reward with service, not discounts)
- Do not send Email 3 discount to customers who bought at full price previously if protecting margin

---

## Segmentation Notes

- **First-time visitor** → Full 3 emails, lean on trust signals in Email 1
- **Returning customer** → Email 1 tone shifts to "Welcome back" — reference purchase history
- **High AOV cart** → Consider phone/SMS follow-up alongside email for Email 2
- **Discount-history customer** → They may wait for Email 3 discount; consider A/B testing skipping the discount

---

## Shipping Objection Handling

Cart abandonment is often a shipping cost problem, not a messaging problem. If CVR is low despite good copy:
- Test free shipping threshold (e.g., "Free shipping on orders over $X")
- Mention shipping cost in Email 1 explicitly and either justify or remove it
- Survey recent abandoners to confirm root cause

---

## A/B Test Priorities

1. Email 1 delay: 30 min vs. 1 hour vs. 2 hours
2. Email 3: Discount vs. no discount (protect margin, test impact)
3. Subject lines: Direct ("Your cart expires soon") vs. curiosity ("Did something go wrong?")
4. Email 1: Minimal/text-only vs. full product image layout

---

## Success Metrics

| Metric | Benchmark | Good |
|--------|-----------|------|
| Flow CVR | 10% | 15%+ |
| Email 1 open rate | 40-50% | 55-60% |
| Email 1 CVR | 5-8% | 10%+ |
| Email 3 CVR | 2-4% | 5%+ |
| Revenue recovered per flow email | Track monthly | Increasing |
