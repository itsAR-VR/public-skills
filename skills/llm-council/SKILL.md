---
name: llm-council
description: >
  Stress-test a high-stakes decision by fanning the same question across four
  different model families — Claude (local), GPT-5.6 Sol at ultra effort via
  Codex, MiniMax-M2.7 via its Anthropic-compatible endpoint,
  and Kimi K2.6 via its Anthropic-compatible coding endpoint — each wrapped in
  a Verbalized Sampling prompt that surfaces tail-distribution insights, then
  synthesizing a structured decision brief. Use when the user says "council
  this", "stress test", "pressure test", "test this decision", "have the
  council weigh in", or presents a choice between options with real stakes.
  Supports analytical lenses (default, founder, investor, creator, builder) via
  --lens flag. Combines between-model diversity, within-model diversity (Verbalized
  Sampling), and analytical diversity (lenses) — all three layers from Alex
  Prompter's stack. For single-model brainstorming, see moa. For adversarial
  verification loops, see ecc-santa-method.
metadata:
  author: contributor
  version: 1.2.0
related_skills: [moa, ecc-santa-method, codex, deep-sweep, multi-agent-patterns, kimi-setup]
---

# LLM Council

Four-model decision analysis with Verbalized Sampling and customizable lenses.
Implements the stack from Alex Prompter's April 2026 thread, extended with a
fourth seat:

1. **Between-model diversity** — different training data, different blind spots.
   Claude (Anthropic) + GPT-5.6 Sol with ultra effort (Codex) + MiniMax-M2.7
   (general research lab, China) +
   Kimi K2.6 (coding-tuned lab, Moonshot AI, China). The two Chinese labs share
   a country but not a training recipe — MiniMax skews general-purpose /
   multilingual, Kimi K2.6 is post-trained for code and long-context reasoning.
   They surface different tails.
2. **Within-model diversity** — Verbalized Sampling (Stanford, 2510.01171) asks
   each model to generate 3 candidates with probability estimates, then return
   the lowest-probability tail insight instead of the modal response.
3. **Analytical diversity** — swappable lenses shape what each model looks for.

Codex route checked 2026-07-09 with Codex CLI 0.144.0. Model roster refresh
trigger: before relying on this skill after a provider,
gateway, or Codex CLI change, re-check the current model IDs, token ceilings,
and `codex exec` flags against the provider docs and the `codex` / `kimi-setup`
skills. The MiniMax and Kimi ceilings below are dated operational notes, not
permanent API guarantees.

## When to Use

Trigger phrases:
- "council this: ..."
- "stress test this: ..."
- "pressure test this: ..."
- "test this decision: ..."
- "have the council weigh in on ..."
- Any message that presents a binary or multi-option choice with real stakes

Do **not** auto-trigger on:
- Casual brainstorming or exploratory questions (use direct Claude or `moa`)
- Code review or refactoring (use `code-review`, `deep-sweep`)
- Simple factual lookups

## Prerequisites (verify once)

Before the first run, confirm these are on PATH:

```bash
command -v codex >/dev/null && codex --version
codex debug models | grep -q 'gpt-5.6-sol'   # catalog support; the live council call proves entitlement
command -v claude >/dev/null   # for reference only; council uses codex + curl + local Claude
test -r ~/.config/minimax/token-plan.key && echo "minimax key present ($(wc -c < ~/.config/minimax/token-plan.key) bytes)"
test -r ~/.config/kimi/coding-plan.key && echo "kimi key present ($(wc -c < ~/.config/kimi/coding-plan.key) bytes)"
```

If MiniMax key is missing, tell the user to save it:
```
umask 077 && read -rs "K?Paste MiniMax Token Plan key: " && printf '%s' "$K" > ~/.config/minimax/token-plan.key && unset K
```

If Kimi key is missing (the `kimi-setup` skill bakes the key into wrapper
scripts; this skill needs the same key in a key-file form to stay
provider-agnostic), seed it from the wrapper or paste fresh:
```
# Option A: extract from existing kimi-setup wrapper
mkdir -p ~/.config/kimi && (umask 077 && grep '^KIMI_KEY=' ~/.local/bin/claude-kk \
  | sed 's/^KIMI_KEY="\(.*\)"$/\1/' | tr -d '\n' > ~/.config/kimi/coding-plan.key)

# Option B: paste fresh sk-kimi-... key
umask 077 && read -rs "K?Paste Kimi Coding Plan key (sk-kimi-...): " \
  && printf '%s' "$K" > ~/.config/kimi/coding-plan.key && unset K
```

## Workflow (executed by Claude when triggered)

### Step 1 — Parse input

Extract:
- **Decision text**: everything after the trigger phrase (and after any `--lens X`).
- **Lens**: `--lens default|founder|investor|creator|builder` (if absent, use `default`).
- **Session id**: `council-$(date +%s)` — used as the temp-file namespace.

Example: user says `council this --lens founder: should we self-host our DB or use RDS?`
→ decision = `should we self-host our DB or use RDS?`, lens = `founder`.

### Step 2 — Load the lens

Read the lens file:
```
[~/.claude/skills/llm-council/lenses/{LENS}.md](lenses/default.md)
```

Each lens file defines 4 analytical sub-questions the council should answer.
If the user provided their own lens content (e.g. "use lens: bull case / bear
case / macro / exit"), skip the file read and use their definition inline.

### Step 3 — Build the Verbalized Sampling prompt

Read the VS template:
```
[~/.claude/skills/llm-council/prompts/verbalized-sampling.md](prompts/verbalized-sampling.md)
```

Render it by substituting `{{DECISION}}` and `{{LENS_BODY}}`. Write the result
to `/tmp/council-{SESSION}-prompt.txt` — each council member reads this file
(avoids stdin-size limits on codex, see codex skill's 4KB warning).

### Step 4 — Fan out (in this exact order)

**4a. Claude's perspective — FIRST, BEFORE reading others.**

Generate Claude's tail-sampled response directly in context. Do not peek at
codex or MiniMax output before this. Structure exactly as the VS template
requires (3 candidates with probabilities, selected = lowest). Save to
`/tmp/council-{SESSION}-claude.md`.

Order matters: reading other models first anchors Claude on their framings
and collapses the council back to consensus — defeating the point.

**4b. Launch Codex (GPT-5.6 Sol, ultra effort) in the background.**

Use the nohup detached pattern per the codex skill. Sol at ultra effort on a
genuine decision often runs 2-6 minutes, exceeding Bash's 600s cap.

```bash
SESSION="council-$(date +%s)"
PROMPT_FILE="/tmp/${SESSION}-prompt.txt"
CODEX_OUT="/tmp/${SESSION}-codex.out"
OPENAI_LATEST_MODEL="${OPENAI_LATEST_MODEL:-gpt-5.6-sol}"

nohup codex exec \
  --model "$OPENAI_LATEST_MODEL" \
  -c model_reasoning_effort=ultra \
  --sandbox read-only \
  --skip-git-repo-check \
  "$(cat $PROMPT_FILE)" \
  > "$CODEX_OUT" 2>/dev/null &
CODEX_PID=$!
echo "codex PID: $CODEX_PID"
```

**4c. Fan MiniMax-M2.7 + Kimi K2.6 in parallel via curl (each ~30-180s).**

Both endpoints are Anthropic-compatible and accept extended-compute request
parameters, so we use the same prompt and same Anthropic JSON shape — only the
URL, key, model name, and token ceilings differ. We crank `max_tokens` and
`budget_tokens` to the empirically-verified ceilings on each gateway so each
model spends real compute exploring its distribution rather than returning
the modal response. Verbalized Sampling only works if the model actually
walks its tails; a shallow pass just re-emits the obvious answer.

Run them as parallel background jobs and `wait` — total wall-clock is
`max(MiniMax, Kimi)` ≈ 90-180s, no slower than MiniMax alone. Codex keeps
running in its own nohup-detached process throughout.

**MiniMax ceiling** (`max_tokens: 131072`, `budget_tokens: 120000`) verified
against `api.minimax.io/anthropic` on 2026-04-18 — higher values (200000)
were silently dropped by the gateway.

**Kimi ceiling** (`max_tokens: 32000`, `budget_tokens: 29000`) verified
against `api.kimi.com/coding/v1/messages` on 2026-05-01 — matches the
documented `ANTHROPIC_MAX_TOKENS=32000` ceiling baked into the `kimi-setup`
wrappers. The Kimi gateway maps the request `model: "kimi-k2.6"` to the
internal `kimi-for-coding` inference model — the response will reflect the
internal name, which is normal.

`budget_tokens` is a *cap* not a *floor* — simple decisions use less, hard
ones can think for the full budget on each model.

```bash
MINIMAX_KEY="$(tr -d '\n\r' < ~/.config/minimax/token-plan.key)"
KIMI_KEY="$(tr -d '\n\r' < ~/.config/kimi/coding-plan.key)"

MINIMAX_JSON="$(jq -Rs '{
  model: "MiniMax-M2.7",
  max_tokens: 131072,
  thinking: { type: "enabled", budget_tokens: 120000 },
  messages: [ { role: "user", content: . } ]
}' < "$PROMPT_FILE")"

KIMI_JSON="$(jq -Rs '{
  model: "kimi-k2.6",
  max_tokens: 32000,
  thinking: { type: "enabled", budget_tokens: 29000 },
  messages: [ { role: "user", content: . } ]
}' < "$PROMPT_FILE")"

# Fire MiniMax in the background
curl -sS -X POST https://api.minimax.io/anthropic/v1/messages \
  -H "content-type: application/json" \
  -H "anthropic-version: 2023-06-01" \
  -H "Authorization: Bearer $MINIMAX_KEY" \
  -d "$MINIMAX_JSON" \
  > "/tmp/${SESSION}-minimax.json" &
MM_PID=$!

# Fire Kimi in the background
curl -sS -X POST https://api.kimi.com/coding/v1/messages \
  -H "content-type: application/json" \
  -H "anthropic-version: 2023-06-01" \
  -H "Authorization: Bearer $KIMI_KEY" \
  -d "$KIMI_JSON" \
  > "/tmp/${SESSION}-kimi.json" &
KIMI_CURL_PID=$!

# Wait for both
wait $MM_PID $KIMI_CURL_PID

# Extract the final text blocks (drop thinking for the council view)
jq -r '.content[] | select(.type=="text") | .text' \
  "/tmp/${SESSION}-minimax.json" > "/tmp/${SESSION}-minimax.md"
jq -r '.content[] | select(.type=="text") | .text' \
  "/tmp/${SESSION}-kimi.json" > "/tmp/${SESSION}-kimi.md"

# Do not extract or store provider thinking blocks. The council brief uses
# final text plus observable metadata only.
```

If either curl returns a 429 (Token Plan concurrency cap), retry that one
after 5s. If a request hangs past 4 minutes it was likely dropped by the
gateway — re-issue, don't wait indefinitely.

If a model's final brief feels consensus-y, treat that as evidence from the
visible output. Do not inspect or cite provider thinking traces; re-run with a
different lens or a more specific decision statement if you need stronger
tail-signal.

### Step 5 — Wait for Codex

After MiniMax returns, check if Codex is done:

```bash
ps -p $CODEX_PID > /dev/null 2>&1 && echo "running" || echo "done"
```

If still running, use `ScheduleWakeup` with 180-270s delay (stays in Anthropic's
prompt cache window, avoids cold restart). Each wake: re-check, read if done.

Never poll in a tight sleep loop — that burns context. Wake-up or loop the
skill with a reasonable cadence.

### Step 6 — Read all four perspectives

```bash
cat "/tmp/${SESSION}-claude.md"
cat "/tmp/${SESSION}-codex.out"
cat "/tmp/${SESSION}-minimax.md"
cat "/tmp/${SESSION}-kimi.md"
```

Pay attention to:
- Which CANDIDATE each model selected (probability score)
- Where the selected tail insight diverges from the obvious/modal answer
- What each model flagged as "NOT considering"
- Where MiniMax and Kimi *disagree* — that's the highest-signal axis. They
  share Chinese training-data exposure but not training recipe; agreement
  between them is weaker evidence than agreement across MiniMax↔Claude or
  Kimi↔Codex.

### Step 7 — Synthesize (Claude, chairman role)

Produce the final decision brief in this exact structure. Under 500 words.
No process explanation. Verdict must be real, not "it depends".

```
COUNCIL BRIEF — [decision in one line]
LENS: {LENS}

THE QUESTION
[restate; reframe if the user asked the wrong question]

WHERE THE COUNCIL AGREES
[2-3 convergence points across Claude + GPT-5.6 Sol + MiniMax + Kimi.
Note: agreement weighted higher when it spans different families
(e.g., Claude+Codex+Kimi) than when it spans MiniMax+Kimi alone, since
the two Chinese-lab seats share data-distribution exposure.]

WHERE THE COUNCIL DISAGREES
[1-2 genuine tensions with both sides' reasoning. Surface any
tail-distribution insight that challenges the consensus — label it
[TAIL-X] where X is the model that surfaced it.]

RISK
[most likely failure mode, one sentence]

BLIND SPOT
[unquestioned assumption the user is making, one sentence]

OPPORTUNITY
[unseen upside, one sentence]

VERDICT
[2-3 sentences, clear recommendation, takes a position]

TEST IT THIS WEEK
[specific action + metric + threshold that would confirm or falsify the verdict]

---
Council members: Claude (local) · GPT-5.6 Sol ultra (Codex) · MiniMax-M2.7 · Kimi K2.6
Session: {SESSION}  ·  Lens: {LENS}
```

### Step 8 — Offer follow-ups

After presenting the brief, use `AskUserQuestion` to offer:
- "Run again with a different lens?"
- "Resume the Codex session for deeper analysis with `codex exec resume --last`?"
- "Pressure-test a follow-up decision?"

## Examples

### Example 1: Founder lens

**User says:** `council this --lens founder: should we raise a seed round now or bootstrap another 6 months?`

**Actions:**
1. Parse → decision = "raise seed now vs bootstrap 6 more months", lens = `founder`
2. Load `lenses/founder.md` (Customer / Technical / Timing / Competition)
3. Render VS prompt to `/tmp/council-1744000000-prompt.txt`
4. Claude generates tail-sampled perspective → `/tmp/council-...-claude.md`
5. Launch GPT-5.6 Sol ultra through Codex (nohup) → PID tracked
6. Fire MiniMax + Kimi curls in parallel (`&`/`wait`) → `/tmp/council-...-minimax.md`,
   `/tmp/council-...-kimi.md` (~90-180s, total)
7. ScheduleWakeup(240s), check codex, repeat if needed
8. Read all four, synthesize chairman brief

**Result:** Structured brief with four independent perspectives synthesized into
a concrete verdict + a falsifiable test for this week.

### Example 2: Default lens, quick

**User says:** `stress test this: kill the mobile app and go web-only for Q3?`

**Actions:**
1. Parse → lens defaults to `default` (Risk / Opportunity / Execution / Assumption)
2. Same flow as Example 1 but with default lens
3. If Codex returns in under 2 min, no ScheduleWakeup needed — synthesize inline

### Example 3: User-supplied inline lens

**User says:** `council this, lens: user-retention / unit-economics / distribution / defensibility: should I sunset the free tier?`

**Actions:**
1. Parse → inline lens overrides file-based lens
2. Skip lens file read; use user's 4 sub-questions directly in VS prompt
3. Continue normal flow

## Troubleshooting

### Codex exits with code 2, empty output
- **Cause:** Wrong reasoning-effort flag (`--reasoning-effort` doesn't exist).
- **Fix:** Use `--model gpt-5.6-sol -c model_reasoning_effort=ultra` (the codex skill convention for difficult council work).

### Codex exits with code 2, large input
- **Cause:** Prompt > 4KB piped via stdin.
- **Fix:** Pass the prompt as the positional argument from a file: `"$(cat $PROMPT_FILE)"` (already the pattern above). Never pipe large content via stdin to codex.

### MiniMax curl returns 401
- **Cause:** Key file is stale, has a trailing newline, or key was rotated.
- **Fix:** Check `wc -c < ~/.config/minimax/token-plan.key` (expect ~120-160 bytes, no newline). Rotate at https://platform.minimax.io/subscribe/coding-plan and re-save.

### MiniMax curl returns 429
- **Cause:** Token Plan concurrent-request ceiling hit (common if `ct-mm` team panes are also firing).
- **Fix:** Retry after 5s. If persistent, pause the team session before running the council.

### Kimi curl returns 401
- **Cause:** Key file is stale or wrapper-script key was rotated without updating `~/.config/kimi/coding-plan.key`.
- **Fix:** Check `wc -c < ~/.config/kimi/coding-plan.key` (expect ~70-80 bytes for `sk-kimi-...`, no newline). If `~/.local/bin/claude-kk` has a newer key, re-extract via the seed-from-wrapper command in Prerequisites. Otherwise rotate at https://www.kimi.com/code.

### Kimi curl returns 429 or hangs
- **Cause:** Coding Plan concurrency cap, or `claude-kk` / `ct-kk` panes are concurrently driving the same key.
- **Fix:** Retry after 5s. If persistent, pause active Kimi-backed sessions and re-fire just the Kimi curl.

### Kimi response model says `kimi-for-coding` instead of `kimi-k2.6`
- **Cause:** Not a bug — the Kimi gateway maps the request `model: "kimi-k2.6"` to the internal `kimi-for-coding` inference model. This is the same behavior documented in the `kimi-setup` skill.
- **Fix:** Ignore. The final text output and response metadata are what matter; the routing label is cosmetic.

### Codex still running after 10 minutes
- **Cause:** Unusually complex decision or an ambiguous prompt is making Sol Ultra thrash.
- **Fix:** `kill $CODEX_PID`, simplify the decision statement, and retry. If the decision is actually bounded and lower-stakes, route it to `gpt-5.6-terra` at `high` instead of weakening the council lane silently.

### Synthesis feels consensus-y, no real tension
- **Cause:** The three models converged on the modal answer — VS didn't surface a tail insight, or the decision is genuinely uncontroversial.
- **Fix:** Re-run with a different lens. If still consensus-y, trust it — not every decision has a tail insight, and a unanimous verdict is itself useful information.

### "Tail insights" all sound the same across models
- **Cause:** Decision is too abstract, models fall back to generic business-school framings.
- **Fix:** Restate the decision with concrete numbers, timeframes, and constraints. Specificity forces specificity.

## Related Skills

- **moa** — For single-prompt fanout without the VS wrapper or synthesis structure. Lighter weight.
- **ecc-santa-method** — Adversarial multi-agent verification with convergence. Use when you need a *proof* rather than a *decision*.
- **deep-sweep** — Cross-model deep analysis of code/architecture (not decisions). Orchestrates Claude + GPT-5.6 Sol for technical verification.
- **codex** — Upstream dependency. Source of truth for all `codex exec` patterns used here.
- **multi-agent-patterns** — Theory: when council-style fanout helps vs. single-agent workflows.

## Design Notes

**Why Verbalized Sampling inside each model instead of sampling across models?**
Because alignment training suppresses tail insights in *every* model uniformly.
Multi-model fanout gives you different suppressed distributions, but each
distribution is still mode-collapsed. VS asks each model to explicitly
explore *its own* tails before the council compares notes. The two techniques
compose — they don't substitute.

**Why two Chinese-lab seats (MiniMax + Kimi) instead of one?**
The two Chinese labs share country-of-origin and some training-data exposure
but not training recipe or post-training objective:
- **MiniMax-M2.7** — broad research lab, generalist post-training, high-context
  gateway; verify the exact window before relying on it.
- **Kimi K2.6** — Moonshot AI's *coding-specialized* post-train (the gateway
  literally maps requests through `kimi-for-coding`). Heavy long-context
  reasoning, code-grounded judgment.
Different post-training objectives surface different tail behaviors. On
non-code decisions Kimi's coding-tuned worldview becomes a useful adversarial
lens — it tends to value reproducibility, falsifiability, and explicit
preconditions in ways Anthropic/OpenAI/MiniMax often don't. When MiniMax and
Kimi *agree*, weight that agreement less than agreement spanning different
families (different country/lab pair). When they *disagree*, take the
disagreement seriously — it's signal that survives shared data exposure.

**Why synthesize in the same model that generated one of the perspectives?**
Self-preference bias (NeurIPS 2024) means Claude-synthesizing-Claude's-own
output will rank it higher. The mitigation here is that the synthesis prompt
explicitly labels the tail insights by source and asks for *structural*
synthesis (convergence, tension, blind spot) rather than ranking. If you want
bias-free ranking, swap the chairman role to a model outside the council —
Kimi K2.6 was the May 2026 default "outside" option for code-architectural
decisions, since it has long-context budget and didn't write the candidate
brief; alternatively use a separately configured chairman model once that lens
exists.
