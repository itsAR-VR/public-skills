---
name: browser-harness
description: >
  Default browser automation in the user's real, already-logged-in Chrome.
  Use whenever the user wants to automate, scrape, click through, fill out,
  test, or interact with a webpage — shopping, logins, form filling, outreach
  on LinkedIn, GitHub actions, content posting, TikTok uploads, multi-step
  flows. Connects directly to the user's running Chrome via CDP so cookies,
  logins, and profiles are preserved. The agent writes and edits helpers.py
  mid-task when a capability is missing (self-healing). Searches
  domain-skills/<site>/ before inventing a new approach. Prefer over
  browser-harness-skill, browser-harness, browser-automation, browse-qa,
  browser-qa, live-env-browser-harness, and webapp-testing whenever work should
  happen in the user's real browser. Use browser-harness-skill instead only for
  isolated/headless E2E tests or CI pipelines.
metadata:
  author: contributor
  version: 1.0.0
  source: browser-use/browser-harness
  license: MIT
related_skills: [phase-plan, skill-oracle, think, deep-sweep, deep-build, goal-post, ultra-review, deep-clean]
---

# browser-harness

Default skill for any browser automation task in the user's real Chrome. Wraps `github.com/browser-use/browser-harness` — a thin, self-healing CDP harness the agent extends mid-task by editing `helpers.py`.

When `browser-harness` is part of a phase workflow, read
`skills/phase-plan/references/09_PHASE_PIPELINE_PLAYBOOK.md`. The playbook owns
the beginner-facing proof path, evidence-packet expectations, and labels for
`localhost`, PR preview, Vercel preview, and live production checks. This file
stays focused on real-browser automation mechanics.

## When to Use

Trigger phrases:
- "automate this site" / "do this in my browser" / "click through X"
- "scrape this page" / "extract the prices / reviews / data"
- "fill out this form" / "upload this file to X"
- "star this repo" / "like this post" / "follow this profile"
- "log in and do X" / "post this to X" / "download this"
- Any multi-step browser task that relies on the user's existing session

Prefer over `browser-harness-skill`, `browser-harness`, `browser-automation`, `browse-qa`, `browser-qa`, `live-env-browser-harness`, `webapp-testing` whenever the user wants work done in their real Chrome. Only fall back to `browser-harness-skill` for isolated headless tests or CI.

## Companion Skills (the wider stack)

browser-harness is the **runtime**. Four free companion skills from
[browserbase-skills-pack](../browserbase-skills-pack/SKILL.md) wrap around it
to handle pre-flight, sandboxing, observability, and bot-detection escape:

```
Pre-flight   →  browserbase-what-antibot     [free, before you touch a browser]
Runtime      →  browser-harness              [free, your real Chrome — this skill]
Sandboxing   →  browserbase-safe-browser     [free, when an agent must be domain-locked]
Observability→  browserbase-browser-trace    [free, second CDP client, attach mid-run]
Escape hatch →  browserbase-browser (remote) [paid, only when antibot blocks the free path]
Skill factory→  harness-autobrowse           [free, iteration loop driving this skill]
```

When in doubt, call `browserbase-what-antibot <url>` *before* opening a browser.
A clean negative means browser-harness will work; Cloudflare/DataDome/Akamai
markers mean either escalate to `browserbase-browser env remote` (paid) or
let `harness-autobrowse` learn evasion through iteration.

## Workflow

### 0. Pre-flight (recommended before unfamiliar sites)

Before opening a browser on a site you haven't automated before, probe for
bot protection — it costs one HTTP request and saves a wasted session:

```bash
node ~/.claude/skills/browserbase-what-antibot/scripts/detect.mjs <url>
```

Decision matrix:

| Result | Action |
|---|---|
| `no antibot detected` | Use browser-harness as normal. |
| reCAPTCHA / hCaptcha / Anubis | Try browser-harness first — your logged-in session may pass it. If challenged, escalate. |
| Cloudflare / Akamai / DataDome / PerimeterX / Imperva / Kasada / Shape | Skip browser-harness. Either escalate to `browserbase-browser env remote` (paid: stealth + residential proxies + auto-CAPTCHA) or hand the task to `harness-autobrowse` to learn site-specific evasion. |

### 1. Ensure install (once per device)

```bash
command -v browser-harness
```

If missing, run the bootstrap:

```bash
bash ~/.claude/skills/browser-harness/scripts/bootstrap.sh
```

Bootstrap clones the repo to `~/.local/share/browser-harness` (override with `BROWSER_HARNESS_DIR`), runs `uv tool install -e .` so the `browser-harness` CLI is on `$PATH` while still pointing at the editable checkout. That's what makes the "agent edits `helpers.py` mid-task" pattern work — the next invocation picks up the edit with no reinstall.

### 2. Load the repo's own docs into context

Before the first harness call in a session, read:

```bash
cat ~/.local/share/browser-harness/SKILL.md
cat ~/.local/share/browser-harness/helpers.py
```

The repo's `SKILL.md` is the authoritative usage guide. `helpers.py` is the live API — about 195 lines, easy to read end-to-end. The wrapper here handles routing; those files handle how.

For cold-start or reconnect, also read `install.md` in the repo.

### 3. Check domain-skills before inventing

For any specific site, see if someone already captured the map:

```bash
ls ~/.local/share/browser-harness/domain-skills
rg -n -i "<site>" ~/.local/share/browser-harness/domain-skills
```

If a domain skill exists, read it first — it'll save 10× the steps.

### 4. Invoke

```bash
browser-harness <<'PY'
new_tab("https://example.com")
wait_for_load()
print(page_info())
PY
```

- `new_tab(url)` for first navigation — **not** `goto(url)`, which clobbers the user's active tab.
- Any Python works inside the heredoc; helpers are pre-imported.
- `screenshot()` is the default verification — look at pixels, not assertions.

### 5. Self-heal missing capabilities

If a helper you need doesn't exist, **edit `~/.local/share/browser-harness/helpers.py`** to add it, then use it. That's the design. Keep additions general, not task-specific. The next `browser-harness` call picks up the edit immediately.

### 6. Contribute back

If you learned something non-obvious — a stable selector, a private API endpoint, a framework quirk, a trap — write it to `domain-skills/<site>/<topic>.md` in the cloned repo and open a PR. The harness gets better only because agents file what they learn. Never commit raw pixel coordinates, run narrations, or secrets.

## Examples

### Example 1: Star a repo as a verification task
**User says:** "Star browser-use/browser-harness for me"

**Actions:**
1. `command -v browser-harness` → exists (post-bootstrap)
2. `cat ~/.local/share/browser-harness/SKILL.md helpers.py` (first use this session)
3. Run:
   ```bash
   browser-harness <<'PY'
   new_tab("https://github.com/browser-use/browser-harness")
   wait_for_load()
   screenshot()
   PY
   ```
4. Locate the Star button visually, `click(x, y)`, `screenshot()` again to verify the toggle.

**Result:** Repo starred using the user's real GitHub session — no re-login.

### Example 2: Scrape a product page with no prior skill
**User says:** "Grab price and review count from this Amazon URL"

**Actions:**
1. `ls ~/.local/share/browser-harness/domain-skills/amazon/` — check for existing map
2. If empty: `new_tab(url)` → `wait_for_load()` → `screenshot()` to see the layout
3. Use `js("document.querySelector('#priceblock_ourprice')?.innerText")` for extraction
4. After success, write `domain-skills/amazon/product-page.md` capturing the stable selectors, URL pattern, and any traps (e.g., A/B variants). Open a PR.

**Result:** Data extracted; next agent on Amazon starts with a map, not a blank page.

## Troubleshooting

### `browser-harness: command not found`
- **Cause:** Bootstrap didn't run, or `~/.local/bin` isn't on `$PATH`
- **Fix:** Run `bash ~/.claude/skills/browser-harness/scripts/bootstrap.sh`. If still missing, add `export PATH="$HOME/.local/bin:$PATH"` to your shell rc

### `DevToolsActivePort` missing / can't attach to Chrome
- **Cause:** Remote-debugging checkbox never ticked on the active Chrome profile
- **Fix:** Activate the Chrome window, open `chrome://inspect/#remote-debugging`, have the user tick the checkbox and click Allow. Setting is sticky per-profile.

### `no close frame received or sent` / stale websocket
- **Cause:** Harness daemon is stale, not Chrome
- **Fix:** `cd ~/.local/share/browser-harness && uv run python -c "from admin import restart_daemon; restart_daemon()"` then retry

### Missing a helper I need
- **Cause:** Intentional — `helpers.py` ships thin (~195 lines)
- **Fix:** Edit `~/.local/share/browser-harness/helpers.py`, add the function, use it. This is the self-healing design, not an error.

### Connection refused right after Chrome launch
- **Cause:** Port advertised before listener is ready
- **Fix:** Poll for up to 30 seconds. Don't restart Chrome.

## Observability — debugging a failed run

When a browser-harness run fails in a way you can't diagnose from the final
screenshot, attach `browserbase-browser-trace` as a **second, read-only**
CDP client. Chrome accepts multiple concurrent CDP clients on the same
target — the trace listens to the firehose without disrupting the harness.

```bash
# 1. Find the harness's CDP target (it advertises on whatever port Chrome
#    is using for remote debugging — typically 9222 or 9223).
lsof -iTCP -sTCP:LISTEN -P | grep -i "Google Chrome"

# 2. Start the tracer alongside your run.
node ~/.claude/skills/browserbase-browser-trace/scripts/start-capture.mjs <port> my-run

# 3. Run browser-harness as normal. The tracer captures CDP events,
#    screenshots, and DOM dumps in parallel.

# 4. After the failure, stop and bisect.
node ~/.claude/skills/browserbase-browser-trace/scripts/stop-capture.mjs my-run
node ~/.claude/skills/browserbase-browser-trace/scripts/bisect-cdp.mjs my-run

# 5. Inspect the firehose, joined to screenshots by timestamp.
cat .o11y/my-run/cdp/summary.json
```

This is also how `harness-autobrowse` collects iteration evidence — the
trace artifacts feed back into the next hypothesis.

## Sandboxing — when an agent must stay on allowlisted domains

browser-harness gives the agent **full** authenticated power as the user.
That's the right default for outreach, posting, and personal automation.
For untrusted prompts, link-following from scraped content, or any flow
where prompt-injection could redirect the agent off-domain, use
`browserbase-safe-browser` instead — it generates a Claude Agent SDK app
where the agent has only one tool (`safe_browser`) backed by Browser Harness
with CDP `Fetch` interception enforcing a domain allowlist.

Use `safe-browser` when:
- Reading scraped HTML and acting on links found inside it
- Building a public-facing or shared agent
- Demonstrating prompt-injection containment
- Any task where "agent gets exfiltrated by a malicious page" is a real concern

Use browser-harness when:
- Operating as the user, on sites the user trusts
- Cookies, sessions, and full Chrome capabilities are needed
- The risk model is "this is my computer doing my work for me"

## Cross-Device Portability

This skill is self-bootstrapping. On a fresh device:

1. `setup-skill-packs` pulls `browser-harness/` from `public-skills` into `~/.claude/skills/`
2. First trigger runs `bootstrap.sh` → clones repo, installs CLI
3. First browser attach may prompt to tick the remote-debugging checkbox (per-profile one-time)

No per-device install decisions. Use `sync-skills` to propagate any edits to this wrapper back to `public-skills`.

## Related Skills

- `harness-autobrowse` — skill factory: iteration loop driving browser-harness, graduates passing strategies into `domain-skills/<site>/<task>.md`
- `browserbase-skills-pack` — installs the four free companion skills (what-antibot, safe-browser, browser-trace, browser)
- `browserbase-what-antibot` — pre-flight bot-detection probe (Step 0 above)
- `browserbase-browser-trace` — read-only second CDP client for post-mortem firehose capture
- `browserbase-safe-browser` — constrained-agent builder for domain-allowlisted automation
- `browserbase-browser` — backup runtime with stealth/proxies/CAPTCHA solving (paid in remote mode)
- `browser-harness-skill` / `browser-harness` — headless/isolated E2E, CI pipelines
- `preauthenticated-chrome` — alternative real-Chrome approach
- `sync-skills` / `setup-skill-packs` — how this skill travels across devices
- `browse-qa` / `browser-qa` — screenshot-driven QA workflows (uses a different harness)

<!-- local:browser-harness-computer-use-fallback:start -->
## Local Attach Fallback

If Browser-Harness attach fails on Chrome's `Allow` prompt and Computer Use is available, use Computer Use only to click that native Chrome prompt, then retry Browser-Harness. Do not use Computer Use for page automation.
<!-- local:browser-harness-computer-use-fallback:end -->
