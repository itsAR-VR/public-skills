---
name: explain-simply
description: >
  Explain what YOU just did in dead-simple, jargon-free language — the whole arc:
  big picture, the key decision, how it works, the steps, the assumptions, the
  decisions, and what's next. The inverse of feynman (here you teach the user,
  not the reverse). Trigger when the user says "walk me through that simply",
  "explain simply", "in plain English", "ELI5 / ELI12", "dumb it down", "/simply",
  or wants a no-jargon recap of your work, a decision, or a design.
---

# Explain Simply

The Feynman test: if you can't say it simply, you don't understand it. Explaining your own work plainly is the proof. Audience = a smart 12-year-old.

## The one rule

**Translate everything. Zero jargon survives.** If a word needs the field to understand it, replace it or define it in the same breath. No exceptions.

## Cover the arc, in this order

1. **One breath** — what it is / what you did, in a sentence. No setup, no "great question".
2. **The fork** — the single decision that shaped everything, and why you went that way.
3. **How it works** — the mechanism, carried by one analogy.
4. **The steps** — what you actually did, numbered, one line each.
5. **Assumptions** — what you took for granted, so they can challenge it.
6. **Decisions** — each call + a one-line "why".
7. **Next** — what's left, framed as their choices.

## Make it land

- **Open with one analogy for the whole thing** (radar, plumbing, a bouncer). One good metaphor beats five sentences.
- **Concrete beats vague.** "you'd net $73" > "it's profitable". Use real names and numbers.
- **One idea per step.** Don't jump A→C; show B.
- **Short sections, short lines.** Scannable, not a wall.

## Be honest

- Name the one spot you're least sure landed: *"the part I'd lose a 12-year-old on is X — want that one slower?"*
- If a step was messy, say it was messy. Don't fake clarity.
- "Very simply" means **cut, not cram.** Leave things out on purpose.
- Never claim done-ness you didn't verify.

## Don't

- No preamble, no jargon, no lecturing concepts they didn't ask about.

## Example shape

> **What it is:** a deal scanner for resellers — it pings you when a hot product is cheap enough to flip for profit. It's the radar; you're the fisherman.
> **The fork:** the brief wanted an auto-buying bot — that's illegal, so we built the legal "tell-you-when-to-buy" version instead.
> **How it works:** watches prices → does the profit math → ranks by money → alerts you.
> **Steps:** 1) checked it against the brief 2) wired the data feeds 3) made it track any product…
> **Assumptions:** stay on the legal side; don't touch your passwords/payments.
> **Decisions:** radar not bot — the bot would've killed the business.
> **Next:** turn on Amazon data when a paying customer justifies the cost.

Close by offering to go deeper on the fuzzy part, or to save the walkthrough.
