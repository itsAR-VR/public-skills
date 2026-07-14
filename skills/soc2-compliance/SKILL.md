---
name: soc2-compliance
description: SOC 2 audit-attestation entrypoint. Use when a task is framed around SOC 2 readiness, Type 1 vs Type 2 selection, Trust Services Criteria scoping, vendor SOC 2 review, audit prep, or enterprise procurement gates that demand a current SOC 2 report.
origin: Authored 2026-05-06 as a sibling to hipaa-compliance for the feasibility-tester skill
version: "1.0.0"
---

# SOC 2 Compliance

SOC 2 is not a law — it's an attestation by a licensed CPA firm that an organization meets the AICPA Trust Services Criteria. Buyers (especially enterprise B2B) treat a current SOC 2 report as a procurement gate. The auditor decides scope; you choose which Trust Services Criteria to include.

This skill is for understanding what auditors actually look for, how long preparation takes, and when to push back on enterprise buyers who demand SOC 2 before product-market fit.

## When to Use

- An enterprise buyer is blocking purchase pending SOC 2
- Choosing between Type 1 (point-in-time) and Type 2 (period-of-time) attestation
- Scoping which Trust Services Criteria to include
- Vendor security review where SOC 2 evidence is being requested
- Architecting a system from day one to be SOC-2-ready

## Type 1 vs Type 2

| | Type 1 | Type 2 |
|---|---|---|
| What it attests | Controls are designed appropriately as of a single date | Controls operated effectively over a period (typically 6–12 months) |
| Time to first report | 4–8 weeks | 9–15 months (3-month design + 6–12 month observation) |
| Buyer credibility | Light — most enterprise buyers treat Type 1 as a starting gun | Heavy — Type 2 is what most procurement teams actually want |
| Use case | Cheap signal that "we exist as a security-aware org" | The real attestation; renewable annually |

**Pattern**: ship Type 1 within 3 months when a deal is on the line; commit to Type 2 within the year. Don't try to skip directly to Type 2 — the observation period requires evidence you can only generate by running the program.

## The 5 Trust Services Criteria (TSC)

| Criterion | Always required? | What it covers |
|---|---|---|
| **Security** | YES — mandatory | Logical/physical access, intrusion detection, change management, vendor management, incident response |
| **Availability** | optional | Uptime SLAs, disaster recovery, capacity management, backup/restore |
| **Processing Integrity** | optional | Data is processed completely, accurately, timely; especially relevant for fintech/billing |
| **Confidentiality** | optional | Information designated confidential is protected — different from privacy; e.g., trade secrets, customer data classified as confidential |
| **Privacy** | optional | Personal data handled per GAPP (Generally Accepted Privacy Principles) — overlaps with GDPR/CCPA but distinct |

**Default scope**: Security only. Add Availability if you sell uptime SLAs. Add Confidentiality if customers send you commercially sensitive data. Add Processing Integrity for billing/financial systems. Add Privacy only if you specifically commit to it — privacy criteria are stringent and overlap with regulatory frameworks (handle those separately first).

## SOC 2-Specific Guardrails

- **Pick a small scope and ship.** Most first-time SOC 2 reports cover one production environment, one app, one Security TSC. Don't try to attest your entire org on the first attempt.
- **Vendor management is the section that fails most.** You need a documented vendor inventory + SOC 2 reports for critical vendors + risk assessment. Auditors will ask for sub-processor lists and BAAs/DPAs.
- **Change management beats heroics.** Auditors want evidence that every production change went through a documented approval workflow. Git PR reviews + linked tickets are usually sufficient; ad-hoc deploys are flagged.
- **Access reviews are quarterly minimum.** Document who has admin access to what, who reviewed it, when, and what was changed.
- **Incident response must be documented and tested.** Tabletop exercises annually; post-incident retros for real incidents.
- **Logical access has MFA + SSO + role-based access controls.** Auditors look for shared accounts, missing MFA, terminated employees with active access.
- **Background checks** for employees with production access. Onboarding/offboarding checklists with security tasks.

## What auditors actually look for

The 80/20 of SOC 2 audit findings:
1. Missing or stale access reviews
2. Vendor management gaps (no SOC 2 reports collected from vendors, no risk assessment)
3. Change-management evidence missing for some deploys
4. Onboarding/offboarding not consistently followed
5. Penetration testing not performed in the audit period (usually annual minimum for Type 2)
6. Backup/restore testing not documented (if Availability TSC included)
7. Encryption at rest with managed keys not documented end to end

Vibes-based "we have good security" doesn't pass. Document everything; the report is essentially a paper trail validation.

## Vendor SOC 2 Review (when a buyer demands yours)

Be skeptical of vendor SOC 2 reports:
- Check the **observation period** matches what's claimed (often expired)
- Check the **scope** — many vendors attest only their corporate network, not the actual SaaS product the buyer cares about
- Read the **exceptions** section — auditors flag failures here; many vendors hide real issues in long-form prose
- Confirm the **CPA firm** is reputable (Big 4 / second-tier / niche firm — pricing differs but so does rigor)

## Examples

### Example 1: Procurement gate from a Fortune 500

User request: "Buyer says they need SOC 2 by end of quarter."

Response pattern: scope to Security TSC only, target Type 1 within 8 weeks. Negotiate the contract to allow Type 1 at signing with a Type 2 commitment within 12 months. Don't try to ship Type 2 in 8 weeks — auditors won't sign.

### Example 2: Architecting day one

User request: "We're starting fresh; how do we build SOC-2-ready?"

Response pattern: GitHub PR review + branch protection + linked tickets gives change management. Okta/Google Workspace SSO + MFA gives logical access. AWS/GCP audit logs + a SIEM (Datadog Cloud SIEM, Panther, Vanta-managed) gives monitoring. Vanta / Drata / Secureframe automate evidence collection — most first-time SOC 2 orgs use one of these.

## Authoritative Sources

- **aicpa.org/topic/audit-assurance/audit-and-assurance-greater-than-soc-2** — TSC, audit guides
- **AICPA Trust Services Criteria** (AT-C 105/205) — the standard auditors apply
- The auditor's engagement letter — your binding contract for what gets attested

## Related Skills

- `security-review` — baseline controls SOC 2 audits map onto
- `gdpr-compliance` — overlaps when Privacy TSC is in scope
- `hipaa-compliance` — overlaps for healthcare orgs (often pursued together)
- `security-bounty-hunter` — pen-test findings feed into the audit's Vulnerability Management section
