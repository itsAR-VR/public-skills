# Content Design Contract

Research date: 2026-05-18

Purpose: make UI copy part of the design architecture. Good visual design can
still fail when labels, errors, empty states, dates, commitments, or recovery
copy are unclear.

Primary sources:

- Atlassian content design: https://atlassian.design/get-started/content-design
- Atlassian content foundations: https://atlassian.design/foundations/content
- Carbon content overview: https://carbondesignsystem.com/guidelines/content/overview/
- Carbon writing style: https://carbondesignsystem.com/guidelines/content/writing-style/
- Primer placeholders: https://primer.style/accessibility/patterns/placeholders/

## Content Rules

- Prefer sentence case in product UI.
- Buttons should say the result: `Create project`, `Send invite`, `Save plan`,
  `View receipt`.
- Do not use placeholder-only labels or instructions.
- Error copy must say what happened, what it means, and what to do next.
- Empty states need a next action or a clear reason nothing is shown.
- Success states should confirm the outcome and show where proof/receipt lives.
- Dates, times, currencies, names, addresses, and commitments must be
  unambiguous and localizable.
- Avoid idioms, jokes, culture-specific metaphors, and unexplained acronyms in
  functional UI.
- Keep terminology consistent; maintain preferred and banned terms for serious
  products.
- Do not copy claims, testimonials, logos, or metrics from references.

## Packet Fields

- primary_action_copy:
- secondary_action_copy:
- destructive_action_copy:
- empty_state_copy:
- loading_copy:
- error_copy:
- success_copy:
- commitment_or_price_copy:
- terminology_preferred:
- terminology_banned:
- localization_copy_risk:

## Done Gate

- Button labels are action/result clear.
- Errors include recovery.
- Empty/loading/success copy exists where relevant.
- No placeholder-only form labels.
- No unsupported claims or fake proof.
