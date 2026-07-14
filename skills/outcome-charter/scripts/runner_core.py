#!/usr/bin/env python3
"""Pure deterministic helpers shared by durable outcome-charter runners."""

from __future__ import annotations

from typing import Any

from charter_registry import CharterError, idempotency_key, require_digest, require_integer, require_string


REQUIRED_PLAN_FIELDS = {
    "plan_version",
    "runner_mode",
    "workflow_type",
    "task_queue",
    "workflow_id",
    "charter_id",
    "definition_digest",
    "execution_scope_digest",
    "max_concurrency",
    "overall_timeout_seconds",
    "activities",
}
GATED_SIDE_EFFECTS = {"write", "send", "publish", "delete", "spend", "sign", "deploy"}


def validate_plan(plan: dict[str, Any]) -> None:
    if not isinstance(plan, dict):
        raise CharterError("durable plan must be an object")
    missing = REQUIRED_PLAN_FIELDS - set(plan)
    if missing:
        raise CharterError(f"durable plan missing fields: {', '.join(sorted(missing))}")
    if plan["plan_version"] != "1.0":
        raise CharterError("durable plan version must be 1.0")
    for field in ("workflow_type", "task_queue", "workflow_id", "charter_id"):
        require_string(plan[field], f"durable plan.{field}")
    for field in ("definition_digest", "execution_scope_digest"):
        require_digest(plan[field], f"durable plan.{field}")
    require_integer(plan["max_concurrency"], "durable plan.max_concurrency", minimum=1, maximum=1000)
    require_integer(
        plan["overall_timeout_seconds"],
        "durable plan.overall_timeout_seconds",
        minimum=1,
        maximum=31_536_000,
    )
    activities = plan["activities"]
    if not isinstance(activities, list) or not activities:
        raise CharterError("durable plan.activities must be a non-empty list")
    ids: set[str] = set()
    for index, item in enumerate(activities):
        if not isinstance(item, dict):
            raise CharterError(f"durable plan activity {index} must be an object")
        required = {
            "activity_id",
            "operation",
            "depends_on",
            "input_fields",
            "side_effect",
            "start_to_close_timeout_seconds",
            "retry",
            "requires_idempotency_key",
            "requires_approval_gate",
            "requires_destination_readback",
        }
        absent = required - set(item)
        if absent:
            raise CharterError(f"durable plan activity {index} missing fields: {', '.join(sorted(absent))}")
        require_string(item["activity_id"], f"activity {index}.activity_id")
        require_string(item["operation"], f"activity {index}.operation")
        if item["activity_id"] in ids:
            raise CharterError("durable plan activity IDs must be unique")
        ids.add(item["activity_id"])
        if not isinstance(item["depends_on"], list) or not all(isinstance(value, str) for value in item["depends_on"]):
            raise CharterError(f"activity {item['activity_id']}.depends_on must be a string list")
        if not isinstance(item["input_fields"], list) or not all(isinstance(value, str) and value for value in item["input_fields"]):
            raise CharterError(f"activity {item['activity_id']}.input_fields must be a string list")
        require_integer(
            item["start_to_close_timeout_seconds"],
            f"activity {item['activity_id']}.start_to_close_timeout_seconds",
            minimum=1,
            maximum=86_400,
        )
        retry = item["retry"]
        if not isinstance(retry, dict):
            raise CharterError(f"activity {item['activity_id']}.retry must be an object")
        require_integer(retry.get("maximum_attempts"), f"activity {item['activity_id']}.retry.maximum_attempts", minimum=1, maximum=100)
        non_retryable = retry.get("non_retryable")
        if not isinstance(non_retryable, list) or not all(isinstance(entry, str) and entry for entry in non_retryable):
            # The workflow indexes retry["non_retryable"] unconditionally; a
            # plan without it passes preflight and then KeyErrors in workflow
            # code, which Temporal retries until the execution timeout.
            raise CharterError(f"activity {item['activity_id']}.retry.non_retryable must be a list of strings")
        for field in ("requires_idempotency_key", "requires_approval_gate", "requires_destination_readback"):
            if not isinstance(item[field], bool):
                raise CharterError(f"activity {item['activity_id']}.{field} must be boolean")
        gated = item["side_effect"] in GATED_SIDE_EFFECTS
        if any(item[field] != gated for field in ("requires_idempotency_key", "requires_approval_gate", "requires_destination_readback")):
            raise CharterError(f"activity {item['activity_id']} security gates do not match its side-effect class")
        if item["side_effect"] not in {"none", "read", *GATED_SIDE_EFFECTS}:
            raise CharterError(f"activity {item['activity_id']} has an unknown side-effect class")
    for item in activities:
        unknown = set(item["depends_on"]) - ids
        if unknown:
            raise CharterError(f"activity {item['activity_id']} has unknown dependencies")


def activity_layers(plan: dict[str, Any]) -> list[list[dict[str, Any]]]:
    validate_plan(plan)
    by_id = {item["activity_id"]: item for item in plan["activities"]}
    remaining = {item_id: set(item["depends_on"]) for item_id, item in by_id.items()}
    layers: list[list[dict[str, Any]]] = []
    while remaining:
        ready = sorted(item_id for item_id, dependencies in remaining.items() if not dependencies)
        if not ready:
            raise CharterError("durable plan activity graph contains a cycle")
        layers.append([by_id[item_id] for item_id in ready])
        for item_id in ready:
            del remaining[item_id]
        for dependencies in remaining.values():
            dependencies.difference_update(ready)
    return layers


def step_request(
    plan: dict[str, Any],
    activity_spec: dict[str, Any],
    inputs_ref: str,
    prior_results: dict[str, Any],
    authorization_grant_ref: str | None = None,
) -> dict[str, Any]:
    validate_plan(plan)
    require_string(inputs_ref, "inputs_ref")
    activity_id = activity_spec["activity_id"]
    dependency_results = {dependency: prior_results[dependency] for dependency in activity_spec["depends_on"]}
    request = {
        "workflow_id": plan["workflow_id"],
        "charter_id": plan["charter_id"],
        "definition_digest": plan["definition_digest"],
        "execution_scope_digest": plan["execution_scope_digest"],
        "activity": activity_spec,
        "inputs_ref": inputs_ref,
        "input_fields": activity_spec["input_fields"],
        "dependency_results": dependency_results,
    }
    if activity_spec["requires_approval_gate"]:
        require_string(authorization_grant_ref, "authorization_grant_ref")
        request["authorization_grant_ref"] = authorization_grant_ref
    if activity_spec["requires_idempotency_key"]:
        request["idempotency_key"] = idempotency_key(
            plan["charter_id"],
            activity_id,
            plan["execution_scope_digest"],
            plan["definition_digest"],
        )
    return request


def validate_activity_result(value: Any, activity_id: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise CharterError(f"activity {activity_id} result must be an object")
    allowed = {
        "activity_id",
        "result_ref",
        "evidence_digest",
        "attempted_items",
        "successful_items",
        "destination_readback",
    }
    if set(value) != allowed:
        raise CharterError(f"activity {activity_id} result violates the sanitized envelope contract")
    if value["activity_id"] != activity_id:
        raise CharterError(f"activity {activity_id} result identity does not match")
    require_digest(value["result_ref"], f"activity {activity_id}.result_ref")
    require_digest(value["evidence_digest"], f"activity {activity_id}.evidence_digest")
    attempted = require_integer(value["attempted_items"], f"activity {activity_id}.attempted_items")
    successful = require_integer(value["successful_items"], f"activity {activity_id}.successful_items")
    if successful > attempted:
        raise CharterError(f"activity {activity_id} successful_items exceeds attempted_items")
    if not isinstance(value["destination_readback"], bool):
        raise CharterError(f"activity {activity_id}.destination_readback must be boolean")
    return value


def action_manifest(plan: dict[str, Any]) -> list[dict[str, str]]:
    validate_plan(plan)
    return [
        {"activity_id": item["activity_id"], "operation": item["operation"], "side_effect": item["side_effect"]}
        for item in plan["activities"]
        if item["requires_approval_gate"]
    ]
