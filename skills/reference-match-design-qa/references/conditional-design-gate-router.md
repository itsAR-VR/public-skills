# Conditional Design Gate Router

Research date: 2026-05-18

Purpose: make the specialist design layers operational. Do not let an agent
skip research, IA, content, performance, accessibility, SEO, analytics, or
service-flow checks just because the screen looks good.

## How To Use

Before coding, mark every matching trigger as `required`, `not relevant`, or
`blocked`. Any `required` gate must appear in the reference packet,
no-reference packet, product `DESIGN.md`, or visual review report.

## Gate Table

| Trigger | Required gate | Reference file |
| --- | --- | --- |
| Website, landing page, marketing page, docs page, public product page | Discovery, SEO, metadata, share preview, content structure | `website-discovery-seo-contract.md` |
| App, dashboard, platform, admin, CRM, workspace, repeated workflow | Product evidence, IA, top tasks, service journey | `experience-research-contract.md`, `service-journey-blueprint.md` |
| Onboarding, activation, setup, account creation, import, permission request | Time-to-first-value, skip/resume, consent, activation metric | `experience-research-contract.md`, `measurement-and-experimentation-contract.md`, `cognitive-accessibility-and-privacy-checklist.md` |
| Checkout, billing, pricing, auth, destructive action, finance, healthcare, legal | Trust, privacy, recovery, review-before-submit | `trust-sensitive-flow-checklist.md`, `cognitive-accessibility-and-privacy-checklist.md` |
| Navigation, search, filtering, content-heavy page, docs, marketplace, settings | IA validation, labels, search/filter plan, content hierarchy | `experience-research-contract.md`, `content-design-contract.md` |
| Data table, chart, map, report, analytics, operational dashboard | Decision question, chart/table fallback, annotations, state proof | `data-viz-decision-matrix.md` |
| Modal, popover, sheet, command palette, drag/drop, editor, canvas, AI workspace | Keyboard path, focus return, status announcements, escape/recovery | `interaction-accessibility-checklist.md` |
| Mobile-style app, PWA, native-feeling web app, desktop-like web app | Platform mode, safe areas, back behavior, input mode, app chrome | `platform-adaptation-checklist.md`, `component-adaptivity-checklist.md` |
| Shared component, token change, new theme, reference copied from outside source | Token architecture and design-system maturity | `token-architecture-contract.md`, `design-system-maturity-template.md` |
| Motion, loading screen, transition, animated metric, 3D/canvas effect | Motion budget, reduced motion, performance impact | `motion-budget-checklist.md`, `performance-and-speed-budget.md` |
| Any meaningful UI change | Visual integrity, screenshot proof, state proof | `visual-integrity-gate.md`, `visual-proof-pipeline.md` |
| Any flow that needs business proof | Measurement, funnel events, experiment or rollout criteria | `measurement-and-experimentation-contract.md` |

## Done Rule

If a gate is `required`, the design is not done until the gate is either:

- filled and reflected in the built UI,
- verified with screenshots, tests, or review notes, or
- named as a concrete blocker with the smallest next action.

## Plain-English Use

This router prevents a common AI design failure: making a screen attractive but
forgetting whether people can find it, understand it, trust it, use it with a
keyboard, load it quickly, or measure whether it worked.
