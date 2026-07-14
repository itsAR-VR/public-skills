# Autoreason Task Template

Copy this, fill in the blanks, save as `task.md`, then run:

```
python scripts/autoreason.py --task task.md --out runs/my_run_01
```

---

# Task

{{ one-sentence statement of what you want produced, verbatim. This string is sent
   to every role (critic, author, synthesizer, judges) — identical for all. Keep
   it tight; every word counts. }}

## Context

- **Audience**: {{ who reads this; what they already know; what they're deciding }}
- **Purpose**: {{ the single outcome this artifact must produce }}
- **Success criteria**: {{ how you'll know this is working — even a rough heuristic }}

## Deliverable

{{ exact structure of the output. Use the tightest specification you can.

   BAD:  "a compelling positioning statement"
   GOOD: "a positioning statement with:
           - One-sentence category definition (≤ 20 words)
           - One-sentence primary differentiator (≤ 20 words)
           - One-sentence outcome the customer can measure (≤ 25 words)
           - One proof element (number, logo, or named fact)"
}}

## Constraints

- {{ hard constraint 1 — e.g., word count max, format requirement }}
- {{ hard constraint 2 }}
- {{ hard constraint 3 — anything that must NOT be in the output }}

## Knowledge layer (optional but recommended)

{{ If you have performance data, competitor positioning, customer research, or
   brand voice rules, paste them here OR reference a file. The critic and judges
   will use this to anchor critique in evidence, not gut feel.

   Keep under ~1500 tokens — this goes to every role every pass. }}

---

**Tips for writing a good task prompt:**
- If the constraint "must not be generic" matters, say so explicitly — "if a
  competitor could say this word-for-word, it's not a differentiator."
- Prefer hard constraints over soft suggestions — "max 120 words" beats
  "concise."
- Don't tell the author HOW to do the task, only WHAT. The tournament handles
  "how."
