# Interaction Accessibility Checklist

Research date: 2026-05-18

Purpose: catch interaction failures that a visual screenshot may miss:
keyboard behavior, focus order, focus return, custom-widget semantics, names,
status updates, drag alternatives, and agent/tool state clarity.

Primary sources:

- WAI-ARIA Authoring Practices Guide: https://www.w3.org/WAI/ARIA/apg/
- WCAG 2.2 updates: https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/
- WCAG 2.2 Understanding: https://www.w3.org/WAI/WCAG22/Understanding/
- Primer accessibility design guidance: https://primer.style/accessibility/design-guidance/
- Primer Copilot accessibility principles: https://primer.style/accessibility/foundations/copilot-principles/

## Rules

- Use semantic HTML first.
- If building a custom widget, name the APG pattern or explain why no APG
  pattern applies.
- Interactive controls need visible labels or accessible names that match visible
  text when possible.
- Keyboard order must follow the visual/task order.
- Focus must be visible, not hidden behind sticky headers, modals, or overlays.
- Focus must return to the trigger after modal/sheet/popover close.
- Escape/close behavior must be defined for overlays.
- Drag interactions need a non-drag alternative when the action is meaningful.
- Touch targets must meet WCAG 2.2 target-size minimum as a floor, with larger
  targets for primary mobile actions.
- Loading, saving, streaming, tool-running, error, and success states must be
  perceivable, not just color changes.
- Agent/tool status updates must be attributable: users should know what is
  running, what needs approval, what failed, and what proof was produced.

## Packet Fields

- semantic_html_plan:
- custom_widget_apg_pattern:
- keyboard_map:
- focus_order:
- focus_return:
- escape_close_behavior:
- accessible_names:
- status_update_behavior:
- drag_alternative:
- target_size_floor:
- agent_status_accessibility:

## Done Gate

- keyboard/focus checked:
- custom widgets mapped:
- hidden focus risk:
- drag alternative present:
- status updates perceivable:
- accessibility blocker remaining:
