---
name: six-thinking-hats
description: "Edward de Bono's six thinking modes — White (facts), Red (emotion), Black (caution), Yellow (optimism), Green (creativity), Blue (process). Forced perspective rotation when an analysis or group is stuck in a single mode and missing other angles."
origin: "Edward de Bono — Six Thinking Hats (1985)"
related_skills:
  - ecc-council
  - jobs-to-be-done
  - wrap-decision-framework
---

# Six Thinking Hats

Six Hats is a parallel-thinking method designed to defeat the natural tendency to argue from a single mode. By assigning each "hat" a discrete cognitive posture and forcing rotation through all six, the method surfaces angles that an unstructured discussion or a single-mode analysis predictably misses.

The core insight: most arguments fail not because the participants disagree, but because they're each thinking in different modes simultaneously and conflating mode-disagreement with content-disagreement. Six Hats serializes the modes — everyone wears the same hat at the same time — which makes mode-disagreement collapse into focused mode-by-mode coverage.

## When to Activate

Invoke Six Hats when:

- A discussion is stuck in one mode (typically Black/critical or Yellow/optimistic)
- An analysis is missing a perspective the analyst predictably under-weighs
- A group decision needs structured perspective coverage (not just majority vote)
- Brainstorming has stalled and the team needs forced creative pressure (Green) or forced critical pressure (Black)
- Emotion is influencing a decision but isn't being named (Red)

Do NOT use for:

- High-stakes adversarial review — use **red-team-analysis** for committed counter-thesis
- Source-grounded verification — use **recursive-reasoning-operator**
- Single-symptom root-cause work — use **five-whys**
- Decisions that are already well-rounded — overhead exceeds value

## The Six Hats

### White Hat — Facts and Data

Pure information, no interpretation. What do we know? What don't we know? What evidence is missing?

- Prompts: "What are the facts?", "What's the data?", "What information do we lack?"
- Trap: assertions presented as facts. White hat means *named* evidence, not opinion.

### Red Hat — Emotions and Intuition

Feelings, hunches, and gut reactions, named without justification. The point is *surfacing* emotion so it can be examined, not eliminating it.

- Prompts: "What's my gut read?", "What does this feel like?", "What emotion is in the room?"
- Trap: defending feelings with logic. Red hat is permission to name without explaining.

### Black Hat — Caution and Risk

Critical, skeptical, risk-aware mode. What could go wrong? What are the weaknesses? What are we missing? Black is the most-used hat; the discipline is *not* using it everywhere.

- Prompts: "What could go wrong?", "What's the failure mode?", "What evidence contradicts this?"
- Trap: black-hat hijacking. If Black runs uninterrupted, no other mode gets airtime.

### Yellow Hat — Optimism and Benefits

Best-case thinking with explicit benefit articulation. Why might this work? What are the upside paths? What value would this create?

- Prompts: "What's the best case?", "Why would this work?", "What does success unlock?"
- Trap: hand-waving optimism. Yellow requires *named* benefits, not "this could be huge."

### Green Hat — Creativity and Alternatives

Generative mode. New options, novel approaches, hypothetical "what ifs." Green hat suspends evaluation entirely.

- Prompts: "What if we did the opposite?", "What's a version we haven't considered?", "What would [unrelated industry] do?"
- Trap: evaluating green-hat output before it finishes. Defer judgment until green completes.

### Blue Hat — Process and Meta

Meta-cognition. How is this discussion going? What hat should we wear next? Have we covered enough? When is it time to decide?

- Prompts: "What hat are we wearing?", "What's missing?", "Are we ready to decide?"
- Trap: treating Blue as optional. Blue is what makes the rotation work — without it, the group reverts to single-mode default.

## Method

### Phase 1 — Set the question

State the decision or analysis question explicitly. Six Hats applied to a vague question produces vague output across all six modes.

### Phase 2 — Sequence the hats

The sequence depends on the question:

| Question type | Recommended sequence |
|---|---|
| Decision review | Blue → White → Yellow → Black → Red → Green → Blue |
| Brainstorming | Blue → Green → Yellow → Black → Blue |
| Stuck/blocked | Blue → Red → Black → Green → Blue |
| Strategic exploration | Blue → White → Green → Yellow → Black → Red → Blue |

The sequence is a tool, not a rule. The Blue hat opens and closes every session — it sets the question and judges when coverage is complete.

### Phase 3 — Time-box each hat

Allocate a fixed window per hat (typically 3-7 minutes for individual analysis, 10-15 for group). Hard time-boxing prevents Black-hat hijacking and Yellow-hat sprawl.

### Phase 4 — Synthesize under Blue

The closing Blue hat reads:

- What did we learn from each mode?
- Which insights from which hats change the decision?
- What's missing that no hat surfaced?

The output is not a list of mode outputs. It's a synthesis that incorporates the strongest signal from each hat into the recommendation.

## Output Structure

```markdown
## Question
[The decision or analysis being framed]

## White — What We Know
- [fact / evidence]
- [gap]

## Red — What It Feels Like
- [named emotion / intuition / gut read]

## Black — What Could Go Wrong
- [risk / weakness / missing piece]

## Yellow — What Could Go Right
- [named benefit / upside path]

## Green — Alternatives We Hadn't Considered
- [novel option / inversion / cross-domain idea]

## Blue — Synthesis
[Integrated read incorporating the strongest signal from each hat. Names which mode's insights shifted the analysis.]
```

## Anti-patterns

1. **Skipping the Blue hat.** Without Blue, the group reverts to single-mode default — usually Black or Yellow depending on personality. Blue is non-optional.
2. **Hat hijacking.** One person dominates one hat (typically the team's natural skeptic on Black). Either rotate hat-leads or run the rotation in writing.
3. **Wearing all hats simultaneously.** "I'll be objective and consider risks and benefits" is exactly the failure mode Six Hats fixes. Serialize the modes.
4. **Confusing Red with Black.** Red is *named* emotion as data. Black is *reasoned* critique. They have different evidence requirements.
5. **Using Six Hats for adversarial review.** Six Hats is balanced perspective rotation. For committed counter-thesis, use **red-team-analysis**.
6. **Skipping Green when stuck.** When a group is stalled, the temptation is more Black ("what's wrong with what we have?") when the productive move is Green ("what haven't we considered?").

## Render Mode Guidance

- **Stealth (default)**: the rotation is an internal cognitive move. Output is an integrated synthesis that reflects all six hats without exposing the structure ("the strongest counter is X, the strongest upside is Y, the most underweight angle is Z").
- **Transparent (when group-facing)**: the hat-by-hat structure is the deliverable for group decisions where the *audit trail* of perspective coverage matters. Show the hats.

## Composes Well With

- `ecc-council` (multi-perspective family; Six Hats provides the structured rotation that ecc-council does informally)
- `wrap-decision-framework` (Six Hats fits inside W=Widen for forced option-generation)
- `jobs-to-be-done` (use JTBD to set the question; use Six Hats to evaluate)

## Composes Poorly With

- `moa` (already a multi-perspective synthesis — over-composition)
- `llm-council` (already heavyweight perspective synthesis)
- `recursive-reasoning-operator` (verification shape, not perspective shape)
- `red-team-analysis` (Six Hats balances; red-team commits — different tools)

## Notes

- De Bono's research suggests Six Hats reduces meeting time by ~25% and improves perspective coverage measurably. The mechanism is mode-serialization eliminating the cross-talk where participants think in different modes simultaneously.
- The hats are *modes*, not *people*. Rotating which person wears each hat distributes load and prevents personality-driven hat capture.
- For solo analysis, Six Hats is a self-prompting tool: explicitly write under each hat in turn before synthesizing. The serialization discipline is what produces the value, not the group dynamic.
