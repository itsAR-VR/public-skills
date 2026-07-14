# Design Build Prompt

Use this after the reference packet or no-reference design packet is accepted.

```text
Use the reference-match-design-qa workflow. The packet is the brief, not the
deliverable. Build the actual UI and iterate until screenshots prove it matches
the reference or no-reference design direction.

Target:
[route/screen/component]

Source of truth:
- Reference packet or no-reference packet: [path or pasted packet]
- Product DESIGN.md: [path if available]
- Universal pattern library: references/universal-code-backed-pattern-library.md
- Design architecture map: references/design-architecture-map.md
- Design source database: references/design-source-database-index.md
- Conditional design gate router: references/conditional-design-gate-router.md
- Typography and cultural system: references/typography-and-cultural-system.md
- Visual integrity gate: references/visual-integrity-gate.md
- Existing design docs/components: [paths]

Build rules:
- Preserve the product's brand and workflow.
- Use existing components/tokens first.
- Use the packet's pattern family and selected design patterns before choosing
  component visuals.
- Use the packet's source database choices for typography, color/tokens,
  layout/box structure, UX flow, motion, icons/media, localization, and proof.
- Use every required conditional gate from the packet. For public pages, cover
  discovery/SEO and performance. For apps/platforms, cover research/IA,
  service journey, measurement, cognitive accessibility/privacy, and adaptive
  proof where relevant.
- Use vibe-design-reference-libraries only for pattern help, not blind copying.
- Do not mix more than 2-4 outside references.
- If a visual reference exists, match the actual layout, hierarchy, spacing,
  typography, surfaces, color roles, states, and mobile behavior as closely as
  product constraints allow.
- If no visual reference exists, choose one strong art direction yourself and
  build against it. Do not ship generic AI-looking UI.
- Do not add fake proof, fake logos, fake stats, or unsupported claims.
- Keep motion purposeful and include reduced-motion behavior.
- Include the relevant states for this product type: empty, loading, error,
  success, disabled, hover, focus, selected, destructive, mobile, and any
  workflow-specific state named in the packet.
- Keep text readable and non-overlapping on desktop and mobile.
- Do not ship overlap, clipped text, unresolved overflow, weird nested boxes,
  broken hierarchy, bad mobile collapse, bad layering, weak focus/contrast, or
  critical truncation.

Definition of done:
- implementation complete
- build/typecheck passes or exact blocker named
- desktop screenshot captured
- mobile screenshot captured
- required gate proof captured or exact blocker named
- visual mismatch review completed
- visual integrity gate shows zero blocker-class defects or exact blocker named
```
