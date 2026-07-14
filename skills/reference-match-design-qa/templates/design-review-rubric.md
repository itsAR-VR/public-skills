# Design Review Rubric

Use this before saying meaningful UI work is done.

Score each area 0-2:

- 0 = missing or visibly weak
- 1 = acceptable but needs polish
- 2 = strong

## Review

| Area | Score | Notes |
| --- | ---: | --- |
| Product fit |  | Does this feel like the product, not a generic template? |
| Product evidence |  | Are the user job, top task, assumptions, and research/validation plan named where risk warrants it? |
| Information architecture |  | Are labels, navigation, section structure, search/filter behavior, and recovery paths clear? |
| Reference/no-reference target match |  | Does it match the packet's chosen layout, spacing, type, surfaces, and mood? |
| Information hierarchy |  | Is the most important action or status obvious first? |
| Layout and alignment |  | Are grids, edges, spacing, and rhythm intentional? |
| Typography |  | Are sizes, weights, line heights, and labels readable and consistent? |
| Content design |  | Are labels, helper text, empty/loading/error/success copy, and commitments plain and useful? |
| Color and contrast |  | Are colors purposeful, accessible, and not one-note? |
| Surfaces and depth |  | Do cards, panels, borders, shadows, and radius feel coherent? |
| Interaction states |  | Are hover, focus, active, disabled, loading, empty, error, and success states covered where relevant? |
| Interaction accessibility |  | Are keyboard path, focus return, status announcements, target sizes, and drag/drop alternatives covered where relevant? |
| Motion |  | Does motion clarify state or hierarchy without distracting? |
| Mobile/adaptive behavior |  | Does the layout work across mobile, intermediate, desktop, safe-area, input-mode, and container-size changes? |
| Performance/perceived speed |  | Are Core Web Vitals, font/image/script/motion budgets, loading states, and layout shift risks handled where relevant? |
| Website discovery/SEO |  | For public pages, are title, meta, canonical, Open Graph, headings, structured data, and link paths handled? |
| Measurement |  | Is the success metric, funnel/event plan, guardrail, rollout, or post-launch review defined where relevant? |
| Service journey |  | Are roles, handoffs, notifications, failure paths, receipts, and return states handled for multi-step products? |
| Source quality |  | Did the build use the right reference/code/source lane instead of generic guessing? |
| Code adaptation |  | Were copied or adapted components rewritten into the product's local tokens, states, and conventions? |
| Accessibility basics |  | Are contrast, labels, zoom/text spacing, reduced motion, and screen-reader basics considered? |
| Cognitive accessibility/privacy |  | Are memory load, plain language, undo/back paths, permission rationale, and opt-out/revoke paths covered? |
| Product truth |  | Are metrics, examples, claims, and proofs real or clearly placeholder-safe? |
| Typography and cultural fit |  | Are font source, fallback, script support, localization expansion, and cultural notes handled where relevant? |
| Visual integrity |  | Are overlap, clipping, text overflow, weird boxes/cards, mobile collapse, and layer conflicts absent? |

## Pass Rules

- Reference-led work does not pass if it only captures a vague vibe while
  obvious layout, spacing, typography, surface, or mobile mismatches remain.
- No-reference work does not pass if it looks like generic AI output, a default
  component library demo, or a decorative landing page pasted onto a product
  workflow.
- For meaningful UI work, every blocker-class visual defect must be fixed before
  done unless there is a concrete blocker.
- A copied component does not pass until it feels native to the product instead
  of pasted from a gallery.
- A typography choice does not pass for global or culture-sensitive products
  until fallback/script coverage and text expansion are named.
- A public web page does not pass if metadata, share preview, heading outline,
  indexability, or basic page-performance risks are unaddressed.
- A platform or multi-step app flow does not pass if the journey, failure path,
  receipt/confirmation, and measurement plan are missing.

## Visual Blocker Gate

- Overlap/occlusion:
- Clipped text:
- Text overflow:
- Awkward hierarchy:
- Weird boxes/cards:
- Broken responsive collapse:
- Bad layering/z-index:
- Weak contrast/focus:
- Critical truncation:
- done_allowed:

## Biggest Mismatches

1. TBD
2. TBD
3. TBD

## Must Fix Before Done

- TBD

## Acceptable Follow-Up

- TBD

## Proof

- Desktop screenshot:
- Mobile screenshot:
- Build/typecheck:
- Visual review report:
- Notes:
