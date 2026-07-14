# Sunset

## Overview

**Purpose:** Permanently remove or suppress subscribers who remain completely unengaged after winback attempts. Protecting sender reputation and deliverability is more valuable than list size. Dead weight on your list actively hurts every email you send.

**Trigger:** Completed winback flow with no engagement (no open, no click, no purchase) — OR — 90-120+ days of no email opens with no purchase history

**Goal:** Either reactivate with one final attempt, or gracefully exit them from the active list. A smaller, engaged list always outperforms a large, unengaged one.

**Length:** 2 emails over 7-14 days

**Exit condition:**
- Opens or clicks → move to re-engagement segment, remove from sunset sequence
- Purchases → move to post-purchase
- No engagement → suppress / unsubscribe

**Target:** Reactivate 5-10% of sunset-eligible subscribers. Accept the rest are gone.

---

## Why Sunset Matters

| Without sunset | With sunset |
|----------------|-------------|
| High spam complaint rate | Low spam complaint rate |
| Low sender reputation | Strong sender reputation |
| Emails landing in promotions/spam | Emails landing in inbox |
| Inflated list size, low revenue per subscriber | Lean list, high revenue per subscriber |
| Domain/IP reputation degrading over time | Domain/IP health maintained |

Every unengaged subscriber on your list is actively dragging down deliverability for your engaged subscribers. Sunsetting protects the people who actually want to hear from you.

---

## Email Sequence

### Email 1 — Day 0 (trigger fires)
**Subject angle:** Preference check / "Still want to hear from us?"
**Preview text:** "We want to make sure we're sending you the right things"

**Copy angle:**
- Direct and respectful: "We've noticed you haven't opened our emails in a while"
- No guilt, no pressure — acknowledge that email preferences change
- Give them a clear choice:
  - Option A: Stay subscribed (click to confirm or update preferences)
  - Option B: Unsubscribe easily and clearly
  - Option C: Change to a lower-frequency list ("just the important stuff")
- Explain what happens if they don't click: "If we don't hear from you, we'll remove you from our list in [X] days"
- This email is also a soft winback — if the subject line works and they open, that's a win

**CTA buttons (2):**
- "Yes, keep me subscribed"
- "No thanks, unsubscribe me"

**Tone:** Calm, respectful, zero pressure. This is a preference conversation, not a sales pitch.

---

### Email 2 — Day 7-14 (if no engagement on Email 1)
**Subject angle:** "This is goodbye (for now)"
**Preview text:** "We're removing you from our list — but you're always welcome back"

**Copy angle:**
- Brief, warm, no drama
- "Since we haven't heard from you, we're removing you from our list today"
- Leave the door open: include a re-subscribe link
- Optionally: final offer (your best incentive) — but only if you want to give dormant subscribers one last shot
- Thank them for having been on the list at all

**CTA:** Re-subscribe / Come back anytime

**Note:** After this email, suppress them. Do not continue emailing. In Klaviyo: move to a "Suppressed" or "Sunset" list. They can re-subscribe themselves through your form.

---

## Technical Implementation

### Klaviyo Setup
1. Create a "Sunset" segment: No opens in 90 days + completed winback flow (or no purchase history + no opens in 120 days)
2. Build a sunset flow triggered by segment membership
3. On Email 1 click ("Keep me subscribed") → tag profile as "Re-engaged", exit flow, add to active segment
4. On Email 2 completion with no engagement → add to suppression list, remove from all active flows
5. Set "Cleaned" or "Suppressed" status — do not hard delete (you may need this data for lookalike audiences)

### Suppression vs. Unsubscribe
- **Unsubscribe:** Customer-initiated. Removes from marketing sends but keeps record.
- **Suppression:** Marketer-initiated. You stop sending; they can re-subscribe.
- Use suppression for sunset (not hard unsubscribe) so they can return organically.

---

## List Hygiene Schedule

Run sunset continuously as a flow (triggered by behavior), but also run a manual quarterly audit:

| Frequency | Action |
|-----------|--------|
| Ongoing (flow) | Sunset anyone completing winback with no response |
| Quarterly | Audit all profiles with 90+ day no-open, re-run segment |
| Monthly | Review spam complaint rate — target < 0.1% |
| After major campaigns | Check for bounce spikes — remove hard bounces immediately |

---

## Suppression Logic

- Suppress VIP customers from sunset entirely (high historical LTV — give them more grace, custom treatment)
- Do not sunset someone who purchased recently but hasn't opened email (they may be a buyer-not-opener segment — valuable)
- Sunset email-only, not SMS (unengaged email subscriber may still be an engaged SMS subscriber)

---

## A/B Test Priorities

1. Email 1 subject line: Question ("Still want to hear from us?") vs. Direct ("We're cleaning our list")
2. Email 1: Preference center (3 options) vs. simple yes/no
3. Email 2: Final offer vs. no offer (does an incentive reactivate more than its cost?)
4. Timing: Day 7 vs. Day 14 for Email 2

---

## Success Metrics

| Metric | Benchmark | Good |
|--------|-----------|------|
| Reactivation rate (click "keep me") | 5% | 8-12% |
| Unsubscribe rate on Email 1 | 10-20% (expected) | Lower with preference center |
| Post-sunset list engagement rate | Increasing | 30%+ open rate on remaining list |
| Spam complaint rate (overall) | < 0.1% | < 0.05% |
| Deliverability score improvement | Measurable uplift within 30 days |
