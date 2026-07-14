# Exact Match Acceptance

Use this when a visual reference exists and the user expects the implemented UI
to look like the reference.

## Reference

- Target surface:
- Reference source:
- Match level: exact / close
- Desktop viewport:
- Mobile viewport:

## Must Match

- Layout structure:
- Alignment and grid:
- Spacing density:
- Type scale and weight:
- Color roles:
- Surface treatment:
- Radius and borders:
- Shadow/depth:
- Component anatomy:
- Interaction states:
- Mobile collapse:
- Typography source/fallback:
- Localization/long-text behavior:
- Visual integrity blockers:

## Allowed Adaptations

- Product content:
- Product brand colors:
- Real assets available in repo:
- Accessibility corrections:
- Legal/license constraints:
- Performance constraints:

## Screenshot Review

- Reference screenshot/path:
- Implementation desktop screenshot:
- Implementation mobile screenshot:
- Biggest visible mismatch:
- Second biggest visible mismatch:
- Third biggest visible mismatch:
- Visual blockers remaining:
- Flow/state proof:

## Pass/Fail

- Pass only when the implementation materially resembles the reference at the
  requested match level.
- Fail when the UI only borrows vague mood, uses a generic template, or leaves
  obvious layout/type/spacing/surface mismatches unresolved.
- Fail when any blocker-class visual defect remains: overlap, clipped text,
  unresolved overflow, weird boxes/cards, bad mobile collapse, bad layering,
  weak focus/contrast, or critical truncation.
- If failing, patch the blocker or largest mismatch and review again.
