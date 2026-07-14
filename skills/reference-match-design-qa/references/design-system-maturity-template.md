# Design System Maturity Template

Research date: 2026-05-18

Purpose: help Codex and Claude decide whether a repo needs a tiny design
contract, a component cleanup, or a more formal design-system pass before
building more UI.

Use this for meaningful product UI, shared components, and any design pass that
could affect more than one screen.

## Maturity Levels

| Level | What exists | What to do |
| --- | --- | --- |
| 0. No system | One-off CSS, no tokens, inconsistent components, no design memory. | Create a small `DESIGN.md`, brand bootstrap, typography choice, and visual integrity gate before broad UI work. |
| 1. Local style | A few recurring colors/components, but no clear roles or state coverage. | Name semantic tokens, standardize spacing/radius/surface rules, and repair obvious state gaps. |
| 2. Component set | Reusable components exist, but variants, docs, and states are incomplete. | Add variants, stories/examples where supported, accessibility rules, and long-content proof. |
| 3. Token-backed system | Tokens and components are consistent across surfaces. | Add governance: token change labels, deprecation notes, visual regression, and product-specific pattern guidance. |
| 4. Multi-product system | Multiple apps or brands share primitives with local brand layers. | Separate primitive tokens from brand/product tokens, document exceptions, and require migration notes for changes. |

## Required Fields

- maturity_level:
- current_sources:
- existing_token_source:
- component_library:
- typography_source:
- icon_source:
- motion_source:
- proof_surface:
- biggest_design_debt:
- safe_next_system_step:

## Release Labels

Use these labels when changing shared design behavior:

- `experimental`: usable for one screen or prototype, not a shared default.
- `candidate`: ready for one product area after screenshot proof.
- `stable`: shared use is allowed; states, accessibility, and mobile proof exist.
- `deprecated`: keep working, but do not use for new UI.
- `blocked`: do not ship until the blocker is fixed or explicitly accepted.

## Governance Rules

- A token without a role is a color value, not a design system.
- A component without states is a demo, not a product component.
- A type choice without fallback/script coverage is incomplete for global or
  culture-sensitive products.
- A shared layout pattern needs long-content and mobile/collapse proof.
- Do not expand a design system while leaving obvious visual blockers in the
  current product surface.
