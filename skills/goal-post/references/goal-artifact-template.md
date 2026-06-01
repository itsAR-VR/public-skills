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
authority: "guarded-autonomous"
status: "not-started"
---

# <Phase Name> Goal: <Goal Title>

## Short /goal Prompt

```text
/goal Execute @docs/planning/goals/<file>.md autonomously. Read it, follow the run ledger, create successor phases as needed, run the strategy-confidence loop until 100% certain, and stop only at done or a stop condition.
```

## Objective

Deliver <specific outcome> from <source phase> end to end.

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
6. Restate the goal, constraints, and § Priority Order in one paragraph before
   any non-trivial change. This restatement is the contract for the run.
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
14. If the definition of done is not satisfied, create the next numbered
    `docs/planning/phase-N/` plan around discovered facts, update this ledger,
    and continue. If time, tokens, or live access force a scope cut, drop
    work from lowest § Priority Order tier up; do not silently re-rank.
15. Stop when the definition of done and verification gates pass, or when a
    stop condition below is hit. Do not expand scope after the definition of
    done is satisfied; declare done and emit the Final Report.
16. Run § Strategy Confidence Loop before declaring done.

## Successor Phase Policy

- Create a successor phase when the current phase or PR cannot satisfy the
  definition of done.
- Do discovery first; do not make "Research" a plan step.
- Successor plans must cite this artifact as upstream context.
- Record each successor in the run ledger.
- Continue creating successors until done or a stop condition is hit.

## Required Skills

- `phase-plan` for source-plan structure and successor plans.
- `skill-oracle` for skill routing.
- `deep-sweep` for gap analysis and red-team verification.
- `deep-build` for implementation.
- `ultra-review` for broad review.
- `deep-clean` for review-driven cleanup only.
- `browser-harness` for logged-in browser verification.
- `prompt-optimizer` for tightening any generated short prompt.
- `ecc-autonomous-agent-harness` for long-running loop discipline.
- `ecc-agentic-engineering` for eval-first decomposition and model routing.

## Agent And Model Routing

- Main planner/synthesizer/final judgment: GPT-5.5 or active highest-reasoning
  main model.
- Research/exploration subagents: GPT-5.4 where available for token efficiency.
- Specialist review lanes: use relevant ECC reviewer agents based on changed
  files and risk area.
- Browser verification: use `browser-harness`; do not require passwords in the
  artifact.
- Configuration: use existing `config.toml` agent roles; do not edit config
  unless the user explicitly asks for configuration changes.

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
| Final review | `$ultra-review` | no critical / high blockers | `<reverse merge or revert PR + owner>` |

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
| Last updated | `<YYYY-MM-DD>` |

## Stop Conditions

- Required credentials, live access, provider access, or approved deploy target
  are unavailable.
- A destructive data operation, migration, production change, or policy bypass
  is required but not explicitly approved.
- Provider docs or rate limits prove the plan is not viable.
- Source phase conflicts with newer merged work and cannot be reconciled safely.
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
- The final short `/goal` prompt path.

## Strategy Confidence Loop

This section is the closing instruction. Run it before declaring done and run
it again whenever the strategy changes.

> Are you 100% confident in this strategy? If not, find all possible loopholes,
> suggest proper fixes, and run this loop until you are factually 100%
> confident in the new strategy.

How to run the loop:

1. State the current strategy in one paragraph.
2. List every loophole, gap, hidden assumption, missing evidence, race
   condition, stop-condition trigger, unapplied preflight resolution, silent
   priority re-rank, missing rollback path, or contradiction with the source
   phase, evidence pack, run ledger, or verification gates. If you cannot
   find any, keep looking — silent confidence is not the same as verified
   confidence.
3. For each loophole, propose a concrete fix and update the artifact, the
   source phase, the run ledger, or the verification gates so the fix lives
   on disk and survives the next agent.
4. Re-state the strategy with the fixes applied.
5. Repeat from step 2 until you can write a one-line confidence statement that
   is factually true: "I am 100% confident because: <evidence-backed reasons,
   not vibes>." Cite the gate, evidence row, or successor phase that proves
   each reason.
6. Only then mark the run ledger `done` and emit the Final Report.

If the loop ever requires bypassing a stop condition, escalate instead of
looping. 100% confidence does not authorize policy bypass.
````
