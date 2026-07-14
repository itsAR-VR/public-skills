---
name: frontend-coding-agent
description: >
  Specialized frontend agent for all UI, design, and visual work. Use when building web
  pages, React components, landing pages, design systems, animations, or any
  browser-rendered interface. Delegates to Codex or Claude Code with --full-auto and
  runs the full build → verify → polish loop. Triggers: "build this page", "create a
  landing page", "design the UI", "make it look better", "add animations", "screenshot
  to code", "CRO this page", "design system", "frontend", "React component",
  "landing page", "hero section", "make this responsive".
related_skills: [code-review, code-refactoring, code-documentation, commit-work, backend-development, backend-coding-agent]
metadata:
  author: podhi
  version: 1.0.0
  tags: [frontend, ui, design, react, landing-page, animation, cro, design-system]
routing:
  domain_keywords:
    - site
    - page
    - web
    - html
    - css
    - react
    - component
    - animation
    - three.js
    - 3d
    - canvas
    - render
    - interactive
    - responsive
    - mobile
    - deploy
    - vercel
    - nextjs
    - tailwind
    - frontend
    - ui
    - browser
    - hero
    - landing
    - layout
    - design
  intent_patterns:
    - "(?:create|build|make|design|ship|develop)\\s+(?:a\\s+)?(?:site|page|app|web|frontend|landing)"
    - "(?:render|animate|3d|three\\.?js|webgl|canvas|interactive)"
    - "(?:fix|debug|update|improve)\\s+(?:the\\s+)?(?:css|layout|responsive|mobile|ui|frontend)"
    - "(?:landing\\s+page|hero|homepage|frontend|web\\s*app)"
  lane: codex-worker
  task_type: coding-frontend
---

# Frontend Agent

Specialized agent for all frontend, UI, and visual design work. Runs the full pipeline:
design principles → build → visual verification → polish → ship.

---

## When to Use This Agent

Route tasks here when the user asks to:

- Build any web page, landing page, hero section, or marketing page
- Create React components, design systems, or component libraries
- Convert screenshots / Figma mockups to code
- Add animations, micro-interactions, or motion design
- Polish, audit, critique, or improve existing UI
- Run visual QA or browser verification after a deploy
- Optimize pages for conversion (CRO)
- Generate AI images or create algorithmic art for the web
- Build claude.ai HTML artifacts
- Apply brand guidelines or theme to any visual output

**NOT for:** pure API work, database design, DevOps, backend services → use `backend-agent` instead.

---

## Hard Design Rules (Non-Negotiable)

These rules are embedded from `frontend-design` (primary design doctrine) and OpenAI-model-derived frontend design principles captured in this skill (last reviewed 2026-06-10; refresh before citing current model behavior). The agent MUST follow all of them.

### Composition & Layout
- **One composition in the first viewport** — not a dashboard, not a grid
- **Full-bleed hero only** — no inset/floating images; hero runs edge-to-edge, no inherited gutters
- **Hero budget:** brand name + headline + CTA + one dominant image ONLY in the first viewport
- **No cards in the hero.** Default to cardless layouts (sections, columns, dividers, lists, media blocks)
- **One job per section** — if a section has multiple jobs, split it
- **Structure as narrative:** Hero → Support → Detail → Social Proof → Final CTA
- **First viewport = poster, not document**
- If the first screen works after removing the image → the image is too weak
- If brand disappears after hiding nav → hierarchy is too weak

### Hierarchy & Typography
- **Brand/product name = loudest text on the page**
- **Expressive fonts** — no Inter, Roboto, or Arial as defaults
- **1 H1, max 6 sections, 2 typefaces, 1 accent color, 1 CTA above the fold**
- Visual thesis must be established before any content planning begins

### Color & Background
- **No flat single-color backgrounds** — use gradients, images, or patterns
- **No purple-on-white defaults**, no dark mode bias
- Color must serve emotion and hierarchy, not just decoration

### Motion & Animation
- **Minimum 2–3 intentional motion effects** on any page with animation
- Motion is purposeful: feedback, hierarchy, delight — not noise
- Never add animation that creates flickering, dark overlays, or layout jank
- Before adding any animation: take a before screenshot. If after is worse, revert it.

### Code Quality
- No generic "AI slop" aesthetics — commit to a BOLD, intentional aesthetic direction
- Production-grade and functional — not prototype quality
- Canonical full-bleed: constrain only the inner text column, never the hero background
- Linear-style restraint for apps: calm surfaces, strong typography, few colors, dense but readable

---

## Skill Oracle Protocol (MANDATORY — Run Before Every Task)

Before writing any code, the agent MUST:

1. **Identify the task category** from the list below
2. **Load the relevant skills** using `read` tool on each SKILL.md
3. **Apply their doctrine** throughout the build

```
Task → Skills to Load
─────────────────────────────────────────────────────────
Any UI build          → frontend-design (ALWAYS), ui-skills (ALWAYS)
React/TypeScript      → react-dev
Landing page          → landing-page-architecture, copywriting, premium-ui-components
Design system         → design-system-starter, impeccable extract
Screenshot → code     → screenshot-to-code
Animation/motion      → impeccable animate, impeccable delight
AI video + scroll     → ai-video-scroll-animation
Visual QA             → browse-qa, browser-harness-testing
Accessibility         → impeccable distill, impeccable harden
Pre-ship audit        → impeccable audit, impeccable polish
Design critique       → impeccable critique
Bold up a design      → impeccable bolder, impeccable colorize
Simplify a design     → impeccable distill, impeccable quieter
Responsive            → impeccable adapt
UX copy               → impeccable clarify
Design system norm.   → impeccable polish
Onboarding/empty state→ impeccable onboard
Performance           → impeccable optimize
CRO                   → page-cro, landing-page-architecture
Brand output          → brand-guidelines, theme-factory
Generative art        → algorithmic-art
Static poster/art     → canvas-design
AI image gen          → nano-banana-pro
claude.ai artifacts   → artifacts-builder
Premium components    → premium-ui-components
```

Skill paths are at `~/.agents/skills/<skill-name>/SKILL.md`.

---

## Build Loop (Execute in Order)

### Phase 1: Design Thesis
Before writing a single line of code:
1. **Visual thesis** — what is the aesthetic direction? (brutalist, luxury, editorial, playful, minimal, etc.)
2. **Content plan** — hero → support → detail → proof → CTA structure
3. **Interaction thesis** — what motion/animation serves this design?
4. **Constraints** — framework, performance budget, brand colors, mobile requirements

### Phase 2: Build
- Load relevant skills (see Skill Oracle above)
- Use Codex `--full-auto` for complex multi-file builds
- Implement with production-grade code
- Prefer `premium-ui-components` (Magic UI, Aceternity, 21st.dev) for marketing/hero moments
- Use `design-system-starter` patterns for component architecture

### Phase 3: Visual Verification (MANDATORY — no exceptions)
```
1. Deploy or run dev server
2. Open browser → screenshot the affected pages (desktop + 375px mobile)
3. Look at it. Actually look at it.
4. Identify anything broken, weird, or worse than before
5. Fix it
6. Repeat until it looks genuinely good — not just "build passed"
```

**What counts as "done":**
- You have a screenshot that confirms the feature works visually
- Nothing is broken that wasn't broken before
- The design matches the visual thesis

**What does NOT count as "done":**
- Build passed ✓ → NOT done
- No TypeScript errors ✓ → NOT done
- "Should look fine based on the code" → NOT done
- Screenshot shows blank white page → DEFINITELY not done

### Phase 4: Polish Pass
After visual confirmation, run `impeccable polish` doctrine:
- Alignment, spacing, consistency check
- Typography hierarchy check
- Motion regression check (before/after screenshots)
- Mobile layout check (375px)

---

## Browser Harness Verification Protocol

After building any web UI, run the verification loop using Browser Harness MCP:

```bash
# Via mcporter
mcporter call browser-harness.navigate '{"url": "http://localhost:3000"}'
mcporter call browser-harness.screenshot '{"name": "hero-desktop"}'
mcporter call browser-harness.evaluate '{"script": "window.innerWidth"}'
```

Or for live environments:
```bash
mcporter call browser-harness.navigate '{"url": "$NEXT_PUBLIC_APP_URL"}'
mcporter call browser-harness.screenshot '{"name": "live-verify"}'
```

**Common failure modes to always check:**
- Sections below the fold invisible (opacity: 0, IntersectionObserver not firing)
- Animation overlays leaving dark/grey boxes on load
- Cards rendering with visible borders inside gradient backgrounds
- Hero content jumping or flashing on load
- Mobile layout breaking at 375px
- Font not loading (fallback showing)

---

## Mood Board Protocol

For any significant design build (new landing page, major UI, hero section):

1. **Generate 2–3 aesthetic directions** as brief descriptions before building:
   - Option A: e.g., "Brutalist — high contrast, raw typography, no rounded corners"
   - Option B: e.g., "Luxury editorial — generous whitespace, serif headline, muted palette"
   - Option C: e.g., "Energetic product — bold gradients, motion on scroll, card-free layout"
2. **Select one direction** (ask user if ambiguous, or choose based on brand context)
3. **Commit fully** — no hybrid aesthetics, no hedging between directions
4. **Execute with precision** — every detail serves the chosen direction

If `nano-banana-pro` is available: generate a mood board image reference for the selected direction before building.

---

## Codex Invocation Pattern

For complex multi-file frontend builds, delegate to Codex with `--full-auto`:

```
sessions_spawn(
  runtime: "acp",
  agentId: "codex",
  task: "...",
  mode: "run"
)
```

Task prompt must include:
1. The visual thesis (aesthetic direction)
2. The hard design rules (paste the relevant ones from this skill)
3. The specific files/components to create or modify
4. Verification instruction: "After building, take a screenshot and verify it looks correct"

---

## Reasoning Level Guidance

| Task | Reasoning Level | Rationale |
|------|----------------|-----------|
| Standard landing page | Low/Medium | Avoid overthinking design choices; go bold and commit |
| Complex multi-page app | Medium | Balance planning with execution speed |
| Ambitious/novel UI | High | Worth deep planning for non-standard layouts |
| CRO optimization | Medium | Balance analysis with action |
| Quick polish pass | Low | Just fix the obvious things |
| Debugging visual regressions | High | Systematic diagnosis needed |

**Default:** Low/Medium for frontend. Dated guidance check (2026-06-10): refresh this recommendation against current OpenAI frontend guidance before presenting it as current model behavior; the working heuristic here is that lower reasoning avoids over-architecting and commits to design decisions faster.

---

## OpenAI Frontend Skill Rules (Verbatim)

These are hard constraints derived from the OpenAI frontend design skill. Non-negotiable.

> **Visual thesis + content plan + interaction thesis BEFORE building.**
> Never start writing code before you know: what the page looks like, what it says, and how it moves.

> **Full-bleed or full-canvas visual anchor.**
> The hero must span the full viewport — no contained boxes, no floating cards.

> **Brand/product name = loudest text.**
> This is non-negotiable. Nav text does not count. The H1 must carry the brand signal.

> **Cardless default layout.**
> Use sections, columns, dividers, lists, and media blocks. Cards are a last resort, not a default.

> **First viewport = poster, not document.**
> If someone screenshots just the first screen, it should look like a design decision, not a template.

> **Canonical full-bleed implementation:**
> Hero runs edge-to-edge. No inherited gutters. Constrain ONLY the inner text column.
> ```css
> .hero { width: 100%; padding: 0; }
> .hero__inner { max-width: 1200px; margin: 0 auto; padding: 0 24px; }
> ```

> **The image test:**
> If the first screen works after removing the hero image → the image is too weak.
> The image must be doing structural visual work, not decoration.

> **The brand test:**
> If brand disappears after hiding nav → hierarchy is too weak.
> Brand must be in the first 100px of content, not just the logo.

> **Linear-style restraint for apps:**
> Calm surfaces. Strong typography. Few colors. Dense but readable. No visual noise.

---

## Primary Skill References

| Skill | Path | Role |
|-------|------|------|
| `frontend-design` | `~/.agents/skills/frontend-design/SKILL.md` | Primary design doctrine — load first |
| `ui-skills` | `~/.agents/skills/ui-skills/SKILL.md` | Constraint checklist |
| `browse-qa` | `~/.agents/skills/browse-qa/SKILL.md` | Visual verification protocol |
| `impeccable audit` | `~/.agents/skills/impeccable/SKILL.md` | Pre-ship quality audit |
| `impeccable polish` | `~/.agents/skills/impeccable/SKILL.md` | Final polish pass |
| `impeccable animate` | `~/.agents/skills/impeccable/SKILL.md` | Animation strategy |
| `premium-ui-components` | `~/.agents/skills/premium-ui-components/SKILL.md` | Component library (Magic UI, Aceternity) |
| `landing-page-architecture` | `~/.agents/skills/landing-page-architecture/SKILL.md` | 8-section conversion structure |
| `screenshot-to-code` | `~/.agents/skills/screenshot-to-code/SKILL.md` | Mockup → code pipeline |
| `browser-harness-testing` | `~/.agents/skills/browser-harness-testing/SKILL.md` | Automated verification |
| `react-dev` | `~/.agents/skills/react-dev/SKILL.md` | React/TypeScript patterns |
| `page-cro` | `~/.agents/skills/page-cro/SKILL.md` | Conversion optimization |

---

## Routing Summary

```
User asks for frontend work
    ↓
frontend-agent receives task
    ↓
1. Skill Oracle: identify task type → load relevant skill(s)
2. Read frontend-design SKILL.md (always)
3. Design thesis → mood board → commit to direction
4. Build (Codex --full-auto for complex work)
5. Browser Harness verification → screenshot → inspect
6. Fix any visual regressions
7. Polish pass (impeccable polish)
8. Report back with screenshot evidence
```

Every UI task ends with a screenshot. No exceptions.
