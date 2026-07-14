# Vision Lock Template

Fill this to half a page. Five fields plus mode and freeze. This file is the
binding intent anchor for the whole build; downstream stages cite it and
`goal-post`'s verifier grades the finished build against it (the Matt-test),
not only against the plan's Definition Of Done.

Save the filled artifact to `docs/references/vision-lock.md`.

````markdown
---
vision_lock: "<build-slug>"
created_at: "<YYYY-MM-DD>"
canonical_repo: "<absolute repo path>"
canonical_branch: "<branch>"
mode: "build"        # map | plan | spec | scope | build
status: "draft"      # draft until Matt's explicit yes, then "frozen"
frozen_by: ""        # "Matt" once signed off
frozen_at: ""        # <YYYY-MM-DD> once signed off
---

# Vision Lock: <Build Title>

## Mode
<verbatim what Matt asked for>. If this is not "build", the deliverable is the
<map / plan / spec>, NOT code — do not implement until Matt says build.

## 1. Building (Matt's words)
One real end-to-end outcome, framed as a user living one real moment.
> "<the outcome in Matt's words>"

## 2. Matt-test (binding definition of done)
The 3-5 checks Matt will personally run. Each is product truth — a fresh real
launch, screenshot, click-through, or by-ear listen, against data the build did
NOT author. No "tests pass" / "typecheck green".
1. <what Matt does → what he sees / hears>
2. ...
3. ...

## 3. Design target
- Mode: <reference-led | no-reference>  (chosen via design-intelligence)
- Frozen packet: `<path to reference/no-reference packet saved in repo>`
- Proof required: desktop + mobile screenshots diffed against this packet.
- (`N/A` + reason if this build has no UI.)

## 4. Out of scope / anti-goals
- Not building: <item>
- Do NOT build it like: <negative example to avoid>
- Parked ideas live in: `docs/PARKED.md`

## 5. Reality snapshot
- Already exists — reuse, do NOT rebuild: <surface> — proof: `<file path>`
- Canonical repo + branch: `<repo>` @ `<branch>`
  (chosen over reachable alternatives: <other repos/branches or "none">)
- Leave untouched: <paths or N/A>

---
Frozen on Matt's yes. Downstream stages (deep-sweep, phase-plan, grill-me,
goal-post) treat this as immutable for the build. New facts → a dated amendment
line below with Matt's ok; never a silent overwrite.

### Amendments
- <YYYY-MM-DD>: <change> (approved by Matt)
````
