# Component Adaptivity Checklist

Research date: 2026-05-18

Purpose: make reusable UI adapt to its container, not only to the full viewport.
Use this for cards, panels, tables, sidebars, toolbars, editor surfaces, maps,
charts, mobile sheets, and any component that can appear in multiple layouts.

Primary sources:

- MDN CSS container queries: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_container_queries
- CSS Containment Level 3: https://www.w3.org/TR/css-contain-3/
- web.dev container queries: https://web.dev/learn/css/container-queries/
- MDN subgrid: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout/Subgrid

## Adaptivity Rules

- Define each reusable component's minimum useful width.
- Define what changes at compact, regular, and wide container sizes.
- Use container queries when component layout depends on the parent container.
- Use viewport media queries for page-level shell changes, not every component
  behavior.
- Define what wraps, truncates, scrolls, pins, hides, or moves.
- Use subgrid or shared grid variables when card/table alignment must line up
  across repeated items.
- Do not hide primary actions on small containers without a visible alternate.
- Horizontal scroll must be intentional and discoverable.

## Packet Fields

- component_min_width:
- component_max_width:
- container_breakpoints:
- compact_behavior:
- regular_behavior:
- wide_behavior:
- wrap_rules:
- truncation_rules:
- horizontal_scroll_allowed:
- subgrid_or_alignment_rules:
- proof_viewports_or_container_sizes:

## Done Gate

- first collapse point recorded:
- intermediate screenshot captured:
- long-content stress case captured:
- horizontal scroll intentional:
- primary action reachable:
