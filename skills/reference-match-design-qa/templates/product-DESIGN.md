# DESIGN.md

Use this as the product's design contract for Codex, Claude, and other coding agents.

## Overview

- Product:
- Audience:
- Primary jobs:
- Design feeling in plain English:
- Density: sparse / balanced / dense
- Core promise:
- Default no-reference design direction:
- Default direction_id:
- Design quality bar:
- Primary pattern families:
- Pattern families to avoid:
- Code-backed source preference:
- Primary source database categories:
- Design system maturity level:

## Research, IA, And Service Model

- Primary user segment:
- Top user tasks:
- Known user evidence:
- Open design assumptions:
- Research method to use next:
- Navigation/section model:
- Label terms to use:
- Label terms to avoid:
- Search/filter model:
- Service journey stages:
- Actors/roles:
- Handoffs:
- Failure/recovery model:

## Brand Bootstrap

Use this section when no mature brand system exists.

- Type pairing:
- Icon family:
- Imagery mode:
- Voice/copy tone:
- Elevation model:
- Interaction personality:
- Misuse rules:
- Source recipe:

## Colors

### Roles

- Background:
- Surface:
- Elevated surface:
- Primary text:
- Secondary text:
- Muted text:
- Primary action:
- Secondary action:
- Success:
- Warning:
- Error:
- Focus ring:

### Rules

- Use accents for:
- Do not use accents for:
- Avoid:

## Typography

- Font family:
- Font source:
- Display/accent font:
- Fallback stack:
- Script/language support:
- Display/headline style:
- Body style:
- Label/caption style:
- Mono/code style:
- Line-height rules:
- Letter-spacing rules:
- Numeric style:
- Localization expansion rule:
- RTL support:
- Cultural notes:

## Layout And Spacing

- Base spacing rhythm:
- Page width:
- Section spacing:
- Card/panel spacing:
- Dashboard density:
- Mobile spacing:

## Shapes, Borders, And Depth

- Radius:
- Border style:
- Shadow/depth:
- Blur/transparency:
- Texture/noise:
- What should feel flat:
- What should feel elevated:

## Components

### Buttons

- Primary:
- Secondary:
- Icon-only:
- Disabled:
- Loading:

### Inputs And Forms

- Field style:
- Label style:
- Validation:
- Help text:

### Navigation

- Desktop:
- Mobile:
- Active state:

### Cards, Panels, Tables, Lists

- Cards:
- Panels:
- Tables:
- Lists:
- Empty states:
- Loading states:
- Error states:
- Success states:
- Destructive states:

### Product-Specific Patterns

- App shell:
- Forms/settings:
- Tables/reports:
- AI/agent surfaces:
- Ecommerce/billing:
- Scheduling/calendar:
- Content/editor:
- Canvas/workflow:
- CRM/workflow:
- Maps/spatial:
- Mobile-style behavior:
- Other:

## Website Discovery And SEO

Use this for public web routes.

- Indexable public routes:
- Private/noindex routes:
- Default title pattern:
- Default meta description pattern:
- Canonical URL rule:
- Open Graph/social preview rule:
- Structured data types:
- Heading outline rule:
- Internal linking rule:
- Content freshness/review rule:

## State Priority

- critical_states_first:
- edge_states_required:
- state_proof_required:

## Motion

- Motion purpose:
- Preferred timing:
- Elements that may animate:
- Elements that should not animate:
- Reduced-motion rule:

## Performance And Loading

- LCP target:
- INP target:
- CLS target:
- Image budget/rule:
- Font budget/rule:
- Script/third-party budget:
- Animation budget:
- Loading/skeleton pattern:
- No-layout-shift rule:
- Measurement command:

## Mobile Behavior

- Navigation:
- Primary actions:
- Content priority:
- Touch targets:
- Layout collapse:

## Trust And Risk

- Trust-sensitive flows:
- Review-before-submit rule:
- Receipt/audit rule:
- Destructive action rule:
- Privacy/security copy rule:

## Cognitive Accessibility And Privacy

- Plain-language rule:
- Memory-load rule:
- Visible progress/step rule:
- Undo/back rule:
- Timeout/data-loss rule:
- Keyboard/focus rule:
- Screen-reader status rule:
- Permission rationale rule:
- Data collection summary rule:
- Opt-out/revoke rule:

## Measurement And Experimentation

- Primary success metric:
- Guardrail metrics:
- Funnel steps:
- Event naming rule:
- Data not to collect:
- Experiment policy:
- Rollout/review cadence:

## Visual Integrity Rules

- No overlap/occlusion:
- No clipped text:
- No unresolved text overflow:
- No incoherent card/box nesting:
- No broken responsive collapse:
- No layer conflicts:
- No weak focus/contrast:
- Long-content stress cases:
- Layer map:

## Do

- TBD

## Don't

- TBD

## No-Reference Quality Floor

- Choose one product-appropriate art direction before coding.
- Make hierarchy, spacing, type, surfaces, states, and mobile behavior feel
  intentional even when the user provides no visual reference.
- Avoid generic AI-app defaults: purple-blue gradients, decorative glows, random
  glass cards, oversized marketing copy inside app workflows, and repetitive
  card grids.
- Design the actual workflow, including empty, loading, error, success, hover,
  focus, disabled, and mobile states where relevant.
- Choose typography, layout, box/surface structure, color/tokens, UX flow,
  motion, icons/media, localization, and proof sources from the design source
  database when the repo does not already define them.

## Proof Rules

- Meaningful UI work needs desktop screenshot proof.
- Meaningful UI work needs mobile screenshot proof.
- Reference-matching work needs a reference packet.
- No-reference design work needs a no-reference design packet.
- Conditional gates required by the surface must be filled, proven, or named as
  concrete blockers.
- Public web routes need metadata, share preview, heading outline, speed, and
  indexing proof where relevant.
- App/platform flows need journey, recovery, measurement, and accessibility
  proof where relevant.
- If screenshots are blocked, name the exact blocker and smallest alternate proof.
- Meaningful UI work is not done while visual blockers remain.
