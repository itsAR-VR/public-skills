---
name: designer-visual-critique
description: "Visual critique skills for designers: analyse hierarchy, brand consistency, composition, and typography — then compile a prioritised fix list. Use when the user asks for visual critique workflows, command routing, or the Owl-Listener designer-skills visual-critique plugin."
license: MIT
metadata:
  author: MC Dean
  source: https://github.com/Owl-Listener/designer-skills
  source_commit: 152fc2a19985b061971c61efbf45e675517005c8
  upstream_plugin: visual-critique
---

# visual-critique

Visual critique skills for designers: analyse hierarchy, brand consistency, composition, and typography — then compile a prioritised fix list.

This is the Goated Skills wrapper for the upstream Owl-Listener `visual-critique` plugin. Use it to choose the right imported design skill and command workflow.

## Available Skills

- `critique-brand-consistency`
- `critique-composition`
- `critique-typography`
- `critique-visual-hierarchy`

## Available Commands

- `visual-critique:critique-screen` - see `references/commands/critique-screen.md`

## How To Use

1. Match the user's design task to the closest command under `references/commands/` when they need a complete workflow.
2. Load the named individual skills above when the task needs focused domain guidance.
3. Preserve the upstream command sequence, then adapt the final output to the user's actual product, audience, and constraints.

## Provenance

- Source repo: https://github.com/Owl-Listener/designer-skills
- Source commit: `152fc2a19985b061971c61efbf45e675517005c8`
- Source plugin path: `visual-critique/`
- License: MIT
