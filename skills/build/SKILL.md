---
name: build
description: >
  End-to-end execution lane with explicit gears: plan, eng-review, implement,
  review, browse-qa, ship, and retro. Use when the user wants the full
  build loop or wants to force a specific mode instead of one generic build
  brain. Default chain: plan -> skill-oracle -> phase-gaps -> terminus-maximus
  -> phase-review/code-review -> browse-qa -> commit-work.
aliases: [phase-build]
metadata:
  author: podhi
  version: 2.0.0
related_skills: [terminus-maximus, phase-implement, plan, codex, browse-qa, code-review]
routing:
  domain_keywords:
    - build
    - compile
    - deploy
    - ship
    - launch
    - release
    - pipeline
    - ci
    - cd
    - test
    - lint
    - bundle
    - webpack
    - vite
    - esbuild
    - turbopack
  intent_patterns:
    - "(?:build|compile|bundle|deploy|ship|launch|release)\\s+(?:the\\s+|this\\s+)?"
    - "(?:fix|debug)\\s+(?:the\\s+)?(?:build|compilation|bundle|deploy)"
  lane: codex-worker
  task_type: coding-general
---

# Build

Read all files in `references/` before using this skill.

This skill keeps substantial work in explicit gears instead of treating every
request like one generic "build something" pass.

## What this skill does

1. Forces a deliberate gear choice before work starts.
2. Runs the canonical Podhi build chain when no gear override is given.
3. Maps common build modes onto the skills we already have, plus `browse-qa`.
4. Keeps planning, implementation, review, QA, and shipping as distinct stages.

## Hard rules

- Run a **skill preflight** before non-trivial execution:
  - `find-local-skills`
  - and `skill-oracle` if the task or scope shifts materially.
- Read current project context first: AGENTS, relevant context packets, recent memory, and active phase docs.
- Check `git status` before edits and before commit.
- Audit existing packages/plugins/libraries before inventing custom code.
- For UI or browser-facing work, `browse-qa` is not optional.
- Use `plan`, not `phase-plan`. `phase-plan` is legacy wording.

## Gear map

| Gear | Purpose | Primary local skill(s) | Notes |
|---|---|---|---|
| `plan` | turn request into a concrete phase plan | `plan`, `skill-oracle` | use at the start of substantial work |
| `eng-review` | architecture + risk tightening before coding | `phase-gaps` | architecture, gaps, tests, and failure modes |
| `implement` | do the work to completion | `terminus-maximus` | implementation model stays `openai-codex/<latest-openai-model-id>` high |
| `review` | post-implementation hardening | `phase-review`, optionally `code-review` | use `code-review` when diff/PR-specific |
| `browse-qa` | browser truth-pass with screenshots | `browse-qa` | first-class visual verification gear |
| `ship` | commit and push through the right release path | `commit-work`, plus repo-specific ship path | for `public-skills`, use `push-skills`; for app repos, use normal git/github flow |
| `retro` | capture lessons, missing skills, doctrine patches | local docs + learnings update | optional, high-value after large runs |

## Inputs

- **Goal**: raw user request or explicit implementation objective.
- **Optional flags**:
  - `--gear <plan|eng-review|implement|review|browse-qa|ship|retro>`
  - `--goal "..."`
  - `--phase docs/planning/phase-N`
  - `--url https://...`
  - `--routes /,/pricing,/dashboard`
  - `--skip-review`
  - `--skip-browse`
  - `--skip-qa`
  - `--no-commit`
  - `--verbose`

If `--gear` is omitted, run the **default full chain**.

## Default full chain

### 0) Resolve scope and environment

- Parse the request and target repo/path.
- Confirm whether the work is:
  - code-only,
  - UI/browser-facing,
  - release-only,
  - or review-only.
- If phase docs do not exist and the task is substantial, create them with `plan`.
- Run quick repo truth checks:
  - `git status`
  - active phase overlap scan
  - package/library audit relevant to the ask

### 1) `plan`

Run:

```text
/skill plan "<goal>"
```

Capture the created phase path under `docs/planning/phase-*/plan.md`.
Use the next free phase number if there is a collision.

### 2) `skill-oracle`

Run `skill-oracle` against the same objective and note immediately-available skills and fallbacks in the phase artifacts.

### 3) `eng-review`

Run:

```text
/skill phase-gaps docs/planning/phase-<N>
```

It should tighten architecture, risks, dependencies, fallback paths, test gaps, and coordination hazards before or during implementation.

### 4) `implement`

Run:

```text
/skill terminus-maximus
```

Use:
- `openai-codex/<latest-openai-model-id>`
- `thinking: high`

Keep changes scoped to the approved phase. Update phase artifacts as work lands.

### 5) `review`

Default review path for phase-tracked work:

```text
/skill phase-review
```

If the request is specifically diff-centric or PR-centric, pair with:

```text
/skill code-review
```

It exists to catch structural problems that a successful implementation pass can still miss.

### 6) `browse-qa`

If the work touches UI, routes, browser flows, login, rendering, or deploy behavior, run:

```text
/skill browse-qa --url <target> [--routes ...]
```

Minimum bar:
- screenshot evidence
- desktop + mobile checks for impacted flows
- console inspection
- explicit pass/fail summary
- tab cleanup at the end

If work is strictly non-visual backend work, note why browse QA was not required.

### 7) `ship`

If not `--no-commit`, run:

```text
/skill commit-work
```

Then use the **repo-appropriate ship path**:
- **public-skills**: `push-skills`
- **normal code repo**: commit + push/PR using repo norms
- **local-only proof run**: stop after commit or proof artifact generation

### 8) `retro`

After substantial runs, capture:
- what worked,
- what should become doctrine,
- what should become or patch a skill,
- and what should go into `.learnings` or memory.

## Single-gear mode

Use a single gear when the user is not asking for the full chain.

### `--gear plan`
- Use when the ask is still fuzzy or architectural.
- Output should be the phase path + immediate nextAction.

### `--gear eng-review`
- Use when a phase exists and needs a hard pre-implementation or mid-flight tightening pass.
- Run `phase-gaps`.

### `--gear implement`
- Use when planning is already good enough and the job is to execute.
- Resume the target phase with `terminus-maximus`.

### `--gear review`
- Use when code exists and the task is to audit it, not plan or extend it.
- Prefer `phase-review`; add `code-review` for PR/diff scrutiny.

### `--gear browse-qa`
- Use for browser truth-passes, deploy verification, login flow checks, or visual regressions.
- Always route through `browse-qa` instead of freehand browser flailing.

### `--gear ship`
- Use when the branch is already ready and the job is to package/commit/push responsibly.
- Route through `commit-work` and repo-specific release tooling.

### `--gear retro`
- Use after a big build, failed pass, or doctrine change.
- Produce a concise lessons + follow-ups artifact.

## Model mapping

- **Planning:** follow `plan` defaults
- **Skill discovery / routing:** `skill-oracle` or `find-local-skills`
- **Red-team / eng-review:** follow `phase-gaps` defaults and keep it cross-model from implementation when possible
- **Implementation:** `openai-codex/<latest-openai-model-id>`, `thinking: high`
- **QA / browse:** browser-driven evidence over vibes
- **Commit:** per `commit-work`

## Output contract

Return concise execution-backed updates with:
- active gear
- phase path or target URL
- changed files
- verification status
- blockers/risks
- nextAction

## Examples

```text
/build "ship the new dashboard settings flow"
# full chain: plan -> oracle -> eng-review -> implement -> review -> browse-qa -> commit-work
```

```text
/build --gear browse-qa --url http://localhost:3000 --routes /,/settings,/settings/profile
# run only the browser truth-pass gear
```

```text
/build --gear review --phase docs/planning/phase-42
# post-implementation hardening pass on an existing phase
```
