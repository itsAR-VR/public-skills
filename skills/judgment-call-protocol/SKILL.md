---
name: judgment-call-protocol
description: "Use when a real decision point needs the user's input, including /jc, JC, judgment call, option forks, preference requests, or pauses for direction. Give a plain-English verbal briefing and a committed recommendation the user can approve with one word."
---

# Judgment Call Protocol

Use this when there is a real fork and the user should decide. If there is a clear path forward and no real decision for the user, commit and report instead.

## Output Shape

Write a verbal briefing in prose, as if talking the user through the decision face to face.

1. Start at the user/app level: what they see, what state the work is in, and why the decision matters.
2. Name the fork inside the same flow of prose.
3. Recommend one path clearly: "My recommendation is X because Y."
4. Make it easy for the user to reply with "agree" or a short alternative.

Use bullets only when the supporting information is genuinely list-shaped, such as field names, URLs, or concrete options. The main briefing should be connected prose, not chopped-up fragments.

## Trigger Examples

- Two reasonable interpretations of an ambiguous spec.
- A user-facing behavior choice.
- A naming or vocabulary call that will appear in the product.
- An architectural fork the agent should not resolve alone.
- The user types `/jc`, `JC`, `jc`, or "judgment call".

## Composition

- If asking the user to open or inspect anything, include the full clickable URL in the same turn.
- If the fork exists only because the agent is tempted to substitute or defer, apply the no-substitutions protocol first and only escalate if there is a genuine blocker.

## Template

```text
On [surface/context], [walk through what is happening in plain English]. The fork is between [option A and consequence] and [option B and consequence]. My recommendation is [one option] because [short reason]. If you agree, I’ll do that; if not, tell me the alternative and I’ll follow it.
```
