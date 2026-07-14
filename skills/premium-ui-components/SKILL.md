---
name: premium-ui-components
description: >
  Use when the user wants to enhance UI with premium animated or polished components.
  Triggers: "component library", "magic ui", "aceternity", "21st.dev",
  "animated components", "premium UI", "fancy components", "upgrade the UI",
  "make it look better", "add animations", "landing page components",
  "fancy buttons", "background effects", "text animation", "hero section components".
  All three libraries are MIT-licensed, shadcn/ui-compatible, React + Tailwind + Framer Motion.
related_skills:
  - ui-skills
  - mui
  - react-dev
  - artifacts-builder
  - design-system-starter
  - ecc-frontend-design
routing:
  domain_keywords:
    - animation
    - transition
    - motion
    - glassmorphism
    - gradient
    - particle
    - parallax
    - scroll
    - hover
    - micro-interaction
    - effect
    - shimmer
    - glow
  intent_patterns:
    - "(?:add|create|build)\\s+(?:a\\s+)?(?:premium|animated|fancy|polished|glassmorphic)\\s+(?:component|ui|effect|animation)"
    - "(?:animation|transition|motion|particle|parallax|scroll)\\s+(?:effect|component)"
  lane: codex-worker
  task_type: coding-frontend
---

# Premium UI Component Libraries

## When to Use This Skill vs Coding from Scratch

**Use these libraries when:**
- Building landing pages, marketing sites, or product showcases
- A visual moment needs to feel premium (hero, CTA, testimonials, stats)
- The request is "make it look like [X SaaS product]" or "add some polish"
- You need a specific effect (typewriter, shimmer, parallax, 3D card, aurora)

**Code from scratch when:**
- It's a utility UI (forms, tables, CRUD, dashboards) — animation is noise here
- The design system has strict brand constraints these components would fight
- The effect is simple enough that a Tailwind class or CSS keyframe is 10 lines
- Framer Motion isn't in the project and adding it isn't justified

**Rule of thumb:** If the component serves a *marketing/impression* purpose, reach for the libraries. If it serves a *functional/workflow* purpose, keep it simple.

---

## Library Routing Rules

| Rule | Library | When |
|------|---------|------|
| 1 | **Magic UI** | Animated marketing/landing page elements, text effects, animated buttons, pattern backgrounds |
| 2 | **Aceternity UI** | Hero sections, dramatic backgrounds, 3D effects, interactive product showcases, scroll-driven experiences |
| 3 | **21st.dev** | Utility blocks, navigation, forms, hooks, structured layouts, pricing tables, anything functional-but-styled |
| 4 | All three | shadcn/ui and React/Tailwind compatible — safe to mix across a page, not within a single section |

---

## Install Patterns

### Magic UI

```bash
npx shadcn@latest add "https://magicui.design/r/<component-slug>"
# Component slug = lowercase-hyphenated component name
# AnimatedBeam → animated-beam
# NeonGradientCard → neon-gradient-card
# ShimmerButton → shimmer-button

# Examples:
npx shadcn@latest add "https://magicui.design/r/marquee"
npx shadcn@latest add "https://magicui.design/r/number-ticker"
npx shadcn@latest add "https://magicui.design/r/shimmer-button"
npx shadcn@latest add "https://magicui.design/r/animated-beam"
npx shadcn@latest add "https://magicui.design/r/typing-animation"
```

Components land in `components/magicui/`. Import from `@/components/magicui/<name>`.

### Aceternity UI

```bash
npx shadcn@latest add "https://ui.aceternity.com/registry/<component-slug>.json"
# Or copy-paste from ui.aceternity.com for components not in registry

# Examples:
npx shadcn@latest add "https://ui.aceternity.com/registry/aurora-background.json"
npx shadcn@latest add "https://ui.aceternity.com/registry/background-beams.json"
npx shadcn@latest add "https://ui.aceternity.com/registry/animated-testimonials.json"
npx shadcn@latest add "https://ui.aceternity.com/registry/macbook-scroll.json"
npx shadcn@latest add "https://ui.aceternity.com/registry/3d-card.json"
```

Requires `framer-motion tailwind-merge clsx` — ensure these are installed.

### 21st.dev

```bash
npx shadcn@latest add "https://21st.dev/r/<author>/<component-name>"
# Browse 21st.dev to find the exact CLI command shown on each component page

# General pattern:
npx shadcn@latest add "https://21st.dev/r/<username>/<component-slug>"
```

Community library — review source before using in production.

---

## Quick Component Lookup by Use Case

### Hero Sections
- **AuroraBackground** (Aceternity) — aurora gradient bg
- **BackgroundBeams** (Aceternity) — beam grid bg
- **BackgroundGradientAnimation** (Aceternity) — animated gradient mesh
- **HeroSections** (Aceternity) — pre-built hero layouts
- **MacbookScroll** (Aceternity) — scroll-triggered screen reveal
- **RetroGrid** (Magic UI) — perspective grid floor
- **Globe** (Magic UI) — 3D interactive globe
- **Particles** (Magic UI) — floating particle field

### Text Effects
- **TypingAnimation** (Magic UI) — typewriter
- **HyperText** (Magic UI) — scramble/decode on hover
- **WordFadeIn / WordPullUp / WordRotate** (Magic UI) — word entrance anims
- **SparklesText** (Magic UI) — sparkle particles on text
- **NumberTicker** (Magic UI) — count-up animation
- **AnimatedShinyText** (Magic UI) — shimmer sweep
- **BlurIn** (Magic UI) — blur-to-sharp entrance
- **ColourfulText** (Aceternity) — multi-color animated text
- **EncryptedText** (Aceternity) — matrix-style decode

### Cards
- **MagicCard** (Magic UI) — spotlight hover
- **NeonGradientCard** (Magic UI) — neon border
- **ShineBorder / BorderBeam** (Magic UI) — animated border
- **BounceCards** (Magic UI) — stacked deck
- **3D Card Effect** (Aceternity) — mouse-track 3D tilt
- **CardSpotlight** (Aceternity) — spotlight follows mouse
- **ExpandableCards** (Aceternity) — click to expand
- **FocusCards** (Aceternity) — blur surrounding cards

### Backgrounds & Textures
- **DotPattern / GridPattern** (Magic UI) — SVG patterns
- **AnimatedGridPattern** (Magic UI) — animated highlighted grid
- **MeteorShower / Meteors** (Magic UI) — falling meteors
- **BackgroundBeamsWithCollision** (Aceternity) — colliding beams
- **BackgroundLines / BackgroundRippleEffect** (Aceternity)
- **NoiseBackground** (Aceternity) — grain texture
- **AuroraBackground** (Aceternity) — flowing aurora

### Buttons & CTAs
- **ShimmerButton** (Magic UI) — shimmer sweep CTA
- **RainbowButton** (Magic UI) — rotating rainbow gradient
- **PulsatingButton** (Magic UI) — pulsing ring
- **StatefulButton** (Aceternity) — loading/success/error states

### Navigation
- **FloatingDock** (Aceternity) — macOS-style dock
- **ResizableNavbar** (Aceternity) — shrinks on scroll
- **Dock** (Magic UI) — magnifying dock
- **21st.dev** — search "navbar", "sidebar", "breadcrumb" for utility nav

### Testimonials & Social Proof
- **AnimatedTestimonials** (Aceternity) — cycling testimonials
- **Tweet Card** (Magic UI) — tweet-style card
- **Marquee** (Magic UI) — scrolling review/logo strip
- **AppleCardsCarousel** (Aceternity) — full-bleed card carousel

### Interactive / Microinteractions
- **AnimatedBeam** (Magic UI) — connection beam between elements
- **Orbiting Circles** (Magic UI) — orbiting ring
- **CoolMode / Confetti** (Magic UI) — click bursts
- **TracingBeam** (Aceternity) — scroll reading beam
- **PointerHighlight** (Aceternity) — highlight follows cursor
- **Compare** (Aceternity) — before/after comparison

### Loaders & States
- **Ripple** (Magic UI) — expanding rings
- **Loader** (Aceternity) — animated loaders
- **StatefulButton** (Aceternity) — inline state transitions

### Landing Page Blocks (Complete Sections)
- **BentoGrid** (Magic UI) — feature highlight grid
- **Marquee** (Magic UI) — logo strip / review scroll
- **AppleCardsCarousel** (Aceternity) — featured content
- **3D Marquee** (Aceternity) — 3D tilted scroll
- **HeroSections** (Aceternity) — full hero blocks
- **21st.dev** — pricing tables, FAQ, footer, feature grids

---

## Adapter Pattern: Integrating a Component into an Existing Project

When you pull a component from any of these registries into an existing React project:

### Step 1: Check dependencies

```bash
# These are required by most components
npm list framer-motion tailwind-merge clsx
# Install if missing:
npm install framer-motion tailwind-merge clsx
```

### Step 2: Install via CLI

```bash
npx shadcn@latest add "<registry-url>"
```

If the CLI fails (registry URL format issues), fall back to manual:
1. Open the component page
2. Copy the source code
3. Create `components/<library>/<ComponentName>.tsx`
4. Paste source, fix any missing imports

### Step 3: Wire up Tailwind config

Some components add custom animations to `tailwind.config.ts`. Check the component's docs or look for injected config entries. If the CLI handled install, it usually patches the config automatically.

### Step 4: Use the component

```tsx
import { MagicCard } from "@/components/magicui/magic-card";
import { AuroraBackground } from "@/components/aceternity/aurora-background";

// Wrap your content:
<AuroraBackground>
  <div className="relative z-10">
    <MagicCard>...</MagicCard>
  </div>
</AuroraBackground>
```

**z-index pattern:** Background components sit at `z-0`. Content wrapper must be `relative z-10`.

### Step 5: Customize

These components are source files you own. Edit colors, timing, sizes directly in the component file. Don't fight props that don't exist — just edit the source.

---

## Animation Discipline Rules

**One animated element per section.** A hero section gets one primary motion treatment (background + headline animation = one system, not two separate competing systems).

**Animation must serve a purpose:**
- Directing attention → OK
- Communicating state → OK
- Demonstrating product capability → OK
- "It looks cool" alone → NOT OK

**Never stack these:**
- Two background animations in the same section
- Multiple text scramble/flip effects in the same viewport
- Marquee + Orbiting Circles + AnimatedBeam together without clear visual hierarchy

**Mobile check required:** Run `3D Card Effect`, `Globe`, `MacbookScroll`, and parallax components on a real device or emulator before shipping. GPU-intensive effects degrade badly on mid-range phones.

**`prefers-reduced-motion` check:** Magic UI handles this well. Aceternity components vary. Before shipping, add:
```tsx
const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
```
...and conditionally disable the animation.

---
