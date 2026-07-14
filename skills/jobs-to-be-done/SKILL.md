---
name: jobs-to-be-done
description: "Clayton Christensen's Jobs-to-be-Done framing. Reframe a customer or strategy question as 'what job is the customer hiring this product to do?' Surfaces functional, social, and emotional jobs — and the alternatives a product is actually competing against."
origin: "Clayton Christensen — Competing Against Luck; building on Theodore Levitt"
related_skills:
  - ecc-council
  - wrap-decision-framework
  - six-thinking-hats
---

# Jobs to Be Done

JTBD reframes "what does the customer want?" as "what job is the customer hiring this product to do?" The shift matters because customers don't buy products — they hire products to make progress in a specific situation. The product is interchangeable if a different one does the same job better, cheaper, or with less friction.

The core insight: products compete with anything that gets the same job done, not just with same-category products. A milkshake competes with bagels and coffee for the morning-commute job, not just with other milkshakes. Understanding the *job* — not the product attributes — reveals the real competitive set, the actual switching triggers, and the friction the product is hired to remove.

## When to Activate

Invoke JTBD when:

- A positioning, messaging, or strategy question is framed in product-attribute terms
- A "who is our customer?" question feels too abstract
- Conversion rate or retention is unclear and the analysis lacks situational context
- A new feature or product is being designed without clear job-fit
- Competitive analysis is stuck on category competitors and missing cross-category alternatives

Do NOT use for:

- Already well-understood markets with stable jobs — use **ecc-council** for synthesis
- Source-grounded technical verification — use **recursive-reasoning-operator**
- Adversarial review of an existing strategy — use **red-team-analysis**
- Internal process or operational questions — JTBD is a customer-side lens

## The Three Job Layers

Every "hire" is driven by three layers, weighted differently per buyer.

### Functional Job — What Progress Is Being Made

The literal task the customer is trying to accomplish.

- "Get to work on time"
- "Complete tax filing without errors"
- "Find a candidate for an open role"

### Social Job — How They Want to Be Perceived

Identity and reputation effects of using the product.

- "Be seen as a sophisticated buyer"
- "Be the team member who brought in the new tool"
- "Avoid looking like a beginner"

### Emotional Job — How They Want to Feel

Internal feeling-state effects.

- "Feel in control of finances"
- "Feel less anxious about deadlines"
- "Feel competent / not stupid"

The relative weight depends on the buyer and the moment. B2B SaaS often over-weights functional and under-weights emotional. Consumer products often the reverse. Strategy work that ignores any of the three layers misses the real hire dynamic.

## Method

### Phase 1 — Identify the hire moment

When does the customer "hire" this product? What was happening just before? What triggered the search?

The hire moment is rarely "they realized they needed AI." It is almost always something concrete and situational — a deadline missed, a process that broke, a competitor's move, a personal moment of frustration.

```
Hire-moment template:
  - Trigger event: [the specific thing that happened]
  - Time pressure: [how urgent]
  - Emotional state: [frustrated / anxious / curious / forced]
  - Constraints: [budget / time / political / technical]
```

### Phase 2 — Identify the current solution and its failures

What were they doing before? Why is it inadequate? Critically: not "what's wrong with the current product" but "what's the *job* the current solution is failing to do well."

Failure modes typically cluster:

- Doesn't get the functional job done
- Gets it done but with too much friction
- Gets it done but creates a new social/emotional cost
- Worked once but no longer scales

### Phase 3 — Identify the struggle moments

Within the current solution, where is the customer most uncomfortable? Christensen's research shows that customers tolerate massive product flaws but switch over specific *struggle moments* — the points where the discomfort spikes.

The struggle moment is the conversion lever. Marketing aimed at general dissatisfaction underperforms; marketing aimed at the named struggle moment converts.

### Phase 4 — Identify alternatives considered

What did the customer consider as alternatives? This is the actual competitive set — usually broader than the analyst assumes.

For an AI Audit product:
- Other AI consultancies
- Hiring an internal AI lead
- Doing nothing and waiting
- Buying point-solution AI tools without strategic guidance
- Internal hackathon or pilot project

Each alternative gets the same job done with different tradeoffs. The product's positioning must explain why *this* alternative wins for *this* job in *this* moment.

### Phase 5 — Construct the job statement

Christensen's canonical format:

```
When [situation], I want to [motivation], so I can [expected outcome].
```

Example for an AI Audit:
> When my team is being asked about AI strategy by my board and I don't have a defensible answer, I want a structured assessment that produces a credible roadmap, so I can show progress at the next board meeting without committing to vendors I don't yet trust.

Three tests for a good job statement:

1. **Solution-agnostic**: doesn't mention the product itself.
2. **Outcome-specific**: names what success looks like.
3. **Situational**: anchored to a moment, not a state.

### Phase 6 — Map to product

Once the job is understood, map it back to product decisions:

- **Positioning**: lead with the situation and outcome, not the feature list.
- **Pricing**: anchor to the value of the outcome, not the cost of the alternatives' features.
- **Onboarding**: design the first-week experience around the *struggle moment*, not the product tour.
- **Roadmap**: prioritize features by job-fit, not by feature-count parity with competitors.

## Output Structure

```markdown
## Hire Moment
[Specific situational trigger]

## The Job (Christensen format)
When [situation], I want to [motivation], so I can [expected outcome].

## Three Layers
- **Functional**: [what progress is being made]
- **Social**: [how they want to be perceived]
- **Emotional**: [how they want to feel]

## Current Solution and Why It Fails
[What they're doing now; specific struggle moments]

## Alternatives Considered
| Alternative | Same job? | Why it loses for this hire |
|---|---|---|
| ... |

## Product Implications
- Positioning: ...
- Pricing: ...
- Onboarding: ...
- Roadmap: ...
```

## Anti-patterns

1. **Skipping the situational anchor.** "Customers want efficient AI" is not a job — it's an attribute. The job has a hire moment.
2. **Confusing the job with the product.** "They want our product" is not a job. The job exists independently of the product; the product is just one solution.
3. **Single-layer analysis.** Functional-only JTBD misses social and emotional drivers that often dominate in consumer markets and in B2B trust-purchases.
4. **Competing only with category competitors.** The real competitive set includes anything that gets the same job done — including "do nothing" and "build it internally."
5. **JTBD as a vibe, not a frame.** A good JTBD produces a falsifiable job statement that the team can argue with. A bad JTBD produces "customers want value" platitudes.
6. **Ignoring the struggle moment.** The hire happens at the struggle moment. Marketing without the struggle moment underperforms because it's anchored to dissatisfaction-in-general rather than to the specific spike.

## Render Mode Guidance

- **Stealth (default)**: JTBD reframes the analysis but the output is an integrated strategy recommendation. Embed the job statement and three layers in prose; don't expose the table.
- **Transparent (when team-facing)**: the job statement, three layers, alternatives table, and product implications form a useful artifact for cross-functional alignment. Show the structure when the audience is design + product + marketing + sales who need shared language.

## Composes Well With

- `ecc-blueprint` (decompose the strategy question first; JTBD applied per buyer segment)
- `ecc-council` (multi-perspective on what jobs different buyers are hiring the product to do)
- `wrap-decision-framework` (use JTBD inside W=Widen to surface alternative jobs the product could serve)
- `six-thinking-hats` (use Six Hats inside JTBD's struggle-moment phase for richer emotional and social-job exploration)

## Composes Poorly With

- `recursive-reasoning-operator` (verification shape — different cognitive task)
- `ecc-santa-method` (adversarial verification — wrong cognitive shape for strategy framing)
- `karpathy-guidelines` (code-review guardrails — unrelated)

## Notes

- Christensen's research traces the JTBD framing to Theodore Levitt's "people don't want a quarter-inch drill, they want a quarter-inch hole." The framework formalizes that intuition into a method.
- JTBD is *most* useful when the analyst suspects the team is competing in the wrong category. If the team is sure they know the customer and the data confirms it, JTBD adds little.
- Pairing JTBD with quantitative segmentation often surfaces tension: behavioral segments and JTBD segments rarely match cleanly, which is itself diagnostic information.
