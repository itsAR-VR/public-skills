---
name: loop-engineering
description: "Use when designing agent loops: writing /goal objectives, autonomous iteration, human-gated approval checkpoints, multi-step loops, parallel agent swarms, 10-20 worker fan-out, loop stop conditions, verifier subagent design, rubric design, evaluations, observability, dashboards/ledgers, any 'loop until' request, scheduled agent runs, Ralph-style while-true loops, or reviewing/hardening a loop that prompts agents — choosing verification surfaces, exit conditions, evaluator tiers, launch surfaces (Claude /goal, /loop, hooks, headless; Codex goal mode, automations, codex exec), and safe orchestration. Not the OODA decision framework (ooda-loop), not business open-work inventory (open-loop-radar)."
---

# Loop Engineering

A loop is a goal stated as a machine-checkable condition, an actor, an
independent verifier, an explicit stop rule, and a written state trail.
Everything else — worktrees, schedulers, connectors, memory, dashboards,
approval gates — is scaling equipment for running many loops, not requirements
for one good loop. Prompts buy one output; loops buy verified outcomes.

Plain-English rule for Mo: a prompt is asking one worker to do one thing. A
loop is a small operating system that keeps assigning work, checking the work,
stopping when the answer is good enough, and asking a human before risky moves.

Source check: 2026-06-09 (Claude Code /goal and hooks docs, Codex goal-mode
cookbook, Anthropic harness-design post). Version-gated claims below go stale
on any Claude Code, Codex CLI, or model release touching goal mode, hooks, or
automations — verify against current vendor docs before relying on them. For
Fable 5 prompt-style rules, load `prompt-generation`
`references/claude-fable-5.md` instead of inlining model facts here.

## The Minimal Closed Loop

Every loop that ships has exactly these six parts. Design them first.

| Part | Contract |
|---|---|
| Goal | A machine-checkable condition — test command, scalar metric, schema-validated verdict, labeled browser proof. Never prose intent. |
| Actor | One unit of work per iteration, fresh context each iteration, investigate before implement, commit per iteration so git is the keep/revert mechanism. |
| Verifier | Independent context. Sees only the rubric and the artifact, never the actor's reasoning. Fresh verifier per pass. |
| Stop | All four exits wired before iteration 1: (a) goal met per verifier; (b) hard iteration/budget cap; (c) STUCK — blocked-stop report, exit; (d) same major finding 3x = non-convergence, stop and escalate. |
| Memory | Disk only (ledger, plan, learnings file). Lessons enter only after a verified fix. Prune ruthlessly. |
| Escalation | A designed state, not a failure: package context, hand to a stronger model or a human. |

The human sits on the loop, not in it: reviews surfaced PRs with evidence
attached, watches the first iterations, owns plan regeneration and values.
Keep the human gate on anything that touches production.

The STUCK exit is a report, not a shrug:
`{attempted_paths, evidence_gathered, blocker, next_input_needed}`. A loop
that cannot say why it is stuck just burns budget restating the problem.

## Human-Gated Multi-Step Loops

For any loop that can spend money, publish, message people, touch production,
merge code, modify calendars, or change durable memory, design the human gate
before the first run. A human gate is not "the user can stop it if they see
something wrong"; it is a required pause state that blocks the next step until
approval is recorded.

Use this approval ladder:

| Gate | Required before | Evidence package |
|---|---|---|
| Plan gate | worker fan-out, implementation, external reads at scale | goal contract, task lanes, allowed paths/tools, risk list, budget cap |
| Action gate | writes, sends, deploys, merges, publishes, paid actions | diff/preview, verifier verdict, rollback plan, exact action to approve |
| Escalation gate | retrying after non-convergence, increasing budget/model/tool power | failure fingerprints, attempted paths, why the next retry is different |
| Memory gate | saving durable lessons/preferences | verified lesson, source evidence, why it is reusable |

Approval records must be explicit and durable: `approved_by`, `approved_at`,
`approved_action`, `scope`, and `expiration`. If approval is missing, expired,
or ambiguous, the loop stops with `needs_human`.

Multi-step loops should be modeled as phases, not as one giant prompt:

1. **Scout** — inspect and summarize reality. No edits.
2. **Plan** — decompose into lanes with acceptance criteria.
3. **Build/Act** — run isolated workers.
4. **Verify** — one serialized validation lane decides pass/fail/stuck.
5. **Approve** — human reviews evidence before risky actions.
6. **Commit/Publish/Record** — only the approved action runs.
7. **Learn** — save only verified lessons and errors.

Each phase must name: owner, inputs, outputs, allowed tools, stop condition,
handoff path, and next gate.

For deeper operating guidance, load
`references/human-gated-parallel-loops.md` when the user asks how to run many
agents, build an agent control system, design loop observability, or launch a
multi-agent loop with human approval.

## Running 15 Parallel Agents

Running 15 agents is a supervisor problem, not a prompting problem. The parent
agent is the conductor; workers are isolated lanes. Workers should not chat
with each other, share a dirty worktree, or decide what "done" means.

Default 15-agent pattern:

1. Split into 15 narrow lanes only when the work naturally decomposes. If the
   lanes overlap heavily, use fewer workers.
2. Give every lane a unique `lane_id`, `scoped_goal`, `allowed_paths`,
   `forbidden_actions`, `handoff_path`, and `acceptance_criteria`.
3. Use isolated worktrees or read-only scouts. Never let multiple workers edit
   the same files unless the parent has assigned one as integrator and the
   others are read-only reviewers.
4. Require every worker to return a structured handoff:

```json
{
  "lane_id": "...",
  "status": "done|blocked|failed",
  "changed_files": [],
  "evidence": [],
  "risks": [],
  "questions_for_human": [],
  "recommended_next_action": "..."
}
```

5. Keep validation serialized: many workers can research or build in parallel,
   but one verifier lane decides whether the integrated result passes.
6. Integrate in batches. For 15 workers, use 3 waves of 5 unless tasks are
   read-only and independent. After each wave, update the scoreboard before
   launching the next wave.

The scoreboard is mandatory. Minimum columns: `lane_id`, `owner`, `status`,
`last_update`, `artifact`, `verifier_status`, `human_gate`, `cost_or_turns`,
`blocker`, `next_action`.

If the parent cannot explain the scoreboard in one paragraph, the loop is too
large to run safely.

## Evaluations and Observability

Evaluations answer "did the loop produce the right outcome?" Observability
answers "what is the loop doing right now, what changed, and where is it
stuck?" A serious loop needs both.

Design evals before launch:

| Eval type | Question answered | Example |
|---|---|---|
| Regression eval | Did we break known behavior? | test suite, lint, typecheck, browser screenshot diff |
| Rubric eval | Is subjective quality good enough? | fresh verifier grades binary criteria with evidence |
| Safety eval | Did the loop stay inside boundaries? | diff-scope check, no protected paths, no secrets |
| Progress eval | Is each iteration learning or just repeating? | unique failure fingerprints, changed plan, new evidence |
| Human-value eval | Is this useful to the operator/customer? | approval checklist, decision-ready artifact review |

Observability minimum:

- Append-only `state.json` or `loop-ledger.md` with one entry per iteration.
- Per-lane handoff files for every worker.
- Run IDs on every artifact, PR, deployment, message draft, and verifier
  result.
- Failure fingerprints for repeated findings.
- Cost/turn counters and a hard cap.
- Heartbeat: last useful action timestamp, last verifier result, next gate.
- Human-facing status labels: `running`, `needs_human`, `blocked`, `failed`,
  `verified`, `published`, `rolled_back`.

Never call a loop "done" because agents stopped talking. Done means the named
verification surface passed, the action gate was satisfied if needed, and the
final artifact has proof attached.

## Deriving the Goal

Most loop failures are goal failures. A weak goal is one sentence of outcome;
a strong goal names the verification command and the stop rule. Turn a fuzzy
goal into the six-field contract (Codex's official goal contract — adopt it on
every provider):

1. **Outcome** — what is true when the work is done.
2. **Verification surface** — the test, benchmark, command output, or artifact that proves it. Name the command.
3. **Constraints** — what must not regress.
4. **Boundaries** — files, tools, data, and external actions the loop may touch.
5. **Iteration policy** — how the actor decides what to try next after each attempt.
6. **Blocked stop condition** — when to stop and report that no defensible path remains.

Worked contrast: "make the tests pass" is weak. "`npm test` exits 0 with no
file outside `test/auth/` modified; stop after 15 iterations or when the same
failure repeats 3x, and report the blocker" names the surface, the boundary,
and both stop rules.

Claude `/goal` wrinkle: its evaluator reads only the transcript and runs no
commands, so write the condition as end-state + stated check + constraints,
make the actor surface verification output into the transcript every turn,
and put a turn/time bound inside the condition ("…or stop after 20 turns").

## Verifier Design

The maker never grades its own work. Agents reliably skew positive on their
own output; tuning a standalone evaluator to be skeptical is tractable, making
a generator self-critical is not. Self-critique is allowed only as pre-handoff
hygiene, never as the gate.

Pick the cheapest judge that can actually observe the evidence:

| Tier | Judge | Use when |
|---|---|---|
| T0 | Deterministic script (Stop hook, CI, in-loop gate) | Done-ness is fully machine-checkable: exit codes, file counts, diff scope, lint/test green. Always prefer. |
| T1 | Small-model transcript evaluator (Claude /goal pattern) | Evidence sits in the transcript and needs light judgment to map to the condition. Blind to anything the actor never surfaced. |
| T2 | Fresh-context tool-using verifier subagent | Reality must be inspected independently (re-run tests, fetch cited URLs, click the UI) or the gate is subjective quality. Most expensive — serialize to one validation lane. |

Verdicts are schema-enforced, never prose:

```json
{"verdict": "pass|fail|stuck",
 "criteria": [{"id": "...", "pass": true, "evidence": "...", "severity": "blocker|major|minor"}],
 "summary": "...", "next_action": "..."}
```

All fields required, `additionalProperties: false`. Schema-parse failure, a
refusal, or truncation is a loud FAIL of the verification step — never a
silent retry, never a pass. Map `stuck` to the blocked-stop report.

Severity gates continuation: loop again only on blocker or major findings.
Minor findings never drive another pass — that is how loops thrash on style
nits forever.

Rubric authoring, condensed: per-criterion and binary-checkable ("open X,
confirm it states Z", not "check X is covered"); named evidence required
before any pass; describe the goal, not the steps — a tool-using verifier
finds its own proof; anticipate shortcuts explicitly; include a no-fire list
of things to ignore; hard threshold per criterion; bounded iterations always.

## The Review-Loop Pass Contract

For review-shaped loops, run three roles per pass:

1. A **fresh-context reviewer subagent** reads only the diff and the rubric, returns findings with severities.
2. A **scoped fixer subagent** receives only the blocker/major findings, fixes, commits.
3. The **parent acts as severity judge**: decides whether remaining findings justify another pass, tracks finding fingerprints, stops at 3 repeats of the same major finding.

The parent never fixes and never reviews — splitting the roles is what keeps
the loop closed.

## Launch Surfaces

What each surface gives you free, and what you must still add:

| Surface | Free | You must add |
|---|---|---|
| Claude `/goal` (v2.1.139+) | Per-turn small-model evaluator, yes/no + reason; headless via `claude -p "/goal …"` | Transcript-demonstrable condition; in-condition turn bound; actor surfacing evidence every turn |
| Claude `/loop` | Interval re-trigger (cron or self-paced) | Everything else: goal, verifier, stop, budget — it is a scheduler, not a loop |
| Claude hooks | Deterministic gates: exit-2 PreToolUse blocks, Stop hook blocks turn-end (8-consecutive-block override) | The verification command itself; `stop_hook_active` guard; hook `if` conditions fail open |
| `claude -p` headless | Scriptable single runs with `--allowedTools` | The outer until-loop, an OK/FAIL output contract, budget caps, ledger |
| Claude Workflow / subagents | Fan-out with fresh contexts | A serialized validation lane; the verdict schema |
| Codex `/goal` goal-mode (0.128.0+) | Six-field contract, evidence audit, budget gating, no-tool-call continuation suppression | An independent verifier — completion is self-declared; compensate with external T0/T2 checks |
| Codex automations (thread + standalone) | Scheduling, Triage inbox, auto-archive when quiet | The method — skills define it; goal + stop rules per run |
| `codex exec --json --output-schema` + `resume --last` | Schema-enforced verdicts, resumable sessions | The loop harness around it; budget and non-convergence detection |
| `codex cloud --attempts N` | Best-of-N parallel attempts | A verifier that picks the winner; N is fan-out, not iteration |

Shared invariant both vendors state independently: a loop is only as good as
its named verification surface and its explicit blocked-stop condition.

## Memory and Ledger

goal-post's Lightweight Run Ledger is the canonical cross-loop schema; do not
invent another. Minimal fields per iteration: iteration number, action taken,
evidence link, gate result, scope cuts. Other formats (SHARED_TASK_NOTES.md,
results.tsv) map onto it — keep the mapping, not a fifth format.

Lessons enter memory only after the fix is verified: fail → investigate →
verify → distill → consult. Unverified lessons become spurious generalizations
that misdirect later iterations (CL-Bench: naive full-context beats a memory
system polluted this way). One lesson per file, update rather than duplicate,
prune on schedule.

## Routing — Reference, Never Duplicate

| Need | Use | This skill adds only |
|---|---|---|
| Durable goal artifact, priority tiers, run ledger, stop conditions | goal-post | how to write the rubric and gates that go in it |
| Loop until CI is green on a PR | loop-on-ci | nothing — it is the leaf implementation |
| Adversarial confidence pass on a plan | loophole-loop | when to schedule it (plan close) |
| Choosing among runnable loop patterns | ecc-continuous-agent-loop | the design layer above the catalog |
| Scalar-metric experiment loop (keep/discard on a number) | autoresearch | the worked example of metric-as-rubric |
| Claude-side observer/supervision layer | claude-heartbeat-loop | the provider-neutral supervisor contract |
| Authoring the goal/rubric prompt text itself | prompt-generation | the loop-specific structure |

Not this skill: `ooda-loop` is Boyd decision tempo, not an agent loop;
`open-loop-radar` is business open-work inventory. Route those requests there.

## Production Hardening

Before running any loop unattended, scheduled, or with permission prompts
relaxed, read `references/production-hardening.md` in full — deterministic-gate
ladder, sandbox profiles, cost-governance ladder, supervisor contract,
failure-mode taxonomy with detection signals, loop-file lint rules. Do not
load it when designing a single attended interactive loop.

## Anti-Patterns

- **No convergence condition.** A while-true with vibes exits only by crash or by bill. Wire all four stops before the first iteration.
- **Verifier sees the actor's reasoning.** It grades the story instead of the artifact. Rubric + artifact only.
- **Parallel validators.** Two verdicts un-close the loop — which one gates? Parallelize reads; serialize validation to one lane.
- **Unverified lessons in memory.** They compound into stale beliefs that misdirect every later iteration.
- **Secrets in loop prompt files.** Anything the loop reads becomes prompt context, then transcript and ledger content. Env-injected auth only.
- **Removing the human gate on prod-touching loops.** An unattended loop making mistakes is the same mistake at machine speed.
- **Raising effort or model tier to fix a failing loop.** The usual root cause is a missing verification surface or boundary, not missing capability. Add a check before adding compute.

## Validation

Structural (proves shape, not behavior):

```bash
python3 skills/skill-creator/scripts/quick_validate.py skills/loop-engineering
python3 scripts/validate-skill-frontmatter.py --json
python3 scripts/validate-skill-evals.py --skills-dir skills --json
python3 scripts/query-skill-graph.py "design a loop that fixes CI until green"
```

Behavioral: run the `evals/evals.json` cases against a live agent and check
each case's assertions; a fresh-context skill-judge pass before shipping
changes to this skill.
