---
name: pipeda-compliance
description: PIPEDA-specific entrypoint for Canadian personal-information work. Use when a task involves Canadian data subjects, the Office of the Privacy Commissioner of Canada (OPC), the 10 Fair Information Principles, Quebec Law 25 specifics, or cross-border data flows involving Canadian persons.
origin: Authored 2026-05-06 as a sibling to hipaa-compliance for the feasibility-tester skill
version: "1.0.0"
---

# PIPEDA Compliance

PIPEDA (Personal Information Protection and Electronic Documents Act) is Canada's federal private-sector privacy law. It applies to commercial activities involving personal information of Canadians.

Quebec, Alberta, and BC have substantially similar provincial laws. **Quebec's Law 25 is materially stricter** — if you have Quebec users, plan for it specifically. As of the 2026-06-10 source check, Bill C-27/CPPA had not replaced PIPEDA; verify the current Parliament tracker before treating any federal replacement as active law.

## When to Use

- Operating commercial services that touch Canadian users' personal information
- Quebec-specific requirements (PIA mandate, breach notification, Privacy Officer designation)
- Cross-border transfers from Canada to non-adequate countries
- Vendor procurement with Canadian data subjects involved
- Designing consent flows for products entering Canadian markets

## How It Works

### The 10 Fair Information Principles (Schedule 1 of PIPEDA)

PIPEDA codifies these as obligations. Violations are enforceable.

1. **Accountability** — designate someone to oversee compliance; this person must be reachable to OPC
2. **Identifying purposes** — state purposes before or at collection
3. **Consent** — knowledge + meaningful consent; cannot be condition of service unless necessary
4. **Limiting collection** — only what's necessary for stated purposes
5. **Limiting use, disclosure, retention** — only for purposes consented to; retention only as needed
6. **Accuracy** — keep info accurate, complete, current
7. **Safeguards** — physical, organizational, technological controls proportional to sensitivity
8. **Openness** — make policies + practices readily available
9. **Individual access** — data subject can access + correct their info
10. **Challenging compliance** — provide accessible complaint mechanism

### Consent

PIPEDA recognizes a sliding scale: explicit consent for sensitive data, implied consent for less-sensitive data with reasonable expectations of use. The OPC's 2018 guidance is strict — "reasonable expectations" doesn't cover surveillance, profiling, or third-party sharing without explicit consent.

For minors, the OPC's current position is that children under 13 generally cannot provide meaningful consent; consent should come from a parent or guardian. Provincial rules vary, so refresh the source check before making age-threshold advice jurisdiction-specific.

## Quebec Law 25 specifics (the strictest layer)

If you have Quebec users, all of the following kick in:

- **Privacy Officer required** by name + title, contact published, accountable to la Commission d'accès à l'information (CAI)
- **Privacy Impact Assessment (PIA)** required for any project that involves personal info — done before launch, documented, available on request
- **Breach notification** required "without delay" — narrower than PIPEDA's "without unreasonable delay"
- **Cross-border transfer assessments** required before any transfer outside Quebec; must evaluate the destination's privacy regime + ensure equivalent protection
- **Right to data portability** in machine-readable format
- **Automated decision-making** notice + right to ask for human review
- **Retention policy** must be written + published; auto-deletion when purpose is fulfilled
- **Default privacy settings** must be the most protective

Law 25 authorizes significant administrative monetary penalties and penal fines; verify current CAI enforcement history before quoting a specific fine amount.

## Cross-border data flow

PIPEDA does not require data localization, but the **accountability principle** says you remain responsible when you transfer data to a third party (including in another country). The OPC's 2009 guidelines + 2019 enforcement actions establish:

- Notify users in your privacy policy about cross-border transfers + that data may be subject to foreign legal access
- Ensure contractual safeguards with the foreign processor (DPA equivalent)
- Conduct an impact assessment for sensitive transfers

Quebec Law 25 makes the assessment **mandatory + documented**, not merely recommended.

## Breach notification

PIPEDA's mandatory breach reporting (since 2018):
- Report to OPC any breach causing real risk of significant harm
- Notify affected individuals
- Maintain a record of all breaches (regardless of severity) for 24 months
- Quebec: notify CAI + affected individuals "without delay"

## PIPEDA-Specific Guardrails

- **Privacy policy + Privacy Officer + complaints process** are the trio every Canadian-facing service needs visible from day one. OPC complaints almost always cite the absence of one of these.
- **Consent must be meaningful**, which means collected separately from "I agree to terms." A combined ToS+privacy "I agree" is OPC-flagged.
- **Retention schedule** in writing, applied automatically, audited. Indefinite retention is non-compliant.
- **Third-party tracking** without consent is OPC-actionable. Default Google Analytics + behavioral pixels need explicit consent + opt-out.
- **Right of access** must be operationalized — 30-day response window; format must be accessible.
- For **Quebec users specifically**: name a Privacy Officer + complete + publish PIA + automate breach detection + default to maximum privacy.

## Vendor Blockers

Block by default any sub-processor without:
- Signed DPA committing to PIPEDA-equivalent safeguards
- For Quebec users: documented assessment of vendor's jurisdiction adequacy
- For sensitive data: explicit handling commitments (e.g., no training on data for LLM vendors)

## Examples

### Example 1: SaaS expanding to Canadian customers

User request: "We have US customers; now signing a Toronto-based enterprise."

Response pattern: PIPEDA applies for the Canadian customer's users. If any of those users are in Quebec, Law 25 layers in. Need: privacy policy in English + French (Quebec); Privacy Officer designated; cross-border-flow disclosure; breach plan; subject-access workflow tested. If sensitive data → PIA required for Quebec users.

### Example 2: New analytics integration

User request: "Adding Mixpanel for product analytics. Have Quebec users."

Response pattern: requires explicit consent (cookie banner + meaningful opt-in), DPA with Mixpanel, transfer assessment (US-based processor), Privacy Officer review. Default-on tracking is non-compliant in Quebec.

### Example 3: Existing service discovering CAI complaint

User request: "Got a CAI complaint about our consent flow."

Response pattern: respond within the deadline (varies by complaint type), document the consent design, fix the immediate issue, reassess Privacy Officer accountability + complaints process, file an updated PIA if processing scope changed. CAI tends to look favorably on swift remediation; sluggish responses escalate.

## Authoritative Sources

- Source check last refreshed: 2026-06-10. Refresh before relying on Bill C-27/CPPA status, Quebec Law 25 penalties/enforcement, children's consent thresholds, or breach-report timing.
- **priv.gc.ca** — Office of the Privacy Commissioner of Canada (OPC); guidance + enforcement findings
- **cai.gouv.qc.ca** — Commission d'accès à l'information du Québec; Law 25 guidance
- **legisquebec.gouv.qc.ca** — current text of Quebec's private-sector privacy statute as amended by Law 25
- **PIPEDA Schedule 1** — full text of the 10 Principles
- **Bill C-27 / CPPA tracker** — for federal privacy-reform status before treating CPPA as active law

## Related Skills

- `gdpr-compliance` — structurally similar; many controls overlap
- `coppa-compliance` — companion for under-13 Canadian users (PIPEDA defers to provincial age limits)
- `security-review` — baseline; PIPEDA is overlay
