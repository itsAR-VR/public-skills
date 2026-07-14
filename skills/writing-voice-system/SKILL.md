---
name: writing-voice-system
description: Profile-driven writing voice system for rewriting first-person content, copy, founder notes, essays, posts, client emails, newsletters, and human-facing prose. Use when a user wants text in a specific person's voice, wants Mo's voice via the mo profile, says a draft sounds like AI, asks to humanize writing, or when another writing skill needs a reusable voice layer before final cleanup.
---

# Writing Voice System

This is the canonical voice layer for human writing. It generalizes the old
`mo-writing-voice-system` while keeping Mo as the first supported profile.

Use it before a final humanizer pass when the assignment needs a specific
person's voice, not just cleaner prose.

## Profiles

### `mo`

Use the Mo profile when:

- The user asks for Mo's voice.
- A legacy skill invokes `mo-writing-voice-system`.
- The piece is first-person founder writing and no other profile is specified.

Load:

- `references/mo-style-guide.md`
- `references/banned-patterns.md`
- `assets/mo-voice-primer-prompt.md`
- `assets/revision-checklist.md`

Future profiles should follow the same shape: one style guide, one banned list
if needed, one primer, and one revision checklist. Do not create a new skill
for every person unless the workflow itself changes.
If a requested voice has no profile, build one from an explicit user-provided
corpus using that shape; if no corpus is available, decline the voice match and
offer neutral cleanup instead.

## Pipeline

1. Determine the content type, audience, sender, and goal.
2. Select the profile. Default to `mo` only for Mo-attributed or legacy calls.
3. Load the profile files listed above.
4. Draft or rewrite using the selected profile.
5. Run the profile banned-pattern sweep.
5b. Run the `stop-slop` structural sweep using
   `skills/stop-slop/references/phrases.md` and
   `skills/stop-slop/references/structures.md`. Catch throat-clearing openers,
   false agency, narrator-from-a-distance, rhetorical setups, negative listing,
   dramatic fragmentation, vague declaratives, and Wh- sentence starters that
   the profile banned-pattern list does not cover. Treat stop-slop's adverb
   ban and three-item-list rule as guidelines, not absolutes, when the active
   profile's rhythm calls for them (the Mo profile in particular uses some
   adverbs and rule-of-three cadence on purpose).
6. Run the rhythm pass in `assets/revision-checklist.md`.
7. Run `hormozi-humanizer` for memos, posts, essays, client notes, newsletters,
   and any draft that still sounds like AI or corporate writing.
8. For Mo-attributed internal feedback and communications, run
   `mo-book-how-to-win-friends-digital-age` as the relationship-language final
   pass. Use it when the draft involves team feedback, disagreement,
   delegation, resistance, correction, or leadership alignment. Keep Mo's
   direct voice, but reduce avoidable defensiveness by preserving autonomy,
   naming the shared outcome, and asking ownership-preserving questions.
9. Score the draft on the five-dimension rubric in
   `assets/revision-checklist.md` (Directness, Rhythm, Trust, Authenticity,
   Density). Revise if the total is under 35 of 50.
10. Score voice confidence from 1 to 5.
11. If the voice confidence score is below 4 or the rubric total is under 35
    of 50, revise once before returning.
    If it still fails, do not call it voice-matched: name the failed gate, ask
    for more corpus when voice confidence failed, or return neutral cleanup.

## Integration Contract

Writing skills should call this skill as the voice layer, then call their own
format-specific logic. Examples:

- `writers-studio`: AR voice first, this system only when a named non-AR voice
  is requested.
- `copy-editing`: preserve the existing voice, but use this system if the edit
  asks for a named sender.
- `writing-clearly-and-concisely`: use this after clarity edits when the text
  has to sound like a specific person.
- `stop-slop`: structural AI-tell sweep called from this pipeline (step 5b).
  Catches false agency, throat-clearing openers, rhetorical setups, and
  narrator-from-a-distance patterns the profile banned-pattern list does not
  cover. Can also be called standalone for non-voice prose work.
- `hormozi-humanizer`: final anti-slop pass for AI-shaped business writing.
- `mo-book-how-to-win-friends-digital-age`: final relationship-language pass
  for Mo-attributed internal feedback and communications. Use after the Mo
  voice and humanizer passes when the message could create defensiveness,
  argument, shame, ambiguity, or resistance.

## Drafting Rules

- Preserve the author's real point, even when the grammar is rough.
- Do not invent authority, numbers, personal details, or emotional certainty.
- Keep the intelligence in the observation, not in inflated vocabulary.
- Prefer commas, colons, and periods over em dashes.
- If a sentence does not sound speakable aloud, rewrite it.
- If a raw bullet carries the thought better than the paragraph, keep the
  bullet.

## Output Checks

Before returning, check the draft against these observable criteria. Structural
checks cover setup, banned sweeps, required passes, and rubric threshold;
behavioral checks cover voice confidence and sender fit:

- The selected profile is named.
- The draft has no profile banned-pattern violations.
- The `stop-slop` structural sweep ran.
- The Hormozi Humanizer pass ran when the content type calls for it.
- The five-dimension rubric total is at least 35 of 50.
- The final voice confidence score is 4 or 5.
- The result sounds like the sender, not like a generic humanized AI draft.
- For Mo-attributed internal feedback or communications, the Carnegie
  relationship-language pass ran or was explicitly unnecessary because the
  draft had no feedback, disagreement, delegation, correction, or alignment
  risk.
