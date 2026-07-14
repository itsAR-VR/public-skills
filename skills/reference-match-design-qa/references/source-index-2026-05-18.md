# Design Source Index

Research date: 2026-05-18

Purpose: give Codex and Claude better design taste and better pullable code
sources for future UI builds. Use this with `reference-match-design-qa` and
`vibe-design-reference-libraries`.

For build-type selection, use
`universal-code-backed-pattern-library.md` first. This source index answers
"where can we pull or study patterns from?" The universal library answers
"which kind of interface are we building?"

For the design judgment layer, use `design-doctrine-and-qa.md`. For the newest
additive GitHub sources, use `additive-github-source-lanes-2026-05-18.md`.

## Method

- GitHub sweep: 40 broad repository searches across shadcn, Tailwind, React UI
  components, dashboards, admin templates, registries, motion, Storybook,
  design systems, SaaS starters, landing pages, mobile-style UI, and
  copy-paste component libraries.
- GitHub result volume: 1,360 unique repositories after dedupe.
- Targeted follow-up searches checked AI-native UI, assistant/chat shells,
  voice/agent components, motion primitives, animation engines, loading-screen
  sources, Lottie/Rive-style vector animation, and React Aria/Tailwind sources.
- Web sweep: current UI/vibe-coding component sites, shadcn registry explorers,
  real SaaS/app inspiration libraries, and visual QA docs.
- Documentation check: Context7 was used for current Browser Harness and Storybook
  visual testing behavior.
- Follow-up agent research added source-backed doctrine from Apple, Material,
  NN/g, WAI/WCAG, Storybook, W3C Design Tokens, Atlassian, Carbon, Refactoring
  UI, Learn UI Design, LearnVisual.Design, DesignCourse, and Kevin Powell.
- Follow-up GitHub research added high-signal source lanes for Animate UI,
  Number Flow, Auto Animate, Park UI, Base UI, React Spectrum, shadcn-admin,
  tablecn, OpenStatus data-table-filters, CopilotKit, ElevenLabs UI, LangChain
  Agent Chat UI, Vercel Commerce, Schedule-X, Lexical, Plate, xyflow, tldraw,
  dnd-kit, Uppy, and MapLibre.

This is not the literal entirety of GitHub. It is a wide practical sweep of the
GitHub surface most likely to improve product UI quality.

## Highest-Signal Source Lanes

### 1. Pullable shadcn and React/Tailwind code

Use these when the target repo is React/Next/Vite plus Tailwind or shadcn-style
components and we need actual code to adapt.

| Source | Stars at scan | Best use | Notes |
| --- | ---: | --- | --- |
| `shadcn-ui/ui` | 114k+ | Accessible open-code primitives and registry model | Default foundation for React/Tailwind apps. |
| `registry.directory` | n/a | Registry discovery | Lists shadcn/ui, Dice UI, Tailark, Coss UI, AI Elements, Magic UI, Animate UI, ReUI, and more. |
| `keenthemes/reui` | 2.9k+ | Production product flows and complex widgets | Strong for data grid, filters, file upload, Kanban, empty states, cards, timelines. |
| `serafimcloud/21st` | 5.2k+ | Marketplace of shadcn-based blocks/hooks | Use as discovery and code source when licensing/dependencies fit. |
| `magicuidesign/magicui` | 21k+ | Animated shadcn/Tailwind components | Good for memorable public surfaces and selective app polish. |
| `DavidHDev/react-bits` | 39k+ | Animated/interactable React components | Good for hero moments, backgrounds, text, 3D-ish effects; use sparingly. |
| `tailark/blocks` | 2.2k+ | Marketing shadcn blocks | Good for landing pages, feature sections, pricing, nav/hero/footer. |
| `akash3444/shadcn-ui-blocks` | 600+ | Copy/paste shadcn blocks | Good lightweight free block source. |
| `shadcnspace/shadcnspace` | 500+ | Open shadcn blocks/templates/layouts | Good for React/Tailwind/Base UI-friendly structures. |
| `crafter-station/elements` | 490+ | Full-stack shadcn blocks | Auth, payments, AI, logos; inspect dependencies carefully. |
| `shadcnstudio/shadcn-studio` | 1.5k+ | Components, blocks, themes, theme generator | Use for theme exploration and shadcn ecosystem discovery. |
| `damien-schneider/cuicui` | 950+ | Clean copy/paste components, low-JS bias | Good when simple CSS-first components are preferable. |

Default behavior: pull only the needed component or block, then rewrite it into
the local component system. Do not paste a whole visual identity. the user has
approved GitHub code use, so license should not be treated as a blocker when
the user has explicitly approved the source; still inspect safety, provenance,
dependencies, and product fit before copying.

### 2. Dashboard, admin, and dense app shells

Use these for Chief, Jarvis operator views, CRMs, internal tools,
analytics, tables, filters, proof panels, and admin surfaces.

| Source | Stars at scan | Best use | Notes |
| --- | ---: | --- | --- |
| `satnaing/shadcn-admin` | 12k+ | Vite/shadcn admin dashboard | Excellent app shell and dashboard structure reference. |
| `Kiranism/next-shadcn-dashboard-starter` | 6.4k+ | Next.js shadcn admin starter | Strong for Next.js dashboard baseline. |
| `arhamkhnz/next-shadcn-admin-dashboard` | 2.3k+ | Modern Next admin dashboard | Use for shell, nav, layout density. |
| `sadmann7/tablecn` | 6.1k+ | shadcn data table | Use for dense tables with sorting/filtering/pagination. |
| `openstatusHQ/data-table-filters` | 2k+ | Faceted table filters | Good for operational filtering patterns. |
| `marmelab/shadcn-admin-kit` | 900+ | Admin kit using shadcn | Use for CRUD/admin workflow structure. |
| `marmelab/atomic-crm` | 980+ | Full CRM product example | Good for real app flows and data surfaces. |
| `vbenjs/vue-vben-admin` | 32k+ | Vue admin shell | Use as cross-framework dashboard pattern reference. |

Dashboard rule: dense product workflows should feel calm, scanned, and useful.
Avoid marketing hero composition inside admin screens.

### 3. Real product UX and flow galleries

Use these when no code should be copied, but the design needs better product
judgment, screen sequence, state design, or real-world UX patterns.

| Source | Best use | Notes |
| --- | --- | --- |
| Mobbin | Mobile/web app screens, UI elements, flows, microinteractions | Strongest for real product patterns. |
| Nicelydone | SaaS app screens, full user flows, components | Strong for SaaS workflows and comparisons. |
| SaaSFrame | SaaS websites, product screens, sections, patterns | Strong for landing, pricing, onboarding, dashboards, settings. |
| Pageflows | User-flow videos and screenshots | Strong when interaction sequence matters. |
| UIguana | Free mobile app flows | Good fallback for mobile patterns. |
| Godly / Godly.design | High-quality web/app inspiration | Good for art direction and layout quality bar. |
| SiteSee / Minimal Gallery | Curated modern websites | Good for public site and brand direction. |

Workflow: pull 6-12 examples from one flow type, extract common structure, then
choose one direction. Do not copy a brand's look.

### 4. Motion and memorable moments

Use these only when motion improves comprehension, brand memory, or transition
clarity.

| Source | Best use | Notes |
| --- | --- | --- |
| Magic UI | Animated components/effects for design engineers | Good for small public-site polish and hero moments. |
| React Bits | More expressive animation/interaction components | Great for memorable but risky effects; use restraint. |
| Motion Primitives | Open-source animated React primitives | Strong source for cleaner, reusable motion patterns. |
| Animate UI | shadcn-compatible animated primitives | Best app-safe motion source. |
| Auto Animate | Low-setup layout/list animation | Strong for quick list, accordion, and loading-to-loaded polish. |
| Number Flow | Animated number transitions | Strong for dashboard counters, prices, and metric deltas. |
| SmoothUI | Motion-based shadcn-compatible components | Good for small effects. |
| Cult UI | Design-engineering components | Good for selected inspiration. |
| Vengeance UI | Dramatic hero/dock/glow/3D effects | Use only for special moments, not dense tools. |
| MotionSites | Motion-first hero prompts | Use for public/launch surfaces only. |

Motion rule: operational tools should use motion for orientation and state
change, not spectacle.

#### Animation Engines And Loading-State Sources

Use these when the build needs more than component-level polish: custom page
transitions, loading screens, animated illustrations, canvas/WebGL motion,
success/failure celebrations, or branded motion systems.

| Source | Stars at scan | Best use | Notes |
| --- | ---: | --- | --- |
| `motiondivision/motion` | 31.9k+ | Default React/JS UI animation engine | MIT. Best first choice for app-safe enter/exit, layout, gesture, and state transitions. |
| `pmndrs/react-spring` | 29k+ | Physics-based UI motion | MIT. Good for natural transitions and advanced interaction when spring behavior matters. |
| `greensock/GSAP` | 24.7k+ | Complex timelines, scroll animations, hero/site motion | License needs review. Excellent for high-end websites, but usually too much for simple app states. |
| `juliangarnier/anime` | 68.5k+ | Lightweight JS animation timelines | MIT. Useful when not tied to React/Motion and when fine timeline control is needed. |
| `airbnb/lottie-web` | 31.8k+ | After Effects vector animations | MIT. Strong for branded loading screens, empty states, onboarding illustrations, and tiny delight moments. |
| `LottieFiles/dotlottie-web` | 500+ | dotLottie/Lottie web player | MIT. Good modern player when using LottieFiles/dotLottie assets. |
| `rive-app/rive-wasm` | 900+ | Interactive vector animations | MIT. Good for state machines, character/mascot-like loaders, and interactive onboarding, but requires asset workflow. |
| `tsparticles/tsparticles` | 8.8k+ | Particles, confetti, fireworks, animated backgrounds | MIT. Use only when particles carry brand/product meaning; can become generic quickly. |
| `catdad/canvas-confetti` | 12.5k+ | Lightweight success celebration | ISC. Good for rare, meaningful completion moments, not normal workflow feedback. |
| `animate-css/animate.css` | 82.5k+ | Simple CSS entrance/attention animations | License/provenance should be checked. Useful for small CSS-only motion, but can look dated if overused. |
| `barvian/number-flow` | 7.3k+ | Animated numbers | MIT. Useful for metrics and counters when values change. |
| `mrdoob/three.js` | 112k+ | 3D/webgl scenes | MIT. Use for real 3D product moments, not decorative hero filler. |
| `pixijs/pixijs` | 47k+ | 2D WebGL/canvas animation | MIT. Useful for game-like or canvas-heavy interfaces. |
| `darkroomengineering/lenis` | 13.8k+ | Smooth scrolling | MIT. Use for public/storytelling sites only; avoid in dense tools unless tested carefully. |

Animation selection rule:

- App workflow motion: Motion, Motion Primitives, Animate UI.
- Loading screens and empty states: Lottie/dotLottie, Rive, Animate UI
  skeletons, Uiverse/Magic UI loaders.
- Public website/hero motion: GSAP, anime.js, React Bits, Magic UI, Vengeance
  UI, MotionSites.
- Success moments: canvas-confetti, Number Flow, small Motion transitions.
- 3D/canvas-heavy builds: Three.js or PixiJS only when the product actually
  benefits from interactive visuals.

### 5. AI, agent, chat, and voice interfaces

Use these for Chief, Jarvis, AI builders, command workspaces, chat surfaces,
tool-call cards, streaming answers, multimodal/voice UI, MCP/app interfaces,
and generative UI.

| Source | Stars at scan | Best use | Notes |
| --- | ---: | --- | --- |
| `assistant-ui/assistant-ui` | 10.1k+ | AI chat shells and assistant UX | MIT. Strong source for conversation layout, composer, threads, actions, and stateful assistant surfaces. |
| `vercel/ai-elements` | 2k+ | AI-native shadcn components | Strong source for messages, conversations, tool states, reasoning, and generative UI. License/provenance must be checked per component. |
| `CopilotKit/CopilotKit` | 31k+ | Copilots, side panels, generative UI, approvals, and tool-driven workflows | MIT. Heavy framework assumptions; borrow patterns before adopting the stack. |
| `elevenlabs/ui` | 2.2k+ | Multimodal and voice-agent UI | MIT. Strong source for audio/agent components, waveform-style states, and voice surfaces. |
| `langchain-ai/agent-chat-ui` | 2.8k+ | Agent execution surfaces, tool-running, and thread history | MIT. Useful patterns, but avoid coupling to one backend stack. |
| `mnfst/manifest-ui` | small but focused | ChatGPT/MCP app UI | MIT. Use as a focused source for ChatGPT Apps and MCP app component structure. |
| `21st.dev Agent Elements` | registry source | Agent UI primitives | Good for chat shells, tool-call cards, edit/search/todo/plan surfaces, and streaming markdown patterns. |
| `Supabase UI` | registry source | Data-connected product components | Useful when AI/product screens need auth, database, storage, or backend-tied UI blocks. |

AI interface rule: build beyond a chat box. Include pending, streaming,
tool-running, approval-needed, failed, empty, completed, and receipt/proof
states when the workflow needs them.

### 6. Mature design systems and primitives

Use these for accessibility, interaction behavior, component anatomy, and state
coverage.

| Source | Best use |
| --- | --- |
| Radix UI | Accessible React primitives under shadcn-style components. |
| Base UI | Unstyled accessible primitives; strong alternative to Radix. |
| React Spectrum | Deep accessibility, adaptive behavior, and complex component state modeling. |
| Park UI | Ark UI/Panda component anatomy and token structure. |
| Headless UI | Unstyled accessible Tailwind-friendly components. |
| Intent UI, Untitled UI React, Jolly UI | React Aria/Tailwind copy-paste component systems. |
| Storybook | Isolated component review, stories, docs, snapshot/visual test surface. |
| Carbon, Fluent UI, Primer, Polaris, USWDS, TDesign, Arco | Mature systems for enterprise, public, or complex product reference. |

Do not adopt a mature system's brand wholesale unless the project already uses
it. Extract state coverage, spacing discipline, accessibility, and component
anatomy.

### 7. Workflow-specific code sources

Use these when the build type is specific enough that generic blocks are not
enough.

| Source | Stars at scan | Best use | Notes |
| --- | ---: | --- | --- |
| `TanStack/table` | 27.9k+ | Headless tables and data grids | MIT. Pair with local visual components. |
| `TanStack/form` | 6.5k+ | Type-safe forms | MIT. Good for complex settings and intake flows. |
| `react-hook-form/react-hook-form` | 44.7k+ | React form state and validation | MIT. Common practical default. |
| `fullcalendar/fullcalendar` | 20.4k+ | Full event calendars | MIT. Good for booking and scheduling tools. |
| `schedule-x/schedule-x` | 2.3k+ | Modern JS event calendar | MIT. Useful alternative calendar source. |
| `ueberdosis/tiptap` | 36.8k+ | Rich text editor | MIT. Good for docs, CMS, notes, and editors. |
| `facebook/lexical` | 23.4k+ | Extensible editor framework | MIT. Strong editor foundation. |
| `udecode/plate` | 16.2k+ | AI/shadcn rich text editor | License needs review; strong pattern source. |
| `xyflow/xyflow` | 36.6k+ | Node graphs and workflow builders | MIT. Use for flow editors and agent graphs. |
| `tldraw/tldraw` | 47k+ | Whiteboard/canvas SDK | License needs review before direct reuse. |
| `excalidraw/excalidraw` | 123k+ | Whiteboard and diagram reference | MIT. Pattern/source for sketch canvases. |
| `clauderic/dnd-kit` | 17.1k+ | Drag and drop | MIT. Use for boards, sortables, builders. |
| `transloadit/uppy` | 30.7k+ | File uploads | MIT. Use for upload/import/media flows. |
| `pqina/filepond` | 16.3k+ | File upload UI | MIT. Good upload UX reference and code source. |
| `dip/cmdk` | 12.5k+ | Command menu | MIT. Strong command/search primitive. |
| `mapbox/mapbox-gl-js` | 12.2k+ | Interactive maps | License needs review; often pattern/source only. |
| `maplibre/maplibre-gl-js` | 10.6k+ | Open map rendering | License needs review; good Mapbox alternative. |
| `visgl/deck.gl` | 14.1k+ | WebGL data maps | MIT. Use for heavy geospatial visualization. |
| `pmndrs/react-three-fiber` | 30.8k+ | React renderer for Three.js | MIT. Use for real 3D interfaces. |
| `pmndrs/drei` | 9.6k+ | React Three Fiber helpers | MIT. Use with react-three-fiber. |

### 8. AI/vibe-code design sources

Use these to improve prompts and AI-builder handoff, not as final design
authority.

| Source | Best use |
| --- | --- |
| VibeUI | Layout prompts for auth, pricing, heroes, dashboards, onboarding. |
| Vibe Code Components | Component prompt cards for interactions and app patterns. |
| Trickle prompt library | Visual style, interaction, brand mood prompts. |
| Glyphra | AI component generation with live preview/code ideas. |
| SpicyUI | AI-generated/community UI component exploration. |
| Fio | Real-code design canvas concept; useful for agent design-system thinking. |

Prompt sources must still be constrained by the product, stack, target users,
and screenshot proof.

## Visual Proof Sources

Current docs checked:

- Browser Harness `toHaveScreenshot`: supports page/locator screenshot assertions,
  full-page capture, masking dynamic content, animation stabilization,
  thresholds, and pixel-diff settings.
- Storybook: supports isolated stories, interaction play functions, portable
  stories, snapshot tests, and visual testing workflows such as Chromatic.

Default proof ladder:

1. Human-readable desktop and mobile screenshots for every meaningful UI change.
2. Browser Harness screenshots when the repo has Browser Harness or the change is
   repeatable enough to snapshot.
3. Storybook stories when component states matter more than full route context.
4. Visual regression only after dynamic content is masked/stabilized.

## No-Reference Design Quality Bar

When the user provides no visual reference:

1. Infer product type and workflow density.
2. Pick one lane:
   - SaaS/AI app shell
   - dense internal tool
   - mobile-style app
   - public landing/launch surface
   - onboarding/setup flow
   - data-heavy dashboard
   - command/agent workspace
3. Pull 2-4 sources from the lane above.
4. Create a no-reference design packet.
5. Build the actual UI.
6. Screenshot desktop/mobile.
7. Fix generic choices first: weak hierarchy, card soup, bad spacing, boring type,
   missing states, default purple gradients, fake content, poor mobile.

## GitHub Search Evidence

The 2026-05-18 sweep found 1,360 unique repositories from 40 searches. High
signal examples included:

- `storybookjs/storybook` - 89k+
- `animate-css/animate.css` - 82k+
- `juliangarnier/anime` - 68k+
- `mrdoob/three.js` - 112k+
- `pixijs/pixijs` - 47k+
- `tailwindlabs/headlessui` - 28k+
- `airbnb/lottie-web` - 31k+
- `motiondivision/motion` - 31k+
- `pmndrs/react-spring` - 29k+
- `greensock/GSAP` - 24k+
- `alexpate/awesome-design-systems` - 24k+
- `birobirobiro/awesome-shadcn-ui` - 19k+
- `nextjs/saas-starter` - 15k+
- `darkroomengineering/lenis` - 13k+
- `catdad/canvas-confetti` - 12k+
- `satnaing/shadcn-admin` - 12k+
- `assistant-ui/assistant-ui` - 10k+
- `jnsahaj/tweakcn` - 9.8k+
- `themesberg/flowbite` - 9.2k+
- `tsparticles/tsparticles` - 8.8k+
- `barvian/number-flow` - 7.3k+
- `Kiranism/next-shadcn-dashboard-starter` - 6.4k+
- `sadmann7/tablecn` - 6.1k+
- `serafimcloud/21st` - 5.2k+
- `ibelick/motion-primitives` - 5.5k+
- `keenthemes/reui` - 2.9k+
- `tailark/blocks` - 2.2k+
- `elevenlabs/ui` - 2.2k+
- `vercel/ai-elements` - 2k+
- `openstatusHQ/data-table-filters` - 2k+
- `LottieFiles/lottie-player` - 1.6k+
- `intentui/intentui` - 1.9k+
- `untitleduico/react` - 1.7k+
- `jolbol1/jolly-ui` - 1.1k+
- `rive-app/rive-wasm` - 900+
- `marmelab/atomic-crm` - 980+

Use star count only as a signal, not a decision rule. A smaller repo may be more
useful if it solves the exact UI pattern.

## Psychology, Brand, And YouTube Sweep

The follow-up psychology and video sweep added these source lanes:

- visual psychology: NN/g visual design principles for scale, hierarchy,
  balance, contrast, and Gestalt grouping
- color meaning: color semantics research and color psychology reviews; use
  color-emotion claims only as contextual hypotheses, not universal rules
- brand systems: Figma design systems, Frontify, Primer, GitHub Brand Toolkit,
  Carbon, USWDS, and semantic token governance
- AI-ready design systems: Storybook/proof surfaces, component integrity,
  source-of-truth design docs, tokens, and governance
- video learning: Steve Schoger Refactoring UI, Figma design-system videos,
  Memberstack/Build Great Products vibe-coding design videos, Jesse Showalter
  color theory, Kevin Powell CSS implementation, and DesignCourse refactor
  walkthroughs

Video research rule: prefer captions/transcripts when available, then extract
only durable heuristics and anti-patterns. Do not claim a video was fully
watched unless transcript or note evidence exists.

## Source URLs

- https://github.com/shadcn-ui/ui
- https://registry.directory/
- https://reui.io/
- https://github.com/keenthemes/reui
- https://www.shadcnblocks.com/
- https://github.com/akash3444/shadcn-ui-blocks
- https://github.com/shadcnspace/shadcnspace
- https://github.com/crafter-station/elements
- https://github.com/serafimcloud/21st
- https://21st.dev/
- https://github.com/magicuidesign/magicui
- https://magicui.design/
- https://github.com/DavidHDev/react-bits
- https://reactbits.dev/
- https://github.com/motiondivision/motion
- https://motion.dev/
- https://github.com/pmndrs/react-spring
- https://www.react-spring.dev/
- https://github.com/greensock/GSAP
- https://gsap.com/
- https://github.com/juliangarnier/anime
- https://animejs.com/
- https://github.com/airbnb/lottie-web
- https://github.com/LottieFiles/dotlottie-web
- https://github.com/LottieFiles/lottie-player
- https://github.com/rive-app/rive-wasm
- https://rive.app/
- https://github.com/tsparticles/tsparticles
- https://particles.js.org/
- https://github.com/catdad/canvas-confetti
- https://catdad.github.io/canvas-confetti/
- https://github.com/animate-css/animate.css
- https://animate.style/
- https://github.com/barvian/number-flow
- https://number-flow.barvian.me/
- https://github.com/mrdoob/three.js
- https://threejs.org/
- https://github.com/pixijs/pixijs
- https://pixijs.com/
- https://github.com/darkroomengineering/lenis
- https://lenis.dev/
- https://github.com/ibelick/motion-primitives
- https://motion-primitives.com/
- https://github.com/tailark/blocks
- https://tailark.com/
- https://github.com/satnaing/shadcn-admin
- https://github.com/Kiranism/next-shadcn-dashboard-starter
- https://github.com/sadmann7/tablecn
- https://github.com/openstatusHQ/data-table-filters
- https://github.com/assistant-ui/assistant-ui
- https://www.assistant-ui.com/
- https://github.com/vercel/ai-elements
- https://elements.ai-sdk.dev/
- https://github.com/elevenlabs/ui
- https://ui.elevenlabs.io/
- https://github.com/mnfst/manifest-ui
- https://ui.manifest.build/
- https://github.com/intentui/intentui
- https://intentui.com/
- https://github.com/untitleduico/react
- https://www.untitledui.com/react/
- https://github.com/jolbol1/jolly-ui
- https://jollyui.dev/
- https://mobbin.com/
- https://nicelydone.club/
- https://www.saasframe.io/
- https://pageflows.com/
- https://uiguana.com/
- https://godly.design/
- https://sitesee.co/
- https://minimal.gallery/
- https://browser-harness.dev/docs/test-snapshots
- https://storybook.js.org/docs/writing-tests/visual-testing
- https://www.nngroup.com/articles/principles-visual-design/
- https://journals.sagepub.com/doi/10.1177/09637214231208189
- https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2015.00368/full
- https://www.figma.com/design-systems/
- https://www.figma.com/blog/creating-multi-brand-design-systems/
- https://www.frontify.com/en/guide/visual-identity
- https://www.frontify.com/en/guide/brand-system
- https://primer.style/
- https://brand.github.com/
- https://primer.style/primitives/
- https://designsystem.digital.gov/
- https://github.com/VoltAgent/awesome-design-md
- https://designmd.ai/
- https://www.youtube.com/watch?v=ZT4WRRhacWk
- https://www.youtube.com/watch?v=5gdYHlYAKDY
- https://www.youtube.com/watch?v=XI8JtpWza74
- https://www.youtube.com/watch?v=95_NJ-a-CMQ
- https://www.youtube.com/watch?v=N2NwII5mAU4
- https://www.youtube.com/watch?v=qt-xw-3IWt8
- https://www.youtube.com/watch?v=-4lMJ4is2pE
