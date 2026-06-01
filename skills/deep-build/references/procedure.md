# Detailed Procedure

Expanded decision trees and implementation details for each gear of Deep Build.

---

## Pre-Invocation Checklist

- [ ] Problem/feature is clear (user has stated what to build)
- [ ] Working directory is the project root
- [ ] Git state is clean or understood
- [ ] OpenAI-family verifier route is selected for the active harness
- [ ] Model currency check completed against official docs and local CLI support
- [ ] Project can build (`npm run build` or equivalent succeeds)

If no OpenAI-family verifier route is available: stop and ask before degraded mode (see edge-cases.md).

---

## Gear 0: Preflight — Decision Tree

```
START
├── Run $skill-oracle → note available skills
├── Check git status
│   ├── Clean? → proceed
│   ├── Uncommitted? → warn user, proceed
│   └── Merge conflict? → STOP, resolve first
├── Scan active phases
│   ├── No phases? → must start at Gear 1
│   ├── Latest phase incomplete? → check if we should resume it
│   └── Latest phase complete? → create new phase
├── Determine entry gear
│   ├── No plan? → Gear 1 (Plan)
│   ├── Plan exists, no code? → Gear 2 or 3
│   ├── Code exists, not reviewed? → Gear 4
│   ├── Reviewed, not QA'd? → Gear 5
│   └── All done? → Gear 6 (Ship)
└── Announce: "Starting deep-build at Gear {N}: {gear_name}"
```

---

## Gear 1: Plan — Decision Tree

```
PLAN ENTRY
├── Plan exists?
│   ├── YES → validate currency
│   │   ├── Plan files modified since creation? → quick $phase-gaps
│   │   ├── Codebase changed since plan? → OpenAI-family codebase check
│   │   └── Plan still current? → proceed to Gear 2
│   └── NO → run full $deep-sweep
│       ├── Deep sweep creates plan at docs/planning/phase-{N}/
│       ├── Wait for deep-sweep to complete
│       └── Verify plan structure: root plan + subphases
└── Gate: plan on disk, subphases scaffolded
```

---

## Gear 2: Eng Review — Orchestration

Launch two agents in parallel:

**Agent 1: Primary-model RED TEAM**
- Uses $phase-gaps pattern
- Focuses on: missing steps, wrong assumptions, ordering issues
- Output: findings by severity + recommended changes

**Agent 2: OpenAI-Family Codebase Verification**
```text
IF active_harness == "codex":
  Agent(
    name: "openai-eng-review",
    subagent_type: "reviewer",
    prompt: "Verify this implementation plan against the actual codebase: referenced files/functions, compatibility, hidden dependencies, tests to update."
  )

ELSE IF active_harness == "claude":
  OPENAI_LATEST_MODEL="${OPENAI_LATEST_MODEL:-gpt-5.5}"
  CODEX_BIN="${CODEX_BIN:-codex}"
  "$CODEX_BIN" exec --model "$OPENAI_LATEST_MODEL" -c model_reasoning_effort=high --sandbox read-only \
    "Given this implementation plan, verify against the actual codebase:
     1. Do referenced files/functions exist?
     2. Are the planned changes compatible with current code?
     3. Are there hidden dependencies the plan doesn't account for?
     4. What existing tests will need updating?
     Plan: <plan content>" 2>/dev/null

ELSE IF native_subagents_available:
  Agent(name: "openai-eng-review", subagent_type: "reviewer", prompt: <same verifier prompt>)

ELSE:
  STOP and ask user before degraded single-provider verification.
```

In Codex main harness, nested `codex exec` is forbidden. In Claude Code, `codex exec`
is allowed only after `which -a codex`, `codex --version`, and model support checks
pass. If multiple Codex binaries are installed, set `CODEX_BIN` to the highest
supported version before invoking CLI. If the latest model is unsupported, upgrade
Codex or stop; do not downgrade.

Current hardcoded snapshot, refreshed from official docs on 2026-04-28:

- OpenAI/Codex verifier: `gpt-5.5`
- Claude Code pinned latest: `claude-opus-4-7`
- Claude Code family aliases: `opus`, `sonnet`, `haiku`

**Cross-compare:**
- Both agree → update plan with findings
- Disagree → primary-model tie-breaker agent reviews both reports
- CRITICAL findings → must be addressed before Gear 3

**Update plan:**
- Add eng-review findings to root plan
- Update subphase plans with discovered constraints
- Mark plan as "eng-reviewed"

---

## Gear 3: Implement — Orchestration

This is the most complex gear. Full detail in `references/implementation-lanes.md`.

**Summary flow:**

```
1. Read all subphase plans from disk
2. Determine dependency ordering between subphases
3. Launch Tier 1 implementation agents (parallel)
4. As each completes:
   a. Run OpenAI-family diff verification
   b. If findings: fix, re-verify
   c. Update subphase plan with Output/Handoff
5. After every 2nd completion: run cross-monitor
6. Launch Tier 2 when Tier 1 is done (if dependencies exist)
7. Repeat until all subphases complete
8. Final cross-monitor on all completed work
```

**Key decisions during implementation:**

```
Agent reports BLOCKED?
├── Missing env var → note, ask user
├── Missing dependency → install it, re-run
├── Plan unclear → refer to eng-review findings, decide
└── Conflicting code → check cross-monitor, resolve

OpenAI-family verifier finds CRITICAL bug?
├── Agent still running? → SendMessage("Fix: {finding}")
├── Agent done? → spawn fix agent
└── Fix verified? → proceed
     └── Fix not verified? → escalate to user after 3 attempts

Cross-monitor finds conflict?
├── File conflict → determine merge order, fix
├── Type conflict → update shared type, propagate
├── Migration conflict → reorder migrations
└── Unresolvable? → escalate to user
```

---

## Gear 4: Review — Orchestration

Launch three reviewers in parallel:

1. **Primary-model code-reviewer** (subagent_type: "code-reviewer")
   - Full diff review: `git diff {base}...HEAD`
   - Checks: quality, patterns, error handling, naming

2. **OpenAI-family independent review**
   - Same diff, different model
   - Checks: bugs, edge cases, security, type safety

3. **Security reviewer** (subagent_type: "security-reviewer")
   - Only on diffs touching: auth, user input, DB queries, API endpoints, crypto
   - Skip if no security-sensitive changes

**After reviews complete:**

```
Cross-compare all findings
├── All three agree → high confidence, fix immediately
├── Two agree → likely real issue, fix
├── One reports, others don't → investigate before acting
└── Conflicting → primary-model tie-breaker resolves

Fix all CRITICAL findings
Fix all HIGH findings
Note MEDIUM findings in plan
Ignore LOW (unless easy to fix)
```

**Run quality gates:**
```bash
npm run lint     # or project equivalent
npm run build    # must pass
npm run test     # must pass
```

If any gate fails → fix → re-run → must pass before Gear 5.

**Update phase plan:**
- Each subphase: fill in Output and Handoff
- Root plan: update success criteria checkmarks
- Root plan: add review findings summary

---

## Gear 5: QA — 4-Layer Orchestration

> Full protocol in `references/qa-protocol.md`.

Launch QA layers in parallel (skip layers per the skip table in qa-protocol.md):

**Layer 1: Automated Tests** (always)
- Run project test suite (`npm test` / `pytest` / `go test`)
- Check coverage >= 80%
- Write tests for uncovered new code
- No flaky patterns

**Layer 2: Visual QA** (if UI changes)
- Desktop + mobile (375px) screenshots via $browse-qa
- Console error check
- Critical interaction path
- Explicit pass/fail with screenshot evidence

**Layer 3: Functional QA** (if app has interactive features)
- Actually use the app via Claude-in-Chrome MCP tools
- Computer Use for complex interactions (drag-drop, canvas, multi-step)
- Browser Harness CLI (`npx browser-harness test`) for repeatable scripts
- OpenClaw persistent profile for auth-gated flows
- Test: happy path, error states, persistence, auth, mobile

**Layer 4: OpenAI-Family Functional Verification** (always)
- Test suite completeness analysis
- API contract verification
- Data flow correctness
- Error path coverage
- Cross-model independent assessment

**QA failure handling (max 3 retries per layer):**

```
Layer 1 failure?
├── Test fails → report to impl agent, fix code, re-run
├── Coverage low → write missing tests, re-check
└── Environment issue → document, skip with note

Layer 2 failure?
├── Missing UI → fix component, re-screenshot
├── Layout broken → fix styles, re-screenshot
└── Console errors → fix source, re-check

Layer 3 failure?
├── Flow broken → fix implementation, re-test flow
├── Auth issue → check auth logic, re-test
├── Data not persisting → fix DB/state logic, re-test
└── Browser tools unavailable → fallback to Browser Harness CLI or skip

Layer 4 findings?
├── Missing tests → write them now
├── API contract mismatch → fix implementation or types
├── Security finding → fix immediately (CRITICAL blocks)
└── Already covered → document why it's OK

After 3 retries on any layer → escalate to user
```

**QA result aggregation:**
```
LAYER 1: PASS/FAIL — coverage: X% — N tests written
LAYER 2: PASS/FAIL — screenshots attached — N issues
LAYER 3: PASS/FAIL — N flows tested — N issues  
LAYER 4: PASS/FAIL — N findings by severity
OVERALL: PASS (all layers pass) / FAIL (any layer fails)
```

Proceed to Gear 6 only when OVERALL = PASS.

---

## Gear 6: Ship — Orchestration

Follow `$commit-work` pattern strictly:

```
1. git status → identify ONLY session-scoped changes
2. Cross-reference with subphase plans → know what you changed
3. Stage explicitly: git add <specific files>
   NEVER: git add . / git add -A
4. git diff --cached → review staged changes
5. Determine logical commit boundaries:
   - One commit per subphase (if clean)
   - Split if subphase has distinct concerns
6. Conventional Commits message:
   feat(scope): summary
   <body explaining what and why>
7. Final verification: lint + build
8. git commit
9. If push requested: git push -u origin {branch}
```

**Completion report to user:**
- Subphases completed (list with summaries)
- OpenAI-family verification results (findings fixed)
- QA results (test coverage %, visual QA pass/fail)
- Security review results (if applicable)
- Any open items or follow-ups
- Total agents spawned across all gears
