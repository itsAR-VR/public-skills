---
name: conversation-context-hydrator
description: >
  Loads the minimum useful project, person, decision, handoff, history, and
  proof context before Codex/Jarvis answers. Use for "where are we?", "where
  did we leave off?", "resume this build", "answer with the right background",
  "hydrate context", "old handoff", "minimal context packet", stale memory,
  project history, repo plus Linear background, drafting replies, or grounded
  next steps. Route through business-context-intelligence first for broad
  multi-source context; use this skill when the primary job is answer
  preparation.
related_skills:
  - business-context-intelligence
  - relationship-context-brief
  - context-freshness-gate
  - proof-aware-status
  - priority-sensemaker
  - open-loop-radar
  - memory-systems
---

# Conversation Context Hydrator

Use this before an answer would be worse without current context.

The goal is not to load everything. The goal is to load just enough source
truth so the answer sounds grounded in the actual business and build state.

## Fast Path

Identify the entity, check its likely source of truth, run one freshness/proof
check if needed, then answer.

## Escalate Only If Needed

Load additional tools or relationship history only when the answer affects a
decision, external message, status claim, or commitment.

## Safe Automatic Actions

- Read current source truth and run cheap proof/freshness checks.
- Draft replies or talking points, but do not send them.
- Propose follow-up, memory, Linear, or docs updates when rules allow.
- Stop before sends, deploys, credentials, money, public/customer-facing
  actions, or broad private-source searches.

## Hydration Depth

- Fast: one entity, one likely source, answer with a confidence label.
- Standard: source of truth plus one current-state check.
- Deep: multiple entities, cross-tool status, relationship context, and proof.

## Hydration Steps

1. Identify the entities: project, repo, company, person, client, product, or
   issue mentioned by the user.
2. Pick the likely source of truth for each entity.
3. Load the smallest useful context: current handoff, repo docs, Linear issue,
   PR, meeting note, decision log, or proof receipt.
4. Run `context-freshness-gate` if the source could be stale.
5. Answer with confidence labels and source references when practical.

## Context Packet

Build a compact packet before answering:

```text
Context Packet
- Entity:
- Source of truth:
- Current proof:
- Open loop:
- Confidence:
- Blind spot:
```

## Minimum Context Rules

- For a project: load current handoff plus target repo instructions/docs.
- For a build: load plan, latest proof, current git/PR state, and blockers.
- For a person/company: load relationship context and latest interaction.
- For "is it done?": pair with `proof-aware-status`.
- For "what next?": pair with `priority-sensemaker` and `open-loop-radar`.

## Output

Keep the user-facing answer plain:

- What I checked.
- What is true now.
- What that means.
- What to do next.
- What I could not verify.

## Guardrails

- Do not block on perfect context when a scoped answer is enough.
- Do not expose private raw notes, secrets, auth state, or sensitive logs.
- Do not claim a live check happened when the answer uses memory only.
