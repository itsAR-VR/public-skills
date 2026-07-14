# Token Architecture Contract

Research date: 2026-05-18

Purpose: prevent design systems from becoming one-off colors, spacing, radii,
and shadows scattered through components. Use this when creating or changing
tokens, themes, density modes, dark mode, high-contrast mode, or component
variants.

Primary sources:

- Design Tokens Community Group: https://www.designtokens.org/
- Adobe Spectrum design data: https://opensource.adobe.com/spectrum-design-data/spec/
- Style Dictionary: https://amzn.github.io/style-dictionary/
- Atlassian release phases: https://atlassian.design/release-phases/
- USWDS maturity model: https://designsystem.digital.gov/maturity-model/

## Token Layers

Use three layers when the repo does not already define a better system:

1. Primitive tokens: raw colors, size ramps, font families, durations, shadows.
2. Semantic tokens: purpose-based roles like `text.primary`, `surface.raised`,
   `action.primary`, `border.subtle`, `status.danger`, `focus.ring`.
3. Component tokens: specific slots like `button.primary.background`,
   `card.border`, `table.row.hover`, `toast.danger.icon`.

Do not wire components directly to primitives unless the local system already
does that intentionally.

## Required Modes

For serious products, decide whether each mode exists now, future, or not
needed:

- color scheme: light / dark
- contrast: normal / high contrast
- density: comfortable / compact
- motion: normal / reduced
- platform: web / mobile-style web / desktop app / native-adapted
- brand: single brand / multi-brand / white label

## Change Labels

Every token change should be described as one of:

- `add`: new token, no behavior changed.
- `alias`: new name points to existing value.
- `replace-by`: old token should move to a new token.
- `deprecate`: still works but should not be used in new UI.
- `remove`: deleted token; requires migration proof.

## Component Maturity

When adding reusable components, record:

- owner:
- maturity: experimental / early-access / beta / GA / deprecated
- accessibility status:
- visual proof status:
- usage guidance:
- do-not-use cases:
- deprecation or replacement path:

## Build Rules

- Prefer local tokens before outside component styling.
- If copying public code, map raw values into local semantic tokens.
- If no token exists, add the smallest semantic role needed instead of adding
  many raw values.
- Do not add one-off shadows, radii, colors, or font sizes that only exist in a
  single component unless the component has a clear brand reason.
- Token changes need visual proof on at least one representative component or
  screen.
