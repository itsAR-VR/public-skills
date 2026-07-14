# Winback

## Overview

**Purpose:** Reactivate customers who have gone dormant — they bought once (or more), but haven't returned in 60-120+ days. Acknowledge their absence without guilt, offer a genuine reason to return, and make re-engagement effortless.

**Trigger:** Last purchase date > 60/90/120 days ago (choose threshold based on your average purchase cycle)

**Goal:** Drive a repeat purchase from a customer who's forgotten you exist. This flow competes with their inertia — not a competitor.

**Length:** 3 emails over 14-21 days

**Exit condition:** Any purchase exits the flow. If no engagement after Email 3, move to Sunset flow.

**CVR target:** 3-8% of dormant customers → reactivation purchase

---

## Setting Your Winback Threshold

| Average purchase cycle | Winback trigger |
|------------------------|-----------------|
| < 30 days (high-frequency consumable) | 60 days no purchase |
| 30-60 days (monthly consumable) | 90 days no purchase |
| 60-120 days (quarterly purchase) | 120-150 days no purchase |
| 120+ days (seasonal / low frequency) | 180+ days no purchase |

Do not trigger winback before the customer has had a reasonable opportunity to repurchase naturally. Triggering too early cannibalizes organic repurchase.

---

## Email Sequence

### Email 1 — Day 0 (trigger fires)
**Subject angle:** "We miss you" — warm, no guilt, no pressure
**Preview text:** Something human and genuine, not promotional

**Copy angle:**
- Open warmly — acknowledge their absence without accusation
- Reference their history briefly: "It's been a while since [product] was in your life"
- No hard pitch — this is the re-introduction
- Remind them of what they liked: what they bought, why it worked, what results they got
- Soft invitation back: "When you're ready, we're here"
- Make re-engagement feel effortless — one button, one action

**CTA:** Come back and see what's new / Browse our latest

**Tone:** Warm, a little vulnerable, human. Not promotional. Not guilt-tripping.

---

### Email 2 — Day 7
**Subject angle:** Genuine reason to return — new product, social proof, or best offer
**Preview text:** Specific news hook or offer teaser

**Copy angle:**
- Give them a real reason to come back: new product launch, updated formula, bestseller they haven't tried, seasonal item
- Social proof: "Since you were last here, [X] customers discovered [product]"
- Customer transformation story — someone like them who came back and is glad they did
- Introduce a winback offer: discount, free shipping, free gift with purchase
- Create soft urgency: "This offer is for customers we haven't seen in a while — it won't be here forever"

**CTA:** Claim your welcome-back offer / Shop the new arrivals

---

### Email 3 — Day 14-21
**Subject angle:** Last chance — final attempt
**Preview text:** "This is the last time we'll reach out for a while"

**Copy angle:**
- Brief and honest: this is the last email in your winback series
- No hard sell — state clearly that you won't keep emailing them if they're not interested
- Best offer of the series (strongest discount, free product, exclusive access)
- Remove friction: "No need to remember your account — here's a direct link"
- Offer an alternative: "If you're not ready to shop, you can update your preferences here [link]" — this reduces unsubscribes and moves them to a lower-frequency segment instead

**CTA:** Claim your [X]% off before it expires / Update your preferences

---

## Suppression Logic

- Suppress anyone currently in replenishment flow (different intent — they're still active customers)
- Suppress VIPs who haven't purchased — run a separate VIP winback with a higher-value offer
- Suppress if they've gone through a winback sequence in the last 6 months
- Suppress if they unsubscribed from any previous email (honor the opt-out)

---

## Segmentation Tiers for Winback

Run different sequences by purchase history:

| Segment | Customization |
|---------|---------------|
| **1x buyer** | Focus on brand re-introduction, lower offer threshold |
| **2-3x buyer** | Lead with purchase history, stronger offer, "comeback" framing |
| **VIP (4+ purchases)** | Personal tone, most generous offer, handwritten-feel subject line |

---

## Avoiding Guilt-Tripping

Do NOT use:
- "Where did you go?" (accusatory)
- "You've abandoned us" (manipulative)
- "We've been waiting for you" (passive-aggressive)

DO use:
- "It's been a while — we hope everything's great"
- "We've missed having you around"
- "Whenever you're ready, we're here"

---

## A/B Test Priorities

1. Email 1: No offer vs. soft offer (does urgency-free feel better? test revenue/unsubscribe tradeoff)
2. Email 2: New product hook vs. social proof hook vs. discount hook
3. Email 3: Hard expiration urgency vs. soft "preferences update" angle
4. Subject lines: Name personalization vs. product reference vs. curiosity gap

---

## Success Metrics

| Metric | Benchmark | Good |
|--------|-----------|------|
| Flow CVR | 3% | 6-8%+ |
| Email 1 open rate | 20-30% | 35%+ |
| Email 3 CVR | 1-2% | 3-4%+ |
| Revenue recovered per dormant customer | Track monthly | Increasing |
| Post-winback LTV | Track | Increasing vs. non-winback cohort |
