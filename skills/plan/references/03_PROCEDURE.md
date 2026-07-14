# Procedure

Execute these steps literally, in order.

## Step 0 — Multi-Agent Conflict Check

Before creating any files, check for concurrent work:

1. **List the last 10 phases:**
   ```bash
   ls -dt docs/planning/phase-* | head -10
   ```

2. **For each recent phase**, quickly scan its `plan.md`:
   - Check the Purpose, Agent Team, and Subphase Index
   - Identify any files, contracts, or domains that overlap with your planned work

3. **Check git status:**
   ```bash
   git status --porcelain
   ```
   Note any uncommitted changes that might affect your work.

4. **If overlaps exist:**
   - Add a "Concurrent Phases" section to your plan's Context
   - Specify which phases are working on related areas
   - Note any coordination requirements (e.g., "Must complete after Phase 35")

## Step 1 — Compute the Next Phase Number

1. Inspect the repository and verify `docs/planning/` exists.
   - If it does not exist, create it.
2. List existing phase directories under `docs/planning/`.
3. Identify the highest numbered `phase-N` directory.
4. Set `<N>` to:
   - `max(existing N) + 1`, or
   - `1` if none exist.

Do not guess `N`. Always compute it from the filesystem.

## Step 2 — Pre-Flight Product Framing

Before decomposing work, write these answers in memory:

1. **Who is this for?**
2. **What pain or job-to-be-done does this phase address?**
3. **What is explicitly out of scope?**
4. **What metric, artifact, or user-visible outcome proves success?**
5. **What is the smallest acceptable version of this phase?**

If the user request or repo context makes any of these ambiguous, clarify first.

## Step 3 — Skill Discovery for Feasibility

Before creating any files, discover the skills required to implement the plan:

1. Run `/skill-oracle "<capability needed>"` once per distinct capability.
2. If unavailable, fall back to:
   - `find-local-skills`
   - `find-skills`
3. Document only confirmed implementable skills in the plan.
4. If a desired skill is missing, add it to risks/assumptions with a fallback.

## Step 4 — Run the Planning Research Wave

Before drafting the plan, decide which GSD research agents are needed and
dispatch only the relevant ones in parallel. Typical candidates:

- `gsd-project-researcher`
- `gsd-phase-researcher`
- `gsd-assumptions-analyzer`
- `gsd-advisor-researcher`
- `gsd-ui-researcher`
- `gsd-user-profiler`

Synthesize their outputs into one brief that captures:

- relevant architecture and product constraints
- likely parallel lanes
- hidden assumptions
- prior art worth reusing
- agent role / model tier recommendations
- integration and rollout risks

For heavy research scope, stop and recommend `deep-sweep` instead.

## Step 5 — Build the Dependency Graph in Memory

Break the phase into subphases as a graph, not a sequence.

### Rules for Subphase Design

- Subtasks MUST be derived from the discussion. No filler work.
- Prefer 2-6 subphases. Use more only if clearly justified.
- Prefer 2-5 active parallel lanes. If more are needed, consolidate or route to
  `claude-devfleet` / `deep-sweep`.
- Each subphase must be independently verifiable and have one dominant risk.
- Each subphase must name:
  - role / owner
  - model tier
  - dependencies
  - file or contract surface
  - verification plan
  - recovery path
- If 2 or more subphases produce outputs that must be merged, add a dedicated
  synthesis / integration subphase.
- Use subphase letters as stable IDs only. Alphabetical order does **not**
  imply execution order.

If no safe parallelism exists, the plan may remain serial, but the root plan
must state why.

## Step 6 — Draft the Root Plan in Memory

Draft `docs/planning/phase-<N>/plan.md` using the template from
`04_TEMPLATES.md`.

The root plan must include:

- the original user request
- product frame and anti-goal
- distilled planning principles
- agent team / lane assignments
- evaluation strategy
- safety / rollback considerations
- subphase dependency graph
- recommended next execution skill

## Step 7 — Draft Subphase Plans in Memory

For each listed subphase letter, draft:

- `docs/planning/phase-<N>/<letter>/plan.md`

Populate each subphase plan using the subphase template from `04_TEMPLATES.md`.

Each subphase plan must be self-contained enough that a fresh agent can pick it
up cold.

## Step 8 — Run the Plan-Checker Gate

Before writing files, pass the in-memory root plan through `gsd-plan-checker`.

Revision loop:

1. PASS → continue
2. FAIL → revise and re-run (max 3 total attempts)
3. ESCALATE → surface unresolved issues to the user before writing

## Step 9 — Write Files to Disk

Create:

- `docs/planning/phase-<N>/`
- `docs/planning/phase-<N>/plan.md`
- `docs/planning/phase-<N>/<letter>/`
- `docs/planning/phase-<N>/<letter>/plan.md`

Write the approved in-memory drafts to disk.

## Step 10 — Run the Integration Gate

After the plan is on disk:

1. Invoke `gsd-integration-checker`
2. Revise the written plan if it fails
3. Re-run once
4. Surface persistent conflicts to the user

If the project now has 3 or more phases, optionally run `gsd-roadmapper`.

## Output checklist

Confirm on disk before finishing:

- `docs/planning/phase-<N>/plan.md` exists and is populated
- Each listed subphase directory exists
- Each subphase has a populated plan.md
- Root plan has a Subphase Index matching the created subphase folders
- Root plan includes dependency and parallel-lane information
- Each subphase includes verification and recovery sections
