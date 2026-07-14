---
name: compound-rule
description: "Promote a repeated agent mistake into a permanent rule with a regression check. Use when an agent makes the same mistake twice, when asked to promote a lesson to a rule, on @compound mentions, or for compounding-engineering / RULES-LEDGER workflows."
related_skills: [loop-engineering, skill-judge, prompt-generation, ecc-continuous-learning-v2]
---

# Compound Rule



Severity override: data-loss, secrets exposure, or prod-deploy mistakes promote on first occurrence — do not wait for recurrence.

## Workflow

### 1. Capture (ERRORS.md entry)

Every mistake gets an ERRORS.md entry in `.learnings/ERRORS.md` at the moment of correction — not later.

Required fields: Context / Symptom / Root cause / Fix / Prevention / Validation.
Validation **must** cite a tool result (command output, CI link, eval receipt). Self-assertion is not valid.

If this is the **first occurrence**: stop here. No rule yet. No ledger row.

### 2. Recurrence check

Grep `.learnings/ERRORS.md` and `.learnings/RULES-LEDGER.md` for prior entries sharing the same root cause.

Second occurrence of the same root cause → proceed to step 3.
Severity override (data-loss / secrets / prod) → proceed immediately.

### 3. Retrospective

Write two sentences: what the pattern is, and why the current tooling did not prevent it.
This becomes the "why" in the ledger row and the PR body.

### 4. Placement ladder

Choose the most deterministic home for the rule. Work top-down and stop at the first fit:

1. **Hook or CI check** — preferred. Deterministic, runs every time, can fail fast. (Example: a `PreToolUse` hook that blocks a known bad pattern; a CI byte-budget check.)
2. **Skill `references/` file** — for workflow-shaped lessons. Loaded on demand, does not bloat every session.
3. **Nested AGENTS.md** — only for the affected directory, not the repo root.
4. **Root AGENTS.md** — last resort. One line max. Must pass: "Would removing this cause the agent to make the mistake again?" If not, cut.

Never write provenance or reasoning into AGENTS.md. That lives in the ledger.

### 5. Write the regression check

Pick one:

- **CI/hook assertion** — a shell command or hook that fails when the mistake recurs.
- **Eval case** — a prompt + assertion in the public-skills evals manifest pointing back to the ERRORS.md entry (provenance field).
- **Skill-judge rubric line** — a judgment criterion in a reviewer skill that catches the pattern.

No regression check = no merge. This is the only non-negotiable gate.

### 6. RULES-LEDGER.md row

Add a row to `.learnings/RULES-LEDGER.md`:

| date | rule (one line) | source ERRORS.md entries | occurrences | placement | regression check | status |

Status starts as `active`. It becomes `demoted` when a quarterly prune pass shows the regression check still passes after the rule is removed.

### 7. Promotion PR

Open a PR carrying:
- The rule (in its placement home)
- The regression check
- The RULES-LEDGER.md row
- The retrospective in the PR body

Human merge is the review gate. Automation runs only after one manual end-to-end pass.

---

## Anti-patterns

- **Rules without regression checks.** A rule that cannot be tested is folklore. Convert it or drop it.
- **Promoting on first occurrence** (except data-loss/secrets/prod). First occurrence is a correction. Recurrence is a pattern.
- **In-session corrections that never reach a ledger.** If the fix stays in the chat, it dies with the session.
- **Bloating AGENTS.md past budget.** The the project `instructions-budget` CI check hard-fails at 16 384 B. Placement ladder exists to keep the root file lean.
- **Provenance inline in AGENTS.md.** Ledger carries provenance. AGENTS.md carries one-line rules only.

---

## Quarterly prune

Remove a rule on a branch. Run its regression check. If it still passes → the model follows the rule by default now → set status to `demoted` in the ledger and archive the ERRORS.md entry to `.learnings/archive/YYYY-QN.md`.

---

*Design source: the project `docs/research/loop-engineering/deep-dive/compounding-engineering.md` (2026-06-09)*
*Loop: Boris Cherny / @.claude → Codex official "twice" doctrine → Every/Kieran Klaassen Compound Engineering → OpenAI Agent Improvement Loop cookbook*
