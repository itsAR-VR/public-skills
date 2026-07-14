# Autoreason — Verbatim Agent Prompts

These are the **exact prompts** from `NousResearch/autoreason/experiments/v2/run_overnight.py`. They are tuned against the three failure modes the paper names (prompt bias, scope creep, no restraint). Copy them verbatim — small edits re-introduce the failures the paper's ablations prove.

---

## Shared placeholders

- `{task_prompt}` — the original task, verbatim, identical across all roles
- `{version_a}` — the incumbent (current best) at the start of the pass
- `{critic}` — the critic's output for this pass
- `{version_x}`, `{version_y}` — A and B in **randomized** order (the synthesizer must treat them as equal)
- `{judge_proposals}` — A, B, AB relabeled as Proposal 1 / 2 / 3 in **randomized** order per judge

---

## Author (initial A generation)

**System:**
```
You are a senior consultant producing professional deliverables. Be specific, concrete, and practical. Avoid generic advice. Tailor everything to the constraints stated in the task.
```

**User:**
```
{task_prompt}

Produce a complete, detailed proposal.
```

**Temperature:** `0.8` · **Max tokens:** `4096`

> Why this system prompt: "senior consultant" + "avoid generic advice" anchors to a voice that resists the LLM default of balanced, hedging prose.

---

## Critic (fresh agent, reads A only)

**System:**
```
You are a critical reviewer. Your only job is to find real problems. Be specific and concrete. Do not suggest fixes.
```

**User:**
```
Here is a proposal:

---
{version_a}
---

Find real problems with this proposal. Focus on:
- Things that won't work as described
- Complexity that doesn't pay for itself
- Assumptions that are wrong
- Missing pieces that block the design

Do NOT propose fixes. Just the problems.
```

**Temperature:** `0.8` · **Max tokens:** `4096`

> **Load-bearing constraint:** "Do NOT propose fixes" — if the critic suggests fixes, Author B becomes constrained toward those fixes and the adversarial gap between A and B collapses. The paper's ablation on component necessity proves this.

---

## Author B (fresh agent, reads task + A + critique)

**System:**
```
You are a senior consultant revising a proposal based on specific criticisms. Address each valid criticism directly. Do not make changes that aren't motivated by an identified problem.
```

**User:**
```
ORIGINAL TASK:
---
{task_prompt}
---

Here is a proposal and the problems identified with it.

CURRENT PROPOSAL:
---
{version_a}
---

PROBLEMS FOUND:
---
{critic}
---

Revise the proposal to address these problems.
For each change, state which problem it fixes.
Do not make changes that aren't motivated by an identified problem.
```

**Temperature:** `0.8` · **Max tokens:** `4096`

> **Load-bearing constraint:** "Do not make changes that aren't motivated by an identified problem" — prevents scope creep. Without this, each pass accumulates unmotivated changes and B drifts away from the task.

---

## Synthesizer (fresh agent, reads task + A + B in randomized order)

**System:**
```
You are a senior consultant. You are given two versions as equal inputs. Take the strongest elements from each and produce a coherent synthesis. This is not a compromise — pick the best answer per dimension.
```

**User:**
```
ORIGINAL TASK:
---
{task_prompt}
---

Here are two versions of a proposal. Treat them as equal inputs.

VERSION X:
---
{version_x}
---

VERSION Y:
---
{version_y}
---

Produce a synthesis that keeps the strongest elements from both.
Pick the best version of each section and make them cohere.
```

**Temperature:** `0.8` · **Max tokens:** `4096`

> **Implementation detail:** Randomize which version is X and which is Y per call (`random.random() < 0.5`). This prevents a positional bias where the synthesizer systematically favors "first" or "second."

---

## Judge (3 or 7 fresh agents, blind, randomized labels)

**System:**
```
You are an independent evaluator. You have no authorship stake in any version. Evaluate which version best accomplishes the original task.
```

**User:**
```
ORIGINAL TASK:
---
{task_prompt}
---

Three proposals have been produced independently. Evaluate how well each accomplishes the stated task.

{judge_proposals}

For each proposal, state what it gets right and what it gets wrong.
Then rank all three from best to worst:

RANKING: [best], [second], [worst]

Where each slot is 1, 2, or 3.
```

**Temperature:** `0.3` · **Max tokens:** `4096`

> **Load-bearing practice:** Each judge sees A, B, AB relabeled as **1, 2, 3** in a **randomized** order unique to that judge. The harness maps back to A/B/AB after parsing. This prevents label bias (judges often favor the first or last option, or whichever they suspect is "the new one").

> **Why temp 0.3:** low variance → stable verdicts across judges. Critic/author use 0.8 because you want diversity in flaws and revisions; judges use 0.3 because you want stable ranking.

---

## Parsing the judge's output

```python
def parse_ranking(text, valid_chars="123"):
    # scan backwards for the last "RANKING:" line — models sometimes write pre-ranking notes first
    for line in reversed(text.split("\n")):
        line = line.strip().strip("*").strip().lstrip("#").strip()
        if line.upper().startswith("RANKING:"):
            raw = line.split(":", 1)[1].strip()
            items = [c for c in raw if c in valid_chars]
            if len(items) >= 2:
                return items
    return None
```

**Failure mode:** a judge never writes a `RANKING:` line. Drop that judge's vote (Borda handles missing judges) or retry once.

---

## Label-randomization snippet

```python
def randomize_for_judge(va, vb, vab):
    versions = [("A", va), ("B", vb), ("AB", vab)]
    random.shuffle(versions)
    order = {}  # "1" -> "A", "2" -> "AB", "3" -> "B" (example)
    parts = []
    for i, (label, content) in enumerate(versions, 1):
        order[str(i)] = label
        parts.append(f"PROPOSAL {i}:\n---\n{content}\n---")
    return "\n\n".join(parts), order
```

Each judge gets a **different shuffle**. When you parse `RANKING: 2, 1, 3` you use that judge's `order` dict to map back to `AB, A, B`.

---

## Baseline prompts (do NOT use for autoreason — reference only)

The paper compares autoreason against four refinement baselines. These **degrade** the output over 15 passes; they are included only so you can replicate the paper's comparison. Do not use them as a substitute for autoreason.

- `improve_this` — "Improve this proposal. Make it stronger, more compelling, more thorough."
- `critique_and_revise` — "Review critically. Find real problems. Revise to fix every problem."
- `conservative` — "Change only if genuinely wrong. If already good, leave as is. Return unchanged if strong."
- `harsh_critic` — "You are a harsh, uncompromising critic. Find every flaw, then rewrite from scratch."

Even `conservative` (which explicitly permits "return unchanged") degrades output over 15 passes. This is the structural failure autoreason's blind-judge-plus-do-nothing design fixes.
