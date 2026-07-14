---
name: designer-design-systems
description: "Build, document, and maintain scalable design systems — from tokens and components to accessibility and theming. Use when the user asks for design systems workflows, command routing, or the Owl-Listener designer-skills design-systems plugin."
license: MIT
metadata:
  author: MC Dean
  source: https://github.com/Owl-Listener/designer-skills
  source_commit: 152fc2a19985b061971c61efbf45e675517005c8
  upstream_plugin: design-systems
---

# design-systems

Build, document, and maintain scalable design systems — from tokens and components to accessibility and theming.

This is the Goated Skills wrapper for the upstream Owl-Listener `design-systems` plugin. Use it to choose the right imported design skill and command workflow.

## Available Skills

- `accessibility-audit`
- `component-spec`
- `design-system-governance`
- `design-token`
- `documentation-template`
- `icon-system`
- `localization-design`
- `motion-system`
- `naming-convention`
- `pattern-library`
- `theming-system`

## Available Commands

- `design-systems:audit-system` - see `references/commands/audit-system.md`
- `design-systems:create-component` - see `references/commands/create-component.md`
- `design-systems:tokenize` - see `references/commands/tokenize.md`

## How To Use

1. Match the user's design task to the closest command under `references/commands/` when they need a complete workflow.
2. Load the named individual skills above when the task needs focused domain guidance.
3. Preserve the upstream command sequence, then adapt the final output to the user's actual product, audience, and constraints.

## Provenance

- Source repo: https://github.com/Owl-Listener/designer-skills
- Source commit: `152fc2a19985b061971c61efbf45e675517005c8`
- Source plugin path: `design-systems/`
- License: MIT
