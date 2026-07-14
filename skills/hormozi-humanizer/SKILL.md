---
name: hormozi-humanizer
description: AI memo humanizer and corporate slop cleanup for plain-English content, copy, posts, client emails, founder notes, and business writing. Use when a draft sounds AI-written, uses generic transition words, bold-colon bullet spam, neat-bow conclusions, or phrases like delve, unpack, underscores, synergies, leverage our learnings, holistic approach, and ever-changing landscape.
---

# Hormozi Humanizer

Use this as an anti-slop writing pass. The goal is not to make text casual. The
goal is to recover the author's actual point and say it in words a real person
would use.

## Load

Read `references/ai-memo-patterns.md` when the draft is longer than a short
reply, or when the user asks for a memo, post, essay, client note, or rewrite.

If another writing skill already has a voice profile loaded, preserve that
voice. This skill only removes AI tells and corporate fog.

## Required Workflow

1. Identify the raw thinking.
   - Prefer the user's bullets, dictated notes, transcript fragments, or rough
     claims over polished AI paragraphs.
   - If the draft hides the point, write the point in one plain sentence before
     rewriting.

2. Run the slop audit.
   - Scan for the patterns in `references/ai-memo-patterns.md`.
   - Mark any paragraph that sounds smart but cannot be summarized in plain
     English.
   - Treat generic transitions, corporate abstractions, and neat conclusions as
     evidence the draft is substituting language for thought.

3. Rewrite with the author's point intact.
   - Replace abstract claims with concrete cause and effect.
   - Replace "this signals" language with the actual observation.
   - Replace "we need a holistic approach" language with what will change.
   - Replace generic "learnings" with what worked, what did not, and what the
     author is doing next.

4. Read it aloud mentally.
   - If a sentence would not be said in a meeting or voice note, rewrite it.
   - If the paragraph still sounds like a consultant summary, make it plainer.
   - If a bullet is stronger than the rewritten paragraph, keep the bullet.

5. Return only the revised text unless the user asks for notes.
   - For review tasks, include a short "fixed" list.
   - For rewrite tasks, do not explain the anti-slop rules back to the reader.

## Rewrite Rules

- Say the point before decorating the point.
- Prefer "Customers are doing X, so we need to change Y" over "This signals a
  shift in customer behavior."
- Prefer "Here is what worked, here is what did not, here is what we are
  changing" over "leverage learnings and unlock synergies."
- Use ordinary transitions: `but`, `so`, `also`, `still`, `because`.
- Use bullets when they carry the thinking better than prose.
- Cut generic conclusions that could apply to any company.
- Do not add fake warmth, fake authority, fake vulnerability, or fake certainty.

## Output Check

Before sending, confirm internally:

- Every paragraph has a specific point.
- No paragraph survives only because it sounds polished.
- No banned phrase from the reference file remains unless it is quoted for
  critique.
- The rewrite preserves the user's real meaning instead of inventing a better
  one.
