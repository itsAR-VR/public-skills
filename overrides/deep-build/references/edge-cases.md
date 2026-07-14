# Edge Cases and Recovery

Known failure modes for Deep Build and how to handle them.

---

## No Plan Exists

**Symptom:** `docs/planning/` is empty or has no incomplete phases.

**Recovery:**
1. STOP — deep-build does NOT create plans
2. Inform user: "No plan found. Run `/deep-sweep` first to create one."
3. Do not proceed to any gear

---

## OpenAI-Family Verifier Route Unavailable

**Symptom:** The active harness cannot route an OpenAI-family verifier. Examples:
Codex main harness has no native sub-agent route, Claude Code cannot find a usable
Codex CLI, or the local Codex CLI rejects the current hardcoded model.

**Recovery:**
1. Identify active harness first.
2. If active harness is Codex: use native sub-agents only; never call nested `codex exec`, MCP, or shell fallback.
3. If active harness is Claude Code: check `which -a codex`, each candidate's `codex --version`, and support for the current `OPENAI_LATEST_MODEL` value.
   If multiple binaries exist, set `CODEX_BIN` to the highest supported version before invoking CLI.
4. If the latest OpenAI model is unsupported: upgrade Codex or stop and report the unsupported model. Do not downgrade.
5. If no valid route exists: ask user before **degraded mode**.
6. Degraded mode: replace OpenAI-family passes with a second primary-model agent using a "devil's advocate" prompt. Note clearly that this is not cross-model verification.
7. When CLI routing is valid, never pipe large content via stdin — write diffs/plans to /tmp/ and let Codex read from disk.

---

## Implementation Agent Blocked

**Symptom:** impl-{sub} agent reports BLOCKED.

**Recovery:**
1. Read the block reason from the agent's output
2. Common blocks and resolutions:
   - **Missing env var** → note, ask user to provide
   - **Missing dependency** → install it, re-run agent
   - **Plan unclear** → refer to eng-review findings
   - **File locked by another agent** → wait, retry
   - **Build fails** → diagnose, fix, retry
3. If unresolvable: mark subphase as BLOCKED in plan, skip to next
4. Report all blocked subphases to user at end

---

## OpenAI-Family Verifier Finds CRITICAL Bug (Fix Loop)

**Symptom:** OpenAI-family verification finds a CRITICAL issue in the diff.

**Recovery:**
1. Spawn fix agent for that subphase:
   ```
   Agent(name: "fix-{sub}", model: "<active-primary-model>", prompt: "Fix this CRITICAL issue: ...")
   ```
2. Re-run OpenAI-family verification on the fix
3. If still CRITICAL: try once more with more context
4. **Max 3 fix attempts.** After 3: escalate to user
5. Do not proceed to next gear with unresolved CRITICALs

---

## Cross-Monitor Detects Conflict

**Symptom:** cross-monitor agent reports file/type/data conflict between subphases.

**Recovery:**
1. Determine which subphase should "win" (usually the later-completing one)
2. Spawn a merge agent:
   ```
   Agent(name: "merge-{subA}-{subB}", prompt: "Resolve conflict between...")
   ```
3. Re-run cross-monitor to verify resolution
4. If circular: escalate to user — may need plan restructure

---

## QA Failure Loop

**Symptom:** A QA layer keeps failing after fixes.

**Recovery:**
1. **Max 3 retries per layer.** Track retry count.
2. After 3 retries:
   - Collect all failure evidence (screenshots, logs, test output)
   - Present to user with: "Layer {N} failed 3x. Issues: {list}"
   - Ask: fix manually, skip this layer, or abort build
3. Never loop indefinitely on QA failures

---

## Browser Tools Unavailable

**Symptom:** Claude-in-Chrome MCP tools fail or Chrome is not open.

**Recovery:**
1. Check: call `mcp__claude-in-chrome__tabs_context_mcp` — if error, browser not connected
2. **Fallback chain:**
   a. Try Browser Harness MCP tools (`mcp__plugin_browser-harness_browser-harness__*`)
   b. Try Browser Harness CLI (`npx browser-harness test`)
   c. Fall back to CLI-only QA (test suite + OpenAI-family analysis)
3. Note in QA results: "Visual/functional QA skipped — browser tools unavailable"
4. Layer 1 (tests) and Layer 4 (OpenAI-family verifier) still run

---

## Phase Plan Stale/Outdated

**Symptom:** Plan references files that have been renamed/deleted, or codebase
has diverged significantly since plan was created.

**Recovery:**
1. Detected during Gear 1 (Validate Plan):
   - OpenAI-family quick-check finds phantom references
   - `git log --since` shows significant changes
2. Options:
   a. Recommend user runs `/deep-sweep` to refresh the plan
   b. Proceed with caveats (user's choice)
   c. Auto-update plan references (risky — may miss intent changes)
3. Default: recommend `/deep-sweep` refresh

---

## Parallel Agent Timeout

**Symptom:** An implementation agent doesn't return within expected time.

**Recovery:**
1. Primary-model implementation agents: allow up to 15 minutes (complex subphases)
2. OpenAI-family verification: allow up to 5 minutes
3. QA agents: allow up to 10 minutes
4. If timeout:
   - Note the missing work
   - Check git status — agent may have partially committed
   - Proceed with available results
   - Mark affected subphase with lower confidence

---

## Context Degradation in Long Builds

**Symptom:** Later gears produce lower-quality work because context is compressed.

**Prevention:**
1. Each agent gets focused context (not full conversation)
2. All findings written to disk (phase plan files)
3. Later agents read from disk, not conversation
4. Keep conversation-level context minimal

**Recovery:**
1. If quality drops: re-read phase plan from disk
2. If severe: spawn fresh agents that read from disk
3. Use `$context-compression` techniques if needed

---

## Git Conflicts with Concurrent Work

**Symptom:** `git status` shows changes from other agents/sessions.

**Recovery:**
1. Detected during Gear 0 (Preflight)
2. Deep-build ONLY touches files in its phase's scope
3. If overlap: warn user, document in plan
4. Never modify files outside the current phase's scope
5. If merge conflict: attempt auto-resolve, escalate if ambiguous

---

## Dev Server Not Running

**Symptom:** Functional QA can't connect to localhost.

**Recovery:**
1. Check if dev server should be running: look for `dev` script in package.json
2. Start it: `npm run dev &` or equivalent
3. Wait for ready signal (poll localhost until 200)
4. If can't start: skip Layer 2 + 3, run Layer 1 + 4 only
5. Note in QA results: "Visual/functional QA skipped — dev server unavailable"

---

## Single Subphase (No Parallelism Needed)

**Symptom:** Plan has only one subphase.

**Recovery:**
1. Still run the full pipeline — single lane is fine
2. Skip cross-monitor (nothing to compare)
3. All 4 QA layers still run
4. The value is the OpenAI-family cross-verification, not parallelism
