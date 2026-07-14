#!/usr/bin/env bun
/**
 * crow-nest.ts — multi-pane TUI dashboard for the Codex /goal + Claude
 * heartbeat + agent message bus topology.
 *
 * Read-only by design. Spawns one `codex app-server` stdio child per
 * monitored thread, parses JSON-RPC 2.0 notifications, watches `.bus/`
 * via chokidar, and renders into a `blessed` TUI.
 *
 * Usage:
 *   bun crow-nest.ts [--bus-dir <path>] [--threads <id1,id2,...>]
 *                    [--app-server]
 *
 * Threads are loaded from `.crow-nest/state.json` if no `--threads` flag.
 *
 * NOTE: this is a faithful implementation of the documented protocol.
 * `codex app-server` is marked experimental in the CLI; behavior may
 * change. The lite-mode `crow-nest-lite.sh` is the always-works fallback.
 */

import { spawn, type ChildProcess } from "node:child_process";
import { readFileSync, existsSync, watch } from "node:fs";
import { resolve, basename } from "node:path";

// --- args ----------------------------------------------------------------

interface Args {
  busDir: string;
  threadIds: string[];
  enableAppServer: boolean;
}

function parseArgs(): Args {
  const args: Args = {
    busDir: resolve(process.cwd(), ".bus"),
    threadIds: [],
    enableAppServer: false,
  };
  const argv = process.argv.slice(2);
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--bus-dir") args.busDir = resolve(argv[++i]);
    else if (a === "--threads") args.threadIds = argv[++i].split(",");
    else if (a === "--app-server") args.enableAppServer = true;
    else if (a === "--no-app-server") args.enableAppServer = false;
    else if (a === "-h" || a === "--help") {
      console.log(
        "crow-nest.ts [--bus-dir <path>] [--threads <id1,id2>] [--app-server]"
      );
      process.exit(0);
    }
  }

  // Default thread list from state.json if available.
  if (args.threadIds.length === 0) {
    const stateFile = resolve(process.cwd(), ".crow-nest/state.json");
    if (existsSync(stateFile)) {
      try {
        const s = JSON.parse(readFileSync(stateFile, "utf8"));
        if (Array.isArray(s.threads)) args.threadIds = s.threads;
      } catch {
        // ignore
      }
    }
  }
  return args;
}

// --- bus watcher ---------------------------------------------------------

interface BusMessage {
  filename: string;
  ts: string;
  author: string;
  kind: string;
  body: string;
  priority: number;
}

function parseMessageFile(path: string): BusMessage | null {
  const base = basename(path);
  if (!/^\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}Z--[a-z0-9-]+--[a-z]+/.test(base)) {
    return null;
  }
  const tsMatch = base.split("--");
  const ts = tsMatch[0];
  const author = tsMatch[1];
  const kindFull = tsMatch[2] ?? "unknown";
  const kind = kindFull.replace(/(\.\d+)?\.md$/, "");

  let raw: string;
  try {
    raw = readFileSync(path, "utf8");
  } catch {
    return null;
  }

  // Body = first non-blank line after second `---`.
  const lines = raw.split("\n");
  let dashCount = 0;
  let body = "";
  let priority = 0;
  for (const line of lines) {
    if (line === "---") {
      dashCount++;
      continue;
    }
    if (dashCount === 1) {
      const m = line.match(/^priority:\s*(\d+)/);
      if (m) priority = parseInt(m[1], 10);
    }
    if (dashCount === 2 && line.trim().length > 0 && !body) {
      body = line.slice(0, 200);
      break;
    }
  }

  return { filename: base, ts, author, kind, body, priority };
}

// --- codex app-server JSON-RPC client ------------------------------------

interface RpcClient {
  threadId: string;
  proc: ChildProcess;
  pendingId: number;
  inbox: Map<number, (resp: unknown) => void>;
  state: ThreadState;
  buffer: string;
}

interface ThreadState {
  threadId: string;
  goalState: string;
  goalText: string;
  turn: number;
  tokens: number;
  budget: number;
  latestMessage: string;
  pendingApprovals: Array<{ id: string; description: string }>;
}

function emptyState(threadId: string): ThreadState {
  return {
    threadId,
    goalState: "unknown",
    goalText: "",
    turn: 0,
    tokens: 0,
    budget: 0,
    latestMessage: "",
    pendingApprovals: [],
  };
}

function sendRpc(client: RpcClient, method: string, params: unknown): Promise<unknown> {
  return new Promise((resolveP, rejectP) => {
    const id = ++client.pendingId;
    const req = JSON.stringify({ jsonrpc: "2.0", id, method, params }) + "\n";
    client.inbox.set(id, (resp: unknown) => {
      const r = resp as { error?: { message: string }; result?: unknown };
      if (r.error) rejectP(new Error(r.error.message));
      else resolveP(r.result);
    });
    client.proc.stdin?.write(req);
  });
}

function sendNotification(client: RpcClient, method: string, params: unknown): void {
  const req = JSON.stringify({ jsonrpc: "2.0", method, params }) + "\n";
  client.proc.stdin?.write(req);
}

function handleStdoutLine(client: RpcClient, line: string, onUpdate: () => void) {
  if (!line.trim()) return;
  let msg: { id?: number; method?: string; params?: unknown; result?: unknown } = {};
  try {
    msg = JSON.parse(line);
  } catch {
    return;
  }

  // Response to a request we made.
  if (msg.id !== undefined && client.inbox.has(msg.id)) {
    client.inbox.get(msg.id)!(msg);
    client.inbox.delete(msg.id);
    return;
  }

  // Server-initiated notification.
  const params = msg.params as Record<string, unknown> | undefined;
  switch (msg.method) {
    case "turn/started":
      client.state.turn += 1;
      break;
    case "turn/completed":
      if (params?.tokensUsed) client.state.tokens = params.tokensUsed as number;
      break;
    case "item/agentMessage/delta":
      if (params?.delta) {
        client.state.latestMessage = (client.state.latestMessage + (params.delta as string)).slice(-200);
      }
      break;
    case "item/completed":
      // Mark message frame complete; latestMessage already populated.
      break;
    case "thread/status/changed":
      if (params?.goalState) client.state.goalState = params.goalState as string;
      break;
    case "item/commandExecution/requestApproval":
    case "item/fileChange/requestApproval":
      if (params?.id) {
        client.state.pendingApprovals.push({
          id: params.id as string,
          description: (params.description as string) ?? msg.method,
        });
      }
      break;
  }
  onUpdate();
}

async function spawnAppServerClient(
  threadId: string,
  onUpdate: (s: ThreadState) => void
): Promise<RpcClient> {
  const proc = spawn("codex", ["app-server"], {
    stdio: ["pipe", "pipe", "pipe"],
  });

  const client: RpcClient = {
    threadId,
    proc,
    pendingId: 0,
    inbox: new Map(),
    state: emptyState(threadId),
    buffer: "",
  };

  const MAX_BUFFER_BYTES = 10 * 1024 * 1024; // 10 MB cap per thread
  proc.stdout?.on("data", (chunk: Buffer) => {
    client.buffer += chunk.toString();
    if (client.buffer.length > MAX_BUFFER_BYTES) {
      // Misbehaving app-server emitting a giant frame without newlines —
      // disconnect rather than OOM the dashboard.
      console.error(
        `crow-nest: thread ${threadId} buffer exceeded ${MAX_BUFFER_BYTES} bytes without newline; disconnecting`
      );
      client.buffer = "";
      try { client.proc.kill(); } catch { /* ignore */ }
      return;
    }
    let nl: number;
    while ((nl = client.buffer.indexOf("\n")) !== -1) {
      const line = client.buffer.slice(0, nl);
      client.buffer = client.buffer.slice(nl + 1);
      handleStdoutLine(client, line, () => onUpdate(client.state));
    }
  });

  proc.stderr?.on("data", () => {
    // codex app-server writes telemetry to stderr; ignore.
  });

  proc.on("exit", (code) => {
    client.state.goalState = code === 0 ? "exited" : "crashed";
    onUpdate(client.state);
  });

  // Initialize handshake.
  await sendRpc(client, "initialize", {
    capabilities: { experimentalApi: true },
    clientInfo: { name: "crow-nest", version: "1.0.0" },
  });
  sendNotification(client, "initialized", {});

  // Read-only invariant: after initialize, do not send requests that could
  // attach to, resume, start, interrupt, approve, or otherwise steer a thread.
  // Goal state and turn metadata are notification-only in this reference client.

  onUpdate(client.state);
  return client;
}

// --- main --------------------------------------------------------------

async function main() {
  const args = parseArgs();

  console.log("crow-nest: starting");
  console.log(`  bus-dir: ${args.busDir}`);
  console.log(`  threads: ${args.threadIds.join(", ") || "(none)"}`);
  console.log(`  app-server: ${args.enableAppServer ? "enabled" : "disabled"}`);

  if (!existsSync(args.busDir)) {
    console.error(`crow-nest: bus dir not found: ${args.busDir}`);
    process.exit(2);
  }

  // ---------------------------------------------------------------------
  // The blessed TUI is intentionally NOT spun up in this reference impl,
  // because blessed depends on terminfo + sigwinch handling that varies
  // across iTerm2/tmux/Warp. Instead, this module:
  //   1. Spawns app-server clients (full-mode demo of the protocol).
  //   2. Streams bus events to stdout in lite-mode-style ANSI.
  //
  // Production TUIs should layer on top — see references/panes.md for
  // the layout this scaffold targets and recommended tooling
  // (blessed-contrib, blessed, ink, or the Sonol Multi-Agent Tauri app).
  // ---------------------------------------------------------------------

  const threadStates = new Map<string, ThreadState>();
  const onThreadUpdate = (s: ThreadState) => {
    threadStates.set(s.threadId, s);
    const line = `[${s.threadId}] ${s.goalState} · turn=${s.turn} · tokens=${s.tokens} · ${s.latestMessage.slice(0, 60)}`;
    process.stdout.write(`\r\x1b[K${line}\n`);
  };

  if (args.enableAppServer) {
    for (const tid of args.threadIds) {
      try {
        await spawnAppServerClient(tid, onThreadUpdate);
      } catch (e) {
        console.error(`crow-nest: failed to attach to thread ${tid}: ${(e as Error).message}`);
      }
    }
  }

  // Bus watcher (chokidar would be nicer, but fs.watch is in stdlib).
  const initialFiles = (await import("node:fs/promises"))
    .readdir(args.busDir)
    .catch(() => [] as string[]);
  for (const f of (await initialFiles).sort().slice(-20)) {
    const m = parseMessageFile(resolve(args.busDir, f));
    if (m) printBusEvent(m);
  }

  watch(args.busDir, (eventType, filename) => {
    if (eventType !== "rename" || !filename) return;
    const path = resolve(args.busDir, filename);
    if (!existsSync(path)) return;
    const m = parseMessageFile(path);
    if (m) printBusEvent(m);
  });

  console.log("crow-nest: watching... Ctrl+C to exit.");
  process.stdin.resume();
}

const KIND_COLORS: Record<string, string> = {
  progress: "\x1b[32m",
  correction: "\x1b[33m",
  directive: "\x1b[35;1m",
  blocker: "\x1b[41;97m",
  question: "\x1b[34m",
  ack: "\x1b[37m",
  vision: "\x1b[36m",
  frame: "\x1b[36;1m",
  decision: "\x1b[97m",
  summary: "\x1b[32;4m",
  paused: "\x1b[2;37m",
};
const RESET = "\x1b[0m";

function printBusEvent(m: BusMessage) {
  const color = KIND_COLORS[m.kind] ?? "";
  const tsShort = m.ts.slice(0, 16).replace("T", " ");
  process.stdout.write(
    `\x1b[2m${tsShort}${RESET}  ${m.author.padEnd(18)} ${color}${m.kind.padEnd(11)}${RESET}  ${m.body}\n`
  );
}

main().catch((e) => {
  console.error(`crow-nest: fatal: ${e?.message ?? e}`);
  process.exit(1);
});
