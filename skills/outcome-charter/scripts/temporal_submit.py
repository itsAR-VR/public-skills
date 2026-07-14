#!/usr/bin/env python3
"""Submit an opaque-reference outcome charter to the isolated Temporal worker."""

from __future__ import annotations

import argparse
import asyncio
import importlib
import json
import os
from datetime import timedelta
from pathlib import Path

from charter_registry import canonical_hash, require_digest, require_integer, require_string, sha256_label


SUBMISSION_FIELDS = {
    "workflow_id",
    "charter_id",
    "workflow_type",
    "task_queue",
    "overall_timeout_seconds",
    "plan_ref",
    "inputs_ref",
    "capability_ref",
    "approval_ref",
    "definition_digest",
    "execution_scope_digest",
    "preview_digest",
}


def load_object(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def submission_workflow_id(submission: dict) -> str:
    identity = {
        "charter_id": submission["charter_id"],
        "definition_digest": submission["definition_digest"],
        "execution_scope_digest": submission["execution_scope_digest"],
    }
    return "charter:" + canonical_hash(identity)


def submission_scope_digest(submission: dict) -> str:
    return sha256_label(
        {
            field: submission[field]
            for field in ("inputs_ref", "capability_ref", "approval_ref", "preview_digest")
        }
    )


def validate_submission(submission: dict) -> None:
    if not isinstance(submission, dict) or set(submission) != SUBMISSION_FIELDS:
        raise ValueError("submission fields must exactly match the opaque-reference contract")
    for field in ("workflow_id", "charter_id", "workflow_type", "task_queue"):
        require_string(submission[field], f"submission.{field}")
    if submission["workflow_type"] != "OutcomeCharterWorkflow":
        raise ValueError("submission workflow_type is not allowed")
    if submission["task_queue"] != "outcome-charters":
        raise ValueError("submission task_queue is not the runner-owned queue")
    for field in (
        "plan_ref",
        "inputs_ref",
        "capability_ref",
        "definition_digest",
        "execution_scope_digest",
        "preview_digest",
    ):
        require_digest(submission[field], f"submission.{field}")
    if submission["approval_ref"] is not None:
        require_digest(submission["approval_ref"], "submission.approval_ref")
    require_integer(
        submission["overall_timeout_seconds"],
        "submission.overall_timeout_seconds",
        minimum=1,
        maximum=31_536_000,
    )
    if submission["workflow_id"] != submission_workflow_id(submission):
        raise ValueError("submission workflow_id does not match its immutable content identity")
    if submission["execution_scope_digest"] != submission_scope_digest(submission):
        raise ValueError("submission execution_scope_digest does not match its opaque references")


def load_data_converter():
    module_name = os.environ.get("OUTCOME_CHARTER_CODEC_MODULE", "temporal_codec")
    module = importlib.import_module(module_name)
    factory = getattr(module, "data_converter", None)
    if not callable(factory):
        raise RuntimeError("Temporal codec module must expose data_converter()")
    return factory()


async def submit(address: str, namespace: str, submission: dict, *, wait: bool) -> dict:
    validate_submission(submission)
    try:
        from temporalio.client import Client
        from temporalio.common import WorkflowIDConflictPolicy, WorkflowIDReusePolicy
        from temporalio.exceptions import WorkflowAlreadyStartedError
    except ImportError as exc:
        raise RuntimeError("install scripts/requirements.txt before submitting a Temporal workflow") from exc
    client = await Client.connect(address, namespace=namespace, data_converter=load_data_converter())
    try:
        # FAIL (not USE_EXISTING) makes attachment detection exact: a still-
        # running duplicate raises WorkflowAlreadyStartedError and we attach
        # explicitly below. first_execution_run_id is NOT an attachment
        # indicator — the SDK sets it from resp.run_id on every no-signal
        # start, including USE_EXISTING attaches.
        handle = await client.start_workflow(
            submission["workflow_type"],
            submission,
            id=submission["workflow_id"],
            task_queue=submission["task_queue"],
            execution_timeout=timedelta(seconds=submission["overall_timeout_seconds"]),
            id_conflict_policy=WorkflowIDConflictPolicy.FAIL,
            id_reuse_policy=WorkflowIDReusePolicy.REJECT_DUPLICATE,
        )
        attached_to_existing = False
    except WorkflowAlreadyStartedError:
        handle = client.get_workflow_handle(submission["workflow_id"])
        attached_to_existing = True
    response = {"workflow_id": handle.id, "attached_to_existing": attached_to_existing}
    if wait:
        response["result"] = await handle.result()
    return response


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--submission", required=True, type=Path)
    parser.add_argument("--address", default="localhost:7233")
    parser.add_argument("--namespace", default="default")
    parser.add_argument("--wait", action="store_true")
    args = parser.parse_args()
    try:
        result = asyncio.run(submit(args.address, args.namespace, load_object(args.submission), wait=args.wait))
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}, sort_keys=True))
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
