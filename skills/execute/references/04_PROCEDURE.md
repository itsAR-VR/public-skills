# Procedure

## Step 0 — Multi-Agent Pre-Flight Check

Before beginning execution, detect potential conflicts with concurrent work:

1. **Check git status:**
   ```bash
   git status --porcelain
   ```
   Note any uncommitted changes — another agent may be actively working.

2. **Scan last 10 phases for overlaps:**
   ```bash
   ls -dt docs/planning/phase-* | head -10
   ```
   For each, check if their plan.md mentions files you'll modify.

3. **Check for active work signals:**
   - Partially completed plan.md files (empty Output/Handoff sections)
   - Very recent git commits (within minutes)

4. **If conflicts detected:**
   - Read the conflicting phase's plan.md to understand their work
   - Decide: wait, work around, or coordinate
   - Log the conflict in your current subphase's plan.md

## Step 1 — Determine active subphase

A subphase is considered complete if its `plan.md` includes a non-empty **Output** and a non-empty **Handoff**.

1. Starting from `a`, find the first subphase that is not complete.
2. That is the active subphase.
3. If all are complete, proceed to Phase wrap-up (Step 5).

## Step 2 — Load only what you need

Read:

- Root: `docs/planning/phase-<N>/plan.md`
- Active: `docs/planning/phase-<N>/<letter>/plan.md`
- Any referenced artifacts mentioned in Inputs (only as needed)

## Step 3 — Execute the active subphase

### 3a — Re-verify file state before modifying

Before modifying any file:

1. **Re-read the file** — Do not rely on cached content from earlier in the session
2. **Check git status for that file** — Has it changed since you last read it?
3. **If the file has unexpected content:**
   - Run `git log --oneline -5 -- <filepath>` to see recent commits
   - Check the last 10 phase plans for who modified it and why
   - Merge your changes with their changes semantically
   - Document the merge in your Output section

### 3b — Handle unexpected failures

If you encounter build failures or type errors that seem unrelated to your changes:

1. **Check git status** — Another agent may have introduced breaking changes
2. **Check recent phases** — Find which phase caused the issue
3. **Options:**
   - Fix the issue if it's quick and clearly correct
   - Wait for the other phase to complete
   - Document the blocker and move to independent work

### 3c — Perform the work

In the active subphase `plan.md`:

- Expand **Work** into a concrete sequence of steps that can be performed now.
- Perform the steps.
- Record the results under **Output**.
- Write a clear **Handoff** for the next subphase.

Do not perform steps that belong to later subphases.

### 3d — Document any coordination

If you integrated changes from another phase or encountered conflicts, add a **Coordination Notes** section to your Output:

```markdown
## Coordination Notes

**Integrated from Phase N:** <description of changes you merged>
**Files affected:** <list of files>
**Potential conflicts with:** <other active phases>
```

## Step 4 — Advance to the next subphase

After completing `<letter>`:

- Move to the next letter in the root Subphase Index.
- Repeat Steps 2–4.

If the next subphase folder does not exist but the index includes it:

- Create it and scaffold `plan.md` using the same template structure already present.

## Step 5 — Phase wrap-up

When all subphases in the root Subphase Index are complete:

1. Update `docs/planning/phase-<N>/plan.md`:
   - Check off the root Success Criteria that were met.
   - If any success criteria were not met, add a short note explaining what remains.
2. Append a short **Phase Summary** section at the end of the root plan:
   - What was done
   - Key decisions
   - Links/paths to produced artifacts
   - Any follow-up phase suggestion if needed
