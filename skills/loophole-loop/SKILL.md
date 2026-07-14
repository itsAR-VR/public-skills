---
name: loophole-loop
description: Iteratively grill a strategy, plan, or design until factually 100% confident. Lists every loophole, hidden assumption, missing evidence, race condition, and contradiction; proposes concrete on-disk fixes; reruns until certain. Use when the user says "loophole loop", "find the loopholes", "are you 100% confident", "loop until certain", "stress-test this strategy", "100% sure?", or wants a self-grilling confidence pass on the active plan.
---

Run a confidence loop on the active strategy, plan, decision, or design until factually 100% confident in it.

For each cycle:

1. State the current strategy in one paragraph. No vibes — quote the actual claim, file path, function name, gate, or commitment.
2. List every loophole, hidden assumption, missing evidence, race condition, edge case, contradiction with earlier context, and silent failure mode. If you cannot find any, keep looking — silent confidence is not the same as verified confidence.
3. For each loophole, propose a concrete fix and apply it (edit the code, update the plan doc, add the test, log the assumption, tighten the gate). Fixes must live on disk, not just in conversation context.
4. Re-state the strategy with the fixes applied.
5. Repeat from step 2 until you can write a one-line confidence statement that is factually true: "I am 100% confident because: <evidence-backed reasons>." Cite the file, gate, test result, or evidence row that proves each reason.
6. Only then declare done.

Rules:

- If a question can be answered by reading the codebase, read the codebase instead of asking the user.
- If the loop ever requires bypassing a stop condition, policy, or destructive-change guardrail, escalate to the user instead of looping. 100% confidence does not authorize policy bypass.
- When invoked inside a `goal-post` artifact, also update the artifact's run ledger and verification gates with the fixes you applied.
