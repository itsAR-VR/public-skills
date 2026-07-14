#!/usr/bin/env python3
"""record_event.py — Phase 2 client wiring: emit one preference event after
skill-oracle returns a recommendation.

Each invocation:
  1. Resolves the local eval-repo clone (`$SKILL_ORACLE_EVAL_REPO`, else
     `~/.openclaw/public-skills-evals-private/`, else the dev clone path).
  2. Reads the cached identity at `~/.openclaw/skill-oracle/identity.json`
     (created by `bootstrap-client.sh`).
  3. Classifies the prompt into an intent cluster via `classify_cluster.py`.
  4. Builds an event matching the v1 schema in
     `docs/preference-schema.md` from the eval repo.
  5. Writes each draft's stack text to `outputs/evt-<id>-<a|b|c>.txt` so the
     validator's `--strict` mode (which hashes those files) passes.
  6. Atomically appends one line of JSON to `prefs/<github_user>.jsonl`.

Graceful degradation: if any prerequisite is missing (identity not bootstrapped,
eval repo absent, `prefs/` missing, disk full) the script prints a warning to
stderr and exits 0 so the calling skill-oracle workflow is never blocked. Each
warning includes a remediation hint (e.g., "run scripts/bootstrap-client.sh").

CLI examples:
    python3 record_event.py \
        --prompt "write a cold email to a Series B founder" \
        --drafts '[["cold-email","customer-research"],["cold-email","operator-spin","brand-voice"]]' \
        --winner A \
        --reason "tighter, leads with the routing problem"

    # Single-draft (typical skill-oracle case): the user took or skipped the
    # only recommendation. Use winner=A for "used it", BOTH_BAD for "didn't".
    python3 record_event.py \
        --prompt "build a landing page with pricing" \
        --drafts '[["landing-page-architecture","pricing-page-psychology-audit"]]' \
        --winner A
"""
from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Co-located helper. Import lazily-as-script so we work either as a CLI from
# this directory or when imported by another script in the same package.
_THIS_DIR = Path(__file__).resolve().parent
if str(_THIS_DIR) not in sys.path:
    sys.path.insert(0, str(_THIS_DIR))
from classify_cluster import classify  # noqa: E402

# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------

ROUTER_VERSION_TAG = "skill-oracle-v2.0.0-phase2"
"""Bumped whenever the event-emission contract changes. Independent of the
public-skills git SHA, which is captured separately in router_version's value."""

SCHEMA_VERSION = 1
DEFAULT_FILTER_MODE = "heuristic"
DEFAULT_FILTER_PARAMS = {
    "seed_score_threshold": 5.0,
    "min_score": 1.0,
    "hop_decay": 0.2,
}
TASK_PREVIEW_LEN = 80  # The schema doc specifies "first 80 characters".

_CANONICAL_CLIENT_CLONE = Path.home() / ".openclaw" / "public-skills-evals-private"
_DEV_FALLBACK_CLONE = Path.home() / "Desktop" / "Codespace" / "public-skills-evals-private"
_IDENTITY_FILE = Path.home() / ".openclaw" / "skill-oracle" / "identity.json"


# ----------------------------------------------------------------------------
# Result type — lets the calling skill know what happened without raising.
# ----------------------------------------------------------------------------

@dataclasses.dataclass
class RecordResult:
    written: bool
    reason: str            # human-readable explanation
    event_id: str | None   # uuid of the event if written
    shard_path: str | None # absolute path to the prefs shard appended to


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------

def _warn(msg: str) -> None:
    """Stderr warning. Never raises."""
    print(f"[record_event] WARN: {msg}", file=sys.stderr)


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_text(text: str) -> str:
    return _sha256_hex(text.encode("utf-8"))


def resolve_eval_repo() -> Path | None:
    """Resolve the local eval-repo clone in priority order.

    Order:
      1. `$SKILL_ORACLE_EVAL_REPO` env var (must exist on disk)
      2. `~/.openclaw/public-skills-evals-private/` if present
      3. dev fallback at `~/Desktop/Codespace/public-skills-evals-private/`

    Returns None if none of those exist on disk so callers can warn cleanly.
    """
    env_override = os.environ.get("SKILL_ORACLE_EVAL_REPO")
    if env_override:
        p = Path(env_override).expanduser()
        if p.is_dir():
            return p
        _warn(
            f"SKILL_ORACLE_EVAL_REPO={env_override!r} does not exist; "
            "trying default locations."
        )

    if _CANONICAL_CLIENT_CLONE.is_dir():
        return _CANONICAL_CLIENT_CLONE
    if _DEV_FALLBACK_CLONE.is_dir():
        return _DEV_FALLBACK_CLONE
    return None


def load_identity() -> dict | None:
    """Load `~/.openclaw/skill-oracle/identity.json`. None if missing/invalid."""
    if not _IDENTITY_FILE.exists():
        return None
    try:
        with _IDENTITY_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        _warn(f"failed to read {_IDENTITY_FILE}: {e}")
        return None
    if not isinstance(data, dict) or not data.get("github_user"):
        _warn(f"{_IDENTITY_FILE} missing 'github_user' field")
        return None
    return data


def _git_short_sha(repo: Path) -> str:
    """Return the current HEAD SHA of a git repo, or 'unknown' on failure."""
    try:
        out = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        )
        return out.stdout.strip() or "unknown"
    except (subprocess.SubprocessError, FileNotFoundError, OSError):
        return "unknown"


def resolve_router_version(goatedskills_repo: Path | None) -> str:
    """`git-sha:<sha>` of the public public-skills repo at routing time."""
    if goatedskills_repo and (goatedskills_repo / ".git").exists():
        return f"git-sha:{_git_short_sha(goatedskills_repo)}"
    return "git-sha:unknown"


def resolve_graph_version(goatedskills_repo: Path | None) -> str:
    """`skill-graph.json:sha256:<hex>` over the current graph contents.

    Falls back to `:unknown` if the graph file isn't where we expect it.
    """
    if not goatedskills_repo:
        return "skill-graph.json:sha256:unknown"

    # Prefer `graphify-out/.commit` if present (cheap, deterministic), else
    # hash the actual graph file. .commit is written by graphify on build.
    commit_marker = goatedskills_repo / "graphify-out" / ".commit"
    if commit_marker.exists():
        try:
            sha = commit_marker.read_text(encoding="utf-8").strip()
            if sha:
                return f"skill-graph.json:sha256:{sha}"
        except OSError:
            pass  # fall through to hashing the graph file directly

    graph_file = goatedskills_repo / "graphify-out" / "skill-graph.json"
    if graph_file.exists():
        try:
            return f"skill-graph.json:sha256:{_sha256_hex(graph_file.read_bytes())}"
        except OSError as e:
            _warn(f"unable to hash {graph_file}: {e}")

    return "skill-graph.json:sha256:unknown"


def _stack_hash(stack: list[str], filter_mode: str, params: dict) -> str:
    """Canonical sha256 over (stack + filter_mode + params).

    Truncated to 16 hex chars to match the nightly-batch shard's convention.
    """
    payload = json.dumps(
        {"stack": sorted(stack), "filter_mode": filter_mode, "params": params},
        sort_keys=True,
        separators=(",", ":"),
    )
    return f"sha256:{_sha256_text(payload)[:16]}"


def _render_draft_output_text(prompt: str, stack: list[str], letter: str) -> str:
    """Render a stable, hash-friendly text artifact representing the draft.

    The validator's --strict mode hashes the file at `output_text_path` and
    compares to `output_hash`. Anything stable works; we make it readable.
    """
    lines = [
        f"# Skill Oracle draft {letter.upper()} for prompt:",
        f"# {prompt}",
        "",
        "## Recommended skill stack",
    ]
    for i, skill in enumerate(stack, 1):
        lines.append(f"{i}. {skill}")
    return "\n".join(lines) + "\n"


def _write_atomic(target: Path, data: bytes) -> None:
    """Write `data` to `target` atomically via tmpfile + rename + fsync."""
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(
        prefix=target.name + ".",
        suffix=".tmp",
        dir=str(target.parent),
    )
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, target)
    except OSError:
        # Best-effort cleanup; let caller see the original error.
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def _append_atomic(shard: Path, line: str) -> None:
    """Append one line + newline to `shard` with fsync, line-atomic on POSIX."""
    shard.parent.mkdir(parents=True, exist_ok=True)
    # POSIX guarantees write(2) atomicity for small writes on a single line
    # when opened O_APPEND. We add fsync for durability.
    payload = line.rstrip("\n").encode("utf-8") + b"\n"
    with shard.open("ab") as f:
        f.write(payload)
        f.flush()
        os.fsync(f.fileno())


# ----------------------------------------------------------------------------
# Event construction
# ----------------------------------------------------------------------------

def _build_draft(
    eval_repo: Path,
    event_id: str,
    letter: str,
    prompt: str,
    stack: list[str],
    filter_mode: str,
    params: dict,
    tokens_in: int,
    tokens_out: int,
    latency_ms: int,
) -> tuple[dict, Path, bytes]:
    """Build a draft sub-object + the bytes to write at output_text_path.

    Returns (draft_dict, absolute_output_path, output_bytes). The caller is
    responsible for actually writing the bytes — we keep the I/O at one site.
    """
    rel_path = f"outputs/evt-{event_id[:8]}-{letter}.txt"
    text = _render_draft_output_text(prompt, stack, letter)
    output_bytes = text.encode("utf-8")
    output_hash = _sha256_hex(output_bytes)

    draft = {
        "stack": list(stack),  # spec says alphabetical, but example events
                                # don't enforce it; the validator only requires
                                # list-of-strings.
        "stack_hash": _stack_hash(stack, filter_mode, params),
        "filter_mode": filter_mode,
        "params": params,
        "output_hash": f"sha256:{output_hash}",
        "output_text_path": rel_path,
        "tokens_in": int(tokens_in),
        "tokens_out": int(tokens_out),
        "latency_ms": int(latency_ms),
    }
    return draft, eval_repo / rel_path, output_bytes


def build_event(
    *,
    eval_repo: Path,
    github_user: str,
    prompt: str,
    drafts: list[list[str]],
    winner: str,
    reason: str | None,
    anchor_picks: list[str],
    incomplete: bool,
    drafter_model: str,
    filter_mode: str,
    params: dict,
    tokens_in: int,
    tokens_out: int,
    latency_ms: int,
    intent_cluster: str,
    router_version: str,
    graph_version: str,
) -> tuple[dict, list[tuple[Path, bytes]]]:
    """Construct a fully-populated event + the list of output files to write.

    Returns (event_dict, [(output_path, output_bytes), ...]). Caller writes
    files first (so hashes line up if validator runs --strict immediately
    after), then appends the JSON line.
    """
    if not drafts:
        raise ValueError("at least one draft required")
    if len(drafts) > 3:
        raise ValueError("at most 3 drafts (A, B, C) supported by schema v1")
    if winner not in {"A", "B", "C", "TIE", "BOTH_BAD"}:
        raise ValueError(f"invalid winner: {winner!r}")

    event_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).replace(microsecond=0)
    ts = now.isoformat().replace("+00:00", "Z")

    files_to_write: list[tuple[Path, bytes]] = []
    drafts_dict: dict[str, Any] = {"draft_a": None, "draft_b": None, "draft_c": None}
    models_dict: dict[str, Any] = {}

    for i, stack in enumerate(drafts):
        letter = "abc"[i]
        draft, out_path, out_bytes = _build_draft(
            eval_repo=eval_repo,
            event_id=event_id,
            letter=letter,
            prompt=prompt,
            stack=list(stack),
            filter_mode=filter_mode,
            params=params,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            latency_ms=latency_ms,
        )
        drafts_dict[f"draft_{letter}"] = draft
        files_to_write.append((out_path, out_bytes))
        models_dict[f"drafter_model_{letter}"] = drafter_model

    # The validator requires drafter_model_a/b/c (all three) as top-level
    # keys. For absent drafts, copy the drafter model string but leave the
    # draft object null — the validator allows null drafts as long as the
    # winner doesn't reference them.
    for letter in "abc":
        models_dict.setdefault(f"drafter_model_{letter}", drafter_model)

    event = {
        "schema_version": SCHEMA_VERSION,
        "event_id": event_id,
        "ts": ts,
        "user_id_hash": f"github:{github_user}",
        "task_hash": f"sha256:{_sha256_text(prompt)}",
        "task_preview": prompt[:TASK_PREVIEW_LEN],
        "intent_cluster": intent_cluster,
        "router_version": router_version,
        "graph_version": graph_version,
        "venue": "live",
        **models_dict,
        **drafts_dict,
        "winner": winner,
        "judge_kind": "human",
        "anchor_picks": list(anchor_picks),
        "incomplete": bool(incomplete),
    }
    if reason:
        # The schema says "≤200 chars" — clamp defensively.
        event["reason"] = reason[:200]
    # confidence is intentionally omitted for human judges (schema says
    # "null for human"; absent or null both valid — the validator does not
    # require it.)
    return event, files_to_write


# ----------------------------------------------------------------------------
# Top-level record() — graceful, never raises into the caller.
# ----------------------------------------------------------------------------

def record(
    *,
    prompt: str,
    drafts: list[list[str]],
    winner: str = "A",
    reason: str | None = None,
    anchor_picks: list[str] | None = None,
    incomplete: bool = False,
    drafter_model: str | None = None,
    filter_mode: str = DEFAULT_FILTER_MODE,
    params: dict | None = None,
    tokens_in: int = 0,
    tokens_out: int = 0,
    latency_ms: int = 0,
    goatedskills_repo: Path | str | None = None,
) -> RecordResult:
    """Try to record one preference event. Always returns; never raises."""
    anchor_picks = anchor_picks or []
    params = params or dict(DEFAULT_FILTER_PARAMS)
    drafter_model = drafter_model or os.environ.get("ANTHROPIC_MODEL", "unknown")

    # ---- 1. Resolve eval repo + prefs/ dir ----
    eval_repo = resolve_eval_repo()
    if eval_repo is None:
        msg = (
            "no eval repo found; set $SKILL_ORACLE_EVAL_REPO or run "
            "scripts/bootstrap-client.sh from public-skills-evals-private "
            "to clone it to ~/.openclaw/."
        )
        _warn(msg)
        return RecordResult(False, msg, None, None)

    prefs_dir = eval_repo / "prefs"
    if not prefs_dir.is_dir():
        msg = (
            f"{prefs_dir} does not exist; run "
            "scripts/bootstrap-client.sh inside the eval repo to set it up."
        )
        _warn(msg)
        return RecordResult(False, msg, None, None)

    outputs_dir = eval_repo / "outputs"
    if not outputs_dir.is_dir():
        # outputs/ is required by the strict validator. Make it lazily; the
        # eval repo's design treats it as a regular committed directory.
        try:
            outputs_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            msg = f"cannot create {outputs_dir}: {e}"
            _warn(msg)
            return RecordResult(False, msg, None, None)

    # ---- 2. Identity ----
    identity = load_identity()
    if identity is None:
        msg = (
            f"{_IDENTITY_FILE} missing or invalid; run "
            "scripts/bootstrap-client.sh from public-skills-evals-private "
            "to bootstrap this machine."
        )
        _warn(msg)
        return RecordResult(False, msg, None, None)
    github_user = identity["github_user"]

    # ---- 3. Cluster classification ----
    taxonomy_path = eval_repo / "cluster-taxonomy.json"
    try:
        intent_cluster = classify(prompt, taxonomy_path)
    except Exception as e:  # never block on classifier failure
        _warn(f"cluster classification failed ({e}); falling back to catch-all")
        intent_cluster = "catch-all"

    # ---- 4. Versions ----
    if goatedskills_repo is not None:
        gs_repo = Path(goatedskills_repo)
    else:
        # Best-effort: the public-skills repo is the parent of this script's
        # ancestor chain (.../skills/skill-oracle/scripts/record_event.py ->
        # 3 levels up). If that doesn't look right, fall back to "unknown".
        candidate = Path(__file__).resolve().parents[3]
        gs_repo = candidate if (candidate / "graphify-out").is_dir() else None
    router_version = resolve_router_version(gs_repo)
    graph_version = resolve_graph_version(gs_repo)

    # ---- 5. Build event + output files ----
    try:
        event, files_to_write = build_event(
            eval_repo=eval_repo,
            github_user=github_user,
            prompt=prompt,
            drafts=drafts,
            winner=winner,
            reason=reason,
            anchor_picks=anchor_picks,
            incomplete=incomplete,
            drafter_model=drafter_model,
            filter_mode=filter_mode,
            params=params,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            latency_ms=latency_ms,
            intent_cluster=intent_cluster,
            router_version=router_version,
            graph_version=graph_version,
        )
    except ValueError as e:
        msg = f"invalid event inputs: {e}"
        _warn(msg)
        return RecordResult(False, msg, None, None)

    # Validate the winner references a populated draft. The strict validator
    # will catch this too but we'd rather not emit a known-invalid event.
    if winner in {"A", "B", "C"}:
        key = f"draft_{winner.lower()}"
        if event[key] is None:
            msg = (
                f"winner={winner!r} references {key} which is null; refusing "
                "to write a self-invalid event. Pass that draft in --drafts, "
                "or use winner=BOTH_BAD."
            )
            _warn(msg)
            return RecordResult(False, msg, None, None)

    # ---- 6. Write outputs (atomic), then append the event line. ----
    try:
        for out_path, out_bytes in files_to_write:
            _write_atomic(out_path, out_bytes)
    except OSError as e:
        msg = f"failed writing draft output text: {e}"
        _warn(msg)
        return RecordResult(False, msg, None, None)

    shard_path = prefs_dir / f"{github_user}.jsonl"
    try:
        line = json.dumps(event, ensure_ascii=False, separators=(", ", ": "))
        _append_atomic(shard_path, line)
    except OSError as e:
        msg = f"failed appending to {shard_path}: {e}"
        _warn(msg)
        # Don't try to delete the output files we wrote — they're cheap and
        # the orphan can be GC'd by a future tool. We prefer to over-write
        # than under-write.
        return RecordResult(False, msg, event["event_id"], str(shard_path))

    return RecordResult(True, "ok", event["event_id"], str(shard_path))


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------

def _parse_drafts_json(s: str) -> list[list[str]]:
    """Parse the --drafts JSON arg. Expect a list-of-lists-of-strings."""
    try:
        parsed = json.loads(s)
    except json.JSONDecodeError as e:
        raise argparse.ArgumentTypeError(f"--drafts is not valid JSON: {e}")
    if not isinstance(parsed, list):
        raise argparse.ArgumentTypeError("--drafts must be a JSON array")
    if not (1 <= len(parsed) <= 3):
        raise argparse.ArgumentTypeError("--drafts must have 1 to 3 entries")
    cleaned: list[list[str]] = []
    for i, d in enumerate(parsed):
        if not isinstance(d, list) or not all(isinstance(s, str) for s in d):
            raise argparse.ArgumentTypeError(
                f"--drafts[{i}] must be a list of skill-name strings"
            )
        cleaned.append(d)
    return cleaned


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--prompt", required=True, help="The user's task text.")
    parser.add_argument(
        "--drafts",
        required=True,
        type=_parse_drafts_json,
        help="JSON list of 1-3 draft stacks, e.g. '[[\"cold-email\"],[\"copywriting\"]]'.",
    )
    parser.add_argument(
        "--winner",
        default="A",
        choices=["A", "B", "C", "TIE", "BOTH_BAD"],
        help="Which draft the user actually used. BOTH_BAD if none.",
    )
    parser.add_argument("--reason", default=None, help="Optional free-text rationale.")
    parser.add_argument(
        "--anchor-picks",
        default="[]",
        help="JSON list of skill-name strings the user pinned as anchors.",
    )
    parser.add_argument(
        "--incomplete",
        action="store_true",
        help="Set when the user abandoned mid-eval.",
    )
    parser.add_argument(
        "--drafter-model",
        default=None,
        help="Model ID that produced the draft(s). Defaults to $ANTHROPIC_MODEL or 'unknown'.",
    )
    parser.add_argument("--tokens-in", type=int, default=0)
    parser.add_argument("--tokens-out", type=int, default=0)
    parser.add_argument("--latency-ms", type=int, default=0)
    parser.add_argument(
        "--filter-mode",
        default=DEFAULT_FILTER_MODE,
        choices=["heuristic", "llm", "learned", "auto"],
    )
    parser.add_argument(
        "--public-skills-repo",
        default=None,
        help="Override path to the public public-skills repo. Auto-detected by default.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress non-error stdout. Warnings still go to stderr.",
    )
    args = parser.parse_args(argv)

    try:
        anchor_picks = json.loads(args.anchor_picks)
        if not isinstance(anchor_picks, list) or not all(isinstance(s, str) for s in anchor_picks):
            raise ValueError("must be a JSON list of strings")
    except (json.JSONDecodeError, ValueError) as e:
        print(f"--anchor-picks: {e}", file=sys.stderr)
        return 2

    result = record(
        prompt=args.prompt,
        drafts=args.drafts,
        winner=args.winner,
        reason=args.reason,
        anchor_picks=anchor_picks,
        incomplete=args.incomplete,
        drafter_model=args.drafter_model,
        filter_mode=args.filter_mode,
        tokens_in=args.tokens_in,
        tokens_out=args.tokens_out,
        latency_ms=args.latency_ms,
        goatedskills_repo=args.goatedskills_repo,
    )

    if not args.quiet:
        if result.written:
            print(f"recorded: event_id={result.event_id} -> {result.shard_path}")
        else:
            print(f"skipped: {result.reason}")
    # Always exit 0 — recording is best-effort.
    return 0


if __name__ == "__main__":
    sys.exit(main())
