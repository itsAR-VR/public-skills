---
name: prompt-oracle
description: Analyze an inbound user prompt against the installed Codex skill library and return every plausibly relevant local skill with paths, scores, and concise reasons. Use when the user wants to know which skills apply to a request or wants a prompt populated with matching skills.
related_skills:
  - skill-oracle
  - find-skills
  - find-local-skills
  - llm-application-dev
---

# Prompt Oracle

Use this skill when the task is: "look at my prompt and tell me which Codex skills are relevant" or "populate this request with the right skills."

## What This Skill Does

1. Scans the installed local skill library on the current machine
2. Extracts each skill's name and description from `SKILL.md`
3. Scores the user's prompt against those skills
4. Returns all matches above the relevance threshold, ordered strongest first

## How To Run

Run the bundled matcher with the full user prompt:

```bash
python3 ~/.codex/skills/prompt-oracle/scripts/match_skills.py --prompt "<user prompt>"
```

If the user gave a long prompt, pass it by file:

```bash
python3 ~/.codex/skills/prompt-oracle/scripts/match_skills.py --prompt-file /tmp/request.txt
```

## Output Rules

- Return all matches at or above the threshold. Do not cap at 3.
- Prefer precision over noise, but include adjacent skills if the prompt clearly spans multiple domains.
- If a skill is an obvious umbrella and a child skill is more specific, include both only when both help.
- Exclude hidden and quarantined skills unless the user explicitly asks for them.

## Response Format

Use this structure in the response:

```markdown
Relevant skills for: "<prompt>"

- `skill-name` — short reason
- `skill-name` — short reason
```

If useful, add a second block:

```markdown
Ready-to-paste skill hints:
`use skill-name`
`use another-skill`
```

## Notes

- This skill recommends local skills only. It does not install anything.
- The matcher resolves the live skills directory dynamically. Override with `PROMPT_ORACLE_SKILLS_DIR=/path/to/skills` if needed.
- If the user wants missing capabilities, follow up with `skill-oracle` or `skill-creator`.
