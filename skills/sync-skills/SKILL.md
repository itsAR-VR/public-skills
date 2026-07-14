---
name: sync-skills
description: >
  Sync skills between local skill directories and the public-skills GitHub repo,
  with the live repo as the source of truth. Routine sync is pull-dominant:
  refresh upstream packs, pull live skills, and let the live repo win over local
  on conflict (a diff snapshot is saved first). A genuinely new or improved local
  skill is kept locally AND raised as a PR, never direct-pushed to main. Use when
  the user says "sync skills", "push skills", "pull skills", "update skills",
  "publish skills", "get latest skills", or "sync public-skills". Replaces the old
  push-skills and pull-skills as a single unified workflow.
metadata:
  author: podhi
  version: 2.1.0
related_skills: [find-local-skills, skill-creator, find-skills]
---

# sync-skills

Bidirectional sync between local skill directories and the `public-skills` GitHub repo.

## Source-of-Truth Model

```
Upstream skill packs             ← ECC, npx skills packs, repo packs
        ↓  guarded refresh
~/.claude/skills/                ← primary local skill directory
        ↕  bidirectional sync
GitHub: itsAR-VR/public-skills    ← shared canonical repo
        ↓  distribute
~/.codex/skills/                 ← Codex consumer
~/.agents/skills/                ← Agents consumer
```

**Precedence: the live `public-skills` repo is the source of truth.** Routine
sync is pull-dominant. Pull live, then let live win over local on any conflict
(a diff snapshot is saved first under `~/.codex/skill-sync-diffs/`, so nothing
is lost and you can recover a clobbered local edit). A skill that is genuinely
new or improved locally is preserved AND raised as a PR to `public-skills` so
everyone gets the better version. Changes reach the shared repo through a PR;
never direct-push `main`.

**Key rule: never use corpus-wide `--delete` in rsync.** Both directions are
additive-only for unmanaged skills. Managed upstream skills are different:
when a skill name is owned by a marketplace manifest or git upstream, the
upstream copy replaces the old repo/local copy after a diff snapshot is saved.

**Pack source repos are not skills.** Full upstream clones such as
`everything-claude-code/` are refresh inputs only. Keep them out of the
loader-facing skill tree when possible, and always exclude those source repo
directories from public-skills rsync. Sync the flattened/generated skill
directories instead.

## When to Use

- User says "sync skills", "push skills", "pull skills", "update skills"
- After creating a new skill with `skill-creator`
- After editing or updating an existing skill
- Before sharing skills across machines
- When another machine has pushed new skills to the repo

## Platform Detection

The skill works on both macOS and Linux. Detect paths at the start:

```bash
# Detect public-skills repo location
if [ -d "$HOME/Desktop/Codespace/public-skills" ]; then
  REPO="$HOME/Desktop/Codespace/public-skills"          # macOS
elif [ -d "$HOME/.openclaw/workspace/public-skills" ]; then
  REPO="$HOME/.openclaw/workspace/public-skills"         # Linux
else
  echo "ERROR: public-skills repo not found"; exit 1
fi

# Primary local skills directory
SKILLS="$HOME/.claude/skills"

# Consumer directories (distribute to these after sync)
CONSUMERS=("$HOME/.codex/skills" "$HOME/.agents/skills")

# Resolve symlinks before distribution. On some machines ~/.claude/skills,
# ~/.codex/skills, and ~/.agents/skills all point at the same real directory.
# Keep only unique consumers that are not the primary local skills dir.
dedupe_consumers() {
  python3 - "$SKILLS" "${CONSUMERS[@]}" <<'PYEOF'
import os, sys
from pathlib import Path

primary = os.path.realpath(Path(sys.argv[1]).expanduser())
seen = {primary}
for raw in sys.argv[2:]:
    path = Path(raw).expanduser()
    real = os.path.realpath(path)
    if real in seen:
        print(f"[sync-skills] skip duplicate consumer: {path} -> {real}", file=sys.stderr)
        continue
    seen.add(real)
    print(path)
PYEOF
}
mapfile -t CONSUMERS < <(dedupe_consumers)
```

## Workflow

### Step 1 — Pull remote into local repo
```bash
cd "$REPO" && git pull --ff-only origin main
```
If `--ff-only` fails, try `git pull --rebase origin main`.

### Step 1.4 — Refresh git-backed skill upstreams (dirty-safe)

Some high-value skill packs are installed as real git repositories instead of
marketplace meta-skills. The shared source location is:

```bash
UPSTREAMS_ROOT="$HOME/.claude/skills-upstreams"
```

The currently managed git upstreams include `claude-code-tools`, `ecc`,
`foxai_skills`, `gitnexus`, `impeccable`, `lastXdays`, `openclaw`,
`opendirectory`, and `taste-skill`. They are not captured by the
`manifest.txt` + `scripts/update.sh` marketplace discovery below, so refresh
them before the additive rsync.

`scripts/refresh-skill-upstreams.py` fetches each clean upstream repo, skips
dirty repos instead of stashing or dropping work, runs source-specific
materializers where needed, then replaces the exported skills in both
`$SKILLS` and `$REPO/skills`. It writes a timestamped diff before each
replacement under `$HOME/.codex/skill-sync-diffs/`.

```bash
python3 "$REPO/scripts/refresh-skill-upstreams.py" \
  --repo "$REPO" \
  --local-skills "$SKILLS" \
  --upstreams-root "$UPSTREAMS_ROOT"
```

This lane intentionally excludes `~/.claude/plugins/marketplaces/*`. Claude
plugin marketplaces live outside the skill tree and need a plugin-marketplace
sync, not skill rsync, unless a specific plugin exports skills into `$SKILLS`.

### Step 1.5 — Refresh marketplace skill packs (non-fatal, auto-discovering)

Some skills are managed by external marketplaces (e.g., the Corey Haines
Marketing Skills pack and the Matt Pocock Skills pack, both via `npx skills`).
Refresh them here so any upstream updates land in `$SKILLS` *before* the
additive rsync below picks them up and propagates them into the repo and
other consumers.

A skill is treated as a marketplace meta-skill when it has both a
`manifest.txt` (the names it manages) and `scripts/update.sh`. Discovery is
automatic — drop a new pack into `$SKILLS/<pack-name>/` with those two files
and Step 1.5 picks it up next sync. No edits to this skill required.

```bash
echo "[sync-skills] Discovering marketplace meta-skills..."
for manifest in "$SKILLS"/*/manifest.txt; do
  [ -f "$manifest" ] || continue
  pack_dir="$(dirname "$manifest")"
  pack_name="$(basename "$pack_dir")"
  update_script="$pack_dir/scripts/update.sh"
  if [ -x "$update_script" ]; then
    echo "[sync-skills] → refreshing $pack_name"
    bash "$update_script" || echo "[sync-skills] $pack_name refresh non-fatal failure — continuing"
  else
    echo "[sync-skills] $pack_name has manifest.txt but no executable scripts/update.sh — skip"
  fi
done
```

This step is intentionally non-fatal. If `npx` is unavailable or the registry
is unreachable, sync continues with whatever marketplace state currently
exists locally.

A pack's `update.sh` may also deploy artifacts that skill-rsync does not carry.
For example `cursor-team-kit-skills-pack` runs a `deploy.sh` that symlinks its
subagents into `~/.claude/agents/` (`.md`) + `~/.codex/agents/` (`.toml`) and
injects a delimited rules block into the global `CLAUDE.md` / `AGENTS.md`. Since
Step 1.5 runs every sync, those agents + rules are re-asserted each time
(idempotent, and deploy-only/offline-safe while the pack is pinned). Such packs
may fetch a pinned git subtree (`gh`/`curl`) instead of using `npx`.

### Step 1.6 — Adopt marketplace-managed replacements

`npx skills add ... --copy` writes the latest marketplace copy into `$SKILLS`.
For names claimed by a repo `manifest.txt`, that upstream marketplace copy
should replace the old repo copy. The replacement is scoped to manifest-owned
names only, so local edits to non-marketplace skills survive untouched. A
diff is saved before each replacement under `$HOME/.codex/skill-sync-diffs/`.

```bash
python3 "$REPO/scripts/adopt-marketplace-skill-updates.py" \
  --repo "$REPO" \
  --local-skills "$SKILLS"
```

To add another marketplace pack: drop a `manifest.txt` in its meta-skill
directory listing the names it owns. Step 1.6 picks it up automatically.

### Step 2 — Peer-merge repo ↔ local (3-way, base-aware, conflict-blocking)

Replaces the old additive-rsync pair (Steps 2 + 3 historically). `tri-merge.py`
in peer mode does a real 3-way merge between the repo and the loader-facing
mirror using a saved base snapshot of the last clean sync. Files that diverged
on only one side flow through; both-side text edits get auto-merged when they
touch different lines; same-line collisions are surfaced as conflict artifacts
and **block push**. SKILL.md conflicts never propagate — the staging tree gets
the base copy so the loader stays valid.

```bash
BASE="$HOME/.codex/skill-sync-base/skills"
STAGING="$HOME/.codex/skill-sync-staging/$(date +%Y%m%dT%H%M%SZ)"
SNAPSHOT="$HOME/.codex/skill-sync-conflicts/$(date +%Y%m%dT%H%M%SZ)"

if ! python3 "$REPO/scripts/tri-merge.py" peer \
      --left "$REPO/skills" \
      --right "$SKILLS" \
      --base "$BASE" \
      --staging "$STAGING" \
      --snapshot "$SNAPSHOT"; then
  echo "ERROR: tri-merge surfaced conflicts at: $SNAPSHOT"
  echo "Each conflicted file has left/, right/, base/, and merged/ artifacts."
  echo "Resolve manually in either tree, then re-run sync-skills."
  exit 1
fi
```

**First-sync bootstrap.** If `$BASE` doesn't exist (first run after this skill
landed), tri-merge falls into no-base policy: any file present on both sides
with differing content surfaces as a conflict. Pre-existing harmless divergence
(mtime drift, formatting tweaks) may surface here. To bootstrap, run a
`--dry-run` style inspection first, resolve any divergences manually by picking
a side (typically the repo, since it's the committed state), then proceed.

After tri-merge succeeds, propagate the staging tree to both peers atomically.
The staging tree IS the union — additive-only rsync would no longer be correct,
because tri-merge has already decided which deletions are intentional:

```bash
rsync -a --copy-links --delete \
  --exclude='.DS_Store' --exclude='.system' --exclude='.git' \
  --exclude='.venv' --exclude='__pycache__' --exclude='*.pyc' \
  --exclude='node_modules' \
  --exclude='everything-claude-code/' --exclude='learned/' \
  "$STAGING/" "$REPO/skills/"

rsync -a --copy-links --delete \
  --exclude='.DS_Store' --exclude='.system' --exclude='.git' \
  --exclude='.venv' --exclude='__pycache__' --exclude='*.pyc' \
  --exclude='node_modules' --exclude='learned/' \
  --exclude='everything-claude-code/' \
  "$STAGING/" "$SKILLS/"
```

The base snapshot is refreshed at the very end (Step 9.5) — only after a
successful commit, push, and consumer fan-out. That way, a crash mid-sync
leaves the previous base intact and the next sync re-merges from scratch.

### Step 4 — Repair/report SKILL.md metadata issues before validation

After all repo/local merges, inspect loader-facing `SKILL.md` metadata before
graph generation or validation. The script is report-only: it identifies
missing frontmatter, malformed YAML, missing `name`, missing `description`,
and empty required fields. It must not invent or auto-fill descriptions.

```bash
cd "$REPO"
python3 scripts/validate-skill-frontmatter.py --skills-dir "$REPO/skills" --json
```

If this reports findings, patch the listed `SKILL.md` files directly before
continuing. For missing or empty `description`, read the skill body and write a
real description that explains when to use the skill. For malformed YAML, fix
the exact frontmatter syntax, usually by quoting the offending scalar. Then
rerun Step 5. Do not push while this report still has findings.

This is a repair-before-validate gate, not advisory output. If findings are
present, stop the sync flow, repair the exact files in the merged staging/repo
tree, then rerun the report and validator. Do not let broken frontmatter reach
Codex or Claude Code, because both loaders warn on every startup/session.

### Step 5 — Validate SKILL.md frontmatter and required fields (blocks push)

Claude Code and Codex CLI both require every SKILL.md to begin with a
`---`-delimited YAML block containing at minimum `name:` and `description:`.
Malformed YAML, missing keys, and empty required values make the loader skip
the skill or print warnings. Validate after any agent repairs and before
graph/push:

```bash
cd "$REPO"
if ! python3 scripts/validate-skill-frontmatter.py --skills-dir "$REPO/skills"; then
  echo "ERROR: One or more SKILL.md files still have invalid frontmatter. Push blocked."
  echo "Each SKILL.md must start with valid YAML like:"
  echo "  ---"
  echo "  name: <skill-name>"
  echo "  description: <one-line description>"
  echo "  ---"
  exit 1
fi
```

### Step 6 — Update the skill graph (incremental, no rebuild)

Add any new skills to the knowledge graph:

```bash
cd "$REPO" && python3 scripts/add-skill-to-graph.py --all
```

This appends new skill nodes + edges to `graphify-out/skill-graph.json` (the skill
registry — distinct from graphify's full AST graph at `graphify-out/graph.json`).
Skills already in the graph are skipped. No rebuild needed.

### Step 7 — Security scan (blocks push on HIGH/CRITICAL)

Run the static security scanner on the merged skills before pushing:

```bash
cd "$REPO"
if ! python3 scripts/scan-skills-security.py --skills-dir "$REPO/skills" --fail-on HIGH; then
  echo "ERROR: Security scan found HIGH or CRITICAL findings. Push blocked."
  echo "Fix the findings or update the whitelist in scripts/scan-skills-security.py"
  exit 1
fi
echo "Security scan passed — no HIGH or CRITICAL findings."
```

### Step 7.5 — Hook resolvability check (non-fatal, environment-only)

`sync-skills` doesn't own `~/.claude/settings.json`, but a stale hook command in
that file produces a `MODULE_NOT_FOUND` crash on every Bash/Edit/Write tool call
— and the symptom (a flood of `PreToolUse:Bash hook error` lines in the
transcript) is easy to confuse with a sync problem. This step is a read-only
check that flags the drift so the agent knows to re-run
`setup-skill-packs` Phase 11 (which has an idempotent realignment block).

The check is intentionally non-fatal: a broken hook path on this machine
should not block pushing skill changes that other machines depend on.

```bash
SETTINGS="$HOME/.claude/settings.json"
[ -f "$SETTINGS" ] && python3 - "$SETTINGS" <<'PYEOF'
import json, re, sys
from pathlib import Path

data = json.loads(Path(sys.argv[1]).read_text())
runner_re = re.compile(r'(/[^"\s]+run-with-flags\.js)')
broken = []
total = 0
for event, entries in (data.get("hooks") or {}).items():
    for entry in entries:
        matcher = entry.get("matcher", "*")
        for hook in entry.get("hooks", []):
            cmd = hook.get("command", "")
            for path in runner_re.findall(cmd):
                total += 1
                if not Path(path).exists():
                    broken.append((event, matcher, path))

if broken:
    print(f"[sync-skills] WARN: {len(broken)} of {total} hook script(s) do not resolve:")
    for event, matcher, path in broken:
        print(f"  - {event}/{matcher}: {path}")
    print("[sync-skills] Fix: re-run setup-skill-packs Phase 11 — its 'Realign")
    print("[sync-skills] settings.json hook paths' block rewrites every reference")
    print("[sync-skills] to the canonical $ECC_REPO (currently ~/.codex/skill-packs/")
    print("[sync-skills] everything-claude-code). Idempotent; writes a backup first.")
elif total:
    print(f"[sync-skills] hook resolvability: OK ({total} script(s) resolved)")
else:
    print("[sync-skills] hook resolvability: no run-with-flags.js refs in settings.json")
PYEOF
```

### Step 7.6 — Codex startup hygiene repair (non-fatal, environment-only)

`sync-skills` can surface skill-pack drift that is not itself a skill file:
duplicated Codex ECC role definitions, dead local MCP entries, or an
OAuth-incompatible GitHub MCP created by a plugin refresh. This step runs the
same backup-first repair used by `setup-skill-packs`. It intentionally keeps
the OpenAI-curated GitHub connector enabled and only changes user-level Codex
config when the known warning patterns are present. Supported scalar capacity
keys under `[agents]` are preserved; the repair only removes duplicated ECC
agent aliases plus the known dead MCP/plugin entries.

```bash
if [ -d "$HOME/.codex" ] && [ -f "$REPO/scripts/repair-codex-startup-config.py" ]; then
  python3 "$REPO/scripts/repair-codex-startup-config.py" \
    --codex-home "$HOME/.codex" \
    --apply || echo "[sync-skills] Codex startup hygiene repair failed non-fatally"
else
  echo "[sync-skills] Codex startup hygiene skipped"
fi
```

If Codex still prints `context7 invalid_grant`, clear the stale OAuth grant
after sync with `codex mcp logout context7 || true`. Do not auto-login Context7
inside skill sync; it is a user-specific OAuth action.

### Step 7.7 — Graphify workflow hygiene (repo-local, idempotent)

Graphify git hooks live in `.git/hooks`, so they do not travel through Git. Run
the repair helper after pulling public-skills updates to keep existing clones
aligned with the generated-output policy and the current hook template:

```bash
if [ -f "$REPO/scripts/repair-graphify-workflow.py" ]; then
  python3 "$REPO/scripts/repair-graphify-workflow.py" \
    --repo "$REPO" \
    --apply || echo "[sync-skills] Graphify workflow repair failed non-fatally"
fi
```

### Step 8 — Commit on a branch and open a PR (never direct-push main)
Local skill changes reach the shared repo through review, not a direct `main`
push. Branch, push the branch, open a PR.
```bash
cd "$REPO"
GRAPH_ROUTER_FILES=(
  graphify-out/skill-graph.json
  graphify-out/SKILL_GRAPH_REPORT.md
  graphify-out/query-regression-fixtures.json
  graphify-out/synonyms.json
)

# Do not broadly add graphify-out/. The full Graphify repo graph
# (graphify-out/graph.json + GRAPH_REPORT.md) is generated branch-local churn
# and should only be committed in a dedicated full-graph refresh.
if [ -n "$(git status --porcelain -- skills "${GRAPH_ROUTER_FILES[@]}")" ]; then
  BRANCH="chore/skills-sync-$(date +%Y%m%dT%H%M%SZ)"
  git switch -c "$BRANCH"
  git add skills/
  for path in "${GRAPH_ROUTER_FILES[@]}"; do
    [ -e "$path" ] && git add "$path"
  done
  git commit -m "chore(skills): sync [$(date +%Y-%m-%d)]"
  git push -u origin "$BRANCH"
  gh pr create --fill --base main --head "$BRANCH"
  echo "Opened a sync PR. It reaches main through review, not a direct push."
else
  echo "No changes to push — repo already in sync"
fi
```

If a full Graphify refresh is intentional, do it from a clean merged tree on its
own branch + PR:

```bash
git switch -c "chore/graphify-full-refresh-$(date +%Y%m%d)"
git add graphify-out/graph.json graphify-out/GRAPH_REPORT.md
git commit -m "chore(graphify): refresh full repo graph"
git push -u origin HEAD && gh pr create --fill --base main
```

### Step 9 — Distribute to other unique consumers (additive, no --delete)
```bash
for CONSUMER in "${CONSUMERS[@]}"; do
  if [ -d "$CONSUMER" ]; then
    rsync -av --copy-links \
      --exclude='.DS_Store' --exclude='.system' \
      --exclude='everything-claude-code/' \
      "$REPO/skills/" "$CONSUMER/"
  fi
done
```

### Step 9.5 — Refresh the merge base snapshot

Now that this sync succeeded end-to-end, snapshot the merged state as the base
for the *next* sync's 3-way merge. Done atomically (write to `.new`, then
rename) so a crash between commit and base refresh leaves the previous base
intact — the next sync would re-merge from scratch rather than seeing a
half-written base. The manifest records the tree hash, the repo HEAD at sync
time, the script version, and a timestamp; tri-merge can use these to detect
"the script changed and the base may no longer be trustworthy" in the future.

```bash
python3 "$REPO/scripts/tri-merge.py" refresh-base \
  --source "$STAGING" \
  --base "$BASE" \
  --manifest "$BASE/../base-manifest.json" \
  --repo-head "$(cd "$REPO" && git rev-parse --short HEAD)"
```

Skip this step if you exited early (validation failed, security scan blocked,
etc.) — the base must only advance after a *fully clean* sync.

### Step 10 — Confirm
```bash
echo "claude: $(ls "$SKILLS" | wc -l) skills"
for CONSUMER in "${CONSUMERS[@]}"; do
  if [ -d "$CONSUMER" ]; then
    echo "$(basename "$(dirname "$CONSUMER")"): $(ls "$CONSUMER" | wc -l) skills"
  fi
done
echo "repo:   $(ls "$REPO/skills" | wc -l) skills"
```
All unique loader-facing counts should match. If no consumers print, the
configured consumer paths resolve to the same real directory as `$SKILLS`, so
distribution was already complete.

## Quick Summary

```
pull remote → refresh git-backed upstreams (with overlays) → refresh marketplace packs → adopt managed replacements (with overlays) → tri-merge peer (3-way merge, blocks on conflict) → propagate staging to both peers → repair/report metadata issues → validate frontmatter/required fields → graph update → security scan → hook resolvability check → Codex startup hygiene → Graphify workflow hygiene → commit on a branch + open PR → distribute to unique consumers → refresh merge base
```

## Merge model

The peer reconciliation between repo and `~/.claude/skills` is a real 3-way
merge via `scripts/tri-merge.py`, not bidirectional rsync. The base snapshot at
`~/.codex/skill-sync-base/` represents the last clean sync state; tri-merge
uses it to distinguish "added on one side" from "concurrent edit," and to
auto-merge non-overlapping text changes via `git merge-file`. Same-line
conflicts in any SKILL.md are surfaced as artifacts under
`~/.codex/skill-sync-conflicts/` and **block push** — the staging tree is left
holding the base copy so the loader is never broken by conflict markers.

For managed upstream skills (ECC, opendirectory, lastXdays, marketplace
packs), `refresh-skill-upstreams.py` and `adopt-marketplace-skill-updates.py`
also apply per-skill overlays from `scripts/skill-overlays/<name>.yaml`. These
are local normalizations (descriptions, frontmatter fixes) that survive every
upstream refresh; without them, broken upstream YAML re-clobbers local repairs
on every sync.

Preserve or reapply the marked
`local:browser-harness-computer-use-fallback` block at the end of
`browser-harness/SKILL.md`.

## Troubleshooting

### git pull --ff-only failed
- **Cause:** Local repo has diverged
- **Fix:** `cd "$REPO" && git pull --rebase origin main`

### Permission denied on git push
- **Cause:** SSH key not loaded or HTTPS auth expired
- **Fix:** Run `gh auth login` or `ssh-add`

### Skill counts don't match after sync
- **Cause:** A consumer dir has extra files (e.g., .DS_Store counted)
- **Fix:** Compare with `diff <(ls "$SKILLS" | sort) <(ls "$CONSUMER" | sort)`

### Consumer count missing for Codex or Agents
- **Cause:** `~/.claude/skills`, `~/.codex/skills`, and/or `~/.agents/skills` are symlinks to the same real directory.
- **Fix:** This is expected. The workflow dedupes consumers by real path and skips redundant rsyncs.

### Duplicate `ecc-*` Codex role warnings after sync
- **Cause:** Codex is loading `~/.codex/agents/ecc-*.toml` and duplicate `[agents.<alias>].config_file` entries in `~/.codex/config.toml`.
- **Fix:** Re-run Step 7.6 or `python3 "$REPO/scripts/repair-codex-startup-config.py" --codex-home "$HOME/.codex" --apply`.

### `codex mcp list` rejects `[agents]` scalar values
- **Cause:** Older Codex builds can misparse modern config and report supported `[agents]` capacity keys like `max_threads`, `max_depth`, and `job_max_runtime_seconds` as malformed roles.
- **Fix:** Run `which -a codex` and prefer `~/.local/bin/codex` when present; older Homebrew Codex builds may be first on PATH. Then re-run Step 7.6 to clean duplicate `ecc-*` alias tables and stale MCP/plugin entries. Do not strip supported `[agents]` capacity keys.

### `MCP startup incomplete` mentions context7, github, inngest-dev, or pencil
- **Cause:** Stale Context7 OAuth, unsupported GitHub MCP OAuth, or local-only MCP entries on a machine without the service/binary.
- **Fix:** Run Step 7.6. Then run `codex mcp logout context7 || true` if Context7 reports `invalid_grant`. Re-add `inngest-dev`/`pencil` only when those local targets exist.

### Want to delete a skill permanently
- Delete from `~/.claude/skills/<name>/` AND `public-skills/skills/<name>/`
- Commit the deletion on a branch and open a PR: `cd "$REPO" && git switch -c chore/skills-delete-<name> && git add -A skills/ && git commit -m "chore(skills): remove <name>" && git push -u origin HEAD && gh pr create --fill --base main` (live repo is source of truth, so the deletion propagates to everyone on next sync once merged)

## Related Skills
- **skill-creator**: Create a new skill from scratch
- **find-local-skills**: Search installed skills
- **find-skills**: Search the clawhub registry
