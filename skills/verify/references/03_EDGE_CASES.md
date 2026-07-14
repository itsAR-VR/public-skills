# 03 — Verify Edge Cases

Handling non-ideal verification scenarios.

## Dirty workspace

**Situation:** Uncommitted changes exist when user invokes `/verify`.

**Handling:**
1. Run `git status --porcelain` to list uncommitted files
2. Ask user: "Workspace has uncommitted changes. Options: (a) commit them first, (b) stash and verify committed state only, (c) include them in scope with a note"
3. Do NOT silently verify against dirty state

## Plan.md missing or stale

**Situation:** User invokes `/verify` but no `docs/planning/phase-{N}/plan.md` exists, or the plan is clearly out of date vs. shipped commits.

**Handling:**
- If no plan exists: STOP, ask user what the verification target is. Cannot verify against no spec.
- If plan is stale: offer to reconstruct expected criteria from commit messages + user input, OR have user update plan.md first.

Never fabricate success criteria — that defeats the purpose.

## Partial completion with known-risk acceptance

**Situation:** Phase delivered 80% of criteria. User wants to ship anyway.

**Handling:**
1. Document the 20% gap precisely (which criteria, why, what's blocking)
2. Surface the risk-register implication (what could break, how it's detected)
3. Require explicit user confirmation: "Shipping with these gaps — confirm?"
4. Write verdict as PARTIAL, not COMPLETE (honest labeling)
5. Create follow-up TODO in next phase's plan draft

## Out-of-scope findings

**Situation:** During Phase 2 quality audit, the 8-track scan finds issues in files NOT changed by this phase.

**Handling:**
- Default: flag but don't fix. These are out of scope.
- Exception: CRITICAL security findings — surface to user regardless of scope.
- Record in a separate "Out of scope findings" section of verify.md for future cleanup phases.

## Test suite is broken

**Situation:** `npm test` fails, but the failures are pre-existing (not caused by this phase).

**Handling:**
1. Diff test output: is HEAD's failure set == base branch's failure set?
2. If yes: note "inherited failures" — proceed with verify, flag that the test suite needs separate attention
3. If no: new failures caused by this phase → mark Phase 1 as FAIL

## No external docs exist

**Situation:** Phase 3 finds no READMEs, API docs, or user-facing docs in the project at all.

**Handling:**
- Skip with explicit reason: "Project has no external documentation; doc verification not applicable."
- Record in verify.md
- Do NOT auto-generate docs — that's a separate decision.

## Dual reviewer divergence (phase-review PASS, gsd-verifier FAIL)

**Situation:** The two independent reviewers disagree.

**Handling:**
1. Don't just pick one — divergence is a SIGNAL.
2. Compare their criteria: one might catch something the other missed.
3. Most common cause: phase-review checks "did builds pass?" (forward), gsd-verifier checks "did every requirement get implemented?" (backward). Both valid, both needed.
4. Write both verdicts in verify.md. Verdict is the LESS favorable of the two unless investigation shows one is wrong.

## Deep-clean finding that requires architectural discussion

**Situation:** The 8-track audit surfaces a finding that's real but would require a design decision to fix (e.g., circular dep that reveals a flawed module boundary).

**Handling:**
- Do NOT implement. Per deep-clean's rules: if architectural discussion is required, flag and stop.
- Record in verify.md as "requires follow-up planning"
- Suggest: "Open a new phase via `/phase-plan` to address this."

## Concurrent phases in progress

**Situation:** Verify runs while another phase is actively being worked on in the same repo.

**Handling:**
- Verify only the specific phase-N scope, NOT the whole repo state
- Note other active phase(s) in verify.md Context section
- If concurrent phases touched the same files: flag for coordination
- See `08_MULTI_AGENT_COORDINATION.md` in phase-review for detailed procedures

## User wants only part of verify

**Situation:** User says "just check docs" or "just run the 8-track clean" — not the full pipeline.

**Handling:**
- Honor the scope. Run only the requested layer.
- Do NOT silently expand scope.
- Write a partial verify.md labeled "Scope: {layer} only"

## UI audit on non-UI phase

**Situation:** Phase has no UI changes but gsd-ui-auditor was invoked anyway.

**Handling:**
- UI auditor should return "no UI surface in scope"
- Don't treat as PASS — treat as NOT APPLICABLE
- Skip silently in verify.md (just note "not applicable")

## Security audit on non-sensitive phase

**Situation:** Phase doesn't touch auth/payments/data but security-auditor was invoked.

**Handling:**
- Security auditor should return "no security-sensitive surface in scope"
- Same as UI: NOT APPLICABLE, not PASS
