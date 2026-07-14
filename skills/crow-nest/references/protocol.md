# Codex App-Server JSON-RPC Protocol Reference

Crow's Nest is a read-only client of `codex app-server`. This document
captures only the subset Crow's Nest uses. Full spec:
https://developers.openai.com/codex/app-server.

> The app-server is marked **experimental** in the CLI. Method names and
> capability flags may change. The version this skill targets is
> `codex-cli 0.134.0`, checked locally on 2026-06-10 with
> `REAL_CODEX=1 codex app-server --help` and
> `REAL_CODEX=1 codex app-server generate-json-schema --experimental`.

## Transport

- **Default**: stdio JSON-RPC 2.0. Each message is one JSON object per
  line, terminated by `\n`.
- **Optional**: websocket via `codex app-server --listen
  ws://127.0.0.1:4500`. Non-loopback websocket requires
  capability-token auth (see Auth below).

## Initialize handshake

Client sends:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "capabilities": { "experimentalApi": true },
    "clientInfo": { "name": "crow-nest", "version": "1.0.0" }
  }
}
```

Server responds:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "serverInfo": { "name": "codex-app-server", "version": "..." },
    "capabilities": {
      "experimentalApi": true,
      "fsWatch": true,
      "skills": true
    }
  }
}
```

Client then sends:

```json
{ "jsonrpc": "2.0", "method": "initialized", "params": {} }
```

(notification, no id, no response)

## Methods Crow's Nest may document, but reference client does not call

The reference `crow-nest.ts` sends only the initial `initialize`
handshake. It does not call the methods below by default because the
dashboard must not attach to, resume, start, interrupt, or steer a Codex
thread. Treat these as protocol notes for deliberate local extensions.

### `thread/list`

```json
{ "jsonrpc": "2.0", "id": 2, "method": "thread/list", "params": {} }
```

Response:

```json
{
  "result": {
    "threads": [
      {
        "threadId": "tid_abc123",
        "title": "...",
        "createdAt": "2026-05-08T11:14:23Z",
        "lastTurnAt": "2026-05-08T11:18:02Z"
      }
    ]
  }
}
```

### `thread/resume`

Potentially attaches to an existing thread. The reference Crow's Nest does
NOT call this; attaching is outside the read-only default.

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "thread/resume",
  "params": { "threadId": "tid_abc123" }
}
```

Response:

```json
{
  "result": {
    "threadId": "tid_abc123",
    "model": "gpt-5.2",
    "sandbox": "workspace-write",
    "lastTurn": 124
  }
}
```

### `thread/goal/get` *(experimental)*

Requires `capabilities.experimentalApi: true` in the initialize.

```json
{ "jsonrpc": "2.0", "id": 4, "method": "thread/goal/get", "params": {} }
```

Response:

```json
{
  "result": {
    "state": "pursuing",
    "objective": "Build a playable dungeon-crawler MVP. ...",
    "tokensUsed": 412345,
    "budget": 1000000,
    "turn": 124
  }
}
```

`state` is one of `pursuing`, `paused`, `achieved`, `unmet`,
`budget-limited`. If goal mode is not active, the server returns an
error (`-32601` method not found if `experimentalApi` was not
negotiated, or `-32602` if no goal in this directory).

### `model/list` and `skills/list`

For pane status only.

## Notifications Crow's Nest consumes

Notifications have no `id`. Crow's Nest does not respond to them.

| Notification | Params (subset) | Action |
|---|---|---|
| `turn/started` | `{ threadId, turn }` | increment counter |
| `turn/completed` | `{ threadId, turn, tokensUsed }` | refresh tokens |
| `turn/plan/updated` | `{ threadId, plan: [...] }` | show in pane focus |
| `item/agentMessage/delta` | `{ threadId, delta }` | buffer into latest line |
| `item/completed` | `{ threadId, itemId, type }` | mark line complete |
| `thread/status/changed` | `{ threadId, goalState }` | update goal-state badge |

## Approval requests (server-initiated requests, not notifications)

These are JSON-RPC **requests** with an `id` — the server is asking the
client to respond.

```json
{
  "jsonrpc": "2.0",
  "id": 42,
  "method": "item/commandExecution/requestApproval",
  "params": {
    "threadId": "tid_abc123",
    "itemId": "item_xyz",
    "command": "rm -rf node_modules",
    "description": "Delete node_modules to free space?"
  }
}
```

Crow's Nest's policy: **surface, never respond**. The human approves or
declines in the original Codex session. This avoids turning the dashboard
into a control surface.

## Auth (websocket only)

For `--listen ws://...` non-loopback transport, the server expects a
`capability-token` in the WebSocket handshake's `Authorization` header
or in a query string when `--ws-auth capability-token` is selected.
Provide the token material with `--ws-token-file` or
`--ws-token-sha256`. Local help for `codex-cli 0.134.0` also documents
`--ws-auth signed-bearer-token` with shared-secret, issuer, audience,
and clock-skew options.

Default Crow's Nest mode is **stdio child processes**, which inherit
the parent's auth context — no separate token needed.

## Error model

Standard JSON-RPC 2.0 errors plus Codex-specific codes:

| Code | Meaning |
|---|---|
| `-32601` | Method not found (often: `experimentalApi` not negotiated) |
| `-32602` | Invalid params (often: thread not found / no active goal) |
| `-32603` | Internal error |
| `-30001` | Capability disabled |
| `-30002` | Sandbox violation |

## References

- [Codex App-Server docs](https://developers.openai.com/codex/app-server)
- [openai/codex/codex-rs/app-server README](https://github.com/openai/codex/blob/main/codex-rs/app-server/README.md)
- [CodexMonitor source](https://github.com/Dimillian/CodexMonitor) — Tauri client implementing this protocol
- [Sonol Multi-Agent](https://github.com/volition79/sonol-multi-agent) — local-first dashboard
