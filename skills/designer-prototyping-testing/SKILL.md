---
name: designer-prototyping-testing
description: "Plan and execute design validation through prototyping strategies, usability testing, heuristic evaluation, and A/B experiments. Use when the user asks for prototyping testing workflows, command routing, or the Owl-Listener designer-skills prototyping-testing plugin."
license: MIT
metadata:
  author: MC Dean
  source: https://github.com/Owl-Listener/designer-skills
  source_commit: 152fc2a19985b061971c61efbf45e675517005c8
  upstream_plugin: prototyping-testing
---

# prototyping-testing

Plan and execute design validation through prototyping strategies, usability testing, heuristic evaluation, and A/B experiments.

This is the Goated Skills wrapper for the upstream Owl-Listener `prototyping-testing` plugin. Use it to choose the right imported design skill and command workflow.

## Available Skills

- `a-b-test-design`
- `accessibility-test-plan`
- `click-test-plan`
- `heuristic-evaluation`
- `prototype-strategy`
- `test-scenario`
- `user-flow-diagram`
- `wireframe-spec`

## Available Commands

- `prototyping-testing:evaluate` - see `references/commands/evaluate.md`
- `prototyping-testing:experiment` - see `references/commands/experiment.md`
- `prototyping-testing:prototype-plan` - see `references/commands/prototype-plan.md`
- `prototyping-testing:test-plan` - see `references/commands/test-plan.md`

## How To Use

1. Match the user's design task to the closest command under `references/commands/` when they need a complete workflow.
2. Load the named individual skills above when the task needs focused domain guidance.
3. Preserve the upstream command sequence, then adapt the final output to the user's actual product, audience, and constraints.

## Provenance

- Source repo: https://github.com/Owl-Listener/designer-skills
- Source commit: `152fc2a19985b061971c61efbf45e675517005c8`
- Source plugin path: `prototyping-testing/`
- License: MIT
