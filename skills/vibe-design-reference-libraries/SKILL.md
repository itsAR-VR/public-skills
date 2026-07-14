---
name: vibe-design-reference-libraries
description: >
  Use when designing or improving product UI from modern vibe-coding and UI
  reference tools, including Vibe Coder Blog, Vibe Code Components, Trickle
  prompt library, VibeUI, MotionSites, Uilora, Forge UI, Uiverse, Animate UI,
  Vengeance UI, ReUI, registry.directory, 21st.dev, Magic UI, React Bits, Motion
  Primitives, Shadcnblocks, Mobbin, Nicelydone, SaaSFrame, assistant-ui, AI
  Elements, ElevenLabs UI, Manifest UI, React Aria/Tailwind libraries, and
  real-product UI galleries. Also use when a build needs reusable React,
  Tailwind, shadcn-style, AI-native, agent, chat, voice, or Motion-inspired code
  patterns for apps, dashboards, onboarding, landing pages, command palettes,
  sheets, cards, forms, animated heroes, premium UI polish, Chief,
  Jarvis, PROJECT, ecommerce, checkout, billing, calendars, editors, canvas builders,
  workflow builders, CRMs, Kanban boards, support inboxes, file uploads,
  mobile-style apps, maps, games, 3D surfaces, or Instagram design-tool
  screenshots. Also use for prompts that
  say to pull code from shadcn design repos, use GitHub UI repos, inspect public
  component code, improve a dashboard from design sources, or run screenshot
  review after implementation. Also use for AI agent workspaces, assistant/chat
  shells, tool-call cards, streaming states, voice/agent UI, generative UI, and
  proof-oriented command/workflow screens.
related_skills:
  - reference-match-design-qa
  - premium-ui-components
  - design-taste-frontend
  - design-system-starter
  - canvas-design
routing:
  domain_keywords:
    - design references
    - UI references
    - vibe coding
    - code-backed patterns
    - shadcn blocks
    - React Tailwind
    - reusable UI code
    - ecommerce
    - checkout
    - calendar
    - editor
    - canvas
    - workflow builder
    - agent UI
    - AI workspace
    - dashboard
    - no reference design
  intent_patterns:
    - "(?:use|pull|inspect).*?(?:github|shadcn|react|tailwind).*?(?:design|UI|component|block|pattern)"
    - "(?:make|build|design|improve).*?(?:app|site|dashboard|ecommerce|checkout|calendar|editor|canvas|AI workspace|agent UI).*?(?:reference|pattern|source|code)"
    - "(?:vibe|premium|less AI|not AI slop).*?(?:design|UI|frontend)"
  lane: codex-worker
  task_type: frontend-design-sources
---

# Vibe Design Reference Libraries

For meaningful UI work, `design-intelligence` is the front door. If this skill
is invoked directly, use it as the source/code lane inside the
design-intelligence workflow, not as a standalone gallery-picking shortcut.

Use this skill to turn modern UI prompt/component galleries into product-specific design direction and reusable implementation patterns. The goal is not to copy a gallery style. The goal is to borrow useful structure, interaction patterns, code architecture, and quality bars, then adapt them to the product, stack, and brand.

For tool-by-tool research notes and source URLs, read `references/research-summary.md`.

For the deeper 2026-05-18 source index, read
`../reference-match-design-qa/references/source-index-2026-05-18.md`.

For universal build-type selection across any future app, website, dashboard,
agent workspace, ecommerce flow, editor, calendar, canvas, or product surface,
read
`../reference-match-design-qa/references/universal-code-backed-pattern-library.md`.

For the professional design judgment layer, read
`../reference-match-design-qa/references/design-doctrine-and-qa.md`.

For broad source selection across typography, colors, box/surface structure,
components, UX flows, motion, icons/media, data-viz/maps, localization, and
visual proof, read
`../reference-match-design-qa/references/design-source-database-index.md`.

For typography, cultural design, fallback stacks, localization, and script
support, read
`../reference-match-design-qa/references/typography-and-cultural-system.md`.

For no-overlap/no-clipping/no-weird-boxes QA, read
`../reference-match-design-qa/references/visual-integrity-gate.md`.

For the newest additive GitHub source lanes, read
`../reference-match-design-qa/references/additive-github-source-lanes-2026-05-18.md`.

For broad design resources across learning, UX, free UI, icons, typography,
color, animations, assets, inspiration, data viz, AI UI, and visual QA, read
`../reference-match-design-qa/references/pro-design-resource-library-2026-05-18.md`.

For no-reference design direction, source recipes, state coverage, screenshot
repair, and GitHub code safety, read:

- `../reference-match-design-qa/references/no-reference-art-direction-catalog.md`
- `../reference-match-design-qa/references/source-recipes-by-product-and-direction.md`
- `../reference-match-design-qa/references/state-coverage-matrix.md`
- `../reference-match-design-qa/references/screenshot-repair-playbook.md`
- `../reference-match-design-qa/references/github-code-safety-checklist.md`

For reusable original React/Tailwind/shadcn-style code patterns, read `references/code-pattern-guide.md` and copy from `assets/react-tailwind-shadcn/` only after checking the target repo stack.

## Quick Workflow

1. Identify the target artifact: app screen, dashboard, onboarding flow, landing page, hero section, component, motion pass, or design audit.
2. Identify the product role: SaaS app, internal tool, AI product, dashboard, ecommerce, calendar, editor, canvas, mobile-style web app, Chief app, Floating Chief, Chief website, admin/PROJECT operator view, Chief workflow, or other product area.
3. Check the local stack before importing anything: `package.json`, framework, styling system, component library, icon library, animation library, and test/browser setup.
4. For broad or no-reference requests, use the universal code-backed pattern library to choose the primary pattern family before choosing visual inspiration.
5. For no-reference requests, choose one `direction_id` and one source recipe before selecting sources.
6. Pick one primary source database category before selecting sources. For
   example: typography, color/tokens, layout/boxes, components, UX flow, motion,
   icons/media, data-viz/maps, localization, or proof.
7. Pick at most 2-4 reference patterns for one screen. Use one primary reference for structure, one for interaction, one for motion, and one for polish when needed.
8. When matching a screenshot, website, app reference, Figma frame, or user-approved taste example, use `reference-match-design-qa` to create a reference packet before coding. Figma is optional; use it only when the user provides it.
9. When no visual reference exists but the user wants stronger design, use `reference-match-design-qa` to create a no-reference design packet before coding. Pick a strong product-appropriate direction instead of asking the user to supply taste examples.
10. If code is useful, prefer original local templates from `assets/react-tailwind-shadcn/` before importing third-party code.
11. Translate references into an implementation plan: information hierarchy, components, states, tokens, typography, cultural/localization needs, motion rules, accessibility, dependencies, and verification proof.

## Reference Lanes

Use the prompt/reference lane when the problem is unclear design direction or weak AI prompts:

- **Vibe Coder Blog**: prompt literacy, tool choice, shipping discipline, and design-to-code guidance.
- **Vibe Code Components**: concrete component prompts for interaction patterns like command palettes, sheets, tabs, tooltips, PWA prompts, voice input, toasts, and guided tours.
- **Trickle Vibe Coding Prompt Library**: visual style, page functionality, interaction/UX, brand mood, and cross-media prompts.
- **VibeUI**: structural layout prompts for auth, pricing, bento/features, heroes, CTAs, stats, nav, testimonials, dashboards, onboarding, and content pages.
- **MotionSites**: high-polish motion-first hero and landing prompt ideas.

Use the component/code inspiration lane when the product already has a clear surface and needs better implementation patterns:

- **Uilora**: cross-platform web/mobile component inspiration for Next.js, React, React Native, Expo, TypeScript, Tailwind, Framer Motion, Radix, and shadcn-style stacks.
- **Forge UI**: React/Next/Tailwind/Motion/shadcn-oriented animated UI components for forms, stats, security, notifications, tabs, and SaaS/product surfaces.
- **Uiverse**: community micro-component patterns for buttons, loaders, forms, cards, tooltips, switches, hover effects, and CSS/Tailwind polish.
- **Animate UI**: shadcn-compatible animated primitives and components powered by Motion.
- **Vengeance UI**: dramatic motion components such as animated heroes, docks, glow border cards, perspective grids, liquid/3D effects, and animated text.
- **ReUI**: production-oriented shadcn components for data grid, filters, file upload, Kanban, sortable, empty states, timeline, and dense app flows.
- **registry.directory**: registry discovery layer for shadcn/ui, Dice UI, Tailark, Coss UI, AI Elements, Magic UI, Animate UI, ReUI, and more.
- **21st.dev**: marketplace/discovery for shadcn-based React/Tailwind components, blocks, hooks, and design-engineering patterns.
- **Shadcnblocks / Shadcnspace / Tailark**: block/template sources for landing, marketing, application shell, dashboard, pricing, feature, navbar, and footer sections.
- **Mobbin / Nicelydone / SaaSFrame / Pageflows / UIguana**: real app and SaaS flow references for workflow structure, not code copying.
- **assistant-ui / AI Elements / ElevenLabs UI / Manifest UI**: AI-native interface sources for chat shells, streaming messages, tool calls, multimodal/voice states, MCP/app UIs, and agent workspaces.
- **Motion Primitives / Intent UI / Untitled UI React / Jolly UI**: motion and React Aria/Tailwind sources for polished, accessible components when shadcn alone is not enough.

## Code Pattern Layer

Use the bundled code patterns when the user asks for actual UI code, a faster build baseline, or reusable component recipes:

- `assets/react-tailwind-shadcn/patterns.tsx`: original React + Tailwind templates for app shells, landing heroes, onboarding wizards, command palettes, sheets, premium cards, form states, and skeletons.
- `assets/react-tailwind-shadcn/motion-patterns.tsx`: optional Motion-powered wrappers for reveal, press, presence, and staggered animation with reduced-motion support.
- `assets/react-tailwind-shadcn/styles.css`: optional CSS helpers for focus rings, surfaces, grid backgrounds, shimmer, and reduced-motion behavior.

Use these patterns as starting points, not as a frozen design system. Replace colors, spacing, typography, and component imports with the target repo's design tokens and local helpers.

## Universal Product Guidance

- **SaaS or AI apps**: favor app shells, command palettes, sheets, empty states, onboarding, proof panels, and calm dashboards.
- **Internal tools**: favor dense layouts, tables, filters, status timelines, keyboard paths, and low-motion state feedback.
- **Landing pages**: favor one clear hero, one product visual, proof, CTA, and restrained motion. Use MotionSites/Trickle/Vengeance UI only when the brand can support it.
- **Mobile-style web apps**: favor bottom actions, safe-area spacing, large touch targets, sheets, compact cards, and reduced typing friction.
- **Ecommerce and billing**: favor product clarity, checkout trust, pricing math, payment states, invoice history, and receipt proof.
- **Calendars and scheduling**: favor availability clarity, timezone handling, agenda fallback, conflict states, and accessible date/time controls.
- **Editors, docs, and knowledge bases**: favor reading comfort, saved/publish states, search, version history, comments, and strong navigation.
- **Canvas, whiteboard, graph, and workflow builders**: favor pan/zoom, selection, inspector panels, undo/redo, empty canvas guidance, and keyboard access.
- **Support and collaboration surfaces**: favor threads, assignment, read/unread state, attachments, status, and clear privacy boundaries.
- **Consumer or portfolio surfaces**: favor stronger visual identity, media, kinetic headers, and memorable microinteractions, but keep accessibility and performance intact.

## Product-Specific Guidance

The skill is universal. Chief is one product-specific layer, not the default
for every build. Use the following Chief rules only when the target product is
Chief or a historical Chief context. For any other product, infer or load that
product's own `DESIGN.md`, brand docs, screenshots, and user job before styling.

### Chief Application Guidance

Chief has its own brand direction: lavender, greys, whites, creams, and blacks. Translate liquid-glass and high-motion inspiration into Chief's language; do not copy dark-dashboard, neon, or generic AI-SaaS styling by default.

- **Chief app**: prioritize calm command-center surfaces, work queues, proof states, approval states, timelines, and dense but readable dashboards. VibeUI, Vibe Code Components, Forge UI, and Animate UI are usually the strongest sources.
- **Floating Chief**: use command palette, dock, radial action, sheet, tooltip, and low-latency microinteraction patterns. Vibe Code Components, Animate UI, Uilora, and carefully selected Vengeance UI patterns are useful.
- **Chief website and launch surfaces**: use MotionSites, Trickle, Vengeance UI, and Uilora for one memorable first impression, but keep hero motion restrained and tied to the product story.
- **Chief onboarding**: use VibeUI and Vibe Code Components for multi-step wizards, use-case cards, plan comparison, setup checklists, and helper sheets.
- **Admin/PROJECT operator views**: stay utilitarian. Use dense proof/status/timeline/table patterns, not marketing cards or decorative motion.

## Guardrails

- Do not use more than 2-4 outside references per screen. Mixing many libraries produces incoherent UI.
- Do not install new packages until the repo stack and dependency policy are checked.
- Prefer the shadcn/open-code model when the repo already uses React/Tailwind: copy local component code and adapt it to the existing design system.
- Prefer the expanded source index when choosing between code registries, real-product UX galleries, dashboard starters, motion sources, and mature design systems.
- Prefer original bundled templates from this skill when the outside library dependency graph, safety, or quality is unclear.
- the user has approved GitHub code use, so do not block useful GitHub code because of license anxiety when the user has explicitly approved the source. Still record provenance and run the code safety/product-fit pass before copying.
- Use the canonical GitHub code safety checklist before copying public code,
  including scripts, postinstall hooks, dependency graph, network calls,
  telemetry, trackers, remote assets, credentials, storage, auth/payment,
  clipboard, camera, microphone, geolocation, notifications, dangerous browser
  APIs, dynamic script injection, `eval`, shell commands, obfuscated code, and
  hidden side effects.
- Avoid unsupported metrics, fake social proof, fake logos, or claims copied from inspiration sites.
- Without a user-provided reference, still pick a concrete art direction and quality bar before coding. Do not default to generic AI-SaaS visuals.
- Preserve product hierarchy: user goal, decision state, primary action, secondary action, proof, and recovery path.
- Include reduced-motion behavior for animated surfaces and keyboard/focus states for interactive components.
- Verify mobile and desktop screenshots before calling UI polish done.
- Do not call a visible UI pass done while visual blockers remain: overlap,
  clipped text, unresolved overflow, weird box/card nesting, broken mobile
  collapse, bad layering, weak focus/contrast, or critical truncation.

## Output Contract

When this skill is used, return or implement:

- Selected references and why each one fits the target.
- Selected pattern family and local/code-backed pattern source.
- Component plan with screen hierarchy, states, responsive behavior, and motion rules.
- Code pattern selection when useful, including exact bundled template files or local repo components to adapt.
- Brand adaptation rules, especially for Chief surfaces.
- Dependency plan and safety/provenance notes.
- Accessibility and performance risks.
- Verification proof artifact paths, including browser screenshots for visible
  UI changes, or a concrete blocker that explains why proof could not be
  captured.
