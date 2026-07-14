# skill-oracle — Eval Mode & Preference Events

Load this file ONLY when the task argument contains the literal token `--eval`,
or when the user has explicitly stated which recommended stack they used and a
preference event should be recorded. Do not load for normal routing.

## Mode Detection (Phase 3+)

Two execution modes, set by parsing the user's input:

- **Routing mode** (default): one ranked recommendation. UX unchanged from Phase 2.
- **Eval mode** (`--eval` flag): present a head-to-head binary comparison of
  two competing stacks, capture the user's pick, then record a preference
  event with `judge_kind: human` and K-factor 32 (4× more impact on ratings
  than the nightly silver labels).

To detect: parse the user's task argument for the literal token `--eval`
(case-sensitive). If present:

1. Strip `--eval` from the task text.
2. Set `MODE=eval` for the rest of this invocation.
3. Follow the eval-mode branches in Step 4.5, Step 6.6, and Step 7.1.

Otherwise: `MODE=routing` (default behavior, all eval-mode steps are skipped
except the soft trigger condition in Step 7.1).



### Step 4.5 — Generate competing candidates (MODE=eval only)

Skip this step when MODE=routing.

When MODE=eval, instead of picking ONE stack, pick TWO competing stacks that
are *plausibly different* but *both reasonable*. The goal is to surface user
preference signal, not to ask "which is obviously better." Avoid stacks where
the user would say "well A, obviously" — that's not informative.

Three valid ways to pair Stack A vs Stack B:

| Pairing | Stack A | Stack B | What we learn |
|---|---|---|---|
| Filter mode | heuristic, default params | llm, default params | Does LLM filtering beat heuristic for this prompt? |
| Composition breadth | top 2 highest-scoring skills | top 1 + 2 complementary neighbors | Does depth or breadth win for this task? |
| Sequencing | skill-X → skill-Y | skill-Y → skill-X | Does ordering matter? |

Default pairing: **filter mode** (heuristic vs llm). It's the most actionable
signal for the router's fusion-weight tuner downstream.

Record the (Stack A, Stack B, filter_mode_A, filter_mode_B, params_A, params_B)
tuple in memory for Step 6.6 and Step 7.1.



## Step 6.6 — Eval mode head-to-head prompt (MODE=eval only)

Skip this step when MODE=routing.

After Step 6's standard output, append a head-to-head section that asks the
user to pick between Stack A and Stack B (built in Step 4.5). Use this
template literally — the structure matters because record_event.py downstream
parses the user's reply:

```
## Head-to-Head Eval

You passed `--eval` — here are two competing stacks for the same task.
Pick A or B (or BOTH_BAD if neither helps).

**Option A** (filter_mode: <heuristic|llm>, params: <params_A>)
- <skill-1>
- <skill-2>
- <skill-3>
Rationale: <one-line reason A is plausible>

**Option B** (filter_mode: <heuristic|llm>, params: <params_B>)
- <skill-4>
- <skill-5>
- <skill-6>
Rationale: <one-line reason B is plausible>

Reply with one of: `A`, `B`, `BOTH_BAD`, `incomplete`.
Optionally append a short reason after the letter (≤200 chars), e.g.
`A — leads with research instead of jumping to copy`.
```

Then STOP and wait for the user's reply. Do not proceed to Step 7 or any
follow-on work until the user has answered. The reply is the binary
preference signal that drives ratings learning.



## Step 7 — PREFERENCE EVENT (Phase 2: human-judged learning signal)

After the routing recommendation is returned AND the user takes (or skips) a
recommended skill, record one preference event to the private evals repo. This
is what starts the `n_human_picks` counter in `ratings.json` growing — every
event is weighted 4× heavier than the nightly silver labels (K-factor 32 vs 8).

The event captures: which skills were drafted, which one the user actually
used, what cluster the prompt belonged to, and the router/graph versions at
recommendation time. See
[`preference-event-flow.md`](preference-event-flow.md)
for the complete contract.

### Invocation

```bash
python3 "$REPO/skills/skill-oracle/scripts/record_event.py" \
  --prompt    "<the user's task text>" \
  --drafts    '[["skill-a","skill-b"],["skill-c"]]' \
  --winner    A \
  --reason    "optional ≤200 chars why this draft won"
```

Mapping skill-oracle's output to drafts:

- **Single-recommendation mode** (typical): pass one entry in `--drafts` —
  the recommended stack. Set `--winner A` if the user used it, `--winner BOTH_BAD`
  if they didn't, or pass `--incomplete` if they abandoned mid-flow.
- **Head-to-head eval mode** (`--eval` flag, Phase 3+): pass 2-3 entries — one
  per drafter configuration. Set `--winner` to the letter the user picked.

### Eval-repo resolution

The recorder resolves the local eval-repo clone in this order:

1. `$SKILL_ORACLE_EVAL_REPO` if it exists on disk.
2. `~/.openclaw/public-skills-evals-private/` (canonical client clone).
3. `~/Desktop/Codespace/public-skills-evals-private/` (dev fallback).

The cached GitHub identity at `~/.openclaw/skill-oracle/identity.json` is
required and is created by `scripts/bootstrap-client.sh` in the eval repo.

### Graceful degradation

Every prerequisite is checked, and missing ones warn to stderr and exit 0
rather than blocking the routing recommendation:

| Prerequisite missing | Behavior |
|---|---|
| `identity.json` not bootstrapped | warn, skip write, suggest `bootstrap-client.sh` |
| Eval-repo clone not found anywhere | warn, skip write |
| `<eval_repo>/prefs/` directory absent | warn, skip write |
| Disk full / permission denied on shard | warn, skip write |
| `--winner` references a null draft | warn, refuse to emit invalid event |

The routing recommendation is always returned to the caller; the event
recording layer is observability, not a critical path.

### Output

Each event becomes one JSON line appended to
`<eval_repo>/prefs/<github_user>.jsonl` and one rendered text artifact per
draft at `<eval_repo>/outputs/evt-<id>-<a|b|c>.txt` (the strict validator
hashes those files). Every line passes
`<eval_repo>/scripts/validate-event-schema.py --strict`.

## Step 7.1 — When to invoke record_event.py (activation triggers — Phase 3)

Step 7 documents the CLI. This step tells Claude exactly *when* to fire it.

### Always fire — eval mode resolution

When `MODE=eval` AND the user has replied to the Step 6.6 prompt with one of
`A`, `B`, `BOTH_BAD`, or `incomplete`: this IS the binary preference signal.
You MUST record it. Construct the call from the in-memory stacks (built in
Step 4.5) and the user's reply:

```bash
python3 "$REPO/skills/skill-oracle/scripts/record_event.py" \
  --prompt    "<the user's task text, --eval stripped>" \
  --drafts    '[["<Stack A skills>"],["<Stack B skills>"]]' \
  --winner    <A | B | BOTH_BAD>   # OR pass --incomplete
  --reason    "<the user's stated reason, if any, ≤200 chars>"
```

Fire this BEFORE writing your final user-facing acknowledgment. If the
recorder warns + exits 0 (graceful-degradation path), continue. If it
crashes, log the error in your reply but do not block the user.

### Consider firing — routing mode with explicit signal

When `MODE=routing` AND the user explicitly states in the same conversation
which recommended skill they used (e.g., "I used cold-email + customer-research
like you suggested" or "I went with a different stack — used X instead"):

```bash
python3 "$REPO/skills/skill-oracle/scripts/record_event.py" \
  --prompt    "<original task text>" \
  --drafts    '[["<recommended stack you returned>"]]' \
  --winner    <A or BOTH_BAD>
```

Single-draft event, `winner=A` if they followed the recommendation, `BOTH_BAD`
if they used something else.

### Never fire when

- The user invokes the skill but doesn't engage with the recommendations
  ("interesting, let me think about it" → ambiguous; skip).
- The user pivots away from the original task before deciding ("actually
  let's do something different" → skip).
- You cannot confidently infer the user's pick from conversation context.
- The user is asking a meta-question about the skill itself rather than
  using it ("what does this skill do?" → skip).

Silence is better than a fabricated event. K-factor 32 means each event has
4× the impact of a silver label — wrong signal is worse than no signal.

### Sanity check before firing

Before invoking the recorder, confirm:

- The `--prompt` is the original task text, not your paraphrase of it
- The `--drafts` JSON is well-formed (each entry a list of skill directory
  names, exactly matching what you returned in Step 6)
- The `--winner` letter matches an actual draft index (A=0, B=1, C=2)
- You're NOT recording an event for a skill-oracle meta-invocation or test

