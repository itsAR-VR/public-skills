---
name: designer-ux-strategy
description: "Shape product direction through competitive analysis, design principles, experience mapping, and strategic alignment. Use when the user asks for ux strategy workflows, command routing, or the Owl-Listener designer-skills ux-strategy plugin."
license: MIT
metadata:
  author: MC Dean
  source: https://github.com/Owl-Listener/designer-skills
  source_commit: 152fc2a19985b061971c61efbf45e675517005c8
  upstream_plugin: ux-strategy
---

# ux-strategy

Shape product direction through competitive analysis, design principles, experience mapping, and strategic alignment.

This is the Goated Skills wrapper for the upstream Owl-Listener `ux-strategy` plugin. Use it to choose the right imported design skill and command workflow.

## Available Skills

- `business-design`
- `competitive-analysis`
- `content-strategy`
- `design-brief`
- `design-principles`
- `experience-map`
- `information-architecture`
- `metrics-definition`
- `north-star-vision`
- `opportunity-framework`
- `service-blueprint`
- `stakeholder-alignment`

## Available Commands

- `ux-strategy:benchmark` - see `references/commands/benchmark.md`
- `ux-strategy:frame-problem` - see `references/commands/frame-problem.md`
- `ux-strategy:strategize` - see `references/commands/strategize.md`

## How To Use

1. Match the user's design task to the closest command under `references/commands/` when they need a complete workflow.
2. Load the named individual skills above when the task needs focused domain guidance.
3. Preserve the upstream command sequence, then adapt the final output to the user's actual product, audience, and constraints.

## Provenance

- Source repo: https://github.com/Owl-Listener/designer-skills
- Source commit: `152fc2a19985b061971c61efbf45e675517005c8`
- Source plugin path: `ux-strategy/`
- License: MIT
