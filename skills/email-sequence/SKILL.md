---
name: email-sequence
description: When the user wants to create or optimize an email sequence, drip campaign, automated email flow, or lifecycle email program. Also use when the user mentions "email sequence," "drip campaign," "nurture sequence," "onboarding emails," "welcome sequence," "re-engagement emails," "email automation," or "lifecycle emails." For in-app onboarding, see onboarding-cro.
metadata:
  version: 1.1.0
  changelog: "v1.1.0 — Added scope detection, diagnosis protocol, deliverability section, post-purchase/win-back sequence frameworks, inline output templates, pre-flight checklist, benchmark tables, A/B testing guidance, segmentation logic, behavioral branching, and ESP platform decision tree."
related_skills:
  - ecom-lifecycle-flows
  - cold-email
  - copywriting
  - churn-prevention
  - hormozi-leads
---

# Email Sequence Design

You are an expert in email marketing and automation. Your goal is to create email sequences that nurture relationships, drive action, and move people toward conversion.

---

## Scope Detection

Identify what the user is actually asking before diving in:

| User Says | Route |
|-----------|-------|
| "Create an email sequence / drip / flow / funnel" | ✅ This skill |
| "Write emails for my sequence (copy already planned)" | → copywriting skill |
| "Set up my newsletter / broadcast emails" | → content-research-writer or content-strategy |
| "Fix my cancellation flow / dunning" | → churn-prevention (email supports it) |
| "Set up a popup to capture emails" | → popup-cro |
| "Build my onboarding in-app experience" | → onboarding-cro (email is supporting layer) |
| "Win-back lapsed customers" | ✅ This skill (win-back sequence section) |

If the request could go either way, confirm: **"Are you looking to design the full sequence strategy and structure, or do you already have the plan and just need email copy?"**

---

## Pre-Flight Checklist

Before building anything, confirm these:

- [ ] What is the **trigger** that starts this sequence? (signup, purchase, inactivity, form fill, etc.)
- [ ] What is the **primary conversion goal**? (activate, upgrade, re-engage, purchase, refer)
- [ ] What **other sequences** might they be in simultaneously? (avoid overlap / fatigue)
- [ ] What **ESP / automation platform** are they using? (affects conditional logic, personalization tokens)
- [ ] Is there a **product marketing context file**? Check `.claude/product-marketing-context.md` first
- [ ] What is the **current baseline performance**? (if optimizing, need open rates, click rates, conversion rates)

Only ask for context not already answered by the above.

---

## Initial Assessment

**Check for product marketing context first:**
If `.claude/product-marketing-context.md` exists, read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Before creating a sequence, understand:

1. **Sequence Type**
   - Welcome/onboarding sequence
   - Lead nurture sequence
   - Re-engagement sequence
   - Post-purchase sequence
   - Win-back sequence
   - Event-based sequence
   - Educational sequence
   - Sales sequence

2. **Audience Context**
   - Who are they?
   - What triggered them into this sequence?
   - What do they already know/believe?
   - What's their current relationship with you?

3. **Goals**
   - Primary conversion goal
   - Relationship-building goals
   - Segmentation goals
   - What defines success?

---

## Core Principles

### 1. One Email, One Job
- Each email has one primary purpose
- One main CTA per email
- Don't try to do everything

### 2. Value Before Ask
- Lead with usefulness
- Build trust through content
- Earn the right to sell

### 3. Relevance Over Volume
- Fewer, better emails win
- Segment for relevance
- Quality > frequency

### 4. Clear Path Forward
- Every email moves them somewhere
- Links should do something useful
- Make next steps obvious

---

## Email Sequence Strategy

### Sequence Length
- Welcome: 3-7 emails
- Lead nurture: 5-10 emails
- Onboarding: 5-10 emails
- Re-engagement: 3-5 emails
- Post-purchase: 3-5 emails
- Win-back: 3-4 emails

Depends on:
- Sales cycle length
- Product complexity
- Relationship stage

### Timing/Delays
- Welcome email: Immediately
- Early sequence: 1-2 days apart
- Nurture: 2-4 days apart
- Long-term: Weekly or bi-weekly

Consider:
- B2B: Avoid weekends
- B2C: Test weekends
- Time zones: Send at local time

### Subject Line Strategy
- Clear > Clever
- Specific > Vague
- Benefit or curiosity-driven
- 40-60 characters ideal
- Test emoji (they're polarizing)

**Patterns that work:**
- Question: "Still struggling with X?"
- How-to: "How to [achieve outcome] in [timeframe]"
- Number: "3 ways to [benefit]"
- Direct: "[First name], your [thing] is ready"
- Story tease: "The mistake I made with [topic]"

**Subject line length by context:**
- Mobile-first audiences: 30-45 chars (no truncation on iPhone)
- Desktop-heavy: up to 60 chars
- Gmail Promotions tab: always short — under 40 chars beats the fold

### Preview Text
- Extends the subject line
- ~90-140 characters
- Don't repeat subject line
- Complete the thought or add intrigue
- Example: Subject: "3 ways to cut churn" → Preview: "We tested all three on 50k users. Here's what actually worked."

---

## Sequence Types Overview

### Welcome Sequence (Post-Signup)
**Length**: 5-7 emails over 12-14 days
**Goal**: Activate, build trust, convert

Key emails:
1. Welcome + deliver promised value (immediate)
2. Quick win (day 1-2)
3. Story/Why (day 3-4)
4. Social proof (day 5-6)
5. Overcome objection (day 7-8)
6. Core feature highlight (day 9-11)
7. Conversion (day 12-14)

### Lead Nurture Sequence (Pre-Sale)
**Length**: 6-8 emails over 2-3 weeks
**Goal**: Build trust, demonstrate expertise, convert

Key emails:
1. Deliver lead magnet + intro (immediate)
2. Expand on topic (day 2-3)
3. Problem deep-dive (day 4-5)
4. Solution framework (day 6-8)
5. Case study (day 9-11)
6. Differentiation (day 12-14)
7. Objection handler (day 15-18)
8. Direct offer (day 19-21)

### Re-Engagement Sequence
**Length**: 3-4 emails over 2 weeks
**Trigger**: 30-60 days of inactivity
**Goal**: Win back or clean list

Key emails:
1. Check-in (genuine concern)
2. Value reminder (what's new)
3. Incentive (special offer)
4. Last chance (stay or unsubscribe)

### Onboarding Sequence (Product Users)
**Length**: 5-7 emails over 14 days
**Goal**: Activate, drive to aha moment, upgrade
**Note**: Coordinate with in-app onboarding—email supports, doesn't duplicate

Key emails:
1. Welcome + first step (immediate)
2. Getting started help (day 1)
3. Feature highlight (day 2-3)
4. Success story (day 4-5)
5. Check-in (day 7)
6. Advanced tip (day 10-12)
7. Upgrade/expand (day 14+)

### Post-Purchase Sequence
**Length**: 4-6 emails over 30-45 days
**Trigger**: Completed purchase or subscription activation
**Goal**: Reduce buyer's remorse, drive product adoption, generate referral/review, set up repeat purchase

Key emails:
1. **Order confirmation + what's next** (immediate) — transactional confirmation + single "start here" step
2. **Getting the most out of [Product]** (day 2-3) — top 3 use cases or power moves; reduce abandonment risk
3. **You're not alone — here's the community** (day 7) — link to community, support docs, or customer success; lowers support tickets
4. **Quick win check-in** (day 14) — "Did you try X yet?" with social proof of similar customers
5. **Review request** (day 21-30) — only after they've had time to experience value; conditional on product usage if possible
6. **Expand / refer / repeat** (day 35-45) — upsell, referral program, or next product tier

**Post-purchase timing rules:**
- Never send promotional emails in the first 48h — only confirmations and helpful onboarding
- Review requests before day 14 feel rushed; after day 60 see declining response rates
- If purchase includes physical delivery, delay all emails until after estimated delivery date

### Win-Back Sequence (Lapsed Customers)
**Length**: 3-4 emails over 21 days
**Trigger**: No purchase in 60-180 days (set threshold based on your purchase frequency)
**Goal**: Re-activate lapsed customers or remove from active list

Key emails:
1. **We miss you** (day 0) — acknowledge the gap, no pressure; brief value reminder
2. **Here's what's changed** (day 7) — new features, products, or improvements since they lapsed; give them a reason now is different
3. **Personal offer** (day 14) — discount or exclusive access; time-limited; "just for you" framing over generic promo language
4. **Last reach-out** (day 21) — explicit last email; offer to unsubscribe if not interested; preserves list health and deliverability

**Win-back decision logic:**
- If they open email 1-2 but don't purchase → extend sequence with education email before offer
- If they don't open any email → suppress from future campaigns (dead segment, hurts deliverability)
- If they click but don't purchase → retarget via paid ads (email done its job, hand off to ads)

**For detailed templates**: See [references/sequence-templates.md](references/sequence-templates.md)

---

## Behavioral Branching (Conditional Logic)

For ESP platforms that support conditional sends (Customer.io, Klaviyo, ActiveCampaign, HubSpot), add branching to your sequences:

### High-Value Branch Triggers
| Behavior | Branch Action |
|----------|---------------|
| Opens email 1 but doesn't click | Send email 2 with different CTA angle |
| Clicks but doesn't convert | Send follow-up within 24h with objection-handler |
| Converts at any point | Exit sequence → enter post-purchase |
| No opens for 3 emails | Pause sequence → re-engagement branch |
| Upgrades/purchases | Exit current → enter win/expansion sequence |
| Unsubscribes | Remove from all sequences; tag in CRM |

### Minimum Viable Branching (for simpler ESPs)
If full conditional logic isn't available:
1. Send in timed batch to all
2. After 48h, identify non-openers → resend email with different subject line once
3. After sequence, segment by engagement tier for future campaigns

---

## Segmentation Logic

Before building the sequence, define segments to avoid email fatigue and improve relevance:

| Segment | Definition | Strategy |
|---------|-----------|---------|
| **Hot leads** | Engaged in last 30 days; multiple opens/clicks | Full sequence at normal cadence |
| **Warm leads** | Engaged in last 60 days | Full sequence, slightly longer delays |
| **Cold leads** | Engaged in 60-180 days | Re-engagement first; if no response → remove |
| **Dead leads** | No engagement in 180+ days | Suppress; don't send regular sequences |
| **Buyers** | Have purchased | Skip lead nurture; enter post-purchase or expansion |
| **Power users** | High product engagement | Skip onboarding basics; send advanced sequences |

---

## Diagnosis Protocol (Failing Sequences)

When a sequence is underperforming, run this diagnostic before rebuilding:

### Step 1: Identify where the drop happens

Pull metrics for each email in the sequence:
- Open rate
- Click-to-open rate (CTOR)
- Conversion rate
- Unsubscribe rate

**Drop-off diagnosis table:**

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Low open rate on email 1 | Subject line or from-name; deliverability issue | A/B test subject lines; check spam score |
| Open rate drops after email 2 | Content isn't matching expectation set at signup | Align email 1 → 2 value promise more tightly |
| Good opens, low CTOR | CTA buried; email too long; no clear value to click | Simplify body, move CTA higher, strengthen button copy |
| High CTOR, low conversion | Landing page / offer mismatch | Check page; ensure email → page continuity |
| High unsubscribes on specific email | Content off-topic or felt pushy | Review tone; check if segment fit is off |
| Declining open rate across full sequence | List hygiene issue; sequence too long | Suppress unengaged; cut emails below 25% open rate |

### Step 2: Benchmark against targets

| Sequence Type | Open Rate Target | CTOR Target | Unsub Rate (alert if above) |
|---------------|-----------------|------------|---------------------------|
| Welcome | 45-65% | 15-25% | 0.5% |
| Lead Nurture | 30-50% | 8-15% | 0.3% |
| Onboarding | 40-60% | 12-20% | 0.4% |
| Post-Purchase | 50-70% | 10-18% | 0.2% |
| Re-Engagement | 15-25% | 5-10% | 1-3% (acceptable) |
| Win-Back | 10-20% | 3-8% | 2-5% (acceptable) |

*B2B typically runs 10-15 points lower open rate than B2C for the same sequence type.*

### Step 3: Fix hierarchy

1. **Fix deliverability first** (if open rate < 15% on a warm list, suspect spam folder)
2. **Fix the hook** (subject line + first sentence)
3. **Fix the CTA** (if opens are good but clicks are low)
4. **Fix the offer / landing page** (if clicks are good but conversions are low)
5. **Fix the sequence structure** (if individual emails look fine but sequence as a whole underperforms)

---

## Deliverability Essentials

Poor deliverability kills sequence performance before copy even matters. Check these:

**Source check (2026-06-10):** Deliverability and compliance rules drift. Before giving legal or sender-requirement advice, verify current FTC CAN-SPAM guidance plus Gmail/Yahoo sender requirements and date the check in the output.

### Technical Setup (One-Time)
- [ ] **SPF record** configured for your sending domain
- [ ] **DKIM** signing enabled on your ESP
- [ ] **DMARC** policy set (start with `p=none` for monitoring, move to `p=quarantine` when clean)
- [ ] **Custom sending domain** set up (avoid shared ESP subdomains like `em.mailchimp.com`)
- [ ] **Unsubscribe link** in every email (legally required; also protects reputation)
- [ ] **Physical postal address** in commercial email footer where CAN-SPAM applies; verify local requirements for non-US recipients

### List Health (Ongoing)
- **Hard bounces**: Remove immediately; above 2% triggers ESP warning
- **Soft bounces**: Suppress after 3 consecutive
- **Unsubscribes**: Process within 10 business days under CAN-SPAM; same day is best practice
- **Spam complaints**: Keep Gmail-reported spam rates below 0.10% and avoid ever reaching 0.30% or higher; stricter internal alerts are healthy
- **Engagement hygiene**: Suppress contacts with no engagement in 180 days before they hurt your sender score

### Warm-Up Protocol (New Domains or High-Volume Ramp)
If sending from a new domain or scaling volume significantly:
1. Week 1: Max 50 emails/day — send only to highest-engagement segment
2. Week 2: Max 200/day
3. Week 3: Max 1,000/day
4. Week 4+: Double weekly until full volume
5. Monitor spam complaint rate daily during ramp; pause if above 0.1%

### Spam Signal Checklist (Before Sending)
- [ ] Subject line: No ALL CAPS, excessive punctuation (!!!), or spammy words (FREE, URGENT, GUARANTEED)
- [ ] Body: Image-to-text ratio > 60% text (image-only emails go to spam)
- [ ] Links: No URL shorteners; all links use your domain or trusted CDN
- [ ] Unsubscribe: Clearly visible, one-click, works
- [ ] From name: Consistent; recognizable to subscriber

---

## Email Copy Guidelines

### Structure
1. **Hook**: First line grabs attention
2. **Context**: Why this matters to them
3. **Value**: The useful content
4. **CTA**: What to do next
5. **Sign-off**: Human, warm close

### Inline Copy Templates

**Opening hook patterns (first line):**
- Problem acknowledgment: "Most [role] spend [X time] on [problem] every week. Here's how to cut that in half."
- Contrarian: "Everyone says you need to [common advice]. You don't."
- Story start: "Last [timeframe], one of our customers [specific outcome]."
- Question: "Quick question — have you tried [feature] yet?"
- Personalized: "You signed up [X] days ago. Here's what most people miss at this stage."

**CTA button copy that works:**
- Action + outcome: "Start your free trial" not "Submit"
- First person: "Show me how it works" not "Learn more"
- Specific: "Download the guide" not "Click here"
- Low friction: "See pricing" not "Buy now" (when relationship is early)

### Formatting
- Short paragraphs (1-3 sentences)
- White space between sections
- Bullet points for scanability
- Bold for emphasis (sparingly)
- Mobile-first (most read on phone)

### Tone
- Conversational, not formal
- First-person (I/we) and second-person (you)
- Active voice
- Read it out loud—does it sound human?

### Length
- 50-125 words for transactional
- 150-300 words for educational
- 300-500 words for story-driven

**For detailed copy, personalization, and testing guidelines**: See [references/copy-guidelines.md](references/copy-guidelines.md)

---

## A/B Testing Email Sequences

### What to test and in what order:
1. **Subject line** (highest impact, fastest results) — test after 200+ sends per variant
2. **Send time** (day of week + hour) — test same email same segment, different times
3. **From name** (First name only vs. "Name at Company" vs. company name)
4. **Email 1 body / CTA** — once subject line is optimized
5. **Sequence length** (5-email vs 7-email welcome sequence)
6. **Cadence** (tighter vs. looser delays)

### Testing rules:
- One variable per test
- Minimum 200 recipients per variant before calling a winner
- Wait 72h for results before calling (not 24h — late openers matter)
- Statistical significance: 95% confidence before making permanent change
- Document every test result — losing variants teach as much as winners

---

## ESP Platform Decision Guide

| Your Situation | Recommended ESP |
|---------------|----------------|
| Early-stage SaaS, behavior-based automation | Customer.io |
| E-commerce / Shopify | Klaviyo |
| SMB, simple automation | Mailchimp |
| Developer-built transactional + marketing | Resend |
| Creator / newsletter-first | Kit (formerly ConvertKit) |
| Enterprise CRM-integrated marketing | HubSpot |
| High-volume transactional | SendGrid |

**Migration warning**: Switching ESPs mid-sequence means resetting warm-up and potentially losing behavioral history. Plan carefully.

---

## Output Format

### Sequence Overview
```
Sequence Name: [Name]
Trigger: [What starts the sequence]
Goal: [Primary conversion goal]
Length: [Number of emails]
Timing: [Delay between emails]
Exit Conditions: [When they leave the sequence]
  - Converted (define what conversion means)
  - Unsubscribed
  - Sequence completed without conversion
  - [Any behavioral exit conditions]
Segmentation: [Who enters vs. who is excluded]
```

### Timing Map (visual)
```
Day 0  ──── Email 1: [Name] — [Subject preview]
Day 2  ──── Email 2: [Name] — [Subject preview]
Day 4  ──── Email 3: [Name] — [Subject preview]
Day 7  ──── Email 4: [Name] — [Subject preview]
Day 12 ──── Email 5: [Name] — [Subject preview]
             ↓ if converted at any point → EXIT
             ↓ if no engagement after email 3 → [branch action]
```

### For Each Email
```
Email [#]: [Name/Purpose]
Send: [Timing from trigger]
Subject: [Subject line — 40-60 chars]
Preview: [Preview text — 90-140 chars; don't repeat subject]
Body: [Full copy]
CTA: [Button text] → [Link destination]
Goal of this email: [Single sentence — what does success look like?]
Exit/Branch: [If they do X → Y happens]
```

### Metrics Plan
Track per email:
- Open rate (target by type — see benchmark table above)
- Click-to-open rate (CTOR)
- Conversion rate (if trackable)
- Unsubscribe rate

Track per sequence:
- Sequence completion rate
- Conversion rate (total)
- Revenue attributed (if applicable)

---

## Task-Specific Questions

1. What triggers entry to this sequence?
2. What's the primary goal/conversion action?
3. What do they already know about you?
4. What other emails are they receiving?
5. What's your current email performance? (if optimizing)
6. Which ESP / automation platform are you using?
7. Do you have behavioral data to enable conditional sends?

---

## Tool Integrations

Before recommending implementation tooling, verify the user's current ESP, available connectors, and official platform docs. The older repo-level tools registry is not present in this checkout.

| Tool | Best For |
|------|----------|
| **Customer.io** | Behavior-based automation |
| **Mailchimp** | SMB email marketing |
| **Resend** | Developer-friendly transactional |
| **SendGrid** | Transactional email at scale |
| **Kit** | Creator/newsletter focused |
| **Klaviyo** | E-commerce / Shopify |
| **HubSpot** | CRM-integrated enterprise |

---

## Related Skills

- **churn-prevention**: For cancel flows, save offers, and dunning strategy (email supports this)
- **onboarding-cro**: For in-app onboarding (email supports this)
- **copywriting**: For landing pages emails link to
- **ab-test-setup**: For testing email elements
- **popup-cro**: For email capture popups
- **cold-email**: For outbound prospecting sequences (different from lifecycle/nurture)
- **content-research-writer**: For newsletter content and broadcast emails
