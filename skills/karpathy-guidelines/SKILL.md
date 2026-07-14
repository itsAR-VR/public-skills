---
name: karpathy-guidelines
description: Karpathy-inspired behavioral guardrails to reduce common LLM coding mistakes (wrong assumptions, overengineering, drive-by edits, missing verification loops).
source: forrestchang/andrej-karpathy-skills
license: MIT
related_skills: [code-review, build, terminus-maximus, phase-plan, plan]
---

# Karpathy-Inspired Coding Guardrails

Behavioral guidelines to reduce common LLM coding mistakes, derived from [Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876) on LLM coding pitfalls.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## The Problems (Karpathy's Words)

> "The models make wrong assumptions on your behalf and just run along with them without checking. They don't manage their confusion, don't seek clarifications, don't surface inconsistencies, don't present tradeoffs, don't push back when they should."

> "They really like to overcomplicate code and APIs, bloat abstractions, don't clean up dead code... implement a bloated construction over 1000 lines when 100 would do."

> "They still sometimes change/remove comments and code they don't sufficiently understand as side effects, even if orthogonal to the task."

## 1) Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

- State assumptions explicitly; if uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so; push back when warranted.
- If something is unclear, stop; name what's confusing and ask.

**Anti-pattern:** User says "Add export for user data." LLM silently assumes: all users, JSON format, file on disk, specific fields. Fix: list your assumptions explicitly and ask which apply.

## 2) Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If 200 lines could be 50, rewrite it.

Ask: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

**Anti-pattern:** User says "Add a discount function." LLM builds: DiscountStrategy ABC, PercentageDiscount, FixedDiscount, DiscountConfig dataclass, DiscountCalculator class (100+ lines). Fix: `def calculate_discount(amount, percent): return amount * (percent / 100)`. Add complexity when the requirement demands it, not before.

## 3) Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it — don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

Test: Every changed line should trace directly to the user's request.

**Anti-pattern (drive-by refactoring):** User says "Fix the empty email crash." LLM also: adds type hints, rewrites comments, changes quote style, adds username validation nobody asked for. Fix: only change lines that fix the reported issue.

**Anti-pattern (style drift):** User says "Add logging." LLM also: changes `''` to `""`, adds docstrings, reformats whitespace, restructures boolean returns. Fix: add logging lines, match existing quote style, spacing, and patterns.

## 4) Goal-Driven Execution

**Define success criteria. Loop until verified.**

> "LLMs are exceptionally good at looping until they meet specific goals... Don't tell it what to do, give it success criteria and watch it go."

Transform tasks into verifiable goals:

| Instead of... | Transform to... |
|--------------|-----------------|
| "Add validation" | Write tests for invalid inputs, then make them pass |
| "Fix the bug" | Write a test that reproduces it, then make it pass |
| "Refactor X" | Ensure tests pass before and after |

For multi-step tasks, create a brief plan with verifiable checks using the $phase-plan $phase-gaps $phase-review family of skills:

```
1. [Step] -> verify: [check]
2. [Step] -> verify: [check]
3. [Step] -> verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

## 5) KLLM Wiki Architecture

Karpathy's [KLLM wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) is a persistent, compounding knowledge artifact. Instead of re-discovering knowledge on every query (like RAG), the LLM maintains a structured wiki that grows over time.

### Three-Layer Architecture

| Layer | Owner | Purpose |
|-------|-------|---------|
| **Raw sources** | Human | Immutable documents (articles, papers, images). Source of truth. |
| **The wiki** | LLM | Markdown pages organized by entities, concepts, summaries. Cross-referenced and consistent. |
| **The schema** | Human | Config file (e.g., CLAUDE.md) documenting structure, conventions, workflows. |

### Core Operations

- **Ingest:** Process new sources, extract takeaways, write summaries, update entity pages, maintain a log.
- **Query:** Search relevant pages and synthesize answers with citations. Good answers become new wiki pages.
- **Lint:** Periodically health-check for contradictions, stale claims, orphan pages, missing cross-references.

### Navigation Files

- **index.md** — Content catalog organized by category, updated on every ingest.
- **log.md** — Append-only chronological record tracking the wiki's evolution.

### Why This Beats Vanilla RAG

RAG re-discovers knowledge on every query. The KLLM wiki compounds: each ingest makes the wiki richer, cross-references tighter, and queries faster. The tedious bookkeeping falls to the LLM, which doesn't get bored and doesn't forget to update a cross-reference.

**Human judgment drives direction. LLM handles overhead.**

### Relationship to Graphify

Graphify (`/graphify`) takes this further: instead of flat wiki pages, it builds a knowledge graph with nodes, edges, and community detection. They're complementary:

- **KLLM wiki:** text-first, better for narrative knowledge, ongoing curation, human-readable browsing
- **Graphify:** structure-first, better for code intelligence, blast radius analysis, structural relationships, inferred connections

Both solve the same core problem: stop re-discovering knowledge on every query. Compound it instead.

## Success Criteria

These guidelines are working if:
- Fewer unnecessary changes in diffs — only requested changes appear
- Fewer rewrites due to overcomplication — code is simple the first time
- Clarifying questions come before implementation — not after mistakes
- Clean, minimal PRs — no drive-by refactoring or "improvements"
