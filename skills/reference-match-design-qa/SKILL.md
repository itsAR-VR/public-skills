---
name: reference-match-design-qa
description: Depth skill loaded by design-intelligence for reference-match and no-reference design QA. Creates a reference or no-reference design packet before coding, translates the desired visual outcome into product-specific rules, implements the actual UI, and requires desktop/mobile screenshot proof plus mismatch review before UI work is called done. Covers the universal code-backed pattern library for any product type (SaaS, dashboard, ecommerce, calendar, editor, canvas, CRM, agent workspace).
related_skills:
  - design-intelligence
  - vibe-design-reference-libraries
  - ecc-frontend-design
  - design-system-starter
  - browse-qa
  - webapp-testing
routing:
  domain_keywords:
    - reference match
    - visual QA
    - screenshot proof
    - no reference design
    - code-backed design
    - universal design pattern library
    - design packet
    - mismatch review
    - state coverage matrix
    - visual integrity gate
  intent_patterns:
    - "(?:match|recreate|copy).*?(?:screenshot|figma|reference|website).*?(?:design|UI|screen)"
    - "(?:no reference|without a reference|not AI slop|premium UI).*?(?:design|UI|screen)"
  lane: codex-worker
  task_type: frontend-design-qa
---

# Reference Match And Design Excellence QA

For normal use, `design-intelligence` is the front door. If this skill is
invoked directly for meaningful UI work, still apply the full design-intelligence
route before implementation.

Use this skill to make design work less guessy and less generic. The job is not
to produce a target and stop. The job is to build the actual UI to that target,
then force proof that the implementation matches the target.

When the user provides a reference, match the reference as closely as the product
and legal/brand constraints allow. When the user gives no reference, choose a
strong product-appropriate design direction yourself and build against that. Do
not fall back to generic centered cards, soft gradients, oversized hero copy, or
decorative UI that does not serve the workflow.

This skill is not for blindly copying another brand. It is for extracting or
creating useful design structure: layout, hierarchy, spacing, type, color,
surfaces, motion, states, and responsive behavior.

For the current source map, read
`references/source-index-2026-05-18.md`. It captures the expanded GitHub and web
sweep across shadcn registries, React/Tailwind component repos, dashboard
templates, real SaaS/app flow galleries, motion libraries, design systems, and
visual QA tooling.

For broad or no-reference builds, also read
`references/universal-code-backed-pattern-library.md`. It maps any future
website, app, dashboard, agent workspace, ecommerce flow, editor, calendar,
canvas, support surface, or unknown product type to pattern families,
code-backed source lanes, required states, and proof expectations.

For the professional design judgment layer, also read
`references/design-doctrine-and-qa.md`. It captures hierarchy, accessibility,
token, state, motion, Storybook/Browser Harness proof, and anti-generic UI rules.

For the full architecture layer, read `references/design-architecture-map.md`.
It forces product job, information architecture, brand, typography, layout,
content, states, motion, accessibility, visual integrity, proof, and governance
before implementation.

For the broad reusable source database, read
`references/design-source-database-index.md`. It indexes typography, colors,
tokens, layout/box structures, components, UX flows, motion, icons/media,
charts/maps, accessibility/localization, and proof tools.

For typography, font sourcing, script coverage, localization, and cultural
design, read `references/typography-and-cultural-system.md`.

For zero-blocker visual QA, read `references/visual-integrity-gate.md`.

For product-specific workflow anatomy, read
`references/workflow-anatomy-contracts.md`.

For the mandatory gate router, read
`references/conditional-design-gate-router.md`. It tells you which specialist
layers must be active for the surface before coding.

For token architecture, design-system maturity, content, platform, localization,
data-viz, motion, interaction accessibility, trust-sensitive flows, cognitive
accessibility/privacy, website discovery/SEO, research/IA, performance,
measurement, service journeys, and visual proof, read the matching files in
`references/`.

For the newest additive GitHub sources, read
`references/additive-github-source-lanes-2026-05-18.md`.

For broad design resources across learning, UX, free UI, icons, typography,
color, animations, assets, inspiration, data viz, AI UI, and visual QA, read
`references/pro-design-resource-library-2026-05-18.md`.

For no-reference design, read
`references/no-reference-art-direction-catalog.md` and choose one
`direction_id` before coding.

For product/source selection, read
`references/source-recipes-by-product-and-direction.md` and choose one source
recipe before pulling references or code.

For state coverage, read `references/state-coverage-matrix.md` and select the
states that must be built and proven for the product type.

For screenshot repair, read `references/screenshot-repair-playbook.md` and use
it after the first desktop/mobile screenshots.

For public GitHub/component code, read
`references/github-code-safety-checklist.md` before copying code.

## Quick Workflow

1. Identify the target surface: route, screen, flow, component, landing page,
   dashboard, onboarding, mobile view, or app shell.
2. Read the target repo design source if it exists: `DESIGN.md`, design docs,
   brand docs, existing components, screenshots, or product planning.
3. Pick the product/build type before coding. If the product type is broad,
   unknown, or no-reference, read
   `references/universal-code-backed-pattern-library.md` and choose one primary
   pattern family plus any necessary secondary family.
4. Pick the source database category before coding: typography, color/tokens,
   layout/boxes, components, UX flow, motion, icons/media, data-viz/maps,
   accessibility/localization, visual proof, research/IA, performance,
   discovery/SEO, measurement, or service journey. Use
   `references/design-source-database-index.md`.
5. Read `references/conditional-design-gate-router.md` and mark every matching
   trigger as `required`, `not relevant`, or `blocked`. Load the required gate
   files before coding.
6. If source selection is unclear, read `references/source-index-2026-05-18.md`
   and `references/source-recipes-by-product-and-direction.md`, then pick the
   right lane: exact reference, real-product UX pattern, pullable-code
   registry, dashboard/app shell, motion polish, AI/agent UI, design system, or
   workflow-specific source.
7. Choose the design mode:
   - `reference-led`: the user provided a screenshot, website, URL, image,
     app, moodboard, taste example, or optional Figma handoff.
   - `no-reference`: the user only asked for better design, premium polish, a
     redesigned surface, or less AI-looking UI.
8. For `reference-led`, create a reference packet before coding using
   `templates/reference-packet.md`. Figma is optional; use it only when the user
   provides it or the repo already has a useful handoff. Screenshots, websites,
   real product examples, and live browser references are the normal path.
9. For `no-reference`, create an art-direction packet before coding using
   `templates/no-reference-design-packet.md`. Fill `direction_id`, source
   recipe, brand bootstrap, typography/cultural fields, source database choices,
   conditional gates, workflow anatomy, trust/risk/truth fields, and state
   coverage.
10. Decide the match level:
   - `exact`: same visual structure, adjusted only for product content/assets.
   - `close`: same feeling and major layout, adapted to our product.
   - `inspired`: only borrow selected patterns.
   - `pattern-only`: use the reference only to understand an interaction.
11. Pick at most 2-4 references or benchmark patterns. Use one for structure, one
   for workflow, one for motion, and one for polish only when needed.
12. If useful code exists in a compatible open repo or registry, pull only the
   needed component/block and rewrite it into the product's local system.
13. If design memory is missing, create or update a product `DESIGN.md` using
   `templates/product-DESIGN.md` and the brand bootstrap template.
14. If the user has taste feedback, save it in a taste ledger using
   `templates/taste-ledger.md`.
15. Implement the actual UI, not just the packet.
16. Capture desktop and mobile screenshots.
17. Review mismatches with `templates/design-review-rubric.md`,
    `templates/visual-review-report.md`, the screenshot repair playbook, and
    `references/visual-integrity-gate.md`.
18. Fix every blocker-class visual defect before calling the work done. A
    blocker is overlap, clipping, text overflow, weird boxes/cards, broken
    hierarchy, bad mobile collapse, layer conflict, weak focus/contrast, or
    critical truncation.

## When To Stop Before Coding

Stop and create a packet first when the user says any of:

- "make it look like this"
- "match this"
- "use this as inspiration"
- "not AI slop"
- "make it premium"
- "copy this style"
- "use this screenshot"
- "use this Figma" (optional input only, not a default requirement)
- "make it feel like [site/app]"
- "make this look good"
- "make the design better"
- "make it not AI slop"
- "I do not have a reference"

Do not jump straight into implementation from those prompts. The packet is the
design brief, but it is not the deliverable. The deliverable is the built,
verified UI.

## Exact Match Means Build It

If the user provides a visual reference and asks to match it, "done" means the
actual implemented surface visually tracks the reference:

- same major layout and content rhythm
- same visual hierarchy and focal point
- comparable spacing density and alignment
- comparable type scale, weight, and line length
- comparable surface treatment, border weight, radius, and depth
- comparable color roles and contrast, adapted only where product brand requires
- comparable interaction states and mobile collapse

The first coding pass should be treated as a draft. After screenshots, compare
the implementation to the packet/reference, patch all blocker-class visual
defects, then patch the highest-impact remaining mismatches. Do not stop with
"I created a target" or "I matched the vibe" if the screen obviously does not
look like the reference.

Use a concrete blocker only when exact matching is impossible because of missing
assets, inaccessible reference details, unavailable fonts, legal/brand
constraints, missing product data, or a target repo limitation.

## No-Reference Design Mode

Use `templates/no-reference-design-packet.md` when no visual reference is given.
In this mode, the agent must choose a strong design direction itself.

Default behavior:

- Infer the product type, audience, density, and primary workflow from the repo
  and prompt.
- Pick one clear `direction_id` from
  `references/no-reference-art-direction-catalog.md`, not a generic blend.
- Use `references/source-recipes-by-product-and-direction.md` for pattern and
  quality-bar selection without requiring the user to provide an example.
- Fill the brand bootstrap when no stable brand/design memory exists.
- Fill typography source, fallback, script/language support, cultural notes, and
  localization stress cases when the product is global, culture-sensitive, or
  likely to use long/translated content.
- Fill workflow anatomy for AI workspaces, checkout/billing, booking, CRM, maps,
  or other product-specific flows.
- Use `references/state-coverage-matrix.md` to decide which states must be
  built and proven.
- Use existing product components and tokens where they are good; improve weak
  local styling instead of blindly preserving it.
- Add a small amount of distinct product character: typography rhythm, spacing,
  surface rules, icon usage, motion restraint, empty/loading/error states, and
  mobile behavior.
- Avoid default AI UI: centered glass cards, purple-blue gradients, random glow,
  oversized text inside app tools, decorative blobs, repeated card grids,
  fake metrics, and unsupported social proof.

For no-reference work, the acceptance target is "this looks like a serious
product surface for its job," not "this has a fashionable effect."

## Source Selection Lanes

Use the source index to pick the right kind of source before coding:

- **Real-product UX references**: Mobbin, Nicelydone, SaaSFrame, Pageflows,
  UIguana, Godly, SiteSee, Minimal Gallery. Use for workflow structure, states,
  and product patterns. Do not copy brand styling blindly.
- **Pullable shadcn/React code**: shadcn/ui, registry.directory, ReUI,
  Shadcnblocks, 21st.dev, Magic UI, React Bits, Tailark, Dice UI, Coss UI,
  Animate UI, shadcn-admin, next-shadcn-dashboard-starter, shadcn-studio. Use
  when the target repo stack is compatible and the code passes safety/product
  fit checks.
- **Dashboard and app shell references**: shadcn-admin, Kiranism dashboard
  starter, marmelab admin kits, ReUI data grids/filters/Kanban, tablecn, Open
  Status data-table filters. Use for dense internal tools and operational apps.
- **Motion and memorable moments**: React Bits, Magic UI, Animate UI, SmoothUI,
  Cult UI, Vengeance UI, MotionSites. Use sparingly, with reduced-motion.
- **AI and agent interfaces**: Vercel AI Elements, assistant-ui, ElevenLabs UI,
  Manifest UI, 21st.dev Agent Elements, Supabase UI, and assistant/chat
  examples. Use for conversations, tool-call cards, streaming states, agent
  workspaces, voice/audio surfaces, and generative UI.
- **Mature design systems**: Radix, Base UI, Headless UI, Carbon, Fluent, Primer,
  Polaris, USWDS, TDesign, Arco, React Aria/Tailwind libraries, Storybook
  design-system examples. Use for accessibility, structure, and state patterns,
  not as the product brand.
- **Visual proof tooling**: Browser Harness screenshot assertions, Storybook stories,
  Chromatic/visual regression, Argos, or Percy when already available. Use for
  proof, not just final reporting.

The default for React/Tailwind/shadcn repos is: local components first, then
shadcn primitives, then ReUI/registry.directory/21st/Magic UI/React Bits as
pattern or code sources, then screenshot proof.

The default for AI products is: local app shell first, then agent/chat source
lane, then workflow-specific SaaS references, then visual proof across normal,
loading, streaming, tool-running, error, empty, and completed states.

## Universal Pattern Selection

Use `references/universal-code-backed-pattern-library.md` when the request could
be any kind of build, not only Chief or a known product. The selector covers
marketing sites, app shells, admin tools, reports, forms, onboarding, AI/agent
workspaces, ecommerce, scheduling, content/editors, canvas builders, CRMs,
files/media, billing, support, mobile-style apps, maps, documents, games, and
future product categories.

Before coding, record:

- primary pattern family
- secondary pattern family if needed
- selected local starter pattern or external code-backed source
- required states
- no-reference `direction_id` when relevant
- source recipe when relevant
- motion class
- desktop/mobile proof required

This prevents "make it look good" from collapsing into the same generic app
layout every time.

## Code Pull Rules

the user has approved using public GitHub references and pulling code when useful.
Still keep the implementation professional:

- Use `references/github-code-safety-checklist.md` as the canonical checklist
  before copying code from public GitHub/component sources.
- Star count and reputation are a source-selection signal, not a safety pass.
  Reputable repos should be inspected first, then copied from when the code is
  safe and useful.
- the user has approved GitHub code use, so do not block useful GitHub code because
  of license anxiety when the user has explicitly approved the source.
- Preserve source/provenance notes so copied patterns can be traced later.
- Pull the smallest component/block needed, not a whole framework, unless the
  user explicitly asks for the whole repo.
- Rewrite imports, tokens, spacing, type, surfaces, and state handling into the
  target repo's local conventions.
- Use premium or restricted-distribution sources only when the user has approved
  access; still copy the smallest useful block and rewrite it locally.
- Security-check copied code for network calls, trackers, analytics beacons,
  auth/payment behavior, credential handling, secrets, eval/new Function,
  dynamic script injection, remote script loading, postinstall/setup scripts,
  shell commands, unnecessary dependency installs, obfuscated code, dangerous
  browser APIs, and hidden side effects.
- When a reputable source passes the checks and gives us a useful reusable
  pattern, adapt the idea into this skill's local pattern layer or references so
  future builds can learn from it without re-researching from scratch.
- Do not copy fake logos, fake testimonials, fake usage metrics, or claims from
  the source.

## Reference Packet Requirements

Load `templates/reference-packet.md` and fill in:

- source and match level
- pattern family and selected design pattern(s)
- product constraints and anti-goals
- layout and density
- typography
- colors and surfaces
- component anatomy and states
- motion
- mobile behavior
- exact-match items
- product-adaptation items
- code/source candidates
- visual review method
- proof requirements

Keep the packet short enough to guide work. It should be specific, not poetic.

## No-Reference Packet Requirements

Load `templates/no-reference-design-packet.md` and fill in:

- product type and user job
- chosen `direction_id`
- why the direction fits the product, audience, and workflow density
- source recipe
- brand bootstrap fields when no stable design memory exists
- quality bar and comparable product class
- layout and density
- typography
- colors and surfaces
- component/state plan
- critical states and edge states from the state coverage matrix
- motion and mobile rules
- anti-slop checks
- source lane and benchmark candidates
- pattern family and selected design pattern(s)
- code/source candidates
- proof requirements

If the repo has weak or missing design memory, create the no-reference packet
before coding and let it become the temporary design source for the task.

## Product DESIGN.md Requirements

Use `templates/product-DESIGN.md` when a repo lacks stable design memory.

The most useful sections are:

- product feeling in plain English
- audience and workflow density
- default no-reference `direction_id`
- brand bootstrap: voice, typography posture, icon family, surface rules,
  motion posture, imagery posture, and misuse rules
- state priority for the product type
- color roles
- typography rules
- spacing and layout rhythm
- surface/radius/shadow rules
- component patterns
- motion rules
- do/don't list
- proof expectations

For existing products, preserve the current brand direction. Do not replace a
repo's design system just because an external reference looks good.

## Taste Ledger

Use `templates/taste-ledger.md` when the user gives taste feedback or approves /
rejects a reference.

Capture:

- what the user liked
- what felt wrong
- where the example should apply
- where it should not apply
- product-specific rule created from the feedback

This is how the system learns the user's taste over time.

## Visual Review Rubric

Use `templates/design-review-rubric.md` before saying meaningful UI work is
done. Review:

- structure and information hierarchy
- spacing and alignment
- typography
- colors and contrast
- surfaces and depth
- interaction states
- motion restraint
- mobile behavior
- product truth
- accessibility basics

Reference-led work fails review if the screen does not materially match the
reference. No-reference work fails review if it looks generic, template-like, or
less polished than a competent human-designed product surface for the category.

If screenshots are impossible, say why and name the smallest proof still
available. Do not call visual polish done from code inspection alone.

Use Browser Harness when the repo supports it: screenshot assertions can stabilize
animations, mask dynamic elements, compare full-page screenshots, and set pixel
diff tolerance. Use Storybook when component states need isolated review:
default, hover/focus, loading, empty, error, success, dense, and mobile states.

## Implementation Rules

- Use the target repo's existing components and tokens first.
- Use `vibe-design-reference-libraries` for inspiration and code-pattern
  selection, not blind copying.
- Use `references/source-index-2026-05-18.md` when choosing outside GitHub or
  web sources for a new build.
- Use `references/pro-design-resource-library-2026-05-18.md` when the build
  needs design education, UX behavior guidance, free UI blocks, icons,
  typography, color tools, animation assets, product inspiration, charts/maps,
  AI UI sources, or proof tooling.
- Use `references/design-doctrine-and-qa.md` to check hierarchy, state design,
  accessibility, tokens, motion, mobile behavior, and anti-generic risks.
- Use `references/additive-github-source-lanes-2026-05-18.md` when the build
  needs stronger animation, AI/agent, dashboard, commerce, editor, calendar,
  canvas, upload, or map source candidates.
- Use `references/no-reference-art-direction-catalog.md` and
  `references/source-recipes-by-product-and-direction.md` when no visual
  reference is supplied.
- Use `references/state-coverage-matrix.md` to choose states before coding.
- Use `references/screenshot-repair-playbook.md` after screenshots to decide
  what to patch first.
- Use `references/github-code-safety-checklist.md` before copying public code.
- With no reference, still choose a concrete design direction before coding.
- With a reference, implement and iterate until the screen actually matches the
  reference at desktop and mobile sizes.
- Prefer owned/open code patterns over opaque UI packages.
- Check provenance and safety before copying third-party production code.
- Avoid fake metrics, fake testimonials, fake logos, and unsupported proof.
- Keep operational dashboards calm and dense; reserve high-motion effects for
  public or memorable moments.
- Use reduced-motion behavior for animated UI.
- Capture desktop and mobile screenshots for visible work.
- For complex flows, capture enough screens to prove the workflow, not just the
  first viewport.

## Output Contract

When this skill is used, return or implement:

- the filled reference packet, or the path where it was saved
- the no-reference design packet, when no visual reference exists
- selected references and why they fit
- exact implementation plan
- source lane and code-pull plan
- screenshots/proof required before done
- mismatch review after implementation
- final proof artifact paths and remaining mismatches/blockers
