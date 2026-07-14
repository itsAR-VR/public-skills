# Measurement And Experimentation Contract

Research date: 2026-05-18

Purpose: make design outcomes measurable without turning the product into a
tracker-heavy mess. Use this for onboarding, landing pages, conversion flows,
AI-agent workspaces, dashboards, feature launches, pricing, checkout, and any
redesign where "better" should be proven later.

## Sources To Prefer

- Firebase A/B Testing: https://firebase.google.com/docs/ab-testing
- GOV.UK content design data and analytics: https://www.gov.uk/guidance/content-design
- NN/g UX research methods: https://www.nngroup.com/articles/which-ux-research-methods/

## Required Fields

- primary_success_metric:
- secondary_metrics:
- guardrail_metrics:
- funnel_steps:
- event_names:
- event_properties:
- privacy_boundary:
- data_to_avoid_collecting:
- analytics_destination:
- baseline_available: yes / no
- hypothesis:
- experiment_needed: yes / no
- rollout_plan:
- sample_or_timebox:
- decision_rule:
- post_launch_review_date:

## Design Rules

- Define what "better" means before declaring a redesign successful.
- Track user progress through real tasks, not vanity clicks.
- Avoid collecting personal, sensitive, or unnecessary data.
- Name guardrails so a conversion win does not hide a support, trust, or
  accessibility loss.
- If experimentation is not available, still define the metric and the first
  post-launch review question.

## Proof

- analytics_plan:
- instrumentation_status:
- experiment_or_rollout_note:
- post_launch_learning_owner:
- measurement_gap:
