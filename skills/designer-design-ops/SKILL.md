---
name: designer-design-ops
description: "Streamline design operations with critique frameworks, handoff specs, sprint planning, review processes, and team workflows. Use when the user asks for design ops workflows, command routing, or the Owl-Listener designer-skills design-ops plugin."
license: MIT
metadata:
  author: MC Dean
  source: https://github.com/Owl-Listener/designer-skills
  source_commit: 152fc2a19985b061971c61efbf45e675517005c8
  upstream_plugin: design-ops
---

# design-ops

Streamline design operations with critique frameworks, handoff specs, sprint planning, review processes, and team workflows.

This is the Goated Skills wrapper for the upstream Owl-Listener `design-ops` plugin. Use it to choose the right imported design skill and command workflow.

## Available Skills

- `design-critique`
- `design-debt-audit`
- `design-impact-reporting`
- `design-qa-checklist`
- `design-review-process`
- `design-sprint-plan`
- `handoff-spec`
- `team-workflow`
- `version-control-strategy`

## Available Commands

- `design-ops:handoff` - see `references/commands/handoff.md`
- `design-ops:plan-sprint` - see `references/commands/plan-sprint.md`
- `design-ops:setup-workflow` - see `references/commands/setup-workflow.md`

## How To Use

1. Match the user's design task to the closest command under `references/commands/` when they need a complete workflow.
2. Load the named individual skills above when the task needs focused domain guidance.
3. Preserve the upstream command sequence, then adapt the final output to the user's actual product, audience, and constraints.

## Provenance

- Source repo: https://github.com/Owl-Listener/designer-skills
- Source commit: `152fc2a19985b061971c61efbf45e675517005c8`
- Source plugin path: `design-ops/`
- License: MIT
