---
name: jam-mcp-debugger
description: Automatically pull Jam (jam.dev) report context via Jam MCP tools and use it to reproduce, diagnose, and fix issues in the repo whenever “Jam/jam” is mentioned or a jam.dev link is present.
source: local
related_skills: [sentry-debugger, datadog-cli, qa-regression, browser-automation]
---

# Jam MCP Debugger

Use this skill whenever the user mentions **Jam/jam** or includes a **jam.dev** link.

## Trigger (When to Use)

Activate when either is true:
- The user message contains the whole word `jam` (case-insensitive), e.g. regex `(?i)\bjam\b`
- The user message contains a Jam link, e.g. regex `https?://(www\.)?jam\.dev/\S+`

## Required Input

- A Jam link (usually `https://jam.dev/...`).
- If the user didn’t include a link, ask for it (Jam MCP tools require a specific Jam to load).
- If there are multiple links, process **one Jam at a time** and ask which link to prioritize.

## Tools (Jam MCP)

Prefer these tool names (your MCP client may prefix them with `jam.`):
- `getDetails` (always call first)
- `getUserEvents`
- `getConsoleLogs`
- `getNetworkRequests`
- `analyzeVideo`
- `getScreenshot`

## Workflow (Tooling Policy)

1) **Extract Jam links** from the latest user message.
2) **If no link**, ask: “Please paste the Jam link (jam.dev/...) so I can load it via Jam MCP and debug.”
3) **If a link exists**, for the selected Jam:
   - Call `getDetails` first.
   - Then call only the additional tools that match the symptom:
     - Call `getUserEvents` to reconstruct precise repro steps.
     - Call `getConsoleLogs` when runtime errors/log clues exist or are likely.
     - Call `getNetworkRequests` when API failures/auth/CORS/performance is implied.
     - Call `analyzeVideo` when the issue is visual/interaction-based or the root cause is unclear.
     - Call `getScreenshot` only for “screenshot Jams” (or when explicitly needed).
4) **Build an actionable debugging bundle** from Jam artifacts:
   - Repro steps (from `getUserEvents` and/or `analyzeVideo`)
   - Observed vs expected behavior
   - Errors and anomalies (console + network), including timestamps if available
   - Environment context (browser/device/app URL/build info) from `getDetails`
   - 1–3 root-cause hypotheses grounded in the above evidence
5) **Cross-reference the repo**:
   - Use repo search to locate the implicated modules/routes/components.
   - Map each Jam symptom to a code location (or a short list of candidates).
6) **Implement a minimal fix**:
   - Prefer the smallest change that addresses the Jam evidence.
   - Add/adjust tests when the repo already has testing patterns for the affected area.
7) **Verify**:
   - Run the narrowest relevant checks first (unit tests/build/lint).
   - Provide manual verification steps that mirror Jam repro steps.

## Guardrails

- **Context hygiene**: Don’t paste huge logs; summarize and quote only the most relevant lines.
- **Least tooling**: Don’t call every Jam tool by default; expand only as needed.
- **Sensitive data**: Do not echo secrets/tokens/cookies from logs or network traces; redact if present.
- **One Jam at a time**: Avoid loading multiple Jams into context unless the user explicitly requests comparison.

## Example User Prompts (Should Trigger)

- “Jam shows checkout failing: https://jam.dev/abcd…”
- “I recorded a jam — can you debug it?”

