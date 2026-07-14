# Pro Design Resource Library

Research date: 2026-05-18

Purpose: give `design-intelligence` a broad resource map for turning generic AI
UI into stronger product design. Use this after choosing the product type from
`universal-code-backed-pattern-library.md`.

This file is not a dump of links. Each lane tells Codex what the resource is
good for, when to use it, and what to avoid.

## How To Use This Library

1. Pick the product type first.
2. Pick one primary resource lane.
3. Add at most two supporting lanes.
4. Use code-backed sources only when they fit the repo stack.
5. Use asset sources only when they support the product story, not decoration.
6. Use education/article/video sources to improve judgment and review, not as a
   replacement for building.
7. Capture proof after implementation.

## 1. Designer-Learning Resources For Coders

Use these when Codex needs better judgment, a no-reference art direction, or a
plain-English design review.

| Source | URL | Use |
| --- | --- | --- |
| Refactoring UI | https://refactoringui.com/ | Best developer-facing design tactics: hierarchy, spacing systems, type scale, color scales, depth, fewer borders, empty states, and component inspiration. |
| Learn UI Design | https://www.learnui.design/ | Broad UI curriculum for typography, layout, color, components, and visual polish. Use as a quality-bar source. |
| LearnVisual.Design | https://learnvisual.design/ | Free/open visual design guide covering typography, layout, spacing, color, taste, and finishing touches. |
| DesignCourse | https://designcourse.com/ | Useful for UI refactors, hierarchy examples, Figma-to-code thinking, and visual critique. |
| Kevin Powell | https://www.kevinpowell.co/youtube/ | Best CSS implementation source for responsive layout, modern CSS, and turning design intent into code. |
| web.dev Learn Responsive Design | https://web.dev/learn/design | Responsive layout and web platform fundamentals. |
| web.dev Learn Accessibility | https://web.dev/learn/accessibility | Accessibility course covering structure, focus, color/contrast, motion, typography, forms, testing, and design systems. |
| Laws of UX | https://lawsofux.com/ | Useful psychology rules for interface decisions, especially defaults, memory load, feedback, and grouping. |
| NN/g usability heuristics | https://www.nngroup.com/articles/ten-usability-heuristics/ | Behavior review layer: status visibility, user control, consistency, error prevention, recognition over recall, and recovery. |
| IxDF visual hierarchy | https://www.interaction-design.org/literature/topics/visual-hierarchy | Conceptual grounding for hierarchy and attention. |

Skill rule: convert learning resources into checks. Do not answer “study this.”
Apply the lesson to hierarchy, spacing, copy, mobile, states, or proof.

## 2. UX, Functionality, And Product Behavior

Use these when the interface needs to work better, not just look better.

| Source | URL | Use |
| --- | --- | --- |
| NN/g heuristics | https://www.nngroup.com/articles/ten-usability-heuristics/ | Run a heuristic audit after the first build pass. |
| Atlassian Design System | https://atlassian.design/ | State design, content design, tokens, components, empty states, drag/drop, and product messaging. |
| Carbon Design System | https://carbondesignsystem.com/ | Enterprise product patterns, empty/loading states, data-heavy UI, and accessibility discipline. |
| Shopify Polaris | https://polaris.shopify.com/ | Commerce/admin UX, content rules, resource lists, banners, empty states, and merchant workflows. |
| Primer | https://primer.style/ | Developer product UI, tokens, components, navigation, and dense product surfaces. |
| GOV.UK Design System | https://design-system.service.gov.uk/ | Forms, validation, plain language, accessibility, and serious public-service UX. |
| U.S. Web Design System | https://designsystem.digital.gov/ | Accessible government-grade components, tokens, forms, and content guidance. |
| GOV.UK Design Principles | https://www.gov.uk/guidance/government-design-principles | User-need-first product design: do less, simplify hard things, use data, iterate. |
| WAI-ARIA APG | https://www.w3.org/WAI/ARIA/apg/ | Custom widget semantics, keyboard models, accessible names, states, and landmarks. |
| W3C WCAG 2.2 updates | https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/ | Focus appearance, target size, dragging alternatives, redundant entry, and accessible authentication. |
| Information Architecture Institute | https://www.iainstitute.org/ | Organization, labeling, navigation, search, and findability concepts. |
| NN/g UX Research Methods | https://www.nngroup.com/articles/which-ux-research-methods/ | Method choice for card sorting, tree testing, usability testing, field studies, and validation. |
| NN/g Information Foraging | https://www.nngroup.com/articles/information-foraging/ | Information scent and navigation/label clarity. |
| NN/g UX Critique | https://www.nngroup.com/articles/design-critiques/ | Goal-scoped design critique and review discipline. |
| Baymard Checkout UX | https://baymard.com/research/checkout-usability | Conversion-critical field burden, errors, trust, and checkout clarity. |
| Baymard Mobile Ecommerce UX | https://baymard.com/research/mcommerce-usability | Mobile friction patterns: thumb reach, field count, review clarity, and scroll burden. |
| Android Mobile UI Design | https://developer.android.com/design/ui/mobile | Mobile layout/content, behavior patterns, and component rules. |

Skill rule: every serious screen must name its primary user job, primary action,
recovery path, and state coverage before styling.

Functionality rules:

- Every design packet must name the primary user need, the core task, and one
  thing intentionally removed to reduce complexity.
- For multi-screen flows, define organization, labeling, navigation, and search
  strategy. Navigation copy is not cosmetic.
- Score key labels and entry points for information scent: users should know
  what is behind a click and how it moves them toward the goal.
- When redesigning navigation or IA, choose one validation method when feasible:
  card sorting for categories, tree testing for findability, or usability
  testing for flow breakdowns.
- For conversion-critical flows, review field burden, error handling, trust,
  total cost/commitment clarity, and recovery before visual polish.
- Mobile is not a scaled-down desktop pass. Audit thumb reach, scroll burden,
  field count, first-tap task, review-step clarity, and one-handed navigation.
- If custom widgets are used, map them to an APG-style pattern and document
  keyboard behavior, accessible name, state, and landmark structure.
- Reject layouts where DOM order, visual order, and tab order disagree unless
  there is a deliberate accessibility reason.

## 3. Free UI And Code-Backed Component Sources

Use these when the repo stack is compatible and we need concrete UI code or
component anatomy.

| Source | URL | Use |
| --- | --- | --- |
| shadcn/ui | https://ui.shadcn.com/ | Default open-code React/Tailwind component model. |
| registry.directory | https://registry.directory/ | Discover shadcn registries and installable blocks. |
| ReUI | https://reui.io/ | Large shadcn/Tailwind component/block library for real product flows. |
| 21st.dev | https://21st.dev/ | Marketplace/discovery for shadcn blocks, components, hooks, and agent elements. |
| Magic UI | https://magicui.design/ | Animated shadcn/Tailwind components for public surfaces and selective polish. |
| React Bits | https://www.reactbits.dev/ | Expressive animated React components; use with restraint. |
| Motion Primitives | https://motion-primitives.com/ | Clean Motion-based primitives for app-safe animation. |
| Animate UI | https://animate-ui.com/ | shadcn-compatible animated primitives and components. |
| Tailark | https://tailark.com/ | Marketing blocks and landing structures. |
| shadcn-admin | https://github.com/satnaing/shadcn-admin | App shell/admin dashboard source. |
| tablecn | https://github.com/sadmann7/tablecn | Serious shadcn data table patterns. |
| OpenStatus data-table-filters | https://github.com/openstatusHQ/data-table-filters | Faceted filter/table patterns. |
| Uilib | https://www.uilib.co/ | Free React UI components and Tailwind blocks. |
| Base UI | https://base-ui.com/ | Accessible unstyled primitives. |
| React Spectrum | https://react-spectrum.adobe.com/ | Accessibility-rich behavior and state patterns. |
| Park UI | https://park-ui.com/ | Token/component anatomy patterns with Ark UI and Panda. |
| Radix UI | https://www.radix-ui.com/primitives | Accessible primitives behind many shadcn patterns. |
| Headless UI | https://headlessui.com/ | Accessible unstyled Tailwind-friendly interaction primitives. |
| cmdk | https://cmdk.paco.me/ | Command palette and keyboard-first action search. |
| TanStack Table | https://tanstack.com/table | Serious tables for sorting, filtering, selection, pagination, and virtualization. |
| TanStack Form | https://tanstack.com/form | Typed form state when the product needs headless form control. |
| react-hook-form | https://react-hook-form.com/ | Practical default form state library for React. |
| Tiptap | https://tiptap.dev/ | Headless rich text editor. |
| Lexical | https://lexical.dev/ | Performant extensible editor framework. |
| Plate | https://platejs.org/ | shadcn-friendly rich text editor patterns. |
| Fumadocs | https://fumadocs.dev/ | Modern docs-site source for nav/search/content rhythm. |
| Nextra | https://nextra.site/ | MDX/docs site source. |
| Tamagui | https://tamagui.dev/ | Cross-platform web/native UI system. |
| gluestack-ui | https://gluestack.io/ | React Native/Web component source patterns. |

Skill rule: copy the smallest useful block, then rewrite it into local imports,
tokens, states, accessibility behavior, and product copy.

Avoid whole-starter imports. Use starter repos for one useful slice: app shell,
table/filter pattern, editor toolbar, calendar surface, command palette, or
workflow canvas. Inspect auth, billing, analytics, telemetry, uploads, and
external API wiring before lifting anything from a starter.

## 4. Icons

Use icons to clarify tools, status, and navigation. Do not use icons as random
decoration.

| Source | URL | Use |
| --- | --- | --- |
| Lucide | https://lucide.dev/ | Default clean line icons for app/tool UI. |
| Heroicons | https://heroicons.com/ | Tailwind-aligned outline/solid icons. |
| Tabler Icons | https://tabler.io/icons | Large general-purpose line icon set. |
| Phosphor Icons | https://phosphoricons.com/ | Flexible weights for different brand tones. |
| Remix Icon | https://remixicon.com/ | Neutral system-style icons. |
| IconSearch | https://iconsearch.info/ | Compare free SVG icon libraries for React/Next/Vue/Svelte. |
| All SVG Icons | https://allsvgicons.com/ | Search/copy large free SVG/PNG/JSX icon sets. |
| OpenIconLibrary | https://openiconlibrary.com/ | Search open SVG icon packs. |
| React Icons | https://react-icons.github.io/react-icons/ | Aggregator; convenient, but watch bundle size. |

Skill rule: one icon family per surface unless there is a clear reason. Match
stroke weight to type weight and component density.

## 5. Typography

Use typography to create hierarchy, readability, product personality, and polish.

| Source | URL | Use |
| --- | --- | --- |
| Google Fonts | https://fonts.google.com/ | Broad free font catalog and variable fonts. |
| Fontshare | https://www.fontshare.com/ | High-quality free typefaces with strong editorial/UI options. |
| Fontsource | https://fontsource.org/ | Self-hostable open-source font packages. |
| Typewolf | https://www.typewolf.com/ | Font pairing and real-site type inspiration. |
| Practical Typography | https://practicaltypography.com/ | Typography fundamentals and readable text rules. |
| Modern Font Stacks | https://modernfontstacks.com/ | System-font stacks for fast, native-feeling UI. |

Skill rule: choose one UI font and optionally one display/accent font. Define
scale, line height, weight roles, and line-length limits before styling the
screen.

## 6. Color, Gradients, Contrast, And Tokens

Use these when a project lacks a mature palette or semantic token system.

| Source | URL | Use |
| --- | --- | --- |
| Tailwind colors | https://tailwindcss.com/docs/customizing-colors | Practical 50-950 color ramps. |
| Radix Colors | https://www.radix-ui.com/colors | Accessible color scales designed for UI states. |
| Adobe Color | https://color.adobe.com/ | Palette exploration and color harmony. |
| Coolors | https://coolors.co/ | Fast palette generation. |
| Accessible Color Matrix | https://toolness.github.io/accessible-color-matrix/ | Contrast-pair checking across palettes. |
| APCA Contrast Calculator | https://www.myndex.com/APCA/ | Advanced contrast review; use alongside WCAG where appropriate. |
| W3C Design Tokens | https://www.designtokens.org/ | Interoperable token format reference. |
| Style Dictionary | https://amzn.github.io/style-dictionary/ | Token build pipeline reference. |

Skill rule: build semantic roles, not just pretty palettes: background, surface,
text, muted text, border, primary, secondary, success, warning, danger, info,
focus, selection, and chart colors.

## 7. Free Animations, Loading Screens, And Motion Assets

Use these only when motion has a job: orientation, feedback, loading clarity,
state continuity, or one deliberate brand moment.

| Source | URL | Use |
| --- | --- | --- |
| Motion | https://motion.dev/ | Default React/JS UI animation engine. |
| Motion Primitives | https://motion-primitives.com/ | App-safe animated primitives. |
| Auto Animate | https://auto-animate.formkit.com/ | Quick list/layout transitions. |
| Number Flow | https://number-flow.barvian.me/ | Animated metrics and price/value changes. |
| LottieFiles | https://lottiefiles.com/ | Lottie assets and workflow. |
| lottie-web | https://github.com/airbnb/lottie-web | Runtime for Lottie animations. |
| Animated Icons | https://animatedicons.co/ | Free animated SVG/Lottie/PNG icon source. |
| useAnimations | https://useanimations.com/ | Feather-inspired Lottie/SVG micro-animations. |
| Rive | https://rive.app/ | Interactive vector animation and state machines. |
| canvas-confetti | https://github.com/catdad/canvas-confetti | Lightweight completion celebration. |
| tsParticles | https://particles.js.org/ | Particle effects; use sparingly. |
| GSAP | https://gsap.com/ | Advanced timelines and public-site motion. |
| anime.js | https://animejs.com/ | Lightweight JS timeline animation. |
| Three.js | https://threejs.org/ | Real 3D/webgl surfaces. |
| PixiJS | https://pixijs.com/ | 2D WebGL/canvas interfaces and games. |
| GSAP ScrollTrigger | https://gsap.com/docs/v3/Plugins/ScrollTrigger/ | Scroll storytelling and complex marketing/case-study timelines. |
| Lenis | https://lenis.darkroom.engineering/ | Smooth scrolling for public/storytelling sites only after keyboard/touch/focus testing. |
| R3F | https://r3f.docs.pmnd.rs/ | React renderer for Three.js scenes. |
| Drei | https://drei.docs.pmnd.rs/ | Helpers for R3F scenes. |
| Spline | https://spline.design/ | Fast 3D scene creation/export when performance is checked. |
| Awwwards animation collections | https://www.awwwards.com/awwwards/collections/animation/ | Inspiration for public/marketing motion, not dense tools. |
| Awwwards loading collections | https://www.awwwards.com/awwwards/collections/loading-page/ | Loading-page inspiration. |
| Awwwards WebGL collections | https://www.awwwards.com/awwwards/collections/webgl/ | WebGL inspiration when 3D is truly part of the product. |

Skill rule: motion must include reduced-motion behavior and must be verified in
desktop/mobile screenshots or a browser check.

Motion class rules:

- App-safe motion: use Motion, Motion Primitives, Auto Animate, and Number Flow
  for state changes, list insertions, drawers, tabs, hover/press, value changes,
  and loading-to-loaded swaps.
- Branded vector/loading: use Lottie/dotLottie or Rive only when there is a real
  asset, state machine, or product moment.
- Scroll storytelling: use GSAP/anime/Lenis only for public sites, launches,
  case studies, or narrative pages.
- 3D/canvas/WebGL: use Three.js, R3F, Drei, PixiJS, or Spline only when depth,
  simulation, inspection, or direct manipulation matters.

Implementation rules:

- Prefer transform and opacity.
- Use determinate progress when progress is known.
- Use indeterminate progress when progress is unknown.
- Use skeletons only when the future layout is predictable.
- Add accessible labels to progress indicators.
- Replace large movement/parallax with opacity or simpler transitions under
  reduced-motion preferences.
- For 3D, avoid a permanent 60fps loop when nothing moves; reuse geometries,
  materials, and assets; dispose of scenes/assets when removed.
- Confetti and celebrations should be rare: publish, paid, completed onboarding,
  milestone reached. Do not celebrate everyday saves.

## 8. Illustrations, Images, Mockups, And Visual Assets

Use these for marketing pages, empty states, onboarding, product visuals, and
hero sections when real screenshots/assets are unavailable.

| Source | URL | Use |
| --- | --- | --- |
| Unsplash | https://unsplash.com/ | Real photography; avoid generic stock feel. |
| Pexels | https://www.pexels.com/ | Free photos/videos. |
| unDraw | https://undraw.co/illustrations | Custom-color SVG illustrations; can look generic if overused. |
| ManyPixels Gallery | https://www.manypixels.co/gallery | Free SVG illustrations. |
| Open Doodles | https://www.opendoodles.com/ | Hand-drawn SVG illustrations. |
| Blush | https://blush.design/ | Illustration packs and customization. |
| Shots.so | https://shots.so/ | Product screenshot mockups. |
| Squoosh | https://squoosh.app/ | Image compression. |
| SVGOMG | https://jakearchibald.github.io/svgomg/ | SVG optimization. |

Skill rule: prefer product screenshots, real UI, or generated product-specific
images over generic illustrations. If using stock/illustration, adapt it to the
brand and user job.

## 9. Real-Product Inspiration And Flow Libraries

Use these to study actual product patterns when copying code is not the point.

| Source | URL | Use |
| --- | --- | --- |
| Mobbin | https://mobbin.com/ | Real mobile/web app screens and flows. |
| Nicelydone | https://nicelydone.club/ | SaaS screens, flows, components, and comparisons. |
| SaaSFrame | https://www.saasframe.io/ | SaaS websites, product screens, and patterns. |
| Pageflows | https://pageflows.com/ | Flow videos/screenshots for onboarding, checkout, settings, and more. |
| UI Sources | https://www.uisources.com/ | Mobile interaction flow references. |
| Godly | https://godly.website/ | High-polish website inspiration. |
| SiteSee | https://sitesee.co/ | Curated modern web design. |
| Minimal Gallery | https://minimal.gallery/ | Clean minimal website references. |
| Land-book | https://land-book.com/ | Landing page inspiration. |
| Footer.design | https://www.footer.design/ | Footer patterns. |
| Navbar Gallery | https://www.navbar.gallery/ | Navigation patterns. |

Skill rule: extract structure and states, not brand. Use at most 2-4
references per screen.

## 10. Data Visualization, Charts, And Maps

Use these for dashboards, analytics, reports, finance, logistics, and internal
tools.

| Source | URL | Use |
| --- | --- | --- |
| Recharts | https://recharts.org/ | Practical React charts. |
| Nivo | https://nivo.rocks/ | Rich chart library with many chart types. |
| Visx | https://airbnb.io/visx/ | Low-level visualization primitives. |
| Observable Plot | https://observablehq.com/plot/ | Data visualization grammar. |
| D3 | https://d3js.org/ | Custom visualization. |
| Tremor | https://www.tremor.so/ | Dashboard-oriented chart components. |
| MapLibre GL JS | https://maplibre.org/ | Open map rendering. |
| deck.gl | https://deck.gl/ | WebGL data maps and large geospatial visualization. |

Skill rule: charts must answer a decision question. Avoid decorative charts,
fake metrics, and legends that make data harder to read.

## 11. AI, Agent, And Generative UI

Use for assistants, tool-running, approval flows, voice UI, multimodal UI, and
generative interfaces.

| Source | URL | Use |
| --- | --- | --- |
| assistant-ui | https://www.assistant-ui.com/ | Assistant chat/thread/composer patterns. |
| AI Elements | https://ai-sdk.dev/elements | AI-native shadcn components for messages, reasoning, tool calls, and conversations. |
| CopilotKit | https://www.copilotkit.ai/ | Copilots, side panels, generative UI, and agent workflows. |
| ElevenLabs UI | https://github.com/elevenlabs/ui | Voice/multimodal agent UI components. |
| LangChain Agent Chat UI | https://github.com/langchain-ai/agent-chat-ui | Tool-running and agent thread surfaces. |
| Manifest UI | https://github.com/mnfst/manifest-ui | MCP/ChatGPT app UI inspiration. |

Skill rule: never make the whole product a plain chat box. Include tool state,
approval state, failure state, receipts/proof, and a non-chat way to inspect
work.

## 12. Visual QA, Reference Matching, And Accessibility Automation

Use these to prove that the design is not just described well but actually built
well.

| Source | URL | Use |
| --- | --- | --- |
| Browser Harness screenshots | https://browser-harness.dev/docs/test-snapshots | Route-level screenshots and screenshot comparisons. |
| Storybook tests | https://storybook.js.org/docs/writing-tests | Component states as test cases. |
| Chromatic | https://www.chromatic.com/ | Storybook visual regression and review. |
| axe-core | https://github.com/dequelabs/axe-core | Accessibility engine. |
| jest-axe | https://github.com/NickColley/jest-axe | Accessibility assertions in tests. |
| Lighthouse | https://developer.chrome.com/docs/lighthouse | Performance/accessibility/SEO checks. |
| Pa11y | https://pa11y.org/ | Automated accessibility testing. |
| Contrast Grid | https://contrast-grid.eightshapes.com/ | Palette contrast matrix. |
| Percy | https://percy.io/ | Visual regression for pages/components. |
| Argos | https://argos-ci.com/ | Open-source visual regression and PR screenshot review. |

Skill rule: visual proof should match the risk. A single component may need
Storybook states. A page or reference build needs desktop/mobile screenshots.
A shared design system component may need visual regression and accessibility
tests.

## 13. Psychology, Brand Systems, Color Meaning, And Video Learning

Use these when a project needs better design judgment, a stronger brand system,
or a palette that has a real reason behind it.

| Source | URL | Use |
| --- | --- | --- |
| NN/g 5 Visual Design Principles | https://www.nngroup.com/articles/principles-visual-design/ | Practical psychology layer: scale, hierarchy, balance, contrast, and Gestalt grouping. |
| Color Semantics in Human Cognition | https://journals.sagepub.com/doi/10.1177/09637214231208189 | Stronger color rule than "blue means trust": color meaning depends on concept, context, and user expectation. |
| Frontiers color psychology review | https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2015.00368/full | Reminder to treat color psychology as directional, not universal truth. |
| Material color system | https://m1.material.io/style/color.html | Palette roles, primary/secondary colors, state colors, and legibility. |
| W3C contrast guidance | https://www.w3.org/TR/UNDERSTANDING-WCAG20/visual-audio-contrast-contrast.html | Contrast floor for text, icons, controls, and state indicators. |
| Figma design systems | https://www.figma.com/design-systems/ | Design-system workflow, variables, component consistency, and team handoff. |
| Figma multi-brand systems | https://www.figma.com/blog/creating-multi-brand-design-systems/ | Multi-brand/token governance when one product family needs variants. |
| Frontify visual identity | https://www.frontify.com/en/guide/visual-identity | Brand identity beyond logo/color: type, imagery, layout, icons, motion, and usage rules. |
| Frontify brand system | https://www.frontify.com/en/guide/brand-system | Brand governance and reusable brand assets. |
| Primer | https://primer.style/ | Mature product/brand/accessibility system from GitHub. |
| GitHub Brand Toolkit | https://brand.github.com/ | Example of brand decks as usable web systems, including motion and presentation rules. |
| Primer Primitives | https://primer.style/primitives/ | Code-backed design tokens and modes. |
| USWDS | https://designsystem.digital.gov/ | Production-grade governance, accessibility, theming, and public UX rules. |
| awesome-design-md | https://github.com/VoltAgent/awesome-design-md | AI-agent-oriented DESIGN.md library for converting real visual systems into instructions. |
| designmd.ai | https://designmd.ai/ | DESIGN.md library and workflow for AI coding tools. |

Skill rules:

- Hierarchy before decoration: every design packet must name the primary focal
  point, secondary scan path, and grouping cues.
- Do not use universal color-psychology claims. A palette needs audience,
  context, product job, and semantic role rationale.
- When color carries meaning, document the concept-color mapping and test
  whether it matches user expectation.
- Every serious palette needs semantic roles, light/dark behavior, state roles,
  and contrast proof for text, icons, controls, borders, focus, and status.
- Brand systems are more than colors and logos. A serious brand packet needs
  typography, layout, imagery, icon style, motion, voice, misuse rules, and
  governance.
- Use purpose-based token names where possible, such as `color.action.primary`
  or `surface.warning`, instead of paint names like `blue-500`.
- For code-backed systems, capture the token/export path and component source
  path. Screenshots alone are not enough.
- AI-ready design systems need a source of truth, component integrity,
  Storybook or equivalent proof, and token governance.
- For no-reference design, compare 10-30 examples from the same product family
  or source recipe when time allows. The goal is to learn the category shape,
  not to mix all examples into one screen.
- A design review should name the primary user need, primary action, recovery
  path, and one thing the design removed or simplified before discussing style.
- Color cannot be the only status signal. Pair it with text, iconography,
  placement, shape, or component state.
- Readability is a design feature: control line length, line height, contrast,
  label proximity, and paragraph rhythm before adding visual effects.
- AI-assisted design systems need written reasoning and examples, not only
  tokens. Capture why a direction fits, where it should not be used, and what a
  bad version looks like.

### YouTube And Video Research

Use YouTube for learning and critique when it improves design judgment or
implementation craft. Do not blindly copy a video's style.

Checked video lanes on 2026-05-18:

| Video or channel | URL | Use |
| --- | --- | --- |
| Steve Schoger - Refactoring UI: Transistor | https://www.youtube.com/watch?v=ZT4WRRhacWk | Developer-facing UI refactor patterns for spacing, hierarchy, and component polish. Caption availability was checked during research. |
| Steve Schoger - Refactoring UI: WP Pusher Checkout Page | https://www.youtube.com/watch?v=5gdYHlYAKDY | Checkout/payment form hierarchy and trust cues. |
| DesignCourse - This is how you Refactor a UI Design | https://www.youtube.com/watch?v=bFIIHOI5QoE | Fast visual critique and before/after refactor thinking. |
| Kristian - Why Most AI Design Looks Like AI Slop And How to Fix It | https://www.youtube.com/watch?v=NRE4kv8RS68 | AI-specific anti-slop framing: avoid generic patterns, use stronger references, and repair visible weaknesses. Caption availability was checked during research. |
| Tom Is Loading - 10 Ways to Prevent AI Slop in Your Frontend UIs | https://www.youtube.com/watch?v=zKBUBVtoM0g | AI UI quality-control checklist ideas. Use as a critique lane, not style copying. |
| Memberstack - How To Vibe Code Beautiful Front Ends: No More AI Slop | https://www.youtube.com/watch?v=XI8JtpWza74 | AI/vibe-coding-specific front-end process. Caption availability was checked during research. |
| UI Collective - Generate Better AI Designs in Claude Code | https://www.youtube.com/watch?v=nbk0PMS0tos | Claude/Codex prompting and visual review workflow ideas. |
| Malewicz - Claude Design is NOT what you think | https://www.youtube.com/watch?v=IkspcJdeP3U | Taste, critique, and limitations of AI-generated visual design. |
| Build Great Products - How to Build ACTUALLY Beautiful UI With This Claude Code Skill | https://www.youtube.com/watch?v=95_NJ-a-CMQ | Claude/Codex-style skill workflow inspiration. |
| Figma - The future of design systems and AI | https://www.youtube.com/watch?v=N2NwII5mAU4 | AI-ready design-system direction. Caption availability was checked during research. Use only for system thinking, not as a default handoff requirement. |
| Figma - Figma + developer workflows | https://www.youtube.com/watch?v=A4mqzgFbmjI | Design-system and developer workflow ideas for mapped components and source-of-truth thinking. Caption availability was checked during research. |
| Product Craft - AI-Ready Design Systems w/ TJ Pitre | https://www.youtube.com/watch?v=qt-xw-3IWt8 | Long-form AI/design-system strategy; use when improving system governance. |
| Jesse Showalter - Color Theory in UI Design | https://www.youtube.com/watch?v=-4lMJ4is2pE | Color theory for UI builders. Caption availability was checked during research. |
| DesignCourse - Typographic Visual Hierarchy in UI Design | https://www.youtube.com/watch?v=u9XSmlZhYq4 | Typography hierarchy, grouping, and scan-order lessons. Caption availability was checked during research. |
| NNgroup - Visual Hierarchy | https://www.youtube.com/watch?v=8OTbyWndY9M | Research-backed hierarchy explanation for scanning and attention. |
| Jesse Showalter - Master Spacing in UI Design | https://www.youtube.com/watch?v=cf95Z7Ngg8k | Practical spacing and layout rhythm. |
| Jesse Showalter - Amateur vs Pro UI Design | https://www.youtube.com/watch?v=XZf5A0wcruE | Before/after critique lane for spotting amateur visual mistakes. Caption availability was checked during research. |
| Geckoboard - 12 Dashboard design tips | https://www.youtube.com/watch?v=t3cAUt7sOQg | Dashboard-specific hierarchy, chart, and metric presentation lessons. |
| Kevin Powell YouTube channel | https://www.youtube.com/@KevinPowell | CSS layout, responsiveness, and implementation craft. |
| Figma YouTube channel | https://www.youtube.com/@figma | Official design-system, variable, and workflow source. |
| DesignCourse YouTube channel | https://www.youtube.com/@DesignCourse | Developer-to-designer UI lessons, critique, and refactor walkthroughs. |

Video extraction rule:

1. Search the video lane.
2. Prefer official, reputable, or highly specific videos.
3. Download captions/transcripts when available before extracting lessons, but
   do not claim permanent transcript artifacts exist unless they were saved in
   the skill tree.
4. Save only 3-5 reusable heuristics and 1 anti-pattern list.
5. Translate the lesson into layout, hierarchy, typography, color, motion,
   state coverage, accessibility, or proof behavior.

Do not claim a video was fully watched unless screenshots, notes, or transcript
evidence were actually gathered. If only metadata/search results were checked,
say that plainly.

## 14. What This Adds To Codex

When the user gives no reference, Codex should now:

1. infer product type and workflow density
2. choose one art direction
3. choose a resource lane from this file
4. adapt code/assets only when they serve the product
5. build all meaningful states
6. use motion only with a job
7. prove the final UI on desktop and mobile

When the user gives a reference, Codex should:

1. extract layout, hierarchy, spacing, type, color, surfaces, states, and motion
2. build the actual screen
3. compare screenshots against the reference
4. patch the biggest mismatch before calling it done
