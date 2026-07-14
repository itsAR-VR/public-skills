# GSD Execution Layer — Deep Reference

Absorbed from GSD's execution patterns. Augments deep-build's gears with structural awareness, goal-backward test coverage, atomic commits, and structured debug loops.

## Core principle

Every gear now has a corresponding GSD agent that provides an **additional independent signal**:

- Codebase awareness (what's there already) — `gsd-codebase-mapper`
- Coverage awareness (does the test set prove the requirement?) — `gsd-nyquist-auditor`
- Execution discipline (atomic commits, checkpoints) — `gsd-executor`
- Debug discipline (reproduce → isolate → fix → verify) — `gsd-debugger`
- Completion awareness (did we build what we promised?) — `gsd-verifier`

Each is spawned via the Agent tool at its corresponding gear.

## Gear 0 — Codebase Mapping (GSD addition)

Before any code is written, invoke:

```
Agent(
  name: "codebase-map",
  subagent_type: "gsd-codebase-mapper",
  prompt: `
Produce a structural brief of this codebase with the following for the planned scope:

<scope_files_and_modules>
{list from plan.md "Files to modify" section, plus any modules the plan touches}
</scope_files_and_modules>

Include:
- Current module organization (dirs, file sizes, depth)
- Naming conventions already in use (to match)
- Existing patterns in adjacent code (to not violate)
- Tests for the affected code (existing shape, coverage gaps)
- Hidden coupling (imports/exports, shared state)

Do NOT propose changes. Just describe what's there.
Return the brief to disk at docs/planning/phase-{N}/codebase-map.md.
`
)
```

Feed this to Gear 3 implement agents. Prevents writing code that duplicates or clashes with existing structure.

## Gear 1/2 — Nyquist Audit (GSD addition)

Named after the Nyquist sampling theorem: to capture a signal, you must sample at twice its frequency. Analogously, to verify a requirement, you must test it at least twice — once for the happy path, once for the boundary/error case.

After the plan passes phase-gaps validation, invoke:

```
Agent(
  name: "nyquist-audit",
  subagent_type: "gsd-nyquist-auditor",
  prompt: `
Audit the test coverage plan goal-backward.

<plan_md>
{path to plan.md}
</plan_md>

<existing_tests>
{list of test files currently covering the affected modules}
</existing_tests>

For every requirement in the plan, verify:
1. There IS a test that would fail if the requirement is not met (happy path)
2. There IS a test for the boundary/error case
3. The test is at the right abstraction level (unit vs integration vs e2e)

Return:
- Coverage matrix: requirement → test(s) → abstraction level
- Missing coverage flagged as CRITICAL (blocks implementation)
- Over-coverage flagged as LOW (cleanup opportunity)
- Recommended test additions (with skeleton)
`
)
```

If CRITICAL gaps exist → update the plan's test scaffolding before Gear 3.

## Gear 3 — Executor Patterns (GSD addition)

### Atomic commits per task

The plan lists discrete tasks. Each task = one commit. Not one giant PR.

**Why:** If task 4 breaks something, you can `git revert SHA-of-task-4` without losing tasks 1-3. If you batch, revert is all-or-nothing.

**Pattern:**

```bash
# For each task in plan.md subphase:
# 1. Implement the task
# 2. Run tests for affected area
# 3. Commit atomically
git add <files touched by this task>
git commit -m "phase-{N}/{subphase}: <task description>

Implements: <requirement from plan>
Tests: <tests added/updated>
"
# 4. Cross-verify with the harness-routed OpenAI-family verifier (existing deep-build pattern)
# 5. Move to next task
```

### Checkpoint protocol

At every subphase boundary, write a checkpoint to the plan's Output section:

```markdown
## Subphase {X} — Output

Status: COMPLETE | PARTIAL | BLOCKED
Commits: <SHA1>, <SHA2>, <SHA3>
Tests: <count passing / total>
Open issues: <list with severity>
Next: <what's next, or NONE if subphase is done>
```

This lets a resuming agent pick up without re-reading the full code diff.

### Deviation handling

If the plan says "use library X" and during implementation you discover X doesn't fit (wrong version, missing feature, license conflict):

1. **STOP implementing.** Don't silently substitute.
2. Update the plan's Context section with: `Deviation: {what you found, proposed alternative}`
3. If deviation is low-risk (same API shape, same license), proceed with the alternative and note it in the checkpoint.
4. If deviation is high-risk (different abstraction, cross-cutting), escalate to user BEFORE implementing.

Never just "patch around" a deviation without documenting it.

## Gear 3-fail — Debugger (GSD addition)

When a test fails mid-gear-3, invoke:

```
Agent(
  name: "debug-{task}",
  subagent_type: "gsd-debugger",
  prompt: `
A test is failing. Follow the structured debug loop:

<failing_test>
{test name, command to run, last output}
</failing_test>

<recent_diff>
{git diff HEAD~1..HEAD}
</recent_diff>

<related_code>
{codebase-map entries for the affected area}
</related_code>

Steps:
1. **Reproduce** — run the failing test, capture exact output. Confirm it fails consistently (not flaky).
2. **Isolate** — narrow the failure to a specific line or assertion. Use bisection if multi-change.
3. **Hypothesize** — propose the mechanism of failure (not just "the test fails" — WHY).
4. **Fix** — minimal change to address the root cause. Not the symptom.
5. **Verify** — re-run the test + adjacent tests. Confirm fix doesn't break anything else.

Return:
- Root cause (one sentence)
- Fix (diff or description)
- Verification evidence (test output after fix)
- If can't fix in 3 iterations → ESCALATE with what you tried and why it didn't work.
`
)
```

Do NOT suppress the test (skip, xfail) without user approval. A skipped test is a hidden regression.

## Gear 4 — Verifier (GSD addition)

After code review, invoke goal-backward verification:

```
Agent(
  name: "verify-{phase}",
  subagent_type: "gsd-verifier",
  prompt: `
Verify this phase delivered what the plan promised.

<plan_md>
{path to plan.md}
</plan_md>

<implementation_commits>
{git log from start of phase to HEAD}
</implementation_commits>

<test_results>
{full test run output}
</test_results>

For every requirement in the plan:
1. Trace it to the commit(s) that implemented it
2. Trace it to the test(s) that prove it works
3. Flag any requirement not traceable (gap) or not testable (weak requirement)

Return:
- Coverage matrix: requirement → commit → test → status
- Gaps with severity (CRITICAL / HIGH / MEDIUM / LOW)
- Overall verdict: COMPLETE | PARTIAL | FAIL
- If PARTIAL or FAIL: what's needed to reach COMPLETE
`
)
```

A PASS here means: the phase met its stated goal, every requirement is traceable, every test passes.

## Skip criteria

GSD layer MAY be skipped when ALL of these hold:
- Phase scope is trivial (< 50 LOC, single concern)
- Well-covered area (existing tests, familiar code)
- No production impact (local utility, internal doc)

Do NOT skip for: auth, payments, data migration, first phase of a new project, or anything that touches production schemas.

## Related

- `procedure.md` — base deep-build gears
- `implementation-lanes.md` — parallel lane patterns for multi-subphase builds
- `qa-protocol.md` — the 4-layer QA in Gear 5 (GSD debugger integrates here)
- `agent-prompts.md` — base primary-model/OpenAI-family prompts (augment with codebase-map + research-brief when available)
- `~/.claude/get-shit-done/references/` — authoritative GSD references
- `phase-plan` — upstream plan skill (feeds the plan.md to deep-build)
- `deep-sweep` — research/analysis upstream (feeds research-brief.md)
- `verify` — post-execution audit+cleanup (downstream)
