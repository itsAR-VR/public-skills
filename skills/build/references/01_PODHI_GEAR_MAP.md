# Podhi gear map: local skills

This is the concrete operating map for Podhi build work.

## Core decision

Keep explicit gears. Do not collapse planning, implementation, review, QA, and
shipping into one pass.

Podhi already has:
- a persistent browser tool
- skill routing
- planning/review skills
- commit/push skills
- agent orchestration

So the right move is to route each build mode onto the native skill stack.

## Mapping table

| Build mode | Native mapping | Why |
|---|---|---|
| `plan` | `plan` + scope challenge in phase docs | keep purpose and risk explicit before coding |
| `eng-review` | `phase-gaps` | architecture, gaps, tests, failure modes |
| `review` | `phase-review` + `code-review` when needed | keep review distinct from implementation |
| `browse` | `browse-qa` | use browser evidence for UI-facing work |
| `ship` | `commit-work` + repo-specific ship path | keep release discipline |
| `retro` | doctrine + learnings update after major runs | useful after large work |

## Podhi command plan

### Canonical entrypoint

- `/build "<goal>"`

### Gear-aware usage

- `/build --gear plan "<goal>"`
- `/build --gear eng-review --phase docs/planning/phase-N`
- `/build --gear implement --phase docs/planning/phase-N`
- `/build --gear review --phase docs/planning/phase-N`
- `/build --gear browse-qa --url <target> --routes ...`
- `/build --gear ship`
- `/build --gear retro`

This gives us explicit modes without exploding the command surface.

## What to keep aggressively

- explicit mode switching
- screenshot-driven browser QA
- treating review as distinct from implementation
- keeping ship/release steps separate from "figure out what to build"
- retro/learning as a real lane after large work

## Build chain

```text
plan -> skill-oracle -> phase-gaps -> terminus-maximus -> phase-review/code-review -> browse-qa -> commit-work
```
