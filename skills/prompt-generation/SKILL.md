---
name: prompt-generation
description: "Use when generating or rewriting durable prompts, Codex /goal objectives, OpenAI GPT-5.6 prompt packages, Anthropic Claude (Fable 5) prompt packages, agent instructions, skill instructions, SKILL.md rewrites, skill-package best-practice reviews, grader/eval prompts, or model migration prompts (OpenAI-to-Claude or Claude-to-OpenAI) that need source-backed controls, validation, and refresh triggers."
related_skills:
  - openai-docs
  - codex
  - goal-post
  - skill-creator
  - skill-judge
  - prompt-oracle
  - ecc-prompt-optimizer
  - advanced-evaluation
  - ecc-eval-harness
---

# Prompt Generation

Use this skill for reusable prompt architecture: Codex prompts, Codex `/goal`
objectives, API prompts, agent instructions, skill instructions, graders, eval
prompts, and model-migration prompt packages.

Do not use it for a one-off rewrite, casual copy edit, or task that should be
executed directly. Do not use it as a substitute for current OpenAI docs.

## Workflow

1. Classify the surface: Codex task, Codex `/goal`, Responses API, skill,
   sub-agent packet, grader/eval, or cross-model compatibility note.
2. Identify the target model and provider. For volatile OpenAI model/API
   guidance, invoke `openai-docs` and use official docs over bundled notes.
   For volatile Anthropic model/API guidance, verify against current official
   Anthropic docs (platform.claude.com) before hardcoding.
3. Collect source truth: task goal, audience, inputs, constraints, tool/data
   boundaries, output shape, success criteria, and failure modes.
4. Load `references/model-prompt-generation-playbook.md` for substantive prompt
   architecture, model migration, or eval design. When the target model is
   Anthropic Claude, also load `references/claude-fable-5.md` — the dated
   per-model lane for the current Anthropic flagship.
5. Generate the prompt package with prompt text, runtime controls, validation
   cases, assumptions, and refresh triggers separated.
6. For new or rewritten `SKILL.md` packages, use `skill-creator` for package
   shape, frontmatter, references, scripts, and eval hooks, then apply
   `skill-judge` before closeout and carry forward only findings that improve
   trigger quality, knowledge delta, loading, or evalability.
7. For grader/eval prompts, apply `advanced-evaluation` and prefer
   deterministic checks from `ecc-eval-harness` before LLM-as-judge rubrics.
8. Run the anti-pattern check before finalizing.

## Output Contract

Return:

- target surface and target model/provider;
- prompt text or skill text;
- runtime controls to set outside the prompt;
- source assumptions and dated docs checked;
- tool, data, privacy, and external-action boundaries;
- validation cases, grader/eval plan, or proof commands;
- skill-judge findings when the output is a `SKILL.md` package;
- known failure modes and refresh triggers.

For machine-consumable outputs, prefer Structured Outputs or strict tool schemas
over prose-only schema instructions when the host supports them.

## Anti-Patterns

- Starting with a persona such as "You are a senior..." and treating that as
  the prompt structure.
- Model-string-only migrations for complex prompts without evals.
- Hardcoding current model IDs, prices, context windows, or feature flags in
  long-lived skill text without a dated source and refresh rule.
- Mixing provider controls: OpenAI Responses/Codex controls are not Anthropic
  Claude API controls.
- Embedding long reusable playbooks in `SKILL.md` instead of references.
- Rewriting skills without judging the trigger contract, knowledge delta,
  progressive disclosure, and eval hooks.
- Describing tool behavior only in the system prompt when the tool description
  should carry what, when, inputs, side effects, retry safety, and errors.

## Validation

Before closeout:

- verify current official docs for volatile model/API claims;
- check that stable content comes before dynamic content in cache-sensitive
  prompts;
- include a clear done/proof surface;
- include refusal, blocker, or incompatible-input handling where applicable;
- run `skill-judge` for skill packages and record top fixes;
- label eval proof accurately: structural manifest validation is not the same
  as executed behavioral evals;
- run YAML/frontmatter validation when editing skills.
