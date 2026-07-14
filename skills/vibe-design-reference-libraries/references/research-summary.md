# Vibe Design Reference Research Summary

Research date: 2026-05-15

Expanded source sweep: 2026-05-18. See
`../../reference-match-design-qa/references/source-index-2026-05-18.md` for the
broader GitHub/web source map covering 1,360 unique GitHub repositories,
shadcn registries, real-product UX galleries, dashboard/admin repos, motion
libraries, AI/agent interface sources, React Aria/Tailwind sources, design
systems, and visual proof tooling.

Universal pattern selector: see
`../../reference-match-design-qa/references/universal-code-backed-pattern-library.md`.
Use it to choose the build type and pattern family before choosing a visual
reference or code source.

Screenshot set: 10 reference screenshots saved locally by the original
researcher (not committed to the repo; treat as an out-of-band research
artifact).

This note captures the Instagram design tools the user collected and how to use them in future builds. The references are universal for product UI work; Chief is one important use case, not the only use case. Treat these as reference sources, not as a permission to copy visual design or code without checking license and fit.

## Tool Map

| Tool | Source | Best Use | Chief Use | Cautions |
| --- | --- | --- | --- | --- |
| Vibe Coder Blog | https://blog.vibecoder.me/ | Prompt literacy, tool reviews, learning paths, and design-to-code discipline. | Use to improve Chief design prompts and keep design work tied to shipping discipline. | Not a component library. Use as method guidance, not UI source. |
| Vibe Code Components | https://vibecodecomponents.com/ | Component prompt cards for interactions, forms, nav, heroes, CTAs, story, CSS, polish, and text. | Strong for Floating Chief, settings sheets, command palette, guided tours, toasts, tabs, and PWA-style prompts. | Validate generated code, browser APIs, and dependencies like cmdk/sonner before shipping. |
| Trickle Vibe Coding Prompt Library | https://trickle.so/blog/trickle-vibe-coding-prompt-library | 50 prompts across visual style, page functionality, interaction/UX, brand mood, and cross-media. | Use for Chief website art direction, cinematic product moments, onboarding mood, and cross-media launch surfaces. | Many prompts are intentionally broad; constrain them to Chief's route, user, and palette. |
| VibeUI | https://vibeui.online/ | 92 layout prompts across 15 categories like auth, pricing, bento, hero, stats, nav, dashboards, onboarding, and content. | Strong for Chief onboarding, dashboard shells, feature explanation, use-case selection, and admin/PROJECT layouts. | Prompt-first structural tool; it still needs product hierarchy and real content. |
| MotionSites | https://motionsites.ai/ | Premium motion-first hero and landing prompts, plus animated background ideas. | Use for Chief public site, launch page, product reveal, and high-polish demos. | Too much for dense app screens. Always add reduced-motion and performance checks. |
| Uilora | https://www.uilora.com/ | Web/mobile component inspiration for Next.js, React, React Native, Expo, TypeScript, Tailwind, Framer Motion, Radix, and shadcn-style stacks. | Useful for unifying Chief web and possible mobile surfaces with shared component thinking. | Check actual component source, license, and dependency fit before copying. |
| Forge UI | https://forgeui.in/ | React/Next/Tailwind/Motion/shadcn-oriented components built for speed, customization, and polished SaaS surfaces. | Useful for Chief forms, auth/onboarding, stats cards, security/trust surfaces, tabs, and notification panels. | Keep examples adapted to Chief content; avoid generic SaaS filler. |
| Uiverse | https://uiverse.io/ | Large open-source community gallery for buttons, loaders, forms, cards, tooltips, switches, hover effects, and CSS/Tailwind micro-polish. | Useful for small interaction upgrades when Chief needs one sharper control or loading state. | Community quality varies. Curate carefully and keep accessibility/focus states. |
| Animate UI | https://animate-ui.com/docs | Open animated component distribution based on React, Tailwind, Motion, and shadcn-style registry patterns. | Best app-safe motion source for Chief sheets, tabs, accordions, tooltips, sidebars, skeletons, buttons, and icons. | Match existing design tokens and avoid stacking animations on dense screens. |
| Vengeance UI | https://www.vengenceui.com/docs/components-overview | Dramatic components: animated hero, glow border cards, docks, perspective grids, 3D/liquid effects, animated text, and loaders. | Use sparingly for Chief launch surfaces, Floating Chief concept demos, and premium reveal moments. | High-motion patterns can overpower usability. Avoid dark/neon defaults unless explicitly adapted. |
| ReUI | https://reui.io/ | Large shadcn component/pattern source for production flows, data grids, filters, Kanban, file upload, and app states. | Strong for Chief dense work surfaces and operator dashboards. | Pull only needed components; adapt tokens, density, and state behavior. |
| registry.directory | https://registry.directory/ | Explorer for shadcn registries and component ecosystems. | Use to discover current code sources before guessing. | Some registries are affiliate/premium/unclear-license; verify before copying. |
| 21st.dev | https://21st.dev/ | Marketplace/discovery for shadcn-based React/Tailwind blocks, hooks, and design-engineering patterns. | Useful for Chief website, onboarding, and app components when stack-compatible. | Inspect provenance, dependency graph, and license before direct reuse. |
| Mobbin | https://mobbin.com/ | Real-world app screens, UI elements, and flows. | Strong for onboarding, settings, account setup, billing, checkout, and mobile/product flows. | Pattern reference only unless assets are explicitly exportable. |
| Nicelydone | https://nicelydone.club/ | Real SaaS app screens, components, and complete flows. | Strong for Chief SaaS workflow structure and reference links. | Use as UX evidence, not brand copying. |
| SaaSFrame | https://www.saasframe.io/ | SaaS website and product screen library by category, section, and pattern. | Strong for landing, pricing, dashboard, settings, product tour, onboarding, empty state, and table references. | Paid/export features may vary; respect access limits. |
| assistant-ui | https://www.assistant-ui.com/ | React assistant/chat UI library with conversation and composer patterns. | Strong for Chief/Jarvis chat shells, assistant threads, actions, and stateful workspaces. | MIT, but still adapt into the local product system. |
| AI Elements | https://elements.ai-sdk.dev/ | AI-native shadcn component registry for messages, tools, reasoning, and generative UI. | Strong for AI builders, streaming states, tool-call cards, and agent workflows. | Verify component-level provenance/license before direct reuse. |
| ElevenLabs UI | https://ui.elevenlabs.io/ | shadcn-based multimodal/voice agent component source. | Strong for voice/audio agent surfaces and live-state UI. | MIT; keep effects restrained in operational tools. |
| Manifest UI | https://ui.manifest.build/ | shadcn/ui library focused on ChatGPT Apps and MCP Apps. | Useful for MCP/app surfaces and embedded assistant tools. | Smaller source; use for pattern fit, not star count. |
| Motion Primitives | https://motion-primitives.com/ | Open-source animated React primitives. | Good for cleaner motion patterns when Magic UI/React Bits are too dramatic. | MIT; add reduced-motion behavior. |
| Motion / React Spring | https://motion.dev/ | UI animation engines for React and JavaScript. | Best for app-safe enter/exit, layout, gesture, state, and spring transitions. | Prefer for functional app motion before reaching for cinematic site tools. |
| GSAP / anime.js | https://gsap.com/ | Timeline-heavy animation engines for custom website motion. | Strong for landing pages, launch pages, scroll scenes, and complex hero motion. | GSAP license needs review; usually too heavy for routine app states. |
| Lottie / dotLottie / Rive | https://lottiefiles.github.io/dotlottie-web/ | Vector animation players and interactive animation runtime. | Strong for branded loading screens, empty states, onboarding illustrations, and voice/agent state moments. | Requires asset discipline; avoid random stock animations. |
| tsParticles / canvas-confetti / Number Flow | https://particles.js.org/ | Small focused effects for backgrounds, success moments, and animated numbers. | Useful for rare completion celebrations, counters, and meaningful particles/fireworks. | Easy to overuse; avoid generic confetti or particles in serious workflows. |
| Intent UI / Untitled UI React / Jolly UI | https://intentui.com/ | React Aria/Tailwind copy-paste component systems. | Useful when accessibility and component state quality matter more than shadcn defaults. | Check local stack fit and avoid importing a whole new visual identity. |

## Practical Selection Rules

- **Need any new app, site, tool, dashboard, agent workspace, editor, calendar,
  checkout, or future product surface**: start with the universal code-backed
  pattern library, choose the primary pattern family, then select sources below.
- **Need a better prompt for an AI builder**: start with VibeUI, Vibe Code Components, or Trickle.
- **Need a production-style React component pattern**: start with Animate UI, Forge UI, Uilora, or shadcn/ui-compatible sources.
- **Need tiny polish**: start with Uiverse for one micro-component, then rewrite to local standards.
- **Need a cinematic hero**: start with MotionSites, Trickle cross-media prompts, or Vengeance UI.
- **Need a dashboard or operator screen**: start with VibeUI structural prompts, then implement calmly with local components.
- **Need Chief/Floating Chief motion**: prefer Animate UI and Motion for predictable app-safe animation; use Vengeance UI only for special moments.
- **Need loading screens or animated states**: start with Motion/Animate UI for app states, Lottie/dotLottie/Rive for branded vector motion, and only use confetti/particles for rare meaningful success moments.
- **Need high-end website motion**: start with MotionSites, GSAP/anime.js, React Bits, Magic UI, or Vengeance UI, then verify performance and reduced-motion behavior.

## Universal Build Adaptation

- For any build, start with the product type, primary user, workflow density, and stack before choosing references.
- Chief is one product-specific application of this research, not the default
  for every build. Use the target product's own brand/design memory when it
  exists.
- Use the bundled code assets in `assets/react-tailwind-shadcn/` when the repo needs a practical starting point rather than another prompt.
- Treat outside galleries as idea sources. Treat the bundled assets as safer first-pass code because they are original, small, and designed to be rewritten into the target repo.
- For React/Tailwind/shadcn-style apps, prefer local open code over opaque npm UI packages.
- For Motion-heavy work, use motion to clarify state changes, not to decorate every surface.

## Product-Specific Design Adaptation

For every product, load or create its product-specific design contract before
styling. Chief guidance below applies only when the target is Chief.

### Chief

Chief should feel like one branded system across the app, Floating Chief, website, onboarding, docs, decks, and public materials.

- Palette: lavender, greys, whites, creams, and blacks.
- App feel: calm, capable, premium, work-focused, and proof-oriented.
- Website feel: elevated and memorable, but still literal about the Chief product.
- Floating Chief feel: quick, context-aware, low-friction, and accessible.
- Avoid: generic dark AI dashboard, neon purple/blue overuse, fake metrics, fake testimonials, decorative motion without product meaning.

## Future Prompt Template

Use this when asking Codex or Claude to apply the research:

```text
Use the vibe-design-reference-libraries skill.

Target: [route, screen, flow, or component]
Product role: [SaaS app / internal tool / AI workspace / ecommerce / calendar / editor / canvas / Chief app / other]
Pattern family: choose from universal-code-backed-pattern-library.md.
Brand rules: [target product brand and density rules, or create a no-reference packet if missing]
References: pick max 3 from VibeUI, Vibe Code Components, Trickle, MotionSites, Uilora, Forge UI, Uiverse, Animate UI, Vengeance UI.
Code: if useful, adapt patterns from assets/react-tailwind-shadcn/.
Return: art direction, component plan, prompt copy if useful, dependencies, license risks, accessibility/performance risks, and verification steps before editing.
```

## Implementation Notes

- Check the current repo stack before using any library or CLI.
- Prefer copying local component source only when the license and provenance are clear.
- If using shadcn-style components, preserve the local design system and file placement.
- If using Motion, animate transform/opacity/layout intentfully and include reduced-motion behavior.
- Use browser screenshots for desktop and mobile before reporting visible UI work as complete.

## Sources Checked

- https://blog.vibecoder.me/
- https://vibecodecomponents.com/
- https://trickle.so/blog/trickle-vibe-coding-prompt-library
- https://vibeui.online/
- https://motionsites.ai/
- https://www.uilora.com/
- https://forgeui.in/
- https://uiverse.io/
- https://animate-ui.com/docs
- https://www.vengenceui.com/docs/components-overview
- https://ui.shadcn.com/docs
- https://motion.dev/docs
- https://registry.directory/
- https://reui.io/
- https://www.shadcnblocks.com/
- https://21st.dev/
- https://www.assistant-ui.com/
- https://elements.ai-sdk.dev/
- https://ui.elevenlabs.io/
- https://ui.manifest.build/
- https://motion-primitives.com/
- https://motion.dev/
- https://www.react-spring.dev/
- https://gsap.com/
- https://animejs.com/
- https://github.com/airbnb/lottie-web
- https://lottiefiles.github.io/dotlottie-web/
- https://rive.app/
- https://particles.js.org/
- https://catdad.github.io/canvas-confetti/
- https://number-flow.barvian.me/
- https://intentui.com/
- https://www.untitledui.com/react/
- https://jollyui.dev/
- https://mobbin.com/
- https://nicelydone.club/
- https://www.saasframe.io/
