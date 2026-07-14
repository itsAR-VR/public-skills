---
name: ferpa-compliance
description: FERPA-specific entrypoint for US student-records work. Use when a task involves K-12 or higher-education records, school-vendor data agreements, the school-official-with-legitimate-educational-interest exception, directory information, or EdTech operating in US schools.
origin: Authored 2026-05-06 as a sibling to hipaa-compliance for the feasibility-tester skill
version: "1.0.0"
---

# FERPA Compliance

FERPA (Family Educational Rights and Privacy Act) protects "education records" held by educational agencies/institutions that receive federal funding. It gives parents (or eligible students 18+) rights to access, amend, and consent to disclosure.

For software vendors, the operating mode is the **school-official-with-legitimate-educational-interest** exception — schools can disclose records to vendors performing services the school would otherwise perform, provided the contract gives the school direct control.

## When to Use

- Building or selling software to K-12 schools, districts, colleges, universities
- Negotiating a Data Privacy Agreement (DPA) with a school district
- Designing student-facing or teacher-facing systems where grades, attendance, IEPs, transcripts flow
- Discovering existing systems handle student records without explicit FERPA consideration

## How It Works

### Education record (what's protected)

Records, files, documents, and other materials that:
- Contain information directly related to a student
- Are maintained by an educational agency/institution or a person acting for it

Includes: grades, transcripts, disciplinary records, IEPs, attendance, financial aid, student-ID systems, LMS activity, behavioral logs, photos taken in school context, recordings of class sessions where students are identifiable.

Excludes: a few narrow categories — sole-possession records of teachers, law-enforcement records of school police kept separately, employment records of student employees, treatment records of post-18 students used only by the treating professional.

### Directory information (different rules)

Schools may designate certain info as "directory" — name, address, phone, email, photo, dates of attendance, degree, honors, sports participation. Schools must give annual notice + opt-out window. After that, directory info can be disclosed without consent.

But: directory information from the school doesn't transfer to vendors automatically. The vendor's contract still controls.

### The school-official-with-legitimate-educational-interest exception

When a school authorizes a vendor to access student records to perform a function the school would otherwise perform, the vendor is treated as a "school official" — IF four conditions hold:

1. The vendor performs an institutional service or function the school would otherwise use employees for
2. Under direct control of the school with respect to use and maintenance of education records
3. Subject to FERPA's use-and-redisclosure rules — the vendor cannot share, sell, or use records for purposes outside the school's scope
4. The school remains responsible for FERPA compliance — joint liability

This is the standard EdTech operating mode. The contract is where compliance lives.

## FERPA-Specific Guardrails

- **Direct control means direct control.** The school must be able to instruct deletion, audit access, terminate the engagement and pull data back, and dictate what the vendor uses the data for. "Vendor decides retention" or "vendor uses data for product improvement" both fail this test.
- **No marketing, no behavioral advertising, no profile-building** outside the school-designated purpose. Many EdTech vendors quietly do all three; FERPA + state laws make it actionable.
- **Use only for the school-designated purpose.** A grading vendor cannot pivot to college-recruitment lead generation using the same data. Different purpose = different consent regime.
- **Re-disclosure restrictions follow the data.** Sub-processors must commit to the same restrictions; school's annual notice obligations include sub-processor disclosure.
- **Data export + deletion on demand.** Schools must be able to take their data back; vendor must delete on contract termination + demonstrate deletion.
- **Annual training** for vendor employees with access to records — many DPAs require this.
- **Audit logs** of who accessed what student record and when. School auditors want this; some DPAs require live access.
- **Data minimization for AI features.** If you're feeding records to an LLM (summarization, recommendations, tutoring), the LLM provider becomes a sub-processor with same restrictions. Before naming a provider as FERPA-fit, check current provider docs and get the DPA/no-training/retention terms in writing; default or free-tier configs are usually wrong.

## State law layering

State EdTech privacy laws stack on top of FERPA. Common patterns:

- **California AB 1584 / SOPIPA** — bans behavioral profiling and ad targeting; mandates encryption + breach notification
- **New York Education Law 2-d** — requires districts to publish parents'-bill-of-rights covering each vendor; vendor must sign + attach
- **Illinois SOPPA** — vendor must publish DPA + enable parent review of data; restrictive on subcontractors
- **Connecticut, Colorado, Texas** — similar patterns; check the district's DPA, which usually layers in state requirements

Districts often use shared DPA templates (e.g., the Student Data Privacy Consortium's National DPA) — adopting these ahead of procurement saves negotiation cycles.

## Vendor Blockers

Block by default any sub-processor that won't sign a FERPA-compliant DPA:
- Most free-tier analytics
- Most ad networks
- LLM providers without enterprise-tier data agreements
- Email/marketing tools that retain data for product improvement

Replace with school-DPA-friendly alternatives or self-host the equivalent.

## Examples

### Example 1: New gradebook product

User request: "Building a gradebook for K-12 teachers."

Response pattern: FERPA + state laws apply. Sign National DPA + state addenda. No behavioral analytics, no third-party trackers, no data-driven product recommendations. LMS integration via OneRoster + Clever (designed FERPA-fit). Encrypt at rest with managed keys. Audit log per record access. Retention bounded by school year + grace period.

### Example 2: AI tutoring add-on

User request: "Adding ChatGPT-based tutoring to existing platform."

Response pattern: hardest case. Sending student work + context to a general LLM = sub-processor. Need: enterprise-tier LLM with no-training-on-data + bounded retention or zero-retention where required + signed DPA. Verify current provider terms in writing before treating any Anthropic, OpenAI, or other LLM tier as FERPA-fit. Default config almost always wrong.

### Example 3: Existing product picking up school customers

User request: "Schools are buying our consumer product. Are we FERPA-fit?"

Response pattern: probably not by default. Audit data flows + retention + sub-processors. Most consumer products use behavioral analytics + ad-network integrations that are non-starters for school DPAs. Build a school-edition with the offending paths gated off, sign the National DPA template, then sell.

## Authoritative Sources

- Source check last run: 2026-06-10. Refresh before relying on vendor-specific AI claims, state-law requirements, or DPA template status.
- **studentprivacy.ed.gov** — US Department of Education's Student Privacy Policy Office; canonical FERPA guidance
- **34 CFR Part 99** — FERPA regulations
- **National DPA** — studentprivacycompass.org/national-dpa — widely-adopted template
- **State EdTech laws** — varies; districts publish their requirements

## Related Skills

- `coppa-compliance` — companion for under-13 student data (often required together for K-6)
- `gdpr-compliance` — for international student records (EU schools, international branches)
- `security-review` — baseline; FERPA is overlay
