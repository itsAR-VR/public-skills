---
name: deep-sweep
description: >
  Multi-model deep analysis orchestrator with GSD-absorbed parallel research wave.
  Runs a 5-researcher parallel wave (framework + phase + pattern + assumptions +
  advisor researchers) synthesized into a research brief, then sends the active
  primary reasoning model on problems, cross-verifies with a harness-routed
  OpenAI-family verifier,
  consolidates into a phase plan, then runs parallel RED TEAM + cross-comparison
  on every subphase with lane-owner communication. Use when: "deep sweep",
  "war council", "cross verify everything", "analyze deeply", "multi-model
  analysis", "red team this plan", "stress test this architecture". For
  single-pass planning see phase-plan. For execution see deep-build or
  terminus-maximus.
metadata:
  author: AR180
  version: 1.1.0
related_skills:
  - phase-plan
  - skill-oracle
  - think
  - terminus-maximus
  - graphify
  - gitnexus
  - deep-build
  - goal-post
  - ultra-review
  - deep-clean
  - browser-harness
  - verify
  - voice-model-strategy
  - comparative-analysis-orchestrator
  - build
  - llm-council
  - superpowers-dispatching-parallel-agents
---

# Deep Sweep

Multi-model, multi-pass analysis orchestrator. Guarantees thorough coverage through
cross-verification between the **active primary reasoning model** and a
**harness-routed OpenAI-family verifier** (independent verification), with parallel
RED TEAM passes and cross-comparison on every subphase.

When `deep-sweep` is part of a phase workflow, read
`skills/phase-plan/references/09_PHASE_PIPELINE_PLAYBOOK.md`. The playbook keeps
the shared beginner path and handoff sequence out of this skill file. This file
owns the `deep-sweep` mechanics: model routing, research wave, gap register,
red-team passes, and cross-verification.

**Core insight:** Sub-agents exist to isolate context and provide genuinely independent
verification. Primary-model reasoning + OpenAI-family verification catches what
neither catches alone.

## Model Currency & Harness Routing

Current hardcoded model snapshot, verified from official docs on 2026-04-28:

- **OpenAI/Codex verifier:** `gpt-5.5`
- **Claude Code hardcoded latest:** `claude-opus-4-7`
- **Claude Code aliases:** `opus`, `sonnet`, and `haiku` resolve through Claude Code's model configuration; prefer aliases when the user wants automatic latest-family routing.
- **Verification sources:** OpenAI GPT-5.5 release note (`https://openai.com/index/introducing-gpt-5-5/`); Anthropic Claude Code model configuration (`https://support.claude.com/en/articles/11940350-claude-code-model-configuration`, `https://code.claude.com/docs/en/model-config`).

Before changing a hardcoded model ID, do a quick official-source refresh:

1. Check OpenAI model/release docs for the current Codex-capable model.
2. Check Anthropic Claude Code model configuration for the current Claude Code model IDs.
3. Check local CLI support: `which -a codex`, `codex --version`, `codex exec --help`, and `claude --version` when available.
4. Record the model ID and refresh date in the plan or run log.

**Never downgrade to an older OpenAI model.** If the latest required OpenAI model is
unsupported by the local Codex CLI, upgrade Codex or stop and report the unsupported
model. Do not silently fall back.

If `which -a codex` returns multiple binaries, test each candidate and use the
highest supported `codex-cli` version through `CODEX_BIN=/absolute/path/to/codex`.
Do not trust bare `codex` when an older Homebrew/global binary shadows a newer npm
binary.

OpenAI-family verifier routing:

- **Codex main harness:** spawn native sub-agents only. Do not invoke nested `codex`, `codex exec`, MCP, or shell fallback.
- **Claude Code main harness:** `codex exec` is allowed after model-currency and CLI-support preflight passes.
- **Other provider main harness:** use its native agent delegation when available.
- **No native agent route and no allowed Claude-to-Codex CLI route:** stop and ask the user before any degraded single-provider verification.

## When to Activate

| Signal | Example |
|--------|---------|
| Explicit invocation | "deep sweep", "war council", "/deep-sweep" |
| High-stakes planning | Auth, payments, data migrations, breaking changes |
| Complex multi-problem analysis | 3+ interdependent problems or requirements |
| Pre-implementation confidence check | "I want to be sure before we build this" |
| Cross-cutting concern detection | Features that touch multiple domains |

## Composition

This skill composes existing skills + GSD research agents as subroutines:

| Subroutine | Purpose | Phase |
|------------|---------|-------|
| `$skill-oracle` | Discover available skills for the problem domain | 0 |
| `$graphify` | Knowledge graph — cross-document context for analysis agents | 0, 1, 5 |
| `$gitnexus` | Code graph — impact analysis, symbol context, change detection | 0, 1, 4, 5 |
| `gsd-framework-selector` | Stack/framework researcher (GSD wave) | 0.5 |
| `gsd-phase-researcher` | Features/domain researcher (GSD wave) | 0.5 |
| `gsd-pattern-mapper` | Architecture/pattern researcher (GSD wave) | 0.5 |
| `gsd-assumptions-analyzer` | Pitfalls/assumptions researcher (GSD wave) | 0.5 |
| `gsd-advisor-researcher` | Prior-art researcher (GSD wave) | 0.5 |
| `gsd-research-synthesizer` | Merges research wave outputs into a brief | 0.5 |
| `$plan` / `$phase-plan` | Create phase plan structure on disk | 3 |
| `$phase-gaps` | RED TEAM each subphase | 4 |
| OpenAI-family verifier | Independent cross-verification via harness-routed latest OpenAI model | 2, 4 |
| `$phase-review` / `$verify` | Final sanity check on completed plan | 7 |

## Adaptive Gate Selection (harness-aware)

This skill runs across multiple harnesses. Before invoking each internal gate (phase-gaps RED TEAM, OpenAI-family cross-verify, GSD research wave, cross-comparison pair), the runtime checks what the active harness already protects against and skips duplicative gates with a documented reason.

- **Procedure + gate↔harness overlap map**: `~/.claude/skills/lib/adaptive-gate-selection.md`
- **Skip policy**: skips are active decisions, not defaults. If no pre-existing mechanism covers the gate's intent, run the gate.

**Every gate decision MUST be logged:**

```bash
bash $HOME/.claude/skills/lib/skill-gate-logger.sh \
  --skill deep-sweep \
  --gate <gate-name> \
  {--verdict PASS|FAIL|ESCALATE|PARTIAL  OR  --skipped "<why>"} \
  --reason "<one-line reason>"
```

Logs route per-harness automatically.

## Skill Composition (vertical mode)

When `default_slice_type: vertical`, this skill composes with the broader ecosystem at named gates. Tiered: required core fires deterministically; recommended optional fires when conditions match.

### Required core (MUST invoke)

- `$skill-oracle` @ Phase 0 (already wired) — discover available skills for the problem domain.
- `$graphify` + `$gitnexus` @ Phase 0 / 1 / 4 / 5 (already wired) — knowledge-graph + code-graph context for every analysis agent.
- 5 GSD researchers (`gsd-framework-selector`, `gsd-phase-researcher`, `gsd-pattern-mapper`, `gsd-assumptions-analyzer`, `gsd-advisor-researcher`) @ Phase 0.5 (already wired) — parallel research wave synthesized into a research brief.
- ECC `architect` agent @ Phase 4 lane #4 — integration-contract auditor; design lens on cross-feature emit/consumer contracts.
- `gsd-integration-checker` @ Phase 4 lane #4 — complement to architect; cross-feature compatibility verification.

### Recommended optional (SHOULD invoke when conditions match)

- `superpowers-dispatching-parallel-agents` @ Phase 4 lane spawn — discipline for the 4-lane (vertical) or 3-lane (horizontal) per-subphase spawn.
- ECC `chief-of-staff` agent @ Phase 5 cross-comparison — prioritization across all subphase findings.

### Per-slice tools (fire once per feature_id)

- `mcp__gitnexus__impact` per emitter symbol declared in `integration_contracts` — Phase 4 vertical-mode auditor input; surfaces blast radius of each contract symbol.
- `mcp__graphify__get_neighbors` per contract module — community-level co-changes; reveals cross-document neighbors that the auditor must consider.

### Source of truth (avoid rot)

- ECC catalog: `skills/everything-claude-code/agents/` and `commands/`
- GSD catalog: `~/.claude/agents/gsd-*`
- Superpowers catalog: `skills/superpowers-*/` (vendored from `anthropics/claude-plugins-official`; no plugin dependency)

## Procedure

> Detailed prompt templates in `references/agent-prompts.md`.
> Expanded decision trees in `references/procedure.md`.
> Edge cases and recovery in `references/edge-cases.md`.

---

### Phase 0 — Preflight

1. Run `$skill-oracle` — discover skills available for the problem domain
2. `git status --porcelain` — check workspace state
3. `ls -dt docs/planning/phase-* 2>/dev/null | head -10` — scan for active phases
4. **Graphify structural context:**
   - Check if `graphify-out/graph.json` exists and is current
   - If missing: run `/graphify .` to build the knowledge graph (provides god nodes, community structure, cross-document connections)
   - If stale (>50 commits behind): run `/graphify . --update` to refresh
   - If current: read `graphify-out/GRAPH_REPORT.md` — extract god nodes, surprising connections, and community labels for use in Phase 1 agent prompts
   - **Feed every Phase 1 primary-model agent the god nodes list and community map** — this gives them structural awareness before they analyze
5. **GitNexus code graph:**
   - Run `gitnexus status` — verify index exists and is current
   - If stale or missing: run `gitnexus analyze --embeddings --skills` to index
   - For each problem in the problem set, run `mcp__gitnexus__impact` on the primary symbols involved — this reveals blast radius before analysis begins
   - **Feed every primary-model agent the impact results** — they need to know what code depends on what before proposing changes
   - GitNexus provides code-level precision; graphify provides doc-level context. Use both.
6. Extract the **problem set** from conversation context
7. Number each problem: P1, P2, P3, ...

**Gate:** Proceed only with a clear, numbered problem set AND both graph contexts loaded.

---

### Phase 0.5 — GSD Research Wave (parallel)

Absorbed from GSD. Runs AFTER problem set is defined, BEFORE primary-model analysis, so Phase 1 agents enter with a synthesized research brief already in context. All researchers run **simultaneously** — independence prevents framing bias.

**Launch five researchers in parallel** (all spawned in a single message):

```
# 1. Stack/framework lens
Agent(
  name: "research-framework",
  subagent_type: "gsd-framework-selector",
  prompt: <framework research prompt for the problem set — see references/gsd-research-layer.md>
)

# 2. Features/phase lens
Agent(
  name: "research-phase",
  subagent_type: "gsd-phase-researcher",
  prompt: <phase-specific domain deep-dive prompt>
)

# 3. Architecture/pattern lens
Agent(
  name: "research-patterns",
  subagent_type: "gsd-pattern-mapper",
  prompt: <architectural patterns + anti-patterns prompt>
)

# 4. Pitfalls/assumptions lens
Agent(
  name: "research-assumptions",
  subagent_type: "gsd-assumptions-analyzer",
  prompt: <surface hidden assumptions in the problem framing>
)

# 5. Prior-art lens
Agent(
  name: "research-advisor",
  subagent_type: "gsd-advisor-researcher",
  prompt: <find 2-3 battle-tested prior implementations to borrow from>
)
```

**All five must complete before synthesis.** Each returns a structured brief with: findings, evidence, confidence, recommendations.

**Then synthesize:**

```
Agent(
  name: "research-synthesizer",
  subagent_type: "gsd-research-synthesizer",
  prompt: `
Merge the following five research briefs into a single consolidated research document.

<framework_brief>...</framework_brief>
<phase_brief>...</phase_brief>
<patterns_brief>...</patterns_brief>
<assumptions_brief>...</assumptions_brief>
<advisor_brief>...</advisor_brief>

Produce: unified narrative, agreement/disagreement between lenses, open questions, recommended approach with tradeoffs. Flag anything that would change the problem framing itself (upstream issues).
`
)
```

Write synthesized brief to `docs/planning/phase-{N}/research-brief.md` (create dir if missing).

**Gate:** Research brief exists on disk. Feed to every Phase 1 primary-model agent in addition to graphify/gitnexus context.

**Skip criteria:** You MAY skip the research wave when:
- Problem set is self-contained (no external framework or prior-art questions)
- Domain is well-understood and recently worked in (last 2 weeks)
- Total research budget is < 10 min and speed matters more than thoroughness

Record the skip reason in the root plan's Context section. Do NOT skip for: new domain, first-phase projects, or auth/payments/data migration problems.

---

### Phase 1 — Primary-Model Deep Analysis

For each problem P(N), launch a **named** primary-model agent:

```
Agent(
  name: "primary-deep-{N}",
  model: "<active-primary-model>",
  subagent_type: "general-purpose",
  prompt: <Phase 1 prompt from references/agent-prompts.md>
)
```

**Spawn independent problems in parallel.** Each agent:
- Analyzes the problem with full extended thinking budget
- **Uses graphify context** — include god nodes, community labels, and surprising connections from GRAPH_REPORT.md in every agent prompt. This tells the agent which code/doc modules are central, how they cluster, and what cross-cutting relationships exist.
- Identifies risks, dependencies, edge cases, implementation approaches
- Outputs structured findings (see references/agent-prompts.md §1 for format)

**Gate:** Wait for ALL primary-model agents to complete. Collect structured findings.

---

### Phase 2 — OpenAI-Family Cross-Verification

Route an OpenAI-family verifier to independently verify all primary-model findings:

```text
IF active_harness == "codex":
  Agent(
    name: "openai-verify-phase-{N}",
    subagent_type: "reviewer",
    prompt: "Read docs/planning/phase-{N}/deep-sweep-findings.md and all subphase plans. Cross-verify for gaps, contradictions, and over/under-engineering. Rate each finding: CRITICAL/HIGH/MEDIUM/LOW."
  )

ELSE IF active_harness == "claude":
  OPENAI_LATEST_MODEL="${OPENAI_LATEST_MODEL:-gpt-5.5}"
  CODEX_BIN="${CODEX_BIN:-codex}"
  "$CODEX_BIN" exec --model "$OPENAI_LATEST_MODEL" \
    -c model_reasoning_effort=high \
    --sandbox read-only \
    --skip-git-repo-check \
    "Read docs/planning/phase-{N}/deep-sweep-findings.md and all subphase plans. Cross-verify for gaps, contradictions, and over/under-engineering. Rate each finding: CRITICAL/HIGH/MEDIUM/LOW." \
    2>/dev/null

ELSE IF native_subagents_available:
  Agent(name: "openai-verify-phase-{N}", subagent_type: "reviewer", prompt: <same verifier prompt>)

ELSE:
  STOP and ask user before degraded single-provider verification.
```

Verifier task:
- Review each primary-model finding for correctness and completeness
- Find **gaps**: problems the primary-model analysis didn't consider, edge cases missed
- Find **contradictions**: conflicting recommendations across problems
- Find **over/under-engineering**: solutions too complex or too naive
- Rate each gap: CRITICAL / HIGH / MEDIUM / LOW

**Gate:** OpenAI-family gap report collected. Merge with primary-model findings.

---

### Phase 3 — Consolidate into Phase Plan

**Pick the slicing mode for the consolidated plan.** If the primary-model analysis surfaced vertical-feature-shaped problems (one user-visible capability per problem, with DB+API+UI+tests boundaries), set `default_slice_type: vertical` in the root plan front-matter and emit each problem as a vertical subphase with the Feature Slice front-matter. If problems are cross-cutting concerns (refactors, migrations, type changes spanning the whole codebase), set `default_slice_type: horizontal`. Reuse the same decision tree as `/phase-plan` Step 4.5. When in doubt for a feature-shaped phase, default to vertical.

Use the `$plan` pattern to materialize analysis into disk structure:

1. Determine next phase number
2. Create `docs/planning/phase-{N}/`
3. Write root `plan.md`:
   - **Original Request** — verbatim anchor block from user
   - **Problem Set** — P1..P(N) with consolidated analysis
   - **Cross-Model Findings** — primary-model analysis + OpenAI-family gap report
   - **Success Criteria** — derived from analysis
   - **Subphase Index** — one subphase per logical problem area
4. Write subphase scaffolds: `a/plan.md`, `b/plan.md`, etc.
   - Each contains: scope, approach, risks, acceptance criteria

**Gate:** Phase plan exists on disk with all subphases scaffolded.

---

### Phase 4 — Parallel Subphase Analysis

For EACH subphase, launch **three agents in parallel**:

```
# 1. RED TEAM (phase-gaps pattern)
Agent(
  name: "gaps-{sub}",
  model: "<active-primary-model>",
  subagent_type: "general-purpose",
  prompt: <Phase-gaps RED TEAM prompt for subphase {sub}>
)

# 2. Primary-model Deep Dive on subphase specifics
Agent(
  name: "primary-sub-{sub}",
  model: "<active-primary-model>",
  subagent_type: "general-purpose",
  prompt: <Subphase deep dive prompt>
)

# 3. OpenAI-family verifier (harness-routed; see Model Currency & Harness Routing)
OpenAIFamilyVerifier(
  name: "openai-sub-{sub}",
  prompt: "Verify subphase {sub} plan against the actual codebase..."
)
```

**All subphases run their 3 agents simultaneously** — maximum concurrency.
Total agents spawned = (number of subphases) x 3.

**Vertical-mode 4th lane: integration-contract auditor.** When `slice_type: vertical` for the subphase, spawn a 4th agent named `integration-{sub}` alongside the existing three. The auditor is composed of:

- **ECC `architect` agent** — contract design lens on emit/consumer shape, event-type completeness, and wire-format compatibility.
- **`gsd-integration-checker` agent** — cross-feature compatibility verification against sibling slices' surfaces.
- **`mcp__gitnexus__impact`** — fired on each emitter symbol declared in the slice's `integration_contracts` to surface blast radius and reveal callers/consumers the planner did not anticipate.
- **`mcp__graphify__get_neighbors`** — fired on the contract's containing module to surface community-level co-changes (modules historically edited together with the contract module).

- **Inputs**: the slice's `integration_contracts` list from front-matter; the codebase; sibling slices' surfaces; the impact + neighbors results above.
- **Job**: audit cross-feature contract risks. Catch (a) emit shape vs. consumer shape mismatches (e.g., slice A emits `{userId}`, slice B consumes `{user_id}`); (b) missing event types or notification fan-out gaps; (c) wire-format incompatibilities; (d) feature flag toggles that cross slices.
- **Output**: structured findings citing specific symbols + impact zones + community-level co-change patterns (not prose alone), with severity (LOW / MEDIUM / HIGH / CRITICAL) and recommendation. HIGH/CRITICAL findings require contract artifact (Zod / Pydantic / JSON Schema) committed in the emitter slice's surfaces and imported by the consumer slice — prose contracts are not sufficient for HIGH/CRITICAL.

The 3-agent baseline (gaps, primary, verifier) stays unchanged for `slice_type: horizontal` subphases. Total agents per vertical subphase: 4. Total per horizontal subphase: 3.

**Gate:** All subphase analysis agents complete. Collect all findings.

---

### Phase 5 — Cross-Comparison Pair

After Phase 4 completes, launch ONE MORE pair that sees **all subphases together**:

```
# Primary model: cross-subphase interaction analysis
Agent(
  name: "cross-compare-primary",
  model: "<active-primary-model>",
  subagent_type: "general-purpose",
  prompt: <Cross-comparison prompt from references/cross-comparison.md>
)

# OpenAI-family verifier: independent cross-subphase verification
OpenAIFamilyVerifier(
  name: "openai-cross-compare",
  reasoning_effort: "xhigh",
  prompt: "<all subphase plans + Phase 4 findings>"
)
```

This pair looks for:
- **Interaction effects** — things fine in isolation, broken when combined
- **Dependency chains** — A needs B needs C, but C assumes A is done
- **Cross-subphase conflict lens — mode-aware:**
  - **Horizontal mode** (`slice_type: horizontal` subphases): Resource conflicts — two subphases modifying the same files/APIs/migrations. File-overlap and contract-overlap are the failure modes.
  - **Vertical mode** (`slice_type: vertical` subphases): Contract conflicts — feature A's emit shape doesn't match feature B's consumer shape; feature A's schema migration breaks feature B's existing query; feature A's UI prop change breaks feature B's render. Cross-feature `integration_contracts` are the failure modes.
- **Gap coverage** — problems that fall between subphase boundaries
- **Assumption conflicts** — subphase A assumes X, subphase B assumes NOT X
- **Graphify community crossings** — use `/graphify query` to check if subphases cross community boundaries in the knowledge graph. Subphases that touch multiple communities have higher interaction risk.
- **GitNexus blast radius** — for each subphase, run `mcp__gitnexus__impact` on the key symbols being modified. If two subphases have overlapping impact zones, flag as a resource conflict. Run `mcp__gitnexus__detect_changes` on the planned diff to map affected symbols that span subphase boundaries.

**Gate:** Cross-comparison findings collected and severity-rated.

---

### Phase 6 — Lane Communication

For each finding from Phase 4-5 rated HIGH or CRITICAL:

1. **Identify the owning lane** — which subphase does this finding affect?
2. **Communicate to the lane agent:**
   - If the `gaps-{sub}` agent is still addressable: `SendMessage(to: "gaps-{sub}")`
   - Otherwise: spawn a new agent to update the subphase plan file
3. **Lane owner incorporates finding** — update subphase plan.md with:
   - The finding and its severity
   - The proposed mitigation
   - Any new acceptance criteria
4. **Document resolution** in the subphase's Output section

If a finding affects MULTIPLE lanes:
- Communicate to ALL affected lane owners
- Add to root plan's **Cross-Cutting Concerns** section

**Cap:** Maximum 3 communication rounds per finding. If unresolved, escalate to user.

---

### Phase 6.5 — Auto-Correct Plans (MANDATORY)

**This step is not optional.** Confidence numbers are meaningless against uncorrected plans.
The deep-sweep-findings.md file is a changelog, not a TODO list.

For EACH finding rated CRITICAL or HIGH from Phases 4-6:

1. **Read the affected subphase plan from disk** (re-read, don't use cached)
2. **Apply the correction directly into the plan.md:**
   - Add a "Deep Sweep Corrections Applied" section listing what changed
   - Modify the Work steps to incorporate the fix (add missing steps, fix parameters, update file lists)
   - Update any code snippets that were wrong
   - Add new test cases for edge cases discovered
3. **For MEDIUM findings:** add as notes in the plan but don't restructure
4. **Write the updated plan back to disk**

After all plans are corrected:
- Re-assess confidence based on the **corrected** plan, not the original
- The confidence number presented to the user must reflect what will actually be built
- If a correction raises new questions, add them as Open Questions

**Gate:** All subphase plan.md files updated on disk with corrections incorporated.
The deep-sweep-findings.md becomes a record of what was found and fixed, not what remains to do.

**Anti-pattern to avoid:** Reporting 72% confidence because "the plan has gaps" when
the gaps have known fixes. That wastes the user's time asking "why so low?" when the
answer is "because we didn't write the fix into the plan yet." Always correct first,
then report.

---

### Phase 7 — Final Consolidation

1. Re-read all updated subphase plans from disk
2. Update root `plan.md`:
   - **Cross-Cutting Concerns** section (from Phase 5)
   - **Risk Register** — all CRITICAL/HIGH findings + mitigations
   - **Confidence Ratings** per subphase (target: >= 84.7%)
   - Anything below 84.7% becomes an explicit **Open Question**
   - Updated **Success Criteria** incorporating discovered edge cases
3. Run `$phase-review` on the complete plan as a final sanity check
4. Present summary to user with:
   - Total findings by severity
   - Subphase confidence ratings
   - Open questions requiring user input
   - Recommendation: ready to execute, or needs more analysis

---

## Hard Rules

1. **Never skip OpenAI-family cross-verification.** The whole point is independent-model verification. In Codex harness, this must be native sub-agents, not nested CLI. If no valid route exists, STOP and inform user.
2. **Always name agents.** Enables lane communication via SendMessage. Names follow pattern: `primary-deep-{N}`, `gaps-{sub}`, `primary-sub-{sub}`, `cross-compare-primary`, `openai-*`.
3. **Parallel by default.** Only serialize when there's a data dependency between phases. Within phases, maximize concurrency.
4. **Findings flow to lane owners.** Don't just collect findings — communicate them to the agent/plan that can act on them.
5. **Everything on disk.** All analysis, findings, and resolutions written to the phase plan directory. No in-chat-only analysis.
6. **Verbatim original request.** Anchor block preserved in root plan exactly as user stated it.
7. **84.7% confidence threshold.** Below this, raise as explicit Open Question, not assumption.
8. **3-round communication cap.** If a finding can't be resolved in 3 rounds, escalate to user.
9. **Re-read before modify.** Always read current file state before writing. Never rely on cached content.
10. **Multi-agent conflict check.** Scan last 10 phases before starting. Note file/domain overlaps.
