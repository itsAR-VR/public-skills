# Edge Cases

## Missing planning directory

If `docs/planning/` does not exist, create it, then proceed.

## Non-standard folders

Ignore anything not matching `phase-<number>`.

## Gaps in numbering

If phase-1 and phase-3 exist (gap at 2), still pick `max + 1` (phase-4).

## Ambiguous subtasks

Derive the smallest reasonable set from the conversation. Prefer fewer, clearer
subphases over many vague ones.

## No safe parallelism

If the work touches one file, one contract, or one tightly coupled invariant,
the plan may remain serial. Record the reason explicitly in the root plan
instead of pretending parallelism exists.

## Too many candidate lanes

If the plan wants more than 5 active lanes:

- collapse related work into broader packets
- add a synthesis lane
- or recommend `deep-sweep` / `claude-devfleet` for execution

## Shared integration hotspot

If multiple subphases will converge on the same schema, API contract, or core
file set, add an explicit integration subphase instead of allowing unbounded
parallel edits.

## User wants no files

If the user asks for planning but explicitly wants no files written, do not run
this skill. Produce an in-chat plan instead.

## Examples

### Existing phases

If `docs/planning/phase-29/` exists, create:

- `docs/planning/phase-30/`
- `docs/planning/phase-30/plan.md`
- `docs/planning/phase-30/a/plan.md`, `b/plan.md`, ...

### No phases yet

If `docs/planning/` exists but contains no `phase-*` directories, create:

- `docs/planning/phase-1/` and scaffolds
