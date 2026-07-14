# Preference Event Flow — Phase 2 Client Wiring

This skill emits one **preference event** every time it gives a routing
recommendation that the user acts on. The events are the human-judged learning
signal for Skill Oracle v2; they accumulate in the private evals repo and
feed `compute_ratings.py` (Phase 4) so the router can learn which skill stacks
actually win for which intent clusters.

This doc owns the contract between this skill and the eval repo's schema.

## What gets recorded

For each routing call, one append-only line is written to
`<eval_repo>/prefs/<github_user>.jsonl`. The line conforms to the v1 schema
documented at `<eval_repo>/docs/preference-schema.md`.

Each event captures:

| Field | What it records |
|---|---|
| `schema_version` | Always `1` in Phase 2. |
| `event_id` | UUID-v4. Unique across all shards. |
| `ts` | ISO-8601 UTC with `Z` suffix. Real wall-clock time, never frozen. |
| `user_id_hash` | `github:<github_user>` from the cached identity. |
| `task_hash` | `sha256:<hex>` over the prompt bytes. |
| `task_preview` | First 80 chars of the prompt. |
| `intent_cluster` | One of the 18 clusters in `cluster-taxonomy.json`. |
| `router_version` | `git-sha:<sha>` of the public public-skills repo at routing time. |
| `graph_version` | `skill-graph.json:sha256:<hex>` over the graph file. |
| `venue` | Always `"live"` (human-attended); `"batch"` is reserved for the nightly cron. |
| `drafter_model_a/b/c` | Model ID; defaults to `$ANTHROPIC_MODEL` or `"unknown"`. |
| `draft_a/b/c` | Stack + filter params + token/latency stats + output path/hash. |
| `winner` | `A` / `B` / `C` / `TIE` / `BOTH_BAD`. |
| `judge_kind` | Always `"human"` for client-side picks. |
| `anchor_picks` | Skills the user explicitly anchored (boost). |
| `incomplete` | True if the user abandoned mid-eval; `compute_ratings.py` skips these. |
| `reason` | Optional ≤200-char free text. |

## How drafts map to skill-oracle's output

| Skill-Oracle Output Shape | Draft Mapping |
|---|---|
| 1 recommendation (typical) | `draft_a = recommendation`; `draft_b/c = null` |
| 2 head-to-head drafts (`--eval`) | `draft_a/b = competing stacks`; `draft_c = null` |
| 3-way comparison (`--eval` future mode) | `draft_a/b/c = competing stacks` |

The "winner" field is the user's judgment:

| User signal | `winner` |
|---|---|
| User used draft A's skill stack | `A` |
| User used draft B's skill stack | `B` |
| User used draft C's skill stack | `C` |
| User picked something neither drafted | `BOTH_BAD` |
| User said both/all were equally good | `TIE` |
| User abandoned mid-flow | `BOTH_BAD` with `--incomplete` |

## Eval-repo resolution order

1. `$SKILL_ORACLE_EVAL_REPO` env var (must exist on disk).
2. `~/.openclaw/public-skills-evals-private/` — the canonical client clone.
3. `~/Desktop/Codespace/public-skills-evals-private/` — dev fallback.

If none of these exist, the recorder skips writing and warns to stderr.
Routing recommendations still flow to the caller normally.

## Identity

The cached identity at `~/.openclaw/skill-oracle/identity.json` is required.
It's created by `scripts/bootstrap-client.sh` inside the eval repo on each
new machine. The recorder reads `github_user` from this file and uses it for
both `user_id_hash` and the shard path (`prefs/<github_user>.jsonl`).

If the identity file is missing, the recorder warns and exits 0 without
writing anything. The user is asked to run `bootstrap-client.sh`.

## Cluster classification

`scripts/classify_cluster.py` does keyword-weighted overlap between the prompt
and each cluster's `name + description + example_prompts + anchor_skills` in
`cluster-taxonomy.json`. The highest-scoring cluster wins; if no cluster
scores above the confidence floor, the prompt routes to `catch-all`
(the taxonomy's blessed fallback).

This classifier is intentionally simple — the v1 goal is to start
`n_human_picks` growing from 0. A higher-fidelity LLM classifier can replace
the keyword model without changing the event schema.

## Output file artifacts

The strict validator (`validate-event-schema.py --strict`) hashes the file
at each draft's `output_text_path` and compares to `output_hash`. So the
recorder writes one rendered text artifact per draft at
`<eval_repo>/outputs/evt-<id>-<a|b|c>.txt`. The file is a stable,
human-readable rendering of the draft's skill stack — sufficient for
auditability and for the hash to be reproducible.

## Atomicity

- Output files are written via `tempfile` + `os.replace` for crash safety.
- The JSON line is appended via `O_APPEND` + `fsync` for line-atomicity
  on POSIX. No locking is needed — `write(2)` to an `O_APPEND` fd of a
  single short line is atomic across processes.
- On any I/O failure, the recorder warns to stderr and exits 0 — the
  routing recommendation is never blocked.

## Determinism caveat

The schema doc's determinism requirement (canonical JSON, sorted keys, etc.)
applies to **batch reprocessing** of recorded events. Recording events
themselves uses real wall-clock time for `ts` and a fresh UUID for
`event_id` — those are the only non-deterministic fields. Hashes, sort
orders, and field shapes are deterministic.

## Validating locally

After recording, you can confirm your shard is schema-clean:

```bash
cd "$SKILL_ORACLE_EVAL_REPO"   # or ~/.openclaw/public-skills-evals-private
python3 scripts/validate-event-schema.py --strict
```

This is what CI runs on every push to the eval repo. If `--strict` fails,
fix the event-emission code, not the validator.

## Phase boundary

Phase 2 (this PR) **records** events on every routing call where the user
acts on the recommendation. Phase 3 adds the `--eval` flag for explicit
side-by-side comparisons. Phase 4 wires `compute_ratings.py` so the events
actually update the ELO/Bradley-Terry tables. The recording contract
established here is forward-compatible with all three phases.
