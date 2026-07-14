# Additive GitHub Source Lanes

Research date: 2026-05-18

Purpose: capture additional code-backed repositories found after the main
source index. Use this as an addendum to `source-index-2026-05-18.md` when a
specific product type needs stronger implementation patterns.

Star counts are research-time estimates and should not be treated as permanent.
They are selection signals, not quality guarantees.

## Motion, Animation, Loading, And Microinteractions

| Source | Best use | Notes |
| --- | --- | --- |
| `imskyleen/animate-ui` | shadcn-compatible animated primitives, sheets, drawers, loaders, and app-safe transitions | Strong source for polish in React/Tailwind apps. Inspect package scripts and copy only needed code. |
| `barvian/number-flow` | animated dashboard metrics, counters, prices, and deltas | Useful for values that change; avoid decorative overuse. |
| `formkit/auto-animate` | list insertions, accordions, loading-to-loaded swaps, and quick layout motion | Very practical for small interaction polish. Check reduced-motion behavior and dense-list performance. |
| `motiondivision/motion` | default React/JS animation engine for app motion | Use for enter/exit, layout, gestures, and state transitions. |
| `pmndrs/react-spring` | physics-based transitions and advanced interaction | Use when spring behavior materially improves interaction. |
| `airbnb/lottie-web` and `LottieFiles/dotlottie-web` | branded loading screens, empty states, onboarding illustrations | Use when there is a real vector asset or brand moment. |
| `rive-app/rive-wasm` | interactive vector/state-machine animations | Useful for voice/agent states, onboarding, and playful stateful loaders. |
| `catdad/canvas-confetti` | rare success celebrations | Use only for meaningful completion moments. |
| `darkroomengineering/lenis` | smooth scrolling for storytelling/marketing pages | Do not use for dense app tools by default; verify keyboard, anchor, reduced-motion, and performance behavior. |

## App Shells, Dashboards, Tables, And Dense Tools

| Source | Best use | Notes |
| --- | --- | --- |
| `satnaing/shadcn-admin` | dashboard nav rhythm, density, layout scaffolding, settings/admin flows | Excellent app-shell source; do not copy the whole admin-template feel blindly. |
| `sadmann7/tablecn` | serious shadcn data tables, sorting, filtering, pagination, server-state patterns | Best when the repo already uses TanStack/shadcn patterns. |
| `openstatusHQ/data-table-filters` | faceted filters and query-param data views | Useful for professional SaaS table interactions. |
| `chakra-ui/park-ui` | token structure, component anatomy, Ark UI + Panda patterns | Use as design-engineering reference when token/component anatomy matters. |
| `chakra-ui/ark` / Ark UI | headless accessible primitives backed by state machines | Strong for custom-looking products that still need reliable menus, dialogs, comboboxes, tabs, and complex widget behavior. |
| `mui/base-ui` | accessible unstyled primitives and state behavior | Strong when shadcn/Radix is not enough or when behavior is more important than visuals. |
| `adobe/react-spectrum` | accessibility depth, adaptive behavior, selection, complex state modeling | Use mainly as behavior/state reference unless the target repo wants Spectrum. |
| React Aria / React Spectrum | accessibility-first component behavior, tables, overlays, pickers, collections, and adaptive interactions | Use as the state/keyboard reference when building custom UI on top of local styling. |
| Atlassian Pragmatic Drag and Drop | polished drag/drop for boards, builders, lists, and work queues | Use for workflow DnD ergonomics. Verify keyboard alternatives, mobile behavior, and non-drag fallback. |
| `argos-ci/argos` | open-source visual regression and screenshot review | Use when a repo needs PR-level screenshot review and already has browser-test infrastructure. |
| Floating UI | popovers, menus, tooltips, comboboxes, and collision-aware overlays | Use for layer/collision behavior; pair with the visual integrity layer map. |
| Conform | accessible form state, validation messages, and progressive enhancement | Useful for serious forms and checkout/intake flows when the stack fits. |
| Framework7 | mobile-native web app patterns | Use as mobile behavior reference; do not blindly adopt its full visual language. |

## AI, Agent, Chat, Voice, And Generative UI

| Source | Best use | Notes |
| --- | --- | --- |
| `CopilotKit/CopilotKit` | copilots, side panels, generative UI, approvals, and tool-driven workflows | Heavy framework assumptions; borrow patterns before adopting the stack. |
| `assistant-ui/assistant-ui` | assistant shells, threads, composer, message actions | Good default for AI chat/product surfaces. |
| `vercel/ai-elements` | shadcn-style AI-native messages, tool calls, reasoning, and generative UI | Useful when the repo already fits React/Tailwind/shadcn. |
| `elevenlabs/ui` | voice-agent and multimodal UI: waveforms, mic states, interruptions, transcripts | Adapt interaction states, not the whole brand. |
| `langchain-ai/agent-chat-ui` | tool-running, agent status, thread history, LangGraph-style execution surfaces | Do not couple UI too tightly to a single backend framework. |
| `mnfst/manifest-ui` | MCP/app UI and ChatGPT-style surfaces | Useful for agent app/component structure. |
| `steven-tey/novel` | AI-native editor/composer interactions and slash-command writing surfaces | Useful for assistant-assisted writing, proposal builders, docs, and knowledge tools. |
| `livekit/components-js` | realtime voice/video room UI, participant controls, audio states, and call surfaces | Use for voice/video products; inspect token, media permission, and connection state handling carefully. |

## Commerce, Calendar, Editor, Canvas, Upload, And Maps

| Source | Best use | Notes |
| --- | --- | --- |
| `vercel/commerce` | storefront hierarchy, product detail, cart, checkout, merch-heavy layouts | Strong Next.js assumptions; adapt only what fits. |
| `schedule-x/schedule-x` | modern calendar and scheduling UI | Good alternative when FullCalendar is too heavy or generic. |
| `gpbl/react-day-picker` | accessible date picker and calendar-day selection | Use for date picking, not full scheduling. Verify keyboard and locale/timezone behavior. |
| Cal.com Atoms | booking, availability, timezone, and scheduling UI building blocks | Useful for scheduling/booking products; treat service/API-key requirements as implementation boundaries. |
| `facebook/lexical` | serious composer/editor/doc surfaces | Framework-level editor foundation, not a quick widget. |
| `udecode/plate` | rich text plus AI and shadcn-friendly editor UI patterns | Large surface area; copy only the needed editor chrome/pattern. |
| `toeverything/blocksuite` | doc-canvas hybrid workspace patterns | Useful for knowledge bases, collaborative docs, whiteboards, and spatial document products. Heavy architecture; borrow UX patterns before adopting. |
| `xyflow/xyflow` | node editors, automation builders, agent graphs, workflow canvases | Requires deliberate QA for zoom, keyboard, selection, and performance. |
| `tldraw/tldraw` | infinite canvas, handles, selection, minimaps, whiteboard UX | the user has approved GitHub code use; still inspect product fit and avoid over-adopting. |
| `clauderic/dnd-kit` | Kanban, sortable lists, builders, drag-heavy UIs | Drag quality depends on collision, keyboard, and mobile behavior. |
| `transloadit/uppy` | serious file uploads, progress, retries, previews, multipart/import flows | Watch upload tokens, storage privacy, and backend boundaries. |
| `maplibre/maplibre-gl-js` | open map rendering for logistics, route, territory, geospatial dashboards | Tile data, geocoding, and style sources still need review. |
| `keplergl/kepler.gl` | large-scale spatial analytics and map-based exploration | Use for logistics, territories, fleet, location intelligence, and data-heavy maps. |
| `apache/echarts` | advanced charting grammar for dense analytics, dashboards, and unusual visualizations | Use when basic chart libraries cannot express the decision view; verify accessibility and performance. |
| Observable Plot | grammar-of-graphics charts and concise visual analysis | Good reference for decision-focused charts; adapt accessibility and responsive behavior. |
| `visgl/react-map-gl` | React map components for Mapbox/MapLibre-style map apps | Use for map/list sync and spatial operations when it fits the map provider. |

## Guided Tours, Uploads, And Product Education

| Source | Best use | Notes |
| --- | --- | --- |
| `kamranahmedse/driver.js` | guided tours, product walkthroughs, feature spotlights, and onboarding hints | Tours must be dismissible, resumable, mobile-safe, keyboard-safe, and never the only path to learn the product. |
| Shepherd | product tours and guided onboarding | Useful as pattern inspiration; check license/commercial fit and accessibility before adopting. |
| UploadThing | upload/dropzone flows, file state, upload routing, and developer-friendly upload UX | Service/API-key boundaries matter. Inspect credentials, network calls, storage privacy, and backend requirements before adopting. |

## Typography, Localization, And International Product Fit

| Source | Best use | Notes |
| --- | --- | --- |
| Google Fonts / Noto | broad font catalog and multilingual/script coverage | Use language filters and deliberate fallback stacks. |
| Fontsource | self-hosted open-source fonts | Good for privacy/performance/offline control. |
| FormatJS | ICU messages, dates, numbers, plurals, and React i18n | Use when copy, dates, currencies, and counts need real locale formatting. |
| next-intl | Next.js routing/messages/dates/numbers | Strong for Next.js apps that need product-grade localization. |
| MDN CSS container queries and subgrid | responsive components and nested alignment | Use when viewport-only breakpoints cannot protect cards, panels, tables, and embedded components. |

## Use Rule

Use these repositories as code-backed sources when they fit the target stack and
product job. the user has approved GitHub code use, so license should not block
use, but safety and product fit still matter:

- inspect scripts and dependency graph before running code
- inspect network calls, trackers, telemetry, auth/payment behavior, secrets,
  unsafe execution, and hidden side effects
- copy the smallest useful block or behavior
- rewrite into the repo's local imports, tokens, states, accessibility behavior,
  product copy, and proof loop
- add a generalized local pattern only when the result is broadly reusable
