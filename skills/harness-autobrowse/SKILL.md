---
name: harness-autobrowse
description: >
  Self-improving browser-skill factory built on top of browser-harness. Runs
  one task → reads the trace → forms one hypothesis → updates strategy.md →
  retries, until the task passes on 2 of the last 3 runs, then graduates the
  proven strategy into browser-harness's domain-skills/<site>/<task>.md so
  every future browser-harness run on that site benefits. Use when the user
  says "auto-browse this site", "build a skill for X site", "learn how to
  scrape Y", "fix the failing automation on Z", "auto-improve the linkedin
  outreach", "make this browser run reliable", or wants the autobrowse
  iteration loop without paying for BrowserBase's `browse` CLI runtime.
  Free — uses browser-harness (which uses your real Chrome) as the runtime,
  Anthropic API tokens for the iteration only when delegated to a sub-agent.
metadata:
  author: contributor
  version: 1.0.0
  inspired_by: github.com/browserbase/skills/tree/main/skills/autobrowse
  license: MIT
related_skills: [browser-harness, browserbase-skills-pack]
---

# harness-autobrowse — Self-Improving browser-harness Skill Factory

The autobrowse iteration discipline (TDD applied to browser automation),
ported to drive `browser-harness` instead of BrowserBase's `browse` CLI.
The runtime is your real, logged-in Chrome — not a paid cloud session.

**Inspired by:** `github.com/browserbase/skills/tree/main/skills/autobrowse`
**Differences from upstream autobrowse:**

| | Upstream autobrowse | harness-autobrowse |
|---|---|---|
| Runtime | `browse` CLI (free local; paid remote) | `browser-harness` (always free) |
| Authenticated sessions | `browse env local --auto-connect` | Native — your real Chrome |
| Helper API | Fixed CLI surface | Editable `helpers.py` (self-extending) |
| Graduation target | Standalone `~/.claude/skills/<task>/SKILL.md` | `domain-skills/<site>/<task>.md` (browser-harness's existing convention) |
| Inner agent | Spawned Claude Agent SDK process | The current outer agent (Claude in this session) |
| Cost | Anthropic API tokens (and BB if remote) | Anthropic API tokens only — and zero if outer agent does the loop directly |

## When to Use

Trigger phrases:
- "auto-browse this site" / "build a skill for <site>"
- "learn how to scrape <site>" / "fix the failing automation on <site>"
- "auto-improve the <site> flow" / "make this browser run reliable"
- "iterate until <site> works"
- After a manual `browser-harness` run fails repeatedly with no clear single fix

Don't use for:
- One-off tasks the user wants done *now* (just run `browser-harness` directly)
- Tasks where the bottleneck is bot detection — escalate to `browserbase-browser env remote` first or accept that the free path may not converge

## The Loop (the whole skill)

```
┌───────────────────────────────────────────────────────────┐
│  task.md          (read-only spec — URL + goal + expected │
│                    output schema; written once)           │
├───────────────────────────────────────────────────────────┤
│  strategy.md      (mutable working file — outer agent     │
│                    edits this between iterations)         │
├───────────────────────────────────────────────────────────┤
│  runs/run-NNN/    (per-iteration artifacts: strategy      │
│                    snapshot, screenshots, helper output,  │
│                    final status, hypothesis tested)       │
├───────────────────────────────────────────────────────────┤
│  history.jsonl    (one line per run: pass/fail + notes)   │
└───────────────────────────────────────────────────────────┘

For each iteration:
  1. start-run     → creates run-NNN/, snapshots strategy.md
  2. agent runs browser-harness following strategy.md
  3. agent records artifacts (screenshots, helper output)
  4. finish-run    → writes status + hypothesis to run-NNN/
  5. agent reads run summary, forms ONE hypothesis, edits strategy.md
  6. repeat (max 5 iterations by default)

Graduation: when status passes on 2 of the last 3 runs, copy strategy.md
            to ~/.local/share/browser-harness/domain-skills/<site>/<task>.md
```

## Workspace Layout

All training artifacts live under `${CWD}/harness-autobrowse/` — never inside
`~/.claude/skills/`. Same convention as upstream autobrowse: this keeps agent
writes out of the home dir and isolates per-project task state.

```
./harness-autobrowse/
  tasks/
    <task-name>/
      task.md             # read-only spec
      strategy.md         # mutable, evolves each iteration
  runs/
    <task-name>/
      run-001/
        strategy.md       # snapshot of strategy at run time
        summary.md        # outer agent writes this after the run
        status.txt        # "pass" | "fail" | "partial"
        hypothesis.txt    # one-line hypothesis tested in this run
        screenshots/      # captured by browser-harness or attached trace
      run-002/
        ...
      latest -> run-NNN   # symlink to most recent run
      history.jsonl       # {ts, run, status, hypothesis} one per line
  reports/
    <iso-date>-<task>.md  # session report after the loop ends
```

## Workflow

### Step 0 — Pre-flight (recommended)

Probe the site for bot detection before investing iterations:

```bash
node ~/.claude/skills/browserbase-what-antibot/scripts/detect.mjs <url>
```

If the result is Cloudflare/DataDome/Akamai, decide upfront: either accept
that browser-harness alone may not converge (and consider escalating to
`browserbase-browser env remote`), or proceed knowing strategy.md will need
to capture session-warming heuristics.

### Step 1 — Initialize the task

```bash
bash ~/.claude/skills/harness-autobrowse/scripts/init.sh \
    <task-name> <url> "<one-sentence goal>"
```

Creates `./harness-autobrowse/tasks/<task-name>/{task.md,strategy.md}` from
templates in this skill's `references/`. Edit `task.md` to add the expected
output schema and any constraints. **Don't edit task.md after the first
iteration** — it's the spec.

### Step 2 — Run an iteration

```bash
RUN_DIR=$(bash ~/.claude/skills/harness-autobrowse/scripts/start-run.sh <task-name>)
echo "Run dir: $RUN_DIR"
```

This snapshots the current `strategy.md` into `$RUN_DIR/strategy.md` and
prints the run directory. The outer agent (you, in this session) now:

1. Reads `tasks/<task-name>/task.md` for the goal and `tasks/<task-name>/strategy.md` for the latest plan.
2. Optionally attaches `browserbase-browser-trace` for full CDP firehose capture (recommended after iteration 2 if iterations 1-2 failed unclearly).
3. Runs `browser-harness <<'PY' ... PY` to execute the task, taking screenshots into `$RUN_DIR/screenshots/` at decision points.
4. Writes a brief `$RUN_DIR/summary.md` with: turn-by-turn what happened, where it deviated from the goal, the final outcome.

### Step 3 — Finish the run

```bash
bash ~/.claude/skills/harness-autobrowse/scripts/finish-run.sh \
    <task-name> <status> "<one-line hypothesis tested>"
```

`<status>` ∈ `pass | fail | partial`. The hypothesis records *what change*
the outer agent made to strategy.md *for this run* (or "baseline" for the
very first run). Appends a line to `runs/<task-name>/history.jsonl`.

### Step 4 — Form one hypothesis, edit strategy.md

This is the discipline that makes the loop work:

> **One hypothesis per iteration.** Find the exact turn things broke. Form
> one heuristic that would have prevented it. Edit strategy.md to encode
> that heuristic. Don't fix three things at once — you won't be able to
> tell which fix mattered.

Good hypotheses (concrete, single-cause):
- "After clicking the dropdown, wait 1s — options animate in before they're clickable"
- "Navigate directly to `/cart/` instead of going through the homepage — saves 4 turns and avoids the modal"
- "Use `js(\"document.querySelector('#field_3')?.dispatchEvent(new Event('change'))\")` after fill — the form clears its inner state on focus events"
- "When the page shows a spinner at turn 8, add `wait_for_load()` and another `screenshot()` before the next click"

Bad hypotheses (vague, multi-cause):
- "Make it more reliable"
- "Handle errors better"
- "Add waits"

If a run regresses (passes turned to fails), **revert strategy.md to the
previous run's snapshot** (`runs/<task-name>/run-(NNN-1)/strategy.md`) and
try a different hypothesis.

### Step 5 — Graduate

When the task passes on **2 of the last 3 consecutive runs**, run:

```bash
bash ~/.claude/skills/harness-autobrowse/scripts/graduate.sh <task-name>
```

This:
1. Verifies the 2-of-last-3 rule from `history.jsonl`.
2. Extracts the site host from `task.md`.
3. Copies `tasks/<task-name>/strategy.md` to `~/.local/share/browser-harness/domain-skills/<site>/<task-name>.md`, prefixing with the standard browser-harness domain-skill header.
4. Suggests opening a PR back to `browser-use/browser-harness` so the skill ships to other agents.

## Strategy.md — what to put in it

Good strategies have **four sections**, mirroring the structure that
graduates well into a domain-skill:

```markdown
# <Task Title> — Strategy

## Fast Path
<Direct URL or shortcut to skip exploration. Often the single biggest win.>

## Step-by-Step Workflow
<Exact browser-harness helper sequence with timing notes. Reference
selectors, JS expressions, screenshot checkpoints.>

## Site-Specific Heuristics
<Bullet list of every hard-won rule from iterations. This is the core
value — what the next agent needs to know that isn't in the HTML.>

## Failure Recovery
<What to do when X goes wrong. Each entry is a {symptom → fix} pair.>
```

`references/example-strategy.md` in this skill is the starting template
that `init.sh` copies.

## Examples

### Example 1: Build a reliable cart-add automation for a Shopify store

```bash
bash ~/.claude/skills/harness-autobrowse/scripts/init.sh \
    my-store-cart-add https://my-store.com/products/widget \
    "Add the medium variant to cart and verify the count goes up by 1"

# Edit ./harness-autobrowse/tasks/my-store-cart-add/task.md to add the
# expected output schema and any selectors you already know.

# Iteration 1 — baseline
RUN_DIR=$(bash ~/.claude/skills/harness-autobrowse/scripts/start-run.sh my-store-cart-add)
# Outer agent runs browser-harness, captures screenshots, writes summary.md
bash ~/.claude/skills/harness-autobrowse/scripts/finish-run.sh \
    my-store-cart-add fail "baseline — no strategy"

# Outer agent reads $RUN_DIR/summary.md, sees "size dropdown didn't register
# the click — modal closed before the option was selected"

# Edit strategy.md: add the heuristic about waiting 500ms after dropdown open

# Iteration 2 — test the heuristic
RUN_DIR=$(bash ~/.claude/skills/harness-autobrowse/scripts/start-run.sh my-store-cart-add)
# ... iterate ...
```

### Example 2: Fix a flaky LinkedIn-outreach automation

If `browser-harness` already sort-of works on a site but fails 30% of the
time, harness-autobrowse turns that into a deterministic flow. Init the
task pointing at the failing flow, run baseline, hypothesize one stability
fix per iteration, graduate when stable.

## Troubleshooting

### `start-run.sh` says "no strategy.md exists"
- **Cause:** Forgot to run `init.sh` first.
- **Fix:** `bash scripts/init.sh <task-name> <url> "<goal>"`.

### `graduate.sh` says "2-of-last-3 not yet met"
- **Cause:** History doesn't show enough passes.
- **Fix:** Look at `runs/<task-name>/history.jsonl` — find which iteration regressed and form a hypothesis to fix it.

### Runs alternate pass/fail with no apparent cause
- **Cause:** Probably non-determinism the strategy doesn't account for (timing, A/B variants, dynamic content).
- **Fix:** Add `browserbase-browser-trace` mid-run to capture network and console activity. Look for the *difference* between passing and failing runs in the firehose.

### Strategy file gets long and hard to read
- **Cause:** Adding too many heuristics without consolidating.
- **Fix:** After every 3-4 iterations, refactor strategy.md — group related rules, delete superseded ones. The graduated domain-skill should be readable.

## Rules

- **Only edit `strategy.md`** — never modify `task.md` after init (unless the spec genuinely changed and you want to start over).
- **Stay in `./harness-autobrowse/`** — never write training artifacts to `~/.claude/skills/`. The skill source is read-only.
- **One hypothesis per iteration** — test one change at a time.
- **Build on wins** — keep what worked, add to it.
- **Trust the trace** — if the outcome doesn't match expectation, the trace is the ground truth.
- **Graduate to `domain-skills/`** — the only file written outside the workspace is the final graduated `<site>/<task>.md`.
