---
name: code-review
description: >
  Automated code review for pull requests using specialized review patterns.
  Analyzes code for quality, security, performance, and best practices. Use when
  the user asks to review code, review a PR, audit code quality, check for security
  issues, or says "review this," "code audit," or "check this PR." For refactoring
  existing code, see code-refactoring. For running coding agents, see coding-agent.
related_skills: [code-refactoring, code-documentation, commit-work, backend-development, backend-coding-agent, frontend-coding-agent]
metadata:
  author: anthropic-community
  version: 1.2.0
source: anthropics/claude-code
license: Apache-2.0
---

# Code Review

## Workflow

### Step 0: Get the Diff

Choose the appropriate input mode:

| Input Mode | How to Get It |
|-----------|---------------|
| GitHub PR | `gh pr diff <number>` — or `gh pr view <number> --json files,additions,deletions` |
| Local git diff | `git diff main...HEAD` or `git diff HEAD~1` |
| Pasted code/snippet | User pastes directly — treat as a single-file review |
| File path | `cat <file>` or `read <file>` — review the whole file |
| Specific function | Extract context around the function; note any callers if visible |

**Large diffs (>500 lines changed):** Break into file-by-file passes. Prioritize: (1) security-sensitive files, (2) core logic changes, (3) tests, (4) config.

**Files to skip automatically:**
- Lock files (`package-lock.json`, `yarn.lock`, `Cargo.lock`, `poetry.lock`)
- Auto-generated files (`*.pb.go`, `schema.graphql` if generated, migration files with only schema)
- Formatting-only changes (whitespace, line length fixes without logic)
- Binary files, assets, fonts

### Step 1: Understand the Change
- Read the PR description or diff summary
- Identify the change category: feature, bugfix, refactor, config, dependency update
- Note the PR size and risk level before applying reviews

### Step 2: Run Category Reviews
Apply in this order, skipping inapplicable categories:

1. **Security** — always run
2. **Code Quality** — always run
3. **Performance** — skip for config-only, docs, or trivial changes
4. **Testing** — skip only if no logic changed (pure docs, types, or config)

### Step 3: Format and Deliver
Use the Review Output Format below. On large PRs with Critical issues, omit the Nits section — don't bury blockers in noise.

---

## Severity Decision Guide

Use this to decide where each finding belongs:

| Severity | When to use |
|----------|-------------|
| 🔴 Critical | Security vulnerability; data loss risk; correctness bug that will break in production; blocks merge |
| 🟡 Suggestion | Best practice violation; missing tests for new logic; maintainability concern; performance issue in a hot path |
| 🟢 Nit | Style preference; naming that could be slightly clearer; minor polish; subjective improvements |
| ✅ What's Good | Patterns worth calling out positively; good test coverage; clean abstractions |

**Rule:** If you have 3+ Criticals, omit Nits entirely. Signal > noise.

---

## Review Categories

### 1. Security Review
Check for:
- SQL injection vulnerabilities
- XSS (Cross-Site Scripting)
- Command injection
- Insecure deserialization
- Hardcoded secrets/credentials
- Improper authentication/authorization
- Insecure direct object references
- Missing rate limiting on auth endpoints
- API keys/tokens in logs or error messages

### 2. Performance Review

*Skip for: config-only changes, pure refactors with no algorithmic change, docs, or trivial single-field changes.*

Check for:
- N+1 queries
- Missing database indexes
- Unnecessary re-renders (React)
- Memory leaks
- Blocking operations in async code
- Missing caching opportunities
- Large bundle sizes (new heavy deps)

### 3. Code Quality Review
Check for:
- Code duplication (DRY violations)
- Functions doing too much (SRP violations)
- Deep nesting / complex conditionals
- Magic numbers/strings
- Poor naming
- Missing error handling
- Incomplete type coverage
- API contract changes / backward compatibility breaks

### 4. Testing Review

*Skip for: pure config, dependency bumps with no API change, or documentation-only PRs.*

Check for:
- Missing test coverage for new code
- Tests that don't test behavior (test implementation, not outcome)
- Flaky test patterns (time-dependent, network calls without mocks)
- Missing edge cases
- Mocked external dependencies without integration test coverage

---

## Review Output Format

```markdown
## Code Review Summary

### 🔴 Critical (Must Fix)
- **[File:Line]** [Issue description]
  - **Why:** [Explanation]
  - **Fix:** [Suggested fix]

### 🟡 Suggestions (Should Consider)
- **[File:Line]** [Issue description]
  - **Why:** [Explanation]
  - **Fix:** [Suggested fix]

### 🟢 Nits (Optional)
- **[File:Line]** [Minor suggestion]

### ✅ What's Good
- [Positive feedback on good patterns]
```

---

## Common Patterns to Flag

### Security — JavaScript/TypeScript
```javascript
// BAD: SQL injection
const query = `SELECT * FROM users WHERE id = ${userId}`;

// GOOD: Parameterized query
const query = 'SELECT * FROM users WHERE id = $1';
await db.query(query, [userId]);
```

### Security — Python
```python
# BAD: SQL injection
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

# GOOD: Parameterized query
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

### Performance — JavaScript
```javascript
// BAD: N+1 query
users.forEach(async user => {
  const posts = await getPosts(user.id);
});

// GOOD: Batch query
const userIds = users.map(u => u.id);
const posts = await getPostsForUsers(userIds);
```

### Error Handling — JavaScript
```javascript
// BAD: Swallowing errors
try {
  await riskyOperation();
} catch (e) {}

// GOOD: Handle or propagate
try {
  await riskyOperation();
} catch (e) {
  logger.error('Operation failed', { error: e });
  throw new AppError('Operation failed', { cause: e });
}
```

### Error Handling — Python
```python
# BAD: Bare except swallowing errors
try:
    risky_operation()
except:
    pass

# GOOD: Specific exception + logging
try:
    risky_operation()
except ValueError as e:
    logger.error("Validation failed: %s", e)
    raise
```

---

## Review Checklist

- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] Error handling complete
- [ ] Types/interfaces defined
- [ ] Tests added for new code
- [ ] No obvious performance issues
- [ ] Code is readable and documented
- [ ] Breaking changes documented
- [ ] API contracts unchanged (or migration path noted)

---

## Examples

### Example: Review a GitHub PR

**User says:** "Review PR #42 on our repo"

**Actions:**
1. `gh pr diff 42` — fetch the diff
2. Check size: if >500 lines, prioritize by risk (security files first)
3. Skip lock files, auto-generated files
4. Apply Security + Code Quality always; Performance + Testing if applicable
5. Format findings by severity, omit Nits if Criticals present
6. Post or report back

### Example: Review pasted code

**User says:** "Review this function [pastes code]"

**Actions:**
1. Treat as single-file review — no need to fetch diff
2. Apply all applicable categories based on what's visible
3. Note any assumptions about context you couldn't see (callers, dependencies)

---

## Troubleshooting

### Review is too noisy (too many nits)
- **Cause:** Reviewing auto-generated code, formatting changes, or lock files
- **Fix:** Skip those files. Focus on logic changes, not formatting.

### Can't determine if a change is safe without runtime context
- **Cause:** Change depends on database state, external service, or config
- **Fix:** Flag as "needs manual verification" with specific concerns noted.

### False positive security warning
- **Cause:** Pattern-matching flagged safe code (e.g., parameterized query looks like injection)
- **Fix:** Read the full context. Note in review: "Verified safe because [reason]."

### PR is too large to review holistically
- **Cause:** 500+ line diff across many files
- **Fix:** Break into file-by-file passes; prioritize security-sensitive and core logic files first; note "reviewed subset, high-risk files" in output.

---

## Related Skills

- **code-refactoring**: Use when review reveals structural issues worth fixing — hand off refactoring work here after review
- **commit-work**: Use when review is clean and change is ready to land — structured commit message generation
- **coding-agent**: Use when the review reveals enough issues that an automated fix pass makes sense (spawn Codex/Claude Code)
- **github**: Use for PR operations — commenting inline, approving, or merging via `gh` CLI
- **backend-development**: Reference for backend patterns when evaluating API design or database changes
