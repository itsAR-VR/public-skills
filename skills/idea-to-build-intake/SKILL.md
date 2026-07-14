---
name: idea-to-build-intake
description: >
  Evaluates raw build ideas before planning or implementation and decides
  capture, clarify, plan, or ignore. Use when Matt brainstorms, says "we should
  build", "should we build this", "build or note", "just a note", "this could
  be useful", "is this worth building?", "fake urgency or real opportunity",
  "smallest useful version", "capture before implementation", "not ready to
  code", or mentions future features, agents, workflows, products, or
  automations across Jarvis, Codex, Chief/PROJECT, or future systems. Route through
  business-context-intelligence first for broad context; use this skill when the
  primary job is idea triage, not coding.
related_skills:
  - business-context-intelligence
  - business-memory-signal-capture
  - priority-sensemaker
  - phase-plan
  - requirements-clarity
---

# Idea To Build Intake

Turn an idea into one of four outcomes: capture, clarify, plan, or ignore.

This prevents two failure modes: losing good ideas and turning every thought
into a noisy project.

## Fast Path

Identify the pain, beneficiary, smallest useful version, proof, and where the
idea belongs. Choose capture, clarify, plan, or ignore.

Default to read-only triage and recommendation. Do not write memory, repo docs,
issue comments, CRM notes, or task updates unless the user asked for that write
or standing workspace rules explicitly allow that exact target.

## Escalate Only If Needed

Check Linear, repo docs, or memory only when the idea may duplicate existing
work or is ready to become a real plan.

## Safe Automatic Actions

- Compare against active builds and known ideas when reachable.
- Propose capture, clarification, or first-version wording.
- Create/update Linear, docs, or memory only when the idea is ready and current
  rules allow the exact target.
- Stop before implementation unless Matt explicitly asked to build now.

## Intake Mode

Use this before implementation unless Matt explicitly asks to build now. The
default goal is to decide where the idea belongs, not to expand scope.

## Intake Questions

Answer from available context:

- What user/business pain does this solve?
- Who benefits?
- What current build or system would it improve?
- What would be true when it works?
- What is the smallest useful first version?
- What proof would close it?
- What risk, approval, or dependency exists?

## Decision

Choose one:

- Capture: useful idea, not ready for action.
- Clarify: promising but missing outcome, owner, or proof.
- Plan: ready for a phase/issue/spec with first action and done criteria.
- Ignore: not enough value, duplicate, or fake urgency.

## Escalation Rules

- Create or update Linear only when the idea is ready for planned work or is a
  real active build decision.
- Save to memory/docs only when the idea has reusable future value and current
  memory rules allow it.
- Ask one concise question when the value is promising but the outcome is
  unclear.
- Ignore without ceremony when it is duplicate, vague, or disconnected from a
  real outcome.

## Proactive Promotion Rules

Promote an idea from capture to clarify/plan only when:

- It appears repeatedly across sweeps or meetings.
- It connects to a current blocker, revenue opportunity, or repeated friction.
- A smallest useful version and proof target are clear.
- It is not already covered by an active build or existing skill.

Otherwise keep it captured and out of the active priority list.

## Output

```text
Build Intake

Decision: capture / clarify / plan / ignore
Why:
- ...

First Useful Version:
- ...

Definition Of Done:
- ...

Where It Belongs:
- repo / Linear / memory / no action
```

## Guardrails

- Do not create Linear issues for vague ideas.
- Do not start implementation unless the user asked to build or the workflow
  clearly permits it.
- Keep project-specific ideas in the project source of truth.
