# Visual Review Report

Use this after implementing a meaningful UI change. The goal is to force the
blocker-class visual issues and largest remaining mismatches into the open
before calling the design done.

- Target surface:
- Mode: reference-led / no-reference
- Pattern family:
- Selected design pattern(s):
- Reference packet or no-reference packet:
- Product `DESIGN.md`:
- Desktop screenshot:
- Mobile screenshot:
- Build/typecheck:
- Browser/Storybook/Browser Harness proof:
- Accessibility proof:
- Research/IA proof:
- Website discovery/SEO proof:
- Performance proof:
- Measurement/analytics proof:
- Service journey proof:
- Figma/Code Connect context, if used:
- Repair playbook used:
- Visual integrity gate used:
- done_allowed: yes / no

## Source Lane Used

- Real-product UX reference:
- Pullable code source:
- Dashboard/app shell source:
- Universal pattern library source:
- Motion source:
- Design-system primitive source:
- Pro design resource library source:
- Why these were chosen:

## What Improved

- Hierarchy:
- Layout/density:
- Typography:
- Color/surfaces:
- Components/states:
- Motion:
- Mobile:

## Reference Or Packet Match

| Area | match / mismatch / blocker | Note |
| --- | --- | --- |
| Layout |  |  |
| Hierarchy |  |  |
| Spacing |  |  |
| Typography |  |  |
| Color and surface |  |  |
| Component anatomy |  |  |
| States |  |  |
| Motion |  |  |
| Responsive behavior |  |  |
| Accessibility |  |  |
| Content design |  |  |
| Research/IA |  |  |
| Performance |  |  |
| Website discovery/SEO |  |  |
| Measurement |  |  |
| Service journey |  |  |

- Must-match items satisfied:
- Biggest remaining mismatch:
- Second mismatch:
- Third mismatch:
- Product constraint causing any mismatch:

## Visual Blockers

Any `fail` means the design is not done until fixed, re-shot, or named as a
concrete blocker.

| Blocker | pass / fail / blocked | Screenshot/state | Note |
| --- | --- | --- | --- |
| Overlap / occlusion |  |  |  |
| Clipped text |  |  |  |
| Text overflow |  |  |  |
| Awkward hierarchy |  |  |  |
| Weird boxes/cards |  |  |  |
| Cramped controls |  |  |  |
| Misaligned grid |  |  |  |
| Broken responsive collapse |  |  |  |
| Bad layering / z-index |  |  |  |
| Weak contrast / focus |  |  |  |
| Awkward whitespace |  |  |  |
| Typography mismatch |  |  |  |
| Critical truncation |  |  |  |
| Unclear state |  |  |  |

## Flow Proof Required

- User sequence checked:
- Primary action checked:
- Recovery path checked:
- Trust/commitment step checked:
- State transition proof:
- Product-specific anatomy proof:
- Service journey/handoff proof:
- Measurement or event proof:

## Discovery, Speed, And Measurement

- Metadata/title/meta/canonical checked:
- Open Graph/share preview checked:
- Heading outline checked:
- Structured data checked:
- Core Web Vitals or Lighthouse checked:
- Font/image/script budget checked:
- Loading/layout shift checked:
- Analytics/events checked:
- Experiment or rollout criteria checked:

## Repair Pass

- repair_order:
- patch_applied:
- re_shot_desktop: yes / no / blocked
- re_shot_mobile: yes / no / blocked
- state_recheck:
- accessibility_recheck:
- remaining_blocker:
- visual_blockers_remaining:

## Anti-Slop Check

- No generic purple/blue AI gradient:
- No decorative blobs/glows without purpose:
- No card soup where a workflow layout is better:
- No fake metrics/logos/testimonials:
- No missing empty/loading/error/success states where relevant:
- No missing hover/focus/disabled/destructive states where relevant:
- No mobile text overlap or unusable touch targets:
- No animation without a clear UX/brand job:
- Reduced-motion behavior exists when motion is used:
- Icons come from one consistent family unless justified:
- Typography scale and line lengths are deliberate:
- Contrast/focus/target-size floor checked:
- Long labels, translated strings, names, numbers, prices, or paths checked:
- Layer conflicts checked for sticky bars, sheets, modals, popovers, tooltips, and toasts:
- Keyboard path and focus return checked:
- Screen-reader status announcements checked:
- Cognitive load and memory burden checked:
- Permission/privacy rationale checked:

## Proof Lane

- Storybook component states checked:
- Browser Harness page screenshots checked:
- Visual regression checked:
- Automated accessibility checked:
- Manual keyboard/focus check:
- Localization/RTL/long-text stress checked:
- Visual integrity gate result:

## Next Patch If Time Allows

1. TBD
2. TBD
3. TBD
