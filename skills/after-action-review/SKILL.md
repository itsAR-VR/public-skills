---
name: after-action-review
description: "US Army-style retrospective using four questions: What was supposed to happen? What actually happened? Why was there a difference? What do we sustain or improve? Use for routine operations review where extracting durable lessons matters more than incident analysis."
origin: "US Army Center for Army Lessons Learned (CALL)"
related_skills:
  - post-mortem
  - five-whys
  - ooda-loop
---

# After-Action Review

The After-Action Review (AAR) is a structured retrospective developed by the US Army for extracting lessons from training exercises and combat operations. Unlike a post-mortem (which focuses on incidents and failures), AAR focuses on *any* meaningful unit of activity — successful or unsuccessful — and asks four questions designed to surface lessons that would otherwise dissolve into "good job, team."

The core insight: most lessons are lost because the team moves to the next thing without explicitly comparing intent vs outcome. The four AAR questions force that comparison and produce two outputs that drive durable improvement: things to sustain (what worked, deliberately preserved) and things to improve (what didn't, with specific changes).

## When to Activate

Invoke AAR when:

- A discrete operation, sprint, project, or campaign has just completed
- A repeated activity (weekly release, monthly close, quarterly campaign) needs structured review
- The team's tacit knowledge from this cycle should become explicit
- Both successes and shortfalls deserve analysis — not just failures
- Lessons from this cycle should inform the next cycle's planning

Do NOT use for:

- Customer-impacting incidents — use **post-mortem** with blameless framing
- Forward-looking decision analysis — use **pre-mortem**
- Single-symptom drilling — use **five-whys**
- Strategic decisions with no completed outcome to review — premature

## The Four Questions

AAR's strength is its constraint. Four questions, in order, no skipping.

### 1. What was supposed to happen?

State the intended outcome and the plan that was supposed to produce it. Be specific:

- What was the goal? (Outcome metric, target date, success criterion.)
- What was the plan? (Steps, owners, dependencies.)
- What were the explicit assumptions?
- What was the success threshold?

This question is harder than it looks. Teams often discover during AAR that the intended outcome was *never explicitly stated* — which is itself a finding.

### 2. What actually happened?

Pure observation. What was the actual outcome? What actually occurred?

- What's the actual metric vs target?
- Where did the plan match reality? Where did it diverge?
- What unexpected events happened?
- What did the team do that wasn't in the plan?

No interpretation here. Just observation. Interpretation comes in question 3.

### 3. Why was there a difference?

This is where most of the analysis effort goes. The gap between intent and reality has causes — surface them.

For each significant difference (positive or negative):

- What conditions changed that the plan didn't anticipate?
- What information did the team have that the plan didn't account for?
- What was the team's adaptation? Did it work?
- What broke? Where? Why?

For *positive* differences (we exceeded the goal): why? What did we do that worked beyond expectation? This is critical — positive differences often go unanalyzed and the team loses the chance to make the success repeatable.

For *negative* differences: use **five-whys** to drill from proximate cause to systemic cause.

### 4. What do we sustain or improve?

Convert the analysis into two named lists:

**Sustain**: specific things that worked and should be deliberately preserved or replicated.

- Not "good teamwork" — specific behaviors, processes, decisions.
- Not "we had energy" — specific structural conditions that enabled the energy.

**Improve**: specific things that should change next time. Each improvement must be:

- Concrete (not "communicate better" — what specifically changes)
- Owned (single accountable person)
- Verifiable (how do we know in the next cycle whether the improvement landed)

The sustain list is often skipped or filled with platitudes. Resist this. Naming what worked, specifically, is how successful patterns become repeatable.

## AAR vs Post-Mortem — The Key Distinction

Both are backward-looking. Both surface lessons. The difference:

| Dimension | Post-mortem | AAR |
|---|---|---|
| Trigger | Incident, failure, customer impact | Any completed unit of activity |
| Cadence | Reactive (per incident) | Routine (per cycle) |
| Tone | Blameless analysis of what went wrong | Balanced sustain/improve |
| Output | Action items + root cause | Sustain list + improve list |
| Scope | Diagnose and prevent recurrence | Continuous improvement |

Use post-mortem when something broke. Use AAR when something completed.

## Format and Cadence

The AAR works best when:

- It happens *immediately* after the activity (within 24 hours; memory decays fast)
- It is short (30-60 minutes for routine; longer for major operations)
- It includes everyone who participated, not just leadership
- It is conducted by a facilitator, not the most senior person (so seniors can speak freely)
- Notes are captured in writing — the artifact survives the meeting

The Army's research on AAR convergence: teams that hold AARs after every operation reach high performance ~50% faster than teams that don't. The mechanism is *cumulative explicit lesson-extraction*, not the meeting itself.

## Output Structure

```markdown
## Operation
[The activity being reviewed; date range]

## 1. What Was Supposed to Happen
- Goal: ...
- Plan: ...
- Assumptions: ...
- Success threshold: ...

## 2. What Actually Happened
- Outcome vs target: ...
- Plan vs reality: ...
- Unexpected events: ...

## 3. Why Was There a Difference?
For each significant difference:
- **[Difference]**: [why — proximate cause + systemic cause]

## 4. Sustain
1. [specific thing that worked + structural reason it worked]
2. ...

## 4. Improve
| # | What changes | Owner | Verification next cycle |
|---|---|---|---|
| 1 | ... |

## Lessons (one paragraph for the next-cycle planner)
[The 1-3 most important things the next cycle's planner needs to know]
```

## Anti-patterns

1. **Skipping question 1.** Without explicit intent, there's nothing to compare reality against. The whole AAR collapses.
2. **Mixing observation and interpretation.** Question 2 is observation, question 3 is interpretation. Mixing them produces "what happened was that we failed because we were tired" — which is interpretation disguised as observation.
3. **Sustain list as platitudes.** "Good teamwork" is not a sustain. "The cross-functional standups at 9am produced visible alignment that we should keep" is a sustain.
4. **Improve list without owners.** A list of improvements with no accountability is a wish list.
5. **Senior-driven AAR.** When the most senior person sets the narrative, juniors don't share what they actually saw. Use a facilitator.
6. **Holding AAR weeks later.** The lesson decays exponentially. The 24-hour rule matters.
7. **Treating AAR as performance review.** AAR is about the *operation*, not the people. Performance review is a separate process with separate norms.

## Render Mode Guidance

- **Transparent (default)**: the four-question structure is the deliverable. Show it. The audit trail of intent-vs-reality is the value.
- **Stealth (rare)**: only when AAR feeds into a synthesis report. Even then, the four-question structure usually survives because it's compact and lossless.

## Composes Well With

- `five-whys` (use inside question 3 for negative-difference root-cause drilling)
- `post-mortem` (AAR for the cycle; post-mortem for any incidents *within* the cycle)
- `ooda-loop` (AAR feeds the Orient phase of the next OODA cycle)
- `ecc-blueprint` (decompose multi-track operations into per-track AARs)

## Composes Poorly With

- `pre-mortem` (opposite time direction; AAR is retrospective)
- `feynman` (explanation, not retrospective analysis)
- `recursive-reasoning-operator` (verification shape — different cognitive task)
- `karpathy-guidelines` (code review — different scope)

## Notes

- The Army's AAR practice was originally developed at the National Training Center and is now codified in CALL doctrine. The framework has crossed into business retrospective practice through Agile, but the four-question discipline is often diluted in software contexts.
- AAR works for solo work too. The four questions, asked of yourself after a meaningful unit of work, surface lessons that journaling alone misses.
- The most underrated question is question 4 / sustain. Successful patterns are usually invisible to the team that produced them — naming them explicitly is what makes them repeatable.
