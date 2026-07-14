---
name: post-compact
description: "Use after a conversation compact, when the user invokes /pc or post-compact, or when context may have been lost. Regain understanding before acting by reading the summary, current files, memory, or asking the user instead of guessing."
---

# Post-Compact Orientation

After a context compact, regain understanding before doing more work. The agent may have lost prior conversation detail, so it should not charge ahead from partial memory.

## Recovery Steps

1. Read the compact summary or latest available conversation context.
2. Re-read the actual files, code, PR, artifact, or source material being discussed.
3. Use relevant memory or repo instructions when continuity matters.
4. Ask the user directly when the missing context changes the next action.
5. Proceed only after the requested outcome, current state, and next proof step are clear.

## Standing Reminders

- The user makes major judgment calls.
- Pause on unexpected behavior instead of looping blindly.
- Work from observed evidence: code, files, source docs, current PRs, screenshots, or user confirmation.
- If the user has not seen or verified the thing, it is not fully done.

## Recovery When Invoked

If the user types `/pc`, stop the current action long enough to re-ground. Briefly state what you are checking, what you recovered, and what you will do next.
