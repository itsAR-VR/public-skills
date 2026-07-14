# 01 — Verify Procedure

Expanded procedure for the three verification layers. This doc is loaded when SKILL.md says "see `references/01_PROCEDURE.md`".

## Phase 0 — Preflight (detailed)

### Establish the verification target

```bash
# What phase are we verifying?
ls -dt docs/planning/phase-* 2>/dev/null | head -3

# What commits are in scope?
git log --oneline $(git merge-base HEAD main)..HEAD

# What's the workspace state?
git status --porcelain
```

If workspace is dirty: commit or stash before verify. Uncommitted changes pollute the audit.

### Sanity check

- Plan.md exists: `test -f docs/planning/phase-{N}/plan.md`
- Commits reference the phase: grep commit messages for `phase-{N}` marker
- Test suite runs: `npm test` (or language-specific) passes or has documented failing tests

## Phase 1 — Goal-Backward Verification (detailed)

### Parallel dual-reviewer pattern

Launch both reviewers at the same time (single message, two Agent calls):

**Reviewer A: phase-review skill**

Apply the phase-review skill flow (see `~/.claude/skills/phase-review/references/04_PROCEDURE.md`):
- Re-read plan.md
- Extract Success Criteria
- Map each criterion to evidence
- Run lint/build/test gates
- Write post-implementation review to `docs/planning/phase-{N}/review.md`

**Reviewer B: gsd-verifier agent**

```
Agent(
  subagent_type: "gsd-verifier",
  description: "Goal-backward phase verification",
  prompt: <see 02_TEMPLATES.md §goal-backward>
)
```

### Convergence check

Both reviewers return verdicts. Expected outcomes:

| A verdict | B verdict | Action |
|-----------|-----------|--------|
| PASS | PASS | Proceed to Phase 2 |
| PASS | FAIL | Investigate B's gap — may be a goal-backward catch |
| FAIL | PASS | Investigate A's gap — may be a build/test regression |
| FAIL | FAIL | Document both sets of gaps, STOP, escalate to user |
| PARTIAL | PARTIAL | Merge gap lists, continue only if user approves |

### Conditional UI audit

If any commit touches UI files (components, routes, layouts, styles):

```
Agent(
  subagent_type: "gsd-ui-auditor",
  prompt: <see 02_TEMPLATES.md §ui-audit>
)
```

### Conditional security audit

If any commit touches auth, payments, user data, secrets, or crypto:

```
Agent(
  subagent_type: "gsd-security-auditor",
  prompt: <see 02_TEMPLATES.md §security-audit>
)
```

## Phase 2 — Quality Audit (detailed)

Apply the deep-clean skill's 8-track flow, scoped to the phase's diff (not the whole codebase, unless the user explicitly asks).

### Scope the audit

```bash
# Files touched by this phase
git diff --name-only $(git merge-base HEAD main)..HEAD
```

Feed this list to the 8 track tools so they audit only phase changes.

### The 8 tracks (scoped)

1. **Deduplication** — `jscpd --pattern 'src/**' --ignore 'node_modules,dist'`
2. **Shared types** — scan for duplicate `interface|type` definitions in the changed files
3. **Unused code** — `knip`, `ts-prune`, `depcheck` — focus on exports from changed files
4. **Circular deps** — `madge --circular src/` but filter to cycles involving changed files
5. **Typing** — grep for `any` in changed files, review each
6. **Error handling** — grep for empty `catch` blocks, over-broad catches in changed files
7. **Legacy paths** — grep for `@deprecated`, `// TODO: remove`, version-gated fallbacks
8. **AI artifacts** — grep for `// stub`, `// TODO: AI`, `// placeholder`, unused imports

### Apply the decision gate

Deep-clean's rule: findings bucket into Green (auto-apply), Yellow (review first), Red (requires user approval).

- **Green:** unused imports, duplicate type definitions, dead exports with no callers
- **Yellow:** anything that might be dynamically referenced (decorators, string-based registration, framework conventions)
- **Red:** legacy paths, error handling changes, public API shape changes

Only Green bucket applies automatically. Yellow/Red need approval per finding.

## Phase 3 — Documentation Verification (detailed)

```
Agent(
  subagent_type: "gsd-doc-verifier",
  prompt: <see 02_TEMPLATES.md §doc-verify>
)
```

The doc-verifier checks:

- **README freshness** — does it describe the shipped functionality?
- **API docs accuracy** — do signatures in docs match actual code?
- **Inline comment truth** — comments that claim X, code that does Y
- **Plan.md completeness** — are Output sections filled?
- **External docs** — changelog, release notes, migration guides (if shipping externally)

### Inline comment check specifics

Grep for lying comments:

```bash
# Find comments that may have drifted
git diff $(git merge-base HEAD main)..HEAD -- '*.ts' '*.tsx' '*.py' '*.js' \
  | grep -E '^\+.*(//|#)' | head -50
```

Review each added comment: does it match the code it's next to?

## Phase 4 — Synthesis (detailed)

Write `docs/planning/phase-{N}/verify.md` using the template in `02_TEMPLATES.md §synthesis`.

### Verdict rubric

- **COMPLETE** — all Phase 1 criteria met, Phase 2 findings applied or approved-deferred, Phase 3 docs accurate
- **PARTIAL** — some criteria met, gaps documented, known-risk decision to ship anyway
- **FAIL** — criteria not met, or quality/docs have unresolved blockers

### Recommendation to user

Based on verdict:

- COMPLETE → "ready to merge / deploy"
- PARTIAL → "ship with caveats — here's the risk register" (requires explicit user confirmation)
- FAIL → "do not ship — here's what needs to happen first"

## Hard skips

You MAY skip a phase only with explicit reason:

- Phase 1 skip reason: "no plan.md exists — verification target undefined" (then you're not really verifying — stop and ask user)
- Phase 2 skip reason: "single-line fix, no quality surface to audit"
- Phase 3 skip reason: "no user-facing or external docs in this phase"

Skip reasons go into `verify.md` for audit trail.

## Related

- `02_TEMPLATES.md` — all agent prompts
- `03_EDGE_CASES.md` — partial completeness, out-of-scope findings, dirty workspace
- `~/.claude/skills/phase-review/` — authoritative phase-review flow
- `~/.claude/skills/deep-clean/` — authoritative 8-track flow
