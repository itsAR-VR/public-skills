---
name: gdpr-compliance
description: GDPR-specific entrypoint for EU personal-data work. Use when a task is explicitly framed around GDPR, EU data subjects, lawful basis selection, cross-border transfers, data-subject rights (access/erasure/portability/objection), DPAs with processors, or DPIAs for high-risk processing.
origin: Authored 2026-05-06 as a sibling to hipaa-compliance for the feasibility-tester skill
version: "1.0.0"
---

# GDPR Compliance

Use this when the task touches data of natural persons in the EU/EEA, regardless of where the controller is located. GDPR is extraterritorial — a US SaaS with one paying EU user is in scope.

This skill is intentionally thin. For the broader privacy-engineering layer (RLS, audit trails, leak vectors), pair with `healthcare-phi-compliance` — its patterns generalize to GDPR. For US healthcare, prefer `hipaa-compliance`.

## When to Use

- Building or reviewing software that processes data of EU/EEA natural persons
- Selecting or defending a lawful basis (Art. 6) for a new processing activity
- Designing data-subject-rights workflows (access, rectification, erasure, portability, objection)
- Cross-border transfers to non-adequate countries (especially US, post-Schrems II)
- Sub-processor selection and DPA negotiation
- High-risk processing that may require a Data Protection Impact Assessment

## How It Works

GDPR has six lawful bases. Pick exactly one per processing activity, document it, and prove it would survive a regulator's question.

### The 6 lawful bases (Art. 6)
1. **Consent** — freely given, specific, informed, unambiguous; revocable as easily as it was given. Pre-ticked boxes and "by using this site" don't qualify.
2. **Contract** — necessary to perform a contract the data subject is party to (e.g., shipping the product they bought).
3. **Legal obligation** — required by EU/Member State law (e.g., tax record retention).
4. **Vital interests** — life-or-death (rare in software).
5. **Public task** — government / public-interest tasks.
6. **Legitimate interest** — your interest, balanced against the data subject's rights. Requires a documented Legitimate Interest Assessment (LIA). NOT available to public authorities for their core duties.

For sensitive categories (Art. 9 — health, ethnicity, biometrics, sexual orientation, religion, political opinions, trade-union membership, genetic) you also need an Art. 9 condition (explicit consent, employment law, vital interests in incapacity, etc.).

## GDPR-Specific Guardrails

- **Transparency by construction**: every processing activity needs a public privacy notice (Arts. 13–14) covering purpose, legal basis, retention period, recipient categories, transfer mechanisms, data-subject rights, complaint routes.
- **Cross-border transfers** to non-adequate countries require: Standard Contractual Clauses (post-2021 module set) + a Transfer Impact Assessment, OR an adequacy decision (US status last checked 2026-06-10: EU-US Data Privacy Framework — recipient must be DPF-certified, verifiable at dataprivacyframework.gov), OR Binding Corporate Rules.
- **Data-subject rights** must be operationalized end-to-end. Response window: 1 month (extendable to 3 for complex cases). Erasure must propagate to backups + sub-processors + cached copies.
- **Sub-processor controls**: every processor (including LLM providers, observability vendors, hosting) needs a signed DPA with the controller. Sub-processor list must be public and updated; controllers get notice + objection rights for new sub-processors.
- **DPIA required** when: large-scale special-category processing, systematic monitoring of public spaces, profiling that produces legal effects, automated decisions, large-scale combination of datasets. The processing-activities tracker should flag DPIA candidates by default.
- **Breach notification**: 72 hours to the supervisory authority for breaches likely to result in risk to rights/freedoms; "without undue delay" to data subjects for high-risk breaches. Document everything even if you don't notify.
- **Records of Processing Activities (ROPA)** required (Art. 30) — controllers + processors with 250+ employees, or any processor handling sensitive data, or any non-occasional processing. Write it once; update with every new feature.

## Vendor Blockers (block-by-default until DPA + transfer mechanism confirmed)

- US-based SaaS without DPF certification AND no SCC option (verify at the vendor's Trust Center / DPA portal)
- Free-tier tools that explicitly disclaim DPAs (most "free for personal use" SaaS)
- LLM providers without an EU data residency option AND no SCCs (some still treat the EU as a marketing region, not a residency one)
- Analytics that fingerprint without consent (as of 2026-06-10, 2022-2023 EU supervisory-authority decisions against Google Analytics transfers remain a risk marker; verify current local DPA guidance, transfer mechanism, consent, and minimization settings before use)

## Examples

### Example 1: New feature that profiles EU users

User request: "Add ML-based content recommendations for EU users."

Response pattern: legitimate interest is plausible but requires a documented LIA + opt-out. If recommendations produce legal/significant effects (e.g., job/credit/insurance decisions), Art. 22 likely applies and you need explicit consent + meaningful human review. DPIA required. Transfer mechanism for the recommendation model's hosting must be in place.

### Example 2: Vendor procurement

User request: "Can we use Acme Analytics for product metrics? They're US-based."

Response pattern: block until (a) signed DPA with current SCC modules, (b) DPF certification or sub-processor list with all transfers documented, (c) data-minimization configuration in place (no IP storage, no fingerprinting without consent), (d) deletion-on-request workflow tested.

## Authoritative Sources

Last checked: 2026-06-10. Refresh this section before relying on transfer mechanisms, DPF status, regulator decisions, model/vendor data-residency claims, or jurisdiction-specific guidance.

- **eur-lex.europa.eu/eli/reg/2016/679/oj/eng** — official GDPR text
- **edpb.europa.eu/our-work-tools/general-guidance** — European Data Protection Board guidelines and recommendations
- **commission.europa.eu** — adequacy decisions and European Commission data-protection guidance
- **dataprivacyframework.gov/list** — current US DPF certification verification
- Local supervisory authorities (CNIL, ICO, BfDI, Garante) for jurisdiction-specific guidance

## Related Skills

- `healthcare-phi-compliance` — engineering patterns (RLS, audit, leak vectors) generalize to GDPR
- `hipaa-compliance` — US healthcare overlay; many controls overlap
- `pipeda-compliance` — Canadian counterpart with similar structure
- `security-review` — baseline; GDPR is overlay, not replacement
