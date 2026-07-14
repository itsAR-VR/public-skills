---
name: coppa-compliance
description: COPPA-specific entrypoint for products directed at children under 13 in the US. Use when the audience is under-13 children, when "actual knowledge" of under-13 users exists, when designing verifiable parental consent (VPC) flows, or when scoping data minimization for kids' platforms.
origin: Authored 2026-05-06 as a sibling to hipaa-compliance for the feasibility-tester skill
version: "1.0.0"
---

# COPPA Compliance

COPPA (Children's Online Privacy Protection Act) is enforced by the FTC and applies to operators of websites/online services **directed at children under 13** OR with **actual knowledge** that they're collecting personal info from children under 13.

Before collecting any personal info from a covered child, **verifiable parental consent (VPC)** is required. "Click yes if you're a parent" does NOT qualify.

## When to Use

- Building consumer products with under-13 audiences (kids' games, kids' streaming, K-6 learning apps)
- Discovering an existing service has under-13 users despite age-gating
- Designing parental dashboards, age gates, or VPC flows
- Education vendors operating under the school exception
- COPPA-adjacent products for ages 13–17 that need to consider state laws (California's Age-Appropriate Design Code, NY SHIELD)

## How It Works

### Trigger conditions (either is sufficient)

1. **Directed-to-children**: site/service is directed at children under 13. The FTC weighs subject matter, visual content, language, character/animation use, advertised age range, evidence of actual audience.
2. **Actual knowledge**: operator obtains actual knowledge that a particular user is under 13 (e.g., they self-report age in a profile field).

If either triggers, COPPA applies to the under-13 user's data.

### Personal info under COPPA (broader than most laws)

- First/last name, address, online contact (email, IM, screen name that contains identifying info)
- Telephone, SSN
- Persistent identifier (cookie, device ID, IP, customer number) **even when used alone for behavioral advertising**
- Photo, video, audio of the child (especially face/voice)
- Geolocation precise enough to identify a street/city
- Any info concerning the child + any of the above

### The 5-step VPC requirement

1. **Pre-collection notice** to the parent of what you'll collect, how you'll use it, third-party sharing, parent's rights
2. **Get verifiable parental consent** before any collection
3. **Right to review** — parent can see all info collected from their child on demand
4. **Right to delete** — parent can demand deletion of all of the child's info
5. **Right to refuse further collection** — parent can revoke consent

### Acceptable VPC methods (FTC source check: 2026-06-10)

- **Signed consent form** returned via mail, fax, or scan
- **Government-issued ID** check (collect, verify, then delete the ID)
- **Knowledge-based authentication** (KBA) — credit-bureau-style questions
- **Video conference** verification with parent + their ID
- **Toll-free phone call** staffed by trained personnel
- **Credit card / debit card / online payment** that notifies the account holder of each discrete transaction
- **Email-plus** — email confirmation followed by a second action (call, second email, mail) when the operator does not disclose children's personal info
- **Text-plus** — text confirmation plus a second assurance step, also limited to no-disclosure use cases
- **Face match** to verified photo ID (FTC-approved in 2015 and codified in the 2025 COPPA Rule amendments)

What does NOT qualify: pre-checked boxes, "click here if you're a parent," parent's email alone, age-gate-then-pretend.
Refresh this list against FTC COPPA FAQ + 16 CFR 312.5 before relying on it for production VPC design; FTC finalized COPPA Rule amendments in 2025 and operators had until 2026-04-22 to comply.

## COPPA-Specific Guardrails

- **Data minimization is mandatory**, not aspirational. Collect only what's necessary for the activity the child wants to participate in.
- **Behavioral advertising to under-13s without VPC is forbidden.** Even your own first-party retargeting requires VPC.
- **Persistent identifiers used solely for internal operations** (security, fraud, contextual ads, network communications) are exempt — but the moment you cross into behavioral profiling, VPC kicks in.
- **Parental dashboard** must work end-to-end: review, delete, revoke. Test it; auditors / FTC investigators will.
- **Retention only as long as necessary**, then secure deletion. Document the retention schedule.
- **Third parties**: COPPA liability is joint — if you share with an analytics provider, ad network, etc., you remain on the hook. Vendor must commit to COPPA-compliant handling. Most don't by default.

## The school exception

When a school authorizes the operator to collect personal info from students for an educational purpose, the school can provide consent on behalf of parents — IF the use is limited to the educational context.

Contractual provisions required:
- The vendor uses data only for the school-designated educational purpose
- No marketing, behavioral advertising, or profile-building outside the educational use
- School retains direct control + can delete on demand
- Vendor uses same protections that the school would

This is the typical EdTech operating model. See also `ferpa-compliance`.

## Vendor Blockers

Block by default any SaaS for under-13 contexts unless:
- Vendor has explicit COPPA-compliant DPA
- Sub-processor list discloses every third party touching child data
- Default analytics turned off (Google Analytics for kids, Facebook Pixel — both blocked unless special configuration)

## Examples

### Example 1: New kids' app

User request: "Building a math game for 8-year-olds with leaderboards."

Response pattern: COPPA applies. Leaderboard with username + score is fine if username can't identify the child. Add VPC flow before any account creation. No third-party analytics by default — use first-party server-side metrics. No behavioral ads. Parental dashboard for review/delete.

### Example 2: Existing service discovers under-13 users

User request: "Our analytics shows 8% of users are under 13 despite the 13+ gate."

Response pattern: this triggers "actual knowledge." Either tighten the age gate (and delete known under-13 user data) OR build COPPA compliance for that segment. The middle ground (knowing they're there but not acting) is the highest-risk legal position.

### Example 3: EdTech under the school exception

User request: "K-6 reading app sold to school districts."

Response pattern: school exception applies. Need a districts-friendly DPA template + COPPA-clean configuration. Default opt-out of analytics + behavioral profiling. Parent dashboard still required (some districts demand it; others do it through their LMS).

## Authoritative Sources

- **ftc.gov/business-guidance/privacy-security/childrens-online-privacy-protection-rule-coppa** — FTC's COPPA Rule + FAQ
- **ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa** — full rule text (16 CFR Part 312)
- **State laws**: CA AADC (Age-Appropriate Design Code), NY SHIELD, IL kid privacy bills — additional requirements layered on COPPA

## Related Skills

- `ferpa-compliance` — companion for school-context EdTech
- `gdpr-compliance` — EU equivalent (GDPR-K + national age-of-consent rules, varies 13–16)
- `security-review` — baseline; COPPA is overlay
