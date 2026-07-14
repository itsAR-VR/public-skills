---
name: post-mortem
description: "Backward-looking incident or failure analysis. Build a timeline, separate root causes from contributing factors, extract actionable lessons. Blameless by default — analyzes systems, not people."
origin: "Aerospace / engineering culture; popularized in software engineering by Etsy, Google SRE practice"
related_skills:
  - five-whys
  - after-action-review
  - ecc-santa-method
---

# Post-Mortem

A post-mortem analyzes an incident or failure that has already occurred. The goal is not to assign blame — it is to extract lessons that prevent recurrence of the *class* of failure, not just this specific instance. Blameless framing is non-optional: the moment a post-mortem becomes about who, the participants stop telling the truth and the analysis becomes useless.

The core insight: the cause of an incident is almost always *systemic*, not individual. Even when an operator made an error, the post-mortem question is "why did the system allow that error to cause this outcome?" not "why did the operator make the error?" Systems are fixable; blaming people prevents the system fix.

## When to Activate

Invoke post-mortem when:

- An incident, outage, or significant failure has occurred
- A project has visibly missed its goal
- A customer-impacting event needs structured review
- A decision turned out badly and the team needs to extract learning

Do NOT use for:

- Forward-looking risk analysis — use **pre-mortem**
- Routine operational retrospectives without an incident — use **after-action-review**
- Single-symptom drilling — use **five-whys** (which is a *tool inside* post-mortem)
- Adversarial review of an existing artifact — use **red-team-analysis**

## Phases

### Phase 1 — Establish the timeline

Before analyzing causes, build the timeline of what happened. Pure observation, no interpretation.

- Start: when did the impact begin?
- Detection: when was the issue first detected? By whom? Through what signal?
- Response: who was notified? What was the first action?
- Mitigation: what stopped or contained the impact?
- Resolution: when was the issue fully resolved?
- Recovery: when did affected systems / customers / metrics return to normal?

The timeline is foundational. Disagreements about cause often dissolve when the timeline is laid out — participants discover they were misremembering sequence.

### Phase 2 — Establish the impact

Quantify what happened. This drives the priority of action items in Phase 5.

- Customers affected: count and severity
- Revenue impact: direct loss + indirect (refunds, churn risk)
- Time impact: duration of incident, response, recovery
- Operational impact: hours of engineering time consumed, opportunity cost
- Trust impact: reputational, customer-relationship, regulatory

Specific numbers, not "significant impact."

### Phase 3 — Identify contributing factors

Most incidents have *multiple* contributing factors — not a single cause. List them:

- What had to be true for this incident to occur?
- What missing controls would have prevented it?
- What system properties made the impact larger?
- What detection gaps delayed the response?
- What response gaps slowed mitigation?

Each contributing factor is a separate failure of a system property. Listing them all matters because fixing one factor often only buys partial protection — the *combination* of factors caused the impact.

### Phase 4 — Identify root cause(s)

For each top contributing factor, drill via **five-whys** to a systemic root cause. The root cause must satisfy:

- **Sufficiency**: removing it would have prevented the incident.
- **Generalization**: fixing it prevents this class of failure, not just this instance.
- **Actionability**: a concrete fix exists.

Multi-cause incidents may have multiple root causes. Don't force-collapse to a single one if the system genuinely had multiple independent failures.

### Phase 5 — Counter-factuals

For each root cause, ask:

- What would have caught this earlier? (detection improvement)
- What would have prevented the incident entirely? (prevention)
- What would have reduced the blast radius? (containment)

Each counter-factual becomes a candidate action item.

### Phase 6 — Action items

Convert counter-factuals to specific, owned, dated, verifiable actions. Every action must:

- Solve a *systemic* gap, not a personal one ("write a runbook" not "be more careful")
- Have a single owner (not a team)
- Have a deadline
- Have a verification step (how do we know the gap is closed?)

Prioritize ruthlessly: 3-5 high-leverage actions beat 20 ambitious ones. A long action list rarely gets executed.

### Phase 7 — Lessons learned

Two paragraphs maximum, written for an audience that will read this six months later:

- What surprised us about this incident?
- What pattern, if recognized earlier, would have changed the response?

Lessons are the part of the post-mortem most likely to be re-read. Make them sharp.

## Blameless Framing — Why It's Load-Bearing

The temptation in incident analysis is to identify "who messed up." This temptation is corrosive in three ways:

1. **It encourages lying.** Operators won't share what they actually did, what they actually thought, or what signals they ignored, if they expect blame. The analysis becomes fiction.
2. **It misdiagnoses the cause.** Even when an operator did the wrong thing, the systemic question is why the system allowed the wrong thing to cause the outcome. People will always make errors; the system has to absorb them.
3. **It makes the fix unactionable.** "Be more careful" is not a fix. Systemic fixes (validation, automation, review gates, observability) are fixes.

Practical blameless framing:

- Use roles and systems as subjects: "the deployment process allowed an unreviewed migration" not "Alice deployed an unreviewed migration."
- Assume good intent and competence: ask "what made this seem like the right action at the time?"
- Surface decision context: what did the operator know? What signals were available? What was the time pressure?

## Output Structure

```markdown
## Incident Summary
- Date / time: ...
- Duration: ...
- Severity: ...
- One-line description: ...

## Timeline
| Time (UTC) | Event | Source |
|---|---|---|
| HH:MM | ... | (logs / chat / human) |

## Impact
- Customers affected: ...
- Revenue impact: ...
- Operational impact: ...

## Contributing Factors
1. [factor] — [what had to be true]
2. ...

## Root Cause(s)
For each: a five-whys chain ending at a systemic cause that passes sufficiency / generalization / actionability tests.

## Counter-factuals
- Detection: ...
- Prevention: ...
- Containment: ...

## Action Items
| # | Action | Owner | Deadline | Verification |
|---|---|---|---|---|

## Lessons Learned
[2 paragraphs, sharp, written for a 6-months-later reader]
```

## Anti-patterns

1. **Blame.** "Operator error" is not a root cause. It's a sign the analysis stopped early.
2. **Single-cause framing on multi-cause incidents.** Forcing a complex incident into one root cause loses the systemic insight.
3. **Action items without owners or deadlines.** The post-mortem becomes a wishlist instead of decision infrastructure.
4. **"Be more careful" as a fix.** Systemic gaps are not solved by personal vigilance.
5. **Skipping the timeline.** Without a precise timeline, cause analysis is built on faulty memory.
6. **Post-mortem as a meeting, not an artifact.** A good post-mortem produces a written document that survives the meeting. The artifact is the value, not the meeting.
7. **Treating impact softly.** Without quantified impact, the priority of action items is impossible to set.

## Render Mode Guidance

- **Transparent (default)**: the timeline, contributing factors, and action items form the deliverable structure. The post-mortem document IS the output. Show the structure.
- **Stealth (rare)**: only when post-mortem is embedded in a longer narrative. Most post-mortems should remain transparent — the structure is what makes it auditable later.

## Composes Well With

- `five-whys` (use inside Phase 4 root-cause drilling)
- `after-action-review` (similar shape; AAR is for routine ops, post-mortem is for incidents)
- `ecc-blueprint` (decompose multi-system incidents into per-system contributing factors)

## Composes Poorly With

- `pre-mortem` (opposite time direction)
- `feynman` (explanation, not analysis)
- `karpathy-guidelines` (code review, not incident analysis)
- `deep-sweep` (over-composition for what should be a focused post-incident analysis)

## Notes

- The Etsy and Google SRE post-mortem cultures pioneered the blameless-by-default convention. The empirical result across both organizations was *more* honest reporting and *faster* fix cycles, not less accountability.
- Post-mortems that produce no action items are signs the analysis stopped at "we got unlucky" — which is rarely the actual cause.
- A post-mortem that no one reads six months later didn't extract durable lessons. The "Lessons Learned" section is the highest-leverage piece for future-team learning.
