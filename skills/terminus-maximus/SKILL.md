---
name: terminus-maximus
description: Relentless end-to-end execution loop for coding tasks. Always resume the latest docs/planning/phase-N (highest N unless user specifies) and keep working until the phase is complete or truly blocked. On every turn, update phase docs with progress and run a RED TEAM pass (phase-gaps) to surface next steps, assumptions, and targeted user questions. Use when the user says "Terminus Maximus", "Ralph Loop", "never stop", "keep going", "continue", or wants full completion with explicit blocker handling and phase-plan/gaps/implement/review discipline.
related_skills: [skill-oracle, plan, phase-implement, phase-gaps, phase-review, build, karpathy-guidelines]
---

# Instructions

Read all references in `references/` before using this skill.

## Companion Skills (Mandatory)

Always apply these skills as **subroutines** of $terminus-maximus. They exist to improve the Terminus Maximus loop (clarity, correctness, verification) and should not replace it. Default output format remains Terminus Maximus (templates + phase doc updates) unless the user explicitly asks for a different format.

1. $skill-oracle — **Primary skill discovery.** At the start of each turn and whenever a new capability is needed, run `/skill-oracle "<task description>"` to find relevant skills from the full local catalog (~244 skills) and ClawHub. Use discovered skills as subroutines. This replaces `find-local-skills` and `find-skills`.
2. $karpathy-guidelines — Apply at the start of every turn to keep changes minimal, assumptions explicit, and verification tight.
3. $recursive-reasoning-operator — Use its PLAN/LOCATE/EXTRACT/SOLVE/VERIFY/SYNTHESIZE workflow whenever you are making claims or decisions grounded in docs/planning, references, or other provided materials. Then synthesize back into the Terminus Maximus progress updates + user response skeleton.
4. $ecc-documentation-lookup — If documentation is mentioned or platform/library behavior is version-sensitive, pull the relevant docs via Context7 MCP (resolve then query) before answering. Funnel findings back into Terminus Maximus updates; stay within Context7 call limits.
5. $skill-creator — If the task involves creating or updating any skill (including this one), follow its creation/update and validation steps.

## Original User Request Preservation

- When this workflow is currently triggered by /phase-plan or $phase-gaps, treat the exact original user request text as canonical context.
- Before any planning or RED TEAM reasoning, verify `docs/planning/phase-N/plan.md` begins with the literal user request copied verbatim (no paraphrase), and keep it unchanged.
- If the exact prompt block is missing, extract it from the invocation trigger and add:
  - `## Original User Request (verbatim)`
  - The full original prompt content exactly as provided
- Keep this block intact during subsequent `phase-gaps` passes and only reference it for context.

## Multi-Agent Awareness

**IMPORTANT:** Multiple agents may be working on different phases concurrently. Every turn:

1. Run `git status` and note unexpected changes
2. Scan the last 10 phases for overlaps with files you will touch
3. Document any coordination conflicts in the active subphase Output

See `07_MULTI_AGENT_COORDINATION.md` for procedures.

## Signals

- The user says "Terminus Maximus" / "Ralph Loop" / "never stop" / "keep going"
- The user wants you to finish the task fully, not partially
- The work is tracked via `docs/planning/phase-N/`

## References

**Directory:** `references/`

- `01_INTENT.md`
- `02_PRECONDITIONS.md`
- `03_RULES.md`
- `04_PROCEDURE.md`
- `05_TEMPLATES.md`
- `06_EDGE_CASES.md`
- `07_MULTI_AGENT_COORDINATION.md`
