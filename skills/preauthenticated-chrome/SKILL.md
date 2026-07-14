---
name: preauthenticated-chrome
description: Use the user's real, already signed-in Google Chrome window instead of sandboxed browser contexts when browser auth, passkeys, existing cookies, or anti-bot checks matter. Trigger when the user says to use their Chrome instance, mentions they are already logged in, needs native passkey prompts, or when Browser Harness/browser automation is blocked by login friction, Turnstile, MFA, or missing session state.
related_skills:
  - browser-automation
---

# Preauthenticated Chrome

Use the user's actual Google Chrome profile through AppleScript before falling back to isolated browser tooling. This preserves existing logins, cookies, and native macOS passkey behavior.

## Workflow

1. Verify Chrome is reachable:

```bash
osascript -e 'tell application "Google Chrome" to get title of active tab of front window'
osascript -e 'tell application "Google Chrome" to get URL of active tab of front window'
```

2. Open a new tab in the front window instead of hijacking an unrelated tab when possible:

```bash
osascript <<'APPLESCRIPT'
tell application "Google Chrome"
  activate
  tell front window
    make new tab with properties {URL:"https://example.com"}
    set active tab index to (count of tabs)
  end tell
end tell
APPLESCRIPT
```

3. Inspect the current page with JavaScript executed in the active tab:

```bash
osascript <<'APPLESCRIPT'
tell application "Google Chrome"
  return execute active tab of front window javascript "document.body.innerText.slice(0, 2000)"
end tell
APPLESCRIPT
```

4. Perform DOM actions with JavaScript when the page is stable:

```bash
osascript <<'APPLESCRIPT'
tell application "Google Chrome"
  execute active tab of front window javascript "Array.from(document.querySelectorAll('button')).find(el => /continue/i.test(el.innerText || '')).click(); 'clicked'"
end tell
APPLESCRIPT
```

5. For complex pages, inspect first, then target stable ids, names, or exact button text. Prefer direct ids over broad text matching when available.

## Rules

- Prefer this skill whenever auth state matters more than browser isolation.
- Use the user's real Chrome for:
  - Google/Shopify/Meta/Slack/admin console logins
  - native passkey prompts
  - flows blocked by Cloudflare Turnstile or similar anti-bot checks
  - sites where the user is already signed in
- Ask the user to complete passkey/MFA in the Chrome window when a native prompt appears, then resume automation.
- Preserve the user's session. Do not sign out, clear cookies, close unrelated windows, or switch profiles unless explicitly asked.
- Create a new tab for automation work when possible.
- If DOM automation is brittle, stage the page in Chrome, let the user finish the human-only step, then continue with scripted DOM actions.
- Fall back to sandboxed Browser Harness only when the task explicitly needs isolation or when Chrome automation is unavailable.

## Useful Patterns

Get a quick structured snapshot:

```bash
osascript <<'APPLESCRIPT'
tell application "Google Chrome"
  execute active tab of front window javascript "JSON.stringify({title: document.title, url: location.href, buttons: Array.from(document.querySelectorAll('button')).map((el, i) => ({i, text: (el.innerText || '').trim()})).filter(x => x.text).slice(0, 20)})"
end tell
APPLESCRIPT
```

Fill a known input by id:

```bash
osascript <<'APPLESCRIPT'
tell application "Google Chrome"
  execute active tab of front window javascript "(function(){ const el = document.getElementById('email'); if (!el) return 'missing'; el.focus(); el.value = 'user@example.com'; el.dispatchEvent(new Event('input', {bubbles:true})); el.dispatchEvent(new Event('change', {bubbles:true})); return 'filled'; })()"
end tell
APPLESCRIPT
```

Wait for a page state from the shell:

```bash
osascript <<'APPLESCRIPT'
on waitForText(theNeedle, maxTries)
  tell application "Google Chrome"
    repeat with i from 1 to maxTries
      delay 2
      set bodyText to execute active tab of front window javascript "document.body.innerText.slice(0, 4000)"
      if bodyText contains theNeedle then return true
    end repeat
  end tell
  return false
end waitForText
APPLESCRIPT
```

## Decision Boundary

- Use this skill first for authenticated browser work on this machine.
- Do not use this skill for tasks that require a clean browser profile, incognito-like isolation, or reproducible test conditions.
