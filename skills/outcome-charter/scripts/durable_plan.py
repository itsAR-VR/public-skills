#!/usr/bin/env python3
"""Compile a validated charter into a deterministic durable-runner plan."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from charter_registry import CharterError, canonical_hash, definition_digest, load_json, require_digest, validate_definition


def stable_topological_steps(steps: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {step["step_id"]: step for step in steps}
    remaining = {step_id: set(step["depends_on"]) for step_id, step in by_id.items()}
    ordered: list[dict[str, Any]] = []
    while remaining:
        ready = sorted(step_id for step_id, dependencies in remaining.items() if not dependencies)
        if not ready:
            raise CharterError("cannot compile a cyclic durable plan")
        for step_id in ready:
            ordered.append(by_id[step_id])
            del remaining[step_id]
            for dependencies in remaining.values():
                dependencies.discard(step_id)
    return ordered


def compile_plan(definition: dict[str, Any], execution_scope_digest: str) -> dict[str, Any]:
    validate_definition(definition)
    require_digest(execution_scope_digest, "execution_scope_digest")
    runner = definition["runner"]
    workflow_id = "charter:" + canonical_hash(
        {
            "charter_id": definition["charter_id"],
            "definition_digest": definition_digest(definition),
            "execution_scope_digest": execution_scope_digest,
        }
    )
    activities = []
    for step in stable_topological_steps(definition["steps"]):
        side_effecting = step["side_effect"] not in {"none", "read"}
        activities.append(
            {
                "activity_id": step["step_id"],
                "operation": step["operation"],
                "depends_on": step["depends_on"],
                "input_fields": step["input_fields"],
                "side_effect": step["side_effect"],
                "schema_digest": definition["tool_schemas"].get(step["operation"], {}).get("schema_digest"),
                "auth": step.get("auth"),
                "start_to_close_timeout_seconds": step.get("timeout_seconds", 60),
                "retry": {
                    "maximum_attempts": step.get("maximum_attempts", 3),
                    "non_retryable": ["PermissionDenied", "SchemaMismatch", "ValidationError", "ApprovalRequired"],
                },
                "requires_idempotency_key": side_effecting,
                "requires_approval_gate": side_effecting,
                "requires_destination_readback": side_effecting,
            }
        )
    return {
        "plan_version": "1.0",
        "runner_mode": runner["mode"],
        "workflow_type": runner["workflow_type"],
        "task_queue": runner["task_queue"],
        "workflow_id": workflow_id,
        "charter_id": definition["charter_id"],
        "definition_digest": definition_digest(definition),
        "execution_scope_digest": execution_scope_digest,
        "max_concurrency": runner["max_concurrency"],
        "overall_timeout_seconds": runner["overall_timeout_seconds"],
        "preflight": ["verify_capability_attestation", "verify_current_schemas"],
        "activities": activities,
        "completion": ["verify_destination_readbacks", "emit_signed_sanitized_receipt"],
        "model_context_policy": "field-level-inputs-only",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--definition", required=True, type=Path)
    parser.add_argument("--execution-scope-digest", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        plan = compile_plan(load_json(args.definition), args.execution_scope_digest)
        payload = json.dumps(plan, indent=2, sort_keys=True) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(payload, encoding="utf-8")
        else:
            print(payload, end="")
    except (CharterError, OSError, ValueError, TypeError) as exc:
        print(json.dumps({"error": str(exc)}, sort_keys=True))
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
