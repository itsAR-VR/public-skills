---
name: skill-oracle
description: >
  Graph-routed skill discovery, activation, and quality routing. Given any
  task, queries the public-skills knowledge graph to find the most relevant
  skills, installs missing ones locally, recommends the best stack, decides
  whether a new skill is justified, and flags weak or stale skills into the
  refresh loop. Use when: asked "do we have a skill for X?", "find a skill
  for X", "what skill should I use?", "should we create a new skill?", as
  preflight routing before nontrivial work, or when a capability gap or a
  low-quality skill is detected mid-task.
argument-hint: "<task description or capability query>"
allowed-tools: Bash, Read, Write
related_skills: [find-local-skills, find-skills, skill-creator, prompt-generation, skill-judge, outcome-charter, loop-engineering, sync-skills, phase-plan, think, deep-sweep, deep-build, goal-post, ponytail, ponytail-review, ponytail-audit, ponytail-debt]
---

# skill-oracle: Graph-Routed Skill Discovery

Route the smallest set of skills that produces the best output for a task.
Three jobs, one invocation: recommend existing skills, prevent duplicate
creation, and feed weak skills into the quality loop. The bar (owner-set):
explicit, curated, model-aware, token-efficient skills — the oracle exists to
make the skill tree better every time it routes, not just to search it.

When routing a phase workflow, defer composition order to
`skills/phase-plan/references/09_PHASE_PIPELINE_PLAYBOOK.md`; this skill picks
the concrete skills, the playbook owns the cross-skill gates.

## Step 0 — Resolve the task

This skill runs in the invoking context (it is NOT forked), so the task is in
the conversation in front of you. Resolve it from whichever of these carries
it: the text after `/skill-oracle`, the Skill-tool `args`, an `ARGUMENTS:`
block, or — most reliably — the user's current request itself. The task may sit
before, after, or wrapped around the invocation, and may span multiple lines;
read the whole request, not just same-line arguments. Treat a single empty
argument slot as a non-signal, not a blocker, when the request clearly states a
task. Only when the user genuinely gave no task anywhere do you return ONE
compact line: preflight status plus "what task should I route?" Never print a
full status dump for a missing task, and never fabricate a task from stale
context.

> Why not forked: a fork is isolated from the invoking conversation, so any task
> the user phrased before/around the command (or that the harness did not inject
> as `ARGUMENTS:`) became invisible and the skill wrongly reported "no task." In-context
> execution makes the task always reachable. This is the routing-reliability fix.

## Step 1 — Locate the public-skills repo

```bash
REPO=""
for CAND in \
  "$HOME/Desktop/codespace/public-skills" \
  "$HOME/Desktop/Codespace/public-skills" \
  "$HOME/Documents/public-skills" \
  "$HOME/.codex/vendor/public-skills" \
  "$HOME/.openclaw/workspace/public-skills"; do
  if [ -d "$CAND/.git" ] && [ -f "$CAND/graphify-out/skill-graph.json" ]; then
    REPO="$CAND"; break
  fi
done
if [ -z "$REPO" ]; then
  FOUND=$(find "$HOME" -maxdepth 6 -name skill-graph.json -path "*public-skills*" \
            -not -path "*/.Trash/*" 2>/dev/null | head -1)
  [ -n "$FOUND" ] && REPO="$(dirname "$(dirname "$FOUND")")"
fi
if [ -z "$REPO" ]; then
  echo "ERROR: public-skills repo not found — run sync-skills or clone itsAR-VR/public-skills"
  return 1 2>/dev/null || exit 1
fi
echo "REPO=$REPO"
```

A candidate must have both `.git` and the graph file — `.git` alone selected
half-cloned mirrors. The `find` fallback is depth-bounded on purpose.

## Step 2 — Sync, best effort, never blocking

```bash
cd "$REPO"
DIRTY=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
if [ "$DIRTY" = "0" ]; then
  if PULL_OUTPUT=$(git pull --ff-only origin main 2>&1); then
    printf '%s\n' "$PULL_OUTPUT" | tail -3
  else
    printf '%s\n' "$PULL_OUTPUT" | tail -3
    echo "WARN: pull failed; using local graph"
  fi
else
  git fetch origin main --quiet 2>/dev/null || true
  echo "INFO: $DIRTY local file(s) modified; skipping pull, using local graph"
fi
```

Never auto-stash — this skill must not mutate the user's working tree. A
failed sync never blocks routing; the on-disk graph is good enough.

## Step 3 — Staleness check, then query

```bash
cd "$REPO" && python3 - <<'PY'
import json, os
graph = json.load(open('graphify-out/skill-graph.json'))
in_graph = {n['source_file'].split('/')[1] for n in graph['nodes']
            if n.get('source_file','').startswith('skills/')}
on_disk = {d for d in os.listdir('skills') if os.path.isfile(f'skills/{d}/SKILL.md')}
missing = sorted(on_disk - in_graph)
if missing:
    print(f"WARN: {len(missing)} skill(s) on disk but not in graph — run: "
          f"python3 scripts/add-skill-to-graph.py --all --skills-dir ./skills")
    print("      " + ", ".join(missing[:10]))
PY
cd "$REPO" && python3 scripts/query-skill-graph.py "TASK_TEXT" \
  --top 60 --precision --precision-top 8 --json
```

If more than a handful are missing, run the indexer (additive, never deletes)
before querying. Never pass `--top 0` — it slices to nothing; raise it to a
large finite number when recall matters.

## Identifier truth

Three identifiers exist per skill and they can differ: the directory name
(`skills/<dir>/`), the frontmatter `name:`, and the graph node `id`. Roughly
30 graph IDs are stale aliases (`ckm:banner-design`, `phase-implement`).
**The query result's `path` field is the only authoritative bridge to the
filesystem** — always derive the directory name from `path`, never from the
`skill` field:

```bash
DIR_NAME=$(echo "$SKILL_PATH" | awk -F/ '{print $2}')
```

## Step 4 — Select the stack

- Direct matches with score ≥ 3.0 are relevant; neighbors ≥ 2.0 add value.
- Cap at 5 skills — more is noise, and every loaded skill costs tokens.
- Prefer diversity when the task spans domains; prefer the single best skill
  when it doesn't.
- **Ponytail baseline:** for development, debugging, implementation,
  refactoring, architecture, code-review, build, PR, workflow, and agent-tooling
  tasks, reserve one stack slot for `ponytail` even when the raw graph query
  does not rank it. This makes minimum-working-solution pressure part of every
  engineering workflow. Do not add it for pure research, external writing,
  scheduling, data lookup, or user-support tasks unless the user asks for
  simplification.
- For review tasks, include `ponytail-review` alongside the normal correctness
  reviewer when the user asks what to delete, whether something is
  over-engineered, or how to simplify the diff. For repo-wide simplification
  sweeps, use `ponytail-audit`; for collecting deliberate shortcut markers, use
  `ponytail-debt`.
- Ponytail is a guardrail, not veto power: never use it to skip requested
  behavior, trust-boundary validation, security, accessibility, data-loss
  handling, tests for non-trivial logic, or real hardware calibration.
- **Reuse over creation:** if selected skills cover ~70% of the workflow,
  recommend composing them. A new skill is justified only when no skill
  covers the core workflow AND the workflow is repeated and high-value.

## Step 4.5 — Charter reuse branch

When the routed task is multi-system, repeated, event-driven, long-running,
or side-effecting, reserve one stack slot for `outcome-charter` and **load
`references/charter-routing.md` in full** — it holds the route choice
(direct / reuse-suggest / compile), the deterministic matcher invocation
against the operator-configured registry, and the authorization rules. If
none of those signals apply, keep the direct skill stack and do NOT load the
reference. Two rules survive outside the reference: never load a charter
registry into model context, and Oracle routing metadata never authorizes
execution — `charter_registry.py authorize` gates every side effect.

## Step 5 — Install missing skills (additive, idempotent)

```bash
SKILL_PATH="skills/cold-email/SKILL.md"            # from query result `path`
DIR_NAME=$(echo "$SKILL_PATH" | awk -F/ '{print $2}')
if [ -z "$DIR_NAME" ] || [ ! -d "$REPO/skills/$DIR_NAME" ]; then
  echo "SKIP: $SKILL_PATH (source missing in repo)"
else
  SEEN_REAL=""
  for CONSUMER in "$HOME/.claude/skills" "$HOME/.codex/skills" "$HOME/.agents/skills"; do
    [ -d "$CONSUMER" ] || continue
    REAL=$(cd "$CONSUMER" && pwd -P)
    case "$SEEN_REAL" in *"|$REAL|"*) continue ;; esac
    SEEN_REAL="$SEEN_REAL|$REAL|"
    if [ ! -d "$CONSUMER/$DIR_NAME" ]; then
      cp -R "$REPO/skills/$DIR_NAME" "$CONSUMER/$DIR_NAME"
      echo "INSTALLED $DIR_NAME -> $CONSUMER"
    else
      echo "EXISTS    $DIR_NAME -> $CONSUMER"
    fi
  done
fi
```

Consumer dirs are often symlinks to one shared tree — dedupe by realpath
before copying (the pattern above runs on bash 3.2). Never overwrite an
existing install; `sync-skills` owns updates.

## Step 6 — Return results

Pick the mode from intent: **team-facing** when the user is evaluating
options (short list, when-to-use per skill, suggested order, duplicate-risk
call); **agent activation** when an agent is about to execute (table of
dir-name / score / match / install status, then exact SKILL.md paths to
load). Always show directory names, never graph aliases.

## Duplicate-risk decision

| Result | Recommendation |
|---|---|
| One skill covers the core workflow | Use it. No new skill. |
| Several compose cleanly | Recommend the stack and order. New skill only if the orchestration repeats often. |
| Skills cover only fragments | Consider a wrapper skill that delegates — name the skills it delegates to. |
| Nothing scores ≥ 3.0 | A new skill may be justified — see creation routing below. |
| One-off deliverable | Do the work directly; no skill. |

**Creation routing:** when a new skill IS justified, route through
`prompt-generation` (it owns prompt architecture, per-model references, and
the Skill Rewrite Quality Gate) with `skill-creator` for package shape, and
gate with a fresh-context `skill-judge` pass before shipping. Never hand the
task to bare `skill-creator` without the generator and the judge.

## Quality-loop hook

The oracle touches more skills than anything else in the system — use that
position. When a routed or surfaced skill shows any of: undated model claims
(stale model IDs presented as current), a vague non-trigger description, a
body over ~500 lines with no references, or instructions to echo internal
reasoning — say so in one line of the reply and recommend the refresh loop
(`loop-engineering` plus the skill-refresh contract). If
`docs/research/skill-refresh/` registries exist in the repo, check whether
the skill already carries a backlog row before flagging. Routing quality
signal is part of the answer, not a side quest.

## When no match is found

Re-run with `--explain --top 10 --min-score 0.5` to see what the router
matched — user phrasing often misses indexed triggers; try a synonym. Then
check `graphify-out/GRAPH_REPORT.md` communities. Only suggest creating a
skill if the workflow will repeat; otherwise do the work directly.

## Eval mode and telemetry (load on demand)

- Task argument contains the literal token `--eval` → **load
  `references/preference-events.md` in full** and follow it (head-to-head
  stacks, user pick, preference event recording).
- Routing mode AND the user explicitly states which recommended stack they
  used (or that they used a different one) → **load
  `references/preference-events.md`** and follow its "Consider firing"
  rules to record the single-draft preference event.
- `SKILL_ORACLE_TELEMETRY` truthy in the environment → **load
  `references/telemetry.md`** and follow it (append-only observability;
  read its privacy rules before writing anything).
- None of the above → do NOT load either reference. Routing output never
  depends on them.

## Graph maintenance

```bash
cd "$REPO" && python3 scripts/add-skill-to-graph.py --all --skills-dir ./skills
```

Additive only; never delete graph nodes from this skill. Stale aliases are
fixed by aligning the offending SKILL.md `name:` with its directory, then
re-running the indexer.

## Routing boundaries

| Need | Use instead |
|---|---|
| Thin preflight task→skill routing | find-local-skills (delegates here for complex matches) |
| External skill discovery (skills.sh, ClawHub) | find-skills |
| Refreshing already-installed skills | sync-skills |
| Building the new skill | prompt-generation + skill-creator, judged by skill-judge |
| Cross-app execution contract, verified charter reuse | outcome-charter (via Step 4.5 + references/charter-routing.md) |

## Anti-patterns

- **Fabricated routing signal.** No task argument → one-line ask, never an
  invented task or a guessed recommendation. Silence beats wrong signal.
- **Trusting the `skill` field for filesystem ops.** ~30 graph IDs are stale;
  `path` is truth.
- **Recommending more than 5 skills.** Token cost is a quality bar; a stack
  the agent can't afford to load is not a recommendation.
- **Auto-stash or any working-tree mutation during sync.** Fetch-only on
  dirty trees, always.
- **Creating a skill when composition covers ≥70%.** Duplicates rot the
  graph and split future improvements across copies.
- **Skipping the staleness check before declaring "no skill exists."**
  Missing graph nodes look identical to missing capability.

## Validation

```bash
python3 scripts/validate-skill-frontmatter.py --json   # canonical — must pass
python3 scripts/query-skill-graph.py "find a skill for writing cold emails" --top 8 --precision
python3 scripts/query-skill-graph.py "ponytail review over-engineering what can we delete" --top 8 --precision
python3 skills/skill-creator/scripts/quick_validate.py skills/skill-oracle
```

Known: `quick_validate.py` exits 1 on this skill's pre-existing
`argument-hint`/`context` frontmatter keys (its allowlist is stricter than
the canonical validator). That exit is expected, not a regression — the
canonical `validate-skill-frontmatter.py` is the gate. Structural checks
only; behavioral proof is a routed task that loads the right skills. Source check for operational claims (stale-ID count, script
flags): 2026-06-10 — re-verify when the graph schema or query scripts change.
