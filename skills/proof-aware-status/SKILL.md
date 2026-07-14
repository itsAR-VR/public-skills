---
name: proof-aware-status
description: >
  Answers status with evidence instead of vibes. Use for "is this done?",
  "actually done", "what shipped?", "can I trust this?", "can I tell the
  client this is ready?", "ready or not?", "in review or done?", "move it to
  done?", failing checks, proof gaps, shipped claims, and closing work across
  builds, PRs, Linear, deployments, or automations. Route through
  business-context-intelligence first for broad multi-item context; use this
  skill when the primary job is judging one outcome against proof.
related_skills:
  - business-context-intelligence
  - context-freshness-gate
  - open-loop-radar
  - ecc-verification-loop
  - ultra-review
---

# Proof Aware Status

Status is not a feeling. Status is the relationship between the requested
outcome, available proof, and remaining open loops.

## Scope Boundary

Own one-item status judgment. Use `open-loop-radar` for broad unresolved-work
inventory and `daily-business-context-sweep` for a full operating picture.

Status classification is read-only by default. Move Linear/GitHub/task state
only when the user asked for it or standing workflow rules explicitly allow it.
Before moving state, cite the proof and confirm no approval, live test,
privacy, or deployment gate remains.

## Fast Path

Identify the claim, find the strongest direct proof, check remaining approvals
or live steps, then assign one status label.

## Escalate Only If Needed

Run deeper checks only when proof is stale, status affects external action, or
the claim depends on PR/CI/deployment/automation state.

## Safe Automatic Actions

- Run local verification commands when safe.
- Inspect PR/CI/deployment/Linear state when available.
- Gather and cite missing proof.
- Recommend state moves, but apply them only when allowed by user request or
  standing workflow rules.
- Stop before deploys, customer/public claims, production changes, money,
  credentials, or ambiguous durable writes.

## Done Gate

Before saying "done", check:

1. Requested outcome and definition of done.
2. Direct proof that the outcome works.
3. Remaining approvals, reviews, deployments, live tests, or follow-ups.
4. Whether current proof could have drifted.

## Status Labels

Use one label:

- Done: proof exists and no next action remains.
- Shipped: user-facing/deployed/merged, but monitoring or follow-up may remain.
- In Review: proof exists, but a human/teammate approval remains.
- Blocked: exact blocker prevents progress.
- Partial: some acceptance criteria pass, but the outcome is incomplete.
- Unverified: implementation or claim exists, but proof is missing.
- Stale: old proof exists, but the current state may have drifted.

## Proof Ladder

Prefer current direct proof:

1. Passing tests, build, lint, typecheck, or proof script.
2. Screenshot, browser run, local app run, or receipt JSON.
3. GitHub PR/CI/deployment status.
4. Linear issue state with proof comment.
5. Repo docs/handoff with recent timestamp.
6. Memory or chat only, labeled as memory-derived.

Use `context-freshness-gate` when proof is older than the thing being claimed
or when PR/CI/deployment/automation state may have changed.

## Checklist

- Outcome and done criteria identified.
- Strongest proof cited.
- Remaining work named.
- Status label chosen from the allowed set.
- Missing proof stated precisely.

## Output

```text
Status: [label]
Checked at: YYYY-MM-DD HH:MM TZ

Plain English:
- ...

Proof:
- ...

Remaining:
- ...

Next action:
- ...
```

## Guardrails

- Do not mark Done when approval, live proof, deployment, merge, or review is
  still pending.
- Do not let stale memory override current repo or PR evidence.
- If proof is missing, say exactly what proof would close it.
- If evidence only supports a recommendation, output "Recommended status move"
  instead of applying it.
