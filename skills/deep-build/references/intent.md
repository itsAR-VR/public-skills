# Intent: Deep Build

## Why This Exists

The `build` skill runs a single-model execution pipeline. It's effective, but shares
the same blind spot as all single-model workflows: **the implementing model reviews
its own work.** Self-review catches surface issues but systematically misses certain
error classes — the same reasoning patterns that produced the bug also rationalize
it during review.

Deep Build solves this by inserting **cross-model verification at every gear**:
- The active primary model implements in the current harness
- A harness-routed OpenAI-family verifier independently verifies each diff (different model, different blind spots)
- The combination catches what neither catches alone

## How It Relates to Other Skills

```
deep-sweep ──(produces plan)──> deep-build ──(produces code)──> ship
     │                              │
     │  analysis only               │  full execution
     │  multi-model planning        │  multi-model building
     │  output: phase plan          │  output: working, QA'd code
     │                              │
     └──── both use primary-model + OpenAI-family cross-verification ──┘
```

- **deep-sweep**: The planning counterpart. Can be invoked as Gear 1 of deep-build.
- **build**: The single-model version. deep-build enhances every gear with cross-model verification.
- **terminus-maximus**: The implementation engine. deep-build uses it as the core of Gear 3.

## Design Decisions

### Why the primary model implements and OpenAI-family verifier checks?
- The primary model is already attached to the user's current harness and tool context
- In Claude Code, the current hardcoded latest snapshot is `claude-opus-4-7`; aliases like `opus` can resolve to the latest family model
- The OpenAI-family verifier supplies a different model family and different blind spots
- In Codex main harness, use native sub-agents instead of nested CLI
- In Claude Code, `codex exec` can run in read-only sandbox after model support is verified
- Different roles for different strengths

### Why verify EVERY diff, not just the final result?
- Catching bugs at the subphase level is cheaper than finding them in final review
- Each diff is small enough for the verifier to analyze thoroughly
- Compound bugs (A looks fine, B looks fine, A+B breaks) are caught by cross-monitor

### Why parallel subphase lanes?
- Independent subphases have no reason to wait for each other
- Parallelism reduces total wall-clock time significantly
- Cross-monitor catches interaction effects between parallel lanes
- Follows the dispatching-parallel-agents pattern from Superpowers

### Why the three-pass minimum?
Every piece of code gets verified three times by different mechanisms:
1. **Implementation review** — primary model self-reviews as it implements (terminus-maximus)
2. **Cross-model review** — OpenAI-family verifier independently reviews the diff
3. **QA verification** — Tests + visual QA + security review

This mirrors the testing pyramid (unit → integration → e2e) but applied to review.
