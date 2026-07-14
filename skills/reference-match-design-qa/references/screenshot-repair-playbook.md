# Screenshot Repair Playbook

Research date: 2026-05-18

Purpose: make visual QA actionable after screenshots. Do not just say what is
wrong. Patch all blocker-class defects first, then patch the highest-impact
remaining issue, re-shoot, and report what remains.

## Repair Order

Use this order for both reference-led and no-reference work:

0. Visual blockers
   - Fix overlap, clipped text, unresolved text overflow, broken mobile
     collapse, bad layering, weak focus/contrast, critical truncation, and
     weird nested boxes/cards before treating anything as polish.

1. Layout and spacing
   - Fix grid, alignment, grouping, overflow, fold, and mobile collapse.
   - If the screen feels cheap, check spacing rhythm before changing colors.
2. Typography and measure
   - Fix heading hierarchy, body size, line height, line length, label scale,
     tabular numbers, and truncation.
3. Surfaces, borders, and depth
   - Fix card soup, nested cards, random borders, weak elevation, blur/glass
     overuse, and unclear panel hierarchy.
4. Color and state clarity
   - Fix low contrast, color-only status, unclear selected/disabled/error
     states, and semantic misuse.
5. Component anatomy
   - Fix button/input/table/card/nav anatomy, icon weight, hit targets, and
     control placement.
6. Motion and polish
   - Add or reduce motion only after static hierarchy works. Respect reduced
     motion.
7. Content and proof
   - Remove fake metrics/logos/testimonials. Replace vague copy with action,
     recovery, or proof copy.

## Re-Shoot Rules

- Re-shoot desktop after any layout, typography, color, or surface patch.
- Re-shoot mobile after any width, nav, table, form, or primary-action patch.
- Re-run Storybook/visual states when component anatomy changes.
- Re-run accessibility checks when contrast, focus, labels, or targets change.
- If re-shooting is blocked, name the exact blocker and the smallest alternate
  proof.

## Mismatch Triage

| Symptom | First fix | Avoid |
| --- | --- | --- |
| Everything feels equally important | Rebuild hierarchy and grouping | Adding glow, blur, or gradients |
| Screen feels generic SaaS | Choose a direction_id and source recipe | Asking for "more premium" |
| Dense screen feels chaotic | Reduce panels, align groups, prioritize states | Turning everything into cards |
| Mobile feels squeezed | Reorder content and actions for first tap | Shrinking desktop layout |
| Reference match is off | Fix layout/spacing before color details | Tweaking shadows first |
| AI/agent UI feels like plain chat | Add tool state, proof, artifacts, approvals | Adding avatar bubbles only |
| Dashboard feels fake | Remove fake metrics, clarify decision question | Adding more charts |
| Form feels untrustworthy | Fix labels, help, validation, recovery | Styling placeholders |

## Report Fields

Every visual review should include:

- repair_order:
- patch_applied:
- re_shot_desktop: yes / no / blocked
- re_shot_mobile: yes / no / blocked
- state_recheck:
- accessibility_recheck:
- remaining_blocker:
- visual_blockers_remaining:
- done_allowed:
