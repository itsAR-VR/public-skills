#!/usr/bin/env python3
"""Run the encrypted outcome-charter workflow against Temporal's test server."""

from __future__ import annotations

import asyncio
import base64
import json
import os
import tempfile
from pathlib import Path

from durable_plan import compile_plan
from temporal_codec import data_converter
from temporal_runtime import ACTIVITIES, OutcomeCharterWorkflow, configure_adapter
import temporal_submit
from temporal_submit import submission_scope_digest, submission_workflow_id
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker


class VerificationAdapter:
    def __init__(self, plan: dict) -> None:
        self.plan = plan

    async def preflight(self, submission: dict) -> dict:
        return {"trusted_plan": self.plan, "inputs_ref": submission["inputs_ref"]}

    async def authorize(self, payload: dict) -> dict:
        assert payload["actions"]
        return {"authorization_grant_ref": "sha256:" + "8" * 64}

    async def execute_step(self, payload: dict) -> dict:
        return {
            "activity_id": payload["activity"]["activity_id"],
            "result_ref": "sha256:" + "9" * 64,
            "evidence_digest": "sha256:" + "a" * 64,
            "attempted_items": 1,
            "successful_items": 1,
            "destination_readback": payload["activity"]["requires_destination_readback"],
        }

    async def emit_receipt(self, payload: dict) -> dict:
        assert "inputs" not in payload and "results" not in payload
        count = len(payload["result_envelopes"])
        return {"receipt_ref": "sha256:" + "b" * 64, "attempted_items": count, "successful_items": count}


def build_submission(plan: dict) -> dict:
    value = {
        "workflow_id": "placeholder",
        "charter_id": plan["charter_id"],
        "workflow_type": plan["workflow_type"],
        "task_queue": "outcome-charters",
        "overall_timeout_seconds": plan["overall_timeout_seconds"],
        "plan_ref": "sha256:" + "1" * 64,
        "inputs_ref": "sha256:" + "2" * 64,
        "capability_ref": "sha256:" + "3" * 64,
        "approval_ref": "sha256:" + "4" * 64,
        "definition_digest": plan["definition_digest"],
        "execution_scope_digest": "placeholder",
        "preview_digest": "sha256:" + "7" * 64,
    }
    value["execution_scope_digest"] = submission_scope_digest(value)
    plan["execution_scope_digest"] = value["execution_scope_digest"]
    value["workflow_id"] = submission_workflow_id(value)
    plan["workflow_id"] = value["workflow_id"]
    return value


async def verify() -> None:
    root = Path(__file__).resolve().parents[1]
    definition = json.loads((root / "references" / "example-registry.json").read_text(encoding="utf-8"))["charters"][0]
    plan = compile_plan(definition, "sha256:" + "6" * 64)
    submission = build_submission(plan)
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as stream:
        json.dump({"active_key_id": "test", "keys": {"test": base64.b64encode(os.urandom(32)).decode()}}, stream)
        keyring = Path(stream.name)
    os.chmod(keyring, 0o600)
    converter = data_converter(keyring)
    configure_adapter(VerificationAdapter(plan))
    try:
        async with await WorkflowEnvironment.start_time_skipping(data_converter=converter) as environment:
            temporal_submit.load_data_converter = lambda: converter
            async with Worker(
                environment.client,
                task_queue=submission["task_queue"],
                workflows=[OutcomeCharterWorkflow],
                activities=ACTIVITIES,
            ):
                address = environment.client.service_client.config.target_host
                first = await temporal_submit.submit(
                    address,
                    "default",
                    submission,
                    wait=True,
                )
                second = await temporal_submit.submit(address, "default", submission, wait=True)
                assert first["result"]["receipt_ref"] == "sha256:" + "b" * 64
                assert first["result"]["attempted_items"] == len(plan["activities"])
                assert second["attached_to_existing"] is True
                assert second["result"] == first["result"]
    finally:
        keyring.unlink(missing_ok=True)
    print("encrypted Temporal outcome-charter E2E and idempotent resubmission: PASS")


if __name__ == "__main__":
    asyncio.run(verify())
