# Design Doctrine And QA

Research date: 2026-05-18

Purpose: turn professional design guidance into hard checks that Codex and
Claude must use when building UI. This file is for the judgment layer: how to
avoid generic AI-looking screens, how to decide whether the screen is usable,
and how to prove the design is actually better.

## Source Base

- Apple HIG and Apple UI design tips: platform conventions, hierarchy,
  alignment, direct manipulation, readable text, purposeful motion, and
  generous touch targets.
- Material design principles: hierarchy through typography, grids, space,
  scale, color, and focus order.
- NN/g heuristics: visibility of status, real-world language, consistency,
  error prevention, recognition over recall, minimalist design, and useful
  recovery.
- WAI/WCAG 2.2: contrast, focus, structure, labels, target size, reflow, and
  keyboard accessibility.
- Storybook testing guidance: stories are QA fixtures for states, not just
  documentation.
- W3C Design Tokens and Atlassian design tokens: semantic token governance,
  theming, and drift prevention.
- Google Fonts, Noto, Fontsource, Typewolf, Apple HIG, Material, Carbon, W3C
  i18n, and web.dev: typography, script support, localization, line length,
  and culturally aware visual decisions.
- Carbon, Atlassian, and other mature systems: empty states, loading states,
  error copy, and governance examples.
- NN/g visual design principles: scale, visual hierarchy, balance, contrast,
  and Gestalt grouping.
- Color semantics and color psychology research: color meaning depends on
  concepts, audience, task, and context; broad color-emotion claims are weak
  without product-specific evidence.
- Figma, Frontify, Primer, GitHub Brand Toolkit, USWDS, and Carbon: brand
  systems, token governance, visual identity, motion, accessibility, and
  design-system operating models.
- Refactoring UI, Learn UI Design, LearnVisual.Design, DesignCourse, and Kevin
  Powell: practical developer-to-designer training for hierarchy, spacing,
  typography, color, layout, and CSS implementation craft.
- YouTube/video sources checked during the 2026-05-18 sweep: Steve Schoger's
  Refactoring UI videos, Figma design-system videos, Memberstack/Build Great
  Products vibe-coding design videos, Jesse Showalter color theory, Kevin
  Powell CSS implementation lessons, and DesignCourse refactor walkthroughs.

## Non-Negotiable Doctrine

1. **Hierarchy first.** Decide what the user must notice first, second, and
   third. Use layout, type, contrast, spacing, and grouping before decorative
   effects.
2. **Platform-first, not trend-first.** Respect the product platform and user
   workflow before applying a trendy visual style.
3. **Product type first.** A dashboard, checkout, editor, calendar, AI
   workspace, CRM, support inbox, and landing page should not share one generic
   composition.
4. **Semantics over decoration.** Color, icons, badges, motion, and emphasis
   must communicate status, action, priority, or product character.
5. **Color psychology is contextual.** Do not assume a color has a universal
   meaning. Document why the palette fits the audience, product job, cultural
   context, and concept-color mapping.
6. **Brand systems beat palettes.** A real brand system includes typography,
   layout, imagery, icon style, motion, voice, usage rules, and governance.
7. **Semantic tokens beat paint names.** Prefer purpose-based token names that
   map to UI roles, states, and modes instead of raw color names.
8. **State coverage is design quality.** Empty, loading, error, disabled,
   focus, hover, success, selected, destructive, permission-limited, and mobile
   states are part of the design, not cleanup.
9. **Accessibility is the floor.** Use WCAG AA as the minimum and follow
   stronger platform guidance where relevant.
10. **Tokens beat raw values.** Use semantic tokens when the repo has them. If a
   token is missing, add a small local token or document the exception.
11. **Motion needs a job.** Motion should explain change, preserve orientation,
   provide feedback, clarify loading, or create one deliberate brand moment.
12. **Copy is UX.** Button, error, empty, success, and loading copy should say
   what happened, what it means, and what to do next.
13. **Video learning becomes heuristics.** YouTube research is useful only when
    it produces 3-5 reusable rules and one anti-pattern list that are applied
    to the current build.
14. **Proof beats taste claims.** Meaningful UI work needs desktop/mobile
    screenshots or a concrete blocker.
15. **Visual blockers stop completion.** Overlap, clipped text, unresolved
    overflow, weird boxes/cards, broken hierarchy, bad mobile collapse,
    z-index/layer conflict, weak focus/contrast, and critical truncation are
    blockers, not subjective polish.
16. **Typography is a system choice.** Pick a font source, type posture,
    fallback stack, script/language support, line length, numeric behavior, and
    localization expansion rule where relevant.

## Preflight Packet

Before coding a serious UI surface, capture:

- product type
- target platform and viewport expectations
- primary user job
- workflow density: public/marketing, daily app, dense operations, mobile,
  canvas, editor, commerce, or AI/agent
- one art direction or one reference-led match target
- 2-4 sources max
- primary pattern family
- source lane
- primary source database category and at most two supporting database
  categories
- typography source, fallback stack, and script/language support where relevant
- focal point, scan order, and grouping cues
- palette role rationale and color-meaning assumptions
- brand-system requirements: typography, layout, imagery, icons, motion, voice,
  and misuse rules when relevant
- required states
- accessibility risks
- motion class: none, app-safe state motion, loading/empty-state motion,
  branded vector motion, public-site hero motion, success effect, or 3D/canvas
- screenshot proof required
- visual integrity blocker list

## Design QA Rubric

Score these before calling a UI polished:

| Area | Good Means | Common Failure |
| --- | --- | --- |
| Hierarchy | The next action and primary information are obvious. | Everything has equal weight. |
| Layout | Related items are grouped and aligned. | Random spacing and disconnected sections. |
| Typography | Type scale, weight, line length, and line height guide reading. | Oversized headings or cramped text. |
| Color | Color communicates role/status and meets contrast. | Decorative color with unclear meaning. |
| Surfaces | Cards, borders, shadows, and backgrounds create structure. | Nested cards or glass everywhere. |
| States | Empty/loading/error/success/focus/disabled/mobile states exist. | Only the default happy path is designed. |
| Motion | Motion has a clear purpose and reduced-motion fallback. | Motion is decorative or distracting. |
| Accessibility | Keyboard, labels, focus, contrast, and targets are handled. | Only mouse/visual use works. |
| Mobile | The screen is usable on a phone-sized viewport. | Desktop layout is squeezed. |
| Brand | The screen has product-specific character. | It looks like a generic AI SaaS template. |
| Source database | Typography, colors, boxes, UX flow, motion, icons/media, localization, and proof sources fit the product. | The screen mixes random libraries or trendy fonts without a reason. |
| Visual integrity | No overlap, clipping, unresolved overflow, weird boxes, bad layering, or critical truncation. | The screen looks fine at one size but breaks with real content or mobile. |

## Anti-Generic Checks

Reject or patch these:

- centered glass card as the default app layout
- purple/blue gradient as the main identity without brand reason
- decorative blobs, bokeh, or glow with no product purpose
- repeated card grid when the workflow needs table, timeline, board, editor, or
  canvas structure
- fake metrics, fake logos, fake testimonials, or unsupported claims
- marketing hero composition inside a dense tool
- no empty/loading/error states
- no mobile screenshot
- no focus or keyboard states
- raw colors/radii/shadows where tokens exist
- animation that does not explain state or support brand memory
- clipped labels, overlapping controls, card-inside-card clutter, accidental
  horizontal scroll, hidden primary actions, or critical truncation

## Developer-Designer Study Loop

Use this loop when improving the skill or training design taste:

1. Pick a real screen from a high-quality product or reference gallery.
2. Redraw the hierarchy in words: primary action, secondary action, proof,
   recovery path.
3. Extract spacing rhythm, type scale, color roles, surfaces, states, and
   motion.
4. Rebuild a local version using the target repo's components and tokens.
5. Capture before/after screenshots.
6. Write one sentence explaining why the new version is easier to use.

This loop matters because good design is not a link list. It is repeated
comparison between intent, implementation, and proof.

## Storybook And Visual Proof

Use Storybook-style stories when component states matter more than the full
route. Stories should cover meaningful states:

- default
- loading
- empty
- error
- success
- disabled
- focus/keyboard
- mobile or narrow layout
- long copy
- permission-limited
- destructive action

Use Browser Harness screenshots for route-level proof, especially when layout,
responsive behavior, or reference matching matters.

## Plain-English Outcome

When this doctrine is used correctly, the user can say "make this app look good"
without supplying a reference, and Codex should produce a more serious first
pass because it is forced to choose a product type, source lane, hierarchy,
states, motion class, and proof loop before it starts styling.
