---
name: design-intelligence
description: Meta-router for serious UI/UX work. Encapsulates the full design-skill constellation in the repo (taste, shape, brand, layout, typeset, colorize, polish, delight, design-an-interface, premium-ui-components, landing-page-architecture, screenshot-to-code, and more). Picks the product type before styling, chooses reference-led vs no-reference mode, routes to the right specialist skill per phase (discover, explore, source, refine, polish, prove), and requires screenshot proof. Triggers on "design intelligence", "design-in", "design intel", "better UI/UX", "premium design", "less AI slop", "visual QA", "no-reference design", "reference match".
related_skills:
  - reference-match-design-qa
  - vibe-design-reference-libraries
  - ultra-review
  - taste-skill
  - design-taste-frontend
  - design-an-interface
  - shape
  - premium-ui-components
  - ecc-frontend-design
  - ui-styling
  - ui-skills
  - ui-ux-pro-max
  - frontend-agent
  - frontend-coding-agent
  - design-system-starter
  - design
  - screenshot-to-code
  - image-to-code-skill
  - images-taste-skill
  - landing-page-architecture
  - landing-page-guide-v2
  - layout
  - typeset
  - colorize
  - polish
  - delight
  - impeccable
  - brand
  - brand-alchemy
  - brand-guidelines
  - brandkit
  - canvas-design
  - theme-factory
  - svg-animations
  - ai-video-scroll-animation
  - ecc-liquid-glass-design
  - minimalist-skill
  - brutalist-skill
  - browse-qa
---

# Design Intelligence

Use this as the single, easy front door for serious UI/UX work.

This skill instructs the agent to stop guessing, pick the right product type,
study the right code-backed references, build the actual interface, and prove
the result with screenshots before calling the design done.

The canonical source for this skill lives in the public-skills repository.
Mirrors in `~/.claude/skills/` and `~/.codex/skills/` are maintained by the
sync-skills workflow — run it after editing source to refresh the mirrors.

## Routing Signals

Use this skill when the user says or implies: design intelligence, design-in,
design intel, better design, UI/UX design, reference match, no-reference
design, premium UI, less AI slop, visual QA, visual integrity, no overlap,
clipped text, typography/font database, design source database, UX database,
box/surface structure, cultural design, screenshot proof, animation, loading
screen, AI workspace, agent UI, ecommerce UI, editor UI, calendar UI, canvas
UI, dashboard UI, SEO design, performance budget, user research, information
architecture, service journey, design measurement, or cognitive accessibility.

The deep skills remain separate because they do different jobs, but the user
should not need to remember their names. Start here, then load the supporting
skills listed below.

## The One Command To Use

In Codex or Claude Code, use the slash command:

```text
/design-intelligence [what you want built or improved]
```

If the slash command is unavailable, paste this into any agent thread:

```text
Use the design-intelligence skill for this UI build.
If your environment supports skill loading (Claude Code Skill tool, Codex skill
loader), load the design-intelligence skill by name.
If you cannot load the skill file, still follow the design-intelligence contract:
pick the product type before styling, choose reference-led or no-reference mode,
activate only the conditional design gates that apply, build the actual UI, and
prove the result with desktop/mobile screenshots or a concrete blocker.
If I provide a reference, match the built UI to it and prove it with desktop/mobile screenshots.
If I do not provide a reference, choose a strong product-appropriate design direction yourself.
Use safe, reputable GitHub/component code when it helps, but inspect it for dangerous behavior before copying and rewrite it into the local product patterns.
```

## Primary Companion Skills (Always Available)

These three are the default load-list for any design-intelligence session:

1. `reference-match-design-qa`
   - Creates reference packets when the user provides a screenshot, URL, app
     example, taste reference, or optional Figma handoff.
   - Creates no-reference design packets when the user only says the design
     should be better.
   - Uses the universal code-backed pattern library to choose the product type
     before coding.
   - Requires desktop and mobile screenshot proof.

2. `vibe-design-reference-libraries`
   - Chooses code-backed sources such as shadcn/ui, ReUI, Magic UI, React Bits,
     Animate UI, Motion Primitives, assistant-ui, AI Elements, ElevenLabs UI,
     data-table libraries, editor libraries, calendar libraries, canvas
     libraries, and real-product UX galleries.
   - Provides original React/Tailwind starter patterns that can be adapted into
     a project.

3. `ultra-review`
   - Use at the end of meaningful work to check scope, safety, proof, blockers,
     and the exact next action.

## The Design Skill Constellation

`design-intelligence` is a **meta-router**. The deep work lives in specialized
companion skills that have been battle-tested across many projects in this
repo. Don't reinvent — route. Pick the right specialist by phase of the
design work. For the full descriptions, tradeoffs, and examples per skill,
read `references/design-skill-constellation.md`.

### Phase 1 — Discover & Plan (before any code)

| Skill | When to invoke |
|---|---|
| `shape` | New feature with no design memory; need a structured discovery interview → design brief before code |
| `taste-skill` | Need the Senior UI/UX Engineer voice to override generic LLM defaults; metric-based rules, strict component architecture. **Prefer this as the canonical handle.** |
| `design-taste-frontend` | Near-duplicate of `taste-skill` (identical description). Prefer `taste-skill`; kept here only because some workflows still invoke this name |
| `brand` | Brand voice, identity, messaging frameworks needed before visual choices |
| `brand-alchemy` | Naming, brand DNA discovery, domain availability — pre-launch identity work |
| `brand-guidelines` / `brandkit` | Existing brand standards exist; apply them or generate brand-board assets |

### Phase 2 — Explore Variants (compare options before committing)

| Skill | When to invoke |
|---|---|
| `design-an-interface` | Want to see 2-5 radically different interface designs for the same module, generated in parallel |
| `reference-match-design-qa` (no-reference mode) | Pick one `direction_id` from the art-direction catalog when the user has no visual example |
| `minimalist-skill` | Style direction: clean editorial, warm monochrome palette, typographic contrast, flat bento grids, muted pastels |
| `brutalist-skill` | Style direction: raw mechanical, Swiss typographic print + military terminal aesthetics, rigid grids, extreme type scale contrast |

### Phase 3 — Source & Build (real components, real UI)

| Skill | When to invoke |
|---|---|
| `vibe-design-reference-libraries` | Default code-backed source: shadcn/ui, ReUI, Magic UI, React Bits, Animate UI, Motion Primitives, assistant-ui, AI Elements |
| `premium-ui-components` | Polished/animated components (Magic UI, Aceternity, 21st.dev) |
| `frontend-design:frontend-design` (plugin) | Vercel official frontend design patterns — invoke via the Vercel plugin namespace |
| `ecc-frontend-design` | ECC's production-grade frontend patterns that avoid generic AI aesthetics |
| `ui-styling` | Implementation: shadcn/ui + Tailwind + Radix UI |
| `ui-skills` | Opinionated constraints layer for building better interfaces with agents (smaller than `ui-styling`; pure rules, no implementation) |
| `ui-ux-pro-max` | Broad catalog: 50+ styles, 161 palettes, 57 font pairings, 161 product types, 99 UX guidelines |
| `frontend-agent` | When the work needs an autonomous frontend agent loop (build → review → iterate) rather than direct edits |
| `frontend-coding-agent` | Similar to `frontend-agent` but tuned for code-heavy implementation tasks |
| `design-system-starter` | Bootstrap a new design system from scratch (tokens, components, accessibility, docs); also use when working within an existing design system |
| `design` | Logos (55 styles, Gemini AI), corporate identity programs (50 deliverables), banners (22 styles), icons (15 styles), social photos |
| `screenshot-to-code` | Figma/screenshot → HTML/Tailwind/React/Vue/Bootstrap code |
| `image-to-code-skill` / `images-taste-skill` | Generate the design image first, deeply analyze, then implement to match it |
| `landing-page-architecture` | 8-section conversion-focused landing page framework |
| `landing-page-guide-v2` | Next.js 14+ + ShadCN landing pages following 11-element framework |
| `canvas-design` | Static visual art: posters, .png/.pdf documents |

### Phase 4 — Refine Atoms (layout, type, color, motion)

| Skill | When to invoke |
|---|---|
| `layout` | Spacing, visual rhythm, hierarchy feels off; monotonous grids; alignment problems |
| `typeset` | Typography needs work: font choice, sizing, weight, readability, hierarchy |
| `colorize` | Design feels gray/dull/monochromatic; needs strategic color |
| `theme-factory` | Apply one of 10 preset themes or generate a new theme on-the-fly |
| `svg-animations` | SVG animations, animated logos, path animations, loading spinners |
| `ai-video-scroll-animation` | Scroll-driven video animations |
| `ecc-liquid-glass-design` | iOS 26 Liquid Glass material for SwiftUI/UIKit/WidgetKit |

### Phase 5 — Polish & Delight (final pass before shipping)

| Skill | When to invoke |
|---|---|
| `polish` | Final quality pass: alignment, spacing, consistency, micro-detail. User-invocable front door; runs design-system discovery and calls `impeccable` first |
| `impeccable polish` | Impeccable-family member; applies the `polish` prompt directly (skip discovery). Use when already inside an Impeccable workflow |
| `delight` | Add joy, personality, unexpected touches, micro-interactions. User-invocable front door |
| `impeccable delight` | Impeccable-family member; applies the `delight` prompt directly. Use when already inside an Impeccable workflow |
| `impeccable bolder` | Amplify safe/boring designs without breaking usability |
| `impeccable clarify` | UX copy, error messages, microcopy, labels, instructions |
| `impeccable` | Parent skill: production-grade frontend with high design quality, avoids generic AI aesthetics |

### Phase 6 — Visual QA & Proof (before declaring done)

| Skill | When to invoke |
|---|---|
| `reference-match-design-qa` (proof mode) | Desktop/mobile screenshot proof + mismatch review against reference packet |
| `browse-qa` | Browser screenshot proof of the deployed/local UI |
| `ultra-review` | End-of-work scope, safety, proof, blocker review |

### Routing Heuristic

Quick decision tree when the user asks for design help:

1. **No spec yet?** → start with `shape` (discovery)
2. **Need a voice/persona shift to override generic LLM defaults?** → `taste-skill` or `design-taste-frontend`
3. **User wants to see options before deciding?** → `design-an-interface`
4. **User has a reference?** → `reference-match-design-qa` reference-led mode + `screenshot-to-code` if direct conversion
5. **User has no reference but wants premium UI?** → `reference-match-design-qa` no-reference mode + `vibe-design-reference-libraries` source lanes
6. **Specific atomic problem (layout/type/color)?** → jump straight to `layout`, `typeset`, or `colorize`
7. **Brand work?** → `brand`, `brand-alchemy`, `brand-guidelines`, or `brandkit` depending on stage
8. **Landing page specifically?** → `landing-page-architecture` (framework) or `landing-page-guide-v2` (Next.js/ShadCN)
9. **Final pass before ship?** → `polish` then `delight` then `browse-qa`
10. **Proof before declaring done?** → `reference-match-design-qa` proof mode + `browse-qa` + `ultra-review`

The constellation is additive — many real sessions hit Phase 1 → Phase 3 → Phase 5 → Phase 6. Don't try to use all of them; pick the ones that close the gap between where the work is and where it needs to be.

## Core Promise

This skill should improve design even when the user provides no reference.

The default output should not be generic AI UI. It should feel like a real
product screen built for a real job, with a clear hierarchy, deliberate spacing,
product-specific states, usable mobile behavior, and restrained motion.

## Does This Actually Improve Anything?

Yes, when it changes the build behavior. This skill is useful only if it makes
the session do these concrete things:

1. Choose the product type and workflow before choosing decoration.
2. Use one clear reference or one clear no-reference direction instead of a
   vague "premium" vibe.
3. Pull from local components/tokens first, then from safe source libraries only
   when they improve the product.
4. Build real states: empty, loading, error, success, hover, focus, disabled,
   destructive, mobile, and flow-specific states where relevant.
5. Run visual proof and repair: screenshots, mismatch review, no overlap, no
   clipped text, no broken hierarchy, no weird boxes, no broken mobile collapse.

If a session only reads this skill and then produces a generic layout, the skill
was not applied. Patch the design until the built UI is visibly more
product-specific, usable, and proven.

## Non-Noise Rule

Do not load every reference file by default. Load the fast required core first,
then load only the deeper references triggered by the actual task.

Fast required core:

- product type / pattern family
- reference-led or no-reference mode
- conditional design gates
- source lane
- implementation
- screenshots or exact blocker
- mismatch repair

Full research mode is only for broad design-system work, source-library
expansion, typography/cultural research, or when the user explicitly asks for
a deep sweep.

## Workflow

1. Read the target repo instructions and existing product/design files.
2. Identify the surface: website, app shell, dashboard, onboarding, commerce,
   AI/agent workspace, editor, calendar, canvas, support, mobile-style app, or
   another product type.
3. Load `reference-match-design-qa`.
4. Load `vibe-design-reference-libraries`.
5. Always read the universal pattern library:
   `../reference-match-design-qa/references/universal-code-backed-pattern-library.md`.
6. Always read the design architecture map:
   `../reference-match-design-qa/references/design-architecture-map.md`.
7. Always read the design source database:
   `../reference-match-design-qa/references/design-source-database-index.md`.
8. Always read the visual integrity gate:
   `../reference-match-design-qa/references/visual-integrity-gate.md`.
9. Always read the conditional design gate router:
   `../reference-match-design-qa/references/conditional-design-gate-router.md`.
10. For every matching trigger, load only the required gate before coding:
   research/IA, website discovery/SEO, performance, measurement, service
   journey, cognitive accessibility/privacy, platform adaptivity, data-viz,
   interaction accessibility, trust, token governance, motion, and proof.
11. For no-reference work, read the no-reference art direction catalog and
    source recipes:
    `../reference-match-design-qa/references/no-reference-art-direction-catalog.md`
    and `../reference-match-design-qa/references/source-recipes-by-product-and-direction.md`.
12. For reference-led work, create a reference packet and extract structure,
    hierarchy, spacing, typography, surfaces, states, motion, and responsive
    behavior before coding.
13. For code-backed source use, read additive GitHub source lanes and the GitHub
    code safety checklist before copying:
    `../reference-match-design-qa/references/additive-github-source-lanes-2026-05-18.md`
    and `../reference-match-design-qa/references/github-code-safety-checklist.md`.
14. For typography, cultural, localization, or global products, read:
    `../reference-match-design-qa/references/typography-and-cultural-system.md`.
15. For broad design research, free resources, video learning, or source-library
    expansion, read the pro resource library:
    `../reference-match-design-qa/references/pro-design-resource-library-2026-05-18.md`.
16. For visual proof and repair, read the state coverage matrix and screenshot
    repair playbook:
    `../reference-match-design-qa/references/state-coverage-matrix.md`
    and `../reference-match-design-qa/references/screenshot-repair-playbook.md`.
17. Pick one primary pattern family before coding.
18. Pick one primary database category plus at most two supporting categories
   before coding: typography, color/tokens, layout/boxes, components, UX flow,
   motion, icons/media, data-viz/maps, accessibility/localization, proof,
   research/IA, performance, discovery/SEO, measurement, or service journey.
19. Pick one source lane:
   - exact visual reference
   - no-reference art direction
   - pullable shadcn/React/Tailwind code
   - dense dashboard/app shell
   - real-product UX gallery
   - motion/loading/animation
   - AI/agent/chat/voice UI
   - mature design system/primitives
   - workflow-specific source such as ecommerce, editor, calendar, canvas,
     upload, map, or 3D
20. Build the actual UI.
21. Capture desktop and mobile screenshots.
22. Compare against the reference packet or no-reference design packet.
23. Use the screenshot repair playbook and visual integrity gate. Patch every
   blocker-class issue before saying the design is done.
24. Run `ultra-review` before saying meaningful design work is done.

## Design QA Pipeline

Use this order for meaningful UI work:

1. `Intake`: identify user goal, product type, platform, route/screen/flow,
   audience, workflow density, and reference/no-reference mode.
2. `Design contract`: read existing `DESIGN.md`, brand docs, tokens, component
   library, screenshots, and product planning. If no design memory exists for a
   serious product, create or propose a small `DESIGN.md` using
   `../reference-match-design-qa/templates/product-DESIGN.md`.
3. `Reference context`: if the user provides a screenshot, website, product
   example, image, Figma link, or other visual reference, extract layout,
   hierarchy, typography, color, surfaces, states, motion, and responsive
   behavior before coding. Screenshots, websites, and real product examples are
   the normal path; Figma is optional and only matters when the user provides it.
4. `Pattern/source/database lane`: choose the product pattern family,
   reference/no-reference mode, one no-reference direction when needed, one
   primary source recipe, and one primary source database category from the
   universal pattern library, source recipes, design source database, typography
   system, and pro resource library.
5. `Conditional gates`: use the conditional design gate router. If the surface
   is public web, load website discovery/SEO. If it is a serious app/platform,
   load research/IA and service journey. If speed or motion matters, load the
   performance budget. If success needs proof later, load measurement. If the
   flow asks for data, permission, money, approval, or multi-step memory, load
   cognitive accessibility/privacy and trust gates.
6. `Implementation`: build the actual UI in the target repo using local
   components/tokens first, then safe code-backed sources.
7. `Proof`: capture desktop/mobile screenshots. Use Storybook for component
   states and Browser Harness for full-page route proof when supported.
8. `Mismatch repair`: score and patch the visible issues using the screenshot
   repair playbook and visual integrity gate. Overlap, clipping, text overflow,
   bad hierarchy, weird cards/boxes, broken mobile collapse, bad layering, weak
   contrast, and critical truncation are blockers, not polish.
9. `Final review`: use `ultra-review` and report proof or the exact blocker.

## Optional Design Handoff Branch

Figma is not the default path. Use it only when the user provides a Figma
link/file, or when the repo already has a design-system handoff that clearly
saves time. Otherwise, use screenshots, websites, real product examples,
code-backed GitHub/component sources, and browser screenshot proof.

Use Figma/Code Connect context only when available:

- screenshot/frame capture
- variable and style definitions
- design-system search
- mapped component snippets/imports
- component names and props
- spacing, typography, color, and token values

If a frame uses mapped components, prefer the mapped snippets/imports over
generic recreation. If components are not mapped, say confidence is lower and
match visually with screenshots.

Screenshot-to-code or Figma-to-code is a bootstrap only. It may create
first-pass structure, but it is not acceptance proof. Acceptance proof comes
from post-implementation screenshots and mismatch repair.

## Reference Match Scorecard

For reference-led work, classify each item as `match`, `mismatch`, or `blocker`:

- layout
- hierarchy
- spacing
- typography
- color and surface
- component anatomy
- states
- motion
- responsive behavior
- accessibility

Patch the highest-impact mismatch first.

## Token And Component Governance

When a project has tokens, use them. When it lacks tokens and the UI work is
serious, keep new design values small and semantic.

Default token roles:

- background
- surface
- elevated surface
- border
- text
- muted text
- primary
- secondary
- success
- warning
- danger
- info
- focus
- selection
- chart colors

If adding or changing tokens, keep one canonical token source where possible and
export into app formats from there. Avoid raw-value drift across components.

## Design Doctrine

Use these as enforced defaults, not optional advice:

- Start with hierarchy, not decoration. Decide what users must see first,
  second, and third.
- Start with user need, not UI shape. Name the core user task and one thing the
  design intentionally removes or simplifies.
- Platform-first, not trend-first. Respect web, mobile, desktop, and target
  product conventions before adding style.
- Product job first. A CRM, checkout, calendar, AI workspace, editor, and
  landing page need different layouts.
- Use semantic tokens where the repo has them. Avoid random raw colors, radii,
  shadows, and spacing values when local tokens exist.
- Build spacing as a system. Prefer a 4/8-based rhythm unless the repo already
  has a clear scale.
- Use typography for hierarchy: size, weight, line height, line length, and
  grouping before visual effects.
- Typography is a database-backed decision. Pick from product-fit sources such
  as Google Fonts, Noto, Fontsource, Typewolf, system stacks, or existing brand
  fonts, and document fallback/script coverage for global or culture-sensitive
  products.
- Use color semantically. Error colors are for errors, success colors are for
  success, and color is never the only status signal.
- Treat color psychology as contextual, not universal. Do not use internet
  claims like "blue means trust" unless the audience, product job, and
  concept-color mapping support that choice.
- Brand systems are more than logo and palette. Serious brand work needs
  typography, layout, imagery, icon style, motion, voice, misuse rules, and
  governance.
- Name tokens by purpose when possible: action, surface, text, border, state,
  focus, chart, and brand role. Avoid paint-name drift across files.
- Motion must have a job: feedback, orientation, continuity, loading clarity,
  or one deliberate brand moment.
- Respect reduced motion and keyboard/focus behavior.
- Write interface copy as actions and recovery paths: `Save`, `Create`,
  `Retry`, `Connect`, `Invite`, `View receipt`.
- For multi-screen flows, define organization, labeling, navigation, and search
  strategy. Navigation wording is part of the design.
- For mobile, audit thumb reach, scroll burden, field count, first-tap task,
  and one-handed navigation instead of only shrinking desktop.
- For conversion-critical flows, check field burden, error recovery, trust,
  price/commitment clarity, and review-step clarity before polish.
- State design is required: default, hover, focus, active, disabled, loading,
  empty, error, success, selected, destructive, permission-limited, and mobile
  behavior where relevant.
- WCAG AA is the minimum floor for contrast, focus visibility, semantics,
  labels, and target size unless a stronger platform rule applies.
- Visual integrity is mandatory. No overlap, clipped text, unhandled overflow,
  weird nested boxes/cards, incoherent hierarchy, broken mobile collapse, or
  layer conflict can remain in a completed design pass.

## Psychology, Brand, Color, And Video Rules

Use these rules when the task includes brand identity, color, emotion,
psychology, visual taste, vibe coding, AI-assisted UI, or no-reference design.

- Hierarchy first: name the focal point, scan order, and grouping cues before
  choosing effects.
- Color meaning comes from context. If color communicates meaning, document the
  concept-color mapping and make sure it matches user expectation.
- Every palette needs semantic roles, contrast proof, and state behavior:
  default, hover, focus, selected, disabled, success, warning, danger, and info.
- A brand packet is incomplete without typography, layout, imagery, icons,
  motion, voice, and misuse rules.
- A design system is AI-ready only when the source of truth, tokens,
  components, states, Storybook/proof surface, and governance are clear.
- YouTube is allowed as a learning source, but extract durable rules rather
  than copying a visual style. Prefer captions/transcripts when available.
- After any video research pass, save only 3-5 reusable heuristics and one
  anti-pattern list, then apply those lessons to the current build.

Useful video lanes are listed in
`../reference-match-design-qa/references/pro-design-resource-library-2026-05-18.md`.

## Anti-Generic Checklist

Fix these before calling the design polished:

- generic centered glass card
- purple-blue gradient default
- decorative blobs/orbs/noise with no product purpose
- repeated card grid when a workflow/table/timeline would be clearer
- fake metrics, fake testimonials, fake logos, or unsupported claims
- oversized hero treatment inside an app tool
- no empty/loading/error states
- no mobile layout proof
- no keyboard/focus path
- motion that only exists because the page felt plain
- copied component styling that ignores local brand tokens

## Source Lane Router

Use the newer source lanes when the product type is specific:

- Motion and loading: Animate UI, Motion Primitives, Motion, React Spring,
  Auto Animate, Number Flow, Lottie/dotLottie, Rive, canvas-confetti, GSAP,
  anime.js, Three.js, PixiJS.
- AI/agent/voice: assistant-ui, AI Elements, CopilotKit, ElevenLabs UI,
  LangChain Agent Chat UI, Manifest UI, Vercel AI SDK examples.
- Dashboards/tables/admin: shadcn-admin, tablecn, OpenStatus data-table
  filters, ReUI, TanStack Table, React Spectrum patterns, Base UI, Park UI.
- Ecommerce: Vercel Commerce, Medusa, Saleor, Stripe React, Shopify Hydrogen
  patterns.
- Calendar/scheduling: Schedule-X, FullCalendar, Cal.com patterns, shadcn date
  components.
- Editors/docs/CMS: Lexical, Plate, Tiptap, Fumadocs/Nextra-style docs
  patterns, Storybook docs.
- Canvas/workflow/boards: xyflow, tldraw, Excalidraw, dnd-kit, React Three
  Fiber, drei.
- Uploads/media: Uppy, FilePond, ReUI upload patterns.
- Maps/logistics: MapLibre, deck.gl, Mapbox-style references when appropriate.
- Mature design systems: Apple HIG, Material, NN/g, WAI/WCAG, Atlassian,
  Carbon, Primer, Polaris, Fluent, React Spectrum.

Do not mix many lanes. Pick one main lane and at most two supporting lanes.

## GitHub Code Rule

When the user has approved using GitHub code for design work, do not block
useful GitHub code due to license anxiety once the user has explicitly
approved use.

Still do the safety pass before copying:

- use
  `../reference-match-design-qa/references/github-code-safety-checklist.md`
  as the canonical checklist
- inspect package/install scripts, postinstall hooks, CLIs, setup commands, and
  dependency graph
- check network calls, analytics, trackers, telemetry, remote scripts, remote
  assets, and hidden external services
- check auth, payment, credentials, cookies, tokens, localStorage/sessionStorage,
  file-system, clipboard, camera, microphone, geolocation, notifications, and
  dangerous browser/device APIs
- check dangerous execution such as `eval`, `new Function`, dynamic script
  injection, obfuscated source, shell commands, and heavy dependency bloat
- strip fake content, logos, metrics, claims, and brand styling
- copy the smallest useful block and rewrite it into local imports, tokens,
  states, accessibility behavior, product copy, and proof

In normal words: permission handles the legal concern; inspection handles the
safety and quality concern.

## Reference-Led Mode

Use when the user provides a screenshot, URL, website, product example, image,
app, taste example, or optional Figma handoff.

Done means the built UI materially tracks the reference:

- same major layout and content rhythm
- same hierarchy and focal point
- comparable spacing density and alignment
- comparable type scale and weight
- comparable surfaces, borders, radius, and depth
- comparable interaction states and mobile collapse
- screenshot proof after implementation

The reference packet is the brief, not the deliverable. Build the thing.

## No-Reference Mode

Use when the user says the design should be better but gives no visual
reference.

Default behavior:

1. Infer the product type, audience, workflow density, and platform.
2. Pick one `direction_id` from the no-reference art direction catalog.
3. Fill the brand bootstrap when the product lacks clear design memory.
4. Pick one source recipe for the product type and direction.
5. Select required states from the state coverage matrix.
6. Pull 2-4 references or code-backed sources from the correct lane.
7. Build the actual UI.
8. Use screenshots to catch generic-looking weaknesses and visual blockers.
9. Patch the screen with the screenshot repair playbook and visual integrity
   gate before calling it done.

No-reference acceptance target: "this looks like a serious product surface for
its job," not "this has a fashionable effect."

## Proof Requirements

For meaningful UI work, provide at least one of:

- desktop and mobile screenshots
- Browser Harness screenshot proof
- Storybook stories for component states
- visual regression evidence when the repo supports it
- a concrete blocker explaining why screenshots could not be captured

For animation or 3D/canvas work, also verify the primary animated/canvas surface
is nonblank, framed correctly, and usable on desktop and mobile.

## Done Means

- The UI exists in code.
- The design is specific to the product and user job.
- A product type, reference/no-reference mode, `direction_id` when relevant,
  source recipe, and source lane were chosen before coding.
- Required states are handled.
- GitHub/component code was inspected and rewritten into local patterns.
- Desktop/mobile proof artifact paths exist or a concrete blocker is named.
- No blocker-class visual defect remains: no overlap, clipped text, unresolved
  text overflow, bad hierarchy, weird cards/boxes, broken mobile collapse, bad
  layering, weak focus/contrast, or critical truncation.
- `ultra-review` found no unresolved blocker that changes the answer.
