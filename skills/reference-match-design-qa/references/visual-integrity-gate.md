# Visual Integrity Gate

Research date: 2026-05-18

Purpose: prevent visually broken UI from being called done. This is stricter
than a taste review. Any blocker-class defect means the build is not complete
until it is fixed, re-shot, or explicitly named as blocked with proof.

## Blocker Rule

Meaningful UI work is not done while any visual blocker is present.

Use this loop:

1. Capture desktop, mobile, and any meaningful intermediate/collapse screenshots.
2. Classify visual blockers using the table below.
3. Patch all blocker-class defects.
4. Re-shoot the affected viewport/state.
5. Repeat until `done_allowed: yes`, or name the exact blocker and owner
   decision needed.

## Visual Blockers

| Defect | What fails | Required fix |
| --- | --- | --- |
| Overlap / occlusion | Text, controls, cards, panels, modals, charts, maps, or media cover each other unintentionally. | Change layout, spacing, stacking, or responsive behavior and re-shoot. |
| Clipped text | Text is cut off vertically or horizontally without a deliberate reveal path. | Increase container, allow wrap, reduce copy, add reveal, or redesign component. |
| Text overflow | Long labels, numbers, emails, names, paths, prices, or translated strings escape the container. | Add wrap/truncate/reveal rules and prove with long-content case. |
| Awkward hierarchy | The wrong thing is visually dominant, scan order is unclear, or headings are too large/small for the surface. | Rebalance type, weight, spacing, grouping, and focal point. |
| Weird boxes/cards | Cards inside cards, decorative panels, inconsistent radii/shadows, or boxes that do not map to real grouping. | Remove unnecessary containers or define a clear surface model. |
| Cramped controls | Buttons, tabs, inputs, filters, or table actions are too tight to read/use. | Increase spacing, reduce density, group actions, or move secondary controls. |
| Misaligned grid | Baselines, columns, gutters, icons, badges, or card edges visibly drift. | Fix grid/flex alignment, spacing tokens, or component dimensions. |
| Broken responsive collapse | Mobile/tablet layout hides primary actions, creates horizontal scroll accidentally, stacks in the wrong order, or loses context. | Define collapse rules and re-shoot all meaningful modes. |
| Bad layering / z-index | Sticky bars, dropdowns, popovers, modals, sheets, tooltips, toasts, or drawers conflict. | Define layer map and focus/escape behavior; re-test overlay state. |
| Weak contrast / focus | Text, icons, borders, chart marks, focus rings, or status colors are hard to see. | Adjust tokens and verify contrast/focus visibility. |
| Awkward whitespace | Empty zones, uneven gutters, accidental gaps, or crowded clusters make the screen feel unfinished. | Normalize spacing rhythm and grouping. |
| Typography mismatch | Fonts, weights, casing, line height, letter spacing, or type scale conflict with product tone or readability. | Pick a type posture and apply it consistently. |
| Critical truncation | A primary action, price, status, name, error, warning, route, or legal commitment is truncated without reveal. | Never hide critical meaning; redesign the component. |
| Unclear state | Loading, empty, error, success, disabled, selected, destructive, or permission states are missing or visually ambiguous. | Add state-specific copy, icon/status, and proof. |

## Required Stress Cases

Select stress cases before coding and prove the relevant ones after coding:

- long person/business names
- long labels and translated strings
- long numbers, prices, dates, and percentages
- long emails, file names, paths, URLs, or addresses
- dense filters or bulk action bars
- empty state plus banner/alert
- table overflow and hidden columns
- multi-line buttons or tabs
- 200% text zoom or larger system text where feasible
- mobile keyboard open state for forms/search/chat
- safe-area and bottom-action layout on mobile
- modal over sheet, popover over sticky header, tooltip near edge
- chart legend overflow or map marker clustering

## Responsive Rules

- Record the first collapse point.
- Say what wraps, truncates, scrolls, pins, hides, or moves.
- Horizontal scroll is allowed only for deliberate data tables, timelines,
  canvases, code blocks, maps, or media strips; it must be discoverable.
- Primary actions must remain visible or reachable on mobile.
- Touch targets must be at least 24x24 CSS px as a floor, with larger targets
  preferred for primary mobile actions.
- Use container queries when a component's layout depends on its parent width,
  not just viewport width.

## Layer Rules

Every serious app shell or interactive surface should define:

- `layer_map`
- `overflow_containers`
- `sticky_or_fixed_elements`
- `modal_sheet_popover_tooltip_order`
- `toast_position`
- `focus_trap_and_escape_behavior`
- `nested_card_exceptions`

## Done Gate

- visual_blockers_remaining:
- blocker_screenshots:
- re_shot_after_fix: yes / no / blocked
- done_allowed: yes / no

If `done_allowed` is `no`, do not say the design is complete.
