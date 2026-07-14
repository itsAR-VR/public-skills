---
name: wrap-decision-framework
description: "Heath brothers' WRAP method for high-stakes decisions: Widen options, Reality-test assumptions, Attain distance before deciding, Prepare to be wrong. Counters the four villains of decision-making — narrow framing, confirmation bias, short-term emotion, overconfidence."
origin: "Chip Heath and Dan Heath — Decisive: How to Make Better Choices in Life and Work"
related_skills:
  - pre-mortem
  - ecc-council
  - six-thinking-hats
  - ooda-loop
---

# WRAP Decision Framework

WRAP is a four-step decision process designed to defeat the four most common decision-making failure modes documented in the Heaths' research:

| Villain | WRAP step that defeats it |
|---|---|
| Narrow framing ("should I do X or not?") | **W**iden options |
| Confirmation bias (selective evidence) | **R**eality-test assumptions |
| Short-term emotion | **A**ttain distance |
| Overconfidence | **P**repare to be wrong |

Each step has specific, named cognitive moves — not generic "think more" advice. The framework's value is that it routes around the *specific* failure modes most likely to corrupt the decision.

## When to Activate

Invoke WRAP when:

- A high-stakes decision is being framed as binary ("should we do X or not?")
- A team has converged on an answer with limited option-search
- The decision involves emotional or political pressure
- Pilot or prior evidence is thin
- The cost of being wrong is high enough to justify deliberate process

Do NOT use for:

- Reversible, low-stakes decisions — overhead exceeds value
- Already-explored option spaces with strong evidence — use **ecc-council** for synthesis
- Time-sensitive operational decisions — use **ooda-loop**
- Pure exploration with no decision pending — premature

## Phase 1 — W: Widen Your Options

Narrow framing is the single most common decision pathology. The fix is forcing the option-set wider before evaluating.

### Cognitive moves

**Vanishing options test**: "If the current option were unavailable, what would I do?" This forces consideration of alternatives the original framing excluded.

**Opportunity-cost framing**: "What else could I do with the resources this decision consumes?" Reframes the decision from yes/no to what-instead.

**Multitracking**: explicitly develop 2-4 alternatives before evaluating any. Single-track decisions correlate with worse outcomes in the Heaths' research; multitrack does not require more time but does require explicit option-search.

**Find someone who solved this problem**: who has already faced this decision? What did they learn? Look for ladders, not blank slates.

### Output of Phase 1

A list of 3-5 distinct options, each clearly stated. If the original framing was "should we do X?", at least four options should now exist (do X, don't do X, do something different from X, do a piece of X).

## Phase 2 — R: Reality-Test Your Assumptions

Confirmation bias is the next villain. The fix is engineering disagreement, not seeking it.

### Cognitive moves

**Consider the opposite**: for each option, what evidence would falsify the case for it? Search for that evidence specifically, not for confirming evidence.

**Zoom out, zoom in**: compare base rates (zoom out: how often do projects of this type succeed?) AND specific evidence (zoom in: what does this exact case look like up close?). Either alone biases.

**Ooch**: run a small, cheap, time-boxed experiment that produces real data instead of more debate. Pilots beat predictions.

**Devil's advocate that won't dissolve**: appoint someone (not rotating) to argue against the leading option through the entire deliberation, with kill criteria specified upfront for when their objections would change the decision.

### Output of Phase 2

For each option from Phase 1: the strongest disconfirming evidence available, the base-rate, and where possible, the result of a cheap experiment.

## Phase 3 — A: Attain Distance Before Deciding

Short-term emotion is the third villain. The fix is structured perspective-shifting before commitment.

### Cognitive moves

**10/10/10**: how will I feel about this decision in 10 minutes? 10 months? 10 years? Reveals which emotions are short-lived and which are durable.

**Advice to a friend**: if a friend faced this exact situation, what would I tell them to do? Strips the situational urgency and personal stake.

**Core priorities check**: which of the options best serves the long-term priorities I committed to before this decision arose? If priorities shift to fit the decision, that's a red flag for short-term-emotion capture.

### Output of Phase 3

A statement of which option best serves long-term priorities, with explicit acknowledgment of which short-term emotions are pulling in a different direction.

## Phase 4 — P: Prepare to Be Wrong

Overconfidence is the fourth villain. The fix is engineering the decision to survive being wrong.

### Cognitive moves

**Bookend the future**: imagine the best plausible outcome and the worst plausible outcome. The realistic range is usually wider than initial planning assumes.

**Pre-mortem**: assume the chosen option failed in 12 months. Why? (See the **pre-mortem** operator for the full method.)

**Tripwires**: define specific observables that, if seen, would change the decision. Without tripwires, decisions drift on autopilot — the bias toward continuing what was started overpowers contradicting evidence.

**Set kill criteria**: what would we have to see for us to abandon this option, and by when?

### Output of Phase 4

A list of 3-5 tripwires and at least one explicit kill criterion. Without these, Phase 4 has not actually happened.

## Output Structure

```markdown
## Decision Frame
[The original question, restated to avoid narrow framing]

## W — Options Considered
1. [option] — [one-sentence summary]
2. ...
4. ...
(Vanishing-options test result: ...)
(Opportunity-cost framing: ...)

## R — Reality-Tested Assumptions
| Option | Disconfirming evidence | Base rate | Pilot/Ooch result |
|---|---|---|---|
| 1 | ... |
| ... |

## A — Distance Check
- 10/10/10 read: ...
- Advice-to-a-friend read: ...
- Long-term-priority alignment: ...

## P — Preparing to Be Wrong
**Tripwires** (any one of these triggers reconsideration):
1. [observable] by [date]
2. ...

**Kill criterion**: [the single observable that would force abandoning the chosen option]

## Decision
[Chosen option + rationale + acknowledged short-term emotions running counter]
```

## Anti-patterns

1. **Skipping W.** "We considered other options" without naming them is not Widen. Force at least 3 named options into Phase 1.
2. **Reality-testing the chosen option only.** R must apply to all options, not just the leader. Otherwise it becomes confirmation-search dressed up as Reality-test.
3. **Treating 10/10/10 as a vibe-check.** The point is comparing time-horizon emotional weight, not using "10 years from now" as an excuse for the leader's preferred answer.
4. **Tripwires without owners.** A tripwire that no one is watching for has no effect on the decision's risk profile.
5. **WRAP as theater.** If the answer was decided before W started and the framework is run after the fact, it is not improving the decision. Run WRAP *before* commitment.

## Render Mode Guidance

- **Stealth (default)**: WRAP applies internally; the output is an integrated decision recommendation with embedded rationale ("we considered three options, the strongest disconfirming evidence on the leader is X, the 10/10/10 read is Y, the kill criteria are Z"). Phase 0 data shows decide-class tasks benefit from stealth rendering.
- **Transparent (when stakes warrant)**: high-stakes irreversible decisions justify showing the full WRAP table — not because the framework needs to be visible, but because the *decision audit trail* needs to be visible.

## Composes Well With

- `pre-mortem` (fills the P=Prepare-to-be-wrong step)
- `ecc-council` (adds multi-perspective evaluation inside W and R)
- `red-team-analysis` (sharpens the disconfirming-evidence search in R)
- `six-thinking-hats` (provides forced perspective rotation inside W when option-search is stuck)

## Composes Poorly With

- `deep-sweep` (already heavyweight; over-composition)
- `feynman` (different cognitive shape — explanation, not decision)
- `recursive-reasoning-operator` (verification-shape, not decision-shape)

## Notes

- WRAP's research base is decision-quality outcomes across ~10,000 documented decisions in the Heaths' synthesis. The most reliably damaging villain is narrow framing, which makes Phase 1 (W) the most consequential step.
- The four steps are independently useful. If only one phase is run, run W. If two, run W + P. If three, drop A.
- WRAP composes well with quantitative decision tools (DCF, expected-value, scenario analysis). The framework is a process scaffold, not an analysis method.
