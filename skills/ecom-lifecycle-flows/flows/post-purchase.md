# Post-Purchase

## Overview

**Purpose:** Reduce buyer's remorse, set up successful product use, build loyalty, and create the conditions for repeat purchase. The post-purchase window is the most underused email real estate in e-commerce.

**Trigger:** Order confirmed / payment captured

**Goal:** Convert a one-time buyer into a repeat customer. Protect the first purchase experience. Every email here seeds the next purchase.

**Length:** 4-5 emails over 21-30 days

**Exit condition:** Repeat purchase → move to a new post-purchase flow (for the new order). Suppress from replenishment flow if this flow is running.

**Target:** 25-40% repeat purchase rate from first-time buyers

---

## Email Sequence

### Email 1 — Send immediately (or within 1 hour of order confirmation)
**Subject angle:** Order confirmed + anticipation building
**Preview text:** Order number + what happens next

**Copy angle:**
- Confirm the order (include order number, product name, estimated delivery)
- This is not a dry transactional email — use it to build excitement
- Reinforce the decision: "Great choice — here's why you'll love it"
- Short piece of content that sets up success (tip for using the product, what to expect)
- Set delivery expectations to prevent anxiety and support tickets
- Include a secondary action if time allows: follow on social, join community

**CTA:** Track your order / Follow us on [platform] for tips

**Note:** Many ESPs separate transactional vs. marketing emails. If using Klaviyo, this is the "Order Confirmation" flow — customize the template to add brand voice and the above copy elements.

---

### Email 2 — Day 3-5 (before or just after delivery)
**Subject angle:** Product education / "how to get the most out of [product]"
**Preview text:** Quick tip or usage guide teaser

**Copy angle:**
- Teach them how to use the product correctly — this alone reduces returns dramatically
- Lead with the outcome they want, then the method
- Short how-to (3-5 steps, or a GIF/video link if available)
- Set expectations: "You'll notice X in the first week"
- Include a quick tip that makes the product feel more premium or effective
- Soft ask: "Have questions? Reply to this email — we're here"

**CTA:** Read the full guide / Watch the tutorial / Shop accessories

---

### Email 3 — Day 7-10 (after delivery)
**Subject angle:** Review request / "How's it going?"
**Preview text:** "Would love to hear what you think"

**Copy angle:**
- Check in — warm, personal, not automated-feeling
- "We'd love to know how you're getting on with [product]"
- Make the review ask easy: link directly to review page
- Explain why reviews matter (they help other customers make the right choice)
- If they have a problem → make it easy to contact support (preempt a bad review with good service)
- Optionally: reward the review with loyalty points or a small incentive

**CTA:** Leave a review / Share your experience / Rate your order

---

### Email 4 — Day 14-21
**Subject angle:** Cross-sell / "customers who bought X also love Y"
**Preview text:** Complementary product teaser

**Copy angle:**
- "You've had [product] for a few weeks now — here's what pairs with it"
- Lead with the customer benefit of the complementary product (not just "buy more stuff")
- Show 2-3 complementary SKUs with brief benefit descriptions
- Social proof: "X customers who bought [original product] also love [cross-sell]"
- Offer a loyalty angle if applicable: VIP early access, bundle discount, points

**CTA:** Shop the pairing / Complete your routine / Add to your order

---

### Email 5 — Day 28-30 (optional for consumables)
**Subject angle:** Running low? Replenishment reminder
**Preview text:** "Based on typical usage, you might be getting close"

**Copy angle:**
- Only relevant for consumable products (skip for non-consumables — use email 4 cross-sell instead)
- "Based on normal use, you're probably at [X]% remaining"
- Easy one-click reorder link
- Lock in subscription savings if you have a subscribe-and-save offer

**CTA:** Reorder now / Subscribe and save [X]%

---

## Suppression Logic

- Suppress from welcome flow if they purchase during welcome sequence
- Suppress from cart abandonment if order is confirmed
- If customer orders again during post-purchase flow, restart post-purchase for new order

---

## Segmentation Notes

- **First-time buyer** → Full 5-email sequence, heavy on trust and education
- **Returning buyer** → Skip emails 1-2 education content, lead with review + cross-sell
- **High AOV purchase** → Add extra education content, consider SMS check-in alongside email
- **Gifted purchase** → Modify Email 2 for gift usage, add gift card / share-with-friend CTA

---

## A/B Test Priorities

1. Email 2: Tutorial email vs. community/social proof email
2. Email 3: Review ask at Day 7 vs. Day 10 (timing affects response quality)
3. Email 4: Cross-sell grid vs. single curated hero product
4. Email 1: Purely transactional tone vs. warm brand voice (measure repeat purchase impact)

---

## Success Metrics

| Metric | Benchmark | Good |
|--------|-----------|------|
| Repeat purchase rate | 25% | 35-40%+ |
| Review conversion (Email 3) | 5-10% | 15%+ |
| Cross-sell CTR (Email 4) | 8-12% | 15%+ |
| Return rate | Track vs. pre-flow baseline | Decreasing |
| Time-to-second-order | Track vs. baseline | Shortening |
