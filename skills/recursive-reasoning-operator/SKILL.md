---
name: recursive-reasoning-operator
description: Produce correct, source-grounded answers using a Plan/Locate/Extract/Solve/Verify/Synthesize evidence trail. Use when the user requests strict grounding in provided material, wants auditable support, or needs answers derived only from supplied documents or excerpts.
related_skills: [advanced-evaluation, evaluation, comparative-analysis-orchestrator, plan]
---

# Recursive Reasoning Operator

## Overview

Deliver a correct answer that is grounded exclusively in the provided material. Make the answer auditable by showing the plan, evidence, conclusions, verification checks, and synthesis.

## Workflow

1. PLAN: State the sub-questions that must be answered.
2. LOCATE: For each sub-question, specify exactly what to find (keywords, entities, sections). Ask for missing documents if needed.
3. EXTRACT: Quote the minimum necessary excerpts. Label them clearly.
4. SOLVE: Answer each sub-question using only the extracted excerpts. Assign a confidence score from 0.0 to 1.0.
5. VERIFY: Check for missing assumptions, contradictions, or weak logic.
6. SYNTHESIZE: Produce the final answer. Explicitly state uncertainty where confidence is low.

## Output Template

Use this exact section order in responses.

```text
PLAN
<sub-questions>

LOCATE
<what to find for each sub-question; request missing docs if needed>

EXTRACT
<labeled, minimal quotes>

SOLVE
<answer each sub-question using only excerpts; include confidence 0.0-1.0>

VERIFY
<assumptions, contradictions, weak logic>

SYNTHESIZE
<final answer, explicitly state uncertainty where confidence is low>
```

## Constraints

1. Prefer targeted extraction over summarization.
2. Use only the provided material; do not add external knowledge.
3. If context is large or missing, request it in chunks based on the LOCATE plan.
4. Optimize for correctness, not fluency.
