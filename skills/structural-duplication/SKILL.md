---
name: audit-structural-duplication
description: >
  Identify structurally duplicate logic (pipeline-spine duplication) across
  semantically distinct modules. Use when parallel orchestration, repeated
  infrastructure, or abstraction seams need a duplication map and safe
  extraction/refactor plan.
related_skills: [code-refactoring, reducing-entropy, audit-inline-complexity, audit-semantic-noise]
---

# Instructions

Read all references in `references/` before starting.

## Goal

Detect and report **structural duplication** across modules (not copy/paste), especially where:

- different domain concepts remain correctly separate, but
- the underlying processing pipeline is parallel/duplicated, risking drift.

When unification likely requires **subtle abstraction**, produce a **staged plan** that can be executed safely.

## Scope

- This skill **does not** enforce “thin public facades” or restructure public APIs.
- This skill **does** identify shared pipeline spines and propose extraction targets and abstraction seams.

## Signals

Activate when any of the following are true:

- Multiple modules implement similar orchestration stages (even with different operators).
- There are parallel implementations of structurally similar functionality in the codebase.
- The agent (or a developer) is about to re-implement “the same infrastructure again” for a new product.

## Procedure

Follow `references/03_PROCEDURE.md`.

## Output

Produce a single Markdown report using `references/05_OUTPUT_TEMPLATE.md`.
If abstraction is needed, include a staged plan using `references/04_REFACTOR_PLAN_TEMPLATE.md`.
