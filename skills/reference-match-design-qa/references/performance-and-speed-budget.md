# Performance And Perceived Speed Budget

Research date: 2026-05-18

Purpose: keep design from becoming slow, jumpy, heavy, or frustrating. A design
is not professional if it only looks good after all assets load perfectly.

Use this for websites, dashboards, app shells, animation-heavy surfaces,
media-heavy pages, mobile-style apps, data-heavy screens, and any route where
loading or interaction delay would damage trust.

## Sources To Prefer

- Web Vitals: https://web.dev/articles/vitals
- web.dev performance: https://web.dev/performance
- web.dev responsive design: https://web.dev/learn/design
- Lighthouse: https://developer.chrome.com/docs/lighthouse

## Required Fields

- route_or_surface:
- performance_risk: low / medium / high
- lcp_target:
- inp_target:
- cls_target:
- image_budget:
- font_budget:
- script_budget:
- css_budget:
- animation_budget:
- third_party_budget:
- loading_strategy:
- skeleton_or_placeholder_strategy:
- first_content_priority:
- lazy_load_plan:
- text_stability_plan:
- no_layout_shift_rule:
- reduced_motion_performance_rule:
- measurement_command:

## Design Rules

- Make the most important content appear first.
- Avoid layout shift from late-loading images, fonts, ads, embeds, charts, or
  async cards.
- Treat font choice as a performance decision: choose fewer weights and define a
  fallback stack.
- Heavy animations, WebGL, video, and 3D need a job, a budget, and a fallback.
- Loading states should be honest and stable, not decorative screens that hide
  slow work.

## Proof

- lighthouse_or_web_vitals_result:
- before_after_note:
- slow_network_note:
- mobile_note:
- unresolved_performance_blocker:
