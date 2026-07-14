# Reference Packet

- Target surface:
- Product/repo:
- Source reference:
- Reference type: screenshot / Figma / website / app / moodboard / taste example
- Match level: exact / close / inspired / pattern-only
- Primary pattern family:
- Secondary pattern family:
- Selected design pattern(s):
- Source lane: screenshot / Figma / live URL / app flow / code registry / AI-agent UI / design system / mixed
- primary_database_category:
- supporting_database_categories:
- Owner decision needed before build: yes / no

## Plain-English Target

Describe what the finished screen should feel like in one short paragraph.

## Product Constraints

- Product brand rules:
- Existing components/tokens to preserve:
- Local starter pattern(s) to adapt:
- Public code/component sources to inspect:
- Public code/component sources safe to copy:
- Inspiration-only sources:
- Audience:
- Workflow density: sparse / balanced / dense
- Must not do:

## Source Database Choices

Use `references/design-source-database-index.md`.

- selected_sources:
- why_these_sources_fit:
- what_not_to_copy:
- code_safety_needed:
- proof_method:
- design_system_maturity_level:
- token_architecture_needed:

## Conditional Design Gates

Use `references/conditional-design-gate-router.md`. Mark every matching gate
before coding.

- research_or_IA_gate: required / not relevant / blocked
- website_discovery_SEO_gate: required / not relevant / blocked
- performance_speed_gate: required / not relevant / blocked
- measurement_experimentation_gate: required / not relevant / blocked
- service_journey_gate: required / not relevant / blocked
- cognitive_accessibility_privacy_gate: required / not relevant / blocked
- interaction_accessibility_gate: required / not relevant / blocked
- platform_adaptivity_gate: required / not relevant / blocked
- data_viz_map_gate: required / not relevant / blocked
- token_governance_gate: required / not relevant / blocked
- motion_budget_gate: required / not relevant / blocked
- visual_proof_gate: required / not relevant / blocked

## Research, IA, And Service Journey

Use `references/experience-research-contract.md` and
`references/service-journey-blueprint.md` when required. A visual reference
does not replace product evidence.

- user_segment:
- user_job_to_be_done:
- top_task:
- design_assumption:
- evidence_available:
- research_question:
- recommended_validation_method:
- section_map:
- label_terms_to_use:
- search_or_filter_plan:
- actors_or_roles:
- journey_stages:
- handoffs:
- failure_points:
- recovery_paths:

## Website Discovery And Page Metadata

Use `references/website-discovery-seo-contract.md` for public pages.

- page_intent:
- search_intent:
- title_tag:
- meta_description:
- canonical_url:
- robots_indexing:
- open_graph_preview:
- heading_outline:
- structured_data:
- internal_links:
- content_freshness_or_review_date:

## Performance, Measurement, And Experimentation

Use `references/performance-and-speed-budget.md` and
`references/measurement-and-experimentation-contract.md` when required.

- performance_risk:
- lcp_target:
- inp_target:
- cls_target:
- image_budget:
- font_budget:
- animation_budget:
- loading_strategy:
- measurement_command:
- primary_success_metric:
- guardrail_metrics:
- funnel_steps:
- event_names:
- privacy_boundary:
- hypothesis:
- experiment_needed:
- rollout_or_review_plan:

## Workflow Skeleton

Use `references/workflow-anatomy-contracts.md` for AI workspace, checkout,
booking, CRM, and map/spatial surfaces. Reference-led work still needs this
when the reference is a real workflow, not just a visual surface.

- workflow_type:
- first_user_decision:
- repeated_user_action:
- system_feedback_needed:
- approval_or_commitment_boundary:
- receipt_or_audit_surface:
- recovery_path:
- product_specific_anatomy:

## Trust / Risk / Truth

Use `references/trust-sensitive-flow-checklist.md` for checkout, billing, auth,
agent approvals, destructive actions, privacy, finance, healthcare, and legal
flows. A reference can inspire layout, but it cannot remove trust obligations.

- trust_sensitive_flow: yes / no
- commitment_or_risk:
- price_permission_or_data_summary:
- review_before_submit_needed:
- receipt_or_confirmation_state:
- cancellation_or_recovery_path:
- no_fake_metrics_or_claims:
- product_truth_risks:

## Cognitive Accessibility And Privacy

Use `references/cognitive-accessibility-and-privacy-checklist.md` when required.

- plain_language_checked:
- memory_load_risk:
- visible_steps_or_progress:
- help_in_context:
- undo_or_back_path:
- timeout_or_data_loss_risk:
- keyboard_path:
- focus_return:
- screen_reader_status_messages:
- permission_or_data_request:
- permission_rationale:
- opt_out_or_revoke_path:

## Reference Breakdown

### Layout And Composition

- Page structure:
- Grid/columns:
- Alignment:
- Whitespace/density:
- First thing the eye should see:
- Secondary areas:

### Typography

- typography_posture:
- font_source:
- primary_font:
- secondary_or_display_font:
- mono_font:
- script_language_support:
- fallback_stack:
- Font direction:
- Heading scale:
- Body scale:
- Weight/casing:
- Line height:
- Max line length:
- Numeric style:
- Localization expansion rule:
- RTL support needed:
- Cultural notes:
- Typography stress cases:
- What must not happen:

### Color And Surfaces

- Background:
- Primary text:
- Secondary text:
- Accent roles:
- Cards/panels:
- Borders:
- Radius:
- Shadows/depth:
- Texture/blur/noise:

### Components And States

- Buttons:
- Inputs/forms:
- Navigation:
- Cards/lists/tables:
- Empty states:
- Loading states:
- Error/success states:
- Hover/focus/pressed states:
- Disabled/destructive states:

### Motion

- Motion purpose:
- Timing/easing:
- Elements that move:
- Reduced-motion behavior:
- Motion to avoid:

### Mobile Behavior

- Layout collapse:
- Navigation:
- Touch targets:
- Content priority:
- Anything hidden or moved:

### Visual Integrity And Stress Cases

Use `references/visual-integrity-gate.md`.

- visual_blockers_to_test:
- long_text_cases:
- dense_data_cases:
- mobile_keyboard_or_safe_area_cases:
- first_collapse_point:
- wrap_truncate_scroll_rules:
- layer_map:
- overflow_containers:
- nested_card_exceptions:

## Exact Match Items

These should match the reference closely:

- TBD

## Product Adaptation Items

These should be adapted to our brand/product instead of copied:

- TBD

## Build Plan

1. TBD
2. TBD
3. TBD

## Proof Required

- Desktop screenshot viewport:
- Mobile screenshot viewport:
- Intermediate/collapse screenshot viewport:
- Build/typecheck command:
- Visual review report path:
- Visual comparison notes required:
- Visual integrity gate required:
- Dynamic content to mask/stabilize:
- Required state screenshots or notes:
- Required flow proof:
- Long-content stress proof:
- Accessibility/localization proof:
- License/provenance check:

## Done Means

- The target surface is implemented.
- Screenshots exist.
- Required conditional gates are filled, proven, or named as concrete blockers.
- No blocker-class visual defect remains.
- The largest mismatches are fixed or named as concrete blockers.
- Any remaining mismatch has a clear reason or next action.
