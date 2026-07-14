---
name: ooda-loop
description: "John Boyd's Observe-Orient-Decide-Act cycle. Decision-making framework for fast-moving competitive situations where the speed of the cycle and the quality of orientation matter as much as the quality of any single decision."
origin: "John Boyd — USAF / military strategy; adapted broadly for competitive decision-making"
related_skills:
  - wrap-decision-framework
  - after-action-review
  - ecc-blueprint
---

# OODA Loop

The OODA Loop — Observe, Orient, Decide, Act — is John Boyd's framework for decision-making under competitive pressure. The framework's value is not the four steps (which look obvious) but the insight that *Orient* dominates the cycle: how you interpret what you observe determines what you can decide and act on. Two opponents with the same observations can reach opposite decisions because their orientation — informed by experience, culture, mental models, and prior conditioning — produces different interpretations.

The core insight: in fast-moving situations, the operator who completes OODA cycles faster *and* with better orientation has structural advantage. Boyd's analysis of dogfights showed that the side with the faster OODA cycle won even with inferior aircraft, because each cycle produced a position the opponent's orientation hadn't yet caught up to.

## When to Activate

Invoke OODA when:

- A decision is being made under competitive or adversarial pressure
- The situation is changing faster than the analysis cycle
- The team is over-deliberating in a context that rewards speed
- Multiple parties are reacting to the same evolving signal
- The cost of a slow correct decision exceeds the cost of a fast approximate one

Do NOT use for:

- High-stakes irreversible decisions where deliberation is appropriate — use **wrap-decision-framework**
- Backward-looking analysis — use **after-action-review** or **post-mortem**
- Strategic decisions with long horizons — OODA is for tactical/operational tempo
- Single-symptom diagnostics — use **five-whys**

## The Four Steps

### Observe — What Is Happening

Gather information from the environment. Sensors, signals, data feeds, customer reports, market moves, opponent actions.

The observation phase has two failure modes:

- **Observing too narrowly**: missing signals from outside the expected channel.
- **Observing too much**: drowning in noise without filter.

Good observation requires pre-defined signal categories that capture what matters without consuming attention on what doesn't.

### Orient — What Does It Mean

The dominant phase. Boyd's claim: orientation is "the most important part of the OODA loop because it shapes the way we interact with the environment — hence orientation shapes the way we observe, the way we decide, the way we act."

Orient integrates:

- **Cultural traditions**: assumptions baked in by the operator's environment
- **Genetic heritage**: deep priors about how the world works
- **Previous experience**: pattern recognition from prior cycles
- **New information**: from the current Observe
- **Analysis and synthesis**: explicit reasoning about the situation

The orient phase is where wrong mental models corrupt the entire cycle. An operator with outdated orientation will mis-interpret current observations, decide based on the misinterpretation, and act in a way that worsens position. Speed of the cycle matters less than orientation quality — but ideally both.

### Decide — What Will I Do

Choose the action. In Boyd's military framing, the decision is hypothesis-formation: "given my current orientation, this action should produce that outcome." The decision is testable; the next cycle's Observe will confirm or refute.

Decision speed is constrained by orientation quality. With strong orientation, decisions can be near-immediate (intuitive recognition of the situation pattern). With weak orientation, decisions require deliberation — which slows the cycle.

### Act — Execute and Test

Execute the decision. Crucially, the act phase produces *new observations*: it changes the environment, surfacing how the system responds. The act is both an output and an input to the next cycle.

A complete OODA cycle ends with the action *and* the start of the next observation phase. There is no terminal state — the loop runs as long as the situation requires.

## Why Orient Dominates — Boyd's Asymmetry

Boyd's central claim: in competitive pressure, the operator who can disrupt the opponent's orientation faster than they can re-orient *wins regardless of resource asymmetry*. Examples:

- Dogfights where the faster OODA pilot wins despite inferior aircraft
- Market entries where the incumbent's orientation is anchored to a now-obsolete competitive set
- Negotiations where one party reframes the deal terms before the other's orientation catches up

The implication for operators: investing in orientation quality (sensor diversity, mental-model updating, post-action review) compounds across cycles. Investing only in decision speed without orientation produces fast wrong decisions.

## Method

### Phase 1 — Set the cycle scope

OODA scales from seconds (combat) to weeks (market response). Define the cycle scope before applying the framework:

- What's the cycle horizon? (How fast does the situation change?)
- What's the reasonable cycle time? (How fast can I complete OODA?)
- What's the consequence of a misaligned decision? (Recoverable / costly / fatal?)

For software / business operations, cycles typically run hours to days. For competitive responses to opponent moves, cycles run days to weeks.

### Phase 2 — Observe with pre-defined categories

Pre-define what signals matter so that the observe phase doesn't drift. Examples:

- Customer behavior signals (conversion, retention, support volume)
- Competitive signals (pricing, feature parity, hiring patterns)
- Internal signals (team velocity, error rates, deployment frequency)
- External signals (regulatory, macro, partner ecosystem)

Without pre-defined categories, observation collapses to "whatever I noticed today" — which biases toward salient-but-irrelevant.

### Phase 3 — Orient explicitly

Force the orientation step into explicit form:

- Given these observations, my current model says ___
- The most relevant prior pattern is ___
- The assumption I'm making about the opponent / market / system is ___
- What would have to be true for my current orientation to be wrong?

The last question is the most valuable. Boyd's orientation-disruption insight applies to your *own* orientation: the operator who routinely asks "what would falsify my current orientation?" updates faster than one who doesn't.

### Phase 4 — Decide with hypothesis framing

Frame the decision as a testable hypothesis:

- Action: ___
- Expected outcome: ___
- Confirming signals: ___ (what we'd see if right)
- Disconfirming signals: ___ (what we'd see if wrong)

The disconfirming signals matter most — they trigger the next OODA cycle's re-orientation.

### Phase 5 — Act and immediately observe

Execute the decision. The act phase ends when the next observation phase begins — observe the response, re-orient, decide again.

## Output Structure (per cycle)

```markdown
## Cycle [N] — [date/time]

## Observe
- Signals: [pre-defined categories with current values]
- New / unexpected: ...

## Orient
- Current model: ...
- Most relevant prior pattern: ...
- Operating assumption: ...
- What would falsify this orientation: ...

## Decide
- Action: ...
- Expected outcome: ...
- Confirming signals: ...
- Disconfirming signals: ...

## Act
- Executed: ...
- Immediate response observed: [feeds Cycle N+1's Observe phase]
```

## Anti-patterns

1. **Treating OODA as four discrete sequential steps without recognizing Orient's dominance.** This produces fast cycles built on bad orientation — a worse outcome than slow cycles with good orientation.
2. **Skipping the falsification question in Orient.** Without it, OODA becomes confirmation-cycling: each observation is interpreted to fit the existing orientation and the cycle never updates.
3. **Decision without disconfirming signals.** A decision without specified disconfirming signals can't drive the next cycle's re-orientation.
4. **OODA for non-competitive contexts.** The framework was designed for competitive pressure. Applying it to high-deliberation strategic decisions slows the analysis without adding value — use **wrap-decision-framework** instead.
5. **Cycle-time obsession.** Faster cycles with worse orientation lose to slower cycles with better orientation. Speed is necessary but not sufficient.
6. **No artifact.** OODA cycles run in operators' heads. Without writing the orient and decide phases, learning across cycles doesn't compound.

## Render Mode Guidance

- **Either** — OODA can be applied internally with the output being the action itself (stealth), or transparently with each cycle's table written down for review (transparent). For high-stakes operations, transparent rendering creates an audit trail that supports post-action review.
- **Transparent recommended for**: competitive responses where the team needs shared orientation; operations where AAR follows the cycle; cycles long enough to be worth writing down (hours+).

## Composes Well With

- `wrap-decision-framework` (use WRAP for the strategic decision; use OODA for the operational tempo of executing it)
- `after-action-review` (AAR feeds the Orient phase of the next OODA cycle by extracting structured lessons)
- `ecc-blueprint` (decompose multi-front situations into per-front OODA cycles)

## Composes Poorly With

- `feynman` (explanation, not decision tempo)
- `recursive-reasoning-operator` (verification shape — different cognitive task)
- `deep-sweep` (heavyweight analysis — incompatible with OODA cycle tempo)
- `llm-council` (heavyweight synthesis — too slow for OODA cycles)

## Notes

- Boyd never published the full theory in book form; the framework is reconstructed from briefings ("Patterns of Conflict") and interpreters (Coram, Osinga). The OODA loop is the most-cited element but the *Conceptual Spiral* and *Destruction and Creation* essays carry the deeper philosophy.
- Boyd's insight is widely shallowed into "decide faster." The actual claim is "out-orient your opponent." These are different.
- For business operators, OODA pairs naturally with feedback-cycle hygiene: short release cycles, observable customer behavior, fast post-action review. The framework rewards organizations whose architecture supports rapid orient-update.
