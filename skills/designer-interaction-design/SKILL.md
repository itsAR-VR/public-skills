---
name: designer-interaction-design
description: "Design meaningful interactions with micro-animations, state machines, gestures, error handling, and feedback patterns. Use when the user asks for interaction design workflows, command routing, or the Owl-Listener designer-skills interaction-design plugin."
license: MIT
metadata:
  author: MC Dean
  source: https://github.com/Owl-Listener/designer-skills
  source_commit: 152fc2a19985b061971c61efbf45e675517005c8
  upstream_plugin: interaction-design
---

# interaction-design

Design meaningful interactions with micro-animations, state machines, gestures, error handling, and feedback patterns.

This is the Goated Skills wrapper for the upstream Owl-Listener `interaction-design` plugin. Use it to choose the right imported design skill and command workflow.

## Available Skills

- `animation-principles`
- `doherty-threshold`
- `error-handling-ux`
- `feedback-patterns`
- `fitts-law`
- `form-design`
- `gesture-patterns`
- `hicks-law`
- `interfaces-that-feel`
- `loading-states`
- `micro-interaction-spec`
- `millers-law`
- `navigation-patterns`
- `onboarding-design`
- `search-ux`
- `state-machine`

## Available Commands

- `interaction-design:design-interaction` - see `references/commands/design-interaction.md`
- `interaction-design:error-flow` - see `references/commands/error-flow.md`
- `interaction-design:map-states` - see `references/commands/map-states.md`

## How To Use

1. Match the user's design task to the closest command under `references/commands/` when they need a complete workflow.
2. Load the named individual skills above when the task needs focused domain guidance.
3. Preserve the upstream command sequence, then adapt the final output to the user's actual product, audience, and constraints.

## Provenance

- Source repo: https://github.com/Owl-Listener/designer-skills
- Source commit: `152fc2a19985b061971c61efbf45e675517005c8`
- Source plugin path: `interaction-design/`
- License: MIT
