---
name: browse-qa
description: >
  Screenshot-driven browser QA using OpenClaw's persistent browser profile.
  Use when the user asks to verify a deploy, truth-pass a UI, click through a
  flow, check responsive layouts, run browse QA, do a browser verification pass,
  or confirm that a changed route actually works. Covers desktop/mobile
  screenshots, critical-path interactions, console inspection, and tab cleanup.
metadata:
  author: podhi
  version: 1.0.0
related_skills: [browser-harness, ecc-browser-qa, webapp-testing, browser-automation, qa-regression]
routing:
  domain_keywords:
    - qa
    - test
    - verify
    - screenshot
    - browser
    - check
    - responsive
    - desktop
    - mobile
    - visual
    - inspect
    - validation
  intent_patterns:
    - "(?:check|verify|test|qa|inspect|screenshot)\\s+(?:the\\s+)?(?:site|page|app|ui|deploy)"
    - "(?:does it|is it)\\s+(?:look|work|render)\\s+(?:right|correctly|good)"
  lane: codex-worker
  task_type: qa-verification
---

# browse-qa

This is the repo-native browse lane built for OpenClaw's browser tool.

## When to use

Use this skill when the task involves any of the following:
- deployed UI verification
- localhost/dev UI verification
- screenshot-based truth pass
- login flow or key browser-path verification
- responsive/mobile spot checks
- browser regression check after a feature change
- "browse QA", "browser verify", "truth pass", or "look at the site" asks

For generic browser automation or scraping, see `browser-automation`.
For the full plan -> implement -> review -> browse -> ship chain, see `build`.

## Core idea

A valid browser QA pass is not:
- "the page loaded"
- "the code looks right"
- "tests passed"

A valid browser QA pass **is**:
- target opened in a persistent browser session
- screenshots captured for the impacted states
- critical interaction path exercised
- console checked
- pass/fail called explicitly
- task tabs closed afterward

## Preferred browser runtime

### Default
Use the `openclaw` browser profile.

Why:
- persistent cookies/sessions
- isolated agent-controlled browser
- best fit for repeatable QA runs

### If user explicitly mentions Chrome extension / Browser Relay / attached tab
Use profile `chrome` and keep the same attached tab.

## Workflow

### 1) Resolve target and scope

Identify:
- base URL
- impacted route(s)
- critical interaction path(s)
- whether auth is required
- whether desktop-only or desktop + mobile is required

If the task changed a UI, default to **desktop + mobile**.

### 2) Open the target in one controlled tab

- Start or use browser profile `openclaw`
- Open/navigate to the target URL
- Take a snapshot and preserve the returned `targetId`
- Reuse the same `targetId` across subsequent actions

Best practice:
- use `snapshot` with `refs="aria"` for stable refs
- use `act` for clicks/fills/presses
- avoid `wait` unless there is no better state signal

### 3) Capture initial evidence

Minimum evidence:
- desktop screenshot of the impacted route
- snapshot of the page structure or interactive controls
- visible confirmation that the expected UI is present

Treat these as immediate FAIL signals:
- 404 / 500 / framework error shell
- blank page or blank content region
- missing primary UI for the route
- auth loop when auth should already exist

### 4) Exercise the critical path

Do the smallest realistic interaction sequence that proves the changed flow works.
Examples:
- open modal -> fill form -> submit -> verify success state
- navigate landing page -> scroll to changed section -> inspect rendered layout
- login -> visit dashboard -> trigger changed action -> verify result

After meaningful state changes:
- take another screenshot
- re-snapshot if refs became stale

### 5) Mobile / responsive pass

If the flow is user-facing, also verify a narrow viewport.
Default mobile check:
- 375px width

Capture:
- mobile screenshot
- any broken wrapping, overflow, hidden controls, layout collisions

### 6) Console check

Inspect browser console output after the main flow.
Classify:
- no relevant errors
- warnings only
- relevant errors tied to changed flow

Relevant errors tied to the changed flow mean FAIL unless clearly proven unrelated.

### 7) Cleanup

Close every tab opened for the task as soon as the pass is complete.
Do not leave QA tabs hanging around.

## Output contract

Return:
- target URL(s)
- routes checked
- interactions performed
- screenshot states captured
- console status
- pass/fail result
- known limitations
- confirmation that task tabs were closed

## Troubleshooting

### Refs stopped working
- Cause: navigation or DOM change invalidated them
- Fix: take a fresh snapshot and continue with new refs

### Browser appears logged out
- Cause: wrong profile or expired session
- Fix: retry with the intended persistent profile; if auth is genuinely required, note the blocker clearly

### Flow is flaky
- Cause: relying on arbitrary waits
- Fix: prefer explicit UI signals, text disappearance, stable elements, or URL change

### Browser session got messy
- Cause: too many leftover tabs from prior runs
- Fix: close task tabs aggressively and re-open a clean target tab

## Success bar

Do not report "looks good" unless you actually captured visual evidence and exercised the flow.
If proof is partial, say so plainly.
