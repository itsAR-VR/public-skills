# Builder lens — engineering and technical decisions

Use for architecture, stack selection, refactors, build-vs-buy, and
system-design calls. Forces the council to think beyond the code itself —
most engineering decisions are bottlenecked by operability, not correctness.

## Sub-questions (answer all four)

### 1. Correctness & simplicity
- What is the **simplest** implementation that could plausibly be correct?
- Where does this introduce a **subtle failure mode** that won't show up in
  unit tests — concurrency, retries, partial failures, time zones, encoding?
- What invariant does this design **rely on** that isn't enforced by the
  type system or a test?

### 2. Maintainability & operability
- Who will **debug this at 3am** in 6 months, and do they have what they
  need? (Logs, metrics, a runbook, the ability to reproduce?)
- What **accidental coupling** does this decision create between components
  that should stay independent?
- If this needs to be **rewritten in a year**, how hard is the migration?
  (Hint: the easier the rewrite, the better the design.)

### 3. Performance & cost
- What's the **P99 latency** and the **throughput ceiling** of the design,
  not just P50?
- Where are the **non-obvious cost leaks** — retries, logging, cache misses,
  cold starts, orphan resources, LLM token burn?
- At **10x** current load, what breaks first — and is that the thing the
  design assumed would scale?

### 4. Security & blast radius
- What's the **worst outcome** if this component is compromised — data
  exfiltration, lateral movement, denial of service, silent corruption?
- Does this **expand** the trust boundary or **contract** it?
- What's the **blast radius** of a bug or misconfiguration — blast contained
  to one user, one tenant, one region, or does it affect everyone?
