# GSD Research Layer — Deep Reference

Absorbed from GSD's parallel-research pattern. Slots into deep-sweep as Phase 0.5 — between problem-set definition and primary-model analysis.

## Why parallel

Sequential research contaminates itself: later researchers anchor on earlier findings. Parallel researchers each see ONLY the problem set + their lens, so their outputs are independent signals that the synthesizer combines.

This is the same principle as between-model diversity in LLM Council — isolate each perspective, then aggregate.

## The five lenses

| Lens | Agent | What it looks for |
|------|-------|-------------------|
| Stack / framework | `gsd-framework-selector` | Which stack/framework fits, version constraints, ecosystem maturity |
| Features / phase | `gsd-phase-researcher` | Domain-specific patterns for the feature being built |
| Architecture / patterns | `gsd-pattern-mapper` | Architectural fit, anti-patterns to avoid, structural constraints |
| Pitfalls / assumptions | `gsd-assumptions-analyzer` | Hidden assumptions that would break if wrong |
| Prior art | `gsd-advisor-researcher` | Battle-tested implementations to borrow from |

## Agent prompt templates

### Framework lens

```
You are the framework/stack researcher. Given the problem set below, identify:
- Recommended stack (with version)
- Tradeoffs vs. alternatives
- Ecosystem health (maintenance, security, community)
- Hard constraints (platform, license, deployment target)

<problem_set>
{P1..PN from Phase 0}
</problem_set>

Return: structured brief with evidence and confidence per recommendation.
Do NOT assume other research outputs exist yet — your brief is standalone.
```

### Phase-researcher lens

```
You are the feature/domain deep-dive researcher. Given the problem set, investigate:
- Domain-specific patterns (how is this class of problem typically solved?)
- Failure modes in this domain
- Observable metrics that indicate success/failure
- Edge cases the problem statement may miss

<problem_set>
{P1..PN}
</problem_set>

Return: domain brief with concrete examples, references, and open questions.
```

### Pattern-mapper lens

```
You are the architecture/pattern researcher. Given the problem set and the codebase context, identify:
- Architectural patterns that fit
- Anti-patterns to avoid
- Structural constraints from existing code (coupling, module boundaries)
- Tradeoffs between patterns

<problem_set>
{P1..PN}
</problem_set>

<codebase_context>
{graphify god nodes + gitnexus impact for key symbols}
</codebase_context>

Return: pattern recommendations with structural rationale.
```

### Assumptions-analyzer lens

```
You are the assumptions auditor. Given the problem set, surface:
- Hidden assumptions (things taken as true without evidence)
- Invalidating conditions (what would make this problem unsolvable?)
- Missing context (what does the plan need to know that isn't in the problem statement?)

<problem_set>
{P1..PN}
</problem_set>

<user_request_verbatim>
{original user prompt}
</user_request_verbatim>

Return: ranked list of assumptions by plan-invalidating impact, with verification steps.
```

### Advisor lens

```
You are the prior-art researcher. Given the problem set, find 2-3 battle-tested implementations to learn from or adopt:
- Open-source projects that solve ≥80% of this problem
- Canonical patterns from library/framework docs
- Production case studies

<problem_set>
{P1..PN}
</problem_set>

Preference: adopt over build. Return: comparison table (approach, effort-to-adopt, tradeoffs) + recommendation.
```

## Synthesis prompt

```
You are the research synthesizer. Merge the five research briefs below into a consolidated document.

<framework_brief>...</framework_brief>
<phase_brief>...</phase_brief>
<patterns_brief>...</patterns_brief>
<assumptions_brief>...</assumptions_brief>
<advisor_brief>...</advisor_brief>

Produce docs/planning/phase-{N}/research-brief.md with sections:

1. **Unified narrative** — what the research tells us about the problem set
2. **Agreement / disagreement** — where the lenses converge and diverge (divergence is often the most interesting signal)
3. **Recommended approach** — with tradeoffs, confidence, and fallback options
4. **Open questions** — anything that needs user input before planning proceeds
5. **Upstream issues** — anything that would change the problem framing itself (escalate these)

Length: 400-800 words. Favor structured tables for comparison. Cite which brief each claim comes from.
```

## Integration with Phase 1 Primary-Model Agents

After the research brief is written, every Phase 1 primary-model agent's prompt must include:

```
<research_brief>
@docs/planning/phase-{N}/research-brief.md
</research_brief>
```

This gives primary-model agents the synthesized context BEFORE they do their deep analysis, so they don't duplicate research or make framework/pattern choices that contradict the brief.

## Skip criteria (detailed)

Skip Phase 0.5 ONLY when all of these hold:
- Problem is self-contained (no "what framework?" or "what pattern?" questions)
- Domain is well-understood and recently worked in (last ~14 days of conversation)
- Speed matters more than thoroughness (quick patch, not new feature)
- No risk of unknown unknowns (mature codebase, familiar territory)

Do NOT skip for:
- First phase of a new project
- New domain (even for experienced teams)
- Auth, payments, or data migration
- Anything that touches production schemas
- Anything the user said "I'm not sure how to approach this" about

## Failure modes

- **Researcher timeout** — if any researcher hasn't returned in reasonable time, proceed with a noted gap. The synthesizer should flag the missing lens.
- **Contradictory findings** — surface as `## Disagreement` in the synthesis. Don't force consensus.
- **Upstream issues surfaced** — if any researcher finds something that changes the problem framing (e.g., "this class of problem is unsolvable in this framework"), STOP and escalate to user before Phase 1.

## Related

- `procedure.md` — base deep-sweep procedure
- `agent-prompts.md` — Phase 1+ primary-model prompts (must include research-brief)
- `~/.claude/get-shit-done/references/` — authoritative GSD patterns
- `phase-plan` skill — light research subroutines for planning (not deep-sweep's heavy wave)
