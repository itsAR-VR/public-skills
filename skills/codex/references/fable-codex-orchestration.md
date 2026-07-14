# Fable → Codex Orchestration Lane

Use this reference when Claude (Fable 5, orchestrator lane) delegates
implementation, verification, or investigation work to the Codex GPT-5.6 tier family —
single delegations, parallel fan-outs, and ultracode sessions with
Codex-heavy execution.

Source check: 2026-07-09 (OpenAI Codex guides on developers.openai.com,
Anthropic Fable 5 prompting guide, Anthropic and OpenAI orchestration
cookbooks, and live model probes on codex-cli 0.144.0).
Stale after any Codex CLI major release or 90 days. Current official docs
outrank this file. The model table and routing rules live in
`share-codex-config` `assets/coding-doctrine.md` — canonical, not
re-copied here.

## When To Delegate At All

Delegate to Codex when the subtask is bulk or mechanical with a clear
spec, would flood the orchestrator with context it does not need
afterward, or genuinely parallelizes. Otherwise do it inline —
multi-agent splits add coordination overhead and multiply token cost.
Keep one coherent unit per worker (a feature and its tests together),
not plan/implement/test/review pipeline stages; stage handoffs degrade
fidelity like a telephone game.

Fable stays the single thread of control: each Codex run is a tool call
whose output Fable judges (agent-as-tool, not handoff). The worker never
grades its own output.

## The Per-Worker Prompt (what Fable writes)

GPT-5.6 steers outcome-first. Give the destination and constraints, not
a procedure — step-by-step lists ported from older prompt stacks shrink
its search space and are the main quality regression OpenAI warns about.

Each brief is self-contained and context-isolated: objective, the exact
files and errors, output contract, boundaries. Never the orchestrator's
conversation history. Shape it with the four-part contract from the
`codex` skill: goal, context, constraints, done-when.

- Done-when is machine-checkable: name the commands (full test suite,
  lint, build) the worker must run before claiming done. Guard the
  "ran one test, declared victory" failure mode explicitly.
- Tell it to proceed on reasonable assumptions and list them in the
  hand-back; nobody is available to answer questions mid-run.
- Headless runs: do not request upfront plans, preambles, or status
  narration. OpenAI's Codex prompting cookbook recommends removing these
  from non-interactive rollouts — they can end a turn prematurely.
- Results come back as files plus a compact structured hand-back
  (status, files changed, commands run with results, evidence paths,
  assumptions), not a raw transcript. Briefs above a few KB go in a
  file the short prompt argument points at — never stdin.
- A weak result means the brief was vague: tighten spec and stopping
  criteria. Do not raise effort to rescue a vague prompt; higher effort
  on a conflicted brief produces overthinking and loops.

## Invocation Mechanics (codex-cli 0.144+)

- Difficult, deep, review, or orchestrator work:
  `codex exec -m gpt-5.6-sol -c model_reasoning_effort=ultra [-C <dir>] "<brief>"`.
- Bounded worker work:
  `codex exec -m gpt-5.6-terra -c model_reasoning_effort=high [-C <dir>] "<brief>"`.
- Tiny mechanical work:
  `codex exec -m gpt-5.6-luna -c model_reasoning_effort=low [-C <dir>] "<brief>"`;
  use `medium` when the task remains small but needs more care.
- Access gate: before the first 5.6 delegation, require `codex debug models` to
  list all three tier IDs and efforts, then run a live read-only selected-tier
  probe after login. The catalog check alone does not prove account entitlement.
  If either check fails, stop with a blocker; never downgrade silently.
- Always pass the model explicitly; config.toml defaults vary by machine.
- Sandbox: `-s read-only` for investigation and review;
  `-s workspace-write` for implementation. Prefer `--add-dir` for extra
  writable paths over escalating to danger-full-access.
- Result capture: `-o <file>` (`--output-last-message`) writes only the
  final message — the cleanest hand-back; `--json` streams JSONL events;
  `--output-schema <schema.json>` constrains the final response shape
  (validate the output anyway; conformance has known gaps).
- Continuation: `codex exec resume --last` (or a session id) keeps
  thread state across follow-ups. Persist session ids as checkpoints in
  long loops so a failed lane resumes instead of restarting.
- Do not trust the exit code alone. Confirm the `-o` file content or the
  last JSONL event before declaring a worker done; Codex has a reported
  silent-failure mode with detached TTYs and long stdin prompts
  (openai/codex issue #19945).

## Effort Mapping (Codex-side)

Tier mapping: Luna at `low` or `medium` for tiny mechanical tasks; Terra at
`high` for bounded workers; Sol at `ultra` for difficult, deep, review, or
orchestrator work. `max` and `ultra` are accepted advanced Codex effort values,
but should not be carried into every lane by default.

An ultracode session does not mean every worker runs Sol at ultra. Ultracode
raises orchestration ambition — more lanes, adversarial verification,
deeper synthesis. Each Codex worker still runs the lowest effort its own
task merits: Luna for tiny mechanics, Terra at high for bounded workers, and
Sol at ultra only for genuinely difficult synthesis or independent review. Codex effort
values never translate to Anthropic effort values; re-derive per
provider (see `prompt-generation` `references/claude-fable-5.md`).

## Fan-Out Shape

- Default width 3-5 concurrent workers; batch-synchronous Codex waves are
  fine — dispatch a wave, judge, dispatch the next. Fable's own subagent
  dispatch stays asynchronous: keep working while lanes run.
- Concurrent write lanes against one repo need isolation: one git
  worktree per workspace-write worker, or disjoint `--add-dir` scopes.
  Merging and reconciling diffs is the orchestrator's job, never a
  worker's.
- Partial failure: a failed or timed-out worker gets one retry with a
  tightened brief that includes the failure evidence. After that, report
  the lane as failed in the synthesis. Never silently drop a lane.
- Verification wave: fresh-context verifiers see only the artifact, the
  rubric, and the commands to run — never the producer's reasoning.
  Instruct them to refute, re-derive claims independently, and default
  to refuted when uncertain. Gate progression on artifact existence and
  command output, not the worker's self-report.

## Plugin And Alternate Lanes

- With the openai-codex plugin installed: `/codex:review` and
  `/codex:adversarial-review` for review lanes; the `codex:codex-rescue`
  subagent for single delegations. The rescue subagent is a forwarder by
  design — one Codex call per rescue, no orchestration inside it. Always
  pass model and effort explicitly: the plugin's own defaults reference
  older model generations.
- Orchestrator-controlled fan-out is concurrent `codex exec` processes:
  Fable judges every lane. Codex also has native subagents that work under
  exec — built-in `default`/`worker`/`explorer` agents (a custom agent with
  the same name takes precedence), custom agents as TOML under
  `~/.codex/agents/`, and the experimental `spawn_agents_on_csv` batch tool
  (one worker per CSV row, structured per-row results, ~6 concurrent
  threads by default). Use native subagents for many-similar-item sweeps
  inside one Codex lane; keep cross-lane judgment with the orchestrator. In
  non-interactive runs any action needing fresh approval fails back to the
  parent, so pin sandbox scope up front.
- For persistent programmatic control of many sessions, use
  `codex mcp-server` or the app-server/SDK lane; pin approval-policy
  never and sandbox workspace-write for deterministic unattended runs.
- CI: `CODEX_API_KEY=<key> codex exec` scopes auth to one invocation;
  `codex cloud exec --env <ENV_ID> --attempts N "<brief>"` gives remote
  best-of-N runs (`--branch` as needed).

## Fable-Side Rules

Orchestrator behavior — autonomy, anti-early-stop, verifier design,
Anthropic effort and task budgets — lives in `prompt-generation`
`references/claude-fable-5.md`. Delegate independent subtasks and keep
working while they run; intervene only when a lane is off track or
missing context.
