---
name: moa
description: >
  Mixture of Agents — query multiple models on the same prompt and synthesize their
  responses into one answer. Useful for architecture reviews, code review, risk analysis,
  and tradeoff calls.
metadata:
  author: podhi
  version: 1.2.0
related_skills: [comparative-analysis-orchestrator, advanced-evaluation, evaluation, llm-application-dev]
---

# Mixture of Agents (MoA)

## Current truth

**MoA is not OpenClaw-native yet.**

No runnable MoA helper is currently shipped in `skills/moa/`, and this checkout
does not contain the older documented path `scripts/moa/run.sh`. Do not tell
operators to run that path unless it exists in their repo.

The last known implementation shape was a **direct HTTP / gateway orchestration script**:
- it calls provider APIs directly when matching API keys are available
- or it uses an OpenAI-compatible gateway path when configured
- it does **not** use OpenClaw's first-class model routing as its execution backend

This is the honest current state and should be described that way.

## Why it is not native yet

We attempted the clean native path and hit a real blocker:
- `openclaw agent --session-id <temp>` works non-interactively for plain prompts
- synthesis through a fresh temp session also works
- but **non-interactive model rebinding** via `/model ...` was not reliable enough to ship
- spawn-time binding experiments were also not reliable enough on the running setup to count as a production-ready hard pin

### Native blocker summary

The blocker is **model pinning from shell automation**, not basic session creation.

What failed reliably enough to block shipping:
- temp-session `/model anthropic/claude-sonnet-4-6` rebinding, from the original blocker notes
- clean spawn-time model hard-pinning through the available local CLI/runtime path

Model freshness note: source-checked 2026-06-10 against Anthropic's public model
docs, where `claude-sonnet-4-6` is listed as a pinned Claude Sonnet 4.6 model ID.
Before re-running or restoring MoA examples, re-check the provider's current
model list and the gateway's accepted model-name format.

### Closest viable future architecture

The likely correct native design is:
1. create separate OpenClaw lanes already pinned to model at spawn time
2. run the same prompt in those lanes
3. collect outputs
4. synthesize in a final model-pinned lane

That is an **orchestrator/session-spawn design**, not a tiny shell-only `/model` mutation trick.

## What MoA is still good for today

Even in direct-HTTP mode, it is still useful for:
- architecture reviews
- tradeoff analysis
- code review prompts
- research synthesis
- cross-checking one strong answer against another

Do **not** represent it as native OpenClaw model orchestration until that blocker is actually removed.

## Usage

No executable runner is present in this skill directory today. If a repo-level
runner is restored, first verify the path exists:

```bash
test -f scripts/moa/run.sh
```

Expected runner interface, only after that path exists:

```bash
# Default set of available models
bash scripts/moa/run.sh "What are the pros and cons of microservices vs monolith?"

# Explicit models
bash scripts/moa/run.sh "Review this Go error handling pattern" \
  --models openai-codex/<latest-openai-model-id>,anthropic/claude-sonnet-4-6 \
  --synthesizer anthropic/claude-sonnet-4-6

# Longer timeout
bash scripts/moa/run.sh "Analyze the security tradeoffs of JWT vs opaque tokens" \
  --timeout 120
```

## Output

A restored runner should emit JSON like:

```json
{
  "mode": "direct-http",
  "synthesis": "...",
  "models": [
    {
      "model": "openai-codex/<latest-openai-model-id>",
      "response": "...",
      "durationMs": 8200
    }
  ],
  "totalDurationMs": 17580
}
```

`mode` should be included so callers can tell this is still the non-native implementation.

## Requirements

Restored runner requirements should stay **provider/gateway level**, not OpenClaw-native:
- matching provider API keys, or
- an OpenAI-compatible gateway path configured for the script

## Operator note

If you want the true native version, treat it as a separate implementation task:
- build it around **spawn-time model-bound OpenClaw lanes**
- do not rely on shell-driven `/model` mutation
- do not claim completion until cross-model pinning is proven end-to-end
