---
name: autoreason
description: >
  Run a tournament-style self-refinement loop for subjective tasks that have no
  clean metric. Use when the user asks to refine positioning, landing-page copy,
  ad briefs, brand voice, email subject lines, pitch decks, or any proposal where
  "better" is a judgment call. Four fresh isolated agents per pass (critic, author
  B, synthesizer, 3+ blind judges) compete the incumbent A against a revision B
  and a synthesis AB via Borda count; converge when A wins twice. Differs from
  autoresearch (numeric metric) — use this when the only judge is taste.
  For autonomous ML experiments with a measurable metric, see autoresearch.
  For deterministic critique of code/prose, see impeccable critique.
metadata:
  author: contributor
  version: 1.0.0
  source: "NousResearch/autoreason (SHL0MS + Hermes Agent, 2026)"
related_skills: [autoresearch, impeccable, hormozi-offers, copywriting, writers-studio, content-research-writer]
---

# Autoreason — Adversarial Self-Refinement for Subjective Tasks

Iterative self-refinement on LLMs usually makes things **worse**. Models hallucinate flaws to satisfy critique prompts, each pass expands scope unchecked, and they almost never decline to change anything. Autoreason fixes all three by making "do nothing" a first-class option, running the critic/author/synthesizer/judges as **fresh isolated agents with no shared context**, and terminating only when the output is genuinely stable.

**Paper source**: https://github.com/NousResearch/autoreason (SHL0MS + Hermes Agent, 2026; model claims last reviewed for this skill on 2026-06-10). In the paper snapshot, Haiku 3.5 + autoreason scored 42/42 perfect Borda across 3 tasks; every standard refinement baseline **degraded** the same model's single-pass output. Refresh named model IDs, pricing, and context-window claims against current official provider docs before treating them as current recommendations.

## When to Use

- User asks to refine **positioning**, value prop, one-liner, mission statement
- User asks to **sharpen landing-page copy**, ad brief, or email subject line
- User asks to **develop brand voice** or tone rules
- User asks to **shape a pitch deck**, proposal, or investor memo
- User says "make this better" on a subjective artifact and the previous single-pass draft is weak
- User references "autoreason", "tournament refinement", "adversarial review", or "Nous autoreason"
- The task has **no metric** (no pass rate, no CTR target, no held-out test) — only taste

## When NOT to Use

- **The task has a metric.** Use `autoresearch` instead (Karpathy-style keep/discard loop).
- **Single-shot task.** One-off code fix, one-off factual answer — just answer.
- **The incumbent is unknown.** Autoreason compares candidates; if A doesn't exist, generate A first with a normal prompt.
- **You want deterministic critique, not competition.** Use `impeccable critique`.
- **Tiny model (<paper Haiku-class).** The paper shows refinement **destroys** weak models (59–70% word-count collapse over 15 passes of critique-and-revise). Use a currently verified small-frontier-or-stronger model tier; do not rely on stale named model IDs.

## The Loop (One Pass)

```
Task Prompt → Incumbent A (current best)
                  │
                  ├── Critic (fresh agent, reads A only) ──────→ Critique
                  │
                  ├── Author B (fresh, reads task + A + critique) → Revision B
                  │
                  └── Synthesizer (fresh, reads task + A + B) ──→ Synthesis AB
                                        │
                                        ▼
                  Judge Panel (3 or 7 fresh blind judges, Borda rank)
                                        │
                                        ▼
                            Winner becomes new A
                                        │
                   ┌────────────────────┴───────────────────┐
                   ▼                                         ▼
             A wins k=2 in a row? → DONE            Otherwise → loop
```

Every role is a **fresh isolated agent**: no system/chat history, no access to sibling outputs or private notes. The critic never sees the author's change notes; judges never see the critic's list.

## Authoritative Config (from the paper)

| Parameter | Value | Why |
|-----------|-------|-----|
| `author_temperature` | **0.8** | High variance → B meaningfully differs from A |
| `judge_temperature` | **0.3** | Low variance → stable, reproducible verdicts |
| `max_tokens` | 4096 | Fits a proposal; increase for long docs |
| `num_judges` | **3** (default) / **7** (faster) | 7 judges → 3× faster convergence; 1 judge is noisy |
| `convergence_threshold` | **2** | A must prevail twice consecutively |
| `max_passes` | **30** | Cap runaway loops (paper never needed >28) |
| `tiebreak_winner` | **"A"** | Ties keep the incumbent — no churn |

See [references/convergence-and-config.md](references/convergence-and-config.md) for rationale and ablation results.

## Workflow — Running Autoreason by Hand

Use this when the user wants **you** (Claude, one session) to drive autoreason via sub-agents. For a headless batch run across many tasks, use [scripts/autoreason.py](scripts/autoreason.py) instead.

### Step 0 — Clarify the task

Before generating A, confirm:
- **Task prompt** (verbatim, short — the same string goes to every role)
- **Constraints** (word count, sections, tone, audience)
- **Knowledge layer?** If the user has campaign data / brand rules / competitor positioning, load it into `references/` and tell the critic + judges to ground criticism and verdicts in it. See [references/knowledge-layer.md](references/knowledge-layer.md).

### Step 1 — Generate Incumbent A

Use the **Author** system prompt and the task prompt. Temperature 0.8. Save as `pass_00/version_a.md`.

### Step 2 — For each pass (1..N):

Dispatch in parallel (the critic, author B, and synthesizer have no dependencies on one another's outputs — only on A and the task):

1. **Critic** (fresh Agent) — reads A only, produces critique. **Must not propose fixes.**
2. Wait for critic, then:
3. **Author B** (fresh Agent) — reads task + A + critique, writes a full revision addressing each flaw. **Must justify every change against a named flaw.**
4. **Synthesizer** (fresh Agent) — reads task + A + B (order randomized per call), picks best-per-section. **Not a compromise — pick, don't average.**

Then run the judge panel:

5. **Judges** (3 or 7 fresh Agents in parallel) — each sees A, B, AB **relabeled as Proposal 1/2/3 in randomized order**. Each returns `RANKING: <best>, <second>, <worst>`.
6. **Borda aggregate**: each 1st = 3pts, 2nd = 2pts, 3rd = 1pt. Sum across judges. Highest total wins. **Ties → A wins.**

### Step 3 — Update incumbent

- If **winner == A**, `streak += 1`.
- Else `streak = 0`, `current_a = winner_text`.
- If `streak >= 2`, **converged** — write `final_output.md` and stop.
- Else loop.

See [references/agent-prompts.md](references/agent-prompts.md) for the exact verbatim prompts used in the paper. Use them literally — they were tuned to prevent prompt bias (critic-hallucinating-flaws) and scope creep.

## Knowledge Layer (Strongly Recommended for Marketing/Copy)

Without data, the loop debates from general copywriting principles. With data, it debates from **your results**. Feed the critic and judges:

1. **Past campaign performance** — open rates, CTR, conversion by segment, revenue
2. **Winning vs losing copy** — the 38% subject line next to the 12% one
3. **Audience research** — reviews, support tickets, Reddit threads, call transcripts
4. **Competitor positioning** — how rivals describe themselves; where you overlap
5. **Brand voice rules** — specific words, tone, patterns that sound like you

The critic can now say *"this reads like the subject lines that averaged 12% for us, not the 38% ones"* instead of arguing from gut feel. Results from each run **feed back into the knowledge layer** — the loop gets sharper every campaign.

Template at [references/knowledge-layer.md](references/knowledge-layer.md).

## Examples

### Example 1: Product positioning refinement

**User says:** "Sharpen my product positioning for this dev tool. Here's the current draft: [...]"

**Actions:**
1. Treat the user's draft as `incumbent_A`. Save verbatim.
2. Ask for competitors' positioning + any analytics (lands it in knowledge layer).
3. Dispatch parallel agents per pass 1: critic + (after critic) author B + synthesizer.
4. Run 3 blind judges with randomized labels; Borda score.
5. Repeat until A wins twice. Expect **~10 passes** for positioning (paper finding).
6. Output final positioning + trajectory (`A → B → AB → A → A`).

**Result:** A positioning statement that has survived adversarial review, not just a single model's first-take-plus-polish. User sees the trajectory — which pass displaced the original, which synthesis survived.

### Example 2: Email subject line tournament with performance data

**User says:** "I have a list of past email subject lines with open rates. Use autoreason to draft a new subject for this launch."

**Actions:**
1. Load open-rate CSV into a knowledge-layer summary (`top decile` vs `bottom decile` patterns).
2. Generate A with author prompt + "Match the patterns of the 38%+ open-rate set."
3. Critic gets the same knowledge layer and is told: **"Flag anything that pattern-matches the <20% set."**
4. Judges get the knowledge layer and are told: **"Rank by likelihood of beating the historical top-decile."**
5. Run until convergence. With a knowledge layer this tight, expect convergence in 5–8 passes.

**Result:** Subject line grounded in the user's actual data, not generic principles. Performance of the winning line feeds back into the dataset for the next run.

### Example 3: Converting an existing CLAUDE.md block into autoreason

**User says:** "We have a mission statement that's been through 10 rounds of internal edits — can autoreason tell us if it's stable?"

**Actions:**
1. Load mission statement as A.
2. Run autoreason with convergence_threshold=3 (higher bar — user is checking for stability, not searching).
3. If A wins 3 rounds immediately, report: **stable, no changes warranted**.
4. If A loses any round, report the flaw the critic found and the B/AB alternative.

**Result:** Either confirmation that the mission statement has earned its stripes, or a concrete alternative with documented critique.

## Common Failure Modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| B is always nearly identical to A | Critic is suggesting fixes instead of just problems | Use the exact critic prompt in `references/agent-prompts.md` — it forbids proposing fixes |
| Convergence happens in 2–3 passes every time | Missing B or AB from the panel — collapses the tournament | The paper ablation confirms: **both B and AB are necessary**. Don't skip. |
| Judges flip-flop every pass | Judge temperature too high or single judge | Use 3+ judges at temp 0.3; go to 7 judges if still noisy (3× faster convergence) |
| Output gets longer every pass (scope creep) | You're running a baseline (critique-and-revise), not autoreason | Autoreason's "do nothing" option + blind judges prevent this. Check you're running the full tournament. |
| Never converges within 30 passes | Task is genuinely too broad, or judges can't distinguish | Add knowledge layer; increase judges to 7; tighten task prompt with harder constraints |
| Weak model (<paper Haiku 3.5 tier) produces degraded output | Small models can't self-critique reliably | Per paper: refinement destroys weak models. Upgrade to a currently verified stronger model tier. |
| A judge returns no `RANKING:` line | Parse failure; judge went off-script | Retry with a fresh call; drop that judge's vote if repeat failure (Borda handles missing judges) |

## Convergence Expectations (from paper)

| Task type | Typical passes to converge |
|-----------|---------------------------|
| Simple policy / positioning | ~10 |
| Open-ended writing | 15–20 |
| Multi-stakeholder operational | up to 28 |
| Something broke if… | >30 (hit the cap) |

A trajectory like `B → AB → A → B → AB → AB → A → A` is **normal** — incumbents get displaced, recover, get displaced again; convergence is when the output is genuinely stable, not when the model runs out of things to say.

## Related Skills

- **autoresearch** — Karpathy's original loop, for tasks that **have** a numeric metric (val_bpb, pass rate, conversion). Autoreason is its subjective-domain cousin.
- **impeccable critique** — one-shot adversarial critique (not a tournament loop). Use when you just want a single critic pass, not convergence.
- **hormozi-offers / hormozi-hooks / copywriting** — good sources for the knowledge layer when refining marketing copy.
- **writers-studio / content-research-writer** — can generate the Incumbent A before handing off to autoreason.
- **brainstorm** (superpowers) — different purpose: explore the solution space. Autoreason refines a chosen direction.

## Reference Implementation

A runnable reference implementation is at [scripts/autoreason.py](scripts/autoreason.py). It uses the `openai` SDK (per project preference — direct SDK, no AI Gateway) with configurable model, runs critic/author-B/synthesizer sequentially per pass, dispatches judges in parallel, and handles rate-limit retries with exponential backoff.

Paper code (LiteLLM + Anthropic) is at [NousResearch/autoreason/experiments/v2/run_overnight.py](https://github.com/NousResearch/autoreason/blob/main/experiments/v2/run_overnight.py) — the reference implementation faithfully mirrors its prompts and Borda logic.

## Citation

```
@article{shl0ms2026autoreason,
  title={Autoreason: Self-Refinement That Knows When to Stop},
  author={SHL0MS and Hermes Agent},
  year={2026},
  url={https://github.com/NousResearch/autoreason}
}
```
