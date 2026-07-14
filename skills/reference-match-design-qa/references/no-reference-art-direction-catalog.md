# No-Reference Art Direction Catalog

Research date: 2026-05-18

Purpose: give Codex and Claude named visual directions when the user asks for
better design without a reference. Pick one direction before coding. Do not
blend many directions unless the product genuinely needs a hybrid.

Each direction is a starting contract, not a rigid theme. Adapt it to the target
repo's tokens, components, audience, and product job.

## How To Use

1. Pick the product type from `universal-code-backed-pattern-library.md`.
2. Pick one `direction_id` from this file.
3. Record why the direction fits the user, workflow density, and brand.
4. Choose source recipes from `source-recipes-by-product-and-direction.md`.
5. Fill a brand bootstrap if the repo has no design contract.
6. Build, screenshot, and repair using `screenshot-repair-playbook.md`.

## Direction Selector

| direction_id | Use when | Avoid when |
| --- | --- | --- |
| `calm-operator` | Dense SaaS, admin, ops, CRM, support, finance, logistics | Public marketing pages that need emotional storytelling |
| `editorial-saas` | Launch pages, portfolios, docs, thought-leadership, premium SaaS | Data-heavy daily tools |
| `precision-fintech` | Finance, billing, reports, analytics, compliance, serious B2B | Playful consumer products |
| `warm-human-services` | Healthcare, coaching, local services, education, onboarding | Hardcore developer/admin tools |
| `developer-console` | API products, devtools, infrastructure, docs, technical dashboards | Consumer lifestyle products |
| `ai-command-center` | Agent workspaces, copilots, tool-running, voice/multimodal AI | Simple brochure sites |
| `mobile-native-clean` | Mobile-style web apps, booking, onboarding, personal tools | Wide dense desktop dashboards |
| `luxury-minimal` | High-end service, portfolio, premium offer, luxury ecommerce | Workflows with many controls or error states |
| `playful-consumer` | Consumer apps, habit tools, games, family/community, lightweight onboarding | Compliance-heavy enterprise surfaces |
| `brutalist-utility` | Bold campaigns, internal prototypes, developer/admin surfaces needing strong identity | Trust-sensitive finance/health flows |
| `glass-depth-showcase` | Product launches, immersive heroes, creative portfolios, AI/media public pages | Dense app screens or accessibility-risky surfaces |
| `spatial-canvas-lab` | Canvases, node editors, maps, creative tools, 3D/inspection surfaces | Simple forms or text-heavy docs |

## Direction Details

### calm-operator

- Feeling: quiet, competent, fast, low-drama.
- Typography: neutral UI sans; medium weight for section labels; avoid oversized
  hero type inside the app.
- Density: balanced to dense; compact controls with generous group spacing.
- Color posture: low-saturation neutrals plus one clear action color.
- Surface language: flat panels, light borders, minimal elevation, strong table
  and split-pane structure.
- Motion voice: subtle state continuity only: drawers, row expansion, filters,
  loading-to-loaded.
- Icon family: Lucide, Tabler, or Phosphor regular; one family only.
- Best sources: shadcn-admin, ReUI, TanStack Table, OpenStatus filters,
  Atlassian, Carbon, Primer.
- Anti-patterns: marketing hero in app chrome, decorative gradients, fake
  metrics, repeated cards where a table or work queue is clearer.

### editorial-saas

- Feeling: sharp, credible, story-led, spacious.
- Typography: expressive display or high-quality sans for headings plus readable
  body; line length is controlled.
- Density: sparse to balanced.
- Color posture: restrained palette, one memorable accent, strong black/white or
  light/dark rhythm.
- Surface language: full-width sections, editorial grids, product screenshots,
  comparison bands.
- Motion voice: scroll reveals and micro motion only when it supports narrative.
- Icon family: minimal line icons or custom product glyphs.
- Best sources: Tailark, shadcn blocks, Godly, Land-book, Siteinspire,
  Awwwards, Refactoring UI.
- Anti-patterns: generic centered hero, fake testimonials, abstract gradient
  shapes without product proof.

### precision-fintech

- Feeling: exact, trustworthy, controlled.
- Typography: crisp sans, tabular numerals, clear labels, conservative headings.
- Density: balanced to dense.
- Color posture: semantic status colors; action color is strong but not loud.
- Surface language: tables, charts, summary strips, audit trails, visible
  validation.
- Motion voice: restrained; number transitions only when values change.
- Icon family: thin line icons with consistent stroke.
- Best sources: Primer, Carbon, React Spectrum, TanStack Table, Tremor,
  Recharts/Nivo/Apache ECharts.
- Anti-patterns: color-only risk state, decorative chart noise, rounded-cute
  cards, hidden fees/commitment copy.

### warm-human-services

- Feeling: approachable, clear, reassuring.
- Typography: humanist sans; larger body text; plain language.
- Density: sparse to balanced.
- Color posture: warm neutrals plus accessible action/status colors.
- Surface language: clear steps, large touch targets, friendly empty states,
  visible recovery paths.
- Motion voice: gentle feedback; avoid flashy transitions.
- Icon family: Lucide/Phosphor with softer weights.
- Best sources: GOV.UK, USWDS, web.dev accessibility, Baymard mobile forms,
  Practical Typography.
- Anti-patterns: vague wellness gradients, low contrast, hidden validation,
  long forms with placeholder-only labels.

### developer-console

- Feeling: technical, legible, efficient.
- Typography: neutral sans plus mono for code/IDs/logs.
- Density: balanced to dense.
- Color posture: dark or light system palette with clear semantic states.
- Surface language: docs nav, command palette, code blocks, logs, tabs,
  inspectable receipts.
- Motion voice: minimal; command/result continuity and progress only.
- Icon family: Lucide/Tabler; avoid decorative brand icons.
- Best sources: Primer, Fumadocs, Nextra, Storybook docs, cmdk, React Aria,
  Radix/Base UI.
- Anti-patterns: hiding technical detail behind marketing copy, unreadable code
  blocks, no keyboard flow.

### ai-command-center

- Feeling: capable, transparent, controlled.
- Typography: clean app sans plus mono for tool calls/logs.
- Density: balanced; side panels and receipts matter.
- Color posture: neutral workspace with semantic status colors for tool states.
- Surface language: split panes, thread + work artifact, tool cards, approvals,
  proof/receipt panels.
- Motion voice: streaming, tool-running, state transitions, voice/listening
  feedback; all with reduced-motion.
- Icon family: one line icon family plus status indicators.
- Best sources: assistant-ui, AI Elements, CopilotKit, ElevenLabs UI,
  LangChain Agent Chat UI, LiveKit Components.
- Anti-patterns: plain chat box as the whole product, hidden failures, no
  approval boundary, no proof panel.

### mobile-native-clean

- Feeling: direct, lightweight, thumb-friendly.
- Typography: high readability, clear labels, short section titles.
- Density: sparse on mobile, balanced on tablet/desktop.
- Color posture: simple surfaces and one action color.
- Surface language: bottom actions, step cards, sheets, clear empty states.
- Motion voice: sheet transitions, progress continuity, small confirmations.
- Icon family: Lucide/Phosphor with larger hit targets.
- Best sources: Android mobile UI, Apple HIG, Baymard mobile, React Aria,
  Driver.js only for optional tours.
- Anti-patterns: desktop table squeezed into mobile, small tap targets,
  ambiguous date/time fields, hidden primary action.

### luxury-minimal

- Feeling: premium, restrained, confident.
- Typography: high-quality display or editorial serif/sans pairing; large
  whitespace.
- Density: sparse.
- Color posture: very limited palette; high contrast; careful material cues.
- Surface language: large images/product proof, controlled spacing, few cards.
- Motion voice: slow, deliberate, not constant.
- Icon family: minimal or custom; use few icons.
- Best sources: high-end portfolio/brand sites, Typewolf, Fontshare, Awwwards,
  Minimal Gallery.
- Anti-patterns: low contrast gray text, too many CTAs, fake luxury via gold
  accents, cramped product details.

### playful-consumer

- Feeling: friendly, energetic, memorable.
- Typography: rounded or expressive sans with readable body fallback.
- Density: sparse to balanced.
- Color posture: richer palette, but semantic status colors still distinct.
- Surface language: rounded controls, illustrations, progress, rewards, lively
  empty states.
- Motion voice: celebratory only for real milestones; avoid constant bouncing.
- Icon family: Phosphor/Lucide rounded feel or custom illustration set.
- Best sources: Mobbin consumer flows, Blush, unDraw, Lottie/Rive, React Bits
  with restraint.
- Anti-patterns: childish UI for serious tasks, inaccessible pastel contrast,
  celebration on routine actions.

### brutalist-utility

- Feeling: bold, fast, opinionated.
- Typography: heavy sans, direct labels, high contrast.
- Density: balanced; strong blocks and clear actions.
- Color posture: high contrast, limited palette, intentional roughness.
- Surface language: hard borders, simple grids, chunky controls.
- Motion voice: minimal; interaction feedback can be punchy.
- Icon family: simple solid or heavy line icons.
- Best sources: Brutalist Websites, Godly, selected marketing references,
  Tailwind/shadcn basics.
- Anti-patterns: sacrificing readability, using aggression for trust-sensitive
  tasks, inconsistent spacing.

### glass-depth-showcase

- Feeling: immersive, advanced, polished.
- Typography: modern sans, strong hero scale, short copy.
- Density: sparse.
- Color posture: dark/light depth with strong contrast checks.
- Surface language: layered panels, frosted surfaces, product visuals, 3D or
  video when useful.
- Motion voice: hero and transition motion; must respect reduced motion.
- Icon family: minimal line icons.
- Best sources: Motion, GSAP, R3F/Drei, Spline, Awwwards WebGL/loading
  galleries, Magic UI/React Bits.
- Anti-patterns: permanent blurred glass on dense tools, unreadable text,
  heavy GPU animation with no product purpose.

### spatial-canvas-lab

- Feeling: exploratory, precise, directly manipulable.
- Typography: compact labels and readable inspector text.
- Density: dense canvas plus clean inspectors.
- Color posture: neutral canvas with high-contrast selection/status colors.
- Surface language: canvas, handles, minimap, side inspector, command palette,
  layers, zoom/pan controls.
- Motion voice: pan/zoom/selection continuity, not decorative motion.
- Icon family: Lucide/Tabler tool icons with tooltips.
- Best sources: xyflow, tldraw, Excalidraw, BlockSuite, MapLibre/deck.gl,
  Pragmatic Drag and Drop.
- Anti-patterns: no keyboard shortcuts/focus states, hidden selection handles,
  unusable mobile/touch behavior, no empty canvas starter.

## Direction Choice Rules

- For dense work tools, prefer `calm-operator`, `precision-fintech`, or
  `developer-console`.
- For public-facing marketing, prefer `editorial-saas`, `luxury-minimal`, or
  `glass-depth-showcase`.
- For AI/agent products, prefer `ai-command-center` unless the product is a
  simple consumer assistant.
- For canvas/map/builder products, prefer `spatial-canvas-lab`.
- For health, education, services, or onboarding, prefer
  `warm-human-services` or `mobile-native-clean`.
- For consumer apps, prefer `playful-consumer` or `mobile-native-clean`.
- Use `brutalist-utility` only when the product can tolerate a bold identity
  and readability remains strong.
