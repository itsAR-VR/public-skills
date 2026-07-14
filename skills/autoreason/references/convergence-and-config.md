# Convergence and Configuration — Ablation-Backed Rationale

Every parameter in autoreason was tested against alternatives in the paper. This reference explains **why** each default exists and **when** to deviate.

## The defaults (from `config_v2.yaml`)

Model IDs below are paper/config snapshots, not current-provider defaults. Last reviewed for this skill on 2026-06-10; refresh named Anthropic/OpenAI model IDs, prices, and context windows against current official docs before running or publishing updated recommendations.

```yaml
author_model: "anthropic/claude-sonnet-4-20250514"   # paper snapshot; replace with a currently verified model ID
judge_model:  "anthropic/claude-sonnet-4-20250514"
author_temperature: 0.8
judge_temperature: 0.3
max_tokens: 4096
num_judges: 3
max_passes: 50          # paper overrides to 30 in run_overnight.py
convergence_threshold: 2
```

## Convergence threshold (`k`)

### Why `k = 2`

The paper's convergence rule is: **A must win `k` consecutive rounds to converge.**

- `k = 1` (A wins once) is too weak: a lucky pass converges prematurely. The paper's trajectories show A often wins once, gets displaced, then wins again — `k=1` would stop at the first win.
- `k = 2` (default) is the stability check: A must survive two independent tournaments with different random shuffles and different Author-B outputs. If the same incumbent prevails twice against fresh adversaries, it's genuinely stable.
- `k ≥ 3` is used for **high-stakes artifacts** (brand voice, investor one-liner) where the cost of premature convergence is large. Adds ~2–5 passes on average.

### Observed trajectories

From the paper's illustrative trajectory (26 passes):
```
B → AB → A → B → AB → AB → A → B → A → AB → A → AB → A → A
                                                         ^^^^
                                                         converged
```
Note the displacement-recovery-displacement pattern. This is healthy — weak convergence rules would have stopped at pass 7 or pass 9.

## Number of judges

### Why `num_judges = 3` (default)

- **`1` judge**: noisy. A single model's biases dominate. The paper shows 1-judge runs produce inconsistent winners across Monte Carlo runs.
- **`3` judges**: paper default. Good cost/stability balance. Ties resolved by Borda.
- **`7` judges**: **3× faster convergence** than 3. Each judge is more likely to reach consensus, streaks build faster. Cost per pass is ~2.3× higher but total passes drop → often cheaper end-to-end.

### When to increase to 7

- Wall-clock is the binding constraint (running many tasks in parallel)
- You've observed verdict flapping with 3 judges
- The task is cheap per pass (short outputs) — the judge cost is small in absolute terms

### When NOT to drop below 3

- Never drop to 1 — Monte Carlo variance becomes unacceptable.
- `2` is degenerate — Borda needs an odd count to break natural ties.

## Temperature asymmetry

### Why `author = 0.8` and `judge = 0.3`

Different cognitive tasks want different variance:

| Role | Temp | Reason |
|------|------|--------|
| Author (A, B) | 0.8 | Diverse generation — maximize B ≠ A |
| Critic | 0.8 | Don't want every critic pointing at the same flaw |
| Synthesizer | 0.8 | Creative merging; low temp collapses to "return A" or "return B" |
| Judge | 0.3 | Stable, reproducible verdicts; flaky rankings defeat Borda |

Running all roles at a single temperature (paper ablation did not test this directly, but it's a common practitioner mistake) produces either:
- All at 0.8 → judges flip-flop, never converge
- All at 0.3 → B drifts too close to A, AB becomes bland, convergence is trivially fast but on a weaker output

## Max tokens

Default `4096`. Set to fit the expected output plus pre-ranking notes. For:
- One-liners / subject lines: 512 is plenty
- Landing copy: 1024
- Full proposals / briefs: 4096 (default)
- Long-form memos: 8192

Over-budgeting wastes cost; under-budgeting truncates critic/synthesizer outputs.

## Max passes (runaway protection)

Default `30` in `run_overnight.py` (config file lists 50, overridden by runner).

- Paper's longest observed convergence: **28 passes** (multi-stakeholder operational task)
- If you hit 30 without convergence: the task is genuinely too broad, or the knowledge layer is too thin for judges to discriminate.
- Do **not** blindly raise past 40 — past that point you're almost certainly in a judge-noise loop, not productive refinement.

## Tiebreak rule

Default `tiebreak_winner = "A"`. Load-bearing.

### What happens if you remove it

Random ties displace the incumbent. The streak resets. Convergence becomes stochastic. In Monte Carlo runs, some seeds converge in 10 passes and others in 40+ on the same task. The paper's convergence metrics all assume A-tiebreak.

### When to use a different tiebreak

Never, in the main loop. The only place tiebreak matters differently is the **5-way method comparison judge** where no candidate has "incumbent" status — there, ties can be broken by randomization or declared "inconclusive."

## Component ablations (why A, B, AB are all necessary)

Paper finding: **removing B or AB collapses the tournament.**

| Config | Convergence passes | Result |
|--------|--------------------|--------|
| Full (A, B, AB) | 24 (median) | Paper default |
| Only A vs B | 2–3 | Trivially converges — B usually loses to A because synthesizer advantage is gone |
| Only A vs AB | 2–3 | Trivially converges — AB often matches A because B isn't there to pull it away |
| Only B, AB (no incumbent) | diverges | No "do nothing" option → scope creep returns |

This is why the paper insists on all three. Don't skip B to save cost — you eliminate the mechanism.

## Judge aggregation ablations (why Borda, not majority)

Paper finding: **Borda > majority > first-place-only.**

- **First-place-only**: reduces to majority vote; AB (often 2nd place in many judge rankings) loses even when it's the broadly-preferred option.
- **Majority**: more ties than Borda; less discrimination; premature convergence from random majorities.
- **Borda**: uses full ordering; stable across judge counts; distinguishes "narrow but strong" (AB often winning on breadth) from "wide but shallow" (A often winning on familiarity).

## Length-controlled evaluation (paper finding)

The paper's length-controlled ablation: judges scored outputs blind to length, only comparing against a matched-word-count reference. Autoreason still won **21 of 28 comparisons** — meaning the gains are not just from writing more words. This matters for tasks like one-liners or subject lines where longer is not better.

## Model-tier considerations

These model-tier names and results are preserved from the paper/source snapshot, not asserted as current provider catalog truth. Re-check current official Anthropic/OpenAI docs before mapping the guidance to today's model IDs.

Paper results across model tiers on code tasks (150 CodeContests problems, private test):

| Model | Single-pass | Autoreason |
|-------|-------------|------------|
| Haiku 3.5 | low 30s% | **40%** |
| Haiku 4.5 | ~60% | ~60% (**transition point — gap closes**) |
| Sonnet 4 | ~60% | **64%** |
| Sonnet 4.6 | 73% | **77%** |

### Implications for your choice of model

- **Haiku 3.5 / early-generation models in the paper**: autoreason is a **large** multiplier. 42/42 perfect Borda sweep on writing tasks.
- **Haiku 4.5 / small-model tier in the paper**: gains shrink. Generation-evaluation gap has closed for some tasks — the single-pass answer is already near optimum.
- **Sonnet 4.6 / frontier tier in the paper**: autoreason still adds points (4 points on code), but the cost-benefit is task-dependent.

**Practical rule**: autoreason is most valuable on models where you notice the single-pass draft has clear flaws but the model has the capacity to identify and revise them. For the strongest frontier models on their strongest tasks, the loop is often overkill.

## Rate-limit and retry strategy

Exponential backoff with jitter:
```python
for attempt in range(max_retries):
    try:
        return await llm_call(...)
    except (RateLimitError, OverloadedError):
        wait = min((2 ** attempt) * 5, 120)
        await asyncio.sleep(wait)
```

The paper's runner uses `max_retries = 8`, cap at 120s. With 3 judges in parallel + author/critic/synthesizer sequentially per pass, a 20-pass run at ~60s per pass takes ~20 minutes wall-clock under ideal conditions, 30-40 minutes with rate-limit retries.

## Cost model (rough)

Per pass:
- 1× critic call (~500 tokens in + output)
- 1× author B call (~task + A + critique in + full output out)
- 1× synthesizer call (~task + A + B in + full output out)
- N× judge calls (~task + A + B + AB in + ~200 tokens out)

Total tokens per pass scales as:
```
cost_per_pass ≈ 3 × (task + proposal_size) + N × (task + 3 × proposal_size + 200)
```

For a 2000-token task and 1500-token proposals with 3 judges: ~20k input + 8k output tokens per pass. Over 20 passes: ~400k input / 160k output. Using a dated 2026-06 paper-era Sonnet 4.5 price example (~$3 / MTok in, $15 / MTok out), that's ~$1.20 input + $2.40 output = **~$3.60 per converged run**. Recalculate with current provider pricing before quoting this externally.

In the same dated price snapshot, Haiku 4.5 was ~10× cheaper. For the paper's 42/42 Haiku 3.5 sweep, per-task cost was roughly $0.30–0.50.

## When autoreason is the wrong tool (revisited)

- **You have a metric.** Use `autoresearch`. Stop reading here.
- **Single-shot task.** Just answer the question.
- **You're doing research.** Use `deep-research` / `autoresearch` not autoreason.
- **The incumbent doesn't exist yet.** Generate A first with a normal prompt; then enter autoreason if refinement is warranted.
- **You're refining code that has tests.** Use the tests as the metric → autoresearch. Autoreason is for *subjective* tasks.
