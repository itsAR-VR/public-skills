#!/usr/bin/env python3
"""
Autoreason — reference implementation.

Adversarial self-refinement for subjective tasks. Runs the tournament loop
(critic → author B → synthesizer → blind judge panel via Borda count) until
the incumbent A wins k=2 consecutive rounds.

Based on NousResearch/autoreason (SHL0MS + Hermes Agent, 2026).
Prompts are the paper's verbatim prompts.

Pass --model explicitly, or set OPENAI_LATEST_MODEL / ANTHROPIC_LATEST_MODEL
after checking current official provider docs. The script refuses to guess a
volatile provider model ID.
OpenAI and Anthropic work via --provider.

Usage:
  python autoreason.py --task task.md --out runs/positioning_01
  python autoreason.py --task task.md --out runs/positioning_01 \\
      --provider openai --model "$OPENAI_LATEST_MODEL" --judges 7 --max-passes 30

Environment:
  OPENAI_API_KEY       (for --provider openai)
  OPENAI_LATEST_MODEL  (OpenAI model id verified at execution time)
  ANTHROPIC_API_KEY       (for --provider anthropic)
  ANTHROPIC_LATEST_MODEL  (Anthropic model id verified at execution time)
"""

import argparse
import asyncio
import json
import os
import random
import sys
import time
from pathlib import Path

# ── Verbatim paper prompts ─────────────────────────────────────────────

AUTHOR_SYSTEM = (
    "You are a senior consultant producing professional deliverables. "
    "Be specific, concrete, and practical. Avoid generic advice. "
    "Tailor everything to the constraints stated in the task."
)

CRITIC_SYSTEM = (
    "You are a critical reviewer. Your only job is to find real problems. "
    "Be specific and concrete. Do not suggest fixes."
)

AUTHOR_B_SYSTEM = (
    "You are a senior consultant revising a proposal based on specific criticisms. "
    "Address each valid criticism directly. Do not make changes that aren't "
    "motivated by an identified problem."
)

SYNTHESIZER_SYSTEM = (
    "You are a senior consultant. You are given two versions as equal inputs. "
    "Take the strongest elements from each and produce a coherent synthesis. "
    "This is not a compromise — pick the best answer per dimension."
)

JUDGE_SYSTEM = (
    "You are an independent evaluator. You have no authorship stake in any "
    "version. Evaluate which version best accomplishes the original task."
)

GENERATE_A = "{task_prompt}\n\nProduce a complete, detailed proposal."

CRITIC_PROMPT = """Here is a proposal:

---
{version_a}
---

Find real problems with this proposal. Focus on:
- Things that won't work as described
- Complexity that doesn't pay for itself
- Assumptions that are wrong
- Missing pieces that block the design

Do NOT propose fixes. Just the problems."""

AUTHOR_B_PROMPT = """ORIGINAL TASK:
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
Do not make changes that aren't motivated by an identified problem."""

SYNTHESIZER_PROMPT = """ORIGINAL TASK:
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
Pick the best version of each section and make them cohere."""

JUDGE_RANK_3_PROMPT = """ORIGINAL TASK:
---
{task_prompt}
---

Three proposals have been produced independently. Evaluate how well each accomplishes the stated task.

{judge_proposals}

For each proposal, state what it gets right and what it gets wrong.
Then rank all three from best to worst:

RANKING: [best], [second], [worst]

Where each slot is 1, 2, or 3."""

# ── LLM wrapper (provider-agnostic) ────────────────────────────────────


class LLMClient:
    """Minimal provider abstraction. Defaults to OpenAI (project preference)."""

    def __init__(self, provider: str, model: str):
        self.provider = provider
        self.model = model
        if provider == "openai":
            from openai import AsyncOpenAI
            self.client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
        elif provider == "anthropic":
            from anthropic import AsyncAnthropic
            self.client = AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        else:
            raise ValueError(f"Unknown provider: {provider}")

    async def call(
        self,
        system: str,
        user: str,
        temperature: float,
        max_tokens: int,
        max_retries: int = 8,
    ) -> str:
        for attempt in range(max_retries):
            try:
                if self.provider == "openai":
                    resp = await self.client.chat.completions.create(
                        model=self.model,
                        messages=[
                            {"role": "system", "content": system},
                            {"role": "user", "content": user},
                        ],
                        temperature=temperature,
                        max_tokens=max_tokens,
                    )
                    return resp.choices[0].message.content
                else:  # anthropic
                    resp = await self.client.messages.create(
                        model=self.model,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        system=system,
                        messages=[{"role": "user", "content": user}],
                    )
                    return resp.content[0].text
            except Exception as e:
                err = str(e).lower()
                transient = any(
                    k in err for k in ("rate", "429", "overloaded", "529", "timeout")
                )
                if attempt < max_retries - 1 and transient:
                    wait = min((2 ** attempt) * 5, 120)
                    print(f"      [retry {attempt+1}/{max_retries} in {wait}s: {str(e)[:80]}]")
                    await asyncio.sleep(wait)
                elif attempt < max_retries - 1:
                    await asyncio.sleep(10)
                else:
                    raise
        raise RuntimeError(f"Failed after {max_retries} retries")


# ── Judge helpers ──────────────────────────────────────────────────────


def randomize_for_judge(va: str, vb: str, vab: str):
    """Shuffle A/B/AB and relabel as Proposal 1/2/3. Returns (text, order-dict)."""
    versions = [("A", va), ("B", vb), ("AB", vab)]
    random.shuffle(versions)
    order = {}
    parts = []
    for i, (label, content) in enumerate(versions, 1):
        order[str(i)] = label
        parts.append(f"PROPOSAL {i}:\n---\n{content}\n---")
    return "\n\n".join(parts), order


def parse_ranking(text: str, valid_chars: str = "123"):
    """Extract 'RANKING: a, b, c' line. Scans backwards for pre-ranking notes."""
    for line in reversed(text.split("\n")):
        line = line.strip().strip("*").strip().lstrip("#").strip()
        if line.upper().startswith("RANKING:"):
            raw = line.split(":", 1)[1].strip()
            items = [c for c in raw if c in valid_chars]
            if len(items) >= 2:
                return items
    return None


def aggregate_rankings(rankings, labels=("A", "B", "AB"), tiebreak_winner="A"):
    """Borda count. 1st=3pts, 2nd=2pts, 3rd=1pt. Ties → tiebreak_winner."""
    scores = {l: 0 for l in labels}
    n = len(labels)
    valid = [r for r in rankings if r is not None]
    for ranking in valid:
        for pos, label in enumerate(ranking):
            if label in scores and pos < n:
                scores[label] += (n - pos)
    if tiebreak_winner:
        priority = {l: (0 if l == tiebreak_winner else i + 1) for i, l in enumerate(labels)}
    else:
        priority = {l: i for i, l in enumerate(labels)}
    ranked = sorted(scores.keys(), key=lambda k: (-scores[k], priority[k]))
    return ranked[0], scores, valid


# ── One autoreason pass ────────────────────────────────────────────────


async def run_pass(
    llm: LLMClient,
    task_prompt: str,
    current_a: str,
    pass_num: int,
    pass_dir: Path,
    num_judges: int,
    author_temp: float,
    judge_temp: float,
    max_tokens: int,
):
    pass_dir.mkdir(parents=True, exist_ok=True)

    # Resume from cache if this pass was already run
    result_file = pass_dir / "result.json"
    if result_file.exists():
        ex = json.loads(result_file.read_text())
        w = ex.get("winner")
        if w == "A":
            return w, current_a, ex
        wf = pass_dir / f"version_{w.lower()}.md"
        if wf.exists():
            return w, wf.read_text(), ex

    t0 = time.time()
    (pass_dir / "version_a.md").write_text(current_a)

    # 1. Critic (reads A only)
    critic = await llm.call(
        CRITIC_SYSTEM,
        CRITIC_PROMPT.format(version_a=current_a),
        temperature=author_temp,
        max_tokens=max_tokens,
    )
    (pass_dir / "critic.md").write_text(critic)

    # 2. Author B (reads task + A + critique)
    vb = await llm.call(
        AUTHOR_B_SYSTEM,
        AUTHOR_B_PROMPT.format(task_prompt=task_prompt, version_a=current_a, critic=critic),
        temperature=author_temp,
        max_tokens=max_tokens,
    )
    (pass_dir / "version_b.md").write_text(vb)

    # 3. Synthesizer (reads task + A + B, random order)
    if random.random() < 0.5:
        vx, vy = current_a, vb
    else:
        vx, vy = vb, current_a
    vab = await llm.call(
        SYNTHESIZER_SYSTEM,
        SYNTHESIZER_PROMPT.format(task_prompt=task_prompt, version_x=vx, version_y=vy),
        temperature=author_temp,
        max_tokens=max_tokens,
    )
    (pass_dir / "version_ab.md").write_text(vab)

    # 4. Judge panel (parallel, blind, randomized labels)
    tasks, orders = [], []
    for _ in range(num_judges):
        proposals, order = randomize_for_judge(current_a, vb, vab)
        orders.append(order)
        tasks.append(
            llm.call(
                JUDGE_SYSTEM,
                JUDGE_RANK_3_PROMPT.format(task_prompt=task_prompt, judge_proposals=proposals),
                temperature=judge_temp,
                max_tokens=max_tokens,
            )
        )
    judge_responses = await asyncio.gather(*tasks, return_exceptions=True)

    rankings, details = [], []
    for resp, order in zip(judge_responses, orders):
        if isinstance(resp, Exception):
            rankings.append(None)
            details.append({"error": str(resp)})
        else:
            raw = parse_ranking(resp, "123")
            mapped = [order.get(r, r) for r in raw] if raw else None
            rankings.append(mapped)
            details.append({"ranking": mapped, "order": order, "raw_tail": resp[-400:]})

    # 5. Borda aggregate (ties → A)
    winner, scores, valid = aggregate_rankings(rankings, ("A", "B", "AB"), tiebreak_winner="A")
    elapsed = time.time() - t0

    vmap = {"A": current_a, "B": vb, "AB": vab}
    result = {
        "pass": pass_num,
        "winner": winner,
        "scores": scores,
        "valid_judges": len(valid),
        "elapsed_s": round(elapsed, 1),
        "judge_details": details,
    }
    result_file.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    return winner, vmap[winner], result


# ── Main loop ──────────────────────────────────────────────────────────


async def run_autoreason(
    llm: LLMClient,
    task_prompt: str,
    out_dir: Path,
    label: str = "",
    num_judges: int = 3,
    max_passes: int = 30,
    convergence_threshold: int = 2,
    author_temp: float = 0.8,
    judge_temp: float = 0.3,
    max_tokens: int = 4096,
):
    out_dir.mkdir(parents=True, exist_ok=True)

    # Generate or resume initial A
    init_file = out_dir / "initial_a.md"
    if init_file.exists():
        current_a = init_file.read_text()
        print(f"  [{label}] Resumed initial A: {len(current_a.split())} words")
    else:
        current_a = await llm.call(
            AUTHOR_SYSTEM,
            GENERATE_A.format(task_prompt=task_prompt),
            temperature=author_temp,
            max_tokens=max_tokens,
        )
        init_file.write_text(current_a)
        print(f"  [{label}] Initial A: {len(current_a.split())} words")

    streak = 0
    history = []
    for p in range(1, max_passes + 1):
        winner, winner_text, result = await run_pass(
            llm,
            task_prompt,
            current_a,
            p,
            out_dir / f"pass_{p:02d}",
            num_judges,
            author_temp,
            judge_temp,
            max_tokens,
        )
        history.append(
            {
                "pass": p,
                "winner": winner,
                "scores": result.get("scores", {}),
                "words": len(winner_text.split()),
            }
        )
        print(
            f"  [{label}] Pass {p}: {winner} "
            f"(A={result['scores'].get('A',0)}, "
            f"B={result['scores'].get('B',0)}, "
            f"AB={result['scores'].get('AB',0)}) "
            f"[{result.get('elapsed_s',0):.0f}s]"
        )

        if winner == "A":
            streak += 1
        else:
            streak = 0
            current_a = winner_text
            (out_dir / f"incumbent_after_{p:02d}.md").write_text(current_a)

        if streak >= convergence_threshold:
            print(f"  [{label}] ✔ Converged at pass {p} (A won {streak} in a row)")
            break
    else:
        print(f"  [{label}] ⚠ Hit max_passes={max_passes} without convergence")

    (out_dir / "final_output.md").write_text(current_a)
    (out_dir / "history.json").write_text(json.dumps(history, indent=2))
    trajectory = " → ".join(h["winner"] for h in history)
    print(f"  [{label}] Final: {len(current_a.split())} words | trajectory: {trajectory}")
    return current_a, history


# ── CLI ────────────────────────────────────────────────────────────────


def main():
    p = argparse.ArgumentParser(description="Autoreason tournament refinement loop.")
    p.add_argument("--task", required=True, help="Path to task prompt file (markdown or text)")
    p.add_argument("--out", required=True, help="Output directory for runs")
    p.add_argument("--provider", default="openai", choices=["openai", "anthropic"])
    p.add_argument("--model", default=None, help="Model id. Pass explicitly or set the provider's *_LATEST_MODEL env var after checking current model availability.")
    p.add_argument("--judges", type=int, default=3, help="Judges per pass (3 default, 7 for 3× faster convergence)")
    p.add_argument("--max-passes", type=int, default=30)
    p.add_argument("--convergence", type=int, default=2, help="k — consecutive A-wins required")
    p.add_argument("--author-temp", type=float, default=0.8)
    p.add_argument("--judge-temp", type=float, default=0.3)
    p.add_argument("--max-tokens", type=int, default=4096)
    p.add_argument("--label", default="run", help="Label used in log prefixes")
    args = p.parse_args()

    if args.model:
        model = args.model
    else:
        env_var = f"{args.provider.upper()}_LATEST_MODEL"
        model = os.environ.get(env_var)
        if not model:
            raise SystemExit(
                f"{args.provider.title()} model not set. Check current official provider docs, "
                f"then pass --model or set {env_var}."
            )

    task_prompt = Path(args.task).read_text().strip()
    out_dir = Path(args.out)

    print("=" * 60)
    print(f"AUTOREASON — {args.provider}/{model}")
    print(f"Judges: {args.judges} · Convergence: k={args.convergence} · Max passes: {args.max_passes}")
    print(f"Task file: {args.task} ({len(task_prompt.split())} words)")
    print(f"Output:    {out_dir}")
    print("=" * 60)

    llm = LLMClient(args.provider, model)
    asyncio.run(
        run_autoreason(
            llm,
            task_prompt,
            out_dir,
            label=args.label,
            num_judges=args.judges,
            max_passes=args.max_passes,
            convergence_threshold=args.convergence,
            author_temp=args.author_temp,
            judge_temp=args.judge_temp,
            max_tokens=args.max_tokens,
        )
    )


if __name__ == "__main__":
    main()
