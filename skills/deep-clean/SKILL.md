---
name: deep-clean
description: >
  Run a careful, coordinated code-quality cleanup pass across 8 tracks —
  deduplication, shared types, unused code, circular dependencies, typing,
  error handling, legacy paths, and AI artifacts — with per-track validation
  and a hard pause-and-review gate before implementing any non-trivial
  change. Use when the user says "deep clean", "deep cleanup", "clean up
  the codebase", "do a cleanup pass", "improve code quality", "dedupe code",
  "consolidate duplication", "remove unused code", "run knip", "find
  circular deps", "run madge", "strengthen typing", "remove any usage",
  "remove legacy paths", "remove AI stubs", "low-risk refactor", or
  "careful refactor". Not for new features (see code-refactoring) or
  single PR reviews (see code-review).
metadata:
  author: contributor
  version: 1.0.0
related_skills:
  - phase-plan
  - skill-oracle
  - think
  - deep-sweep
  - deep-build
  - goal-post
  - ultra-review
  - browser-harness
  - terminus-maximus
  - superpowers-test-driven-development
---

# Deep Clean

A disciplined, reversible quality pass for existing codebases. The goal is
to ship a sequence of small, safe patches — not a sweeping rewrite. "Deep"
means *thorough coverage across 8 tracks*, not *aggressive*. If a change
needs architectural discussion, flag it and stop; do not implement.

When `deep-clean` is part of a phase workflow, read
`skills/phase-plan/references/09_PHASE_PIPELINE_PLAYBOOK.md`. The playbook owns
when cleanup is a required patch item versus a follow-up. This file stays
focused on reversible cleanup execution, scope control, and per-track
validation.

## Modes

- **Repo-wide (default)** — `/deep-clean` invoked with no scope arg. Runs
  all 8 tracks across the entire repo. Behavior unchanged from before.
- **Feature-scoped** — `/deep-clean --scope=feature:<feature_id>` runs all
  8 tracks scoped to: (1) files listed under `surfaces:` in the feature's
  slice front-matter at `docs/planning/phase-N/<letter>/plan.md`,
  (2) immediate import neighbors of those files (1-hop via
  `mcp__gitnexus__impact`), and (3) tests that import any of the above.
  Used as a sub-routine inside `/deep-build` Gear 4 (Review) when
  `slice_type: vertical`.

## Skill Composition (vertical mode)

When invoked as `--scope=feature:<feature_id>` (sub-routine of
`/deep-build` Gear 4 in vertical mode), this skill composes with the
broader ecosystem at named gates. Tiered: required core fires
deterministically; recommended optional fires when conditions match.
Repo-wide mode does not use the composition section — it's vertical-mode
specific.

### Required core (MUST invoke)

- `gsd-codebase-mapper` (focus: feature-footprint) @ Step 0.0 scope
  resolution — adds structural context (modules, ownership boundaries,
  community membership) used by Phase 4 architectural review.
- `mcp__gitnexus__impact` @ Step 0.0 (already wired in Round 1) — 1-hop
  import-neighbor expansion of `surfaces[]`.
- ECC `refactor-cleaner` agent @ Phase 4 implementation — canonical
  cleanup execution for Green-bucket patches.

### Recommended optional (SHOULD invoke when conditions match)

- ECC language-specific reviewer @ Phase 1 tracks 5/6 (typing, errors)
  — auto-detected from scope file extensions: `*.ts/*.tsx` → ECC
  `typescript-reviewer`; `*.py` → ECC `python-reviewer`; `*.go` → ECC
  `go-reviewer`; `*.rs` → ECC `rust-reviewer`; `*.kt` → ECC
  `kotlin-reviewer`; `*.java` → ECC `java-reviewer`; `*.cpp/.h` → ECC
  `cpp-reviewer`.
- `gsd-intel-updater` @ Phase 0 baseline — refreshes intel before scope
  resolution when the codebase has drifted since the last sweep.
- `superpowers-test-driven-development` @ Phase 4 implementation —
  fix-with-test-first discipline, fired when the cleanup fix introduces
  new test scaffolding.

### Per-slice tools (fire once per feature_id when invoked)

- `mcp__gitnexus__impact` for surface symbols — scope expansion to 1-hop
  neighbors per surface entry.

### Source of truth (avoid rot)

- ECC agent catalog: `~/.claude/agents/{refactor-cleaner,*-reviewer}.md`
- GSD catalog: `~/.claude/agents/gsd-*`
- Superpowers catalog: `skills/superpowers-*/` (vendored from `anthropics/claude-plugins-official`; no plugin dependency)

## When to Use

Activate when the user asks to:

- "clean up the codebase" / "do a cleanup pass" / "improve code quality"
- "dedupe code" / "consolidate duplication"
- "find unused code" / "run knip" / "remove dead code"
- "detect circular dependencies" / "run madge"
- "strengthen typing" / "remove any usage" / "narrow types"
- "review error handling" / "remove defensive try/catch"
- "remove legacy paths" / "remove deprecated code" / "remove fallbacks"
- "remove AI stubs" / "clean AI-generated comments"
- "deep clean" / "deep cleanup" / "thorough cleanup"
- "low-risk refactor" / "careful refactor" / "conservative cleanup"

Do NOT activate for:

- New feature implementation in **repo-wide** mode. The **feature-scoped**
  mode (`--scope=feature:<feature_id>`) IS appropriate as a sub-routine of
  `/deep-build` Gear 4 in vertical mode — that mode scopes the 8 tracks
  to the feature's footprint and is safe to run on in-progress features.
  For greenfield refactors unrelated to a feature slice, use
  code-refactoring's "make the change easy" instead.
- Fixing a specific bug — use superpowers-systematic-debugging.
- Reviewing a PR or recent diff — use code-review.
- Sweeping architectural change — requires a plan skill, not cleanup.

## Non-Negotiable Rules

1. **No speculative rewrites.** Every change must address a concrete finding.
2. **No public-behavior changes** unless explicitly justified and flagged.
3. **Verify before removing.** Dynamic imports, framework file conventions,
   string-based registration, config-driven loading, decorators, codegen
   output, and test runner discovery can all make code appear dead.
4. **Small, grouped patches.** One concern per commit.
5. **Explain why each change is safe.** If you cannot articulate the reason,
   demote the finding to Yellow and do not implement it.
6. **Pause at the decision gate** (Phase 3) before implementing anything
   outside the Green bucket.
7. **Never touch generated code** (Prisma, protoc, OpenAPI codegen, etc.).
8. **Never edit framework convention files** unless the change is the
   explicit subject of the finding.

## The 8 Tracks

1. **Deduplicate code** where it reduces complexity without obscuring intent.
2. **Consolidate shared type definitions** where duplication causes drift.
3. **Identify unused code** — functions, components, exports, imports,
   and dependencies. Use knip / ts-prune / depcheck (JS/TS), vulture
   (Python), `go mod why` / staticcheck (Go). Verify every finding
   manually against framework conventions and dynamic usage.
4. **Untangle circular or problematic dependencies** with madge (JS/TS)
   or language equivalents. Prioritize cycles that affect maintainability,
   build correctness, or module load order.
5. **Strengthen typing** by replacing unsafe `any` with narrower types.
   Keep `unknown` at system boundaries where it is legitimately correct.
6. **Review error handling** — remove unnecessary or misleading defensive
   patterns (empty catches, catches that rethrow the same error, catches
   that swallow errors silently). Preserve catches that serve a real
   boundary, recovery, logging, cleanup, or user-facing error-handling
   purpose.
7. **Remove legacy paths** — deprecated, dead, fallback, or legacy code
   that is clearly obsolete and not required for compatibility, migration,
   configuration, or active users.
8. **Remove low-value AI artifacts** — placeholder stubs, redundant
   comments, narration that restates code, TODO-style notes with no owner,
   comments that describe edit history instead of intent. Keep comments
   that explain WHY the code exists.

## Per-Track Loop

For each of the 8 tracks, run this five-step loop:

1. **Inspect** — read the relevant code and run the appropriate tooling
   (knip, madge, grep, ts-prune, vulture, etc.). Capture raw findings.
2. **Assess** — write a brief critical assessment separating framework
   false positives and codegen artifacts from real findings.
3. **Propose** — rank recommended changes by confidence and risk, and
   assign each finding to the Green / Yellow / Red bucket.
4. **Implement** — apply only Green (high-confidence, low-regret)
   changes. Yellow and Red findings stop at the decision gate for
   user signoff.
5. **Validate** — run the relevant targeted check (typecheck + lint for
   touched files); run the full validation suite at the end. Report
   results and any assumptions you could not verify.

The phase-based workflow below orchestrates this loop across all tracks:
parallel inspection (Phase 1), shared bucket classification (Phase 2),
a single combined decision gate (Phase 3), coordinated implementation
(Phase 4), and final validation (Phase 5). For small repos or when the
user requests maximal certainty, run Phase 5 validation after each track
instead of only at the end.

## Workflow

### Phase 0 — Baseline (always first)

**Step 0.0 — Scope resolution (run first if `--scope=feature:<feature_id>`
was passed):**

**Step 0.0a — Codebase map (run before file resolution):** Invoke
`gsd-codebase-mapper` with `focus: feature-footprint` and
`paths: <surfaces[] from front-matter>`. The codebase-mapper output adds
structural context (which modules the surfaces belong to, ownership
boundaries, community membership in the codebase graph) that informs
Phase 4's Yellow-bucket evaluation against architectural intent. Cache
the output for use in Phase 4 review.

1. Read `docs/planning/phase-{N}/{letter}/plan.md` front-matter for the
   matching `feature_id`. (The plan path can be inferred from `git log`
   for recent phase work, or the user can pass
   `--phase-plan-path=<path>`.)
2. Expand `surfaces.db`, `surfaces.api`, `surfaces.ui`, `surfaces.tests`
   arrays into a single flat list of file paths.
3. Compute 1-hop impact for each file via `mcp__gitnexus__impact`. Add
   returned import-neighbors to the list.
4. Add any tests that import the surfaces files (search `tests/` for
   matching imports).
5. Deduplicate. Write the resolved list to
   `/tmp/deep-clean-scope-{feature_id}.txt` (one path per line).
6. Phases 1–5 below operate ONLY on this resolved list.

If no `--scope` was passed (repo-wide mode), skip this step and proceed
with the existing Phase 0 behavior below.

Capture a known-good reference before any change. Run in parallel:

- Typecheck: `npm run typecheck` / `tsc --noEmit` / `mypy` / `cargo check`
- Lint: `npm run lint` / `eslint` / `ruff` / `golangci-lint` / `clippy`
- Tests (if fast): `npm test` / `pytest` / `go test ./...` / `cargo test`
- Git state: are there substantial uncommitted changes?

Record exact error/warning counts. Every later check will be compared
against this baseline.

If the repo has substantial uncommitted work, stop and ask the user to
commit or stash before proceeding. Cleanup diffs should not be mixed
with in-progress features.

If a code-graph tool is available (GitNexus, Sourcegraph, LSP), note it.
Use impact analysis before modifying any symbol.

### Phase 1 — Parallel analysis

Run analysis tools in parallel, preferring `npx` to avoid polluting
`package.json`. In feature-scoped mode, restrict each invocation to the
resolved scope file at `/tmp/deep-clean-scope-{feature_id}.txt`.

```bash
# Repo-wide (existing default):
npx --yes knip --reporter=compact

# Feature-scoped:
npx --yes knip --reporter=compact --include "$(cat /tmp/deep-clean-scope-{feature_id}.txt | tr '\n' ',')"
```

```bash
# Repo-wide (existing default):
npx --yes madge --circular --extensions ts,tsx src

# Feature-scoped:
xargs -a /tmp/deep-clean-scope-{feature_id}.txt npx --yes madge --circular --extensions ts,tsx
```

Run these grep queries in parallel (adjust path for language). In
feature-scoped mode, pipe the scope file into the search rather than
walking the whole repo (e.g. `xargs -a /tmp/deep-clean-scope-{feature_id}.txt
rg <pattern>`):

- Weak typing: `(:\s*any\b|\bas\s+any\b|@ts-ignore|@ts-expect-error|@ts-nocheck)`
  — exclude `node_modules`, `**/generated/**`, `**/*.d.ts`.
  - Feature-scoped: `xargs -a /tmp/deep-clean-scope-{feature_id}.txt rg
    '(:\s*any\b|\bas\s+any\b|@ts-ignore|@ts-expect-error|@ts-nocheck)'`
- Legacy markers: `(TODO|FIXME|XXX|HACK|LEGACY|DEPRECATED|@deprecated)`.
  - Feature-scoped: `xargs -a /tmp/deep-clean-scope-{feature_id}.txt rg
    '(TODO|FIXME|XXX|HACK|LEGACY|DEPRECATED|@deprecated)'`
- Catches for classification: `catch\s*\([^)]*\)\s*\{`.
  - Feature-scoped: `xargs -a /tmp/deep-clean-scope-{feature_id}.txt rg
    'catch\s*\([^)]*\)\s*\{'`
- Filename duplicates (macOS Finder artifacts): `**/*[ _-]2.{ts,tsx,js,jsx,py,go}`,
  `**/* copy.*`, `**/*Copy.*`.
  - Feature-scoped: filter the scope file by basename pattern instead of
    globbing the repo (e.g. `grep -E '[ _-]2\.(ts|tsx|js|jsx|py|go)$|
    copy\.|Copy\.' /tmp/deep-clean-scope-{feature_id}.txt`).
- Duplicate string constants: long literal URLs, magic numbers repeated 3+ times.
  - Feature-scoped: same `xargs -a` pattern; restrict the literal
    extraction to the resolved file list.

If a tool does not support file-list scoping natively (e.g. `ts-prune`,
`depcheck`, `vulture`), run repo-wide and post-filter findings to those
whose `file:line` is in the scope file:
`<tool> | rg -F -f /tmp/deep-clean-scope-{feature_id}.txt`.

**Hard rule (scope mode only):** Phase 4 implementation MUST reject any
proposed diff that touches a file not in
`/tmp/deep-clean-scope-{feature_id}.txt`. Scope leakage is a
fail-the-cleanup condition; escalate to the user before applying any
patch that crosses the boundary.

### Phase 2 — Per-track assessment

For each finding, produce a row with:

- **Finding** — what and where (file:line).
- **Evidence** — grep results, dynamic-usage check, framework check.
- **Confidence** — High / Medium / Low.
- **Risk** — Low / Medium / High.
- **Proposed change** — exact diff or deletion plan.

Assign each finding to exactly one bucket:

| Bucket | Meaning | Action |
|--------|---------|--------|
| **Green** | High-confidence, low-risk, self-contained | Implement in Phase 4 |
| **Yellow** | Needs user signoff, cross-track coordination, or a naming choice | Present and wait |
| **Red** | Would change behavior, touch a public API, or has high blast radius | Document and do not touch |

Default to Yellow when in doubt. Green means "I would bet the build on this."

### Phase 3 — Combined decision gate

Before any implementation, stop and present:

1. **Summary per track** — how many findings, bucket distribution.
2. **Cross-track overlaps** — e.g. one file is flagged by both knip and
   lint; a single change resolves both.
3. **Green list** — exactly what will be implemented without further input.
4. **Yellow list** — what requires the user's decision. Include the
   specific question (e.g. "canonical name: A or B?").
5. **Red list** — what will not be touched and why.

Do not proceed past this gate on Yellow or Red items without explicit
user approval.

### Phase 4 — Implement Green bucket

**Implementation composition (scope mode):**

- **Required**: ECC `refactor-cleaner` agent for the canonical cleanup
  execution.
- **Auto-detect language-specific reviewers** (when fix involves typing
  or error handling — tracks 5/6): `*.ts/*.tsx` → ECC
  `typescript-reviewer`; `*.py` → ECC `python-reviewer`; `*.go` → ECC
  `go-reviewer`; `*.rs` → ECC `rust-reviewer`; `*.kt` → ECC
  `kotlin-reviewer`; `*.java` → ECC `java-reviewer`; `*.cpp/.h` → ECC
  `cpp-reviewer`. Reviewers run as second-pass verifiers on the cleanup
  diff.
- **Recommended**: `superpowers-test-driven-development` for
  fix-with-test-first when the fix introduces new test scaffolding.

For each Green change, in this order:

1. If a code-graph tool is available, run impact analysis on every symbol
   touched. If risk comes back HIGH or CRITICAL, demote to Yellow and skip.
2. Apply the smallest possible diff.
3. Run the targeted check (typecheck + lint for the touched files/directory).
4. Commit with a message naming the track and the specific finding. Example:
   `refactor(track-1): remove Outcomes 2.tsx macOS duplicate`.

If a Green change unexpectedly fails validation, revert it and demote
the finding to Yellow with a note about what went wrong.

### Phase 5 — Final validation

Run the full suite matching Phase 0:

- Full typecheck
- Full lint
- Full tests (or the relevant subset if the full suite is slow)
- Full build

Cleanup must leave the codebase no worse than baseline on every metric.

For small repos or when the user requests maximal certainty, run Phase 5
after each track instead of only at the end.

## Verification Checklist Before Removing Anything

Before deleting a symbol, file, or dependency, confirm it is not used via:

- [ ] Static imports (grep across the whole repo, not just `src/`)
- [ ] Dynamic imports / `require()` / `importlib` / reflection
- [ ] Framework file-based conventions (see Framework Magic below)
- [ ] String-based lookups (`templates[name]`, `handlers['x']`,
      `registry.get('y')`)
- [ ] Config or environment-driven registration
- [ ] Hooks / plugins / decorators / dependency-injection containers
- [ ] Code-generation input or output (never edit generated files)
- [ ] Test runner discovery patterns (`*.test.ts`, `*_test.go`,
      `test_*.py`)
- [ ] Public API exports that downstream packages may import
- [ ] Storybook stories, MDX docs, example apps, or fixtures

If any of these is unclear, the finding is Yellow, not Green.

## Framework Magic Reference

Files and patterns that look dead to static analysis but are loaded by the
framework. NEVER treat as "unused" without explicit confirmation:

**Next.js App Router**

- `page.tsx`, `layout.tsx`, `loading.tsx`, `error.tsx`, `not-found.tsx`,
  `global-error.tsx`, `default.tsx`, `template.tsx`
- `route.ts` / `route.js` (API route handlers)
- `middleware.ts`
- `opengraph-image.*`, `twitter-image.*`, `icon.*`, `apple-icon.*`
- `sitemap.ts`, `robots.ts`, `manifest.ts`
- `instrumentation.ts`

**Next.js Pages Router**

- `_app.tsx`, `_document.tsx`, `_error.tsx`, `api/**/*.ts`

**Rails / Spring / Django / Laravel**

- Autoloaded classes based on naming conventions
- URL-routing configs and controller methods referenced by string
- Migrations in a sequenced directory
- Django `urls.py`, `admin.py`, `models.py`, `apps.py`

**Generated / regenerated directories — never edit**

- `src/generated/**`, `**/generated/**`, `.prisma/**`, `*.pb.go`,
  `*_pb2.py`, `*.g.dart`, OpenAPI client output, tRPC / GraphQL codegen.

**Dependency false positives**

- Peer dependencies loaded indirectly (`@prisma/client` via generated
  code, `pg` via `@prisma/adapter-pg`).
- Binaries-as-deps used only through npm scripts (`tsx`, `python3`).
- Build-time-only packages (`postcss`, `autoprefixer`) loaded from
  config files.

## Final Output Template

When the workflow completes, produce exactly this report:

```
## Deep Clean Report

### Scope
Mode: `feature:<feature_id>` (or `repo-wide`).
Files in scope: `<count>` (resolved at `/tmp/deep-clean-scope-<feature_id>.txt`
for feature-scoped mode).

### Baseline (Phase 0)
- typecheck: <pass|N errors>
- lint:      <pass|N errors, M warnings>
- tests:     <pass|fail|skipped>
- build:     <pass|fail|skipped>

### Summary of issues found
<Track 1>: <N findings — X Green / Y Yellow / Z Red>
...
<Track 8>: <...>

### Changes implemented
- <track>: <file>: <what changed> — <why it is safe>
...

### Changes intentionally not implemented (Yellow / Red)
- <track>: <file>: <finding> — <why deferred> — <decision needed from user>
...

### Risks and follow-ups
- <any validation regression, flaky test, borderline call>

### Assumptions requiring human verification
- <e.g. "knip flagged @ai-sdk/anthropic unused; user memory says direct
  OpenAI SDK preferred — user should confirm before uninstalling">

### Final validation (Phase 5)
- typecheck: <compared to baseline>
- lint:      <compared to baseline>
- tests:     <compared to baseline>
- build:     <compared to baseline>
```

## Examples

### Example 1: Full cleanup pass on a Next.js project

**User says:** "Do a deep clean pass on this codebase."

**Actions:**

1. Phase 0: `npm run typecheck` + `npm run lint` in parallel; record
   baseline (e.g. typecheck clean, lint 156 problems).
2. Phase 1: `npx knip`, `npx madge --circular src`, and grep queries
   in parallel.
3. Phase 2: Classify every finding. Example: `Outcomes 2.tsx` (macOS
   duplicate) is Green; `@ai-sdk/anthropic` unused dep is Yellow
   (user memory says direct SDK preferred — ask before uninstalling);
   `route.ts` under `api/webhooks/` flagged by knip is Red (Next.js
   convention file, framework-loaded).
4. Phase 3: Present the combined picture. Stop and wait for Yellow/Red
   approval.
5. Phase 4: Apply Green only. One commit per track.
6. Phase 5: Re-run full typecheck + lint + build; confirm no regression.

**Result:** A short sequence of reversible commits plus a written list
of Yellow/Red items for the user to decide on.

### Example 2: Knip flags a framework file

**User says:** "Remove unused code."

**Actions:**

1. knip reports `src/app/api/webhooks/fireflies/route.ts` as unused.
2. Check: filename is `route.ts` directly under `app/api/**` — Next.js
   App Router convention.
3. Tag Red. Document: "framework-loaded via App Router convention;
   knip cannot trace file-based routing."

**Result:** The file stays. The false positive is recorded in the
final report so it is not re-investigated next time.

### Example 3: Duplicate exports with shared call sites

**User says:** "Consolidate duplication."

**Actions:**

1. knip reports `BUSINESS_CALENDLY_URL` and `PRIMARY_CTA_URL` in
   `src/lib/config.ts` as duplicate exports (one aliases the other).
2. Grep both names across the repo — each has ~6–8 import sites in
   components and pages.
3. Tag Yellow. This is a naming choice, not a safe deletion.
4. Present the question: "These two exports are literally `const
   PRIMARY_CTA_URL = BUSINESS_CALENDLY_URL`. Which name should be
   canonical? Consolidation will require touching ~14 call sites."

**Result:** User picks the canonical name. Only then perform a
graph-aware rename (not find-and-replace) in a dedicated commit.

## Troubleshooting

### knip flags `@prisma/client` or `pg` as unused

- **Cause:** Loaded via generated code or peer-dependency patterns knip
  cannot trace.
- **Fix:** Treat as false positive unless a real grep confirms zero
  transitive imports.

### madge reports cycles only in generated code

- **Cause:** Prisma 7, protoc, and similar generators emit circular
  references intentionally; they regenerate on every build.
- **Fix:** Exclude generated directories from the report. Do not edit
  generated files.

### Typecheck was clean in Phase 0 but fails in Phase 5

- **Cause:** A Green change broke something despite the checklist.
- **Fix:** Bisect Phase 4 commits. Revert the offender. Demote the
  finding to Yellow with a note on what went wrong — future runs
  should not re-attempt it.

### The user has substantial uncommitted work when you start

- **Cause:** In-progress feature work would get mixed with cleanup.
- **Fix:** Stop. Ask the user to commit or stash. Do not try to
  untangle their work for them.

### The test suite is slow or missing

- **Cause:** No fast feedback loop for Phase 4 per-change verification.
- **Fix:** Scope each Green change narrowly enough that typecheck +
  lint are sufficient safety. If a finding needs test coverage to be
  safe, demote it to Yellow.

### A finding appears in multiple tracks

- **Cause:** Cleanup concerns overlap (e.g. an unused import is both
  Track 3 and Track 8).
- **Fix:** Single commit, attribute it to whichever track has the
  strongest primary signal. Note the overlap in the final report.

### Lint errors exist in `tmp/` or scratch directories

- **Cause:** Scratch/probe scripts are in the lint scope but shouldn't be.
- **Fix:** Tag as Yellow. Propose adding the directory to the lint
  ignore list. Do not delete the scripts without asking.

## Related Skills

- **code-refactoring** — refactoring techniques (extract method, early
  return, parameter object) to apply once a cleanup target is chosen.
- **code-review** — for reviewing recently changed code, a specific PR,
  or a diff.
- **ecc-security-review** — run when cleanup touches auth, input handling,
  crypto, or any security-sensitive code.
- **gitnexus-impact-analysis**, **gitnexus-refactoring** — if the
  codebase is GitNexus-indexed, use these for impact analysis and
  graph-aware rename (not find-and-replace).
- **refactor-cleaner** (agent) — dispatch for bulk cleanup of clearly
  dead code after human signoff.
