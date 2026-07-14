# No-Reference Design Packet

Use this when the user wants stronger design but does not provide a screenshot,
Figma frame, website, app, moodboard, or taste example.

- Target surface:
- Product/repo:
- User job:
- Product type: SaaS app / internal tool / AI product / landing page / onboarding / dashboard / ecommerce / calendar / editor / canvas / support / mobile-style app / other
- Primary pattern family:
- Secondary pattern family:
- Selected design pattern(s):
- Workflow density: sparse / balanced / dense
- Source lane: real-product UX / pullable code / dashboard shell / motion polish / AI-agent UI / design system / mixed
- primary_database_category:
- supporting_database_categories:
- Selected benchmark sources:
- Chosen art direction:
- direction_id:
- why_this_direction_fits:
- type_pairing:
- surface_rules:
- icon_family:
- source_recipe:
- Comparable quality bar:
- Owner decision needed before build: yes / no

## Plain-English Direction

Describe the one design direction the agent will build. Be specific enough that
another agent could continue the work without inventing a new style.

Use `references/no-reference-art-direction-catalog.md` for `direction_id`.
Use `references/source-recipes-by-product-and-direction.md` for `source_recipe`.
Use `references/design-source-database-index.md` for the typography, color,
layout/box, UX flow, motion, icon/media, data-viz/map, localization, and visual
proof source choices.

## Brand Bootstrap

Use `templates/brand-system-bootstrap.md` when no product `DESIGN.md` or brand
contract exists.

- Existing brand contract: yes / no
- Brand bootstrap needed: yes / no
- Type:
- Color roles:
- Surfaces/depth:
- Icon/asset mode:
- Voice/copy:
- Misuse rules:

## Architecture And Source Database

- product_job:
- primary_action:
- recovery_path:
- information_architecture:
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
`references/service-journey-blueprint.md` when required.

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

## Performance And Speed

Use `references/performance-and-speed-budget.md` when required.

- performance_risk:
- lcp_target:
- inp_target:
- cls_target:
- image_budget:
- font_budget:
- animation_budget:
- loading_strategy:
- skeleton_or_placeholder_strategy:
- measurement_command:

## Measurement And Experimentation

Use `references/measurement-and-experimentation-contract.md` when required.

- primary_success_metric:
- guardrail_metrics:
- funnel_steps:
- event_names:
- privacy_boundary:
- hypothesis:
- experiment_needed:
- rollout_or_review_plan:

## Product Context

- Audience:
- Primary action:
- Secondary actions:
- Decision state users need to understand:
- Existing components/tokens to preserve:
- Weak local styling to improve:
- Local starter pattern(s) to adapt:
- Public code/component sources to inspect:
- Public code/component sources safe to copy:
- GitHub code safety checklist completed:
- Inspiration-only sources:
- Must not do:

## Workflow Skeleton

Use `references/workflow-anatomy-contracts.md` for AI workspace, checkout,
booking, CRM, and map/spatial surfaces.

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
flows.

- trust_sensitive_flow: yes / no
- commitment_or_risk:
- price_permission_or_data_summary:
- review_before_submit_needed:
- receipt_or_confirmation_state:
- cancellation_or_recovery_path:
- no_fake_metrics_or_claims:
- product_truth_risks:

## Cognitive Accessibility And Privacy

Use `references/cognitive-accessibility-and-privacy-checklist.md` when the flow
asks users to remember steps, grant permission, share data, approve work, pay,
recover from errors, or complete multi-step tasks.

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

## Layout And Hierarchy

- Page structure:
- Grid/columns:
- Navigation position:
- Primary focal point:
- Secondary zones:
- Density rules:
- Empty/loading/error/success placement:

## Typography

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
- Label/caption style:
- Weight/casing:
- Line height:
- Max line length:
- Numeric style:
- Localization expansion rule:
- RTL support needed:
- Cultural notes:
- Typography stress cases:
- What must not happen:

## Color And Surfaces

- Background:
- Primary text:
- Secondary text:
- Accent roles:
- Cards/panels:
- Borders:
- Radius:
- Shadows/depth:
- Texture/blur/noise:
- Palette risk to avoid:

## Components And States

- critical_states_first:
- edge_states_required:
- state_proof_required:
- Buttons:
- Inputs/forms:
- Navigation:
- Cards/lists/tables:
- Empty states:
- Loading states:
- Error/success states:
- Hover/focus/pressed states:
- Disabled/destructive states:

## Motion

- Motion purpose:
- Timing/easing:
- Elements that move:
- Reduced-motion behavior:
- Motion to avoid:

## Mobile Behavior

- Layout collapse:
- Navigation:
- Touch targets:
- Content priority:
- Anything hidden or moved:

## Visual Integrity Gate

Use `references/visual-integrity-gate.md`. Any blocker means the build is not
done until fixed, re-shot, or explicitly blocked with proof.

- visual_blockers_to_test:
- long_text_cases:
- dense_data_cases:
- mobile_keyboard_or_safe_area_cases:
- first_collapse_point:
- wrap_truncate_scroll_rules:
- layer_map:
- overflow_containers:
- nested_card_exceptions:
- done_allowed_initially: no

## Anti-Slop Checks

- No generic centered glass-card layout unless it is the correct product pattern.
- No decorative blobs/orbs/glows unless they carry real product meaning.
- No one-note palette or default purple-blue AI gradient.
- No fake metrics, fake logos, fake testimonials, or unsupported proof.
- No oversized marketing hero treatment inside dense app workflows.
- No repeated card grid when a table, timeline, split pane, or focused workflow is better.
- No missing hover, focus, disabled, empty, loading, error, or success states for relevant controls.

## Build Plan

1. TBD
2. TBD
3. TBD

## Proof Required

- Desktop screenshot viewport:
- Mobile screenshot viewport:
- Intermediate/collapse screenshot viewport:
- Build/typecheck command:
- Visual review notes required:
- Screenshot repair playbook required:
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
- The screen looks intentionally designed for this product and job.
- No blocker-class visual defect remains: no overlap, clipped text, unresolved
  text overflow, weird boxes/cards, broken mobile collapse, bad layering, weak
  focus/contrast, or critical truncation.
- Weak or generic design choices that materially affect the experience are
  fixed or named as concrete blockers.
