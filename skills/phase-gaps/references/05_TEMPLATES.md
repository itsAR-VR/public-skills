# Templates (RED TEAM)

Use these templates when refining plans. Prefer patching existing sections over wholesale rewrites.

## Root plan section: Repo Reality Check

```md
## Repo Reality Check (RED TEAM)

- What exists today:
  - <bullet list of current files/flows relevant to this phase>
- What the plan assumes:
  - <bullets>
- Skills discovered via `find-local-skills`:
  - <list local skills confirmed available for this phase>
- Skills discovered via `find-skills`:
  - <list global skills confirmed available for this phase>
- Verified touch points:
  - <list of key files + identifiers you confirmed exist>
```

## Root plan section: Skill Feasibility

```md
## Skill Feasibility (RED TEAM)

- Critical skill check:
  - <required skill> → <available/missing>
- Missing but required:
  - <skill> → <fallback plan>
```

## Root plan section: RED TEAM Findings

```md
## RED TEAM Findings (Gaps / Weak Spots)

### Highest-risk failure modes
- <failure mode> → <mitigation>

### Missing or ambiguous requirements
- <gap> → <plan fix>

### Repo mismatches (fix the plan)
- <wrong file/path/assumption> → <correct reference>

### Performance / timeouts
- <risk> → <budget/timeout/fallback step>

### Security / permissions
- <risk> → <explicit guard step>

### Testing / validation
- <missing check> → <specific command or verification>
```

## Root plan section: Open Questions (Need Human Input)

```md
## Open Questions (Need Human Input)

- [ ] <question> (confidence <84.7%)
  - Why it matters: <what changes if answered differently>
  - Current assumption in this plan: <what you assumed so the plan is executable>
```

## Root plan section: Assumptions (optional)

```md
## Assumptions (Agent)

- <assumption> (confidence >=84.7%)
  - Mitigation question/check (optional): <how to verify or what to change if wrong>
```

## Subphase plan patch: add validation steps

```md
## Validation (RED TEAM)

- <command or manual check>
- <expected outcome>
```

## Subphase plan patch: skills availability

```md
## Skills Available for This Subphase
- `find-local-skills`: <result summary relevant to this subphase>
- `find-skills`: <result summary relevant to this subphase>
- Planned invocations: <only include confirmed available skills>
```

## Subphase plan patch: assumptions / open questions (optional)

```md
## Assumptions / Open Questions (RED TEAM)

- <assumption or question>
  - Why it matters: <impact>
  - Current default: <assumption in plan>
```

## Subphase scaffold template (append-only)

```md
# Phase <N><letter> — <Subtask Name>

## Focus
(What this subphase does and why)

## Inputs
(Explicit inputs: file paths, previous subphase outputs)

## Work
(Concrete steps; include "RED TEAM" validations)

## Output
(What is produced/changed)

## Handoff
(Instruction to the next letter)
```
