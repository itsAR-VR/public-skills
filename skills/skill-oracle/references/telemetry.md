# skill-oracle — Telemetry Hook

Load this file ONLY when SKILL_ORACLE_TELEMETRY is set to a truthy value in the
environment. Telemetry is observation-only and never changes routing output.

## Step 6.5 — TELEMETRY HOOK (silent observability)

After Step 6 returns the recommended skills, write one append-only line to the
per-month telemetry file. This is observation only; it never changes what was
returned to the caller.

Path: `$HOME/.claude/skill-oracle-telemetry/YYYY-MM.jsonl` (one file per month,
where YYYY-MM is the current UTC year-month — e.g.
`$HOME/.claude/skill-oracle-telemetry/2026-05.jsonl` for May 2026).

### PRIVACY — read this before enabling

The telemetry log captures the user's raw `task` string and (when the host-agent
fallback fires) the full `host_response_raw` text. These fields can contain:

- Personal/customer names, emails, internal project codenames, business
  context the user typed
- Sensitive snippets the LLM emitted while reasoning about routing

The files are local to `$HOME/.claude/`. They are NOT uploaded anywhere by this
skill. **But:** if your home directory is backed up, synced to cloud storage,
inside a tarball you share, or scraped by another telemetry/forwarding system,
this data goes with it. Treat the telemetry directory as you would chat logs.

**Hardening recommendations:**

1. **Opt out hard** if you don't need the data: set `SKILL_ORACLE_TELEMETRY=0`
   in the environment. The host agent MUST short-circuit and skip the write
   when this var is `0`, `false`, or empty-after-strip. Treat the opt-out as
   the first condition of the hook block.
2. **Truncate** the `task` field at 200 chars in the write step if you want
   smaller blast radius. The raw value is rarely needed past the headline.
3. **Skip `host_response_raw`** unless `SKILL_ORACLE_TELEMETRY_VERBOSE=1` is
   set. The host's full reasoning text is the highest-sensitivity field; it's
   off by default in this recommendation but the schema below shows it
   populated for completeness.
4. **Gitignore** `~/.claude/skill-oracle-telemetry/` if any part of `$HOME` is
   ever committed to a repo.
5. **Rotate** monthly files older than a retention window you choose; the
   monthly partitioning makes this trivial (`rm $HOME/.claude/skill-oracle-telemetry/YYYY-MM.jsonl`).

### Schema

One JSON object per line, no trailing newline inside the object:

```json
{
  "ts": "2026-05-19T12:34:56Z",
  "session_id": "$CLAUDE_SESSION_ID or unknown",
  "task": "<the user's task string — see PRIVACY above>",
  "A_top5": [{"skill": "name", "score": 18.5}, ...],
  "fired_fallback": false,
  "fallback_reason": null,
  "host_top5": null,
  "host_response_raw": null,
  "validation_status": null,
  "latency_ms": {"L": 3, "S": 0, "total": 3},
  "accepted_skill": null
}
```

The `accepted_skill` field is left null at write time; a separate Stop hook (added
in a later phase) backfills it from the agent's subsequent skill invocation.

Implementation: enforce the `SKILL_ORACLE_TELEMETRY=0` opt-out check FIRST,
then append the JSON object plus a trailing newline. Create the directory and
the monthly file if missing. Use `mkdir -p` and `>>` for the write; no locking
needed because writes are line-atomic in POSIX append mode.

