# Goal-Backed Phase Pipeline Playbook

This playbook shows how to compose the common planning and delivery skills into
one reliable operator workflow. It is written for beginners and agents: each
stage explains the idea plainly, gives a template, and shows what good output
looks like.

## Source Of Truth

This playbook is the source of truth for the shared phase-pipeline process. The
individual skill files should keep their own activation rules, constraints,
templates, and execution details, then link here for the common order of
operations. When a detail is useful to every phase-pipeline skill, keep it here
instead of repeating it across `SKILL.md` files.

Beginner default: read this playbook first when the user is trying to understand
which skill comes next. Advanced default: load only the specific skill file plus
this playbook section that matches the current branch point.

The short version:

1. Use `skill-oracle` to choose the right skills before planning.
2. Use `phase-plan` to create the decision record and dependency graph.
3. Use `think` at branch points to simplify the operator's next move.
4. Use `deep-sweep` when risk signals show the plan needs a gap hunt.
5. Use `deep-build` when implementation needs executable build packets.
6. Use `goal-post` only for longer autonomous runs that should launch through
   Codex native `/goal`.
7. Use `ultra-review`, `deep-clean`, and `browser-harness` as proof and repair
   gates when the phase touches code, cleanup, UI, browser workflows, or PR
   readiness.

## Beginner Mental Model

A phase is not a to-do list. A phase is a promise that a specific outcome can
be delivered, verified, and handed off without hidden context.

Think of the pipeline as a relay:

- `skill-oracle` chooses the right tools.
- `phase-plan` writes the map.
- `think` resolves confusing forks in the road.
- `deep-sweep` finds gaps before they become build failures.
- `deep-build` turns the map into execution packets.
- `goal-post` packages the plan for a long-running autonomous loop.
- Review, cleanup, and browser proof keep the result honest.

## How The Skill Files Should Use This

Each anchor skill keeps a local contract:

- `skill-oracle` owns discovery and routing.
- `phase-plan` owns the planning artifact shape and validation gates.
- `think` owns operator simplification at branch points.
- `deep-sweep` owns risk discovery, gap registers, and red-team analysis.
- `deep-build` owns implementation packets and cross-verified execution.
- `goal-post` owns goal artifacts and short `/goal` prompts.
- `ultra-review`, `deep-clean`, and `browser-harness` own proof, repair, and
  browser evidence.

Do not move these skill-specific contracts into the playbook. Do move repeated
shared-process explanations here: when to run the next skill, what beginners
should inspect first, evidence-packet expectations, and handoff language.

## Stage 0 - Fresh Context

Plain-language purpose: do not plan against stale repo state. Before making a
phase, confirm the current branch, live remote, open PRs, and local changes.

Template:

```text
Freshness:
- Repo state checked: <command/output summary>
- Source branch checked: <remote/ref>
- Open PRs/issues checked: <links or none>
- Dirty worktree risk: <none / isolated in worktree / blocked>
```

Example:

```text
Freshness:
- Repo state checked: clean worktree on team/main
- Source branch checked: fetched team/main on 2026-05-11
- Open PRs/issues checked: PR #229 is adjacent training work, not a blocker
- Dirty worktree risk: current checkout dirty, implementation uses clean worktree
```

## Stage 1 - Skill Discovery with `skill-oracle`

Plain-language purpose: ask the skill graph what should be used before the
operator guesses. Run it before drafting, and rerun it when scope changes.

Hard gate:

- Required before the first phase draft.
- Required again if the phase gains a new domain, repo, UI workflow, deploy
  target, data source, or autonomous-run branch.
- Record selected skills and rejected-but-relevant skills.

Template:

```text
Skill discovery:
- Query: <capability or task>
- Selected skills: <skill -> why>
- Rejected skills: <skill -> why not now>
- Missing skills/fallbacks: <gap -> fallback>
```

Example:

```text
Skill discovery:
- Query: goal-backed phase pipeline with sweep/build/goal-post automation
- Selected skills: phase-plan, skill-oracle, think, deep-sweep, deep-build,
  goal-post, ultra-review, deep-clean, browser-harness
- Rejected skills: karpathy-guidelines -> advisory lens, not a hard gate
- Missing skills/fallbacks: prompt-optimizer -> use manual short-prompt check
```

## Stage 2 - `phase-plan` as Orchestrator and Record

Plain-language purpose: make one durable artifact that says what the phase is,
why it matters, what is in scope, what is out of scope, and how agents should
execute it.

Required sections:

- Original user request, verbatim.
- Product or operator frame.
- Current state and dependencies.
- Skill discovery summary.
- Workstreams or build packets.
- Risks, assumptions, and stop conditions.
- Proof requirements.
- Next branch: manual execution, `deep-sweep`, `deep-build`, or `goal-post`.

Template:

```text
Phase decision:
- Outcome: <one sentence>
- Audience: <operator / engineer / external>
- In scope: <items>
- Out of scope: <items>
- Hard gates: <checks>
- Next branch: <manual / deep-sweep / deep-build / goal-post>
```

Example:

```text
Phase decision:
- Outcome: beginner-runable playbook for goal-backed phase delivery
- Audience: operators supervising Codex/Claude/Podhi agents
- In scope: shared playbook, the project applied phase, sample goal artifact
- Out of scope: installed skill sync, production deploy, UI changes
- Hard gates: skill validation, security scan, graph rebuild, PR proof
- Next branch: deep-sweep because the work is cross-repo and skill-router
  metadata changes
```

## Stage 3 - `think` at Branch Points

Plain-language purpose: use `think` when the operator has too many possible
paths. It selects a thought pattern and makes the next move obvious.

Hard gate:

- Required at branch points.
- Not required for every routine step.
- Output a visible decision card, not raw scratchpad.

Branch signals:

- Multiple valid next skills.
- Conflicting delivery paths.
- Scope is growing.
- The operator cannot tell whether a task is planning, sweeping, building, or
  goal-loop work.

Decision card template:

```text
Think decision card:
- Situation: <what is confusing>
- Pattern used: <simplify / compare / sequence / isolate>
- Recommended next move: <action>
- Why this reduces complexity: <one sentence>
```

Example:

```text
Think decision card:
- Situation: two repos need updates and the the project checkout is dirty
- Pattern used: isolate
- Recommended next move: create clean worktrees for both repos
- Why this reduces complexity: it prevents unrelated local changes from entering
  either PR
```

## Stage 4 - `deep-sweep` for Discovery, Risk, and Gaps

Plain-language purpose: run a sweep when the plan could be wrong because the
surface is broad, stale, cross-repo, cross-module, or evidence-heavy.

Trigger threshold:

Run `deep-sweep` when any two risk signals are present:

- Cross-repo change.
- Cross-module or shared-contract change.
- Unclear requirements.
- Active PR or phase overlap.
- New domain or unfamiliar system.
- Hidden data, deploy, browser, or provider dependency.
- Skill-router or generated-graph metadata change.

Required output:

```text
Deep-sweep output:
- Findings: <facts discovered>
- Affected surfaces: <repos/files/systems>
- Gap register: <gap -> patch item>
- Dependencies: <upstream/downstream>
- Go/amber/stop: <decision and reason>
```

Gap patch rule:

Every material gap becomes a named patch-plan item before `deep-build`. Do not
hide gaps inside vague implementation tasks.

## Stage 5 - `deep-build` for Executable Packets

Plain-language purpose: turn the locked plan, sweep findings, and gap register
into packets an implementation agent can execute without making new decisions.

Trigger threshold:

Run `deep-build` when the phase changes code, schemas, deploy behavior,
cross-agent contracts, skill-router metadata, user-visible workflows, or any
work requiring proof beyond docs review.

Packet template:

```text
Build packet:
- Goal: <specific outcome>
- Likely surfaces: <files/systems>
- Inputs: <source docs/artifacts>
- Validation: <commands/checks>
- Proof artifact: <PR/check/deploy/screenshot>
- Rollback: <how to undo safely>
- Done condition: <observable completion>
```

Example:

```text
Build packet:
- Goal: add shared phase pipeline playbook
- Likely surfaces: skills/phase-plan/references, workflow-anchor SKILL.md files
- Inputs: approved phase plan and goal-post template
- Validation: frontmatter validator, security scan, graph rebuild, router tests
- Proof artifact: public-skills PR with validation summary
- Rollback: revert the playbook commit and regenerated skill graph artifacts
- Done condition: PR green and linked from the project phase plan
```

## Stage 6 - `goal-post` for Long-Running `/goal`

Plain-language purpose: do not paste a long plan into Codex `/goal`. Store the
long context in a Markdown artifact, then launch `/goal` with a short pointer.

Use `goal-post` only when the task is long-running, autonomous, or needs a run
ledger. It is optional for small docs-only work.

Artifact rules:

- Store under `docs/planning/goals/`.
- Use `<phase-key>__<goal-slug>.md`.
- Keep the short `/goal` prompt under 300 characters.
- Include stop conditions, evidence pack, run ledger, successor-phase policy,
  and the strategy-confidence loop.
- Do not execute `/goal` unless the user separately asks.

Default short prompt:

```text
/goal Execute @docs/planning/goals/<file>.md autonomously. Read it, follow the run ledger, create successor phases as needed, run the strategy-confidence loop until 100% certain, and stop only at done or a stop condition.
```

For Codex native goal mode, launch with:

```text
/goal budget 1000000
/goal Execute @docs/planning/goals/<file>.md autonomously. Read it, follow the run ledger, create successor phases as needed, run the strategy-confidence loop until 100% certain, and stop only at done or a stop condition.
```

Before launching, verify the active Codex environment supports native `/goal`
(`codex features list` should show `goals` enabled). `goal-post` should record
the expected routing from the active `config.toml`; it should not edit Codex
configuration unless the user explicitly asks for configuration changes.

## Stage 7 - Review, Cleanup, and Browser Proof

Plain-language purpose: proof is what lets the operator know the phase is
actually done.

Use these gates when relevant:

- `ultra-review`: broad review before PR readiness or after implementation.
- `deep-clean`: scoped cleanup only when review or sweep finds cleanup that is
  necessary for the phase.
- `browser-harness`: mandatory for UI, logged-in browser, admin, posting,
  provider, or live workflow evidence.

Evidence packet template:

```text
Evidence packet:
- Branch/PR: <link>
- Checks: <command summaries>
- Review: <review skill/findings summary>
- Browser proof: <localhost / PR preview / Vercel preview / live production>
- Deploy proof: <URL/commit/timestamp or N/A>
- Linear/issues: <status and proof link>
- Remaining risks: <none or listed>
```

Environment labels:

- `localhost`: local dev server or local browser proof.
- `PR preview`: PR-scoped preview proof.
- `Vercel preview`: Vercel preview deployment proof.
- `live production`: public production proof only after merged production deploy
  is confirmed.

## Optional Long-Run Observer Appendix

For very long autonomous runs, pair Codex native `/goal` with observer tooling:

- `agent-message-bus` for durable progress, blocker, correction, and pause
  messages.
- `claude-heartbeat-loop` for periodic supervision and course correction.
- `crow-nest` for read-only dashboard visibility.

Beginner default: skip observer setup unless the run may last hours, has
multiple agents, or needs external monitoring.

## Final Readiness Checklist

Before calling a phase ready:

- `skill-oracle` ran and selected skills are recorded.
- `phase-plan` captures the verbatim request, scope, risks, and proof.
- `think` decision cards exist for major branch points.
- `deep-sweep` ran if two or more risk signals were present.
- Material gaps have patch-plan items.
- `deep-build` packets exist for implementation-risk work.
- `goal-post` artifact exists only if a long-running `/goal` branch is needed.
- Evidence packet links the PR, checks, review, browser/deploy proof when
  relevant, and issue completion state.
- Linear or issue tracker items are marked complete only after proof is linked.
