---
name: five-whys
description: "Root-cause drilling on a single observed symptom. Iteratively ask 'why' until reaching the underlying systemic cause that, if fixed, prevents recurrence — not just the proximate cause that, if fixed, fixes only this instance."
origin: "Sakichi Toyoda / Toyota Production System — adapted by Taiichi Ohno"
related_skills:
  - post-mortem
  - after-action-review
  - ecc-blueprint
---

# Five-Whys

Five-whys drills from a symptom to the root cause by iteratively asking "why" until reaching a cause that, if removed, prevents the symptom from recurring. The "five" is approximate — it usually takes 4-7 iterations. The discipline is *stopping in the right place*, not at a fixed count.

The core insight: most problems are diagnosed at the proximate cause and fixed there, then recur in a different form. Five-whys forces the analysis past the first few comfortable layers (operator error, missing config, bad data) into the systemic layer (no validation gate, no review process, no observability) where fixes actually prevent recurrence.

## When to Activate

Invoke five-whys when:

- A single, observable, recurring problem needs root-cause analysis
- A post-incident review needs to go past the proximate cause
- A symptom is being treated repeatedly without resolution
- An "operator error" or "bad data" diagnosis feels too convenient

Do NOT use for:

- Multi-cause systemic failures with no single root — use **post-mortem** with contributing-factor analysis
- Forward-looking risk analysis — use **pre-mortem**
- Exploratory work without a clear symptom — use **socratic** or **ecc-blueprint**
- Problems where the root cause is genuinely unknowable — five-whys can produce false confidence

## Method

### Phase 1 — State the symptom precisely

The symptom must be observable, specific, and recent. Vague or attributional symptoms produce vague chains.

| Bad symptom | Good symptom |
|---|---|
| "Deploys are flaky" | "Deploy #4271 on 2026-04-14 failed with `connection refused` on the migration step at 14:23 UTC" |
| "The team is stressed" | "Three engineers logged ≥55 hours last week and one filed a PTO cancellation" |
| "Sales is underperforming" | "March Q1 close rate was 18%, vs forecast 28%, driven by a 47% drop in close-rate on enterprise deals" |

A specific symptom anchors the chain in observable reality. Vague symptoms drift into opinion.

### Phase 2 — Iterate the why chain

Ask "why" of the symptom. Answer with a single causal statement. Then ask "why" of the answer. Repeat until reaching a systemic cause.

```
Why #1: Why did deploy #4271 fail?
  → Because the migration could not connect to the read-replica.
Why #2: Why couldn't the migration connect to the read-replica?
  → Because the IAM role lacked the new VPC permission added last week.
Why #3: Why did the IAM role lack the new VPC permission?
  → Because the migration deploy step doesn't run our IAM-sync workflow.
Why #4: Why doesn't the migration deploy step run IAM-sync?
  → Because IAM-sync was added to api-deploy and ui-deploy but not migration-deploy.
Why #5: Why was migration-deploy missed?
  → Because we have no shared deploy template; each pipeline duplicates IAM logic.
```

The chain stops here because Why #5 surfaces a systemic cause (no shared template) whose fix (extract a shared template) prevents recurrence in any future pipeline. Why #4's fix (add IAM-sync to migration-deploy) only fixes this one symptom — the next new pipeline will have the same gap.

### Phase 3 — Test for root cause

A candidate root cause is a true root cause if and only if both:

1. **Sufficiency test**: removing it would have prevented the symptom.
2. **Generalization test**: fixing it prevents this class of symptom from recurring, not just this instance.

If the candidate fails either test, ask "why" again.

### Phase 4 — Convert root cause to action

The output is not the chain. The output is one or more concrete actions tied to the root cause. Each action must:

- Be assignable to a single owner
- Have a deadline
- Have a verification step (how do we know the root cause is fixed?)

```
Root cause: No shared deploy template; each pipeline duplicates IAM logic.

Actions:
  1. Extract IAM-sync into shared workflow `deploy-iam-bootstrap.yml`.
     Owner: AR. Deadline: 2026-04-30. Verification: all four pipelines reference it.
  2. Add a deploy-pipeline checklist requiring shared-workflow inclusion before merge.
     Owner: Mo. Deadline: 2026-05-07. Verification: next new pipeline auto-fails CI without it.
```

## Output Structure

```markdown
## Symptom
[Observable, specific, dated]

## Why Chain
1. **Why?** — [question]
   → [answer]
2. **Why?** — [question building on #1]
   → [answer]
... (continue until root cause)

## Root Cause
[The systemic cause that, if removed, prevents recurrence of this class of symptom]

Sufficiency check: [yes/no — would removing this have prevented the symptom?]
Generalization check: [yes/no — does fixing it prevent this class, not just this instance?]

## Actions
| # | Action | Owner | Deadline | Verification |
|---|---|---|---|---|
| 1 | ... |

## Stopping Note
Stopped at Why #N because [reason — typically: hit a systemic cause whose fix generalizes].
```

## Anti-patterns

1. **Stopping too soon (proximate-cause trap).** Stopping at "the engineer forgot to add the permission" yields one fix; stopping at "we have no shared template" yields recurring fixes for years.
2. **Stopping too late (rabbit-hole trap).** Drilling past the actionable systemic cause into philosophy ("why does the company exist?") makes the analysis useless.
3. **Blaming people, not systems.** "Why did the engineer forget?" should be answered with system-level explanations (no checklist, no automated check, no review gate), not "they were tired" or "they were new." Toyota's original framing was explicit: people don't cause defects, systems cause defects.
4. **Single-chain thinking on multi-cause problems.** If multiple independent causes contributed, five-whys is the wrong tool — use post-mortem with contributing-factor analysis.
5. **Treating the chain as the deliverable.** The chain is method; the actions are deliverable. A five-whys without owned, dated, verifiable actions is incomplete.
6. **Confirmation drilling.** "Why" should genuinely surface alternatives at each step. If every "why" leads to the answer the analyst wanted from the start, the chain is theatre.

## Render Mode Guidance

- **Transparent (default)**: the chain itself is the deliverable structure. Show it. Five-whys without a visible chain is just an assertion.
- **Stealth (rare)**: only useful when five-whys is embedded inside a larger synthesis. Compress to "the proximate cause was X but the systemic cause was Y" prose.

## Composes Well With

- `post-mortem` (use five-whys *inside* the root-cause phase of a post-mortem)
- `after-action-review` (use five-whys *inside* the "why was there a difference?" question)
- `ecc-blueprint` (decompose the symptom first if it has multiple components)

## Composes Poorly With

- `pre-mortem` (different time direction — pre-mortem is forward, five-whys is backward)
- `deep-sweep` (already heavy; five-whys is intentionally lightweight)
- `llm-council` (multi-perspective synthesis is overkill for single-chain root-cause work)
- `moa` (mixture-of-agents is over-composition for a single-chain operator)

## Notes

- The "five" is approximate. Empirically, root cause is usually reached in 4-7 iterations. If you're at 10+ "whys," you've drilled past actionable territory.
- A five-whys with a "we don't know" answer at any step is honest and useful — it surfaces an investigation gap. Don't fabricate causes to keep the chain going.
- Toyota's original use case was manufacturing defects. The framework generalizes well to incident analysis, ops failures, and recurring sales/delivery problems. It generalizes *less* well to strategic decisions or multi-cause systemic failures.
