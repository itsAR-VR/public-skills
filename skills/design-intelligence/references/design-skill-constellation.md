# The Design Skill Constellation

This is the compact map of design-related skills in this repo. Use
`design-intelligence` as the front door, then load only the specialist skills
that match the task.

## Phase 1: Discover And Plan

| Skill | Use when |
|---|---|
| `shape` | A new feature needs a design brief before code. |
| `taste-skill` / `design-taste-frontend` | The agent needs stronger UI judgment and anti-generic constraints. |
| `brand` | Brand voice, identity, and messaging need to shape the UI. |
| `brand-alchemy` | Naming, brand DNA, and domain availability are still open. |
| `brand-guidelines` / `brandkit` | Existing brand standards must be applied to an artifact. |

## Phase 2: Explore Variants

| Skill | Use when |
|---|---|
| `design-an-interface` | The user wants multiple distinct interface options. |
| `reference-match-design-qa` | The user has a reference or needs a no-reference design packet. |
| `minimalist-skill` | The target style is clean, editorial, and restrained. |
| `brutalist-skill` | The target style is raw, mechanical, grid-heavy, or terminal-like. |

## Phase 3: Source And Build

| Skill | Use when |
|---|---|
| `vibe-design-reference-libraries` | Code-backed source selection is needed. |
| `premium-ui-components` | Premium animated components are explicitly useful. |
| `ecc-frontend-design` | The implementation needs distinctive frontend patterns. |
| `ui-styling` | The project uses shadcn/Tailwind/Radix. |
| `ui-skills` | The agent needs a compact UI rules layer. |
| `frontend-agent` / `frontend-coding-agent` | The implementation needs an autonomous frontend loop. |
| `design-system-starter` | Tokens, components, accessibility, or system docs are in scope. |
| `design` | Logos, banners, icons, and static brand assets are needed. |
| `screenshot-to-code` | A screenshot, mockup, or Figma design needs conversion to code. |
| `image-to-code-skill` / `images-taste-skill` | The design image should be generated first, then implemented. |
| `landing-page-architecture` / `landing-page-guide-v2` | The work is a landing page. |
| `canvas-design` | The output is static visual art or a document. |

## Phase 4: Refine Atoms

| Skill | Use when |
|---|---|
| `layout` | Spacing, rhythm, hierarchy, or alignment is off. |
| `typeset` | Font choice, type scale, hierarchy, or readability is off. |
| `colorize` | The design is too gray, dull, or visually flat. |
| `theme-factory` | A complete theme needs to be applied quickly. |
| `svg-animations` | SVG motion, logos, or path animations are in scope. |
| `ai-video-scroll-animation` | Scroll-driven video animation is in scope. |
| `ecc-liquid-glass-design` | Apple-platform Liquid Glass design is in scope. |

## Phase 5: Polish And Delight

| Skill | Use when |
|---|---|
| `polish` | The UI needs final alignment, spacing, consistency, and micro-detail repair. |
| `delight` | The UI needs personality, motion, or memorable interaction details. |
| `impeccable` family | The work is already inside an Impeccable frontend flow. |

## Phase 6: Visual QA And Proof

| Skill | Use when |
|---|---|
| `reference-match-design-qa` | Desktop/mobile screenshot proof and mismatch repair are required. |
| `browse-qa` | A running local or deployed UI must be verified in browser. |
| `ultra-review` | Final scope, safety, proof, and blocker review are needed. |

## Quick Mappings

| User says | First skill |
|---|---|
| "Design this from scratch" | `shape` |
| "Make it look better" | `reference-match-design-qa` no-reference mode |
| "Match this screenshot" | `screenshot-to-code` or `reference-match-design-qa` |
| "Show me a few options" | `design-an-interface` |
| "We need a brand" | `brand-alchemy` then `brand` |
| "Apply our brand" | `brand-guidelines` |
| "Make the landing page" | `landing-page-architecture` or `landing-page-guide-v2` |
| "Spacing feels off" | `layout` |
| "Fonts look wrong" | `typeset` |
| "Too gray" | `colorize` |
| "Add delight" | `delight` |
| "Final polish" | `polish`, then `browse-qa` |
| "Did we get the visual details right?" | `reference-match-design-qa` plus `browse-qa` |
