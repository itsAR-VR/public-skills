---
name: claude
description: >
  Use when the user asks to run Claude Code CLI (claude, claude -p, claude
  resume/continue) or references Anthropic Claude for code analysis,
  refactoring, review, or automated editing. Uses the current Anthropic
  flagship model by default for high-end software engineering.
metadata:
  author: community
  version: 1.0.0
related_skills: [codex, claude-code-best-practice, build, code-review]
---

# Claude Skill Guide

## Running a Task

1. Default to the current Anthropic flagship model. As of 2026-06-09, official Anthropic docs list `claude-fable-5` as the current flagship API ID (long-context variant `claude-fable-5[1m]`), with `claude-opus-4-8` as the fallback lane; Claude Code docs say `opus` resolves to the latest Opus model. Whether Claude Code maps an alias to Fable 5 is version-dependent — verify at execution time via `/model` or `claude --help` before pinning. If pinning a concrete Anthropic model ID, verify the current recommended model from official Anthropic docs or the current Claude Code environment first.
2. Default to `--effort high` for serious coding, review, architecture, and long-running agentic tasks. On Fable 5, `high` is the default and even `low` exceeds prior generations' `xhigh`; reserve `xhigh` for the most capability-sensitive work. Use lower effort when the user asks for speed/cost tradeoffs, and use `max` only with explicit user approval on models that support it.
3. Choose the permission mode required for the task:
   - `--permission-mode plan` for read-only planning or strategy.
   - `--permission-mode default` for normal interactive guarded work.
   - `--permission-mode acceptEdits` for local edit tasks where Claude should still ask before risky commands.
   - `--permission-mode auto` for trusted local execution with reduced prompting.
   - `--permission-mode bypassPermissions` or `--dangerously-skip-permissions` only when the user explicitly asks for fully autonomous execution.
4. Assemble non-interactive commands with `-p, --print`:
   - `--model <alias-or-model-id>`
   - `--effort <low|medium|high|xhigh|max>`
   - `--permission-mode <default|acceptEdits|plan|auto|dontAsk|bypassPermissions>`
   - `--add-dir <DIR>` for extra allowed directories.
   - `--tools <tools>` to restrict available tools, or `--allowedTools <rules>` to pre-approve specific tools.
   - `--output-format <text|json|stream-json>` when machine-readable output is needed.
   - `--max-turns <N>` for bounded scripted runs.
   - `--setting-sources user` when project-local Claude hooks/settings are noisy and the task does not require project Claude config.
5. Prefer passing prompts as a quoted command argument or a short stdin payload. For content over 4 KB, write it to a temporary file and tell Claude to read that file instead of piping large content directly.
6. Run the command, capture stdout/stderr, and summarize the result. Keep stderr available when debugging auth, MCP, hooks, permissions, or model selection.
7. After Claude completes, tell the user they can resume this Claude Code session with `claude --continue -p "..."` or `claude --resume <session-id> -p "..."` when relevant.

### Quick Reference

| Use case | Command pattern |
| --- | --- |
| Read-only analysis | `claude -p --model opus --effort high --permission-mode plan "review this repo"` |
| Edit with guarded permissions | `claude -p --model opus --effort high --permission-mode acceptEdits "fix the failing tests"` |
| Fully autonomous trusted run | `claude -p --model opus --effort high --dangerously-skip-permissions "complete the task"` |
| Continue latest local session | `claude --continue -p "continue with the next step"` |
| Resume a specific session | `claude --resume <session-id> -p "finish the implementation"` |
| Structured output | `claude -p --output-format json "return a JSON summary"` |
| Extra directories | `claude -p --add-dir ../other-repo "inspect both repos"` |
| Bypass noisy project hooks | `claude -p --setting-sources user --model opus --effort high "analyze this task"` |

## Model Options

| Model | Best for | Notes |
| --- | --- | --- |
| `claude-fable-5` | Current flagship for high-end coding, review, architecture, and hard agentic work | Current Anthropic flagship API ID as of 2026-06-09. Defaults to `high` effort; `low` exceeds prior generations' `xhigh`. Claude Code support — verify at execution time. |
| `claude-fable-5[1m]` | Long-context flagship variant | 1M context window, 128K max output (2026-06-09). Availability — verify at execution time. |
| `opus` | Latest-Opus alias work and the Fable 5 fallback lane | Alias for latest Opus in Claude Code (Opus 4.8 as of 2026-06-09). Prefer aliases over stale pinned IDs. |
| `claude-opus-4-8` | Pinned fallback Opus ID | Fallback lane when Fable 5 is unavailable or declined. Verify before use if time has passed. |
| `sonnet` | Daily coding tasks where speed/cost matter more | Alias for latest Sonnet in Claude Code. |
| `opusplan` | Plan with Opus, execute with Sonnet | Useful for longer work where architecture quality matters but execution cost should be lower. |
| `haiku` | Simple or latency-sensitive tasks | Fast model for small tasks. |

## Effort Levels

- `high` - Default on Fable 5 and Opus 4.8 (2026-06-09); the default for coding and agentic tasks.
- `xhigh` - Extended depth for the most capability-sensitive work; was the Opus 4.7 default.
- `medium` - Standard implementation, cleanup, and bounded analysis.
- `low` - Short, scoped, latency-sensitive work; on Fable 5 still exceeds prior generations' `xhigh`.
- `max` - Deepest reasoning; use only when explicitly requested because it can overthink and spend more. Historically Opus 4.6 only — verify at execution time.

## Following Up

- Continue the most recent session in the current directory with:

```bash
claude --continue -p "new prompt"
```

- Resume a specific session with:

```bash
claude --resume <session-id> -p "new prompt"
```

- Do not add fresh model, effort, or permission flags on resume unless the user explicitly asks to change them.
- Restate the chosen model, effort, and permission mode when proposing follow-up actions.

## Error Handling

- Check `claude --version` and `claude auth status --text` when auth or CLI availability is uncertain.
- If flag syntax fails, run `claude --help`; Claude Code supports `--effort`, not Codex's `-c model_reasoning_effort=...` syntax.
- If model selection is uncertain, prefer `--model opus` over a stale full model ID.
- If permissions block a non-interactive run, retry with a narrower `--allowedTools` rule or ask before using `--dangerously-skip-permissions`.
- If MCP, hooks, or plugins are causing noisy startup failures and the task does not need them, consider `--bare` only when `ANTHROPIC_API_KEY` or an `apiKeyHelper` is available. `--bare` skips OAuth/keychain/Claude Max auth.
- If project-local hooks are noisy but Claude Max auth is needed, prefer `--setting-sources user` over `--bare`.

## CLI Version

Source check 2026-06-09: Claude Code v2.1.111+ documents `xhigh` effort (default on Opus 4.7), and v2.1.154 added Opus 4.8 (supports `xhigh`, defaults to `high`). The Claude Code version gate for Claude Fable 5 is not yet documented here — verify against the current Claude Code changelog at execution time. Check version:

```bash
claude --version
```

Configure durable defaults in `~/.claude/settings.json`, project defaults in `.claude/settings.json`, and local project overrides in `.claude/settings.local.json`. Use `/model` and `/effort` inside an interactive Claude Code session to inspect or change active settings.

## Common Gotchas

| Symptom | Cause | Fix |
| --- | --- | --- |
| Unexpected old model | Full model ID was pinned and became stale | Use `--model opus` or recheck official Anthropic model docs. |
| Effort flag ignored or lowered | Active model does not support requested level | Use a model that supports the requested level (Fable 5 and Opus 4.8/4.7 support `xhigh` — verify at execution time), or accept fallback to the highest supported level. |
| Non-interactive run stalls on permissions | Tool permission prompts cannot be answered | Use `--permission-mode plan`, narrower `--allowedTools`, or explicit bypass with approval. |
| Too much noisy setup | Hooks, plugins, MCP, or skills load during scripted run | Use `--bare` only with API-key auth; otherwise fix or bypass the noisy hook/plugin. |
| Project hook warning after a good answer | Project-local `.claude` hook path is stale | Use `--setting-sources user` for sidecar runs or repair the project hook. |
| Wrong mental model from Codex | Codex and Claude flags differ | Claude uses `--effort`; Codex uses `-c model_reasoning_effort=...`. |
