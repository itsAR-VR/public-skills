---
name: dev-workflow
description: End-to-end development workflow for repositories that use phase planning, red-team review, implementation, pull requests, independent review, and deployment proof. Use before nontrivial coding, debugging, refactoring, or release work.
license: MIT
related_skills: [phase-plan, deep-sweep, deep-build, code-review, goal-post]
---

# Development Workflow

Use this workflow when a repository does not provide stricter local instructions. Repository-level `AGENTS.md` or equivalent instructions always win.

## Rules

- Treat the default branch as read-only. Ship through a task branch and pull request.
- Read the files, nearby patterns, tests, and current git state before editing.
- Preserve dirty work. Fetch for freshness and use a clean worktree when the active checkout is unsafe.
- Start nontrivial work with a versioned plan that names the goal, scope, risks, verification, and stop conditions.
- Red-team the plan with `deep-sweep` before implementation.
- Run impact analysis before changing shared symbols. If no code-graph tool exists, search every usage manually.
- Build the smallest complete change with `deep-build`; do not mix unrelated cleanup into the diff.
- Test the failing behavior first for bug fixes, then run focused and regression checks.
- Use an independent reviewer for anything user-facing or release-bound. The producer does not grade its own work.
- Do not merge until required checks, review findings, and deployment or runtime proof are complete.
- Never print, commit, or publish credentials, private customer data, raw sessions, or local authentication state.

## Pipeline

1. Refresh read-only context: branch, status, remotes, default branch, open pull requests, and issue state.
2. Write the plan and success criteria.
3. Run `deep-sweep`; amend the plan for valid findings.
4. Create a task branch from the current default branch.
5. Run impact analysis for each symbol before editing it.
6. Implement with `deep-build` and keep the diff surgical.
7. Run focused tests, type checks, builds, and end-to-end checks proportional to risk.
8. Inspect the final diff and run a secret/private-data scan.
9. Open a pull request with source context, validation, risks, and proof.
10. Resolve independent review findings and re-run affected checks.
11. Merge only after gates pass, then verify the real deployed or runtime surface.

## Done Means Proven

A task is complete only when the requested outcome is visible on the surface that matters. A local build does not prove a deployment, a generated file does not prove it renders, and an open pull request does not prove the change shipped.

Record:

- branch and commit
- pull request and check state
- commands run and their results
- runtime, browser, or artifact proof
- remaining human or external gates

If a repository has no formal planning or deployment system, keep the same sequence and use the lightest local equivalent.
