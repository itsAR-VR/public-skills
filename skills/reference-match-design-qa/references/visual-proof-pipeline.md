# Visual Proof Pipeline

Research date: 2026-05-18

Purpose: turn "looks good" into repeatable proof. Use this for visible UI
changes, shared components, reference matching, no-reference design, and
visual-regression setup.

Primary sources:

- Browser Harness visual comparisons: https://browser-harness.dev/docs/test-snapshots
- Storybook visual testing: https://storybook.js.org/docs/writing-tests/visual-testing/
- Chromatic visual tests: https://www.chromatic.com/storybook
- Argos visual regression: https://argos-ci.com/

## Proof Levels

| Work type | Minimum proof | Stronger proof |
| --- | --- | --- |
| One visible page | desktop and mobile screenshots | Browser Harness snapshots for stable route |
| Reference match | reference screenshot plus desktop/mobile implementation screenshots | pixel/visual comparison with masks for dynamic regions |
| Shared component | state screenshots or Storybook stories | Storybook visual tests across states/themes |
| Complex flow | key sequence screenshots | Browser Harness flow plus state transitions |
| Design system change | representative component/page screenshots | visual regression baseline review |
| Animation/canvas/3D | nonblank, framed screenshot plus interaction check | video or pixel/canvas checks where supported |

## Stability Rules

- Freeze or mask dynamic timestamps, avatars, randomized data, animations, and
  external media when comparing screenshots.
- Generate and compare snapshots in the same browser/OS environment when using
  strict baselines.
- Record viewport, theme, density, locale, data state, and route.
- Do not approve visual snapshot updates unless the design change is intentional.
- For no-reference work, compare against the no-reference packet and visual
  integrity gate, not just against previous screenshots.

## Required Fields

- proof_level:
- desktop_viewport:
- mobile_viewport:
- intermediate_viewports:
- states_captured:
- dynamic_regions_masked:
- locale/theme/density:
- visual_regression_tool:
- baseline_update_needed:
- approved_diff_reason:
- proof_artifact_paths:
