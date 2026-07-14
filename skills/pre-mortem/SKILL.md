---
name: pre-mortem
description: "Stress-test a forward-looking decision, launch, bet, or plan by asking what could go wrong, walking through risks, assuming it has already failed, and reverse-engineering the causes. Surfaces failure modes BEFORE commitment, when changes are still cheap."
origin: "Gary Klein — Sources of Power"
related_skills:
  - ecc-council
  - ecc-blueprint
  - red-team-analysis
  - wrap-decision-framework
---

# Pre-Mortem

A pre-mortem inverts the post-mortem. Instead of analyzing why something failed after the fact, you assume the plan has already failed at a future date and work backward to enumerate causes. The shift from "what could go wrong?" to "this has gone wrong — what killed it?" is what makes pre-mortem effective: prospective hindsight is more vivid, more honest, and more comprehensive than abstract risk-listing.

The core insight: imagining a definite failure produces sharper causal reasoning than imagining a probabilistic one. People who are asked "why might this fail?" generate generic risks. People asked "this failed in 6 months — explain the failure" generate specific, concrete failure paths.

## When to Activate

Invoke pre-mortem when:

- A forward-looking decision or bet is about to be committed
- Stakes are medium-to-irreversible
- The plan claims high confidence but lacks pilot evidence
- A team is in agreement (groupthink risk)
- A recommendation is being framed as the obvious answer

Do NOT use for:

- Backward-looking failure analysis — use **post-mortem**
- Pure exploration before any plan exists — premature
- Trivial reversible decisions — overhead exceeds value
- Adversarial review of an *existing artifact* (not a forward bet) — use **red-team-analysis**

## Phases

### Phase 1 — Anchor the failure scenario

Set the time horizon explicitly. Generic "this might fail" is weaker than "It is December 2026. The launch failed."

```
Anchor template:
  - Date: [specific future date — typically 6-18 months from decision]
  - Verdict: [the plan failed / the bet did not pay off / the system was rolled back]
  - Visible signal: [the concrete observable that confirms failure]
```

The anchor must be definite, not probabilistic. "It might have failed" produces weak causal reasoning. "It failed" produces strong reasoning.

### Phase 2 — Enumerate causes

For 5-15 minutes, brainstorm causes of the assumed failure. Focus on plausibility, not exhaustiveness. Useful prompts:

- What did we assume that turned out to be wrong?
- What did we ignore that we shouldn't have?
- What did the market / customer / system do that surprised us?
- Who made a decision based on incomplete information?
- What feedback signal did we miss or dismiss?
- What dependency broke that we didn't think to plan for?

Capture each cause as a one-sentence claim. Resist clustering during brainstorming — that comes next.

### Phase 3 — Cluster and rank

Group causes into 4-6 themes. For each theme, score:

| Dimension | 1 (low) | 3 (med) | 5 (high) |
|---|---|---|---|
| Likelihood | Implausible given current evidence | Plausible | Already partially observable |
| Impact | Recoverable inside the plan | Forces re-planning | Kills the bet entirely |
| Detectability | Will be visible early | Visible mid-stream | Invisible until terminal |

Risk score = Likelihood × Impact × (6 − Detectability). Higher is more dangerous (likely + high-impact + invisible-until-late = nightmare).

### Phase 4 — Derive kill criteria and mitigations

For the top 3-5 ranked failure modes:

- **Kill criterion**: a specific observable that, if seen, means stop the plan. Must be measurable, not vibes.
- **Mitigation**: a specific change to the plan that reduces likelihood OR increases detectability.
- **Owner**: who is watching for the kill criterion?
- **Review cadence**: how often is it checked?

Kill criteria are the most important output. A pre-mortem without kill criteria is risk-theater; with kill criteria it becomes decision infrastructure.

## Output Structure

```markdown
## Failure Anchor
On [date], [plan/bet] failed because [verdict]. The visible signal was [observable].

## Top Failure Modes
| # | Failure mode | Likelihood | Impact | Detectability | Risk score |
|---|---|---|---|---|---|
| 1 | ... | 5 | 5 | 1 | 125 |
| ... |

## Kill Criteria
1. **[Failure mode]** — Stop if [observable] by [date]. Owner: [name]. Review: [cadence].
2. ...

## Mitigations
- [Change to plan] — Addresses failure mode #N by [reducing likelihood / increasing detectability].

## What Survives
The mitigations and kill criteria leave [residual risk profile]. Acceptable / unacceptable.
```

## Anti-patterns

1. **Treating "what could go wrong?" as a pre-mortem.** That's a risk register. Pre-mortem requires the assumed-failure anchor.
2. **Skipping kill criteria.** A pre-mortem that produces only mitigations is half a pre-mortem. The kill criteria are what make it actionable.
3. **Optimistic framing in the anchor.** "If this fails…" is weaker than "this failed." Stay in the failure tense.
4. **Letting one person dominate.** Independent enumeration before group ranking surfaces more failure paths than group brainstorming.
5. **Generic causes.** "Bad execution" is not a failure mode. "We hired three CSMs but the second-month CSM ramp was 6 weeks not 3" is.
6. **Pre-mortem as theater.** If the kill criteria are not actually monitored after the decision, the pre-mortem has no effect on the bet's risk profile.

## Render Mode Guidance

- **Transparent (default for verify-adjacent or audit-grade work)**: the failure-mode table and kill-criteria list are the deliverable. Show them.
- **Stealth (when embedded in a synthesis)**: integrate the strongest 2-3 failure modes into the recommendation prose, framed as "the bet is conditional on X, Y, Z; if any of those break, here's what we'll see." Don't expose the table or scoring.

## Composes Well With

- `ecc-blueprint` (decompose the plan first; pre-mortem each branch)
- `ecc-council` (after multi-perspective synthesis, pre-mortem the chosen verdict)
- `wrap-decision-framework` (pre-mortem fills the P=Prepare-to-be-wrong step)
- `red-team-analysis` (red-team attacks the plan; pre-mortem imagines its failure — different angles, both useful)

## Composes Poorly With

- `deep-sweep` (already heavyweight; over-composition)
- `llm-council` (already a heavy synthesis; pre-mortem belongs upstream)
- `feynman` (different cognitive shape — explanation, not stress-testing)
- `socratic` (questioning, not failure-imagination)

## Notes

- Klein's original protocol used 1-2 minutes per cause-enumeration round. Resist the urge to over-deliberate — pre-mortem rewards breadth over depth in Phase 2.
- Pre-mortem is most valuable for plans with confident-sounding language. The more certain the recommendation, the more pre-mortem is needed.
- A pre-mortem that produces zero plausible failure modes means the planner is missing something, not that the plan is bulletproof. Recalibrate.
