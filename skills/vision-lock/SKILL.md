---
name: vision-lock
description: >
  Freeze exactly what Matt wants — in his words, with his sign-off — into one
  half-page artifact BEFORE research or planning starts. Use at the very front
  of a build (before deep-sweep / phase-plan), or when Matt says "lock the
  vision", "vision lock", "what are we actually building", "freeze the intent",
  "build contract", "before we plan", or kicks off any non-trivial build.
  Produces docs/references/vision-lock.md: the outcome in Matt's words, the
  Matt-test (3-5 product-truth checks), a frozen design target, explicit
  out-of-scope, and a reality snapshot of what already exists. This file becomes
  the truth anchor that deep-sweep researches around, phase-plan decomposes
  toward, grill-me writes its resolved decisions into, and goal-post's verifier
  grades the finished build against — so the build comes out as envisioned, not
  just internally consistent.
related_skills:
  - grill-me
  - deep-sweep
  - phase-plan
  - goal-post
  - idea-to-build-intake
  - design-intelligence
  - reference-match-design-qa
---

# Vision Lock

The first stage of a build. Its only job: freeze, in Matt's own words and with
his explicit sign-off, the answer to "what exactly are we building and how will
we know it's right" — into ONE half-page file the rest of the pipeline obeys.

Why this exists: `deep-sweep` researches the *how* and `phase-plan` decomposes
it, but both assume the *what* is already clear (`deep-sweep` literally extracts
the problem set from the conversation; `phase-plan` only preserves the request
verbatim — which is the ambiguous thing). `grill-me` resolves ambiguity but
writes nothing to disk. So intent has been living only in volatile conversation,
and builds drift: a read-only context brain became an enterprise app; "open the
app and talk to it" became 55 phases of vanity features; a calm founder cockpit
became a dense ops console. Vision Lock makes intent a durable, checkable
artifact and the binding contract for everything downstream.

## Pipeline position

intake → **[vision-lock — FREEZE + Matt sign-off]** → deep-sweep → phase-plan →
grill-me (writes resolved decisions back here) → goal-post → `/goal` run.

This operationalizes Matt's standing Build Contract rule
(`~/.claude/rules/build-verification.md` §1) as a real pipeline stage instead of
a passive note that gets skipped under build momentum.

## How to run it

1. **Inspect before asking.** Check the repo, memory, and existing planning docs
   FIRST. Most answers — what already exists, the canonical repo, prior
   decisions — are discoverable locally. Never ask Matt what you can read.
   (Inherits `grill-me`'s core instinct.)
2. **Ask one question at a time, with a recommended answer.** Propose-and-proceed
   for a non-technical owner: state your best-guess answer so Matt can say "yes"
   or correct it, rather than facing an open-ended blank.
3. **Resolve the five fields** (below). Keep it to a half page — this is a
   contract, not a PRD. No plan theater, no phase docs.
4. **Write `docs/references/vision-lock.md`** from
   `references/vision-lock-template.md`.
5. **Get the explicit freeze.** Show Matt the half page and ask for a yes. On
   "yes", stamp it `frozen`. Nothing downstream proceeds until it is frozen.

## Mode lock (first line of the contract)

Record verbatim what Matt asked for: map / plan / spec / scope / build. If the
mode is anything other than `build`, the deliverable is the artifact (map, plan,
or spec) — NOT code. Do not write implementation until Matt explicitly says
build. This closes the most-repeated drift seam: treating "map/plan/spec" as
permission to start coding.

## The five fields (the whole contract)

1. **Building** — the one real outcome in Matt's words. The smallest version
   that is genuinely the thing he wants, framed as a user living one real
   end-to-end moment ("open the app, ask for my brief, get a real brief"), not a
   feature list.
2. **Matt-test** — the 3-5 checks Matt will personally run to call it done. Each
   MUST be a product-truth check (a fresh real-app launch, a screenshot, a
   click-through, a by-ear listen) against data the build did not author — never
   "tests pass" or "typecheck green". Matt is not QA; these are what HE will see.
3. **Design target** — for any UI, the frozen look. Route through
   `design-intelligence` to choose reference-led vs no-reference, then save the
   packet (via `reference-match-design-qa`) as a repo file and link it here. No
   UI code starts before this is set. Mark `N/A` + reason for non-UI builds.
4. **Out of scope / anti-goals** — what we are explicitly NOT building, plus
   "do NOT build it like this" negative examples. Mid-build ideas get parked
   here or in `docs/PARKED.md`, never absorbed into the frozen build.
5. **Reality snapshot** — what already EXISTS and where (so reuse is not rebuilt
   as net-new), and the ONE canonical repo + branch this build targets (chosen
   explicitly when several are reachable). Cite proof (a file path) for each
   "already exists" claim — never assumption.

## Handoff

Report the frozen `docs/references/vision-lock.md` path and recommend
`deep-sweep` next (or `phase-plan` for smaller builds). `deep-sweep`,
`phase-plan`, and `goal-post` all cite this file as the binding intent anchor;
`goal-post` pins it as `## Frozen Original Intent` and its verifier grades the
finished build against the Matt-test, not just the plan's Definition Of Done.

## Anti-patterns

- Do not expand into a multi-page PRD or generate phase docs — half a page, five
  fields, frozen. If Matt wants heavy requirements, that is a different skill.
- Do not start research, planning, or code before the file is frozen on Matt's
  yes.
- Do not write "tests pass" or "build green" as a Matt-test item — those are not
  product truth.
- Do not ask Matt what the repo can answer; inspect first.
- Do not let later stages silently edit the frozen intent. New facts go to a
  dated amendment line with Matt's ok, never a quiet overwrite.
- Do not frame reuse work as a net-new build; the reality snapshot exists to
  catch "most of this already exists".
