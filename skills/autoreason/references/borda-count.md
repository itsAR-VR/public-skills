# Borda Count — Scoring, Ties, and Anti-Bias

The judge panel aggregates rankings via **Borda count**, not majority vote. This reference explains why, how the paper implements it, and the tie / missing-judge rules.

## Why Borda, not majority

A majority-vote aggregation asks each judge "which single one is best?" This throws away information: a judge who ranks A > AB > B tells you something different from a judge who ranks A > B > AB, and majority vote treats them as identical ("A wins").

Borda count uses the full ranking:
- 1st place → 3 points (for a 3-way tournament)
- 2nd place → 2 points
- 3rd place → 1 point

Summed across judges. The highest total wins. The paper's ablation replacing Borda with majority shows majority voting **reduces discrimination** — ties become more common, and AB (the synthesis) wins less often because it tends to be many judges' 2nd choice (high Borda, low majority).

## The scoring formula (verbatim from the paper's code)

```python
def aggregate_rankings(rankings, labels, tiebreak_winner=None):
    scores = {l: 0 for l in labels}  # {"A": 0, "B": 0, "AB": 0}
    n = len(labels)  # 3
    valid = [r for r in rankings if r is not None]
    for ranking in valid:
        for pos, label in enumerate(ranking):
            if label in scores and pos < n:
                scores[label] += (n - pos)  # pos 0 → 3pts, pos 1 → 2pts, pos 2 → 1pt
    if tiebreak_winner:
        priority = {l: (0 if l == tiebreak_winner else i+1) for i, l in enumerate(labels)}
    else:
        priority = {l: i for i, l in enumerate(labels)}
    ranked = sorted(scores.keys(), key=lambda k: (-scores[k], priority[k]))
    return ranked[0], scores, valid
```

## Tie rule: incumbent keeps its seat

`tiebreak_winner="A"` is the canonical setting. When two candidates tie on Borda points, the incumbent wins. This is **load-bearing**:

- Without it, random noise displaces the incumbent → infinite churn → never converges
- With it, displacement must come from a clear judge preference, not a tie

If the paper ran with `tiebreak_winner=None`, convergence would take longer and trajectories would be noisier. The paper does not use this setting in any ablation.

## Missing-judge handling

A judge that fails to return a parseable `RANKING:` line contributes nothing to the Borda totals. The remaining judges still vote. With 3 judges and one failure, you fall back to 2 — still deterministic Borda, slightly more noisy.

If **all** judges fail to parse, retry the pass. Do not pick a winner from zero rankings.

## Worked example

Three judges rank three candidates A, B, AB:

| Judge | 1st | 2nd | 3rd |
|-------|-----|-----|-----|
| 1 | AB | A | B |
| 2 | A | AB | B |
| 3 | AB | B | A |

Borda totals:
- A: 2 + 3 + 1 = **6**
- B: 1 + 1 + 2 = **4**
- AB: 3 + 2 + 3 = **8**

Winner: **AB** (synthesis). A gets displaced, current_a ← AB, streak resets to 0.

## Judge-count tradeoff

From the paper's ablations:

| Judges | Behavior |
|--------|----------|
| 1 | Noisy, slow convergence; single judge's biases dominate |
| 3 | Paper default. Good balance of cost and stability. |
| 7 | **3× faster convergence** than 3 (more votes resolve ties earlier) |

If you're cost-sensitive, stay at 3. If you're convergence-speed-sensitive (or running many tasks in parallel where wall-clock matters more than per-task judge cost), use 7. The paper's main results use 3.

## 5-way judge (for method comparison, not the main loop)

When comparing **methods** (autoreason vs critique-and-revise vs improve-this vs harsh-critic vs single-pass), the paper uses a 7-judge panel with a 5-point Borda:

- 1st = 5 pts, 2nd = 4, 3rd = 3, 4th = 2, 5th = 1

Labels A–E are randomized per judge. This is the `run_5way_judge` function in `run_overnight.py`. You only need this if you're running a bake-off between methods, not for the autoreason main loop itself.

## Anti-bias: label randomization (recap)

Even with Borda, a judge may prefer whichever candidate appears first or last. The paper mitigates this by showing each judge **its own random shuffle** of A, B, AB as Proposal 1 / 2 / 3. The harness records each judge's order and maps `RANKING: 2, 1, 3` back to the real labels per judge before summing Borda.

Skipping the shuffle causes position bias → incumbent gets systematically displaced (or systematically defended) based on where you happen to place it.
