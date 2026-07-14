---
name: granola-transcript
description: "Retrieve and search Granola meeting transcripts/notes for AR. Auto-activates on any intent related to meeting content, call notes, transcripts, or discussion recall — not just keyword matching."
version: "2.0.0"
author: podhi
tags:
  - meetings
  - transcripts
  - granola
  - ar-context
related_skills:
  - meeting-insights-analyzer
  - openai-whisper-api
  - autoresearch
intent_routing:
  mode: semantic
  description: >
    Route to this skill when AR's message expresses INTENT to recall, retrieve,
    reference, or act on meeting/call content. This includes implicit references
    like "what did we agree on", "follow up on that call", "the thing from the
    standup", or any context where AR is clearly referencing a conversation that
    was recorded. Do NOT rely solely on keyword matching — use semantic intent.
  positive_signals:
    - Asking about what was discussed/decided/agreed in a meeting or call
    - Referencing action items, follow-ups, or decisions from a conversation
    - Asking for a summary or recap of a meeting
    - Mentioning a specific person + context that implies a meeting occurred
    - Date-based references to calls ("yesterday's sync", "this morning's call")
    - Requests to "pull up", "find", "check" notes from a conversation
    - Questions about who said what or who attended
    - Requests to prepare for a follow-up based on a previous meeting
    - "What's on my plate from [meeting context]"
    - "Did [person] mention [topic]"
    - Any phrasing where the user expects transcript-sourced information
  negative_signals:
    - Mo asking for transcripts (route to Fireflies)
    - Video/YouTube transcript requests (route to whisper/video-transcript)
    - Requests about meetings that haven't happened yet (route to calendar)
    - Generic productivity questions not tied to a specific recorded conversation
  confidence_threshold: 0.6
---

# Granola Transcript Skill

## Purpose

Retrieve meeting transcripts, notes, and summaries from Granola.ai for AR.
AR uses Granola for meeting recording/transcription. This skill activates
when the agent detects AR is referencing or asking about meeting content,
using semantic intent matching rather than rigid keyword triggers.

> **Mo uses Fireflies, not Granola.** If Mo asks for transcript/meeting content,
> route to the Fireflies integration (`integrations/fireflies/`) instead.

## Routing Logic

This skill uses **intent-based routing**, not keyword matching. The agent should
activate this skill when:

1. **Direct requests:** "get the transcript", "pull meeting notes", "check granola"
2. **Implicit recall:** "what did we discuss about pricing?", "any follow-ups from the sync?"
3. **Contextual reference:** AR mentions a meeting and asks about its content or outcomes
4. **Action tracking:** "what did I agree to do?", "what's outstanding from that call?"
5. **Preparation:** "brief me before the follow-up with [person]" (implies prior meeting exists)
6. **Attribution:** "did Sarah say she'd handle the API?", "who was responsible for X?"

The routing should be **aggressive but precise** — when there's a >60% chance AR
is referencing a recorded conversation, activate this skill. False positives are
cheaper than missed recalls.

## MCP Integration — Operational Path

### Primary: Granola MCP app tools (recommended)

Use the configured Granola MCP server/app when available: `query_granola_meetings`,
`list_meetings`, `get_meetings`, or `get_meeting_transcript`.

### Legacy: Direct MCP Client (external helper scripts only)

Uses streamable-http (POST) directly against Granola's endpoint. This path only
applies when the external helper scripts are installed; they are not shipped
with this skill.

- **Script:** `integrations/granola-mcp-server/granola-mcp-client.sh` (external)
- **Token:** `~/.granola-mcp-token` (Bearer access_token from OAuth2)
- **Endpoint:** `https://mcp.granola.ai/mcp` (POST only, 405 on GET)

```bash
# Check status
bash integrations/granola-mcp-server/granola-mcp-client.sh status

# Search meetings
bash integrations/granola-mcp-server/granola-mcp-client.sh search "standup"

# Get recent meetings
bash integrations/granola-mcp-server/granola-mcp-client.sh recent 5

# Get full meeting content
bash integrations/granola-mcp-server/granola-mcp-client.sh content <meeting_id>

# List available tools
bash integrations/granola-mcp-server/granola-mcp-client.sh tools
```

### Fallback: mcporter (when registered)

- **Server name:** `granola` (in mcporter)
- If mcporter transport negotiation fails with a 405 from Granola's POST-only
  endpoint, use the host MCP app tools instead.
- If bearer auth is already configured, mcporter `call` may work even if an
  interactive auth flow does not.

```bash
mcporter call granola search_meetings '{"query": "standup", "limit": 5}'
mcporter call granola get_meeting_content '{"meeting_id": "<id>"}'
```

## Available Tools (when authenticated)

| Tool | Description | Parameters |
|------|-------------|------------|
| `search_meetings` | Search meetings by title/content | `query`, `limit?` (default: 10) |
| `get_meeting_details` | Get meeting metadata | `meeting_id` |
| `get_meeting_content` | Get full notes as Markdown | `meeting_id` |
| `list_workspaces` | List all workspaces | — |
| `list_folders` | List document folders | `workspace_id?` |
| `filter_by_workspace` | Filter meetings by workspace | `workspace_id` |
| `filter_by_folder` | Filter meetings by folder | `folder_id` |

For host MCP app tools, use the live schema instead of the legacy names above.

## Retrieval Workflow

### Step 1: Check auth status

```bash
bash integrations/granola-mcp-server/granola-mcp-client.sh status
```

If using host MCP app tools, proceed when the tool call succeeds. If auth is
missing or expired, use the Setup/Auth section below.

### Step 2: Search for the meeting

Use `search` with the best query derived from the user's request:

- **Date reference:** "yesterday's standup" → search "standup" + filter by date
- **Topic reference:** "the pricing discussion" → search "pricing"
- **Person reference:** "meeting with Sarah" → search "Sarah"
- **Vague reference:** "the last call" → use `recent 5`

```bash
bash integrations/granola-mcp-server/granola-mcp-client.sh search "pricing"
```

### Step 3: Get full content

Once the meeting is identified:

```bash
bash integrations/granola-mcp-server/granola-mcp-client.sh content "<meeting_id>"
```

With host MCP app tools, use `get_meetings` or `get_meeting_transcript`.

### Step 4: Return structured output

Always return:
1. **Meeting title** and date
2. **Summary** (2-3 sentences)
3. **Key discussion points** (bullet list)
4. **Action items** (if present)
5. **Participants** (if available)

## Disambiguation

When the search returns multiple matches and the user's intent is ambiguous:
1. Present top 3-5 matches with title + date + snippet
2. Ask AR to pick which one
3. Do NOT guess — meeting context matters too much to get wrong

When the search returns zero matches:
1. Try broader search terms (remove date qualifiers, simplify query)
2. List recent meetings if the user said "recent" or "last"
3. Report clearly: "No Granola meetings match that query. Want me to try a broader search?"

## Setup — Host MCP/App Auth

The Granola MCP integration requires one human login/reconnect step when the
host reports missing or expired auth.

### Steps:

1. Open the current host's Granola MCP/app connection settings.
2. Connect or reconnect Granola in a browser where AR is logged into Granola.
3. Return to the agent host and retry the same Granola tool call.
4. The host stores auth in its MCP/app configuration.
   - Do not print or copy tokens, cookies, or OAuth state.
   - For mcporter, use its own config only if `granola` is manually registered.
5. Retry `query_granola_meetings` or `list_meetings`.

**This is the ONLY human step. Everything else is automated.**

## Error Handling

| Error | Action |
|-------|--------|
| Granola tool unavailable | Reconnect or enable the Granola MCP app/server in the current host |
| Auth expired (401) | Reconnect the Granola app/server, then retry |
| No meetings found | Broaden search, or list recent meetings |
| Rate limited | Wait and retry (Granola API is generous) |
| MCP endpoint unreachable | Check network; endpoint is `https://mcp.granola.ai/mcp` |

## Output Contract

When returning transcript data, always structure as:

```markdown
## Meeting: <title>
**Date:** <date>
**Participants:** <list or "not available">

### Summary
<2-3 sentence summary>

### Key Points
- <point 1>
- <point 2>

### Action Items
- [ ] <action 1> — <owner if known>
- [ ] <action 2> — <owner if known>

### Full Notes
<collapsed or linked if very long>
```
