# Model Currency

Hardcoded Codex model snapshot, locally verified on 2026-07-09 with Codex CLI
0.144.0:

- **Difficult/deep/review route:** `gpt-5.6-sol` with `ultra` effort.
- **Bounded worker route:** `gpt-5.6-terra` with `high` effort.
- **Tiny mechanical route:** `gpt-5.6-luna` with `low` or `medium` effort.
- **Claude Code highest-capability route:** `fable` selects Claude Fable 5 when
  the account and Claude Code version support it. Fable 5 is not the default.
- **Claude Code current Opus pinned ID:** `claude-opus-4-8`.
- **Claude Code aliases:** `fable`, `opus`, `sonnet`, and `haiku` resolve
  through Claude Code's model configuration. Prefer aliases when the user wants
  automatic latest-family routing, but remember those aliases can lag the newest
  Anthropic release or be unavailable in a user's account.
- **Verification sources:** local Codex CLI model probes; OpenAI GPT-5.6 preview
  (`https://help.openai.com/en/articles/20001325-a-preview-of-gpt-5-6-sol-terra-and-luna`);
  OpenAI latest model guide
  (`https://developers.openai.com/api/docs/guides/latest-model`); Anthropic
  model overview (`https://platform.claude.com/docs/en/about-claude/models/overview`);
  Claude Code model configuration (`https://code.claude.com/docs/en/model-config`).

Before changing a hardcoded model ID, do a quick official-source refresh:

1. Check OpenAI model/release docs for the current Codex-capable model.
2. Check Anthropic Claude Code model configuration and model overview for current
   Claude Code aliases and pinned model IDs.
3. Check local CLI support: `which -a codex`, `codex --version`,
   `codex exec --help`, and `claude --version` when available.
4. Record the model ID and refresh date in the phase plan, run log, or PR notes.

**Never downgrade to an older OpenAI model.** If the latest required OpenAI model
is unsupported by the local Codex CLI, upgrade Codex or stop and report the
unsupported model. Do not silently fall back.

If `which -a codex` returns multiple binaries, test each candidate and use the
highest supported `codex-cli` version through `CODEX_BIN=/absolute/path/to/codex`.
Do not trust bare `codex` when an older Homebrew/global binary shadows a newer
npm binary.

OpenAI-family verifier routing:

- **Codex main harness:** spawn native sub-agents only. Do not invoke nested
  `codex`, `codex exec`, MCP, or shell fallback.
- **Claude Code main harness:** `codex exec` is allowed after model-currency and
  CLI-support preflight passes.
- **Other provider main harness:** use its native agent delegation when
  available.
- **No native agent route and no allowed Claude-to-Codex CLI route:** stop and
  ask the user before any degraded single-provider verification.
