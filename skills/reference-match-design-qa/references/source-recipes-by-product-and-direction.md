# Source Recipes By Product And Direction

Research date: 2026-05-18

Purpose: prevent broad source lists from becoming indecision. Pick one recipe
after choosing product type and `direction_id`.

Use only sources that fit the repo stack. For public GitHub/component code,
inspect scripts, dependencies, network calls, trackers, auth/payment behavior,
secrets, unsafe execution, browser APIs, hidden side effects, fake content, and
product fit before copying.

## Default Recipes

| Product type | Good direction_ids | Default recipe | Alternate recipe | Proof focus |
| --- | --- | --- | --- | --- |
| Marketing/public site | `editorial-saas`, `luxury-minimal`, `glass-depth-showcase` | Tailark or shadcn blocks + Typewolf/Fontshare + real product screenshot | Magic UI/React Bits/Motion Primitives + Awwwards/Godly inspiration | first viewport, mobile fold, product visual, CTA, no fake proof |
| SaaS app shell | `calm-operator`, `developer-console`, `ai-command-center` | shadcn/ui + ReUI + shadcn-admin | Primer/Atlassian + cmdk + Base UI/Ark UI | nav, empty home, permissions, mobile nav |
| Admin/CRUD | `calm-operator`, `precision-fintech` | react-admin/refine pattern + TanStack Table + shadcn forms | ReUI + React Spectrum behavior reference | list/detail/edit/delete, validation, role states |
| Data/reporting | `precision-fintech`, `calm-operator` | TanStack Table + tablecn/OpenStatus filters + Recharts/Nivo | Apache ECharts + React Spectrum table behavior | charts answer decisions, filters reset, mobile summary |
| Forms/settings/intake | `warm-human-services`, `mobile-native-clean`, `calm-operator` | React Hook Form/TanStack Form + shadcn forms + Baymard/GOV.UK guidance | React Aria forms + Base UI/Ark UI primitives | labels, validation, save/dirty/error, mobile inputs |
| Onboarding/setup | `warm-human-services`, `mobile-native-clean`, `ai-command-center` | shadcn blocks + Driver.js if tour is needed + product checklist pattern | assistant-ui guided setup + Pageflows/Mobbin flow research | progress, skip/resume, blocked step, success/retry |
| AI/agent workspace | `ai-command-center`, `developer-console`, `spatial-canvas-lab` | assistant-ui + AI Elements + local app shell + workflow anatomy contract | CopilotKit + LangChain Agent Chat UI + LiveKit Components for voice | streaming, tool calls, approvals, receipts, failures, artifacts, stop/cancel, non-chat inspection |
| Voice/realtime AI | `ai-command-center`, `mobile-native-clean` | ElevenLabs UI + LiveKit Components + assistant-ui transcript patterns | React Aria controls + product-specific status cards | mic/camera permissions, speaking/listening/error, privacy |
| Ecommerce/checkout | `precision-fintech`, `luxury-minimal`, `mobile-native-clean` | Vercel Commerce/Saleor/Medusa pattern + Stripe React + Baymard + trust checklist | shadcn ecommerce blocks + React Hook Form | cart, variants, payment errors, trust, total clarity, review step, receipt |
| Calendar/booking | `mobile-native-clean`, `calm-operator`, `warm-human-services` | Schedule-X/FullCalendar + React DayPicker + Cal.com flow references + booking anatomy contract | shadcn date components + Pageflows booking research | time zones, availability, conflicts, confirmations, reschedule/cancel |
| Docs/editor/CMS | `developer-console`, `editorial-saas`, `spatial-canvas-lab` | Tiptap/Lexical/Plate + Fumadocs/Nextra | Novel for AI editor interactions + Storybook docs | editor chrome, publish states, empty doc, long content |
| Doc-canvas hybrid | `spatial-canvas-lab`, `ai-command-center` | BlockSuite + tldraw/xyflow references | Lexical/Plate + canvas inspector pattern | selection, collaboration, zoom/pan, command palette |
| Workflow/canvas/board | `spatial-canvas-lab`, `calm-operator` | xyflow + dnd-kit + Pragmatic Drag and Drop | tldraw/Excalidraw + React Aria drag/drop references | handles, selection, keyboard, drop indicators, minimap |
| CRM/Kanban/pipeline | `calm-operator`, `brutalist-utility` | dnd-kit + ReUI Kanban + Twenty/atomic-crm references + CRM workflow contract | Pragmatic Drag and Drop + shadcn-admin | drag/drop, empty columns, owner/filter states, next action, audit/history, bulk action conflict |
| File/media/upload | `calm-operator`, `mobile-native-clean` | Uppy/FilePond + UploadThing docs + shadcn upload blocks | React Aria file inputs + ReUI upload patterns | drop, progress, retry, rejected file, privacy |
| Billing/pricing/invoices | `precision-fintech`, `editorial-saas` | Stripe React + shadcn pricing blocks + Vercel Commerce billing patterns | Tailark pricing + table/report patterns | plan comparison, invoices, payment failure, trust |
| Support/inbox/comments | `calm-operator`, `ai-command-center` | assistant-ui + shadcn/admin list-detail + comment/thread patterns | Twenty/react-admin + activity timeline pattern | assignment, SLA/status, attachments, escalation |
| Search/command palette | `developer-console`, `calm-operator` | cmdk + shadcn command + Raycast-style reference | React Aria combobox/menu behavior | keyboard, empty results, grouping, recent actions |
| Maps/logistics/spatial analytics | `spatial-canvas-lab`, `precision-fintech` | MapLibre + deck.gl + table/filter split-pane + spatial operations contract | kepler.gl for analytics-heavy maps | map/table sync, layer states, selected item, route recalculation, exception queue, mobile |
| Presentation/deck/proposal | `editorial-saas`, `luxury-minimal` | product DESIGN.md tokens + editorial slide/document layout guidance | local document templates + Typewolf/Fontshare | one idea per slide, product-consistent brand, export |
| Game/3D/immersive | `glass-depth-showcase`, `spatial-canvas-lab`, `playful-consumer` | Three.js/R3F/Drei + performance checks | PixiJS + custom game UI references | nonblank canvas, frame rate, controls, mobile |

## Recipe Rules

- Pick one default recipe and one backup recipe. Do not open five libraries for
  one screen.
- If the repo already has a component system, use outside sources for anatomy
  and behavior, then rewrite into local components.
- If the task is interaction-heavy, prioritize behavior sources over visual
  block libraries.
- If the task is brand-heavy, pair one visual gallery with typography/color
  sources and do not copy unrelated product UX.
- If the task is proof-heavy, add Browser Harness, Storybook, Chromatic, Percy, or
  Argos depending on what the repo already supports.
- For AI/agent products, include non-chat UI: tool status, approvals, receipts,
  artifacts, error recovery, and inspection surfaces.
- Use `workflow-anatomy-contracts.md` for AI workspaces, checkout/billing,
  booking, CRM/workflow, and map/spatial screens before coding.
- Use `trust-sensitive-flow-checklist.md` when the source recipe includes
  money, authentication, permissions, personal data, agent approvals,
  destructive changes, or legal commitments.
