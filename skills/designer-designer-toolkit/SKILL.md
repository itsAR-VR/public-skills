---
name: designer-designer-toolkit
description: "Essential designer utilities for writing rationale, building presentations, crafting case studies, UX writing, and driving adoption. Use when the user asks for designer toolkit workflows, command routing, or the Owl-Listener designer-skills designer-toolkit plugin."
license: MIT
metadata:
  author: MC Dean
  source: https://github.com/Owl-Listener/designer-skills
  source_commit: 152fc2a19985b061971c61efbf45e675517005c8
  upstream_plugin: designer-toolkit
---

# designer-toolkit

Essential designer utilities for writing rationale, building presentations, crafting case studies, UX writing, and driving adoption.

This is the Goated Skills wrapper for the upstream Owl-Listener `designer-toolkit` plugin. Use it to choose the right imported design skill and command workflow.

## Available Skills

- `case-study`
- `design-negotiation`
- `design-rationale`
- `design-system-adoption`
- `design-token-audit`
- `presentation-deck`
- `ux-writing`

## Available Commands

- `designer-toolkit:build-presentation` - see `references/commands/build-presentation.md`
- `designer-toolkit:write-case-study` - see `references/commands/write-case-study.md`
- `designer-toolkit:write-rationale` - see `references/commands/write-rationale.md`

## How To Use

1. Match the user's design task to the closest command under `references/commands/` when they need a complete workflow.
2. Load the named individual skills above when the task needs focused domain guidance.
3. Preserve the upstream command sequence, then adapt the final output to the user's actual product, audience, and constraints.

## Provenance

- Source repo: https://github.com/Owl-Listener/designer-skills
- Source commit: `152fc2a19985b061971c61efbf45e675517005c8`
- Source plugin path: `designer-toolkit/`
- License: MIT
