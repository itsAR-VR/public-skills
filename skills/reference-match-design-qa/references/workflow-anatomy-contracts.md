# Workflow Anatomy Contracts

Research date: 2026-05-18

Purpose: stop product screens from becoming generic cards. Each product type
has a minimum anatomy: the pieces that must exist for the interface to feel like
the real thing instead of a styled mockup.

Use this with `universal-code-backed-pattern-library.md`,
`source-recipes-by-product-and-direction.md`, and `state-coverage-matrix.md`.

## AI Workspace Contract

- conversation_or_instruction_surface:
- tool_execution_surface:
- artifact_or_output_surface:
- approval_boundary:
- receipt_or_audit_surface:
- failure_recovery:
- non_chat_inspection_view:
- streaming_state:
- stop_or_cancel_control:
- privacy_or_permission_note:

Do not ship an AI workspace as only a chat box unless the product truly is only
chat. Agent work needs tool status, approvals, artifacts, and receipts.

## Conversion / Checkout / Billing Contract

- offer_or_item_summary:
- price_breakdown:
- billing_interval_or_trial_terms:
- trust_cues:
- form_or_payment_state:
- review_before_submit:
- promo_error_or_adjustment_state:
- payment_or_commitment_error:
- receipt_or_next_step:
- cancellation_or_refund_path:

The design must make the decision easy and honest before it tries to look
premium.

## Mobile Booking Contract

- first_tap_task:
- service_or_resource_selected:
- date_time_slot_selected:
- timezone_visible:
- availability_state:
- conflict_or_unavailable_state:
- confirmation_state:
- reschedule_or_cancel_path:
- mobile_bottom_action:
- empty_or_no_availability_recovery:

Booking UI fails when time, location, timezone, confirmation, or recovery is
unclear.

## CRM / Workflow Contract

- default_view:
- record_grain:
- list_board_or_table_view:
- detail_panel:
- owner_or_assignee:
- next_action:
- status_or_stage:
- history_or_audit:
- bulk_action_state:
- filter_or_saved_view:
- permission_or_role_state:

CRM UI should optimize repeated work: scanning, filtering, ownership, next
action, and history.

## Spatial Operations / Map Contract

- map_list_priority:
- selected_entity:
- route_or_area_status:
- layer_controls:
- legend:
- exception_queue:
- eta_or_risk_summary:
- cluster_or_density_behavior:
- geolocation_or_permission_state:
- offline_or_no_tiles_state:
- mobile_fallback:

Map UI must keep map, list, filters, and selected item synchronized. A pretty
map without operational state is not enough.
