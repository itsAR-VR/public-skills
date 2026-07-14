# Code Pattern Guide

This reference turns the design-tool research into reusable implementation patterns. Use it when the user asks for actual UI code, a reusable design kit, or faster production-quality UI starts.

The bundled code is original starter code, not copied from third-party libraries. It is meant to be adapted into the target repo's design system.

For build-type selection across any future product, pair this guide with
`../../reference-match-design-qa/references/universal-code-backed-pattern-library.md`.
That file decides the pattern family; this file decides what local starter code
or outside code source to adapt.

## Bundled Assets

| File | Use When | Dependencies |
| --- | --- | --- |
| `assets/react-tailwind-shadcn/patterns.tsx` | The repo uses React/Next/Vite plus Tailwind or shadcn-style classes and needs reusable layout/component starts. | React, Tailwind CSS. No shadcn package required. |
| `assets/react-tailwind-shadcn/motion-patterns.tsx` | The repo already has Motion, or the user approves adding Motion for reveal/presence/press/stagger animation. | React, Tailwind CSS, `motion`. |
| `assets/react-tailwind-shadcn/styles.css` | The repo needs portable CSS helpers for focus rings, surfaces, grid backgrounds, shimmer, and reduced-motion behavior. | Plain CSS. |

## How To Use

1. Inspect the target repo first: `package.json`, Tailwind config, `components.json`, `components/ui`, `lib/utils`, and any existing design-system components.
2. Copy only the patterns needed for the current screen. Do not install a full outside library just because a gallery uses it.
3. Replace the bundled `cn` helper with the repo's local helper if it exists, usually `@/lib/utils`.
4. Replace plain HTML buttons/cards/inputs with local shadcn/ui components only when the repo already uses them.
5. Keep the code original and product-specific: real labels, real states, real empty/error/loading paths, no fake metrics or borrowed claims.
6. Verify with desktop and mobile screenshots for visible UI work.
7. When using `truncate`, fixed heights, `overflow-hidden`, virtualized rows, or
   dense cards/tables, add a long-content proof case. Critical labels, prices,
   statuses, errors, names, and commitments must have a reveal path.

## External Code Pull Ladder

When bundled assets are not enough, use this order:

1. Target repo local components and tokens.
2. Universal pattern family from
   `../../reference-match-design-qa/references/universal-code-backed-pattern-library.md`.
3. Existing shadcn/ui primitives already installed in the target repo.
4. Reputable open-code shadcn registries and repos from
   `../../reference-match-design-qa/references/source-index-2026-05-18.md`, such
   as ReUI, Tailark, shadcn-ui-blocks, shadcnspace, Magic UI, React Bits,
   Motion Primitives, tablecn, data-table-filters, and shadcn-admin.
5. AI/agent interface sources such as assistant-ui, AI Elements, ElevenLabs UI,
   Manifest UI, 21st.dev Agent Elements, and Supabase UI for chat shells,
   streaming messages, tool-call cards, voice/audio states, approval states,
   and generative UI.
6. Animation sources by need:
   - Motion, Motion Primitives, Animate UI, and React Spring for app-safe state
     transitions.
   - Lottie/dotLottie and Rive for branded loaders, empty states, onboarding
     illustrations, and agent/voice states.
   - GSAP/anime.js, React Bits, Magic UI, Vengeance UI, Three.js, PixiJS, and
     Lenis for public-site or high-end interactive motion after performance and
     reduced-motion checks.
   - canvas-confetti, tsParticles, and Number Flow for small success, particle,
     and counter effects.
7. Real-product UX galleries like Mobbin, Nicelydone, and SaaSFrame for pattern
   extraction only.
8. Premium or restricted-distribution libraries can be used when the user has
   approved access, but copy only what is needed and keep safety/product-fit
   checks in place.

Copying code is allowed when safe, but the copied code must become native to the
target product: local imports, local tokens, local states, local copy, local
accessibility behavior, and local proof.

## Visual Integrity Floor

Before a copied or bundled pattern can be called done, check it against
`../../reference-match-design-qa/references/visual-integrity-gate.md`.

Do not ship a pattern with:

- overlap or occlusion
- clipped text
- unresolved text overflow
- weird nested cards or decorative boxes
- broken mobile collapse
- z-index/layer conflicts
- weak focus or contrast
- critical truncation without reveal

If a pattern intentionally scrolls, truncates, pins, or clips, the behavior must
be named in the packet and proven with a screenshot or story.

## GitHub Code Safety Pass

the user has approved GitHub code use for this design skill, so do not block useful
GitHub code because of license anxiety when the user has explicitly approved the
source. Use reputable, starred GitHub repos as strong candidates, not as
automatic safe sources. Before copying code into a product or into this skill's
local pattern library, check:

- Source/provenance: know which repo/block the code came from so it can be
  traced and updated later.
- Package/install scripts: inspect `package.json` scripts, postinstall hooks,
  CLIs, and required setup commands before running anything.
- Network behavior: look for fetch/XHR/websocket calls, analytics, trackers,
  remote assets, remote scripts, and telemetry.
- Sensitive behavior: auth, payment, credential, cookie, token, localStorage,
  file-system, clipboard, camera, microphone, and geolocation access.
- Dangerous execution: `eval`, `new Function`, dynamic script injection,
  obfuscated/minified source, shell commands, and unsafe dependency bloat.
- Product fit: strip fake content, logos, metrics, claims, and brand styling.

If the source is reputable and passes these checks, copy the smallest useful
block, rewrite it into local imports/tokens/states/accessibility behavior, and
then consider turning the generalized version into a reusable local pattern so
future builds learn from it.

## shadcn-style Rules

Use shadcn's open-code model as the mental model: components live in the app, can be edited, and should compose predictably. If the target repo already uses shadcn/ui, add only the components needed:

```bash
npx shadcn@latest add button card input label dialog sheet command skeleton
```

Do not run `add --all` unless the user explicitly wants a broad design-system setup. For external registries, treat code as third-party code and review license, dependency fit, and accessibility before copying.

## Motion Rules

Use Motion for motion that explains structure: entrance, exit, press feedback, sheet presence, list staggering, and layout continuity. Avoid decorative motion on dense workflows.

- Animate transform and opacity first.
- Use variants for repeated states.
- Use `AnimatePresence` only around conditionally rendered elements with stable keys.
- Respect reduced motion with `useReducedMotion()` or CSS `prefers-reduced-motion`.
- Keep default durations around 150-300ms.

## Pattern Inventory

Use `patterns.tsx` for:

- **ProductAppShell**: dashboard/app shell with rail navigation and header actions.
- **LandingHero**: product-first hero with actions and a visual slot.
- **OnboardingWizard**: multi-step setup flow with progress and action slots.
- **CommandPalette**: lightweight command menu/search pattern.
- **SlideSheet**: accessible drawer/sheet baseline.
- **PremiumCard**: reusable card frame with title, description, action, and footer slots.
- **FieldState**: label, hint, error, and input wrapper.
- **SkeletonBlock**: loading placeholder with stable dimensions.
- **EmptyState**: no-data/recovery pattern.
- **DataTableFrame**: table/report/admin/CRM list frame with stable toolbar
  and state slots.
- **AgentWorkspace**: AI/agent work surface with thread, composer, and
  tool/proof side panel slots.
- **CheckoutSummary**: commerce, billing, cart, and plan checkout summary.
- **CalendarPlanner**: calendar/scheduling layout with agenda and detail slots.
- **EditorWorkspace**: docs, CMS, notes, and editor workspace shell.
- **WorkflowCanvas**: canvas/graph/builder workspace with toolbar and inspector
  slots.
- **KanbanPipeline**: board, CRM, and task pipeline layout.
- **FileDropzone**: upload/import/media drop area with progress/state slots.
- **BillingPlanGrid**: pricing/subscription plan cards.
- **ActivityTimeline**: audit log, notification feed, receipt, or support
  history.

Use `motion-patterns.tsx` for:

- **MotionReveal**: entry animation with reduced-motion fallback.
- **MotionPress**: press/hover feedback wrapper.
- **MotionPresencePanel**: enter/exit panel animation.
- **MotionStagger**: staggered child reveal for short lists.

## Future Build Prompt

```text
Use the vibe-design-reference-libraries skill and its code-pattern layer.

Target: [screen/flow/component]
Stack: [React/Next/Vite + Tailwind/shadcn/Motion status]
Product: [what we are building, not only Chief]
Pattern family: [use universal-code-backed-pattern-library.md]
References: pick max 3 relevant sources from the research summary.
Code: adapt only the needed patterns from assets/react-tailwind-shadcn/.
Constraints: preserve local design tokens, avoid fake content, inspect GitHub code for safety/provenance before copying, include reduced-motion and keyboard/focus states.
Proof: run relevant build/lint/tests and capture desktop/mobile screenshots for visible UI.
```
