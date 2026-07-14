# Goal Artifact Template

Use this template when `goal-post` creates or updates a project goal artifact.
The artifact carries all long context. The `/goal` prompt references this file
and stays under 300 characters.

Always include every section. If a section does not apply, write `N/A` plus a
brief reason so later agents know it was considered.

````markdown
---
goal_name: "<goal-slug>"
source_phase: "docs/planning/phase-<N>/plan.md"
source_phase_name: "<Phase Name>"
created_at: "<YYYY-MM-DD>"
short_goal_prompt_max_chars: 300
native_goal_objective_max_chars: 4000
goal_post_prompt_style: "artifact-pointer"
authority: "guarded-autonomous"
status: "not-started"
---

# <Phase Name> Goal: <Goal Title>

## Frozen Original Intent (immutable)

Pinned from `docs/references/vision-lock.md` at creation — do NOT edit during the
run. The Definition Of Done below is the mutable, plan-level done-list; THIS is
the day-one truth the finished build is judged against. If no `vision-lock.md`
exists, STOP and run `vision-lock` first — never infer intent from the phase
plan alone.

- Building (Matt's words): `<one real end-to-end outcome>`
- Matt-test (binding): `<3-5 product-truth checks from vision-lock>`
- Design target: `<frozen packet path or N/A>`
- Out of scope / anti-goals: `<items>`
- Canonical repo + branch: `<repo @ branch>`

## Short /goal Prompt

```text
/goal Execute @docs/planning/goals/<file>.md. Done only when every gate passes — Frozen Intent (Matt-test), DoD, Verification, Product-Truth Launch, Verifier — and Strategy Confidence Loop closes; else stop with blocker evidence.
```

## Objective

Deliver <specific outcome> from <source phase> end to end.

## Codex Native Goal Contract

Use this table when the launch surface is Codex native `/goal`. The short goal
prompt can point at this artifact, but the artifact must still make completion
auditable.

| Field | Value |
|-------|-------|
| Outcome | `<specific deliverable or state>` |
| Verification surface | `<tests, screenshots, benchmarks, source citations, file readbacks, PR/check state, or other proof>` |
| Constraints | `<repo, safety, approval, tool, privacy, and style limits>` |
| Boundaries | `<in scope, out of scope, and external-action limits>` |
| Iteration policy | `<how to plan, act, test, review, fix, and continue>` |
| Blocked stop condition | `<when to stop and what evidence/next input to report>` |

## Definition Of Done

- `<done criterion 1>`
- `<done criterion 2>`
- `<done criterion 3>`

## Guarded Authority

The executing agent may review, fix, merge, deploy, and browser-verify only when
those actions are explicitly part of this artifact and normal project policy
allows them.

The agent must stop for destructive data changes, missing access, unresolved
critical/high blockers, branch protection failures, production-risk ambiguity,
or requests that would require bypassing repo policy.

## Source Context

- Repo: `<absolute repo path>`
- Source phase: `docs/planning/phase-<N>/plan.md`
- Subphase plans: `<list paths>`
- Current branch/PR/deploy context: `<branch, PR, commit, deploy target>`
- Unrelated files to leave untouched: `<paths or N/A>`
- Current date assumption: `<YYYY-MM-DD if provided, otherwise actual date>`

## Source-Of-Truth Inputs

- Planning docs: `<paths>`
- Process docs: `<paths>`
- Workbooks/spreadsheets: `<paths or links>`
- Transcripts/meeting notes: `<paths>`
- Provider/API docs: `<docs to verify>`
- Live provider data/API checks: `<systems and windows>`
- Browser/admin workflows: `<routes or workflows>`
- Other evidence sources: `<paths/systems>`

## Evidence Pack

### PR And Branch Evidence

| Item | Value | Verification Method | Status |
|------|-------|---------------------|--------|
| PR | `<PR or N/A>` | `gh pr view`, comments, checks | `pending` |
| Branch | `<branch>` | `git status`, `git log` | `pending` |
| Commit | `<commit>` | `git show` | `pending` |
| CI | `<checks>` | provider/GitHub checks | `pending` |

### Deploy Evidence

| Item | Value | Verification Method | Status |
|------|-------|---------------------|--------|
| Deploy target | `<prod/staging/preview>` | Vercel/GitHub/browser | `pending` |
| Deploy URL | `<url or N/A>` | Vercel/browser-harness | `pending` |
| Release/rollback | `<notes>` | deploy logs | `pending` |

### Source API And Provider Evidence

| Provider | Account/Scope | Date Window | Data To Verify | Method | Status |
|----------|---------------|-------------|----------------|--------|--------|
| `<provider>` | `<account/scope>` | `<window>` | `<totals/rows>` | `<API/query>` | `pending` |

### Workbook And Manual Input Evidence

| Workbook/Sheet/Line | Meaning | Manual Input Or Formula | Platform Source | Verification Method | Status |
|---------------------|---------|--------------------------|-----------------|---------------------|--------|
| `<line>` | `<meaning>` | `<manual/formula>` | `<source>` | `<method>` | `pending` |

### Transcript And Product Requirement Evidence

| Transcript/Doc | Requirement | Source Dependency | UI/Model Impact | Follow-Up Needed |
|----------------|-------------|-------------------|-----------------|------------------|
| `<path>` | `<requirement>` | `<dependency>` | `<impact>` | `<yes/no>` |

### Browser Evidence

| Workflow | Route/Target | Expected Evidence | Tool | Status |
|----------|--------------|-------------------|------|--------|
| `<workflow>` | `<route>` | `<screenshot/data>` | `browser-harness` | `pending` |

## Source Mapping Table

Use this whenever source docs, workbooks, manual inputs, provider APIs, or UI
cells must be cross-compared.

| Source/manual line | Source system/API/table | Platform field | Forecast UI row/cell | Verification method | Status |
|--------------------|-------------------------|----------------|----------------------|---------------------|--------|
| `<line>` | `<source>` | `<field>` | `<ui>` | `<method>` | `pending` |

## Preflight Uncertainty Ranking

Run this before § Autonomous Loop. For every uncertainty that could change the
plan, propose the highest-confidence resolution and proceed unless the user
explicitly amends it. Open-ended clarification questions during a run are
forbidden; surface them here as ranked proposals, log the resolution in the
run ledger, and continue.

| # | Uncertainty | Impact if wrong | Proposed resolution | Confidence | User amendment |
|---|-------------|-----------------|---------------------|------------|----------------|
| 1 | `<claim or missing detail>` | `<plan-level impact>` | `<best-guess resolution>` | `<0-100%>` | `<none / edit>` |

Rules for this section:

- Inventing architecture, behavior, or requirements is forbidden. If something
  is missing from the source phase or upstream artifacts, surface it here as a
  proposal — do not silently assume it.
- A resolution with confidence below 80% must include a fallback proposal and
  a kill criterion the executing agent can detect mid-run.
- Once the user has not amended within the agreed window, the proposed
  resolution becomes the contract for the run. Log it in the run ledger.

## Autonomous Loop

1. Read this artifact and the source phase plan before editing.
2. Confirm the source phase is still current against the repo, PRs, and merged
   work.
3. Run `$skill-oracle` for the active capability set and note missing skills.
4. Inspect source-of-truth inputs before writing any successor phase plan.
5. Complete § Preflight Uncertainty Ranking. For every uncertainty that could
   change the plan, propose a highest-confidence resolution. Do not ask
   open-ended clarification questions; propose and proceed. Log each
   resolution in the run ledger.
6. Restate § Frozen Original Intent (Building + Matt-test), the constraints, and
   § Priority Order in one paragraph before any non-trivial change. This
   restatement is the contract for the run.
7. Run `$deep-sweep` to find plan gaps, risks, stale assumptions, evidence
   gaps, and verification gaps.
8. Update this artifact or the phase plan only if the sweep reveals material
   gaps.
9. Run `$deep-build` against the locked plan. Prefer minimal sufficient
   changes over broad rewrites.
10. Run `$ultra-review` after implementation.
11. Fix critical/high findings; use `$deep-clean` only for scoped cleanup
    required by review.
12. Run the gates in § Verification Gates. If a gate fails irreversibly,
    execute that gate's documented Rollback Plan and update the run ledger.
    Do not invent rollback paths.
13. Use `$browser-harness` in the user's real logged-in browser for live
    platform verification when the feature touches UI or platform workflows.
14. Run § Drift Gate against § Frozen Original Intent. If a drift signal trips,
    halt successor creation and re-run `$deep-sweep` scoped to the approach, or
    escalate. Otherwise, if the definition of done is not satisfied, create the
    next numbered `docs/planning/phase-N/` plan around discovered facts, update
    this ledger, and continue. If time, tokens, or live access force a scope
    cut, drop work from lowest § Priority Order tier up; do not silently re-rank.
15. Stop when the definition of done and verification gates pass, or when a
    stop condition below is hit. Do not expand scope after the definition of
    done is satisfied; declare done and emit the Final Report.
16. Run § Verifier Gate before marking the run ledger done. A verifier
    failure returns the run to step 9 and consumes one fix pass
    (see § Stop Conditions).
17. Run § Strategy Confidence Loop after the Verifier Gate passes. It may not
    override a verifier failure.

## Successor Phase Policy

- Create a successor phase when the current phase or PR cannot satisfy the
  definition of done.
- Do discovery first; do not make "Research" a plan step.
- Successor plans must cite this artifact as upstream context.
- Record each successor in the run ledger.
- Continue creating successors until done or a stop condition is hit.

## Drift Gate

Run before creating each successor phase and before the final done-gate. Compare
current work against § Frozen Original Intent (not just the per-phase Definition
Of Done) on four signals:

1. Product-truth regression — an earlier-working real outcome stopped working,
   or a fixture replaced real data.
2. Intent divergence — current work no longer serves the frozen "Building"
   outcome / Matt-test.
3. Scope expansion — new surface area not in § Scope Boundaries (route stray
   ideas to `docs/PARKED.md`; never absorb them).
4. Design-direction flip — the look drifted from the frozen design target.

If any signal trips, do NOT auto-create a successor feature phase. Branch:

- DoD genuinely unmet, approach still sound → create a successor phase.
- Drift signal tripped → HALT and re-run `$deep-sweep` scoped to "is this
  approach still right given the live build and the frozen intent," or escalate
  to Matt. A green per-phase DoD does not authorize continuing through drift.

## Required Skills

- `phase-plan` for source-plan structure and successor plans.
- `skill-oracle` for skill routing.
- `deep-sweep` for gap analysis and red-team verification.
- `deep-build` for implementation.
- `ultra-review` for broad review.
- `deep-clean` for review-driven cleanup only.
- `browser-harness` for logged-in browser verification.
- `prompt-generation` for tightening any generated prompt package or model
  routing guidance.
- `ecc-autonomous-agent-harness` for long-running loop discipline.
- `ecc-agentic-engineering` for eval-first decomposition and model routing.

## Agent And Model Routing

- Main planner/synthesizer/final judgment: current highest-reasoning
  configured model (OpenAI/Codex or Anthropic Claude) verified at execution
  time, or the active config default. Record concrete model IDs only after
  current docs or local config prove them.
- Executor note — Claude (Fable 5): load `prompt-generation`
  `references/claude-fable-5.md`. Effort high by default; audit each progress
  claim against a tool result from this session; propose-and-proceed on
  reversible actions.
- Research/exploration subagents: current configured smaller or cheaper
  models where available for token efficiency.
- Specialist review lanes: use relevant ECC reviewer agents based on changed
  files and risk area.
- Browser verification: use `browser-harness`; do not require passwords in the
  artifact.
- Configuration: use existing `config.toml` agent roles; do not edit config
  unless the user explicitly asks for configuration changes.

## Prompt Or Model Eval Gate

Use this gate whenever the goal changes prompts, model choice, tool routing, or
agent behavior.

| Item | Value |
|------|-------|
| Prompt/model change | `<description or N/A>` |
| Baseline fixture or score | `<fixture, score, or N/A>` |
| Changed fixture or score | `<fixture, score, or N/A>` |
| Regression failures | `<list or none>` |
| Cost/latency note | `<delta or N/A>` |
| Promotion/rollback decision | `<decision plus evidence>` |

## Priority Order

If time, tokens, or live access force a scope cut mid-run, drop work from
lowest priority up. Do not silently re-rank — surface the cut in the run
ledger and the Final Report.

1. P0: `<must-deliver; cutting this fails the run>`
2. P1: `<important; cut only if P0 is at risk>`
3. P2: `<nice-to-have; first to drop>`

Add more tiers only when the goal genuinely has more than three priority
levels. Every P0 item must appear in § Definition Of Done.

## Scope Boundaries

In scope:
- `<item>`

Out of scope:
- `<item>`

## Verification Gates

Every gate row requires a Rollback Plan. Read-only or non-mutating gates use
`N/A (read-only)`. Destructive or high-risk gates require a specific revert
command, deploy rollback, or revert-PR identifier plus owner. The agent
executes the documented Rollback Plan — never an invented one — when a gate
fails irreversibly.

| Gate | Command / Method | Pass Criteria | Rollback Plan |
|------|------------------|---------------|---------------|
| Static / typecheck | `<command>` | `<criteria>` | `N/A (read-only)` |
| Unit / integration tests | `<command>` | `<criteria>` | `N/A (read-only)` |
| Data or pipeline checks | `<command or dashboard>` | `<criteria>` | `<revert path or N/A>` |
| Provider / API docs check | `<docs>` | `<criteria>` | `N/A (read-only)` |
| Browser-harness verification | `<live route / workflow>` | `<criteria>` | `<session rollback or N/A>` |
| PR / CI / deploy checks | `<command or service>` | `<criteria>` | `<deploy revert command + owner>` |
| Product-truth launch | UI goal: `$run`, then `$browser-harness` for logged-in UI. Non-UI goal: the goal's real surface — live endpoint / query / deployed job | one real Matt-test outcome completes against data the build did not author — UI goal in a freshly launched real app with desktop + mobile screenshots; non-UI goal on the real verification surface (launch/mobile `N/A` + reason) | `<session / deploy rollback or N/A>` |
| Final review | `$ultra-review` | no critical / high blockers | `<reverse merge or revert PR + owner>` |

## Product-Truth Launch Gate

"Done" is never tests / typecheck / self-written scripts passing. Before the
Verifier Gate, prove ONE real Matt-test outcome (from § Frozen Original Intent)
against data the build did NOT author — a real account, a human-seeded row, or a
live provider, never a build-written fixture or proof harness:

- Product / UI goal: LAUNCH the real app the way Matt runs it (`$run`;
  `$browser-harness` for logged-in UI); capture desktop + mobile screenshots and
  a click-through of the Matt-test. Do not read compiled exhibits or
  self-validating phase scripts.
- Non-UI goal (backend, data, infra, docs, process — no launched app or mobile
  surface): exercise the goal's real verification surface instead — a live
  endpoint hit, a real query result, a deployed job run, a rendered artifact —
  against non-build-authored data, and mark the launch/mobile fields `N/A` with a
  one-line reason. A real surface is still mandatory; `N/A` never means "skip the
  product-truth proof".

Evidence admissibility: a proof is INADMISSIBLE if its pass-condition can be
true while the product is broken. Inadmissible — string-checks/greps on source
files, doc/fixture internal-consistency checks, screenshots reusable from a
prior run, "it compiles". Admissible — a fresh real-app launch (or, for non-UI
goals, a live exercise of the real surface) producing the real outcome against
non-build-authored data.

## Verifier Gate

Before the run ledger is marked `done`, dispatch a fresh-context verifier
subagent. The verifier sees only this artifact and on-disk evidence — never
the actor's transcript or reasoning — and checks § Frozen Original Intent (the
Matt-test) AND § Definition Of Done AND every § Verification Gates row. The
agent that produced the work must not grade it.

For best independence, the verifier should run on a different configured model
family than the actor (e.g. the harness-routed OpenAI-family verifier that
`deep-sweep` uses) when one is available; if only one family is configured, log
that the cross-model check was degraded.

The verifier returns exactly this verdict shape:

```json
{
  "verdict": "pass | fail | stuck",
  "criteria": [
    {"id": "<DoD item, Matt-test item, or gate row>", "pass": true, "evidence": "<file:line, command output, or URL>", "severity": "blocker | major | minor"}
  ],
  "live_launch_evidence": {
    "launched": true,
    "entrypoint": "<Electron app | dev server URL | deployed URL | 'N/A — non-UI goal: <reason>'>",
    "real_user_action": "<the Matt-test outcome completed in the running app OR on the real verification surface>",
    "non_authored_data": "<real account / human-seeded row / live provider>",
    "screenshots": ["<desktop path>", "<mobile path>"]
  },
  "summary": "<one-line scoreboard>",
  "next_action": "<what the actor does next>"
}
```

Field types are fixed: `launched` is always a boolean and `screenshots` always an
array — never put `N/A` text into them. For a non-UI goal, set `launched: false`
and `screenshots: []`, put the no-app reason in `entrypoint`, and carry the actual
proof in `real_user_action` + `non_authored_data` (which apply to any goal type).

- Every criterion needs named evidence before `pass`; missing evidence is a
  `fail`, not a pass.
- If the build passes § Definition Of Done but fails any § Frozen Original
  Intent Matt-test item, that is a `fail` — building the wrong thing correctly
  is not done.
- Require § Product-Truth Launch Gate evidence (`live_launch_evidence`). For a
  product/UI goal, a verdict without a real-app launch against non-build-authored
  data is a `fail`. For a non-UI goal, keep the shape valid — `launched: false`,
  `screenshots: []`, the no-app reason in `entrypoint` — and require instead a
  `real_user_action` proven on the goal's live verification surface against
  non-build-authored data; a verdict with no real surface exercised is still a
  `fail`. Self-validating scripts and source
  string-checks are inadmissible for either goal type.
- `fail` on any blocker or major criterion returns the run to the fix loop.
- `stuck` maps to the blocked-stop report in § Stop Conditions.
- Treat a malformed or missing verdict as a loud `fail`; never retry silently
  or count it as a pass.
- The Strategy Confidence Loop runs after this gate and may not override a
  verifier failure.

## Lightweight Run Ledger

| Field | Value |
|-------|-------|
| Status | `not-started` |
| Current phase | `<phase>` |
| Active PRs | `<PRs or N/A>` |
| Active branch | `<branch or N/A>` |
| Last verified gate | `none` |
| Successor phases created | `none` |
| Evidence links | `none` |
| Lessons distilled | `none` |
| Last updated | `<YYYY-MM-DD>` |

Lessons distilled: one lesson per entry, recorded only after the fix was
confirmed; update the existing note rather than duplicating it.

## Stop Conditions

- Max fix passes: `3` (default). Each Verifier Gate failure consumes one pass;
  exhausting them is a stop.
- Non-convergence: the same blocker or major finding three times → STUCK.
- STUCK exit: stop and report `{attempted_paths, evidence_gathered, blocker,
  next_input_needed}` instead of looping further.
- Required credentials, live access, provider access, or approved deploy target
  are unavailable.
- A destructive data operation, migration, production change, or policy bypass
  is required but not explicitly approved.
- Provider docs or rate limits prove the plan is not viable.
- Source phase conflicts with newer merged work and cannot be reconciled safely.
- A § Drift Gate signal trips and is not resolvable inside the current approach
  → STUCK / escalate; do not keep spawning successors through drift.
- The § Product-Truth Launch Gate cannot prove one real Matt-test outcome in the
  launched app against non-build-authored data.
- Browser-harness verification cannot prove the user-facing outcome.
- CI, mergeability, or branch protection failures cannot be resolved safely.
- Any critical/high review finding remains unresolved.

## Final Report Requirements

Report:
- PR links, commits, tests, and deploy status.
- What changed by phase/subphase.
- Source API/provider verification evidence.
- Workbook/manual-input/source-mapping evidence.
- Browser-harness evidence.
- Successor phases created and why.
- Remaining limitations and rollback path.
- What could not be verified and why (cite the gate that would have run).
- Preflight uncertainty resolutions actually applied versus user amendments.
- Scope cuts taken under § Priority Order, with the priority tier dropped.
- Lessons distilled during the run — one lesson per entry, only after the fix
  was confirmed; update existing notes rather than duplicating.
- The final short `/goal` prompt path.

## Strategy Confidence Loop

This section is the closing instruction. It runs after § Verifier Gate passes
and may not override a verifier failure. Run it again whenever the strategy
changes.

How to run the loop (max 3 iterations):

1. State the current strategy in one paragraph.
2. List loopholes, hidden assumptions, missing evidence, stop-condition
   triggers, unapplied preflight resolutions, silent priority re-ranks,
   missing rollback paths, or contradictions with the source phase, evidence
   pack, run ledger, or verification gates.
3. For each finding, propose a concrete fix and update the artifact, the
   source phase, the run ledger, or the verification gates so the fix lives
   on disk and survives the next agent.
4. Exit on an evidence-backed confidence statement that cites the gate,
   evidence row, or successor phase proving each reason — or at the iteration
   cap, whichever comes first. Log unresolved findings in the run ledger as
   open risks; blocker or major findings route back through § Verifier Gate,
   not this loop.
5. Only then mark the run ledger `done` and emit the Final Report.

If the loop ever requires bypassing a stop condition, escalate instead of
looping. Confidence does not authorize policy bypass.
````
