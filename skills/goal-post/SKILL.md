---
name: goal-post
description: >
  Create short /goal prompts backed by full project-stored Markdown goal
  artifacts. Use when the user wants a goal prompt, autonomous delivery prompt,
  phase-plan execution prompt, successor phase loop, evidence pack, run ledger,
  or reusable artifact that turns a /phase-plan into a guarded self-verifying
  loop using skill-oracle, phase-plan, deep-sweep, deep-build, ultra-review,
  deep-clean, browser-harness, and follow-up phase plans. Artifacts ship with
  preflight uncertainty ranking (propose-and-proceed, not open-ended
  questions), priority-tier scope control, per-gate rollback plans, a
  fresh-context verifier gate, and a closing strategy-confidence loop.
related_skills: [vision-lock, phase-plan, skill-oracle, think, deep-sweep, deep-build, ultra-review, deep-clean, browser-harness, loophole-loop, codex, prompt-generation, agent-message-bus, claude-heartbeat-loop, crow-nest]
---

# Goal Post

> **Naming note - Codex native `/goal` is a separate feature.** Codex's
> native `/goal` is the thread goal lifecycle in the `codex` skill - see
> `codex/SKILL.md` § "Native `/goal`". This
> skill (`goal-post`) is **independent**: it generates a goal-artifact
> markdown file and emits a *short prompt that references that
> artifact*. The short prompt may use Codex `/goal` syntax as one of
> several launch surfaces, but the artifact-template machinery is
> goal-post's own. If you want long-horizon Codex autonomy with a
> peer-coordination heartbeat, see `codex`, `agent-message-bus`,
> `claude-heartbeat-loop`, and `crow-nest`. When the launch surface is
> Codex native `/goal`, follow the current official slash-command and Goals
> cookbook guidance rather than hardcoded issue workarounds.

Turn an existing `/phase-plan` or long delivery prompt into a durable Markdown
goal artifact, then output a tiny `/goal` prompt that references that artifact.

## Source Of Truth

When `goal-post` is part of a phase workflow, read
`skills/phase-plan/references/09_PHASE_PIPELINE_PLAYBOOK.md`. The playbook owns
the shared beginner path, phase-pipeline order, and when to branch from a normal
phase plan into a long-running `/goal` artifact.

This skill owns only the goal-post contract: find the source phase, create or
update the goal artifact from `references/goal-artifact-template.md`, generate a
short prompt, and enforce the safety checks below. The artifact carries the
detail. The `/goal` prompt stays short enough for goal-command limits.

## Use This For

- Building a reusable `/goal` prompt from a phase plan.
- Capturing an autonomous loop that should plan, sweep, build, review, fix,
  browser-verify, and create successor phase plans when needed.
- Preserving source-of-truth folders, PR/deploy context, workbook/manual-input
  mappings, provider/API verification requirements, transcript requirements,
  and browser evidence in one auditable artifact.
- Giving beginners a single Markdown file they can inspect before launching a
  long agent run.

## Core Rules

- Store artifacts in the active project at `docs/planning/goals/`.
- Name files as `<phase-name-or-number>__<goal-slug>.md`.
- Mention the phase name in the artifact title and metadata.
- Keep the final `/goal` prompt under 300 characters.
- Official Codex `/goal` can carry a longer objective, but `goal-post` house
  style keeps the launch prompt short and stores detail in the artifact.
- The `/goal` prompt must reference the artifact path; do not paste the full
  plan into `/goal`.
- Artifacts always use `references/goal-artifact-template.md`; include every
  section and mark irrelevant sections `N/A` with a brief reason.
- Include a lightweight run ledger and successor-phase policy. If the current
  phase or PR cannot satisfy the definition of done, the agent creates the next
  numbered phase plan after doing discovery first.
- Do not store passwords, API keys, cookies, admin credentials, or live session
  details. Refer to existing secret stores or the user's already logged-in
  browser session.
- Do not execute the goal loop unless the user separately asks to run it.
- Every artifact must include a `## Verifier Gate`: before the run ledger is
  marked done, dispatch a fresh-context verifier subagent that checks the
  Definition Of Done and every Verification Gate row against on-disk evidence
  only — never the actor's transcript or reasoning. The agent that produced
  the work must not grade it. The verdict uses the strict schema in the
  template.
- Every generated artifact must end with a `## Strategy Confidence Loop`
  section. It runs after the Verifier Gate, may not override a verifier
  failure, and exits on an evidence-backed confidence statement citing gates,
  capped at 3 iterations.
- The short `/goal` prompt must reference the verifier gate and
  strategy-confidence loop so the instructions survive even if the agent
  never opens the artifact.
- Every artifact must include `## Preflight Uncertainty Ranking` populated
  before the Autonomous Loop begins. The agent proposes the highest-confidence
  resolution for each uncertainty and proceeds; open-ended clarification
  questions during a run are forbidden. The user may amend any proposal.
- Every artifact must include `## Priority Order` with explicit P0/P1/P2…
  ranking of in-scope items. If time, tokens, or live access force a scope
  cut, the agent drops work from the lowest priority up and records the cut
  in the run ledger and Final Report. Every P0 item must appear in
  § Definition Of Done.
- Every `§ Verification Gates` row must include a `Rollback Plan`. Read-only
  gates use `N/A (read-only)`; destructive or high-risk gates require a
  specific revert command, deploy rollback, or revert PR plus owner.
- Before any non-trivial change, the executing agent restates the goal,
  constraints, and § Priority Order in one paragraph; that restatement is the
  contract for the run.
- Every artifact must include the official native-goal contract: Outcome,
  Verification surface, Constraints, Boundaries, Iteration policy, and Blocked
  stop condition.
- Every artifact must pin a `## Frozen Original Intent` block copied from
  `docs/references/vision-lock.md` at creation. It is immutable for the run, and
  the Verifier Gate grades the finished build against it (the Matt-test) — not
  only the Definition Of Done. If no `vision-lock.md` exists, stop and run
  `vision-lock` first; never infer intent from the phase plan alone.
- Every artifact must include a `## Product-Truth Launch Gate`: before the
  Verifier Gate, one real Matt-test outcome is proven against data the build did
  not author — for a product/UI goal, in the freshly launched real app (desktop +
  mobile); for a non-UI goal (backend, data, infra, docs, process), against the
  goal's real verification surface (a live endpoint, a real query result, a
  deployed job), with the launch/mobile fields marked `N/A` + a one-line reason.
  A real surface is mandatory either way — `N/A` never means skip the proof.
  Self-validating scripts, source string-checks, and "it compiles" are
  inadmissible as acceptance evidence regardless of goal type.
- Every artifact must include a `## Drift Gate`, run before each successor phase
  and the done-gate. A tripped drift signal halts successor creation and triggers
  a scoped `deep-sweep` or escalation; a green per-phase DoD does not authorize
  continuing through drift.

## Workflow

0. **Confirm the frozen intent exists.** Check for
   `docs/references/vision-lock.md`. If it is missing, stop and run `vision-lock`
   first — the artifact's `## Frozen Original Intent` block and the Verifier
   Gate's Matt-test both depend on it. Never infer intent from the phase plan
   alone.

1. **Find the source phase.**
   - If the user provides a phase path, use it.
   - Otherwise inspect `docs/planning/phase-*/plan.md` and choose the relevant
     or latest phase.
   - If no phase plan exists, ask the user to run `/phase-plan` first.

2. **Read enough context.**
   - Read the root `plan.md`.
   - Read each subphase `plan.md` under that phase.
   - Capture objective, dependencies, lanes, acceptance criteria, verification
     gates, risks, and explicit non-goals.

3. **Create the goal artifact.**
   - Use `references/goal-artifact-template.md`.
   - Write to `docs/planning/goals/<phase-key>__<goal-slug>.md`.
   - Prefer a clear slug like `ad-spend-pipeline-verification` over a generic
     slug like `goal`.
   - Preserve any source-of-truth folders, PR links, branch names, dates,
     workbook/transcript references, provider docs, and live verification
     requirements from the user's prompt.
   - Populate the native-goal contract fields before writing the autonomous
     loop.

4. **Generate the short prompt.**
   - Use this default shape:

```text
/goal Execute @docs/planning/goals/<file>.md. Done only when every gate passes — Frozen Intent (Matt-test), DoD, Verification, Product-Truth Launch, Verifier — and Strategy Confidence Loop closes; else stop with blocker evidence.
```

5. **Check the prompt.**
   - If it exceeds 300 characters, shorten it.
   - If it omits the artifact path, fix it.
   - If it omits the verifier-gate or strategy-confidence loop reference, add
     it back.
   - If it includes secrets or large pasted context, remove them.

## Artifact Contract

Use `references/goal-artifact-template.md` as the schema. Do not omit sections:
the evidence pack, source mapping table, autonomous loop, successor policy, run
ledger, model routing, verification gates, verifier gate, stop conditions,
final report requirements, and closing `## Strategy Confidence Loop` all stay
in the artifact. If a section does not apply, mark it `N/A` and say why.

## Guarded Autonomous Authority

When the artifact explicitly names PR, deploy, or live-browser work, it may
authorize the agent to review, fix, merge, deploy, and verify through the
normal project workflow. It must still stop for:

- destructive data changes or production-risk ambiguity without explicit user
  approval;
- missing credentials, missing logged-in browser access, or unavailable provider
  access;
- critical/high review findings that remain unresolved;
- branch protection, CI, or mergeability failures that cannot be fixed safely;
- any request to force-push, force-merge, or bypass project policy unless the
  user explicitly repeats that instruction for the active repo and branch.

## Model And Agent Defaults

- Use the current highest-reasoning configured model — OpenAI/Codex or
  Anthropic Claude — verified at execution time, or the active config default,
  for main planning, synthesis, and final judgment.
- Use current configured smaller or cheaper models for bounded research,
  exploration, and review lanes when the harness supports them.
- Record concrete model IDs only after current docs or local config prove them.
- When the executor is Claude (Fable 5), load `prompt-generation`
  `references/claude-fable-5.md`: effort high by default, audit each progress
  claim against a tool result from this session, and propose-and-proceed on
  reversible actions instead of pausing.
- Use the existing agent roles/model routing from the active `config.toml`.
  Goal Post should record expected routing, not edit configuration.
- Use browser-harness for live logged-in UI verification; use Browser Harness only
  for isolated headless tests or CI-style checks.

## Anti-Patterns

- Do not make `/goal` carry the whole phase plan.
- Do not generate a vague goal like "finish the project"; define the exact
  artifact-backed delivery loop.
- Do not use "Research" as a phase-plan step. Inspect sources first, then write
  a plan around the actual solution.
- Do not skip browser verification for UI or platform workflows.
- Do not create a second phase plan when an adequate source phase can be updated
  safely; create a successor only when needed to satisfy the definition of done.
- Do not let "autonomous" mean unbounded. Include stop conditions.
- Do not ask open-ended clarification questions during a run. Use the
  Preflight Uncertainty Ranking propose-and-proceed pattern; the user may
  amend a proposal, but the agent does not block on questions.
- Do not invent architecture, behavior, or requirements that are not in the
  source phase plan or upstream artifacts. Surface anything missing as a
  Preflight Uncertainty Ranking row; do not silently assume.
- Do not expand scope after the definition of done is satisfied. Declare done
  and emit the Final Report; further work belongs in a successor phase only
  when DoD is genuinely not yet met.
- Do not silently re-rank § Priority Order to make a scope cut look painless.
  Log the cut explicitly in the run ledger and the Final Report.
- Do not invent a Rollback Plan mid-run. If a gate fails irreversibly and the
  documented rollback is missing or wrong, halt and escalate per § Stop
  Conditions.
- Do not infer intent from the phase plan alone; pin it from the frozen
  `vision-lock.md` as `## Frozen Original Intent`.
- Do not accept self-validating scripts, source string-checks, or "tests pass"
  as product-truth proof. Acceptance evidence comes from a fresh real-app launch
  against data the build did not author.
- Do not keep spawning successor phases through drift just because each phase's
  Definition Of Done is green. A tripped § Drift Gate signal halts and escalates.
