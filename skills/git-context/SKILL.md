---
name: git-context
description: Git-aware code review with live repository context
when_to_use: When reviewing code changes in a git repository, understanding recent commit history, or providing context-aware code review
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Git Context — Code Review with Live Repo State

## Current Repository State

### Recent Commits
!`git log --oneline -10 2>/dev/null || echo 'Not in a git repository'`

### Working Tree Status
!`git status --short 2>/dev/null || echo 'Not in a git repository'`

### Current Branch
!`git branch --show-current 2>/dev/null || echo 'unknown'`

## Instructions

You are performing a git-aware code review. Use the injected repository context above to:

1. **Understand recent changes** — the commit log shows what's been happening in this repo
2. **Check working tree** — the status shows uncommitted changes that may affect your review
3. **Consider the branch** — understand which branch you're reviewing on

### Review Checklist
- Are the changes consistent with recent commit patterns?
- Do uncommitted changes introduce conflicts with staged work?
- Are there any files that should have been committed but weren't?
- Does the code follow the conventions visible in recent commits?

### Output Format
Provide your review as:
1. **Summary** — one-line overview of the change set
2. **Observations** — specific findings per file
3. **Recommendations** — actionable improvements
4. **Risk Assessment** — anything that could break in production
