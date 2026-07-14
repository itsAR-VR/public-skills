# Design Source Database Index

Research date: 2026-05-18

Purpose: give Codex and Claude a practical "database" of where to pull from
when a build needs typography, colors, layouts, surfaces, boxes, components,
animations, UX flows, charts, maps, icons, and product patterns.

This is not a folder of thousands of copied assets. It is a curated source
index that points to large living libraries and tells the agent how to choose
from them safely and tastefully.

## Database Model

For any serious UI build, choose from these categories:

1. Typography database
2. Color and token database
3. Layout and box/surface database
4. Component/block database
5. UX flow database
6. Motion/animation database
7. Icon/illustration/media database
8. Data visualization/map database
9. Accessibility/localization database
10. Research and IA database
11. Website discovery/SEO database
12. Performance and speed database
13. Measurement/experimentation database
14. Service journey database
15. Cognitive accessibility/privacy database
16. Visual proof database

Use one primary category and at most two supporting categories for a single
screen. More than that usually creates incoherent UI.

## Typography Database

| Source | URL | Best use |
| --- | --- | --- |
| Google Fonts | https://fonts.google.com/ | Huge open-source font catalog, language filters, variable fonts, quick web use. |
| Google Fonts FAQ | https://developers.google.com/fonts/faq | Language support, Noto, variable fonts, usage boundaries. |
| Noto Fonts | https://fonts.google.com/noto | Multilingual/script support and fallback families. |
| Noto docs | https://notofonts.github.io/noto-docs/website/use/ | Script-specific Noto UI/document guidance. |
| Fontsource | https://fontsource.org/ | Self-hosted open-source web fonts through packages. |
| Typewolf | https://www.typewolf.com/ | Real-world typography inspiration and pairing research. |
| Typewolf lookbooks | https://www.typewolf.com/lookbooks | Directional pairing ideas for editorial/brand surfaces. |
| Fontshare | https://www.fontshare.com/ | High-quality free typefaces, good for expressive brands. |
| Modern Font Stacks | https://modernfontstacks.com/ | Fast system-font stacks with no webfont dependency. |
| Adobe Fonts docs | https://helpx.adobe.com/fonts/using/add-fonts-website.html | Hosted font projects when a product already uses Adobe Fonts. |

Selection rule: choose typography by product job, language/script coverage,
readability, and brand tone. Do not default to a trendy font when the product
needs dense operational clarity.

## Color And Token Database

| Source | URL | Best use |
| --- | --- | --- |
| Radix Colors | https://www.radix-ui.com/colors | Accessible UI color scales and state ramps. |
| Tailwind colors | https://tailwindcss.com/docs/customizing-colors | Practical color ramps for Tailwind stacks. |
| Material color | https://m3.material.io/styles/color/overview | Product color roles, dynamic color thinking, Material apps. |
| Adobe Color | https://color.adobe.com/ | Palette exploration and harmony. |
| Coolors | https://coolors.co/ | Fast palette generation, not final proof. |
| Accessible Color Matrix | https://toolness.github.io/accessible-color-matrix/ | Pairwise contrast checking. |
| Contrast Grid | https://contrast-grid.eightshapes.com/ | Palette contrast grid. |
| W3C Design Tokens | https://www.designtokens.org/ | Standard token structure. |
| Style Dictionary | https://amzn.github.io/style-dictionary/ | Token build/export pipeline. |
| Primer Primitives | https://primer.style/primitives/ | Mature design token reference. |
| Spectrum design data | https://opensource.adobe.com/spectrum-design-data/spec/ | Token/design data architecture. |

Selection rule: colors become design only when they map to semantic roles,
states, contrast, and brand meaning. Never rely on universal color-psychology
claims.

## Layout And Box/Surface Database

| Source | URL | Best use |
| --- | --- | --- |
| MDN CSS Grid | https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout | Grids, columns, alignment, layout fundamentals. |
| MDN Subgrid | https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout/Subgrid | Cross-card/table alignment and nested layouts. |
| MDN container queries | https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_container_queries | Component-scoped responsive behavior. |
| web.dev responsive design | https://web.dev/learn/design | Responsive structure and web platform basics. |
| Every Layout | https://every-layout.dev/ | Robust layout primitives and composition thinking. |
| Refactoring UI | https://refactoringui.com/ | Spacing, hierarchy, borders, depth, and practical visual structure. |
| Carbon layout | https://carbondesignsystem.com/elements/2x-grid/overview/ | Enterprise grid and spacing discipline. |
| Atlassian spacing/grid | https://atlassian.design/foundations/spacing | Product spacing and grid system reference. |
| Apple layout | https://developer.apple.com/design/human-interface-guidelines/layout | Platform layout, safe areas, and native app structure. |
| Material layout | https://m3.material.io/foundations/layout/overview | Adaptive layout and Material structure. |

Selection rule: define the surface model before styling boxes. Cards, panels,
sheets, tables, split panes, timelines, and canvases are different structures,
not interchangeable decoration.

## Component And Block Database

| Source | URL | Best use |
| --- | --- | --- |
| shadcn/ui | https://ui.shadcn.com/ | Open-code React/Tailwind component baseline. |
| registry.directory | https://registry.directory/ | Discovery for shadcn-compatible registries. |
| ReUI | https://reui.io/ | Production-oriented shadcn components and dense app flows. |
| 21st.dev | https://21st.dev/ | Component/block discovery, including agent UI elements. |
| Magic UI | https://magicui.design/ | Animated shadcn/Tailwind polish for public surfaces. |
| React Bits | https://www.reactbits.dev/ | Expressive animated React components. |
| Motion Primitives | https://motion-primitives.com/ | App-safe Motion primitives. |
| Ark UI | https://ark-ui.com/ | Headless state-machine primitives. |
| React Aria | https://react-aria.adobe.com/ | Accessibility-first behavior reference. |
| Radix UI | https://www.radix-ui.com/primitives | Accessible primitives. |
| Base UI | https://base-ui.com/ | Unstyled accessible primitives. |
| Headless UI | https://headlessui.com/ | Tailwind-friendly unstyled primitives. |
| Floating UI | https://floating-ui.com/ | Positioning/collision behavior for popovers, menus, tooltips. |

Selection rule: use local components first, then copy the smallest useful
outside block only after the GitHub code safety checklist passes.

## UX Flow Database

| Source | URL | Best use |
| --- | --- | --- |
| Mobbin | https://mobbin.com/ | Real app screens and mobile/web flows. |
| Pageflows | https://pageflows.com/ | Flow recordings for onboarding, checkout, settings, subscriptions. |
| Nicelydone | https://nicelydone.club/ | SaaS screens, flows, comparisons. |
| SaaSFrame | https://www.saasframe.io/ | SaaS websites and product screens. |
| UI Sources | https://www.uisources.com/ | Mobile flow references. |
| Baymard checkout UX | https://baymard.com/research/checkout-usability | Checkout and conversion flow heuristics. |
| Baymard mobile UX | https://baymard.com/research/mcommerce-usability | Mobile commerce and form friction. |
| GOV.UK Design System | https://design-system.service.gov.uk/ | Serious forms, validation, content, accessibility. |
| Polaris | https://polaris.shopify.com/ | Commerce/admin UX. |
| Atlassian Design System | https://atlassian.design/ | Product UI, content, drag/drop, state design. |

Selection rule: use real-product UX references for flow structure and states,
not for copying brand styling.

## Motion And Animation Database

| Source | URL | Best use |
| --- | --- | --- |
| Motion | https://motion.dev/ | Default React/JS motion engine. |
| Motion Primitives | https://motion-primitives.com/ | App-safe primitives. |
| Animate UI | https://animate-ui.com/ | shadcn-compatible animated primitives. |
| Auto Animate | https://auto-animate.formkit.com/ | Quick list/layout transitions. |
| Number Flow | https://number-flow.barvian.me/ | Animated metrics and values. |
| LottieFiles | https://lottiefiles.com/ | Branded vector/loading assets. |
| Rive | https://rive.app/ | Interactive vector/state-machine animation. |
| GSAP | https://gsap.com/ | Advanced public-site motion. |
| Lenis | https://github.com/darkroomengineering/lenis | Smooth scrolling for storytelling pages only. |
| Three.js | https://threejs.org/ | 3D/WebGL surfaces. |
| PixiJS | https://pixijs.com/ | 2D canvas/WebGL/game-like surfaces. |

Selection rule: motion needs a job and a reduced-motion fallback.

## Icon, Illustration, And Media Database

| Source | URL | Best use |
| --- | --- | --- |
| Lucide | https://lucide.dev/ | Default line icons for app UI. |
| Heroicons | https://heroicons.com/ | Tailwind-aligned outline/solid icons. |
| Tabler Icons | https://tabler.io/icons | Large neutral icon set. |
| Phosphor Icons | https://phosphoricons.com/ | Flexible weights and friendly tone. |
| Remix Icon | https://remixicon.com/ | Neutral system icons. |
| IconSearch | https://iconsearch.info/ | Icon library comparison. |
| All SVG Icons | https://allsvgicons.com/ | SVG/icon search. |
| Unsplash | https://unsplash.com/ | Real photography when product story needs it. |
| Pexels | https://www.pexels.com/ | Photos/videos. |
| Blush | https://blush.design/ | Illustration packs. |
| Shots.so | https://shots.so/ | Product screenshot mockups. |

Selection rule: one icon family per surface unless a brand system says
otherwise. Match icon stroke/weight to type and density.

## Data Visualization And Map Database

| Source | URL | Best use |
| --- | --- | --- |
| Recharts | https://recharts.org/ | Practical React charts. |
| Nivo | https://nivo.rocks/ | Rich responsive charts. |
| Visx | https://airbnb.io/visx/ | Low-level custom visualization. |
| Observable Plot | https://observablehq.com/plot/ | Concise grammar-of-graphics charts. |
| ECharts | https://echarts.apache.org/ | Advanced dense charts and BI. |
| D3 | https://d3js.org/ | Custom visualization. |
| Tremor | https://www.tremor.so/ | Dashboard-oriented chart components. |
| MapLibre | https://maplibre.org/ | Open map rendering. |
| react-map-gl | https://visgl.github.io/react-map-gl/ | React map components for Mapbox/MapLibre. |
| deck.gl | https://deck.gl/ | WebGL data maps. |
| kepler.gl | https://kepler.gl/ | Spatial analytics and map exploration. |

Selection rule: charts and maps must answer a decision question and include a
fallback for dense or inaccessible views.

## Accessibility And Localization Database

| Source | URL | Best use |
| --- | --- | --- |
| WAI-ARIA APG | https://www.w3.org/WAI/ARIA/apg/ | Custom widget semantics and keyboard models. |
| WCAG 2.2 | https://www.w3.org/WAI/WCAG22/Understanding/ | Accessibility requirements and explanations. |
| W3C i18n | https://www.w3.org/International/ | Internationalization guidance. |
| W3C RTL guidance | https://www.w3.org/International/questions/qa-html-dir | Directionality and RTL markup. |
| FormatJS | https://formatjs.io/ | ICU formatting and React i18n. |
| next-intl | https://next-intl.dev/ | Next.js i18n routing/messages/dates/numbers. |
| MDN logical properties | https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_logical_properties_and_values | Direction-aware CSS. |

Selection rule: if a product is global or culture-sensitive, localization is a
design input before it is a translation task.

## Research And IA Database

| Source | URL | Best use |
| --- | --- | --- |
| NN/g UX research methods | https://www.nngroup.com/articles/which-ux-research-methods/ | Choose a practical research method for the design question. |
| NN/g usability heuristics | https://www.nngroup.com/articles/ten-usability-heuristics/ | Heuristic review for status, language, control, consistency, prevention, recognition, efficiency, focus, recovery, and help. |
| GOV.UK user research | https://www.gov.uk/service-manual/user-research | Research planning, participants, methods, and sharing findings. |
| GOV.UK content design | https://www.gov.uk/guidance/content-design | User needs, evidence, content grouping, links, analytics, and SEO thinking. |
| GOV.UK service navigation | https://design-system.service.gov.uk/patterns/navigate-a-service/ | Navigation patterns for multi-task services. |

Selection rule: use research sources to decide what problem the UI solves and
how users find/complete it. If evidence is missing, record the assumption and
the fastest validation path.

## Website Discovery And SEO Database

| Source | URL | Best use |
| --- | --- | --- |
| Google SEO starter guide | https://developers.google.com/search/docs/fundamentals/seo-starter-guide | Public-page search basics and content structure. |
| Google title links | https://developers.google.com/search/docs/appearance/title-link | Search title/link quality. |
| Google snippets | https://developers.google.com/search/docs/appearance/snippet | Meta description and snippet quality. |
| Google canonical URLs | https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls | Canonical and duplicate URL decisions. |
| Google structured data | https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data | Structured data for eligible page types. |
| Open Graph Protocol | https://ogp.me/ | Social/link preview metadata. |

Selection rule: a public page needs search intent, title, meta description,
canonical/indexing decision, heading outline, link path, and share preview.

## Performance And Speed Database

| Source | URL | Best use |
| --- | --- | --- |
| Web Vitals | https://web.dev/articles/vitals | LCP, INP, CLS, and user-centered performance targets. |
| web.dev performance | https://web.dev/performance | Performance learning, loading, assets, and diagnostics. |
| web.dev responsive design | https://web.dev/learn/design | Responsive layout and adaptation fundamentals. |
| Lighthouse | https://developer.chrome.com/docs/lighthouse | Local/page audit for performance, accessibility, SEO, and best practices. |

Selection rule: speed is part of design. Define font, image, script, animation,
loading, and layout-shift budgets before adding heavy polish.

## Measurement And Experimentation Database

| Source | URL | Best use |
| --- | --- | --- |
| Firebase A/B Testing | https://firebase.google.com/docs/ab-testing | Experiment setup and rollout thinking for app experiences. |
| GOV.UK content analytics guidance | https://www.gov.uk/guidance/content-design | Content analytics and SEO improvement. |
| NN/g UX research methods | https://www.nngroup.com/articles/which-ux-research-methods/ | Decide when measurement is enough and when research is needed. |

Selection rule: define the metric, funnel, event names, guardrails, privacy
boundary, and post-launch review before claiming a redesign is successful.

## Service Journey Database

| Source | URL | Best use |
| --- | --- | --- |
| GOV.UK Service Manual | https://www.gov.uk/service-manual | End-to-end service thinking, research, accessibility, and delivery. |
| GOV.UK user research | https://www.gov.uk/service-manual/user-research | Experience maps, service research, and live-service learning. |
| GOV.UK Design System patterns | https://design-system.service.gov.uk/patterns/ | Serious service patterns for task flows, validation, navigation, confirmations, and failure pages. |

Selection rule: for apps and platforms, design the whole journey: before,
during, after, return visit, failure, recovery, roles, handoffs, and receipts.

## Cognitive Accessibility And Privacy Database

| Source | URL | Best use |
| --- | --- | --- |
| W3C COGA usable content | https://www.w3.org/TR/coga-usable/ | Cognitive and learning disability guidance beyond the WCAG floor. |
| WCAG 2.2 understanding docs | https://www.w3.org/WAI/WCAG22/Understanding/ | Accessibility requirement explanations. |
| U.S. Web Design System accessibility | https://designsystem.digital.gov/documentation/accessibility/ | Practical federal accessibility guidance. |
| Apple privacy guidance | https://developer.apple.com/design/human-interface-guidelines/privacy | Permission and privacy expectations for user trust. |

Selection rule: cognitive load, memory burden, visible labels, undo/back,
timeouts, permission rationale, and opt-out/revoke paths are design quality,
not legal afterthoughts.

## Visual Proof Database

| Source | URL | Best use |
| --- | --- | --- |
| Browser Harness screenshots | https://browser-harness.dev/docs/test-snapshots | Route/page screenshot proof and visual comparisons. |
| Storybook visual tests | https://storybook.js.org/docs/writing-tests/visual-testing/ | Component-state visual proof. |
| Chromatic | https://www.chromatic.com/storybook | Storybook visual regression. |
| Argos | https://argos-ci.com/ | Visual regression for Browser Harness/Storybook. |
| Percy | https://percy.io/ | Page/component visual regression. |
| axe-core | https://github.com/dequelabs/axe-core | Accessibility engine. |

Selection rule: proof should match risk. A shared component needs state proof; a
page needs desktop/mobile; a flow needs sequence proof; a design-system change
needs visual regression when supported.

## Database Use Contract

Every design packet should record:

- conditional_gates_required:
- primary_database_category:
- supporting_database_categories:
- selected_sources:
- why_these_sources_fit:
- what_not_to_copy:
- code_safety_needed:
- proof_method:

The database is there to give the agent more professional choices, not to make a
screen look like every source at once.
