# Production Loop Hardening

Load this file before running any loop unattended, on a schedule, or with
permission prompts relaxed. It assumes the minimal closed loop from `SKILL.md`
is already designed; this is the survival layer around it.

Source check: 2026-06-09 — Claude Code hooks/sandboxing docs, Codex
sandboxing/config-reference docs, Anthropic harness-design post, HumanLayer
RPI/ACE-FCA corpus. Stale on any Claude Code, Codex CLI, or sandbox-policy
release. The RPI instruction-ceiling and context-utilization numbers are
practitioner-reported (Horthy, Mar 2026 talk via secondary sources), not
vendor-documented — treat as heuristics.

## Deterministic-Gate Ladder

Escalate enforcement in this order; prose rules are the weakest rung.

1. **In-prompt check** — cheapest, weakest. Fine for attended runs only.
2. **/goal condition** — separate small-model evaluator re-checks every turn.
3. **Deterministic Stop hook** — a script that runs the goal's named
   verification command before allowing turn-end. Exit 2 blocks the stop and
   feeds stderr back to the actor. Exit 1 is NOT blocking — unlike Unix
   convention — so enforcement must use exit 2.
4. **Fresh-context adversarial review** — the agent doing the work is not the
   one grading it.

Hard prohibitions (forbidden commands, protected paths) belong in exit-2
PreToolUse hooks or permission/sandbox rules, not in prompt text.

Stop-hook mechanics to design around:

- Parse `stop_hook_active` from the hook's JSON input and exit 0 (allow stop)
  when true — this guards recursion.
- Claude Code overrides a Stop hook after it blocks 8 times in a row without
  progress; the turn then ends with a warning. Raise deliberately via
  `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP` if a loop legitimately needs more passes;
  treat the cap as the built-in non-convergence backstop, not an annoyance.
- Hook `if` conditions are best-effort and FAIL OPEN. Anything that must hold
  goes in permission rules or the sandbox, never in an `if`.
- The sandbox denies writes to `settings.json` at every scope — a sandboxed
  loop cannot rewrite its own policy. Verify this holds before unattended runs.

## Unattended Sandbox Profiles

Permission-skipping is acceptable only inside an OS-enforced sandbox or a
non-root container with no or minimal network.

Claude Code profile:

- `sandbox.enabled: true`, `failIfUnavailable: true`,
  `allowUnsandboxedCommands: false` (strict mode also ignores the
  `dangerouslyDisableSandbox` escape hatch).
- Default read scope is the ENTIRE machine including `~/.aws` and `~/.ssh` —
  add `sandbox.filesystem.denyRead` for credential paths explicitly.
- `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` strips credentials from subprocess env.
- Network: minimal proxy allowlist. Broad allows like `github.com` create
  domain-fronting exfiltration paths — the proxy does not inspect TLS.
- `--dangerously-skip-permissions` only in a non-root container without
  internet access.

Codex profile:

- `sandbox_mode: workspace-write` + `approval_policy: on-request` +
  `approvals_reviewer: auto_review` is the unattended recipe.
- `requirements.toml` is the admin-enforced floor: forbid
  `approval_policy = "never"` and `sandbox_mode = "danger-full-access"` on any
  shared or client machine. Requirements rules can only prompt or forbid,
  never allow — users cannot widen them.

## Cost-Governance Ladder

Apply in order; each rung is cheaper than the one below it.

1. **Fresh/isolated session per tick** — drops ~100K tokens to ~2–5K per run.
2. **Model downshift per layer** — free shell predicate → cheap-model triage →
   strong-model tick. Effort: low/medium for routine ticks, high default,
   xhigh only for capability-sensitive work.
3. **Active-hours window** — loops that run while nobody can respond burn
   budget producing work nobody gates.
4. **Per-tick caps** — max turns, max budget USD, token ceiling.
5. **Budget exhaustion = investigate drift, never raise the cap silently.**
   Recurring cap hits are a symptom (ledger drift, scope creep, churn), not a
   sizing problem.

Start with a slow cadence and a tight goal condition; scale only once the
loop produces work you actually merge.

## Supervisor Contract (provider-neutral)

- The **doer** writes progress/blocker/question entries to an append-only,
  git-tracked disk ledger. Rollback is `git revert`.
- The **observer** wakes on its own clock (zero-cost predicates → cheap triage
  → deep tick), reads the ledger since its cursor, course-corrects against the
  goal file with file-path specificity, and acks what it has seen.
- Neither agent sits in the other's critical path: an observer missing a tick
  never stalls the doer; a stalled doer is detected as absent progress
  entries, not as a hung call.
- Escalation is designed: package context, hand to a stronger model or human.
  More than 3 unacknowledged corrections pages the human — the loop is
  fighting its supervisor.
- In-session schedulers expire (7-day cron limit); use an external
  launchd/crontab fallback plus a missed-tick alert for long runs. If you
  forget to re-arm, the loop dies silently.
- The human stays on the loop at PR review; architecture decisions are never
  auto-merged. For brownfield work, keep the human plan-gate before
  implementation — it is the canonical anti-PR-slop control.

## Failure-Mode Taxonomy

Every detection signal needs a named response wired before launch.

| Failure | Detection signal | Response |
|---|---|---|
| Loop churn / circling | Same plan items reopened; empty plan-file diff and no progress entries across N ticks | Regenerate the plan — one planning pass is cheap next to circling |
| Same-root-cause retries (non-convergence) | Same finding fingerprint 3x from the verifier | Stop and escalate; never retry a fourth time |
| Duplicate-rebuild drift | Duplication spike; new modules shadowing existing names | Enforce investigate-before-implement each iteration |
| Merge stalls / PR rot | Open-PR count or age past threshold while the loop stacks more | Babysit/merge loop; hard completion gate: no handoff without a PR URL |
| Cost drift | Budget caps hit repeatedly; tokens per tick trending up | Investigate ledger drift first; isolated sessions and caps — never silently raise |
| PR-slop flooding | Review-queue depth and reviewer turnaround climbing; PRs merging with zero comments | Design doc before implementation; severity-gated verifier; surface only ready-to-merge work |
| Spinning without action | Turns producing zero tool calls | Suppress auto-continuation on no-tool-call turns (Codex does this natively; replicate as a Stop-hook check) |
| Memory poisoning | Lessons contradicting repo reality; degrading decisions | Verified-lessons-only rule; scheduled pruning |
| Instruction budget overflow | Checklist items skipped without error | Prune the loop prompt; lint instruction count (see below) |
| Context rot | Quality degrading deep in long sessions | Fresh context per iteration; keep utilization under ~40%, hard fresh-session line at ~60% |
| Over-correcting supervisor | Corrections piling up unacknowledged | >3 unacked → pause observer, collapse corrections into one, page human |
| Silent heartbeat death | Missed ticks; no ledger writes after scheduler expiry | External scheduler fallback from day one; missed-tick alert |
| Secrets leak via loop files | Credentials appearing in prompt files, transcripts, or ledgers | Never put secrets in any loop-read file; env-injected auth only |

## Loop-File Lint Rules

Run these checks on every file a loop reads as prompt context (HEARTBEAT.md,
PROMPT.md, goal artifacts, plan files):

- **No secrets, tokens, or PII.** Loop-read files become prompt context, then
  transcript and ledger content. Env-injected auth only.
- **Instruction count: warn above ~150.** Frontier models lose instruction
  consistency around 150–200 instructions in a single prompt and skip steps
  silently — gates get dropped without any error (practitioner-reported).
- **The goal names its verification command and all four stop conditions** —
  lint for their presence, not just for prose about quality.
