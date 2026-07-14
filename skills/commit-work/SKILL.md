---
name: commit-work
description: >
  Create high-quality git commits: review/stage intended changes, split into
  logical commits, and write clear commit messages (including Conventional Commits).
  Use when the user asks to commit, craft a commit message, stage changes, or
  split work into multiple commits.
related_skills: [code-review, code-refactoring, code-documentation, backend-development, backend-coding-agent, frontend-coding-agent]
metadata:
  author: community
  version: 1.2.0
---

# Commit work

## Goal
Make commits that are easy to review and safe to ship:
- only changes made in **this session** are included
- commits are logically scoped (split when needed)
- commit messages describe what changed and why

## ⚠️ Multi-Agent Safety Rule (CRITICAL)
**Other agents may be working in the same repo simultaneously.**

`git status` shows ALL working-tree changes — including work from parallel agents that is in-progress and not ready to commit. **Never blindly stage everything.**

Before staging anything:
- Know which files YOU touched in this session
- Treat any unfamiliar modified file as another agent's work — **do not stage it**
- When in doubt, ask the user which files are in scope for this commit

Use `git diff <file>` on each candidate file and only stage files you explicitly modified.

## Inputs to ask for (if missing)
- Which files/changes are in scope for this session? (Required if working tree has many changes.)
- Single commit or multiple commits? (Default: multiple small commits for unrelated changes.)
- Commit style: Conventional Commits are required.
- Any rules: max subject length, required scopes.

## Workflow (checklist)
1) Identify session-scoped changes before staging
   - `git status` — note all modified/untracked files
   - `git diff --stat` — get a quick overview
   - Cross-reference against files you actually touched this session
   - Flag any files you did NOT touch to the user before proceeding
2) Decide commit boundaries (split if needed)
   - Split by: feature vs refactor, backend vs frontend, formatting vs logic, tests vs prod code, dependency bumps vs behavior changes.
   - If changes are mixed in one file, use patch staging.
3) Stage only session-scoped changes
   - Stage files explicitly by name: `git add <path> [<path>...]`
   - For mixed-change files, use patch staging: `git add -p <file>`
   - Never use `git add .` or `git add -A` — this risks staging other agents' work
   - To unstage: `git restore --staged -p` or `git restore --staged <path>`
4) Review what will actually be committed
   - `git diff --cached`
   - Sanity checks:
     - no files from outside your session scope
     - no secrets or tokens
     - no accidental debug logging
     - no unrelated formatting churn
5) Describe the staged change in 1-2 sentences (before writing the message)
   - "What changed?" + "Why?"
   - If you cannot describe it cleanly, the commit is probably too big or mixed; go back to step 2.
6) Write the commit message
   - Use Conventional Commits (required):
     - `type(scope): short summary`
     - blank line
     - body (what/why, not implementation diary)
     - footer (BREAKING CHANGE) if needed
   - Prefer an editor for multi-line messages: `git commit -v`
   - Use `references/commit-message-template.md` if helpful.
7) Run the smallest relevant verification
   - Run the repo's fastest meaningful check (unit tests, lint, or build) before moving on.
8) Repeat for the next commit until all session-scoped changes are committed
   - Leave other agents' changes untouched in the working tree

## Deliverable
Provide:
- the final commit message(s)
- a short summary per commit (what/why)
- the list of files staged (confirm these are session-scoped)
- the commands used to stage/review (at minimum: `git diff --cached`, plus any tests run)
