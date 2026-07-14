# Model Prompt Generation Playbook

Use this reference when creating or upgrading reusable prompts, Codex goals,
agent instructions, skill instructions, or eval prompts. Current official docs
outrank this file for model availability, pricing, limits, and API behavior.

Source check for this version: 2026-07-09.

GPT-5.6 family source: `https://help.openai.com/en/articles/20001325-a-preview-of-gpt-5-6-sol-terra-and-luna`.

## Source Quality Gate

Record sources before writing durable model guidance:

- official OpenAI docs or cookbook for OpenAI/Codex/API claims;
- official Anthropic docs for Claude claims;
- concrete local file readback for local skill or config claims;
- inaccessible when a cited source cannot be read.

For latest-model claims, use `openai-docs` first. Do not repeat a model ID,
context window, price, feature flag, or deprecation date unless it was verified
for the target date.

## Prompt Package Anatomy

Separate prompt text from runtime controls.

Prompt text owns:

- goal and user-facing outcome;
- context and source-of-truth inputs;
- constraints, non-goals, and approval boundaries;
- output shape and style;
- done/proof criteria;
- blocker, refusal, and incompatible-input behavior;
- stop conditions.

Runtime controls own:

- model and provider;
- reasoning effort or provider-specific effort;
- verbosity or max output controls;
- Structured Outputs or strict tool schemas;
- tool set, tool choice, and hosted/custom tool split;
- prompt caching key and stable-prefix placement;
- state handling, response replay, and phase preservation.

## Surface Decision Table

| Surface | Use when | Do not use when |
|---|---|---|
| Normal Codex prompt | The task is bounded and the proof surface is clear. | The task needs a durable autonomous loop. |
| Codex `/plan` or planning skill | The problem is complex but the success criteria are not yet tight. | The user asked for a simple edit or answer. |
| Codex `/goal` | The objective is durable, evidence-backed, and may need iteration. | The finish line is vague or one-step. |
| `AGENTS.md` | The rule is durable repo/workspace context. | The rule is task-specific or private. |
| Skill | The workflow is repeatable, triggerable, and benefits from references or scripts. | It is a one-off prompt or live-data lookup only. |
| API prompt package | The host needs explicit runtime controls, schemas, tools, and evals. | The user just needs interactive Codex execution. |

## OpenAI And GPT-5.6

Local Codex CLI 0.144.0 probes on 2026-07-09 verified these GPT-5.6 routes:

- `gpt-5.6-sol` with `model_reasoning_effort=ultra` for difficult, deep,
  review, or orchestrator work;
- `gpt-5.6-terra` with `model_reasoning_effort=high` for bounded workers;
- `gpt-5.6-luna` with `model_reasoning_effort=low` or `medium` for tiny
  mechanical work.

This local Codex proof does not establish Responses API deployment
availability. Verify the current official OpenAI model catalog and supported
controls before using the same IDs in API prompt packages. Treat a GPT-5.6
migration as a retune, not a model-string-only swap.

Default OpenAI API recipe for non-trivial prompt packages:

- Responses API over older chat-only flows when state, tools, multimodality, or
  agentic behavior matters.
- Select a provider-advertised GPT-5.6 deployment and supported reasoning
  effort from current official docs; do not assume Codex CLI tier IDs or effort
  values are portable to the API.
- Use evals to justify raising or lowering API reasoning effort.
- Use `text.verbosity` for visible answer length; do not raise reasoning effort
  just to get more detailed prose.
- Use Structured Outputs or strict function schemas for machine-readable
  outputs.
- Put most tool-specific guidance in tool descriptions.
- Use hosted tools for standard OpenAI-supported capabilities and custom
  functions for internal or side-effecting workflows.
- Use tool search for large tool catalogs when the model supports it.

Prompt caching recipe:

- Put stable system/developer rules, examples, tool definitions, and schemas
  before dynamic user or task context.
- Keep the exact static prefix stable across calls.
- Use a consistent `prompt_cache_key` when the deployment supports it.
- Track `cached_tokens` before claiming cache benefits.
- Recheck privacy, retention, ZDR, and regional implications per deployment.

State recipe:

- Prefer `previous_response_id` for stateful multi-turn Responses flows.
- For stateless or ZDR flows, replay the relevant returned output items.
- Preserve assistant output `phase` when manually replaying history.
- Pass reasoning items and function call outputs back as required by the API.

## Codex Task Prompt

Use this shape for a normal Codex task:

```text
Goal:
<specific outcome>

Context:
<repo/path/branch/files/errors/source docs/runtime proof>

Constraints:
<non-goals, approval boundary, sandbox/network limits, secret/privacy rules,
files to preserve, external side-effect limits>

Done when:
<tests/checks/screenshots/file readback/PR state/source citation proving done>
```

Use a normal prompt for one-off edits, short reviews, explanations, and tasks
with a clear path. Use `/plan` or a planning skill first when the finish line is
unclear. Use `/goal` only when the objective is durable and evidence-backed.

## Codex Native Goal Prompt

Official goal fields:

| Field | Purpose |
|---|---|
| Outcome | Concrete deliverable or state. |
| Verification surface | Evidence that proves completion. |
| Constraints | Rules that must hold while working. |
| Boundaries | In-scope, out-of-scope, and external-action limits. |
| Iteration policy | How Codex should plan, act, test, review, and continue. |
| Blocked stop condition | When to stop and what to report. |

Good `/goal` candidates:

- performance tuning with benchmarks;
- flaky test investigation;
- migration or refactor with clear tests;
- bug hunt requiring reproduction;
- research audit with source-backed final artifact;
- multi-step cleanup where the proof surface is known.

Bad `/goal` candidates:

- one-line edits;
- simple explanations;
- short code reviews;
- single-answer questions;
- vague finish lines;
- hidden or unresolved success criteria.

If the objective is long, store the detail in a file and point the goal at it.
`goal-post` is the artifact-backed pattern for that case.

## Skill And Agent Instructions

For skills:

- keep `SKILL.md` lean and trigger-focused;
- move long playbooks to `references/`;
- put deterministic helpers in `scripts/`;
- include positive and negative trigger guidance;
- include expected outputs and gotchas;
- validate YAML frontmatter after edits.
- run `skill-judge` before closeout and record the score, must-fix issues, and
  top three improvements.

### Skill Rewrite Quality Gate

Use this gate whenever the prompt package creates or rewrites a `SKILL.md`.
Score the draft with `skill-judge` and revise before finalizing if any of these
checks fail:

| Check | Pass condition |
|---|---|
| Trigger contract | Description states when to use the skill with searchable task terms, without summarizing the whole workflow. |
| Knowledge delta | Body captures expert judgment, decision rules, gotchas, or local workflow knowledge rather than generic tutorial text. |
| Progressive disclosure | Main `SKILL.md` stays lean; long, volatile, or rarely needed material moves to references with explicit load triggers. |
| Anti-patterns | Specific failure modes are named with why they matter. |
| Freedom calibration | Creative tasks get principles; fragile operational tasks get exact steps or scripts. |
| Evalability | The package includes validation commands, routing proof, or an `evals/evals.json` case set where the repo supports it, and labels structural validation separately from executed behavioral evals. |
| Refresh boundary | Model IDs, prices, context windows, feature flags, and deprecations are dated or delegated to current official docs. |

If `skill-judge` returns grade C or lower, do not ship the rewrite as-is. Either
apply the top fixes or report why the remaining issue is intentionally deferred.

For sub-agent packets:

- objective;
- non-goals;
- source pack;
- tool boundary;
- output schema;
- proof required;
- stop condition;
- privacy boundary.

## Tool Description Checklist

Tool descriptions should say:

- what the tool does;
- when to use it;
- when not to use it;
- required inputs and formats;
- output meaning;
- side effects;
- auth or privacy boundaries;
- idempotency and retry safety;
- common error modes.

Keep broad tool catalogs behind tool search or deferred loading when available.

## Eval And Refresh Loop

Prompt quality should improve through an eval flywheel:

1. Collect representative examples, regressions, near misses, and desired wins.
2. Define deterministic checks for exact output, schema, file, tool, or command
   behavior.
3. Add LLM graders only for semantic quality; validate them against human labels.
4. Keep a holdout set that is not optimized directly.
5. Compare old versus new prompts for quality, cost, latency, tool-call shape,
   schema adherence, and failure modes.
6. Label proof precisely: schema/frontmatter/eval-manifest validation proves
   structure, while executed fixtures or graders prove behavior.
7. Promote only after review; record rollback guidance.

Refresh triggers:

- a new OpenAI or Anthropic model release;
- changed official prompt guidance;
- deprecation notices;
- production prompt failures;
- new tool surfaces or schema requirements;
- material cost, latency, or cache changes.

Branch or release ledger entries should include source URLs, access quality,
access date, changed guidance, impacted files, eval results, and promotion or
rollback decision.

## Secondary Compatibility: Anthropic Claude

OpenAI/Codex is the default for this skill. For Anthropic targets, load
`references/claude-fable-5.md` — the dated per-model lane for the current
Anthropic flagship (Claude Fable 5, source check 2026-06-09). It covers
model facts, the `effort` control, Fable-5 prompt-style changes, long-run
agentic rules, verifier and memory design, migration recipes from Opus 4.x
and GPT-5.6, and the Claude Opus 4.8 fallback lane for safety-classifier
declines.

Never translate OpenAI `reasoning.effort` or Codex `model_reasoning_effort`
to Anthropic targets; re-derive controls from the per-model reference and
current official Anthropic docs.

## Templates

### API Prompt Package

```text
Target:
<model/provider/surface>

Prompt:
<system/developer/user prompt text>

Runtime controls:
<model, reasoning, verbosity, schema, tools, tool_choice, cache, state>

Validation:
<fixtures, graders, commands, screenshots, acceptance criteria>

Refresh triggers:
<model release, docs change, eval regression, cost/latency change>
```

### Skill Rewrite Package

```text
Skill:
<path>

Trigger contract:
<when to use / when not to use>

Body:
<lean workflow>

References:
<long or volatile guidance moved to references/>

Validation:
<frontmatter parse, local tests, routing proof, stale-claim audit>

Skill-judge:
<score/grade, must-fix issues, top three improvements, deferred risks>
```

### Goal Package

```text
Outcome:
<deliverable>

Verification surface:
<proof>

Constraints:
<rules>

Boundaries:
<scope and side-effect limits>

Iteration policy:
<plan, act, test, review, continue>

Blocked stop condition:
<when to stop and what to report>
```

## Final Anti-Pattern Check

Before finalizing any prompt package, remove or fix:

- vague persona-first prompting;
- missing done/proof surface;
- prompt-only schemas when strict schemas are available;
- hidden external side effects;
- missing tool privacy or retry boundaries;
- stale model/pricing/context claims;
- provider-specific controls used as universal controls;
- overlong reusable instructions pasted into every run;
- skill rewrites with no judge pass or eval hook;
- no eval or validation plan for model migrations.
