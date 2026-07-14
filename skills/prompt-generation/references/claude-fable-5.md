# Claude Fable 5 Prompt Lane

Use this reference when the target model is Anthropic Claude Fable 5 — for
prompt packages, agent instructions, skill text, goal/rubric design, verifier
prompts, or migrations from Claude Opus 4.x or OpenAI GPT-5.6.

Source check for this version: 2026-07-09 (official Anthropic Fable 5
prompting guide, effort/adaptive-thinking/task-budgets/refusals pages,
orchestration cookbook on platform.claude.com, OpenAI GPT-5.6 preview guidance,
and local Codex model probes). Stale after any Anthropic or GPT-5.6 model
release or 90 days, whichever comes first. Current official docs outrank this
file.

## Confirmed Claude Model Facts (2026-07-02)

- API model ID: `claude-fable-5` — one ID, 1M-token context window by
  default, up to 128K output tokens. (There is no separate `[1m]` variant;
  earlier versions of this file were wrong.)
- Adaptive thinking is always on; raw chain-of-thought is never returned.
  The default thinking display is omitted on Fable 5 — set
  `thinking.display: "summarized"` explicitly or the `thinking` field comes
  back empty even though thinking happened and is billed.
- Effort replaces extended-thinking `budget_tokens`. On the Messages API the
  control is `output_config: {"effort": "low"|"medium"|"high"|"xhigh"|"max"}`
  — keep the `output_config` wrapper; `effort` is not a top-level parameter.
  Default to `high`; reserve `xhigh` for the most capability-sensitive work;
  step up to `max` only when evals show measurable headroom at `xhigh`.
  Low effort on Fable 5 still exceeds xhigh on prior model generations.
- Task budgets (beta `task-budgets-2026-03-13`): `output_config.task_budget`
  caps total token spend across a whole agentic loop (thinking + tools +
  output) and lets the model finish gracefully as it depletes. Advisory, not
  a hard cap (`max_tokens` stays the hard cap); minimum 20,000; a too-small
  budget causes refusal-like early stops. Effort tunes per-step depth;
  task_budget bounds the whole run — set both for long autonomous work.
- Safety classifiers decline four categories: `cyber`, `bio`,
  `reasoning_extraction`, and `frontier_llm` (requests that could assist
  development of competing AI models — benign ML work can trip it). Design a
  fallback lane for declined calls (see Fallback: Claude Opus 4.8 below).

## Controls

- Anthropic `output_config.effort` is not OpenAI `reasoning.effort` and not
  Codex `model_reasoning_effort`. Never translate control names or values
  across providers; re-derive them from the target provider's docs.
- Non-default `temperature`, `top_p`, or `top_k` are rejected with a 400
  error on Fable 5 (and Mythos 5, Sonnet 5, Opus 4.7/4.8) — an enforced API
  constraint, not a style preference.
- Do not use manual thinking budgets; `effort` is the depth control.
- Do not raise `effort` to get longer prose; effort buys reasoning depth,
  not verbosity.
- XML-style sections remain useful for mixed context, examples, and inputs.

## Prompt Style That Changed With Fable 5

- Replace enumerated behavior lists with brief directional statements.
  Instruction following is strong enough that one sentence of intent
  outperforms a list of cases; procedural scaffolding written for weaker
  models now reduces quality.
- Never instruct the model to show, echo, transcribe, or explain its internal
  reasoning as response text. On Fable 5 this triggers a
  `reasoning_extraction` refusal. Rely on summarized adaptive thinking and
  evidence-backed output instead.
- Drop aggressive emphasis ("CRITICAL: YOU MUST"). Normal sentences steer
  Fable 5; use "Use this tool when ..." phrasing for tool guidance.
- Add an over-engineering guardrail to any prompt that may run at `high` or
  `xhigh` effort: "Don't add features, refactor, or introduce abstractions
  beyond what the task requires. Do the simplest thing that works well."
- State boundaries explicitly: name what the agent should NOT do (unsolicited
  drafts, git backups, scope expansion). Fable 5 acts on standing authority,
  so missing boundaries become unrequested actions.

## Long-Run / Agentic Rules

- Progress audit: "Before reporting progress, audit each claim against a tool
  result from this session. Only report work with evidence."
- Autonomous mode: "The user is not watching in real time. For reversible
  actions that follow from the request, propose and proceed; do not stop to
  ask permission you already have."
- Anti-early-stop: deep in long sessions Fable 5 may state intent without
  acting ("I'll now run X"). Pair checkpoints with the autonomous-mode
  reminder so stated intent immediately becomes a tool call.
- Context reassurance for long runs: "You have ample context remaining. Do
  not stop or summarize on account of context limits." Avoid surfacing
  explicit context-budget counts in prompts.
- For long asynchronous agents, provide a send-to-user surface so mid-task
  deliverables reach the user without ending the turn.
- Human-readable output rule for reports and final messages: complete
  sentences, no working shorthand or arrow chains, spell out identifiers.
- Periodic self-verification cadence for genuinely long runs (official
  scaffolding guidance): establish a method for checking the work at a set
  interval as it builds, and run that check every interval by verifying with
  subagents against the specification.

## Parallel Subagents / Orchestration

- Fable 5 dispatches subagents more readily than prior models; delegation
  should be frequent and asynchronous. Official recommended prompt line:
  "Delegate independent subtasks to subagents and keep working while they
  run. Intervene if a subagent goes off track or is missing relevant
  context."
- Long-lived subagents that keep context across subtasks save cost via
  cache reads and avoid bottlenecking on the slowest lane.
- Anthropic publishes a worked "Orchestration Mode" cookbook pattern:
  mid-conversation system messages (enter/refresh/exit) plus a Workflow tool
  whose description carries a standing-consent clause, so substantive tasks
  fan out without per-request permission while the mode is on. (Docs state
  mid-conversation system messages are Opus 4.8+; confirm Fable 5 coverage
  against current docs before relying on it.)
- For the Codex-executor side of orchestration (worker briefs, fan-out
  width, worktree isolation, hand-back contracts), see the `codex` skill
  `references/fable-codex-orchestration.md`.

## Verification Design

- Fresh-context verifier subagents outperform self-critique on Fable 5
  (stated directly in Anthropic's prompting guide). The agent that produced
  work must not grade it; the verifier sees only the rubric and the
  artifact, never the producer's reasoning.
- Adversarial verification wave (official cookbook pattern): instruct the
  verifier to try to refute the result, re-derive claims independently
  rather than trusting them, and default to refuted when uncertain.
- "Are you 100% confident — keep looking" self-critique loops are an
  anti-pattern: they induce over-deliberation at high effort and still carry
  self-grading bias. Replace with a verifier gate plus an evidence-backed
  confidence statement. (Internal doctrine consistent with, but not
  verbatim from, Anthropic docs.)
- Write goals and rubrics as machine-checkable conditions (test command,
  metric threshold, schema-validated verdict), never prose intent.

## Memory Design (multi-session work)

- Progression: fail → investigate → verify → distill → consult. A lesson
  enters memory only after the failure was investigated to root cause and the
  fix was confirmed; unverified lessons become spurious generalizations.
- One lesson per file, one-line summary at top; include corrections and
  confirmed approaches; update existing notes rather than duplicating.
- Do not store what the repo already records (code structure, git history).

## Migration: Claude Opus 4.x → Fable 5

- Treat as a retune, not a model-string swap. Re-run evals before promoting.
- Replace `budget_tokens` thinking config with `output_config.effort`.
- Audit for "show your thinking" style instructions (reasoning_extraction
  refusals) and for enumerated behavior lists to compress.
- Expect longer autonomous runs; add the progress-audit and anti-early-stop
  rules above instead of shortening tasks.
- Operational deltas from the official migration guide: pricing roughly
  doubles vs Opus 4.8; Fable 5 requires 30-day data retention and is not
  available under Zero Data Retention (hard blocker for ZDR-committed
  deployments); assistant-message prefill returns a 400; prompt-cache
  minimum drops from 1,024 to 512 tokens.

## Migration: OpenAI GPT-5.6 → Fable 5

- Strip OpenAI runtime controls (`reasoning.effort`, `text.verbosity`,
  `previous_response_id` state notes) and re-derive Anthropic equivalents
  (`effort`, summarized thinking display, Anthropic-native state handling).
- Structured outputs: prefer Anthropic strict tool schemas for
  machine-readable verdicts; do not port OpenAI `text.format` blocks.
- Keep the prompt-text/runtime-controls separation; only the controls change.

## Fallback: Claude Opus 4.8

Use `claude-opus-4-8` as the fallback lane when Fable 5 safety classifiers
decline a legitimate request. Confirmed notes from the 2026-06-08 source
check: use `output_config.effort`; do not set non-default sampling
parameters; do not use manual thinking budgets. Verify against current docs
before hardcoding — these notes age.

Documented mechanics (2026-07-02): the `fallbacks` request parameter (beta
`server-side-fallback-2026-06-01`) lists up to three models tried in order
server-side. Refusals surface as `stop_reason: "refusal"` with
`stop_details.category` and an explanation — branch on `stop_reason`, not
`stop_details`, which can be null. Retry on the fallback model, never the
same model. Configure fallback per request path, and give subagent calls
their own fallback config — the parameter does not propagate into
tool-invoked model calls. Accepted conversations get ~1 hour of sticky
routing to the model that accepted them.

## Anti-Patterns (Fable 5)

- Asking the model to expose internal reasoning (refusal, not just noise).
- Enumerated behavior lists and step-by-step recipes for default behavior.
- Self-critique confidence loops instead of fresh-context verifiers.
- Cross-applying OpenAI control names or values.
- Hardcoding model facts without a dated source check and refresh trigger.
- Raising effort to fix problems that are actually missing verification
  surfaces or missing boundaries.
