---
name: codex
description: "Run or advise on OpenAI Codex CLI, Codex prompts, Codex /goal runs, app-server workflows, and Codex-backed code analysis or editing."
metadata:
  author: community
  version: 1.4.0
related_skills:
  - build
  - code-review
  - prompt-generation
  - openai-docs
  - claude
  - goal-post
  - agent-message-bus
  - claude-heartbeat-loop
  - crow-nest
---

# Codex

Use this skill when the user asks for Codex CLI usage, Codex prompt design,
Codex `/goal`, Codex app-server, or Codex-backed code work.

For current model, pricing, context-window, and prompt-behavior claims, use the
`openai-docs` skill first. Static model tables in skills go stale quickly.

## Prompt Contract

A strong Codex prompt has four parts:

1. Goal: the concrete outcome.
2. Context: repo path, files, errors, source docs, branch, PR, or runtime state.
3. Constraints: non-goals, approval boundary, sandbox/network limits, secrets,
   user-work preservation, and any external side-effect limits.
4. Done when: tests, commands, screenshots, file readbacks, PR/check state, or
   another evidence surface that proves completion.

Use `prompt-generation` when building reusable Codex prompts, model-migration
prompts, eval-backed prompts, or skill instructions.

## Running Codex CLI

Use the GPT-5.6 tier family by default. Pass model and effort explicitly when
the run is delegated or reproducibility matters:

- `gpt-5.6-sol` with `ultra` for difficult, deep, review, or orchestrator work.
- `gpt-5.6-terra` with `high` for bounded worker tasks.
- `gpt-5.6-luna` with `low` or `medium` for tiny mechanical tasks.

GPT-5.6 is preview-access gated. First confirm `codex debug models` lists all
three IDs and the required effort levels; this proves installed catalog support,
not account entitlement. After login, run a live read-only probe for the selected
tier. If either check fails, update Codex or report the entitlement blocker
instead of silently downgrading. Source checked
2026-07-09: `https://help.openai.com/en/articles/20001325-a-preview-of-gpt-5-6-sol-terra-and-luna`.

Useful flags:

- `-m, --model <model>`: explicit model.
- `-c model_reasoning_effort=<low|medium|high|xhigh|max|ultra>`: Codex reasoning effort.
- `-c model_verbosity=<low|medium|high>`: visible output detail where supported.
- `--sandbox <read-only|workspace-write|danger-full-access>`: execution scope.
- `-o, --output-last-message <file>`: write only the final message to a file —
  the cleanest result hand-back for scripts and orchestrators.
- `--json`: JSONL event stream on stdout; `--output-schema <file>`: constrain
  the final response to a JSON Schema (validate the output anyway).
- `codex exec resume --last` (or a session id): continue a prior exec thread.
- `-C, --cd <dir>`: run from another directory.
- `--skip-git-repo-check`: only when the task intentionally runs outside a git
  repo or this local wrapper requires it.

Do not pipe large prompts through stdin. For prompt bodies above a few KB,
write or reference a file and ask Codex to read it.

For delegating work from Claude (Fable orchestrator lane) — single
delegations, parallel fan-outs, ultracode sessions — see
`references/fable-codex-orchestration.md`.

When model or effort choice materially changes cost, latency, or result quality,
state the default you will use and why. Ask the user only when the choice is
truly ambiguous or high impact.

## Reasoning And Verbosity

Use official OpenAI docs for volatile provider/API guidance. Local Codex CLI
0.144.0 probes on 2026-07-09 verified the three GPT-5.6 tier IDs and the
`ultra` effort route:

- `gpt-5.6-sol` plus `ultra` is the difficult/deep/review/orchestrator route.
- `gpt-5.6-terra` plus `high` is the bounded worker default.
- `gpt-5.6-luna` plus `low` is the tiny-task default; use `medium` when the
  task is still small but needs more care.
- `max` and `ultra` are advanced Codex effort values. Keep `ultra` paired with
  Sol for the hardest route instead of raising every worker's effort.
- API-only controls such as `reasoning.effort: none`, `text.verbosity`, hosted
  tools, Structured Outputs, and Responses state replay belong in API prompts,
  not blindly in Codex CLI commands.
- Codex `model_reasoning_effort` values are OpenAI-specific; never carry them
  to Anthropic targets — for Claude prompt ports, load `prompt-generation`
  `references/claude-fable-5.md`.

For API prompt design, separate prompt content from runtime controls:

- Prompt content: goal, context, constraints, done/proof, tool boundaries, stop
  rules, and user-facing style.
- Runtime controls: model, reasoning effort, verbosity, schema, tool set,
  `tool_choice`, prompt caching, and state replay.

## Native `/goal`

Use Codex native `/goal` for durable objectives with a clear finish line,
multi-step or uncertain paths, and an evidence surface that can prove done.
Do not use `/goal` for one-line edits, simple explanations, short reviews,
single-answer questions, or vague finish lines.

Official goal fields to include:

- Outcome: what must be delivered.
- Verification surface: how Codex proves the goal is complete.
- Constraints: repo, safety, approval, tool, and style limits.
- Boundaries: in scope, out of scope, and external-action limits.
- Iteration policy: how Codex should plan, act, test, review, and continue.
- Blocked stop condition: when to stop and what evidence to report.

Current documented slash-command shape:

- `/goal <objective>`: set a goal.
- `/goal`: view the current goal.
- `/goal pause`: pause without losing the goal.
- `/goal resume`: continue a paused goal.
- `/goal clear`: remove the goal.

Keep goal objectives concise. If the instructions are long, store them in a
file and point the goal at that file. Use `goal-post` when the user needs a
project-stored goal artifact with a short launch prompt.

If `/goal` is unavailable in the local CLI, first update or verify Codex and
check the current official Codex slash-command docs. Treat feature flags,
issue-number workarounds, and version-specific behavior as dated local
troubleshooting notes unless current docs or current CLI proof confirms them.

## App-Server

`codex app-server` exposes Codex over JSON-RPC for clients and dashboards. Use
current Codex docs or local CLI help before relying on experimental methods or
capabilities. Do not expose capability tokens, auth state, session transcripts,
or raw secrets in skill docs or reports.

## AGENTS.md

Codex reads the nearest `AGENTS.md` as workspace guidance. Keep it short and
operational:

- build, test, lint, and verification commands;
- repo conventions and non-goals;
- approval and side-effect boundaries;
- project-specific tool routing;
- message-bus or goal-loop protocols when needed.

Do not store secrets, OAuth state, cookies, or session contents in `AGENTS.md`.

## Follow-Up

After a Codex run, report:

- command or surface used;
- model or effort only when it materially matters;
- files changed or evidence inspected;
- tests, checks, screenshots, or blockers;
- how to resume when a resumable session exists.
