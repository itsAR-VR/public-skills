---
name: skill-judge
description: 'Use when asked to "judge skill quality", review, audit, score, or improve SKILL.md files and skill packages against official specifications, knowledge delta, trigger quality, progressive disclosure, anti-patterns, and evalability.'
related_skills: [skill-creator, find-local-skills, find-skills, skill-oracle, evaluation, advanced-evaluation]
---

# Skill Judge

Evaluate Agent Skills against official specifications and patterns derived from 17+ official examples.

**MANDATORY: load `references/judging-detail.md` before scoring.** It carries the full per-dimension scoring tables, the nine common failure patterns, and the report template. This body carries the philosophy, the dimension one-liners, the protocol, and the quick checklist.

---

## Core Philosophy

### What is a Skill?

A Skill is NOT a tutorial. A Skill is a **knowledge externalization mechanism**.

Traditional AI knowledge is locked in model parameters. To teach new capabilities:
```
Traditional: Collect data → GPU cluster → Train → Deploy new version
Cost: $10,000 - $1,000,000+
Timeline: Weeks to months
```

Skills change this:
```
Skill: Edit SKILL.md → Save → Takes effect on next invocation
Cost: $0
Timeline: Instant
```

This is the paradigm shift from "training AI" to "educating AI" — like a hot-swappable LoRA adapter that requires no training. You edit a Markdown file in natural language, and the model's behavior changes.

### The Core Formula

> **Good Skill = Expert-only Knowledge − What Claude Already Knows**

A Skill's value is measured by its **knowledge delta** — the gap between what it provides and what the model already knows.

- **Expert-only knowledge**: Decision trees, trade-offs, edge cases, anti-patterns, domain-specific thinking frameworks — things that take years of experience to accumulate
- **What Claude already knows**: Basic concepts, standard library usage, common programming patterns, general best practices

When a Skill explains "what is PDF" or "how to write a for-loop", it's compressing knowledge Claude already has. This is **token waste** — context window is a public resource shared with system prompts, conversation history, other Skills, and user requests.

### Tool vs Skill

| Concept | Essence | Function | Example |
|---------|---------|----------|---------|
| **Tool** | What model CAN do | Execute actions | bash, read_file, write_file, WebSearch |
| **Skill** | What model KNOWS how to do | Guide decisions | PDF processing, MCP building, frontend design |

Tools define capability boundaries — without bash tool, model can't execute commands.
Skills inject knowledge — without frontend-design Skill, model produces generic UI.

**The equation**:
```
General Agent + Excellent Skill = Domain Expert Agent
```

Same Claude model, different Skills loaded, becomes different experts.

### Three Types of Knowledge in Skills

When evaluating, categorize each section:

| Type | Definition | Treatment |
|------|------------|-----------|
| **Expert** | Claude genuinely doesn't know this | Must keep — this is the Skill's value |
| **Activation** | Claude knows but may not think of | Keep if brief — serves as reminder |
| **Redundant** | Claude definitely knows this | Should delete — wastes tokens |

The art of Skill design is maximizing Expert content, using Activation sparingly, and eliminating Redundant ruthlessly.

---

## Evaluation Dimensions (130 points total)

One-liners only — the full scoring tables, examples, and red/green flags live in `references/judging-detail.md`. Load it before assigning any score.

| Dimension | Max | Question it answers |
|-----------|-----|---------------------|
| D1: Knowledge Delta | 20 | Does every paragraph add knowledge Claude doesn't already have? |
| D2: Mindset + Appropriate Procedures | 15 | Does it transfer expert thinking plus domain procedures Claude wouldn't know? |
| D3: Anti-Pattern Quality | 15 | Are there specific NEVER lists with non-obvious reasons? |
| D4: Specification Compliance | 15 | Valid frontmatter; does the description answer WHAT, WHEN, and KEYWORDS? |
| D5: Progressive Disclosure | 15 | Lean body with references loaded via explicit triggers? |
| D6: Freedom Calibration | 15 | Is specificity matched to task fragility? |
| D7: Pattern Recognition | 10 | Does it follow an established official pattern? |
| D8: Practical Usability | 15 | Can an agent act on it immediately, including edge cases and fallbacks? |
| D9: Refresh Boundary & Evalability | 10 | Are volatile model/price/flag claims dated with named refresh triggers; are validation commands or `evals/evals.json` present; is structural vs behavioral proof labeled? |

---

## NEVER Do When Evaluating

- **NEVER** give high scores just because it "looks professional" or is well-formatted
- **NEVER** ignore token waste — every redundant paragraph should result in deduction
- **NEVER** let length impress you — a 43-line Skill can outperform a 500-line Skill
- **NEVER** skip mentally testing the decision trees — do they actually lead to correct choices?
- **NEVER** forgive explaining basics with "but it provides helpful context"
- **NEVER** overlook missing anti-patterns — if there's no NEVER list, that's a significant gap
- **NEVER** assume all procedures are valuable — distinguish domain-specific from generic
- **NEVER** undervalue the description field — poor description = skill never gets used
- **NEVER** put "when to use" info only in the body — Agent only sees description before loading
- **NEVER** pass undated model, price, or flag claims — volatile facts without a named refresh trigger are future bugs

---

## Evaluation Protocol

**If you authored or edited the skill in this session, dispatch a fresh-context subagent to score it; never self-grade your own draft in-context.** The subagent sees only the skill package and this rubric, not your authoring reasoning.

### Step 1: First Pass — Knowledge Delta Scan

Read SKILL.md completely and for each section ask:
> "Does Claude already know this?"

Mark each section as:
- **[E] Expert**: Claude genuinely doesn't know this — value-add
- **[A] Activation**: Claude knows but brief reminder is useful — acceptable
- **[R] Redundant**: Claude definitely knows this — should be deleted

Calculate rough ratio: E:A:R
- Good Skill: >70% Expert, <20% Activation, <10% Redundant
- Mediocre Skill: 40-70% Expert, high Activation
- Bad Skill: <40% Expert, high Redundant

### Step 2: Structure Analysis

```
[ ] Check frontmatter validity
[ ] Count total lines in SKILL.md
[ ] List all reference files and their sizes
[ ] Identify which pattern the Skill follows
[ ] Check for loading triggers (if references exist)
[ ] Check for dated volatile claims and validation hooks (D9)
```

### Step 3: Score Each Dimension

For each of the 9 dimensions (tables in `references/judging-detail.md`):
1. Find specific evidence (quote relevant lines)
2. Assign score with one-line justification
3. Note specific improvements if score < max

### Step 4: Calculate Total & Grade

```
Total = D1 + D2 + D3 + D4 + D5 + D6 + D7 + D8 + D9
Max = 130 points
```

**Grade Scale** (percentage-based):
| Grade | Percentage | Meaning |
|-------|------------|---------|
| A | 90%+ (117+) | Excellent — production-ready expert Skill |
| B | 80-89% (104-116) | Good — minor improvements needed |
| C | 70-79% (91-103) | Adequate — clear improvement path |
| D | 60-69% (78-90) | Below Average — significant issues |
| F | <60% (<78) | Poor — needs fundamental redesign |

### Step 5: Generate Report

Use the report template in `references/judging-detail.md`: summary (score, grade, pattern, E:A:R ratio, one-line verdict), per-dimension score table, critical issues, top 3 improvements, and detailed analysis for any dimension below 80%.

---

## Quick Reference Checklist

```
┌─────────────────────────────────────────────────────────────────────────┐
│  SKILL EVALUATION QUICK CHECK                                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  KNOWLEDGE DELTA (most important):                                      │
│    [ ] No "What is X" explanations for basic concepts                   │
│    [ ] No step-by-step tutorials for standard operations                │
│    [ ] Has decision trees for non-obvious choices                       │
│    [ ] Has trade-offs only experts would know                           │
│    [ ] Has edge cases from real-world experience                        │
│                                                                         │
│  MINDSET + PROCEDURES:                                                  │
│    [ ] Transfers thinking patterns (how to think about problems)        │
│    [ ] Has "Before doing X, ask yourself..." frameworks                 │
│    [ ] Includes domain-specific procedures Claude wouldn't know         │
│    [ ] Distinguishes valuable procedures from generic ones              │
│                                                                         │
│  ANTI-PATTERNS:                                                         │
│    [ ] Has explicit NEVER list                                          │
│    [ ] Anti-patterns are specific, not vague                            │
│    [ ] Includes WHY (non-obvious reasons)                               │
│                                                                         │
│  SPECIFICATION (description is critical!):                              │
│    [ ] Valid YAML frontmatter                                           │
│    [ ] name: lowercase, ≤64 chars                                       │
│    [ ] description answers: WHAT does it do?                            │
│    [ ] description answers: WHEN should it be used?                     │
│    [ ] description contains trigger KEYWORDS                            │
│    [ ] description is specific enough for Agent to know when to use     │
│                                                                         │
│  STRUCTURE:                                                             │
│    [ ] SKILL.md < 500 lines (ideal < 300)                               │
│    [ ] Heavy content in references/                                     │
│    [ ] Loading triggers embedded in workflow                            │
│    [ ] Has "Do NOT Load" for preventing over-loading                    │
│                                                                         │
│  FREEDOM:                                                               │
│    [ ] Creative tasks → High freedom (principles)                       │
│    [ ] Fragile operations → Low freedom (exact scripts)                 │
│                                                                         │
│  USABILITY:                                                             │
│    [ ] Decision trees for multi-path scenarios                          │
│    [ ] Working code examples                                            │
│    [ ] Error handling and fallbacks                                     │
│    [ ] Edge cases covered                                               │
│                                                                         │
│  REFRESH & EVALABILITY:                                                 │
│    [ ] Model/price/flag claims dated with named refresh triggers        │
│    [ ] Validation commands or evals/evals.json present                  │
│    [ ] Structural vs behavioral proof labeled                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## The Meta-Question

When evaluating any Skill, always return to this fundamental question:

> **"Would an expert in this domain, looking at this Skill, say:**
> **'Yes, this captures knowledge that took me years to learn'?"**

If the answer is yes → the Skill has genuine value.
If the answer is no → it's compressing what Claude already knows.

The best Skills are **compressed expert brains** — they take a designer's 10 years of aesthetic accumulation and compress it into 43 lines, or a document expert's operational experience into a 200-line decision tree.

What gets compressed must be things Claude doesn't have. Otherwise, it's garbage compression.

---

## Self-Evaluation Note

This Skill (skill-judge) should itself pass evaluation:

- **Knowledge Delta**: Provides specific evaluation criteria Claude wouldn't generate on its own
- **Mindset**: Shapes how to think about Skill quality, not just checklist items
- **Anti-Patterns**: "NEVER Do When Evaluating" section with specific don'ts
- **Specification**: Valid frontmatter with comprehensive description
- **Progressive Disclosure**: Routing body with scoring detail in `references/judging-detail.md` behind a mandatory load trigger
- **Freedom**: Medium freedom appropriate for evaluation task
- **Pattern**: Follows Tool pattern with decision frameworks
- **Usability**: Clear protocol, report template, quick reference
- **Refresh & Evalability**: Carries no volatile model claims; validation lives in the repo's skill validators

Evaluate this Skill against itself as a calibration exercise — and if you just edited skill-judge itself, that calibration run goes to a fresh-context subagent too.
