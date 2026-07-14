# State Coverage Matrix

Research date: 2026-05-18

Purpose: make state design workflow-prioritized instead of a generic checklist.
Every serious UI packet should name the top critical states before coding.

## Rules

- Pick the product family first.
- Fill `critical_states_first`, `edge_states_required`, and
  `state_proof_required` in the packet or DESIGN.md.
- Do not design every possible state with equal detail. Design the states that
  decide trust, conversion, safety, or workflow success first.

## Matrix

| Product family | Primary states | Secondary states | Edge states | Proof expected |
| --- | --- | --- | --- | --- |
| Marketing/public site | first load, CTA ready, mobile fold | nav open, form submit, success | failed lead capture, reduced motion, missing media | desktop/mobile screenshots, form state notes |
| SaaS app shell | loading shell, empty home, permission-limited | nav active, command/search open, notifications | expired session, no organization, long names | desktop/mobile app shell screenshots |
| Admin/CRUD | list loaded, create/edit dirty, delete confirm | bulk selected, filter active, save success | server error, role denied, optimistic rollback | list/detail/form screenshots or stories |
| Data/reporting | data loaded, filtered empty, chart loading | no data yet, range changed, saved view | API error, huge dataset, mobile overflow | screenshot with filters and mobile summary |
| Forms/settings/intake | field focus, invalid input, save pending | save success, disabled/read-only, help text | network error, destructive reset, long copy | keyboard/focus check plus mobile |
| Onboarding/setup | first step, blocked step, progress | optional skipped, resume later, success | failed integration, invite pending, lost permission | step screenshots and recovery note |
| AI/agent workspace | empty prompt, streaming, tool-running | approval needed, artifact ready, receipt/audit, completed | tool failed, cancelled, unsafe action blocked, permission denied | state screenshots or Storybook stories |
| Voice/realtime UI | idle, listening, speaking | reconnecting, muted, transcript ready | permission denied, noisy input, call dropped | browser check and privacy/permission note |
| Ecommerce/checkout | product/variant ready, cart, payment form, review before submit | shipping/tax updated, promo/error, order success, receipt | payment failure, card declined, inventory gone, address invalid, tax/total mismatch | checkout mobile and error screenshots |
| Calendar/booking | availability loaded, slot selected, confirmation | conflict, timezone visible, reschedule, cancel | no availability, slot unavailable, double-booking, cancellation failed | desktop/mobile slot and conflict proof |
| Editor/docs/CMS | empty doc, editing, publish ready | autosaved, formatting toolbar, preview | save conflict, offline, permission denied | editor and long-content screenshots |
| Canvas/workflow/board | empty canvas, selected node/card, dragging | inspector open, connection/drop target, zoom | invalid drop, lost connection, mobile fallback | desktop canvas plus keyboard/selection notes |
| CRM/Kanban/pipeline | default list/board, selected record, next action | owner/filter state, detail panel, bulk selected, history/audit | empty column, role denied, bulk conflict, stale record, drag rollback | list/detail/board screenshots and audit proof |
| File/upload/media | empty dropzone, uploading, complete | preview, retry, remove file | rejected type/size, auth expired, privacy warning | upload progress/error proof |
| Billing/pricing/invoices | plan compare, payment method, invoice list | upgrade/downgrade pending, usage warning | failed payment, cancellation, tax/total mismatch | payment error and trust/total clarity proof |
| Support/inbox/comments | unread/open thread, assigned, reply compose | attachment, internal note, SLA status | escalation, failed send, closed/reopen | inbox/thread screenshots |
| Search/command palette | open palette, results, no results | grouped actions, keyboard highlight, recent | permission-hidden action, long result label | keyboard proof and empty result screenshot |
| Maps/logistics | selected item, route/layer active, table split | filter, hover/tooltip, location denied, route recalculation | no tiles, huge route, offline/no GPS, no geolocation, cluster overflow | map/table sync screenshot |
| Deck/proposal | title/offer, comparison, proof slide | appendix, speaker notes, export | missing asset, too much text, print issue | page/screenshot/export check |
| Game/3D/immersive | loaded scene, interaction, pause | success/fail, settings, tutorial | blank canvas, low FPS, mobile control issue | canvas nonblank and mobile proof |

## Critical-State Selection

Use this order when time is limited:

1. Revenue, safety, trust, or data-loss states.
2. The state users hit before value appears: empty, loading, blocked, first run.
3. The most common interaction state: editing, filtering, selecting, dragging,
   streaming, uploading, or booking.
4. The failure state users must recover from.
5. Mobile state if the surface is user-facing or action-heavy.
