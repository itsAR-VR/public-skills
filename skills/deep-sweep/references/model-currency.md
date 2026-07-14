# Model Currency and Harness Routing

Use this reference before hardcoding or changing any model ID, verifier route,
effort control, or Claude Code alias in Deep Sweep.

Codex source check for this version: locally verified on 2026-07-09 with Codex
CLI 0.144.0. Refresh after any OpenAI or Anthropic model release, any Codex or
Claude Code CLI model-support failure, or 90 days, whichever comes first.
Current official OpenAI and Anthropic docs outrank this file for provider/API
availability.

Official sources checked:

- OpenAI GPT-5.6 preview: `https://help.openai.com/en/articles/20001325-a-preview-of-gpt-5-6-sol-terra-and-luna`
- OpenAI latest model guide: `https://developers.openai.com/api/docs/guides/latest-model`
- Claude Code model configuration: `https://code.claude.com/docs/en/model-config`
- Claude extended/adaptive thinking docs: `https://platform.claude.com/docs/en/build-with-claude/extended-thinking`
- Fable 5 local migration reference: `skills/prompt-generation/references/claude-fable-5.md`

## Current Snapshot

- **Difficult/deep/review route:** `gpt-5.6-sol` with `ultra` effort.
- **Bounded worker route:** `gpt-5.6-terra` with `high` effort.
- **Tiny mechanical route:** `gpt-5.6-luna` with `low` or `medium` effort.
- **Access gate:** require `codex debug models` to advertise the chosen GPT-5.6
  ID and effort, then prove account entitlement with a live read-only probe
  after login. Update Codex or stop with a blocker; never downgrade silently.
- **Claude Code preferred route:** use aliases (`best`, `fable`, `opus`,
  `sonnet`, `haiku`) unless the user explicitly needs a pinned model.
- **Pinned Claude fallback when needed:** `claude-opus-4-8` after local
  `claude --version` and provider support checks pass.
- **Fable 5:** select with `/model fable` where available. Fable 5 safety
  classifiers may route cybersecurity or biology-adjacent requests to Opus; log
  the fallback as routing, not a failure.

## Refresh Checklist

Before changing a hardcoded model ID:

1. Check OpenAI model/release docs for the current Codex-capable verifier model.
2. Check Claude Code model configuration for current aliases, pinned model IDs,
   fallback behavior, and minimum CLI versions.
3. Check local CLI support: `which -a codex`, `codex --version`,
   `codex exec --help`, and `claude --version` when available.
4. Record the model ID, source URLs, local CLI support, and refresh date in the
   plan or run log.

## Effort and Reasoning Controls

- For OpenAI/Codex CLI verification, use the tier-appropriate control, such as
  `-c model_reasoning_effort=ultra` for Sol review, only after `codex exec --help` confirms
  support.
- For Claude Fable 5 and recent Opus models, use provider-appropriate effort or
  adaptive thinking controls. Do not use manual `budget_tokens` thinking
  configs for Fable 5, Opus 4.8, or Opus 4.7.
- Never ask a model to show, echo, transcribe, or explain hidden/internal
  reasoning. Request evidence-backed findings, confidence, assumptions, and
  citations to files or tool results instead.
