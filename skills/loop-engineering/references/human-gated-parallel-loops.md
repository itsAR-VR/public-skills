# Human-Gated Parallel Loop Playbook

Use this reference when a user wants to control many agents, design a
multi-step loop, add human approvals, or make agent work observable.

## Table of Contents

- Loop Engineering in Plain English
- The Control Plane
- The 15-Agent Launch Template
- Human Approval Gates
- Evaluation Design
- Observability Schema
- Failure Responses
- Operator Workflow

## Loop Engineering in Plain English

Loop engineering is the shift from "I prompt the agent" to "I design the
system that prompts, checks, remembers, and stops the agent."

Analogy: prompting is hiring one contractor and checking in manually. Loop
engineering is setting up a job board, work orders, inspections, sign-offs,
and a dashboard so many contractors can work without losing control.

Practically, the operator must decide:

- What outcome is the loop chasing?
- What evidence proves it worked?
- What can the loop do without permission?
- What must pause for human approval?
- What happens when the same failure repeats?
- What state survives across runs?

## The Control Plane

Every serious loop needs a control plane: the files, rules, and gates that sit
above the workers.

Minimum files:

```text
LOOP.md            # goal, boundaries, stop rules, approval rules
STATE.json         # current run state and lane scoreboard
handoffs/          # one structured worker result per lane
verdicts/          # verifier outputs, one gate decision at a time
approvals/         # human approval records
artifacts/         # previews, diffs, reports, screenshots, PR links
learnings/         # only verified reusable lessons
```

`STATE.json` should be append-friendly or backed by a ledger. Do not let each
worker rewrite global state directly; workers write handoffs, and the parent
updates the scoreboard.

## The 15-Agent Launch Template

Use this when Mo wants to "prompt 15 parallel agents."

Parent prompt shape:

```text
Outcome:
Definition of done:
Global constraints:
Forbidden actions:
Human gates:
Verification surface:
Stop rules:
Lane table:
  - lane_id:
    role:
    scoped_goal:
    allowed_paths_or_sources:
    editing_allowed:
    handoff_path:
    acceptance_criteria:
    max_turns_or_budget:
Integrator:
Verifier:
```

Worker prompt shape:

```text
You own only lane_id: <id>.
Goal: <scoped_goal>
Allowed paths/sources: <paths>
Forbidden actions: <actions>
Editing allowed: yes/no
Do not coordinate with other workers.
Write no durable memory.
Return only this JSON-compatible handoff:
{
  "lane_id": "<id>",
  "status": "done|blocked|failed",
  "summary": "...",
  "evidence": ["..."],
  "changed_files": ["..."],
  "risks": ["..."],
  "questions_for_human": ["..."],
  "next_action": "..."
}
```

Recommended batching:

| Task type | Batch size | Why |
|---|---:|---|
| Read-only scouting | 10-15 | Low collision risk |
| Code edits in separate modules | 3-5 | Integration risk grows quickly |
| Same file or same UX surface | 1-2 | Avoid merge and design conflicts |
| External/live systems | 1 | Human gate and proof matter more than speed |

If 15 workers all need the same files, the work is not actually parallel. Run
one scout, one planner, one builder, one verifier.

## Human Approval Gates

Approval gate states:

| State | Meaning | Next action |
|---|---|---|
| `drafted` | Agent prepared a plan/artifact/action | verifier checks evidence |
| `verified` | Independent check passed | package for human |
| `needs_human` | Risky next action needs approval | ask exact approval question |
| `approved` | Human approved a named action and scope | execute only that action |
| `rejected` | Human said no or scope changed | revise or stop |
| `expired` | Approval is too old for current state | ask again |

Approval record:

```json
{
  "approval_id": "appr_...",
  "run_id": "run_...",
  "approved_by": "human",
  "approved_at": "2026-06-13T00:00:00-04:00",
  "approved_action": "merge PR #123",
  "scope": ["repo/path"],
  "evidence_reviewed": ["verdicts/v3.json", "artifacts/pr-123.md"],
  "expires_when": "diff changes or 24h passes"
}
```

Never use broad approvals like "do whatever is needed." Ask for the exact
action: "Approve sending this draft to X?" or "Approve merging PR #123 after
CI passes?"

## Evaluation Design

Eval ladder:

1. Deterministic checks first: tests, typecheck, lint, schema validation,
   screenshot existence, URL status, diff scope.
2. Rubric checks second: fresh-context verifier grades subjective quality with
   binary criteria and cited evidence.
3. Human check third: only for judgment, taste, business risk, production,
   publishing, money, or relationship impact.

Rubric criteria must be binary and evidence-backed:

```json
{
  "id": "human_gate_present",
  "question": "Does every production-touching action pause for explicit approval?",
  "pass_condition": "The loop defines a needs_human state before deploy/merge/send and records approval scope.",
  "required_evidence": "File path and exact gate name"
}
```

Loop-quality evals:

- Can the loop say no?
- Can it stop without shame when blocked?
- Does it track repeated failures?
- Does it prevent self-grading?
- Does it preserve human approval before irreversible actions?
- Can the operator inspect state without reading every transcript?

## Observability Schema

Use one scoreboard row per lane:

```json
{
  "run_id": "run_...",
  "lane_id": "lane_07",
  "phase": "scout|build|verify|approve|publish|learn",
  "status": "pending|running|done|blocked|failed|needs_human|verified",
  "owner": "worker|integrator|verifier|human",
  "scoped_goal": "...",
  "last_update_at": "...",
  "artifact_paths": [],
  "handoff_path": "handoffs/lane_07.json",
  "verdict_path": "verdicts/lane_07.json",
  "changed_files": [],
  "failure_fingerprint": null,
  "cost_or_turns": {"turns": 0, "tokens_estimate": null},
  "human_gate": {"state": "not_required|needs_human|approved|rejected|expired"},
  "next_action": "..."
}
```

Status readout for Mo should be plain:

```text
15 agents launched.
9 done, 3 running, 2 blocked, 1 needs your approval.
No external action has been taken.
The next decision is whether to approve <exact action>.
```

## Failure Responses

| Failure | Detection | Response |
|---|---|---|
| Same blocker repeats | same fingerprint 3 times | stop and escalate |
| Worker edits outside scope | diff-scope check fails | reject handoff; revert or isolate |
| Verifier cannot inspect evidence | missing artifact or command failure | fail verification, ask integrator to package proof |
| Too many agents collide | merge conflicts, duplicate files | reduce to one integrator and read-only reviewers |
| Cost grows without progress | cap hit with no new evidence | freeze loop, shrink scope |
| Human approval ambiguous | approval lacks action/scope | treat as missing approval |
| Agent self-grades | maker verdict used as gate | reject; launch fresh verifier |

## Operator Workflow

To become someone who can run 15 agents:

1. Start with read-only scout swarms. Learn to write lane prompts and compare
   handoffs without merge risk.
2. Add one integrator. Scouts gather evidence; the integrator creates the
   decision-ready artifact.
3. Add one verifier. The verifier checks the integrator output against a
   rubric and named evidence.
4. Add human gates. Practice approving only exact actions.
5. Only then allow editing workers, and keep them in separate files/modules.
6. Build a scoreboard habit: every run ends with status, evidence, blockers,
   and next decision.

The operating standard: many agents can work at once, but only one gate decides
what is true and only the human approves risky action.
