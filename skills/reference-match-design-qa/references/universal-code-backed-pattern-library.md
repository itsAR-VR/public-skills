# Universal Code-Backed Design Pattern Library

Research date: 2026-05-18

Purpose: give Codex and Claude a practical design library for any product the user
asks us to build: websites, SaaS apps, internal tools, AI workspaces, CRMs,
dashboards, ecommerce, onboarding, editors, calendars, canvases, mobile-style
web apps, documents, maps, or future categories we have not named yet.

This file is not a claim that we locally own hundreds of complete finished app
designs. The accurate model is better:

- This skill owns the selector, quality rules, state checklist, and proof loop.
- `vibe-design-reference-libraries` owns original starter code patterns.
- Public code-backed sources provide hundreds of blocks/components/examples
  that can be inspected and adapted when the license, dependency fit, and
  product context are safe.

Use this file before coding when the task is broad, the user gives no reference,
or the build type is not obvious.

Pair it with:

- `no-reference-art-direction-catalog.md` for named visual directions
- `source-recipes-by-product-and-direction.md` for product-specific source
  bundles
- `state-coverage-matrix.md` for the states that must be built and proven
- `screenshot-repair-playbook.md` for post-screenshot repair order
- `github-code-safety-checklist.md` before copying public GitHub/component code
- `design-doctrine-and-qa.md` for the professional quality bar
- `additive-github-source-lanes-2026-05-18.md` for newer code-backed source
  candidates

## Non-Negotiable Universal Rules

1. Build the actual UI. A target, packet, mood board, or plan is not the
   deliverable unless the user explicitly asked for only planning.
2. Start from the product job. The right design for a CRM pipeline is different
   from a landing page, checkout, graph canvas, AI command center, or mobile
   onboarding flow.
3. Pick one primary pattern family before coding. Add secondary patterns only
   when the workflow needs them.
4. For no-reference work, pick one `direction_id` and one source recipe before
   coding.
5. Use local repo components first, then open-code primitives or block sources,
   then inspiration-only sources.
6. Include real states: empty, loading, error, disabled, hover, focus, selected,
   success, destructive, and mobile behavior when relevant.
7. Motion must explain state, improve orientation, or create one memorable
   brand moment. Do not add motion because the screen feels boring.
8. Public code can be pulled when safe, but it must become local product code:
   local imports, tokens, copy, states, accessibility behavior, and proof.
9. the user has approved GitHub code use, so license anxiety should not block a
   useful GitHub source when the user has explicitly approved it. Safety, provenance,
   dependency fit, and product fit still matter.
10. Meaningful UI work is not done until desktop and mobile screenshots exist,
   or the exact blocker is named.

## Any-Build Selector

| If the user asks for | Primary pattern family | First code-backed sources | Proof focus |
| --- | --- | --- | --- |
| "make a site", launch page, service page, waitlist, portfolio | Marketing/public site | shadcn/ui blocks, Tailark, Shadcnblocks, Magic UI, React Bits, MotionSites | First viewport, product visual, CTA, mobile fold |
| SaaS app, dashboard, workspace, product home | App shell and command center | shadcn/ui, Radix, ReUI, shadcn-admin, Kiranism dashboard starter | Navigation, density, empty/loading/error, mobile nav |
| Admin, CRUD, back office, operations | Admin and resource management | react-admin, refine, ReUI, shadcn-admin, TanStack Table | Tables, filters, forms, bulk actions, audit trail |
| Reports, metrics, analytics, BI | Analytics and charting | Recharts, Nivo, Visx, Tremor, TanStack Table | Data hierarchy, legends, time ranges, no fake metrics |
| Form, settings, profile, account, intake | Forms and settings | React Hook Form, TanStack Form, shadcn/ui, Base UI, Headless UI | Validation, help text, save states, destructive states |
| Onboarding, setup, activation, checklist | Onboarding and guided flow | shadcn/ui blocks, VibeUI, ReUI, product starter patterns | Progress, skip/resume, success, failure recovery |
| AI assistant, agent, chat, voice, tool calls | AI/agent workspace | assistant-ui, AI Elements, ElevenLabs UI, Manifest UI, Vercel AI SDK examples | Streaming, tool-running, approvals, receipts, failures |
| Ecommerce, marketplace, checkout, subscriptions | Commerce and conversion | Medusa, Saleor, Vercel Commerce, Hydrogen, Stripe React | Cart, variants, checkout, trust, payment states |
| Calendar, scheduling, booking, events | Scheduling and calendar | FullCalendar, Schedule-X, Cal.com, shadcn calendar blocks | Time zones, availability, drag/drop, conflict states |
| Docs, blog, CMS, editor, knowledge base | Content and editor | Tiptap, Lexical, Plate, Storybook docs, shadcn docs blocks | Reading comfort, editor states, publish states |
| Whiteboard, graph, builder, workflow designer | Canvas and node editor | tldraw, Excalidraw, React Flow/xyflow, dnd-kit | Pan/zoom, selection, handles, keyboard, empty canvas |
| Kanban, pipeline, task board, CRM | Board and pipeline | dnd-kit, ReUI Kanban, Twenty, atomic-crm, shadcn-admin | Drag/drop, status, owner, filters, empty columns |
| Files, media, gallery, upload, asset manager | File and media management | Uppy, FilePond, ReUI file upload, shadcn upload blocks | Drop state, upload progress, error/retry, previews |
| Billing, pricing, plans, usage, invoices | Billing and subscription | Stripe React, Vercel Commerce, shadcn pricing blocks, Tailark | Plan comparison, payment errors, invoices, trust |
| Support portal, help desk, inbox, comments | Support and collaboration | Twenty, react-admin, shadcn/ui, assistant-ui, comment patterns | Threading, assignment, SLA/status, attachments |
| Search, command palette, launcher, global actions | Command and search | cmdk, shadcn command, local CommandPalette starter, Raycast-style references | Keyboard, empty results, grouped actions |
| Notifications, activity feed, timeline, audit log | Timeline and activity | ReUI timeline, shadcn timeline blocks, Primer/Polaris patterns | Read/unread, filters, timestamps, action receipts |
| Auth, signup, login, invite, access control | Auth and access | shadcn auth blocks, Supabase UI, Clerk examples, Base UI | Error states, MFA, invite, terms, password reset |
| Developer portal, API docs, SDK page | Developer docs | Nextra, Fumadocs, Mintlify-style references, Storybook docs | Search, code samples, nav, versioning |
| Map, route, dispatch, logistics, field ops | Map and location | Mapbox/MapLibre examples, deck.gl, table/filter sources | Map/table split, selected item, route state, mobile |
| Presentation, report, proposal, PDF-like page | Document and presentation | local docs/PDF templates, design systems, editor patterns | Reading order, export, page breaks, print states |
| Game, simulation, immersive 3D, interactive art | Game/canvas/3D | Three.js, PixiJS, React Three Fiber, game-specific libraries | Nonblank canvas, frame rate, controls, mobile |

## Pattern Families

Use this section to decide what to build. Each family includes code-backed
sources, required states, and what to avoid.

### 1. Marketing And Public Sites

Use for homepages, launch pages, service pages, portfolios, waitlists, campaign
pages, event pages, and product storytelling.

Code-backed sources:

- shadcn/ui blocks, Tailark, Shadcnblocks, Shadcnspace, Magic UI, React Bits,
  Motion Primitives, 21st.dev, ReUI marketing blocks.

States and sections to include:

- first-viewport product signal, CTA, product visual, proof, feature detail,
  pricing/offer if relevant, FAQ, footer, mobile fold, reduced motion.

Avoid:

- generic centered hero with gradient blobs, fake logos, fake testimonials,
  unsupported metrics, five effects from five libraries, or a split hero where
  the product is not visible.

### 2. App Shell And Command Center

Use for SaaS products, AI products, internal workspaces, operational dashboards,
and tools people return to every day.

Code-backed sources:

- local ProductAppShell starter, shadcn/ui, Radix, ReUI, shadcn-admin,
  Kiranism dashboard starter, Headless UI, Base UI.

States to include:

- desktop sidebar/topbar, mobile nav/sheet, user/account menu, loading shell,
  empty home, permission-limited view, notifications, command/search access.

Avoid:

- landing-page hero composition inside the app, oversized headings in dense
  tools, decorative cards, hidden navigation on mobile, and no empty states.

### 3. Admin, CRUD, And Resource Management

Use for back-office tools, user management, inventory, tickets, resource lists,
approval queues, and workflows with create/read/update/delete.

Code-backed sources:

- react-admin, refine, ReUI, shadcn-admin, TanStack Table, TanStack Query,
  shadcn/ui forms, Radix/Base UI primitives.

States to include:

- list, detail, create, edit, delete confirmation, bulk actions, saved/dirty
  state, validation, optimistic updates, audit trail, role/permission states.

Avoid:

- one-off pages that do not share list/detail/form patterns, destructive
  actions without recovery, and tables without filtering/sorting when data can
  grow.

### 4. Data Tables, Filters, And Reports

Use for operational tables, dashboards, logs, analytics, reporting, and CRMs.

Code-backed sources:

- TanStack Table, tablecn, Open Status data-table-filters, ReUI data grid,
  Recharts, Nivo, Visx, Tremor-style references.

States to include:

- loading skeleton, empty filtered result, no data yet, error, pagination,
  sorting, search, saved views, column visibility, row actions, mobile summary.

Avoid:

- chart decoration with no decision value, fake metrics, table overflow that
  breaks mobile, and filters with no clear reset path.

### 5. Forms, Settings, And Intake

Use for profile, settings, checkout forms, lead forms, onboarding questions,
survey flows, account configuration, and admin edit pages.

Code-backed sources:

- React Hook Form, TanStack Form, shadcn/ui forms, Base UI, Headless UI,
  ReUI form blocks, Formbricks for survey/product feedback patterns.

States to include:

- inline validation, hint text, dirty state, save pending, save success, server
  error, disabled/read-only, destructive confirmation, keyboard/focus.

Avoid:

- placeholder-only labels, validation only after submit, too many fields on one
  page, and modal-heavy settings.

### 6. Onboarding, Setup, And Activation

Use for first-run setup, product activation, install flows, account setup,
import/connect flows, and guided checklists.

Code-backed sources:

- local OnboardingWizard starter, shadcn blocks, VibeUI, ReUI, Vibe Code
  Components, assistant-ui when setup is AI-guided.

States to include:

- progress, skip/resume, prerequisites, blocked step, optional step, success,
  invite/member steps, connected/disconnected integration state.

Avoid:

- overlong wizards, no resume state, asking for everything before showing value,
  and progress bars that do not map to real work.

### 7. AI, Agent, Chat, Voice, And Tool Workspaces

Use for assistants, agent control rooms, command surfaces, voice agents,
generative UI, tool-call review, and AI workflows.

Code-backed sources:

- assistant-ui, AI Elements, ElevenLabs UI, Manifest UI, Vercel AI SDK
  examples, Supabase UI, local CommandPalette/ProductAppShell starters.

States to include:

- empty prompt, composing, sending, streaming, reasoning, tool-running,
  approval-needed, tool failed, retry, cancelled, completed, citation/proof,
  voice listening/speaking/idle/error, file/multimodal attachments.

Avoid:

- plain chat box as the whole product, hidden tool state, no approval boundary,
  no receipt/proof after actions, and giant walls of assistant text in app
  workflows.

### 8. Ecommerce, Marketplace, And Checkout

Use for stores, marketplaces, product pages, carts, checkout, subscriptions,
account billing, and payment flows.

Code-backed sources:

- Medusa, Saleor, Vercel Commerce, Shopify Hydrogen, Stripe React Stripe.js,
  shadcn commerce/pricing blocks.

States to include:

- product variants, inventory, cart, coupon, address, shipping, tax, payment,
  failed payment, success receipt, order status, empty cart, account orders.

Avoid:

- unclear total price, hidden fees, weak trust signals, inaccessible payment
  errors, and copied fake product reviews.

### 9. Scheduling, Booking, And Calendar

Use for appointment booking, availability, events, team schedules, reminders,
and calendar-driven workflows.

Code-backed sources:

- FullCalendar, Schedule-X, Cal.com patterns, shadcn calendar/date picker,
  Radix popovers/dialogs.

States to include:

- empty calendar, loading availability, unavailable slot, conflict, timezone,
  reschedule, cancel, recurring event, drag/drop, mobile agenda view.

Avoid:

- time without timezone clarity, tiny tap targets, dragging as the only path,
  and calendar grids without list/agenda fallback.

### 10. Content, Docs, CMS, And Editors

Use for blogs, docs, knowledge bases, CMS, rich text, notes, proposals, and
writing/editing tools.

Code-backed sources:

- Tiptap, Lexical, Plate, Nextra/Fumadocs-style docs, Storybook docs patterns,
  shadcn editor blocks.

States to include:

- read mode, edit mode, saving, saved, unsaved, publish, version history,
  comments, empty document, import/export, mobile read/edit behavior.

Avoid:

- content walls with no hierarchy, editor controls that wrap badly, no autosave
  signal, and docs navigation that collapses into unusable mobile menus.

### 11. Canvas, Whiteboard, Graph, And Workflow Builder

Use for visual builders, node graphs, agent graphs, flow charts, whiteboards,
diagramming, automation builders, and spatial workspaces.

Code-backed sources:

- tldraw, Excalidraw, React Flow/xyflow, dnd-kit, react-grid-layout, Three.js
  only when spatial/3D is truly needed.

States to include:

- blank canvas, selected item, multi-select, pan/zoom, node handles, invalid
  connection, drag/drop, keyboard shortcuts, minimap, save/sync, undo/redo.

Avoid:

- decorative graph with no interaction model, unreachable controls, no keyboard
  path, no empty canvas coaching, and performance-heavy effects before proof.

### 12. Boards, Pipelines, And CRM

Use for Kanban, sales pipelines, task boards, project tracking, support queues,
and owner/status based workflows.

Code-backed sources:

- dnd-kit, ReUI Kanban, Twenty, marmelab atomic-crm, shadcn-admin, TanStack
  Table for board/list parity.

States to include:

- empty column, drag/drop, owner, due date, status reason, blocked state,
  filters, search, list view fallback, activity timeline.

Avoid:

- board-only products with no list view for dense work, drag/drop without
  keyboard alternative, and status labels with no next action.

### 13. File, Media, Upload, And Asset Management

Use for document upload, media libraries, galleries, attachments, imports,
exports, and design asset managers.

Code-backed sources:

- ReUI file upload, Uppy, FilePond, shadcn upload/dropzone blocks, local
  FieldState/EmptyState/SkeletonBlock starters.

States to include:

- drag over, selected files, upload progress, retry, failed file, success,
  preview, remove, file type/size error, empty library, permissions.

Avoid:

- upload with no progress, silent failures, no file restrictions, and tiny
  delete/retry controls.

### 14. Billing, Pricing, Subscription, And Usage

Use for pricing pages, plan selection, billing settings, invoices, trials,
usage dashboards, and subscription upgrades.

Code-backed sources:

- Stripe React, Vercel Commerce, shadcn pricing blocks, Tailark, ReUI cards,
  table/reporting patterns for usage.

States to include:

- current plan, plan comparison, upgrade/downgrade, trial ending, failed
  payment, invoice list, usage limits, proration note, cancellation path.

Avoid:

- confusing price math, hidden limitations, fake urgency, no downgrade path,
  and billing states that require support for normal actions.

### 15. Support, Inbox, Comments, And Collaboration

Use for help desks, customer portals, shared docs, comments, review threads,
notifications, and team workflows.

Code-backed sources:

- shadcn/ui, assistant-ui for AI-assisted support, Twenty/CRM patterns,
  react-admin/refine for admin queues, Primer/Polaris for comments/activity.

States to include:

- unread/read, assigned/unassigned, reply composer, internal note, attachment,
  status, SLA/priority, empty inbox, failed send, optimistic send.

Avoid:

- chat without thread state, no assignment/ownership, no recovery for failed
  sends, and comment UIs with unclear privacy.

### 16. Mobile-Style Web Apps

Use when the target is web but the user experience behaves like a mobile app:
short sessions, bottom actions, touch-first controls, sheets, camera/media,
voice, or location.

Code-backed sources:

- shadcn sheets/drawers, Radix, Headless UI, mobile app references from Mobbin,
  UIguana, Pageflows, and local SlideSheet/CommandPalette starters.

States to include:

- safe area, bottom action, sheet state, keyboard open, compact navigation,
  touch targets, offline/error, mobile-first loading.

Avoid:

- desktop sidebars squeezed into mobile, hover-only actions, tiny controls, and
  hiding core actions behind ambiguous menus.

### 17. Maps, Routes, Dispatch, And Location

Use for logistics, field ops, delivery, territory planning, local discovery,
events, and location-based dashboards.

Code-backed sources:

- Mapbox/MapLibre examples, deck.gl, data table/filter sources, app shell
  patterns, Bottom sheet/mobile map references from real apps.

States to include:

- map/list split, selected location, route, loading tiles, empty search,
  permission denied, offline, cluster, filters, mobile bottom sheet.

Avoid:

- map-only UIs with no accessible list, unreadable markers, and no fallback
  when geolocation fails.

### 18. Games, Simulations, 3D, And Immersive Tools

Use for games, simulations, 3D product views, spatial demos, creative tools,
and interactive visuals.

Code-backed sources:

- Three.js, React Three Fiber/drei, PixiJS, canvas libraries, existing game
  engines when rules/physics matter.

States to include:

- loading, asset failure, controls/help, pause/resume, restart, settings,
  reduced motion where possible, mobile input, nonblank canvas proof.

Avoid:

- decorative 3D that does not support the product, no screenshot/canvas-pixel
  proof, and hand-rolled engines for established game/physics rules.

## Local Starter Pattern Coverage

The bundled starter code in `vibe-design-reference-libraries` gives us owned
starting points for common screens. Use these before pulling outside code when
the target stack is React/Tailwind-compatible:

- ProductAppShell: app shell, dashboards, command centers, workspaces.
- LandingHero: public sites, launch pages, service pages.
- OnboardingWizard: setup, activation, guided flows.
- CommandPalette: global search, action launcher, AI command entry.
- SlideSheet: settings, details, mobile panels, contextual actions.
- PremiumCard: repeated content blocks where a card is actually appropriate.
- FieldState: forms, settings, validation, profile fields.
- SkeletonBlock: stable loading states.
- EmptyState: zero-data and filtered-empty recovery.
- DataTableFrame: tables, reports, admin lists, CRM list view.
- AgentWorkspace: AI assistant, tool calls, proof/receipt panels.
- CheckoutSummary: ecommerce, billing, plan checkout.
- CalendarPlanner: schedule, booking, agenda, availability.
- EditorWorkspace: docs, notes, CMS, proposal editor.
- WorkflowCanvas: graph, node builder, blank canvas, flow editor.
- KanbanPipeline: CRM, task boards, status workflows.
- FileDropzone: upload, media, imports, attachments.
- BillingPlanGrid: pricing, subscriptions, upgrades.
- ActivityTimeline: audit log, notifications, receipts, support history.

## Large Pattern Catalog

Pick from this catalog before coding. The goal is not to use every pattern. The
goal is to avoid defaulting to the same card grid for every problem.

### Public Site Patterns

- Product-first hero
- Visual proof hero
- Waitlist hero
- Launch announcement
- Feature narrative
- Problem/solution split
- Social proof strip
- Pricing section
- FAQ section
- Product demo section
- Case study teaser
- Comparison table
- Footer sitemap
- Sticky CTA bar
- Event landing page
- Portfolio gallery
- Founder story page
- Service package page
- Lead capture form
- Interactive product tour

### App Shell Patterns

- Sidebar shell
- Topbar shell
- Split-pane workspace
- Inbox/work queue
- Command center home
- Detail drawer
- Settings layout
- Notification center
- Global command palette
- User/account menu
- Team switcher
- Breadcrumb header
- Mobile tab bar
- Mobile sheet navigation
- Permission-limited page
- Integration status panel

### Data And Operations Patterns

- Data table with saved views
- Faceted filter bar
- Row action menu
- Bulk action toolbar
- Detail side panel
- Audit timeline
- Status badge system
- Empty filtered result
- Infinite list
- Paginated resource list
- KPI summary strip
- Report builder
- Chart and table pair
- Drill-down analytics
- Export center
- Import review queue
- Error recovery panel
- Approval queue
- Assignment queue
- SLA/priority queue

### Forms And Settings Patterns

- Single-column form
- Two-column settings page
- Progressive disclosure form
- Multi-step wizard
- Inline validation
- Server error summary
- Unsaved changes banner
- Dangerous action zone
- API key manager
- Invite members flow
- Role/permission matrix
- Preferences panel
- Billing form
- Connected account card
- Profile completion checklist
- Survey/intake sequence

### AI And Agent Patterns

- Chat thread
- Streaming message
- Tool-call card
- Approval request card
- Reasoning/progress timeline
- Voice input bar
- Voice waveform state
- Multimodal attachment tray
- Agent run receipt
- Plan/edit/execute workspace
- Human-in-the-loop review
- Memory/reference panel
- Citation/proof drawer
- Error/retry tool state
- Command composer
- Agent activity feed
- Split chat plus work surface
- Floating assistant launcher

### Commerce And Billing Patterns

- Product listing grid
- Product detail page
- Variant selector
- Cart drawer
- Checkout steps
- Payment form
- Address form
- Shipping method selector
- Coupon/discount field
- Order success receipt
- Order history
- Subscription plan cards
- Usage meter
- Invoice table
- Failed payment recovery
- Upgrade/downgrade confirmation

### Content And Editor Patterns

- Docs shell
- Searchable knowledge base
- Article layout
- Rich text editor
- Slash command menu
- Comment thread
- Version history
- Publish checklist
- Draft/saved status
- Table of contents
- Code block examples
- Media embed block
- CMS collection list
- Editor preview split
- PDF/report view

### Canvas And Workflow Patterns

- Blank canvas coaching
- Node graph
- Flow builder
- Edge connection state
- Minimap
- Toolbar
- Inspector panel
- Layer list
- Drag/drop reorder
- Resizable panels
- Kanban board
- Timeline board
- Whiteboard
- Drawing tool palette
- Undo/redo controls
- Zoom controls
- Selection handles
- Invalid connection warning

### Calendar, Support, And Utility Patterns

- Month/week/day calendar
- Agenda list
- Availability picker
- Booking confirmation
- Timezone banner
- Reschedule flow
- Support inbox
- Reply composer
- Internal note
- Attachment uploader
- Notification feed
- Activity timeline
- Map/list split
- Route planner
- File library
- Image gallery
- Upload progress list
- Loading skeleton
- Error page
- Success celebration

## Source Trust Ladder

Use this ladder when deciding whether to copy, adapt, or only reference an
outside source.

1. Target repo components and tokens: safest, use first.
2. Local bundled starter patterns: owned by us, safe to adapt.
3. Public GitHub/component code with user-approved use: usable after provenance,
   dependency, security, and product-fit review.
4. Premium sites or unclear provenance: inspiration only unless the user confirms
   access and scope.
5. Real product galleries: pattern extraction only, no brand/code copying.

## What To Save In The Packet

Every reference or no-reference packet should now include:

- pattern family
- selected pattern(s) from the catalog
- selected `direction_id` for no-reference work
- selected source recipe for broad/product-type work
- code-backed source candidates
- inspiration-only source candidates
- required states
- mobile behavior
- motion class
- proof required
- provenance, dependency, and safety risk
- what the implementation must not copy blindly

## Plain-English Scenario

If the user says, "Build me a booking tool for a consultant," the skill should not
produce a generic SaaS dashboard.

It should select:

- Scheduling and calendar as the primary family
- Forms/settings as the secondary family
- FullCalendar, Schedule-X, Cal.com, and shadcn date picker as code-backed
  sources
- Booking states like unavailable slot, timezone, reschedule, cancel, loading
  availability, and confirmation receipt
- Desktop and mobile proof, including mobile agenda behavior

Outcome: the first build is much closer to a real product because it starts
from the right interface pattern and state checklist, not from a generic
"premium app" look.
