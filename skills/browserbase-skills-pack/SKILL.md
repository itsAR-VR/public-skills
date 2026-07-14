---
name: browserbase-skills-pack
description: >
  Install and update a curated subset of BrowserBase's open-source skills
  (github.com/browserbase/skills) — only the four free, no-API-key-required
  skills that complement browser-harness without overlapping it. Use when the
  user says "install browserbase skills", "update browserbase skills", "add
  browserbase pack", "what-antibot", "safe-browser", "browser-trace", asks
  about CDP firehose tracing, accessibility-tree-driven browsing as a backup
  for bot-detected sites, or constrained domain-allowlisted agents. Wraps a
  custom git-clone + cherry-pick + prefix-rename install (the upstream is a
  GitHub repo, not an `npx skills` marketplace pack), so only the four
  manifested skills land — cloud/account-metered skills (fetch, search,
  cookie-sync) and platform-lock-in tools (functions, browserbase-cli) are
  intentionally skipped. Pairs with browser-harness (primary runtime) and
  harness-autobrowse (skill factory).
metadata:
  author: contributor
  version: 1.0.0
  source: github.com/browserbase/skills
  license: MIT (per upstream)
related_skills: [browser-harness, harness-autobrowse, sync-skills, setup-skill-packs]
---

# browserbase-skills-pack

Meta-skill that installs **four cherry-picked free skills** from
[github.com/browserbase/skills](https://github.com/browserbase/skills) into
`~/.claude/skills/` with a `browserbase-` prefix on each. Designed to
complement `browser-harness` — not replace it.

## Why a custom pack (not `npx skills add`)

The upstream is a plain GitHub repo, not an `npx skills` marketplace package,
and we want only 4 of its 13 skills. Crucially, we also need to **rename them
with a `browserbase-` prefix** so `browserbase-browser` doesn't collide with
the conceptual "browser" slot already held by `browser-harness`. The `npx
skills` CLI doesn't support either selective install or rename-on-install,
so this pack does its own git-clone + cherry-pick + frontmatter-rewrite.

## What's in the pack

| Installed name | Upstream | Why we vendored it |
|---|---|---|
| `browserbase-browser` | `browser` | Backup runtime for bot-protected sites (escalation path from browser-harness). Local mode is free; remote mode requires a Browserbase account/API key and plan-aware cost check. |
| `browserbase-safe-browser` | `safe-browser` | Builder skill for *constrained* agents — emits a Claude Agent SDK app where the agent has only `safe_browser` with CDP `Fetch` interception enforcing a domain allowlist. Free, Browser Harness-based, fully local. Different threat model from browser-harness. |
| `browserbase-what-antibot` | `what-antibot` | Pre-flight detector. Single Node-stdlib HTTP probe checks for Cloudflare, Akamai, DataDome, PerimeterX, Imperva/Incapsula, Kasada, reCAPTCHA, hCaptcha, Anubis, Shape. No deps, no API key. |
| `browserbase-browser-trace` | `browser-trace` | Read-only second CDP client capturing the DevTools firehose, screenshots, and DOM dumps, then bisecting per page. Free in local mode. No equivalent in browser-harness. |

## What's intentionally NOT in the pack

| Upstream skill | Why skipped |
|---|---|
| `fetch` | Browserbase cloud/API-key feature with plan credits and overages. `curl`/`node fetch`/`python requests` are free. |
| `search` | Browserbase cloud/API-key feature with plan credits and overages. Already covered by `brave-search`, `perplexity`, `web-search-plus`, `multi-search-engine`. |
| `cookie-sync` | Only meaningful for remote `browse` sessions. Reinstall via extended manifest if you commit to BB cloud. |
| `browserbase-cli` (`bb`) | Platform tool. Only useful for BB Functions / Browserbase cloud sessions. |
| `functions` | Browserbase-cloud-specific serverless deployment. |
| `autobrowse` | Pattern is valuable, but hardwired to `browse` CLI as runtime. We port the iteration loop in-house as `harness-autobrowse` driving browser-harness. |
| `ui-test` | Overlaps with `browse-qa`, `ecc-browser-qa`, `webapp-testing`. |
| `company-research`, `event-prospecting` | Overlap with `company-research`, `customer-research`, `lead-research-assistant`, `competitor-profiling`. The in-repo versions are more mature. |

## Routing — how this pack interoperates with browser-harness

```
Pre-flight   →  browserbase-what-antibot      [free]
Runtime      →  browser-harness               [free, primary]
Sandboxing   →  browserbase-safe-browser      [free, when agent must be constrained]
Observability→  browserbase-browser-trace     [free, attaches alongside any CDP automation]
Escape hatch →  browserbase-browser (remote)  [account/API key; check pricing before quoting costs]
Skill factory→  harness-autobrowse            [free; produces domain-skills via browser-harness]
```

The "Pre-flight → Runtime → Escalation" pattern is wired into
`browser-harness/SKILL.md`. Use this pack alongside that one — never as a
replacement.

Pricing/currentness note (checked 2026-06-10 against Browserbase's official
pricing and billing-plan docs): Browserbase plans include browser hours and
Fetch/Search credits with overages, so treat cloud/API-key features as
account-metered, not a fixed per-session price. Re-check official Browserbase
pricing before quoting costs.

## Workflow

### Install (first time)

```bash
bash "$HOME/.claude/skills/browserbase-skills-pack/scripts/install.sh"
```

Clones `github.com/browserbase/skills` to `$HOME/.cache/browserbase-skills`,
copies just the four manifested directories into `$HOME/.claude/skills/`
with `browserbase-` prefixes, and rewrites each SKILL.md's `name:` field to
match the prefixed directory.

If a `browserbase-<skill>` directory already exists, the script writes a
diff snapshot under `$HOME/.codex/skill-sync-diffs/<timestamp>/` *before*
replacing — same convention as `sync-skills`.

### Update

```bash
bash "$HOME/.claude/skills/browserbase-skills-pack/scripts/update.sh"
```

`git pull` on the cached clone, then re-runs the cherry-pick. Idempotent.
Network failures are non-fatal — if the upstream is unreachable, the
already-installed copies keep working.

### Verify

```bash
bash "$HOME/.claude/skills/browserbase-skills-pack/scripts/verify.sh"
```

Checks each manifested skill exists at `$HOME/.claude/skills/<name>/SKILL.md`
and that the frontmatter `name:` matches the directory name (the
prefix-rewrite is the most likely thing to silently drift).

## Integration with sync-skills

`sync-skills` Step 1.5 calls every pack's `update.sh` automatically — drop
this pack in `skills/` and sync-skills picks it up with no core edits. Step
1.6 then enforces "upstream wins for manifest-managed names" using the four
prefixed names in `manifest.txt` — so the pack stays current and your edits
to *other* skills are preserved.

## Examples

### Example 1: First-time install
**User says:** "install browserbase skills"

**Actions:**
1. Run `scripts/install.sh`.
2. Confirm with `scripts/verify.sh` that all 4 prefixed skills resolve.
3. Suggest the pre-flight: "`browserbase-what-antibot` checks bot protection on a URL before you spin up a browser."

### Example 2: Bot detection escalation
**User says:** "scrape this Cloudflare-protected page"

**Actions:**
1. `browserbase-what-antibot` probes the URL → detects Cloudflare.
2. Skip browser-harness (would be challenged); fall through to `browserbase-browser` in remote mode (requires `BROWSERBASE_API_KEY`).
3. If user has no API key, surface the account/cost decision: "Browserbase remote mode needs an account/API key and current pricing check. Want to set that up, or work around it?"

### Example 3: Debugging a failed automation
**User says:** "the browser-harness run on linkedin.com died at step 4 — what happened?"

**Actions:**
1. Re-run with `browserbase-browser-trace` attached as a second CDP client (the trace is read-only — doesn't disrupt browser-harness).
2. After failure, run `node scripts/bisect-cdp.mjs <run>` to slice the firehose into per-page network/console/page buckets.
3. Inspect the failure turn's screenshot + DOM dump joined by timestamp.

## Troubleshooting

### `git: command not found`
- **Fix:** `xcode-select --install` (macOS) or `apt install git` (Linux).

### Network unreachable during install
- **Fix:** The script falls back to "use whatever's already in the cache." If the cache is empty, it surfaces a clear error.

### `browserbase-<skill>` directory exists with different content
- **Cause:** Hand-edited locally, or older install with different upstream commit.
- **Fix:** The script writes a diff snapshot under `$HOME/.codex/skill-sync-diffs/<ts>/` before replacing. Inspect that diff if you want to keep your edits.

### Frontmatter `name:` mismatch after install
- **Cause:** The prefix-rewrite step failed (e.g., a file lock).
- **Fix:** Re-run `scripts/install.sh` — the rewrite is idempotent.

## Related Skills

- **browser-harness** — the primary browser runtime; this pack complements it.
- **harness-autobrowse** — skill factory using browser-harness, ports BrowserBase's autobrowse iteration loop in-house.
- **sync-skills** — calls `update.sh` automatically on every sync.
- **setup-skill-packs** — full first-boot bootstrap; can be extended to call `install.sh`.
