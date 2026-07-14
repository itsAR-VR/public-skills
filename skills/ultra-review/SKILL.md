---
name: ultra-review
description: >
  Meta-review orchestrator for comprehensive local reviews. Routes through
  relevant review skills (code-review, ecc-security-review, database-design,
  ecc-database-migrations, framework security skills, AutoReview plan review, etc.),
  dispatches specialized reviewer agents in parallel, and consolidates
  everything into one actionable report. Use when the user says "review this",
  "ultrareview", "code audit", "check this PR", or wants a deep review without
  cloud services.
related_skills:
  - phase-plan
  - skill-oracle
  - think
  - deep-sweep
  - deep-build
  - goal-post
  - deep-clean
  - browser-harness
  - code-review
  - audit
  - ecc-security-review
  - ecc-security-scan
  - database-design
  - database-schema-designer
  - ecc-database-migrations
  - gitnexus-pr-review
  - autoreview
  - phase-review
  - critique
metadata:
  author: local
  version: 1.1.0
---

# Ultra Review

Run a comprehensive local review of the current branch, PR, or file set. Ultra
Review is the orchestrator: it determines scope, activates the right review
skills, dispatches specialized reviewer agents in parallel, and consolidates all
findings into one actionable report with severity classifications.

When `ultra-review` is part of a phase workflow, read
`skills/phase-plan/references/09_PHASE_PIPELINE_PLAYBOOK.md`. The playbook owns
the shared beginner path, evidence-packet language, and readiness sequence. This
file stays focused on review orchestration, severity classification, and optional
fix handling.

Ultra Review should keep working on its core duties while other skills and
agents run:

- **Core duties**: scope, evidence collection, risk model, deduplication, final
  judgment, report quality, and optional fix pass.
- **Skill lanes**: domain checklists and review heuristics loaded from related
  skills such as `code-review`, `ecc-security-review`, `database-design`, and
  framework-specific security skills. For plan or planning-artifact review,
  include `autoreview`, which delegates to the local review chain.
- **Agent lanes**: parallel specialist reviewers such as `reviewer`,
  `security-reviewer`, `database-reviewer`, `typescript-reviewer`, and
  language/framework reviewers.

## When to Use

- User says "review this", "ultrareview", "code audit", "check this PR"
- Before merging a significant feature
- After completing a major implementation phase
- When cloud review services are unavailable or unwanted

## Workflow

### Step 1: Determine Scope

| Scope | How |
|-------|-----|
| Current branch vs main | `git diff main...HEAD --stat` |
| Specific PR | `gh pr diff <number>` |
| Specific files | User provides paths |
| Last N commits | `git diff HEAD~N` |

Collect the changed file list and line-numbered context before dispatching any
lanes. For PRs, prefer live PR state over stale local assumptions:

```bash
gh pr view <number> --json files,headRefName,headRefOid,mergeStateStatus,statusCheckRollup
gh pr diff <number>
```

### Step 2: Detect Project Type and Risk Areas

Run these in parallel to detect languages and frameworks:

```bash
# Detect primary language
ls *.ts *.tsx package.json 2>/dev/null | head -5
ls *.py requirements.txt pyproject.toml 2>/dev/null | head -5
ls *.rs Cargo.toml 2>/dev/null | head -5
ls *.go go.mod 2>/dev/null | head -5
```

Also scan the changed file list for risk triggers:

| Trigger | Examples |
|---------|----------|
| Security-sensitive | auth, sessions, permissions, secrets, webhooks, uploads, payments, crypto |
| Database-heavy | migrations, schema files, SQL, Prisma, Supabase, RLS, indexes, query builders |
| Frontend-heavy | React/Vue/Svelte UI, forms, accessibility, client state, routing |
| Backend/API | route handlers, controllers, services, queues, background jobs, integrations |
| Runtime-specific | Python, Rust, Go, Java, C++, Kotlin, Flutter/Dart |
| Regulated data | healthcare, PHI, PII, audit logs, clinical decision support |
| E2E-sensitive | navigation, auth flows, checkout, onboarding, browser-only behavior |

### Step 3: Activate Review Skills

Ultra Review is a meta skill. Before dispatching agents, activate a small set of
high-signal related skills and use their checklists as review lenses.

#### Skill Oracle Routing

When `skill-oracle` is available, run it as preflight routing with a task string
that includes the review scope, changed file summary, detected stack, and risk
areas:

```bash
python3 scripts/query-skill-graph.py "<review scope + stack + risk areas>" --top 8 --json
```

Select skills using these rules:

1. Always include `code-review`.
2. Always include one security lane: prefer `ecc-security-review`; add
   `ecc-security-review` or `ecc-security-scan` when auth, secrets, user input,
   uploads, payments, APIs, or sensitive data changed.
3. Add database lanes only when database code changed: `database-design`,
   `database-schema-designer`, `ecc-database-migrations`, or project-specific
   database skills.
4. Add framework/domain lanes when directly relevant: `ecc-django-security`,
   `ecc-laravel-security`, `ecc-springboot-security`, `ecc-perl-security`,
   `ecc-healthcare-phi-compliance`, `ecc-healthcare-cdss-patterns`, `gitnexus-pr-review`,
   `phase-review`, or `critique`.
5. Add `autoreview` when the scope includes a plan, spec, roadmap, planning
   packet, or the user explicitly asks for AutoReview or automatic plan review.
   `autoreview` routes to the local review chain; do not activate it for a pure code
   diff unless the plan-review lane is requested or a planning artifact is in
   scope.
6. Cap active skill lanes at 5 unless the user explicitly asks for a broad audit.
   Prefer diversity across code quality, security, database, runtime, and domain.

If no graph result is available, use the static related skill list in this file
and the risk trigger table above.

#### Skill Lane Output Contract

For every activated skill, extract only actionable review criteria and return:

- Skill name
- Files or subsystems it applies to
- Findings with file path, line number, severity, why it matters, and suggested fix
- Explicit "no issue found" note when the lane was relevant but clean

Do not paste long checklist text into the final report. Convert skill guidance
into concrete findings against the diff.

### Step 4: Dispatch Reviewer Agents (Parallel)

Always dispatch these reviewers:

1. **reviewer** — General code quality, logic bugs, maintainability, regressions
2. **security-reviewer** — XSS, CSRF, SQL injection, auth, secrets, OWASP Top 10

Conditionally dispatch based on project type:

| Project Type | Additional Reviewers |
|--------------|---------------------|
| TypeScript / React | typescript-reviewer |
| Python | python-reviewer |
| Rust | rust-reviewer |
| Go | go-reviewer |
| Java / Spring Boot | java-reviewer |
| C++ | cpp-reviewer |
| Kotlin / Android / KMP | kotlin-reviewer |
| Flutter / Dart | flutter-reviewer |
| Database-heavy | database-reviewer |
| Healthcare / Medical | healthcare-reviewer |
| Performance-sensitive | performance-optimizer |
| Browser flow / E2E-sensitive | e2e-runner |

Each reviewer agent receives:
- The list of changed files
- The project type
- Activated skill lanes and their focus areas
- Instructions to focus on their domain
- Request to report findings with file paths, line numbers, and severity (CRITICAL/HIGH/MEDIUM/LOW)

Ultra Review should run its own pass while agents work. Inspect the riskiest
files directly, verify suspicious claims, and check that every reported issue is
grounded in the current diff.

### Step 5: Consolidate Findings

Wait for all reviewers to complete. Then produce a unified report:

```markdown
# Ultra Review Report

## Summary
- **Files reviewed**: N
- **Skill lanes activated**: code-review, ecc-security-review, ...
- **Agent lanes dispatched**: reviewer, security-reviewer, ...
- **Total findings**: N (Critical: N, High: N, Medium: N, Low: N)
- **Blockers**: N (must fix before merge)

## Critical (Block Merge)
1. **[File:Line]** Issue
   - **Found by**: [reviewer agent]
   - **Why**: [explanation]
   - **Fix**: [suggested fix]

## High (Should Fix)
...

## Medium (Consider)
...

## Low (Nits)
...

## Positive Findings
- [What each reviewer praised]
```

### Deduplication Rules

- If multiple skills or reviewers flag the same issue, list it once with all sources
- If reviewers disagree on severity, use the HIGHER severity
- Group related issues (e.g., "missing keys in lists" across multiple files)
- Drop ungrounded findings that cannot be tied to current code, a diff hunk, or live PR state
- Prefer the specialist source when wording the fix, but keep the final judgment in Ultra Review

### Step 6: Optional Fix Pass

If user says "fix them" or "address the feedback":

1. Create tasks for each CRITICAL and HIGH finding
2. Assign fixes by domain:
   - Security/auth/data exposure -> security lane
   - Schema/query/migration/RLS -> database lane
   - Runtime/type issues -> matching language lane
   - Cross-cutting regression -> Ultra Review owner
3. Apply fixes directly or dispatch fix agents with disjoint file scopes
4. Re-run the relevant skill lanes and reviewer agents after fixes
5. Re-check live PR state and status checks before claiming the review is clean

## Severity Mapping

| Source Severity | Ultra Review Severity |
|-----------------|----------------------|
| CRITICAL / P0 / Block | CRITICAL |
| HIGH / P1 | HIGH |
| MEDIUM / P2 | MEDIUM |
| LOW / P3 / Nit | LOW |

## Skill and Agent Prompt Templates

### meta-routing prompt template

```
Review scope:
[SCOPE]

Changed files:
[FILE_LIST]

Detected stack:
[PROJECT_TYPE]

Risk triggers:
[RISK_AREAS]

Find the highest-impact review skills for this scope. Prefer code quality,
security, database, runtime-specific, and domain-specific diversity. Return the
skill names, why each applies, and which files each should inspect.
```

### reviewer prompt template

```
Review the following files on branch [BRANCH]:
[FILE_LIST]

Activated skill lanes:
[SKILL_LANES]

Focus on:
- Code quality and readability
- React patterns and hooks usage (if applicable)
- State management correctness
- Component composition
- Logic bugs and edge cases
- Performance concerns
- Accessibility issues
- DRY violations and duplication

Report findings with:
- File path and line number
- Severity: CRITICAL, HIGH, MEDIUM, or LOW
- Description and suggested fix
```

### security-reviewer prompt template

```
Review the following files on branch [BRANCH]:
[FILE_LIST]

Activated skill lanes:
[SKILL_LANES]

Focus on:
- XSS vulnerabilities (unescaped user input in JSX/HTML)
- CSRF protection on mutating requests
- SQL injection (string concatenation in queries)
- Hardcoded secrets/credentials
- Auth bypasses or missing checks
- Path traversal
- Unsafe URL construction
- Sensitive data exposure in client components

Report findings with:
- File path and line number
- Severity: CRITICAL, HIGH, MEDIUM, or LOW
- Description, impact, and suggested fix
```

### database-reviewer prompt template

```
Review the following database-related files on branch [BRANCH]:
[FILE_LIST]

Activated skill lanes:
[SKILL_LANES]

Focus on:
- Unsafe migrations, locks, and rollback risk
- RLS and tenant isolation gaps
- Missing indexes or query-plan regressions
- N+1 queries and inefficient joins
- Data loss, backfill, and zero-downtime deployment risks
- ORM/schema drift and generated-client assumptions

Report findings with:
- File path and line number
- Severity: CRITICAL, HIGH, MEDIUM, or LOW
- Description, data impact, and suggested fix
```

### typescript-reviewer prompt template

```
Review the following TypeScript files on branch [BRANCH]:
[FILE_LIST]

Activated skill lanes:
[SKILL_LANES]

Focus on:
- Type safety (avoid any, proper unknown narrowing)
- Unsafe 'as' casts without runtime validation
- Missing types on exported functions
- React prop typing
- Null/undefined handling
- Interface vs type alias usage
- Generic usage

Report findings with:
- File path and line number
- Severity: CRITICAL, HIGH, MEDIUM, or LOW
- Description and suggested fix
```

## Output Rules

- Lead with the count of blockers (CRITICAL findings)
- Include activated skill lanes and dispatched agent lanes in the summary
- If 3+ CRITICALs, omit LOW findings to reduce noise
- Always include "Positive Findings" section
- Never make up issues — only report what reviewers found
- If a skill or reviewer finds nothing, note "[Source] found no issues"
- Separate "verified current" findings from stale or fixed findings when reviewing a live PR
