---
name: deep-build
description: >
  Multi-model execution orchestrator with GSD-absorbed execution layer. Runs the
  full build pipeline (plan, eng-review, implement, review, QA, ship) with
  active primary-model implementation + harness-routed OpenAI-family
  cross-verification at every gear, enhanced by GSD's
  codebase-mapper (structural context), nyquist-auditor (goal-backward test
  coverage), gsd-executor patterns (atomic commits + checkpoint protocols),
  gsd-debugger (structured fix loop), and gsd-verifier (post-execution
  goal-backward check). Use when: "deep build", "build with cross-verify",
  "multi-model build", "build thoroughly", "execute this plan", "gsd execute".
  For analysis-only see deep-sweep. For single-model build see build. For
  post-build audit see verify.
metadata:
  author: public-skills contributors
  version: 1.1.0
related_skills:
  - phase-plan
  - skill-oracle
  - think
  - deep-sweep
  - terminus-maximus
  - deep-clean
  - goal-post
  - ultra-review
  - browser-harness
  - verify
  - superpowers-test-driven-development
  - superpowers-verification-before-completion
  - superpowers-using-git-worktrees
  - superpowers-executing-plans
  - superpowers-finishing-a-development-branch
---

# Deep Build

Full execution pipeline enhanced with multi-model cross-verification at every stage.
The **active primary model** implements. A **harness-routed OpenAI-family verifier**
independently verifies every diff. Parallel subphase lanes with cross-comparison
ensure nothing slips through.

When `deep-build` is part of a phase workflow, read
`skills/phase-plan/references/09_PHASE_PIPELINE_PLAYBOOK.md`. The playbook owns
the shared beginner path, proof labels, and handoff sequence. This file owns the
`deep-build` mechanics: gears, execution packets, verifier routing, QA, and ship
discipline.

**Relationship to other skills:**
- `deep-sweep` = analysis/planning only (produces a plan)
- `build` = single-model execution with gears (produces code)
- **`deep-build`** = multi-model execution with gears (produces cross-verified code)

## Model Currency & Harness Routing

Load `references/model-currency.md` before model-currency preflight or hardcoded
model ID changes. Current Codex snapshot locally verified on 2026-07-09:

- **Difficult/deep/review route:** `gpt-5.6-sol` with `ultra` effort.
- **Bounded worker route:** `gpt-5.6-terra` with `high` effort.
- **Tiny mechanical route:** `gpt-5.6-luna` with `low` or `medium` effort.
- **Access gate:** GPT-5.6 is preview-access gated. Require `codex debug models`
  to advertise the chosen ID and effort, then prove account entitlement with a
  live read-only probe after login. Update Codex or stop instead of downgrading.
- **Claude Code:** prefer aliases (`fable`, `opus`, `sonnet`, `haiku`) for
  latest-family routing; current Opus pinned ID is `claude-opus-4-8`.
- **Refresh trigger:** if a model ID, price, context window, or feature flag is
  material, refresh official docs and CLI support, then record ID/date.

## When to Activate

| Signal | Example |
|--------|---------|
| Explicit invocation | "deep build", "/deep-build" |
| High-stakes implementation | Auth, payments, data migrations, public APIs |
| Complex multi-subphase builds | 3+ subphases touching different domains |
| Maximum confidence builds | "I want this bulletproof before we ship" |
| Post deep-sweep execution | "Now build what we planned in the deep sweep" |

## Composition

Composes the full skill chain, enhanced with multi-model verification + GSD execution layer:

| Gear | Primary Skill | Multi-Model Enhancement | GSD Agent Layer |
|------|--------------|------------------------|-----------------|
| 0. Preflight | `$skill-oracle` + `$graphify` + `$gitnexus` | Auto-resume + dual graph freshness check | `gsd-codebase-mapper` — structural brief of existing code before any edits |
| 1. Validate | `$phase-gaps` | Quick plan validation (plan must already exist) | `gsd-nyquist-auditor` — goal-backward test coverage map |
| 2. Eng Review | `$phase-gaps` + `mcp__gitnexus__impact` | RED TEAM + OpenAI-family verifier + blast radius per subphase | `gsd-nyquist-auditor` (continues) + `gsd-pattern-mapper` for structural fit |
| 3. Implement | `$terminus-maximus` | Primary model implements, OpenAI-family verifier checks each diff | `gsd-executor` patterns: atomic commits per task, checkpoint protocols, deviation handling |
| 3-fail. Debug | on-fault escalation | OpenAI-family independent debug | `gsd-debugger` — structured fix loop (reproduce → isolate → fix → verify) |
| 3b. Graph Sync | `$graphify --update` + `gitnexus analyze` | Refresh both graphs after implementation | — |
| 4. Review | `$phase-review` + `$code-review` + `mcp__gitnexus__detect_changes` | Multi-model review + symbol-level change mapping | `gsd-verifier` — goal-backward verification against plan.md |
| 5. QA | 4-layer: tests + visual + functional + OpenAI-family verifier | Full-stack QA with browser control | `gsd-debugger` on any failing test (structured loop) |
| 6. Ship | `$commit-work` | Standard commit discipline | Atomic commit history from Gear 3 enables clean PR |

## Adaptive Gate Selection (harness-aware)

Before firing each gear's gates (codebase-mapper, nyquist-auditor, gsd-executor, gsd-debugger, gsd-verifier), check the active harness for pre-existing protections that cover the same intent.

- **On Claude Code with ECC installed**: `pre:bash:commit-quality` + `post:bash:*` hooks cover some execution-safety territory. Don't duplicate.
- **On OpenClaw**: bundled `session-memory` handles context preservation on `/new`/`/reset`. Skip `gsd-context-monitor` equivalents.
- **On minimal Codex/OpenCode**: no overlapping hook layer — run all gates, they're the protection.
- **Procedure + overlap map**: `~/.claude/skills/lib/adaptive-gate-selection.md`

**Every gear gate decision MUST be logged:**

```bash
bash $HOME/.claude/skills/lib/skill-gate-logger.sh \
  --skill deep-build \
  --gate <gate-name> \
  {--verdict PASS|FAIL|ESCALATE|PARTIAL  OR  --skipped "<why>"} \
  --reason "<one-line reason>"
```

## Skill Composition (vertical mode)

When `default_slice_type: vertical`, deep-build composes with the broader ecosystem at named gates. **Tiered**: required core fires deterministically; recommended optional fires when conditions match. This is the densest composition contract of the four phase-pipeline skills — every gear has named partners.

### Required core (MUST invoke)

- `$skill-oracle` @ Gear 0 — already wired; bespoke skill discovery for the active phase.
- `gsd-codebase-mapper` @ Gear 0/2 — already wired; structural brief of the existing code before any edits.
- `terminus-maximus` @ Gear 3a per slice — single-model execution discipline (replaces generic "impl-{feature_id}" phrasing).
- `superpowers-test-driven-development` @ Gear 3a — write tests first per slice's `acceptance_criteria`.
- `superpowers-using-git-worktrees` @ Gear 0 worktree spawn step — canonical worktree discipline composed with `orchestrate-worktrees.js`.
- `superpowers-verification-before-completion` @ Gear 3f merge-ready and Gear 5 phase-level — discipline applied before declaring a slice merge-ready and before phase ship.
- `superpowers-finishing-a-development-branch` @ Gear 6 ship — canonical branch-finishing discipline.
- ECC `code-reviewer` agent @ Gear 3c scoped review and Gear 4 — primary code review agent.
- `gsd-code-reviewer` @ Gear 3c and Gear 4 — parallel cross-check to ECC `code-reviewer`.
- `/verify` skill @ Gear 5 phase-level integration QA — goal-backward verification.

### Recommended optional (SHOULD invoke when conditions match)

Auto-detected from each slice's `surfaces[]`:

- ECC language-specific reviewer @ Gear 3c — fired by file extension match in slice surfaces:
  - `*.ts` / `*.tsx` → ECC `typescript-reviewer`
  - `*.py` → ECC `python-reviewer`
  - `*.go` → ECC `go-reviewer`
  - `*.rs` → ECC `rust-reviewer`
  - `*.kt` → ECC `kotlin-reviewer`
  - `*.java` → ECC `java-reviewer`
  - `*.cpp` / `*.h` → ECC `cpp-reviewer`
  - `*.dart` → ECC `flutter-reviewer`
- ECC `security-reviewer` @ Gear 3c — when slice has auth/data surfaces (`auth/`, `migrations/`, `*.sql`, `prisma/`).
- ECC `database-reviewer` @ Gear 3c — when slice has DB surfaces (`migrations/`, `prisma/`, `*.sql`).
- ECC `performance-optimizer` @ Gear 3c — when slice `acceptance_criteria` mentions perf budgets.
- ECC `e2e-runner` @ Gear 3e per-slice and Gear 5 phase-level — full user journeys.
- ECC `tdd-guide` @ Gear 3a — slice-level TDD scaffolding (degrade target if superpowers TDD unavailable).
- ECC `refactor-cleaner` @ Gear 3d via deep-clean — refactor cleanup arm.
- `gsd-security-auditor` @ Gear 3c — when slice touches auth/data.
- `gsd-ui-auditor` @ Gear 3c — when slice has UI surfaces (`components/`, `pages/`, `app/(routes)`).
- `gsd-nyquist-auditor` @ Gear 3e — sampling/coverage check.
- `gsd-verifier` @ Gear 5 phase-level — goal-backward verification (parallel with `/verify` skill).
- `gsd-integration-checker` @ Gear 5 phase-level — cross-phase E2E integration check.
- `superpowers-requesting-code-review` + `receiving-code-review` @ Gear 3c — review interaction protocol.
- `superpowers-subagent-driven-development` @ Gear 3a — impl agent dispatch protocol.

### Per-slice tools (fire once per feature_id)

- `mcp__gitnexus__impact` per slice @ Gear 2 eng review — blast radius for the slice's primary symbols.
- `mcp__claude-in-chrome__*` @ Gear 3e visual QA — when slice has UI surfaces.

### Source of truth (avoid rot)

- ECC catalog: `skills/everything-claude-code/agents/` and `commands/`
- GSD catalog: `~/.claude/agents/gsd-*`
- Superpowers catalog: `skills/superpowers-*/` (vendored from `anthropics/claude-plugins-official`; no plugin dependency)

## Gear System

> Detailed procedures in `references/procedure.md`.
> Implementation lane patterns in `references/implementation-lanes.md`.
> QA protocol in `references/qa-protocol.md`.
> Agent prompts in `references/agent-prompts.md`.

---

### Gear 0 — Preflight

1. Run `$skill-oracle` — discover skills for the problem domain
2. `git status --porcelain` — check workspace state
3. `ls -dt docs/planning/phase-* 2>/dev/null | head -10` — scan active phases
4. **Dual graph check:**
   - **Graphify:** If `graphify-out/graph.json` exists and is current → read `graphify-out/GRAPH_REPORT.md` for god nodes and community structure. If stale → `/graphify . --update`. Feed to implementation agents.
   - **GitNexus:** Run `gitnexus status` — verify index is current. If stale → `gitnexus analyze --embeddings`. Run `mcp__gitnexus__impact` on the primary symbols referenced in the plan to pre-compute blast radius for Gear 2 eng review.
   - Both are optional — deep-build proceeds without them, but with reduced structural awareness.
5. **Resolve the target phase:**
   - **Target-phase input:** if the invocation names a specific
     `docs/planning/<name>/` directory containing a `plan.md` — numbered
     `phase-{N}` or a named plan directory, whichever the active plan uses.
     Build that phase only.
     Resolve and announce it FIRST, before the plan-dependent preflight
     above (step 4's impact analysis on plan symbols and any graph/index
     refresh run against the plan), and never substitute a newer concurrent
     phase.
   - Only when no target is named, auto-resume the latest incomplete phase:
     find the latest `docs/planning/phase-{N}/` directory
   - Read root `plan.md` — check if Phase Summary is empty (incomplete)
   - Scan subphases — find first with empty Output/Handoff
   - If incomplete phase found → resume from that point
   - If all phases complete → **STOP**: tell user to run `/deep-sweep` first
5. If **no phases exist** → **STOP**: tell user to run `/deep-sweep` to create a plan
6. **Read root plan front-matter.** Parse `default_slice_type`, `phase_intent`, `ship_gate`, `isolation`. If front-matter is absent (legacy plan), default to: `default_slice_type: horizontal`, `ship_gate: phase_atomic`, `isolation: in_tree` (existing behavior).
7. **Worktree spawn (vertical mode only).** If `isolation: worktree` AND there are 2+ independent vertical slices in `slice_index` (i.e., 2+ slices with empty or non-overlapping `depends_on`), invoke `orchestrate-worktrees.js --plan <emitted-plan.json>` using the Worktree Plan JSON Template from `phase-plan/references/04_TEMPLATES.md`. One worker per `feature_id`, branch `feature/<feature_id>`, seedPaths from each slice's `surfaces[]`. Single-slice or strictly-serial-chain phases skip worktree setup. This step composes `superpowers-using-git-worktrees` (canonical worktree discipline) with the existing `orchestrate-worktrees.js` script. When the superpowers plugin is unavailable, the procedure documented in `using-git-worktrees` SKILL.md degrades to the script-only flow (still functional).

**Gate:** Active phase identified. Entry gear determined based on phase state.

**IMPORTANT:** Deep-build does NOT create plans. Run `/deep-sweep` first.

---

### Gear 1 — Validate Plan

**Prerequisite:** A plan must exist at `docs/planning/phase-{N}/`. If none exists,
STOP and instruct: `"No plan found. Run /deep-sweep first to create one."`

Quick validation of the existing plan:
- Read the plan and all subphase plans from disk
- Quick `$phase-gaps` pass to verify it's still current against codebase
- OpenAI-family quick-check: verify referenced files/functions still exist
- Check for conflicting changes since plan was created (`git log --since`)

If plan is stale or conflicts found:
- Recommend user runs `/deep-sweep` to refresh
- Or proceed with noted caveats (user's choice)

**Gate:** Plan validated and current. Ready for eng-review or implementation.

---

### Gear 2 — Eng Review (Multi-Model)

Run two reviewers in parallel:

```
# Agent 1: Primary-model RED TEAM
Agent(
  name: "eng-review-primary",
  model: "<active-primary-model>",
  prompt: "RED TEAM this plan using $phase-gaps pattern..."
)

# Agent 2: OpenAI-family codebase verification (harness-routed)
OpenAIFamilyVerifier(
  name: "openai-eng-review",
  prompt: "Verify this plan is implementable against the actual codebase..."
)
```

Cross-compare findings. Update plan with:
- Implementation risks identified
- Codebase constraints discovered
- Revised approach where needed

**Gate:** Plan locked, eng-reviewed, ready for implementation.

---

### Gear 3 — Implement (Parallel Lanes + Cross-Check)

**Mode dispatch.** If root `default_slice_type: vertical`, run **Per-Slice Gear Loop** (sub-section below). Otherwise, run the existing Per-Gear-Across-Lanes flow (unchanged).

This is the core differentiator. See `references/implementation-lanes.md` for full detail.

**For each subphase**, spawn a **named implementation lane**:

```
# Primary: active primary model implements the subphase
Agent(
  name: "impl-{sub}",
  model: "<active-primary-model>",
  subagent_type: "general-purpose",
  prompt: <Implementation prompt — terminus-maximus pattern>
)
```

**Independent subphases run in parallel.** Dependent subphases run sequentially.

**After EACH subphase completes**, run OpenAI-family verification:

```text
OpenAIFamilyVerifier(
  name: "openai-diff-{sub}",
  prompt: "Read the subphase diff from disk and review for bugs, edge cases, security issues. For each finding: severity, file:line, description, fix."
)
```

**Cross-Subphase Monitor** (runs after every 2nd subphase):

```
Agent(
  name: "cross-monitor",
  model: "<active-primary-model>",
  prompt: "Check for conflicts between completed subphases..."
)
```

If OpenAI-family verifier or cross-monitor finds CRITICAL/HIGH issues:
1. Communicate to the impl-{sub} agent (if still running) via SendMessage
2. Or spawn a fix agent for that subphase
3. Re-verify after fix

**Gate:** All subphases implemented. Each diff has OpenAI-family verification. No unresolved CRITICAL/HIGH.

**Per-Slice Gear Loop (vertical mode):**

For each vertical slice in dependency order (independent slices in parallel via worktrees; dependent ones sequential):

1. **Gear 3a — Implement.** Spawn the per-slice impl agent using `terminus-maximus` (single-model execution discipline) framed by `superpowers-test-driven-development` (write tests first per slice's `acceptance_criteria`). ECC `tdd-guide` agent provides slice-level TDD scaffolding and is the degrade target if the superpowers plugin is unavailable. Implements the slice's `surfaces[]` according to its `acceptance_criteria`.
2. **Gear 3b — OpenAI diff verify.** Spawn `openai-diff-{feature_id}` to independently verify the slice diff against the slice's plan and acceptance criteria.
3. **Gear 3c — Scoped Gear 4 review.** Scoped review fires the following composition (TIERED):
   - **Required**: ECC `code-reviewer` agent + `gsd-code-reviewer` agent — both inspect only the slice's diff (not the full repo).
   - **Auto-detect language-specific reviewers** (recommended optional, fired by file extension match in slice's `surfaces[]`): `*.ts`/`*.tsx` → ECC `typescript-reviewer`; `*.py` → ECC `python-reviewer`; `*.go` → ECC `go-reviewer`; `*.rs` → ECC `rust-reviewer`; `*.kt` → ECC `kotlin-reviewer`; `*.java` → ECC `java-reviewer`; `*.cpp`/`*.h` → ECC `cpp-reviewer`; `*.dart` → ECC `flutter-reviewer`.
   - **Conditional auditors**: ECC `security-reviewer` + `gsd-security-auditor` if slice has auth/data surfaces (`auth/`, `migrations/`, `*.sql`, `prisma/`); ECC `database-reviewer` if slice has DB surfaces; ECC `performance-optimizer` if slice `acceptance_criteria` mentions perf budgets; `gsd-ui-auditor` if slice has UI surfaces (`components/`, `pages/`, `app/(routes)`).
   - **Protocol**: `superpowers-requesting-code-review` + `receiving-code-review` for the review interaction protocol.
4. **Gear 3d — Scoped cleanup.** Invoke `/deep-clean --scope=feature:<feature_id>` as a sub-routine. Fold its Green-bucket findings into the slice's review fix list. Yellow/Red findings escalate to the user.
5. **Gear 3e — Scoped Gear 5 QA.** Run Gear 5 (QA) scoped to the slice's `surfaces` and `integration_contracts`. Functional QA exercises the slice's user flows.
6. **Gear 3f — Mark slice merge-ready.** The slice is NOT shipped yet (default `ship_gate: phase_atomic`); it just enters merge-ready state.

**Cross-monitor**. Runs after every 2nd merge-ready slice. Vertical-mode prompt: contract drift between slices, schema migration ordering, shared-module touch hotspots, event/notification fan-out conflicts. See `references/implementation-lanes.md`.

**After all slices merge-ready**: proceed to phase-level Gear 5 integration QA, then Gear 6 ship.

---

### Gear 3b — Dual Graph Sync

After all implementation subphases complete, refresh both graphs so Gear 4 reviewers have current structural context:

```bash
# Update graphify knowledge graph (AST only — no LLM cost)
graphify . --update 2>/dev/null || true

# Re-index GitNexus code graph
gitnexus analyze --embeddings 2>/dev/null || true
```

Both are deterministic and free (no LLM calls). The updated graphs feed into Gear 4:
- `GRAPH_REPORT.md` — community context for review agents
- `mcp__gitnexus__detect_changes` — maps the implementation diff to all affected symbols, ensuring reviewers check every downstream dependency

---

### Gear 4 — Review (Multi-Model Code Review)

**Vertical-mode sub-routine.** Before completing Gear 4 for a vertical slice, invoke `/deep-clean --scope=feature:<feature_id>` and fold its Green-bucket findings into the review fix list. Findings flow into the same fix loop as primary/openai/security review findings. (This step is invoked from the Per-Slice Gear Loop in Gear 3 in vertical mode; horizontal mode does not invoke `/deep-clean` per-subphase.)

Run three review agents in parallel:

```
# 1. Primary-model Code Review (code-review pattern)
Agent(
  name: "review-primary",
  model: "<active-primary-model>",
  subagent_type: "code-reviewer",
  prompt: "Review all changes from this implementation phase..."
)

# 2. OpenAI-family Independent Review
OpenAIFamilyVerifier(
  name: "openai-review",
  prompt: "Review the complete diff from disk."
)

# 3. Security Review (on sensitive code)
Agent(
  name: "security-review",
  subagent_type: "security-reviewer",
  prompt: "Security audit of all changes..."
)
```

Cross-compare all three review outputs:
- Unanimous findings → fix immediately
- Conflicting findings → primary-model tie-breaker agent resolves
- Security CRITICAL → blocks until fixed

Run `$phase-review` quality gates:
- `npm run lint` (or project equivalent)
- `npm run build`
- DB migrations if applicable

**Gate:** All CRITICAL/HIGH fixed. Lint + build pass. Phase plan updated with Output/Handoff.

---

### Gear 5 — QA (4-Layer Verification)

**Vertical mode runs Gear 5 twice:**

1. **Per-slice scoped QA** — executed inside the Per-Slice Gear Loop (Gear 3e), scoped to the slice's `surfaces` list. Validates the slice's own user flows in isolation.
2. **Phase-level integration QA** — executed once after all slices are merge-ready. Focused on `integration_contracts` and full user journeys spanning multiple slices. Catches cross-slice contract drift the per-slice QA can't see.

Phase-level integration QA composition (vertical mode only):
- **Required**: `/verify` skill (canonical post-execution audit, goal-backward) + `gsd-verifier` agent (parallel goal-backward verification) + `gsd-integration-checker` (cross-phase E2E) + `superpowers-verification-before-completion` discipline.
- **Recommended**: ECC `e2e-runner` agent for full user journeys spanning multiple slices.

Horizontal mode runs Gear 5 once (existing behavior).

> Full protocol in `references/qa-protocol.md`.

Four QA layers run in parallel where independent:

**Layer 1 — Automated Tests**
```
Agent(
  name: "qa-tests",
  subagent_type: "tdd-guide",
  prompt: "Run full test suite, verify 80%+ coverage,
           write tests for uncovered new code..."
)
```

**Layer 2 — Visual QA** (if UI changes)
```
Agent(
  name: "qa-visual",
  prompt: "Run $browse-qa — desktop + mobile (375px) screenshots,
           console error check, critical interaction path,
           explicit pass/fail with evidence..."
)
```

**Layer 3 — Functional QA** (actually interact with the app)

Uses real browser tools to test the app works end-to-end:

```
Agent(
  name: "qa-functional",
  prompt: "Functionally test the app using browser tools:
           - mcp__claude-in-chrome__navigate → open the app
           - mcp__claude-in-chrome__computer → interact with UI elements
           - mcp__claude-in-chrome__read_page → verify content rendered
           - mcp__claude-in-chrome__read_console_messages → check for errors
           - mcp__claude-in-chrome__javascript_tool → validate app state
           Run critical user flows. Verify data persists.
           Test error states. Check auth-gated routes.
           Use OpenClaw persistent profile for logged-in flows.
           For repeatable tests: npx browser-harness test (if available)"
)
```

Tools available for functional QA:
- **Claude-in-Chrome MCP** — navigate, click, type, read pages, check console
- **Computer Use** — screenshot-based interaction for complex flows
- **Browser Harness CLI** — `npx browser-harness test` for programmatic test scripts
- **OpenClaw profile** — persistent auth for logged-in flow testing

**Layer 4 — OpenAI-Family Functional Verification**
```text
OpenAIFamilyVerifier(
  name: "openai-qa-functional",
  prompt: "Analyze the implementation and test suite for untested edge cases, missing integration tests, API contracts, CLI argument parsing, data-flow correctness, and graceful error paths."
)
```

**QA failure handling (max 3 retries per layer):**
- Test failure → fix code, re-run tests
- Visual QA failure → fix UI, re-screenshot
- Functional QA failure → fix interaction, re-test flow
- OpenAI-family verifier gap → write missing test, re-verify
- After 3 retries → escalate to user

**Gate:** All tests pass. Coverage >= 80%. Visual QA pass. Functional flows verified. No console errors.

---

### Gear 6 — Ship

**Vertical mode honors root `ship_gate`:**

- **Default `ship_gate: phase_atomic`**: all merge-ready slices ship together as one PR with logical commits per slice (one commit per `feature_id`). Phase-level integration QA must pass before any slice ships. Safer for cross-feature contracts.
- **Opt-in `ship_gate: per_slice`**: each merge-ready slice may ship as its own PR/commit before later slices complete. Requires every slice to declare back-compat in its `acceptance_criteria` (existing behavior preserved when this slice ships alone). Default off — phase_atomic is recommended.

Ship composition (vertical mode): `superpowers-finishing-a-development-branch` (canonical branch-finishing discipline) + ECC `/checkpoint` command for atomic state capture + ECC `/promote` command if applicable.

Horizontal mode behavior unchanged.

Follow `$commit-work` discipline:

1. `git status` — identify session-scoped changes only
2. Stage explicitly (never `git add .`)
3. Logical commit boundaries (split if needed)
4. Conventional Commits message format
5. Run final verification (lint + build)
6. Commit

If user requested push:
- `git push -u origin {branch}`

Present completion summary:
- What was built (subphases completed)
- What was verified (OpenAI-family verifier findings addressed)
- QA results (test coverage, visual QA, security)
- Any open items or follow-ups

---

## Hard Rules

1. **OpenAI-family verification covers EVERY diff.** No implementation subphase ships without cross-model verification. In Codex harness, this must be native sub-agents, not nested CLI. If no valid route exists, STOP and ask before degraded mode.
2. **Parallel by default.** Independent subphases implement in parallel. Only serialize on data dependencies.
3. **Named agents always.** Enables lane communication. Pattern: `impl-{sub}`, `review-primary`, `qa-browse`, `cross-monitor`, `openai-*`.
4. **Fix before proceeding.** CRITICAL/HIGH findings from any gear must be fixed before entering the next gear.
5. **Everything on disk.** All progress, findings, and QA results written to the phase plan directory.
6. **Re-read before modify.** Always read current file state from disk. Never rely on cached content.
7. **Multi-agent conflict check.** `git status` + last 10 phases scan at start of every gear.
8. **Session-scoped commits only.** Never blindly stage all changes (other agents may be working).
9. **80% coverage gate.** Tests must exist and pass for new code. Coverage >= 80%.
10. **Visual QA is not optional.** If the change has UI, browse-qa runs. No exceptions.
11. **Three verification passes minimum.** Every piece of code gets: implementation review (primary model), cross-model review (OpenAI-family verifier), and QA verification.
