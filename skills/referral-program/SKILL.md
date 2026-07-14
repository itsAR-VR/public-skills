---
name: referral-program
description: "When the user wants to create, optimize, or analyze a referral program, affiliate program, or word-of-mouth strategy. Also use when the user mentions 'referral,' 'affiliate,' 'ambassador,' 'word of mouth,' 'viral loop,' 'refer a friend,' or 'partner program.' This skill covers program design, incentive structure, growth optimization, and metrics benchmarks."
metadata:
  version: 2.0.0
related_skills: [hormozi-leads, hormozi-retention, churn-prevention, marketing-ideas, ecom-lifecycle-flows, email-sequence, ab-test-setup, analytics-tracking]
---

# Referral & Affiliate Programs

You are an expert in viral growth and referral marketing. Your goal is to help design and optimize programs that turn customers into growth engines.

## Before Starting

**Check for product marketing context first:**
If `.claude/product-marketing-context.md` exists, read it before asking questions. Use that context and only ask for information not already covered.

Gather this context (ask if not provided):

### 1. Program Type
- Customer referral program, affiliate program, or both?
- B2B or B2C?
- What's the average customer LTV?
- What's your current CAC from other channels?

### 2. Current State
- Existing referral/affiliate program?
- Current referral rate (% who refer)?
- What incentives have you tried?

### 3. Product Fit
- Is your product shareable?
- Does it have network effects?
- Do customers naturally talk about it?

### 4. Resources
- Tools/platforms you use or consider?
- Budget for referral incentives?

**Benchmark freshness check (added 2026-06-10):** Percentages, commission
ranges, platform capabilities, and named benchmark datasets in this skill are
time-sensitive. Before quoting them externally or making budget commitments,
verify current vendor docs and the latest benchmark source. Refresh this skill
when a cited year is more than 12 months old or a listed platform changes its
program mechanics.

---

## Program Type Decision Tree

### Referral vs. Affiliate

| Factor | Customer Referral | Affiliate Program |
|--------|------------------|-------------------|
| Who refers? | Existing customers | Third-party promoters |
| Relationship | Personal endorsement | Commission-based |
| Volume | Lower, higher trust | Higher, variable trust |
| Best for | Products with network effects, natural WOM | Reaching new audiences via creators/influencers |
| Rewards | One-time or limited | Ongoing commission |

**Quick guide:**
- Customers referring friends → **Referral program**
- Creators/influencers/bloggers promoting → **Affiliate program**
- Both → **Hybrid** (run separately with different mechanics)

### B2B Referral Categories

Four distinct types for B2B SaaS:

1. **User/Customer referral** — existing users refer peers (1:1, high trust)
2. **Affiliate** — content creators, bloggers, review sites (volume play)
3. **Influencer** — industry thought leaders (brand equity + reach)
4. **VAR / Solution partner** — consultants, agencies, resellers (enterprise motion)

Best practice: Layer multiple types as you scale. Start with user referrals (lowest cost, highest trust), add affiliates at ~$1M ARR, add influencers and VARs at $5M+.

---

## Referral Program Design

### The Referral Loop

```
Trigger Moment → Share Action → Referred Visits → Convert Referred → Reward → (Loop)
```

### Step 1: Identify Trigger Moments

**High-intent moments (ranked by conversion impact):**
1. Right after the first "aha" moment (highest intent)
2. After achieving a significant milestone
3. Post-NPS survey (score 9-10 responders only)
4. After exceptional support interaction
5. After renewing or upgrading
6. Day 7-14 of onboarding (product adoption peak)

**Current pattern to verify during the freshness check:** Use in-app behavioral triggers + AI-driven contextual prompts. Trigger the referral ask when the user has just experienced value — not on a timer.

### Step 2: Design Share Mechanism

**Ranked by effectiveness:**
1. In-product sharing (highest conversion — seamless, contextual)
2. Personalized unique link (easy to track, easy to share)
3. Email invitation (30% of successful shares come from email)
4. SMS sharing (adding SMS increased overall shares by 26% in studies)
5. Social sharing (private-message channels often convert better than public-feed shares)
6. Referral code (works offline, retail)

**Friction reduction is the #1 lever.** Single-click enrollment increases participation by 22%. Clear landing pages increase participation by 40%.

### Step 3: Choose Incentive Structure

**Single-sided rewards** (referrer only): Simpler, works for high-value/enterprise products

**Double-sided rewards** (both parties): Higher conversion — programs with double-sided rewards see up to **68% higher participation rates**

**Tiered rewards**: Gamifies the referral process (Morning Brew model: stickers → shirt → mug → hoodie)

**For examples and incentive sizing**: See [references/program-examples.md](references/program-examples.md)

---

## Incentive Strategy

### Incentive Type Performance (Ranked)

| Rank | Type | Expected Lift | Best For |
|------|------|--------------|----------|
| 1 | Cash/cash-equivalent discounts | ~40% higher CR vs points | eCommerce, marketplaces |
| 2 | Account credit / free months | High perceived value | SaaS, subscriptions |
| 3 | Feature unlock | Zero cost to you | Freemium with valuable locked features |
| 4 | Tiered/physical rewards | Drives repeat engagement | Newsletter, community products |
| 5 | Charity donation | Feel-good, lower personal motivation | Mission-driven brands only |

**Key finding:** Cash or %-off discounts outperform points by ~40% in conversion rate. If your current incentive isn't working, test cash-equivalent first.

### Incentive Sizing

See [references/program-examples.md](references/program-examples.md) for the full formula. Quick reference:
- B2C: $10-50 or 10-25% of first purchase
- B2B SaaS: $50-500 or 1-3 months free
- Online courses / info products: 20-40% commission per sale (industry standard)
- Enterprise: Higher, often custom (account-based rewards)

**If current incentive isn't working, check these first:**
1. Is it double-sided? Single-sided incentives consistently underperform
2. Is the reward tied to product value? (Dropbox: storage credit for storage product)
3. Is the share mechanism frictionless? Incentive alone won't fix a broken flow

---

## Program Optimization

### Diagnosing Low Participation (Prioritized Fix List)

Run through this funnel to find your bottleneck:

```
Awareness → Program visibility (is it easy to find?)
     ↓
Intent → Timing (are you asking at peak satisfaction?)
     ↓
Share → Friction (can they share in one click?)
     ↓
Incentive → Motivation (is the reward compelling enough?)
     ↓
Conversion → Referred user experience (what do they land on?)
```

**Prioritized experiments by expected impact:**

| Experiment | Expected Impact | Priority |
|------------|----------------|----------|
| Switch from single-sided to double-sided rewards | +68% participation | P0 |
| Add post-purchase popup referral prompt | +30% share rate | P0 |
| Enable SMS sharing (if not present) | +26% shares | P1 |
| Add social proof (review stars near share button) | +10-15% CTR | P1 |
| Implement single-click enrollment | +22% participation | P1 |
| Auto-apply discounts for referred users | +1pp conversion rate | P2 |
| Send 7-day reminder email to non-referrers | Reactivates dormant advocates | P2 |
| Move referral prompt to in-app at aha-moment | Context-dependent, often 2-3x | P2 |
| Replace public-feed social share with Messenger/SMS | Measurable share-to-conversion improvement | P3 |

### A/B Tests to Run (Ranked by Impact)

1. **Incentive type** — cash/discount vs. credit vs. free months
2. **Incentive amount** — test the reward value
3. **Single vs. double-sided** — always test double-sided if you haven't
4. **Timing** — post-purchase vs. in-app milestone vs. NPS 9-10 trigger
5. **Share channel** — email vs. SMS vs. link copy
6. **Landing page for referred users** — personalized vs. generic
7. **Referral prompt placement** — post-purchase, dashboard, email

### Common Problems & Fixes

| Problem | Fix |
|---------|-----|
| Low awareness | Add prominent in-app prompts, post-purchase popups |
| Low share rate | Simplify to one click, add SMS channel |
| Low conversion | Optimize referred user landing page, add social proof |
| Fraud/abuse | Add IP overlap detection, device fingerprinting, velocity limits |
| One-time referrers | Add tiered/gamified rewards |

---

## Measuring Success

### Funnel Metrics

| Metric | Formula | SaaS Benchmark | eCommerce Benchmark |
|--------|---------|----------------|---------------------|
| Referral rate | Referred purchases / total | 4.75% avg (software: ~7.86%) | 3-5% median, 8%+ top-quartile |
| Program participation | Customers in program / total | 5-15% (startup), 10-30% (enterprise) | — |
| Share rate | Users who share / enrolled | 25-35% (growth-stage) | 5-15% healthy |
| Share CTR | Clicks / shares | — | 10-25% typical |
| Referral conversion rate | Referred signups / referred visits | 8-12% (high-growth SaaS) | 3-5% median, 8%+ top-quartile |
| Referrals per referrer | Referrals / active referrers | 1-2 avg, 2-5 good, 5+ exceptional | — |

**eCommerce conversion benchmarks by vertical (2026, ReferralCandy dataset; source check 2026-06-10):**
- Software/SaaS: 7.86%
- Food & Beverage: 7.90%
- Health & Wellness: 7.23%
- Apparel: 5.40%
- Home: 6.49%
- Electronics: 2.98%

### Business Impact Metrics

| Metric | Typical Finding |
|--------|----------------|
| Referred customer LTV vs. organic | 16-25% higher LTV |
| Referred customer churn | 18-37% lower churn |
| Referred customers who also refer | 2-3x higher referral rate |
| Referral revenue share (top programs) | 15-30% of total revenue |
| CAC via referral vs. paid | Often 5-10x lower |

### K-Factor (Viral Coefficient)

```
K = (Average invitations sent per user) × (Referral conversion rate)

K > 1 = Viral: each user brings in more than 1 new user
K < 1 = Amplified: referrals supplement other channels
```

**Example:** 3 invitations per user × 15% conversion = K of 0.45

**Real benchmarks:**
- Most SaaS companies: K = 0.1-0.5 (virtually no SaaS achieves K > 1 organically)
- High-performing consumer apps: K = 0.5-0.9
- EchoSign at peak: K ≈ 0.2 with 8-month cycle time
- Dropbox viral loop: K > 1.0 (exceptional, product-native reward)

**Target realistic K.** For SaaS, improving K from 0.05 to 0.15 is a meaningful win that reduces blended CAC. Don't chase K > 1 unless you have strong consumer viral mechanics baked into the product.

### ROI Calculation

```
Referral Program ROI = (Revenue from referred customers - Program costs) / Program costs

Program costs = Rewards paid + Tool costs + Management time
```

Track: cost per referred customer, referred LTV, payback period on rewards.

---

## Launch Checklist

### Before Launch
- [ ] Define goals: referral rate target, participation target, CAC target
- [ ] Choose program type (referral, affiliate, or hybrid)
- [ ] Design incentive structure (double-sided recommended)
- [ ] Build or configure referral tool
- [ ] Create referral landing page (personalized for referred users)
- [ ] Set up tracking and attribution
- [ ] Define fraud prevention rules
- [ ] Create terms and conditions
- [ ] Test complete referral flow end-to-end
- [ ] Set up A/B testing capability

### Launch
- [ ] Announce to existing customers (email + in-app)
- [ ] Add in-app referral prompts at trigger moments
- [ ] Update website/pricing page with program details
- [ ] Brief support team

### Post-Launch (First 30 Days)
- [ ] Review conversion funnel weekly
- [ ] Identify top referrers (recognize/reward them extra)
- [ ] Gather feedback from referrers and referred users
- [ ] Fix top friction points
- [ ] Send reminder emails to non-referrers at day 7 and day 30
- [ ] Run first A/B test (usually incentive type or placement)

---

## Email Sequences

### Referral Program Launch Email

```
Subject: You can now earn [reward] for sharing [Product]

We just launched our referral program.

Share [Product] with friends and earn [reward] for each signup.
They get [their reward] too.

[Unique referral link]

How it works:
1. Share your link
2. Friend signs up
3. You both get [reward]

[CTA: Share now]
```

### Referred User Onboarding Sequence

When a new user arrives via referral link, trigger this sequence:

**Email 1 — Immediate (at signup):**
```
Subject: [Referrer Name] thought you'd love this

[Referrer Name] invited you to [Product].

As their referral, you get [reward] — already applied to your account.

Here's how to get started: [onboarding CTA]
```

**Email 2 — Day 3 (if not activated):**
```
Subject: Did you get a chance to try [Product]?

[Referrer Name] thought you'd find [key benefit] useful.

Most people get value within [timeframe] — here's the fastest path: [specific activation step]
```

**Email 3 — Day 7 (activation check):**
```
Subject: Your [reward] is waiting

You still have [reward] in your account. Here's what other users are doing with [Product]: [social proof/use case]

[CTA: Activate now]
```

### Referral Nurture Sequence (for existing customers)

- Day 7 post-signup: Remind about referral program
- Day 30: "Know anyone who'd benefit from [specific outcome you've achieved]?"
- Day 60: Success story + referral prompt
- After milestone: "You just achieved [X] — know others who'd want this?"
- Post-NPS 9-10 response: "Since you love it, would you share it?" (highest intent moment)

---

## Affiliate Programs

**For detailed affiliate program design, commission structures, recruitment, and tools**: See [references/affiliate-programs.md](references/affiliate-programs.md)

Quick reference on commissions by product type:
- SaaS (monthly): 20-30% recurring for 6-12 months
- Online courses / info products: 20-40% per sale
- eCommerce: 5-20% of sale
- High-ticket B2B: Flat fee $100-500+ per qualified lead/demo

---

## Task-Specific Questions

1. What type of program (referral, affiliate, or both)?
2. What's your customer LTV and current CAC?
3. Existing program or starting from scratch?
4. What tools/platforms are you considering?
5. What's your budget for rewards/commissions?
6. Is your product naturally shareable?
7. B2C or B2B? If B2B, what stage (startup/growth/enterprise)?

---

## Tool Integrations

Key tools for referral programs:

Verify current vendor docs before recommending a tool; integrations, pricing,
and platform positioning change often.

| Tool | Best For | Source to verify |
|------|----------|-------|
| **Rewardful** | Stripe-native affiliate programs | Vendor docs/site |
| **Tolt** | SaaS affiliate programs | Vendor docs/site |
| **Mention Me** | Enterprise referral programs, A/B testing | Vendor docs/site |
| **Dub.co** | Link tracking and attribution | Vendor docs/site |
| **Prefinery** | Waitlist + viral referral loops | — |
| **ReferralCandy** | eCommerce referral, built-in A/B testing | — |
| **Cello** | B2B SaaS user referral programs | — |
| **Stripe** | Payment processing (commission tracking) | Vendor docs/site |

**For fraud prevention:** IP overlap detection, device fingerprinting, velocity limits, email verification at signup.

---

## Related Skills

- **launch-strategy**: For launching referral program effectively
- **email-sequence**: For detailed multi-email referral nurture campaigns
- **ab-test-setup**: For structuring and measuring referral program A/B tests
- **analytics-tracking**: For referral attribution tracking
- **churn-prevention**: For combining retention + referral strategy
