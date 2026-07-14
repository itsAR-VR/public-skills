---
name: gitnexus
description: >
  Self-bootstrapping codebase knowledge graph. One command sets up everything:
  installs GitNexus, configures MCP for all editors, indexes the current repo,
  installs built-in skills + hooks, and verifies end-to-end. Use when: "map this
  repo", "repo graph", "index codebase", "gitnexus", "set up gitnexus",
  "what depends on X", "blast radius". Auto-activates on unfamiliar codebases.
metadata:
  author: contributor
  version: 2.0.0
related_skills:
  - gitnexus-guide
  - gitnexus-cli
---

# GitNexus — Codebase Knowledge Graph

**One invocation. Zero questions. Full setup.**

When this skill is invoked, the agent executes the procedure below top-to-bottom.
No asking the user what to do — just check, install, configure, index, verify, report.

> Detailed tool usage in `references/tool-patterns.md`.
> Detailed setup troubleshooting in `references/setup-protocol.md`.
> Design rationale in `references/intent.md`.

---

## Procedure — Execute Top-to-Bottom

### Step 1 — Preflight (parallel)

Run ALL of these in a single Bash call:

```bash
echo "=== NODE ===" && node --version && \
echo "=== GITNEXUS ===" && (which gitnexus 2>/dev/null && gitnexus --version || echo "NOT INSTALLED") && \
echo "=== INDEX ===" && (ls .gitnexus/meta.json 2>/dev/null && echo "EXISTS" || echo "NO INDEX") && \
echo "=== MCP ===" && (claude mcp list 2>/dev/null | grep -i gitnexus || echo "NOT CONFIGURED") && \
echo "=== CODEX ===" && (grep -c "gitnexus" ~/.codex/config.toml 2>/dev/null || echo "NOT CONFIGURED")
```

**If Node.js < 20:** STOP. Tell user: "GitNexus requires Node.js >= 20. Run: `nvm install 24`"

**Read the output, then skip to whichever step is needed:**

| Preflight result | Skip to |
|-----------------|---------|
| GitNexus NOT INSTALLED | Step 2 |
| Installed but NO INDEX | Step 4 |
| Installed, indexed, MCP NOT CONFIGURED | Step 3 |
| Everything present but index STALE | Step 4 (re-index) |
| Everything green | Step 5 (verify only) |

---

### Step 2 — Install GitNexus

```bash
npm install -g gitnexus 2>&1 | tail -3
gitnexus --version
```

If npm global fails (permissions error), tell user to run:
```bash
sudo npm install -g gitnexus
```

---

### Step 3 — Configure All Editors + MCP + Skills + Hooks

**One command does everything:**

```bash
gitnexus setup
```

This auto-detects all installed editors and configures:
- MCP server registration (Claude Code, Codex, Cursor, Windsurf, OpenCode)
- 7 built-in skills installed to each editor's skill directory:
  - `~/.claude/skills/` (Claude Code)
  - `~/.agents/skills/` (Codex + OpenClaw — shared directory)
  - `~/.cursor/skills/` (Cursor)
  - `~/.config/opencode/skill/` (OpenCode)
- PreToolUse + PostToolUse hooks for Claude Code
- CLAUDE.md updated with GitNexus usage rules (per-project)

**OpenClaw note:** OpenClaw inherits MCP from Claude Code (no separate config needed).
The `~/.agents/skills/` directory is shared between Codex and OpenClaw agents.

#### Step 3b — Fix MCP commands (MANDATORY after setup)

`gitnexus setup` writes `npx -y gitnexus@latest mcp` as the MCP command.
**This breaks.** npx caches corrupt and cause `MODULE_NOT_FOUND` errors.
After running setup, fix ALL editors to use the global binary:

```bash
# Claude Code
claude mcp remove gitnexus -s user 2>/dev/null
claude mcp add -s user gitnexus -- gitnexus mcp

# Codex — edit ~/.codex/config.toml, change to:
# [mcp_servers.gitnexus]
# command = "gitnexus"
# args = ["mcp"]

# Cursor — edit ~/.cursor/mcp.json, change gitnexus command to "gitnexus", args to ["mcp"]
# OpenCode — edit ~/.config/opencode/config.json, same change
```

Or run this one-liner to fix all JSON configs at once:
```bash
for f in ~/.cursor/mcp.json ~/.config/opencode/config.json; do
  [ -f "$f" ] && python3 -c "
import json,sys
d=json.load(open('$f'))
key='mcpServers' if 'mcpServers' in d else 'mcp'
if key in d and 'gitnexus' in d[key]:
  d[key]['gitnexus']={'command':'gitnexus','args':['mcp']}
  json.dump(d,open('$f','w'),indent=2)
  print(f'Fixed: $f')
"
done
```

---

### Step 4 — Index Current Repository

```bash
gitnexus analyze --embeddings --skills 2>&1 | tail -15
```

Flags used:
- `--embeddings` — semantic search (finds code by meaning, not just keywords)
- `--skills` — generates per-cluster skill files in `.claude/skills/generated/`

This creates:
- `.gitnexus/` — graph database (gitignored, local per device)
- `.gitnexus/meta.json` — index metadata
- `.claude/skills/generated/` — auto-generated per-module skills
- Updates to `CLAUDE.md` and `AGENTS.md` with usage rules

---

### Step 5 — Verify (mandatory)

Run ALL checks:

```bash
echo "=== 1. Binary ===" && gitnexus --version && \
echo "=== 2. Index ===" && gitnexus status && \
echo "=== 3. MCP ===" && claude mcp list 2>/dev/null | grep -i gitnexus && \
echo "=== 4. Test Query ===" && gitnexus query "main entry point" 2>/dev/null | head -20
```

**All 4 must pass.** If MCP shows "Failed to connect" — that's normal mid-session.
Tell user: "GitNexus is fully set up. MCP tools activate on next session restart."

---

### Step 6 — Report to User

Print a summary:

```
GitNexus setup complete.

Installed: v{version}
Indexed: {node_count} nodes, {edge_count} edges, {cluster_count} clusters, {flow_count} flows
MCP: configured for {editors}
Skills: 7 built-in + {generated_count} repo-specific
Hooks: PreToolUse + PostToolUse (auto-index on commit)

MCP tools available after session restart:
  mcp__gitnexus__query       — search execution flows
  mcp__gitnexus__context     — 360° symbol view
  mcp__gitnexus__impact      — blast radius analysis
  mcp__gitnexus__detect_changes — map diffs to affected symbols
  mcp__gitnexus__rename      — safe multi-file rename
  mcp__gitnexus__cypher      — raw graph queries

Visual graph: run `gitnexus serve` then open http://localhost:4747
```

---

## When to Activate

| Signal | Action |
|--------|--------|
| `/gitnexus` or "map this repo" | Full procedure (Steps 1-6) |
| "what depends on X?" | Check index exists → `mcp__gitnexus__impact` |
| "how does X work?" | Check index exists → `mcp__gitnexus__query` |
| Before deep-sweep or deep-build | Ensure index is current (Step 4 if stale) |
| New device / fresh clone | Full procedure (Steps 1-6) |
| "show me the graph" | `gitnexus serve` → open http://localhost:4747 |

---

## What `gitnexus setup` Installs

The `setup` command auto-installs these into each editor:

**7 Built-in Skills:**

| Skill | Purpose |
|-------|---------|
| `gitnexus-exploring` | Navigate unfamiliar code via knowledge graph |
| `gitnexus-debugging` | Trace bugs through call chains |
| `gitnexus-impact-analysis` | Assess blast radius before changes |
| `gitnexus-refactoring` | Plan safe renames, extracts, splits |
| `gitnexus-guide` | Tool reference and query patterns |
| `gitnexus-cli` | CLI commands (analyze, status, wiki) |
| `gitnexus-pr-review` | PR review with graph-aware context |

**Hooks (Claude Code):**
- `PreToolUse` — suggests GitNexus tools when relevant
- `PostToolUse` — auto-reindexes after git commit/merge

**Project files:**
- `CLAUDE.md` — usage rules (impact before edit, detect_changes before commit)
- `AGENTS.md` — agent workflow guidance

---

## MCP Tools Quick Reference

| Tool | Purpose | When |
|------|---------|------|
| `query` | Search execution flows by keyword | Exploring, understanding |
| `context` | 360° view of one symbol (callers, callees, flows) | Deep dive |
| `impact` | Blast radius — what breaks if you change X | Before ANY edit |
| `detect_changes` | Map git diff to affected symbols | Before commit |
| `rename` | Dry-run rename with all affected files | Refactoring |
| `cypher` | Raw Cypher graph queries | Advanced analysis |
| `list_repos` | List all indexed repos | Orientation |
| `group_query` | Cross-repo flow analysis | Multi-repo projects |

> Full usage patterns and examples in `references/tool-patterns.md`.

---

## Supported Languages

TypeScript, JavaScript, Python, Java, Kotlin, C#, Go, Rust, PHP, Ruby, Swift,
C, C++, Dart — 14 languages via Tree-sitter AST parsing.

---

## Hard Rules

1. **Execute top-to-bottom.** Don't ask the user what to do. Check, act, report.
2. **Skip steps that are already done.** Preflight tells you what's needed.
3. **Always use `--embeddings --skills` on first index.** Semantic search + per-module skills.
4. **Re-index on staleness.** `gitnexus status` before relying on graph data.
5. **.gitnexus/ is local.** Never committed. Each device indexes independently.
6. **Verify after every setup.** Step 5 is mandatory, not optional.
7. **One command for MCP + skills + hooks:** `gitnexus setup`. Don't configure manually.
8. **Mid-session MCP won't connect.** That's expected. Tools activate on restart.
9. **Impact before modify.** Built into CLAUDE.md rules — agents must run impact before edits.
10. **Visual graph:** `gitnexus serve` → http://localhost:4747 for browser visualization.
