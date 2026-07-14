# 02 — Verify Agent Prompts + Synthesis Templates

## §goal-backward — gsd-verifier prompt

```
Verify this phase delivered what plan.md promised. Goal-backward analysis — start from the stated goal, trace forward to evidence.

<plan_md>
{path: docs/planning/phase-{N}/plan.md}
</plan_md>

<commits_in_scope>
{git log --oneline $(git merge-base HEAD main)..HEAD}
</commits_in_scope>

<test_results>
{output of npm test / pytest / go test / etc.}
</test_results>

For every Success Criterion in plan.md:
1. Identify which commit(s) implemented it
2. Identify which test(s) prove it works
3. Rate: MET | NOT MET | PARTIAL | UNTESTABLE

For every requirement not mapped to a commit: flag as a GAP.
For every commit not mapped to a requirement: flag as OUT-OF-SCOPE or record why.

Return:
- Coverage matrix: requirement → commit(s) → test(s) → rating
- Gaps ranked by severity (CRITICAL / HIGH / MEDIUM / LOW)
- Overall verdict: COMPLETE | PARTIAL | FAIL
- If PARTIAL/FAIL: specific revisions needed to reach COMPLETE

Do not speculate. Every claim ties to plan.md text, a commit SHA, or a test name.
```

## §ui-audit — gsd-ui-auditor prompt

```
Audit the UI changes in this phase against the project's design system and user-facing conventions.

<changed_ui_files>
{git diff --name-only $(git merge-base HEAD main)..HEAD | grep -E '\.(tsx|vue|svelte|jsx)$'}
</changed_ui_files>

<design_system>
{path to design system, component library docs, or style guide}
</design_system>

Check:
- Component reuse (new components duplicate existing ones?)
- Spacing/typography tokens (consistent with system?)
- Empty/loading/error states (present for every user-visible surface?)
- Accessibility (semantic HTML, ARIA where needed, keyboard reachability, focus visible)
- Responsive behavior (mobile/tablet/desktop breakpoints)
- i18n readiness (strings externalized or hardcoded?)

Return findings by severity, each with:
- What (specific element / line)
- Why (rule violated / pattern anti-pattern)
- Recommended fix
```

## §security-audit — gsd-security-auditor prompt

```
Security audit of this phase. Focus on OWASP Top 10 + project-specific risks.

<changed_files>
{git diff --name-only $(git merge-base HEAD main)..HEAD}
</changed_files>

<phase_summary>
{plan.md's Purpose + Success Criteria}
</phase_summary>

Check (per OWASP Top 10):
- Broken access control (auth checks present on protected routes?)
- Cryptographic failures (secrets in code? weak algorithms?)
- Injection (SQL, command, LDAP — user input reaching sinks unescaped?)
- Insecure design (rate limiting, input validation boundaries)
- Security misconfiguration (default creds, verbose errors, debug enabled)
- Vulnerable components (new deps audited?)
- Identification/authentication failures (session management, password storage)
- Software/data integrity (supply chain, CI, deploy artifacts)
- Logging/monitoring (auth events, sensitive ops logged?)
- Server-side request forgery (SSRF in URL fetching?)

Plus project-specific:
- PII / PHI handling (if applicable)
- Payment flows (PCI scope awareness)
- Third-party API secrets (rotation, scope minimization)

Return findings by severity (CRITICAL / HIGH / MEDIUM / LOW), each with:
- Vulnerability (what)
- Exploit scenario (how it's abused)
- Remediation (specific fix)
```

## §doc-verify — gsd-doc-verifier prompt

```
Verify documentation accuracy for this phase.

<changed_files>
{git diff --name-only $(git merge-base HEAD main)..HEAD}
</changed_files>

<doc_files>
{list: README.md, docs/, *.md in changed dirs, plan.md Output sections}
</doc_files>

Check:
1. **READMEs** — do they describe what the code now does (not what it used to do)?
2. **API docs** — do documented signatures match actual code?
3. **Inline comments** — do comments tell the truth about the code below them?
4. **Plan.md outputs** — are Output sections filled with actual outcomes (not placeholders)?
5. **Changelog / release notes** — if shipping externally, do they capture user-facing changes?
6. **Migration guides** — if breaking changes, is the migration path documented?

For each doc finding:
- File and line number
- What the doc says vs. what the code does
- Severity (CRITICAL if it misleads users, MEDIUM if confusing, LOW if style)
- Recommended fix

Return: pass/fail per doc type + aggregated finding list.
```

## §synthesis — verify.md template

```markdown
# Phase {N} — Verification

**Date:** {YYYY-MM-DD}
**Scope:** {commit range, branch}
**Verdict:** {COMPLETE | PARTIAL | FAIL}

---

## Layer 1: Goal-Backward Verification

### phase-review verdict
{PASS | PARTIAL | FAIL}

Quality gates:
- lint: {pass|fail, evidence}
- build: {pass|fail, evidence}
- test: {pass|fail, coverage %}

### gsd-verifier verdict
{COMPLETE | PARTIAL | FAIL}

Success Criteria coverage:
| Criterion | Commit(s) | Test(s) | Rating |
|-----------|-----------|---------|--------|
| {text}    | {SHA}     | {test}  | MET    |
| ...       | ...       | ...     | ...    |

Gaps:
- {CRITICAL/HIGH/MEDIUM/LOW}: {description}

### Conditional audits
- UI audit: {ran? verdict?}
- Security audit: {ran? verdict?}

---

## Layer 2: Quality Audit

| Track | Tool | Findings | Applied | Deferred |
|-------|------|----------|---------|----------|
| Dedup | jscpd | N | N | N (reason) |
| Types | manual | N | N | N |
| Unused | knip | N | N | N |
| Cycles | madge | N | N | N |
| Typing | grep+review | N | N | N |
| Errors | grep+review | N | N | N |
| Legacy | grep | N | N | N |
| AI artifacts | grep | N | N | N |

Applied changes: {commit SHAs}
Deferred findings: {list with reason}

---

## Layer 3: Documentation Verification

- READMEs: {PASS | FAIL — what's outdated}
- API docs: {PASS | FAIL — what's wrong}
- Inline comments: {N lying comments found}
- Plan.md outputs: {filled | incomplete}
- Changelog: {updated | not applicable | missing}

---

## Overall Verdict: {COMPLETE | PARTIAL | FAIL}

### Ready to ship?
{yes | yes-with-caveats | no}

### If PARTIAL/FAIL — what's needed

- [ ] {specific action}
- [ ] {specific action}

### Risk register (if shipping with caveats)
- {risk} — {mitigation / monitoring plan}

---

## Evidence Index

- Plan: `docs/planning/phase-{N}/plan.md`
- Review: `docs/planning/phase-{N}/review.md` (phase-review output)
- Verification: `docs/planning/phase-{N}/verify.md` (this doc)
- Commits: {SHA range}
- Tests: {test run output paths}
```

## Related

- `01_PROCEDURE.md` — step-by-step procedure
- `03_EDGE_CASES.md` — handling partial completion, out-of-scope findings
