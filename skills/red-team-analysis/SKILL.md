---
name: red-team-analysis
description: "Adversarial review of an existing artifact, plan, or claim. Find the strongest counter-argument and stress-test the most load-bearing assumption — not just enumerate generic objections."
origin: "US military / intelligence community red-teaming practice; adapted for analytical review"
related_skills:
  - ecc-santa-method
  - pre-mortem
  - recursive-reasoning-operator
  - ecc-council
---

# Red-Team Analysis

A red team's job is to make the plan fail in argument before it fails in reality. Unlike a generic critique pass, red-teaming requires *adopting the opposing posture* — not just listing concerns from a neutral position. The red-teamer's success metric is "did I find an attack the original author hadn't considered?", not "did I produce a balanced review?"

The core distinction from generic critique: red-team analysis targets the *strongest claim* and the *most load-bearing assumption* — not the weakest. Attacking weak claims is shooting fish in a barrel; attacking the strongest claim is what produces decision-relevant signal.

## When to Activate

Invoke red-team analysis when:

- An existing artifact (plan, audit, recommendation, design doc) needs adversarial review
- A claim is being treated as load-bearing without explicit stress-testing
- Multiple stakeholders agree (groupthink risk)
- A recommendation lacks pilot or empirical evidence
- The cost of a hidden flaw is high enough to justify deliberate hostility

Do NOT use for:

- Generic code review — use `code-reviewer` agent or `karpathy-guidelines`
- Forward-looking decisions without an existing artifact — use **pre-mortem**
- Source-grounded fact verification — use **recursive-reasoning-operator** + **ecc-santa-method**
- Brainstorming new options — use **six-thinking-hats** or **ecc-council**

## Phases

### Phase 1 — Identify the strongest claim

Read the artifact and ask: if I had to bet against one claim, which would be most expensive to be wrong about? That's the target.

Common targets:

- The recommendation framed as "the obvious answer"
- The assumption that drives the entire decision tree
- The claim with the highest confidence label but least evidence
- The "this is high-leverage" framing that anchors the rest of the analysis

The wrong move is targeting weakly-supported claims. Those are easy to attack and produce no signal — the original author already knew they were soft.

### Phase 2 — Adopt opposing posture

This is the move that distinguishes red-team from critique. You are now the advocate for the opposite position. Not neutral — opposite.

Mental shift:

- Critique posture: "I want to find concerns to flag."
- Red-team posture: "I am paid to defeat this claim. What's my best argument?"

The posture shift produces sharper attacks because it forces commitment to a counter-thesis, not just enumeration of doubts.

### Phase 3 — Enumerate attacks

For the targeted claim, enumerate attacks across these vectors. Aim for breadth before depth.

| Attack vector | Question to ask |
|---|---|
| Logic | Does the conclusion follow from the premises? Is there a hidden inference? |
| Evidence | Is the cited evidence sufficient? Is it being used out of context? Is contradicting evidence ignored? |
| Alternative interpretation | Can the same evidence support a different conclusion? |
| Missing data | What evidence would falsify the claim that wasn't sought? |
| Hidden assumption | What must be true for this claim to hold that isn't stated? |
| Selection bias | Was the evidence cherry-picked? Are there relevant cases not examined? |
| Confidence calibration | Is the confidence label justified by the evidence type? |
| Time decay | Is the claim true now but unlikely to remain true? |

Capture each attack as a one-sentence challenge plus the strongest defense the original author could mount.

### Phase 4 — Score and rank attacks

For each attack, score:

- **Strength** (1-5): how hard is this for the original author to refute?
- **Decisiveness** (1-5): if this attack lands, how much does the underlying recommendation change?

Rank by Strength × Decisiveness. Anything ≥ 16 is a survival-threatening attack — surface it loudly. Lower scores are edge concerns.

### Phase 5 — Defender response

For each top-ranked attack, the original author (or someone in their stead) drafts the strongest defense. The output is not "the red team won" or "the defender won" — it's a documented exchange that the decision-maker can read and judge.

A red-team analysis without a defender response is a hit-and-run. A red-team analysis WITH a defender response is decision infrastructure.

## Output Structure

```markdown
## Target Claim
[The single strongest, most load-bearing claim from the artifact]

Original confidence: [high/medium/low as labeled in the source]
Red-team posture: [the counter-thesis being adopted]

## Attacks
| # | Attack | Vector | Strength | Decisiveness | Score |
|---|---|---|---|---|---|
| 1 | ... | logic | 5 | 5 | 25 |
| ... |

## Surviving Attacks (score ≥ 16)
### Attack #N: [one-sentence summary]
- **Challenge**: [the attack in detail]
- **Strongest defense**: [the original author's best response]
- **Net read**: [does the attack land partially, fully, or get refuted?]

## Verdict
- **Claims that survive scrutiny**: [list]
- **Claims that need additional evidence before relying on**: [list]
- **Claims that should be downgraded or removed**: [list]

## Recommendation
[What changes in the original artifact based on the red-team pass]
```

## Anti-patterns

1. **Attacking weak claims.** Easy targets, zero signal. Always target the strongest, most load-bearing claim.
2. **Hostile-for-its-own-sake.** Red-teaming is a *service* to the decision, not a performance of skepticism. The goal is sharper decisions, not winning the argument.
3. **No defender response.** A red-team finding without a defense is a flag, not an analysis. Always close the loop.
4. **Confusing red-team with devil's-advocate.** Devil's-advocate is rotating — anyone can play the role briefly. Red-team is committed — the red-teamer adopts and defends the counter-thesis throughout the analysis.
5. **Generic objections.** "What if your assumptions are wrong?" is not an attack. "Your assumption that 31 leads represents pipeline strength conflates volume with stage-distribution; without funnel-stage data the headline number could be 80% top-of-funnel and the urgency framing collapses" is an attack.
6. **Ignoring confidence calibration.** Often the most decisive attack is "this claim's confidence label doesn't match its evidence type." Worth surfacing explicitly.

## Render Mode Guidance

- **Transparent (default)**: the attack table, surviving attacks, and verdict are the deliverable. The structure IS the value — show it.
- **Stealth (rare)**: only when red-team is embedded inside a longer synthesis that needs integrated output. Lose the table, retain the strongest 2-3 surviving attacks woven into the prose.

## Composes Well With

- `ecc-blueprint` (decompose the artifact first; red-team each major claim)
- `recursive-reasoning-operator` (extract source-grounded claims first; red-team after)
- `ecc-santa-method` (red-team identifies the attack surface; santa-method's two reviewers verify each surviving attack independently)
- `pre-mortem` (red-team attacks an existing claim; pre-mortem imagines a forward failure — paired they cover both retrospective and prospective stress-testing)

## Composes Poorly With

- `feynman` (explanation, not adversarial)
- `socratic` (open-ended questioning, not committed counter-thesis)
- `karpathy-guidelines` (review-style guardrails, not adversarial)

## Notes

- Red-teaming is *creative work*. The best red-teamers find attacks the author hadn't considered, not just amplify concerns the author already noted.
- A red-team pass with zero score-≥16 attacks usually means the target was wrong — pick a stronger claim.
- Red-team output is fuel for the decision-maker, not a verdict on the artifact. Frame findings as "here are the attacks; here are the defenses; you decide whether the bet survives" — not "the plan is broken."
