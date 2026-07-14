# Design Architecture Map

Research date: 2026-05-18

Purpose: define the full architecture of good UI design so Codex and Claude do
not treat design as a palette, a component library, or a screenshot pass. Use
this before implementation for serious UI work, especially no-reference builds.

## Architecture Layers

Work through these layers in order. Do not jump to visual style before the
product job, typography, layout, states, and proof rules are clear.

| Layer | Decision to make | Proof or artifact |
| --- | --- | --- |
| 1. Product evidence | What do we know about the user, task, evidence, and assumptions? | research contract, assumption log, or validation plan |
| 2. Product job | What job does the surface do, for whom, and what should be easier after this screen exists? | one-sentence user job plus primary action |
| 3. Information architecture | What must users find, compare, decide, or complete? | navigation/section map, labels, search/filter plan |
| 4. Service journey | What happens before, during, after, and across roles/channels? | journey table with handoffs, failure paths, receipts |
| 5. Direction | What named design direction fits the product type and audience? | `direction_id` or reference packet |
| 6. Brand system | What voice, typography posture, icon family, imagery, surface language, and misuse rules apply? | `DESIGN.md` or brand bootstrap |
| 7. Typography | Which type families, scale, weights, line lengths, script support, and fallback stack fit the product? | typography/cultural system entry |
| 8. Layout and rhythm | What grid, spacing rhythm, density, alignment, responsive collapse, and page width apply? | layout notes and viewport plan |
| 9. Components | What component anatomy, local tokens, variants, and interaction states are needed? | component/state plan |
| 10. Content design | What labels, helper text, messages, dates, numbers, and recovery copy make the workflow clear? | copy notes and error/success wording |
| 11. Motion and feedback | What motion explains state, continuity, loading, or one brand moment? | motion class and reduced-motion rule |
| 12. Accessibility and inclusion | What contrast, focus, target size, keyboard, screen reader, language, direction, cognitive load, and cultural risks apply? | accessibility/i18n/cognitive notes |
| 13. Privacy and trust | What data, permission, payment, approval, destructive, or security boundaries must be understood? | trust/privacy checklist and recovery path |
| 14. Web discovery | For public pages, how will the page be found, previewed, scanned, and indexed? | metadata, headings, links, structured data |
| 15. Performance and perceived speed | What budgets keep the design fast, stable, and responsive? | Core Web Vitals, asset budgets, loading plan |
| 16. Data and media | What charts, maps, images, icons, illustrations, files, or canvas states support the job? | data/media source and truth check |
| 17. Measurement and learning | How will we know the design worked after launch? | metric, funnel, event plan, experiment or review date |
| 18. Visual integrity | What would make this look broken, off, cramped, overlapped, clipped, or amateur? | visual integrity report |
| 19. Proof loop | What screenshots, state captures, Storybook stories, visual regression, or blockers prove the result? | desktop/mobile/adaptive/state proof paths |
| 20. Governance | What should be saved for future builds? | `DESIGN.md`, taste ledger, source notes, token changes |

## Architecture Rules

- Every serious design pass must name the product job, primary action, and
  recovery path before choosing decoration.
- When evidence is missing, record the assumption and the fastest validation
  path instead of pretending the decision is proven.
- No-reference work must choose one `direction_id`, one source recipe, and one
  typography posture before coding.
- Reference-led work must extract structure, hierarchy, typography, spacing,
  surfaces, states, motion, and responsive behavior before coding.
- Design is not done until visual integrity is checked: no overlap, no clipping,
  no text overflow, no incoherent card/box nesting, no bad mobile collapse, no
  hidden focus state, and no obvious hierarchy conflict.
- If a product lacks brand memory, fill the brand bootstrap and typography
  decisions before adding one-off colors, fonts, shadows, or radii.
- If a product is multilingual, international, or culturally specific, treat
  typography, line height, text expansion, reading direction, symbols, dates,
  currencies, and color meaning as first-class design work.
- If a surface is public web, discovery and speed are design requirements:
  metadata, heading outline, share preview, structured data where relevant,
  image/font/script budget, and layout stability must be considered.
- If a surface is a platform or workflow, the whole journey matters: roles,
  handoffs, status, failure, recovery, receipts, and post-launch measurement
  must be considered.
- Public source code is a supply source, not the architecture. The architecture
  decides what to copy, rewrite, or ignore.

## Plain-English Use

If the user asks for a new build without a reference, this map should force Codex to
make the same decisions a good product designer would make before opening the
code editor. It should prevent the default AI failure mode: attractive-looking
but generic UI that breaks once real text, states, mobile, or culture-specific
content enters the screen.
