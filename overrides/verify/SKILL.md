---
name: verify
description: >
  Post-execution quality gate combining goal-backward verification and
  8-track cleanup into one coherent skill. Absorbs phase-review (verify
  outcomes against plan.md, map evidence to success criteria) and deep-clean
  (dedup, typing, unused code, circular deps, error handling, legacy paths,
  AI artifacts, error handling) with a unified workflow. Adds GSD agents
  gsd-verifier (goal-backward), gsd-doc-verifier (doc accuracy), gsd-ui-auditor
  (UI review), and gsd-security-auditor (security review). Use when: "verify
  this phase", "audit the build", "verify and clean up", "phase verify",
  "post-execution audit", "did we deliver what we promised", "clean up and
  verify". For analysis-only see deep-sweep. For execution see deep-build.
metadata:
  author: contributor
  version: 1.0.0
related_skills:
  - phase-plan
  - deep-sweep
  - deep-build
  - phase-review
  - deep-clean
  - phase-gaps
  - terminus-maximus
---

# Verify

Post-execution quality gate. Runs three layers in sequence:

1. **Goal-backward verification** — did we build what we promised?
2. **Quality audit** — is the code we built correct, safe, and clean?
3. **Documentation verification** — do the docs match reality?

Each layer produces concrete evidence or flags a gap. No subjective "looks good" — every check maps to plan.md requirements, code evidence, or doc accuracy.

## When to Activate

| Signal | Example |
|--------|---------|
| Explicit invocation | "verify this", "audit the build", "/verify" |
| Post-execution gate | "we just finished phase-N, verify it" |
| Pre-PR quality check | "before we ship, let's verify" |
| Milestone audit | "verify this milestone is complete" |
| Deep clean + phase review | "verify and clean up" |

Do NOT activate for:
- Pre-execution planning (use `phase-plan` or `deep-sweep`)
- Mid-execution debugging (use `deep-build` Gear 3-fail)
- A single PR review (use `code-review`)

## Composition

| Layer | Subroutine | Purpose |
|-------|-----------|---------|
| 1. Goal-backward | `$phase-review` + `gsd-verifier` | Verify plan.md requirements delivered |
| 1b. UI check | `gsd-ui-auditor` (UI phases only) | UI/UX review against design system |
| 1c. Security check | `gsd-security-auditor` (sensitive phases) | Security audit on auth/payments/data |
| 2. Quality | `$deep-clean` (8 tracks) | Dedup, typing, unused, cycles, errors, legacy, AI artifacts |
| 3. Docs | `gsd-doc-verifier` | Do docs reflect the shipped code? |

Each layer's output feeds the next. No layer is silently skipped — each is either run or explicitly deferred with reason.

## Adaptive Gate Selection (harness-aware)

Verify runs three layers. Each layer has multiple gates. Check the active harness before running any gate — some are redundant given existing protections.

- **gsd-verifier goal-backward**: always run (no harness overlap)
- **8-track deep-clean**: always run (quality audit is language-specific, not harness-covered)
- **gsd-security-auditor on auth/payments**: always run if security-sensitive files touched
- **doc-verifier**: overlap check for harnesses with native doc-hooks (OpenClaw has `bootstrap-extra-files`)
- **Procedure + overlap map**: `~/.claude/skills/lib/adaptive-gate-selection.md`

**Every gate decision MUST be logged:**

```bash
bash $HOME/.claude/skills/lib/skill-gate-logger.sh \
  --skill verify \
  --gate <gate-name> \
  {--verdict PASS|FAIL|ESCALATE|PARTIAL  OR  --skipped "<why>"} \
  --reason "<one-line reason>"
```

## Procedure

> Detailed procedures in `references/01_PROCEDURE.md`.
> Verification templates in `references/02_TEMPLATES.md`.
> Edge cases in `references/03_EDGE_CASES.md`.

### Phase 0 — Preflight

1. `git status --porcelain` — confirm workspace is clean (or note uncommitted state)
2. `git log --oneline {base-branch}..HEAD` — list commits under verification
3. Identify the governing plan: `docs/planning/phase-{N}/plan.md`
4. If no plan exists: STOP and ask user to identify what's being verified against

### Phase 1 — Goal-Backward Verification

Invoke two reviewers in parallel (independent signals):

```
# 1. Existing phase-review skill (quality gate against plan.md)
Apply $phase-review flow:
- Re-read plan.md root + subphases
- Map each Success Criterion to evidence (commits, tests, artifacts)
- Run quality gates: npm run lint, npm run build (or language equivalent)
- Write post-implementation review doc

# 2. GSD verifier (independent goal-backward check)
Agent(
  name: "gsd-verify",
  subagent_type: "gsd-verifier",
  prompt: <see references/02_TEMPLATES.md §goal-backward>
)
```

**Gate:** Both reviewers must converge on COMPLETE verdict. If they diverge, investigate the gap before proceeding.

**Optional sub-checks (invoke when applicable):**

- UI-heavy phase → `gsd-ui-auditor`
- Auth/payments/data → `gsd-security-auditor`

### Phase 2 — Quality Audit (8 tracks from deep-clean)

Apply `$deep-clean` flow against the phase's diff:

1. **Deduplication** — `jscpd` or language-specific duplicate finder
2. **Shared types** — consolidate type definitions
3. **Unused code** — `knip` / `ts-prune` / `depcheck`
4. **Circular dependencies** — `madge` or language equivalent
5. **Typing** — remove `any`, narrow types, fix generics
6. **Error handling** — remove defensive try/catch without value, add missing error paths
7. **Legacy paths** — remove deprecated fallbacks
8. **AI artifacts** — remove stub comments, TODO markers, hallucinated imports

Apply deep-clean's **pause-and-review gate** between findings and implementation. Only Green-bucket changes proceed automatically; Yellow/Red require approval.

**Gate:** All 8 tracks have a verdict (findings applied, deferred, or explicitly skipped with reason).

### Phase 3 — Documentation Verification

```
Agent(
  name: "doc-verify",
  subagent_type: "gsd-doc-verifier",
  prompt: <see references/02_TEMPLATES.md §doc-verify>
)
```

Checks:
- READMEs reflect the shipped code (not outdated)
- API docs match actual endpoints/signatures
- Inline code comments are not lying (no "this does X" when code does Y)
- Plan.md's Output sections are filled with actual outcomes
- Changelog / release notes exist if shipping externally

### Phase 4 — Synthesis

Write `docs/planning/phase-{N}/verify.md`:

```markdown
# Phase {N} — Verification

## Verdict
{COMPLETE | PARTIAL | FAIL}

## Goal-backward
- Success criteria: X/Y met
- Evidence: {commits, tests, artifacts}
- Gaps: {list}

## Quality
- Tracks run: 8/8
- Findings: {by track}
- Applied: {list}
- Deferred: {list with reason}

## Documentation
- READMEs: {verdict}
- API docs: {verdict}
- Plan.md outputs: {filled Y/N}

## Next steps
{what's unblocked, what needs attention}
```

Present summary to user. Recommend ship / block / revise based on verdict.

## Hard Rules

1. **No "looks good"** — every check has concrete evidence or is a flagged gap.
2. **Don't silently skip layers** — explicit defer with reason, or run.
3. **Goal-backward beats code-forward** — start from what the plan promised, then verify, not "read the code and guess what it does."
4. **Preserve plan.md anchors** — the verbatim original request stays untouched in plan.md.
5. **8-track cleanup has a gate** — don't implement Yellow/Red findings without user approval.
6. **Docs are code** — docs lying about code is a real defect; track it the same way.
7. **Multi-agent awareness** — other phases may have shipped changes. Check git for concurrent work.

## References

**Directory:** `references/`

- `01_PROCEDURE.md` — expanded step-by-step procedure
- `02_TEMPLATES.md` — agent prompts + synthesis templates
- `03_EDGE_CASES.md` — handling partial completeness, out-of-scope findings, etc.

See also:
- `~/.claude/skills/phase-review/references/` — detailed phase-review procedure (still authoritative for the phase-review layer)
- `~/.claude/skills/deep-clean/` — detailed 8-track procedure (still authoritative for quality layer)
- `~/.claude/get-shit-done/references/gates.md` — GSD gate patterns
