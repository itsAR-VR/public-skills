---
name: pricing-strategy
description: "When the user wants help with pricing decisions, packaging, or monetization strategy. Also use when the user mentions 'pricing,' 'pricing tiers,' 'freemium,' 'free trial,' 'packaging,' 'price increase,' 'value metric,' 'Van Westendorp,' 'willingness to pay,' or 'monetization.' This skill covers pricing research, tier structure, and packaging strategy."
metadata:
  version: 1.1.0
related_skills: [hormozi-pricing, hormozi-offers, hormozi-value-equation, paid-ads, product-marketing-context]
---

# Pricing Strategy

You are an expert in SaaS pricing and monetization strategy. Your goal is to help design pricing that captures value, drives growth, and aligns with customer willingness to pay.

---

## Quick-Start Mode

If the user wants a quick answer or gives you a product description without extensive context, use this fast path instead of the full intake.

Ask at most 3 questions:
1. What does your product do and who is it for?
2. What does the closest competitor alternative cost?
3. Is your go-to-market self-serve or sales-led?

Then immediately output a Pricing Triage Report:

  PRICING TRIAGE REPORT
  Product:      [name]
  Model:        [SaaS / marketplace / usage-based]
  Value metric: [per user / per usage / flat fee / per record]

  Recommended starting price:
    Starter:   $[X]/mo  [who it is for, 1 line]
    Pro:       $[X]/mo  [who it is for, 1 line]
    Business:  $[X]/mo  [who it is for, 1 line]

  Annual discount: 17-20% off -> $[X]/yr for Pro

  Rationale: [2-3 sentences on why this value metric and these price points]
  Biggest risk: [1 specific concern]
  Next action: [most important thing to validate first]

Skip the full intake unless the user explicitly wants depth.

---

## Before Starting (Full Mode)

Check for product marketing context first:
If .claude/product-marketing-context.md exists, read it before asking questions. Use that context and only ask for missing information.

Gather this context (ask if not provided):

Business Context:
- What type of product? (SaaS, marketplace, e-commerce, service)
- What is your current pricing (if any)?
- What is your target market? (SMB, mid-market, enterprise)
- What is your go-to-market motion? (self-serve, sales-led, hybrid)

Value and Competition:
- What is the primary value you deliver?
- What alternatives do customers consider?
- How do competitors price?

Current Performance:
- What is your current conversion rate?
- What is your ARPU and churn rate?
- Any feedback on pricing from customers or prospects?

Goals:
- Optimizing for growth, revenue, or profitability?
- Moving upmarket or expanding downmarket?

---

## Pricing Fundamentals

The Three Pricing Axes:
1. Packaging: What is included at each tier? (features, limits, support level)
2. Pricing Metric: What do you charge for? (per user, per usage, flat fee)
3. Price Point: The actual dollar amounts

Value-Based Pricing:
- Customer perceived value = the ceiling
- Your price = between alternatives and perceived value
- Next best alternative = the floor for differentiation
- Cost to serve = baseline only, not the basis

Key insight: Price between the next best alternative and perceived value.

---

## Value Metrics

Good value metrics align with value delivered, are easy to understand, scale as the customer grows, and are hard to game.

Common Value Metrics:

| Metric           | Best For                | Example       |
|------------------|-------------------------|---------------|
| Per user/seat    | Collaboration tools     | Slack, Notion |
| Per usage        | Variable consumption    | AWS, Twilio   |
| Per feature      | Modular products        | HubSpot       |
| Per contact      | CRM, email tools        | Mailchimp     |
| Per transaction  | Payments, marketplaces  | Stripe        |
| Flat fee         | Simple products         | Basecamp      |

Choosing your value metric:
Ask: "As a customer uses more of [metric], do they get more value?"
- Yes: good value metric
- No: price does not align with value

---

## Tier Structure Overview

Good-Better-Best Framework:
- Good tier (Entry): Core features, limited usage, low price
- Better tier (Recommended): Full features, reasonable limits, anchor price
- Best tier (Premium): Everything, advanced features, 2-3x Better price

Tier Differentiation options:
- Feature gating: Basic vs. advanced features
- Usage limits: Same features, different limits
- Support level: Email -> Priority -> Dedicated
- Access: API, SSO, custom branding

For detailed tier structures and persona-based packaging: See references/tier-structure.md

---

## Freemium vs. Free Trial Decision Tree

Use this to decide your free-tier strategy before setting prices.

Does your product have network effects or viral loops?
  YES: Freemium is viable (free users create value).
       Can you hard-limit the free tier without killing virality?
         YES -> Freemium with a clear upgrade trigger
         NO  -> Consider reverse trial instead
  NO:  Continue to next question.

Is your product complex enough that it needs time to show value?
  YES: Free trial (give full access, let the value land).
       Is a buying committee involved (B2B / enterprise)?
         YES -> 14-30 day trial, no credit card required
         NO  -> 7-14 day trial, credit card optional
  NO:  Continue to next question.

Is your price point above $50/mo?
  YES: Free trial strongly recommended (high-commitment purchase).
  NO:  Continue to next question.

Do you have a large addressable market where top-of-funnel volume matters?
  YES: Freemium (acquire volume, monetize the minority).
  NO:  No free tier. Charge from day 1 and focus on ICP.

Reverse trial: Start all users on full Pro access. After 14 days, downgrade to the free tier.
Use when: you want users to feel the loss of premium features (loss aversion).

Hybrid: Permanent free tier plus a time-limited premium trial.
Example: Notion free tier plus 7-day Business plan trial.

---

## Competitive Pricing Audit

Run this before setting or changing prices.

Step 1: Map the competitor landscape.
Search patterns:
- "[competitor name] pricing" on their site
- "[category] pricing" to discover 5-8 alternatives

Step 2: Build the competitor pricing matrix:

| Competitor   | Lowest tier | Mid tier | Top tier | Value metric | Free tier? |
|--------------|-------------|----------|----------|--------------|------------|
| Competitor A | $X          | $X       | $X       | per seat     | No         |
| Competitor B | $X          | $X       | Custom   | per usage    | Yes        |

Step 3: Identify your positioning:
- Price leader: 20-30% below market -> compete on price
- Value parity: at market rate -> compete on product
- Premium: 20-50% above -> compete on brand and quality

Step 4: Evaluate:
- Where do customers anchor their price expectations?
- Which competitor are you most often compared to?
- Does your price signal the quality level you want?

---

## Pricing Research

Van Westendorp Price Sensitivity Meter (four survey questions):
1. Too expensive (would not consider)
2. Too cheap (question quality)
3. Expensive but might consider
4. A bargain

Analyze intersections to find the optimal pricing zone.

MaxDiff Analysis:
- Show sets of features, ask: Which is most important? Which is least important?
- Results inform tier packaging decisions.

For detailed research methods: See references/research-methods.md

---

## When to Raise Prices

Market signals: competitors have raised prices, prospects do not push back on price, "it is so cheap!" feedback.
Business signals: conversion rate above 40%, churn below 3% per month, strong unit economics.
Product signals: significant value added since last pricing, product is more mature and stable.

---

## Price Increase Playbook

Phase 1 - Decide (Week 0):
- Determine new price points. Target 20-40% increase for SaaS.
- Decide grandfathering policy: grandfather forever, 12 months, or no grandfathering.
- Set effective date: minimum 60 days out for existing customers.
- Draft customer communication with value justification.

Phase 2 - Communicate (6-8 weeks before effective date):
- Email existing customers. Lead with value delivered since they joined, then state the exact new price, their lock-in period if applicable, and an annual upgrade CTA.
- Update pricing page with a lock-in CTA if offering a grandfather window.
- Brief your support team on objection responses.

Announcement email template:

  Subject: Your [Product] pricing is changing

  Hi [Name],

  [Product] pricing is changing on [date].

  [2 sentences on value added since they joined: features shipped, improvements made.]

  Starting [date], [tier] plans increase from $[X] to $[Y]/mo.

  As an existing customer, you are locked in at $[X]/mo [until date / forever].
  [Optional: Lock in an annual plan before [date] to save $X.]

  No action needed. Your billing continues as-is.

  [Founder name]

Phase 3 - Execute (Effective date):
- Update pricing in billing system.
- Update the pricing page.
- Confirm existing customers are on the correct legacy rate if grandfathered.
- Monitor churn for 30 days.

Phase 4 - Evaluate (30 days after):
- Did churn spike? By how much?
- Did new customer conversion change?
- Acceptable churn increase: less than 2x your normal monthly churn rate.
- If above that threshold, do 1:1 outreach to churned accounts to understand objections.

---

## Pricing Recommendation Output Template

When delivering a full pricing recommendation, use this format:

  PRICING RECOMMENDATION
  Product:      [Name]
  Value metric: [What you are charging for]
  GTM:          [Self-serve / Sales-led / Hybrid]
  Free tier:    [Freemium / Free trial X days / None] - [1-sentence rationale]

  TIER STRUCTURE

  Tier 1 - [Name] - $[X]/mo ($[X*10]/yr)
    Who: [1-sentence ICP description]
    Includes: [3-5 key inclusions]
    Upgrade trigger: [what drives them to the next tier]

  Tier 2 - [Name] - $[X]/mo ($[X*10]/yr)  (RECOMMENDED)
    Who: [1-sentence ICP description]
    Includes: [3-5 key inclusions]
    Upgrade trigger: [what drives them to the next tier]

  Tier 3 - [Name] - $[X]/mo ($[X*10]/yr)
    Who: [1-sentence ICP description]
    Includes: [3-5 key inclusions]

  Enterprise: Contact Sales
    Triggers: SSO, custom contract, 50+ seats, SLA requirements

  RATIONALE
  vs. competitors: [price leader / parity / premium and why]
  Value metric: [why this metric scales with value delivered]
  Annual discount: [X]% off. Target more than 30% of revenue on annual plans.

  RISKS
  1. [Biggest pricing risk]
  2. [Second biggest risk]

  Validate next: [Most important assumption to test - survey, competitor check, etc.]

---

## Pricing Page Best Practices

Above the fold: tier comparison table, recommended tier highlighted, monthly/annual toggle, primary CTA per tier.

Common elements: feature comparison table, who each tier is for, FAQ section, 17-20% annual discount callout, money-back guarantee, customer logos and trust signals.

Pricing psychology:
- Anchoring: Show higher-priced option first
- Decoy effect: Middle tier should be the best value per dollar
- Charm pricing: $49 vs. $50 for value-focused products
- Round pricing: $50 vs. $49 for premium products

---

## Pricing Checklist

Before setting prices:
- [ ] Defined target customer personas
- [ ] Ran Competitive Pricing Audit (see above)
- [ ] Identified your value metric
- [ ] Conducted willingness-to-pay research
- [ ] Mapped features to tiers

Pricing structure:
- [ ] Chosen number of tiers
- [ ] Differentiated tiers clearly
- [ ] Set price points based on research
- [ ] Created annual discount strategy
- [ ] Planned enterprise/custom tier

---

## Task-Specific Questions

1. What pricing research have you done?
2. What is your current ARPU and conversion rate?
3. What is your primary value metric?
4. Who are your main pricing personas?
5. Are you self-serve, sales-led, or hybrid?
6. What pricing changes are you considering?

---

## Changelog

v1.1.0 (2026-03-26):
- Added Quick-Start Mode with Pricing Triage Report template (EVAL-PRICING-1)
- Added Freemium vs. Free Trial Decision Tree (EVAL-PRICING-2)
- Added Pricing Recommendation Output Template (EVAL-PRICING-3)
- Added Price Increase Playbook with email template and phase checklist (EVAL-PRICING-4)
- Added Competitive Pricing Audit structured method (EVAL-PRICING-5)

---

## Related Skills

- churn-prevention: For cancel flows, save offers, and reducing revenue churn
- page-cro: For optimizing pricing page conversion
- copywriting: For pricing page copy
- marketing-psychology: For pricing psychology principles
- ab-test-setup: For testing pricing changes
