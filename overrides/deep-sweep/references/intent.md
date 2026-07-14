# Intent: Deep Sweep

## Why This Exists

Existing planning skills (plan, phase-gaps, execute) operate within a single model's
perspective. They catch many issues but share a blind spot: **a single model's reasoning
patterns create systematic gaps that the same model cannot detect.**

Deep Sweep solves this by introducing **cross-model verification** — using the active
primary reasoning model for deep analysis and a harness-routed OpenAI-family verifier
for independent verification. Different training data, different reasoning patterns,
different blind spots. What one misses, the other catches.

## Design Decisions

### Why the active primary model for deep analysis?
- It is the model already steering the user's current harness and context
- In Claude Code, aliases like `best`, `fable`, and `opus` route through the current model configuration; see `references/model-currency.md` before pinning
- Provider-appropriate effort or adaptive thinking provides deep reasoning when the selected provider supports it
- Best at identifying non-obvious risks and edge cases
- Can sustain complex multi-step analysis without exposing hidden/internal reasoning

### Why a harness-routed OpenAI-family verifier for cross-verification?
- Genuinely independent model (different training, architecture)
- Strong at code-level verification against actual codebase
- Catches different classes of errors than Claude models
- In Codex main harness, use native sub-agents instead of nested CLI
- In Claude Code, `codex exec` may use a read-only sandbox after model support is verified

### Why the cross-comparison pair?
Most analysis tools look at problems in isolation. The cross-comparison pair exists
specifically to catch **interaction effects** — things that pass every individual
test but fail when combined. This is inspired by:
- Integration testing philosophy (unit tests pass, integration breaks)
- The "telephone game" problem in multi-agent systems
- Real-world failures that occur at boundaries between components

### Why lane communication instead of just a report?
A report collects findings but doesn't close the loop. Lane communication ensures:
1. The agent/plan responsible for a subphase knows about cross-cutting issues
2. Mitigations are incorporated into the plan, not left as TODO items
3. The plan on disk reflects all discovered issues, ready for execution

### Why 84.7% confidence threshold?
Carried from the phase-gaps skill convention. Below this threshold, findings
are raised as explicit Open Questions requiring user input rather than being
treated as assumptions that might be wrong.

## What This Is NOT

- Not an execution skill — it produces plans, not implementations
- Not a single-pass analyzer — minimum 3 verification passes per subphase
- Not a replacement for phase-gaps — it USES phase-gaps as a subroutine
- Not a sequential process — designed for maximum parallelism throughout
