---
name: pci-dss-compliance
description: PCI DSS-specific entrypoint for systems that touch, transmit, process, or store cardholder data. Use when a task involves credit cards, PANs, CVV/CVC, payment processing, tokenization decisions, scope reduction, or SAQ/AOC selection. Mandatory after 2025-03-31 — current standard is PCI DSS v4.0.1.
origin: Authored 2026-05-06 as a sibling to hipaa-compliance for the feasibility-tester skill
version: "1.0.0"
---

# PCI DSS Compliance

Use this when the system handles cardholder data — Primary Account Number (PAN), full magnetic-stripe / chip data, or sensitive authentication data (CVV/CVC, full track, PIN). PCI DSS is a contractual standard imposed by card networks (Visa, Mastercard, Amex, Discover, JCB), enforced by acquirers — not a law, but breach of it ends merchant agreements.

The single most important PCI control is **scope reduction**: keep raw cardholder data out of your servers, networks, and logs by design.

## When to Use

- Building checkout, billing, subscription, or any flow involving card numbers
- Selecting between Stripe Elements / Adyen Drop-in / Braintree Hosted Fields vs. raw API
- Acquirer asks for an SAQ + AOC; need to choose the level
- Architecting card-handling systems with network segmentation, key management, log retention
- Vendor procurement when a SaaS will touch cardholder data

## How It Works

### Step 1 — Determine scope (the most important step)

Anything that **stores, processes, or transmits** cardholder data is in scope. Plus anything **connected to** the cardholder data environment (CDE) — same VLAN, shared admin tools, shared identity store, etc. Auditors look at lateral movement; "we don't store cards" doesn't help if your support tooling can pull them from the processor on demand.

The **Cardholder Data Environment** is the smallest set of systems where PAN can be present. Push it as small as possible. Tokenization is the lever.

### Step 2 — Pick the right SAQ (Self-Assessment Questionnaire)

| SAQ | When it applies | Complexity |
|---|---|---|
| **A** | E-commerce merchants where 100% of card processing is fully outsourced (hosted iframe, redirect-to-processor) | Lowest — shortest SAQ |
| **A-EP** | Hosted iframe but some part of the page is yours; risk of injection on your domain | Medium |
| **B / B-IP** | Imprint-only or standalone payment terminals (rare in software) | Low |
| **C / C-VT** | Payment app + virtual terminal | Medium |
| **D** | Everything else — including merchants that touch raw PAN at any point | Highest — full PCI DSS assessment surface; typically requires QSA assessment |

**Goal: get to SAQ A.** If you can architect so PAN never hits your servers (Stripe Elements, Adyen Drop-in, Braintree Hosted Fields, redirect-to-Checkout flows), you're SAQ A. Every byte of PAN in your system pushes you toward SAQ D and a QSA audit.

## PCI-Specific Guardrails

- **Never store CVV/CVC/full magnetic-stripe data after authorization.** Full stop. No exceptions, no scope-reduction route. PCI DSS v4.0.1 Req. 3.3 / 3.3.1.
- **PAN at rest must be unreadable** (strong cryptography with managed keys, truncation showing only first 6 + last 4, hashing, or tokenization). PCI DSS Req. 3.5.
- **PAN in transit must use TLS 1.2 or higher** with current cipher suites. SSL and early TLS are non-compliant.
- **Network segmentation**: the CDE must be isolated from non-CDE networks. Audit your firewall rules + egress; "anything connected to CDE is in CDE" — penalty for sloppy segmentation is dragging your whole org into SAQ D.
- **Access control by role + least privilege.** Multi-factor authentication for all CDE access. Quarterly access review.
- **Logging**: log all access to cardholder data + all admin actions in CDE. Retain ≥1 year, with ≥3 months immediately accessible. Centralized + tamper-evident.
- **Quarterly external vulnerability scans by an Approved Scanning Vendor (ASV)** for systems connected to the internet. Annual penetration testing for SAQ D / Level 1 merchants.
- **Inventory + classify cardholder data flows** annually. Most merchants have undocumented flows; a flow is the auditor's first question.

## Vendor Blockers

Block by default any SaaS that would touch PAN unless:
- It's a PCI Level 1 service provider (verify on the AOC list at visa.com / mastercard.com / pcisecuritystandards.org)
- It has a current AOC (Attestation of Compliance) on file with appropriate scope
- The integration uses tokenization or hosted fields, NOT raw PAN forwarding

Even with a compliant vendor, the **shared responsibility matrix** matters. Your AOC documents which controls the vendor handles vs. which you handle. Don't assume.

## Examples

### Example 1: New checkout build

User request: "We need to add card payments to our app."

Response pattern: route through Stripe Elements (or Adyen Drop-in / Braintree Hosted Fields) so card data never hits your origin. Confirms SAQ A scope. Validate that the iframe loads from a PCI-compliant payment domain, not your own. Ensure no logging of PAN-containing payloads anywhere upstream of the processor.

### Example 2: Subscription billing with retries

User request: "Tokenize the card for recurring charges."

Response pattern: use the processor's vault (Stripe Customer + PaymentMethod, Adyen Recurring, Braintree Vault) — never store the token + full card details together. The token alone is fine to store; pairing it with last4/expiry is fine; pairing with full PAN is forbidden.

### Example 3: Audit failure

User request: "Our acquirer is pushing for SAQ D — we just send tokens."

Response pattern: before accepting SAQ D, audit the actual data flow. If anywhere — server logs, Sentry events, an admin panel, a customer-service tool — could see raw PAN even briefly, you're in SAQ D. Otherwise push back with the data-flow diagram + AOC of the processor + the fact that PAN never traverses your servers.

## Authoritative Sources

- Source check (2026-06-10): PCI SSC Document Library lists PCI DSS v4.0.1 as the active PCI DSS standard; refresh this skill if the Document Library changes the current PCI DSS version, SAQ set, or transition dates.
- **pcisecuritystandards.org/document_library** — PCI DSS v4.0.1, SAQs, AOCs, ASV list
- Acquirer compliance team (your direct line) — they decide your level + accept your AOC
- **visa.com/cisp** + **mastercard.com/sdp** — card-network supplemental requirements

## Related Skills

- `security-review` — baseline; PCI is overlay
- `security-bounty-hunter` — adversarial framing for "where would a card thief look"
- `gdpr-compliance` — overlapping coverage if EU cardholders involved
- `soc2-compliance` — often demanded together by enterprise buyers
