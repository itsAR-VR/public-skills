# Motion Budget Checklist

Research date: 2026-05-18

Purpose: make animation useful, performant, and accessible instead of decorative
noise.

Primary sources:

- Apple motion: https://developer.apple.com/design/human-interface-guidelines/motion
- web.dev animations and performance: https://web.dev/articles/animations-and-performance
- web.dev prefers-reduced-motion: https://web.dev/articles/prefers-reduced-motion
- Apple reduced motion criteria: https://developer.apple.com/help/app-store-connect/manage-app-accessibility/reduced-motion-evaluation-criteria
- Lenis: https://github.com/darkroomengineering/lenis

## Motion Jobs

Use motion only when it does one of these jobs:

- feedback: confirm press, selection, success, failure
- orientation: show where something came from or went
- continuity: preserve context across list/detail, modal, route, tab, or filter
- loading clarity: show progress or skeleton-to-content transition
- attention: highlight one important change
- brand moment: one deliberate public/marketing/launch moment

## Budget Rules

- Default to transform and opacity.
- Avoid animating layout-heavy properties unless measured and justified.
- Frequent interactions get less motion than rare brand moments.
- Operational dashboards and dense tools should use low-motion feedback.
- Scroll storytelling is for public/editorial pages, not daily work queues.
- `prefers-reduced-motion` must have an alternate behavior.
- Meaning-bearing motion needs a non-motion cue: text, icon, highlight, or
  state change.
- Avoid permanent 60fps loops unless the surface is a game/canvas/active
  simulation and performance is verified.

## Packet Fields

- motion_job:
- animated_elements:
- duration_range:
- easing:
- performance_risk:
- reduced_motion_variant:
- non_motion_equivalent:
- animation_proof:
