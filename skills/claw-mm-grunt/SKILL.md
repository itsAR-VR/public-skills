---
name: claw-mm-grunt
description: >
  Run one-shot, non-interactive MiniMax repo analysis and audit tasks through
  the configured `claw-mm` prompt-mode wrapper. Use when the user wants cheap grunt-work
  passes like repo audits, dead-code scans, flaky-test reviews, file or symbol
  surveys, JSON summaries, or other read-mostly analysis without opening the
  interactive REPL.
---

# claw-mm-grunt

Use this skill when MiniMax should do cheap, disposable repo analysis through
`claw-mm`, not when the task needs an interactive coding session.

## Use for

- Read-only repo audits and review passes
- Enumerating risky files, stale code, flaky tests, naming drift, or missing coverage
- JSON or text summaries that can be consumed by another agent
- One-shot prompts where session continuity does not matter

## Do not use for

- Commits, multi-turn debugging, or interactive editing
- Any task where this main lane should stay the source of truth for changes
- Broad home-directory scans; prefer a specific repo root

## Default lane

1. Run the lightweight prereq check once:

   ```bash
   bash ~/.codex/skills/claw-mm-grunt/scripts/verify.sh
   ```

2. From the target repo root, run:

   ```bash
   bash ~/.codex/skills/claw-mm-grunt/scripts/run.sh "audit prompt here"
   ```

3. The helper defaults to:
   - `--permission-mode read-only`
   - `--output-format text`
   - `--compact`

4. Switch modes only when needed:
   - `--json` for machine-readable output
   - `--write` only if the user explicitly wants writable MiniMax work
   - `--cwd /abs/path/to/repo` if you are not already in the repo
   - `--prompt-file /abs/path/to/prompt.txt` for long prompts

## Prompt shape

Keep prompts scoped and explicit. Good default pattern:

```text
Audit the repository at the current working directory.
Focus on: <goal>.
Return:
1. Findings ordered by severity
2. Exact file paths and symbol names
3. Missing tests or validation gaps
4. Residual risk in 1 short paragraph
Keep the answer concise.
```

## Examples

Text mode:

```bash
bash ~/.codex/skills/claw-mm-grunt/scripts/run.sh \
  "Audit this repo for dead code and duplicated logic. Cite exact files and symbols."
```

JSON mode:

```bash
bash ~/.codex/skills/claw-mm-grunt/scripts/run.sh --json \
  "List the top 10 highest-risk files for test gaps as JSON with path, reason, and confidence."
```

Prompt file:

```bash
bash ~/.codex/skills/claw-mm-grunt/scripts/run.sh \
  --cwd /abs/path/to/repo \
  --prompt-file /tmp/minimax-audit.txt
```

## Verification and repair

- `verify.sh` is intentionally cheap: it checks `claw-mm`, the local `claw`
  binary, the MiniMax key file, and wrapper help without making a model call.
- If verification fails, repair the setup with the existing MiniMax install skill:

  ```bash
  bash ~/.codex/skills/minimax-setup/scripts/install.sh
  bash ~/.codex/skills/minimax-setup/scripts/verify.sh
  ```

## Notes

- `claw-mm` is the MiniMax wrapper; it forwards straight into the local
  `claw` binary with MiniMax auth and base URL pre-set.
- The underlying `claw` source of truth already supports non-interactive prompt
  mode plus `--compact`, `--output-format`, and `--permission-mode`. This skill
  stays thin on purpose.
