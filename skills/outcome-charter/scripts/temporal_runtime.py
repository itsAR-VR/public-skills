#!/usr/bin/env python3
"""Top-level Temporal workflow and activities for outcome charters."""

from __future__ import annotations

import asyncio
from datetime import timedelta
from typing import Any

from temporalio import activity, workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import ApplicationError

# charter_registry pulls attestations -> cryptography; those PyO3 extension
# modules cannot be re-imported inside the Temporal workflow sandbox on every
# workflow run, so they must be passed through from the worker process.
with workflow.unsafe.imports_passed_through():
    from charter_registry import CharterError, sha256_label
    from runner_core import action_manifest, activity_layers, step_request, validate_activity_result, validate_plan


def terminal_validation_error(message: str, cause: Exception | None = None) -> ApplicationError:
    """Terminal validation failures must fail the WORKFLOW, not the workflow task.

    Plain ValueError/CharterError raised from workflow code fails only the
    workflow task, which Temporal retries until the execution timeout — a
    malformed plan or failed readback would hang --wait for up to a year.
    """
    error = ApplicationError(message, non_retryable=True, type="CharterValidationFailed")
    if cause is not None:
        error.__cause__ = cause
    return error


_adapter = None


def configure_adapter(adapter) -> None:
    global _adapter
    _adapter = adapter


def configured_adapter():
    if _adapter is None:
        raise RuntimeError("Temporal outcome-charter adapter is not configured")
    return _adapter


@activity.defn(name="outcome_charter_preflight")
async def preflight(submission: dict[str, Any]) -> dict[str, Any]:
    return await configured_adapter().preflight(submission)


@activity.defn(name="outcome_charter_authorize")
async def authorize(payload: dict[str, Any]) -> dict[str, Any]:
    return await configured_adapter().authorize(payload)


@activity.defn(name="outcome_charter_execute_step")
async def execute_step(payload: dict[str, Any]) -> dict[str, Any]:
    return await configured_adapter().execute_step(payload)


@activity.defn(name="outcome_charter_emit_receipt")
async def emit_receipt(payload: dict[str, Any]) -> dict[str, Any]:
    return await configured_adapter().emit_receipt(payload)


@workflow.defn(name="OutcomeCharterWorkflow")
class OutcomeCharterWorkflow:
    @workflow.run
    async def run(self, submission: dict[str, Any]) -> dict[str, Any]:
        preflight_result = await workflow.execute_activity(
            "outcome_charter_preflight",
            submission,
            start_to_close_timeout=timedelta(seconds=60),
            retry_policy=RetryPolicy(maximum_attempts=1),
        )
        plan = preflight_result["trusted_plan"]
        inputs_ref = preflight_result["inputs_ref"]
        try:
            validate_plan(plan)
            actions = action_manifest(plan)
            layers = activity_layers(plan)
        except (CharterError, ValueError) as exc:
            raise terminal_validation_error(str(exc), exc)
        if plan["workflow_id"] != submission["workflow_id"]:
            raise terminal_validation_error("trusted plan workflow_id does not match submission")
        grant_ref = None
        if actions:
            grant = await workflow.execute_activity(
                "outcome_charter_authorize",
                {"submission": submission, "trusted_plan": plan, "actions": actions},
                start_to_close_timeout=timedelta(seconds=60),
                retry_policy=RetryPolicy(maximum_attempts=3),
            )
            grant_ref = grant["authorization_grant_ref"]
        results: dict[str, Any] = {}
        for layer in layers:
            limit = plan["max_concurrency"]
            for offset in range(0, len(layer), limit):
                chunk = layer[offset : offset + limit]
                batch = []
                for spec in chunk:
                    request = step_request(plan, spec, inputs_ref, results, grant_ref)
                    batch.append(
                        workflow.execute_activity(
                            "outcome_charter_execute_step",
                            request,
                            start_to_close_timeout=timedelta(seconds=spec["start_to_close_timeout_seconds"]),
                            retry_policy=RetryPolicy(
                                maximum_attempts=spec["retry"]["maximum_attempts"],
                                non_retryable_error_types=spec["retry"]["non_retryable"],
                            ),
                        )
                    )
                values = await asyncio.gather(*batch)
                for spec, value in zip(chunk, values, strict=True):
                    try:
                        clean = validate_activity_result(value, spec["activity_id"])
                    except (CharterError, ValueError) as exc:
                        raise terminal_validation_error(str(exc), exc)
                    if spec["requires_destination_readback"] and not clean["destination_readback"]:
                        raise terminal_validation_error(
                            f"activity {spec['activity_id']} requires successful destination readback"
                        )
                    results[spec["activity_id"]] = clean
        result_envelopes = list(results.values())
        receipt = await workflow.execute_activity(
            "outcome_charter_emit_receipt",
            {
                "submission": submission,
                "trusted_plan_digest": plan["definition_digest"],
                "result_envelopes": result_envelopes,
                "result_manifest_digest": sha256_label(result_envelopes),
                "required_readbacks": [
                    item["activity_id"] for item in plan["activities"] if item["requires_destination_readback"]
                ],
            },
            start_to_close_timeout=timedelta(seconds=60),
            retry_policy=RetryPolicy(maximum_attempts=3),
        )
        return {
            "workflow_id": plan["workflow_id"],
            "receipt_ref": receipt["receipt_ref"],
            "attempted_items": receipt["attempted_items"],
            "successful_items": receipt["successful_items"],
        }


ACTIVITIES = [preflight, authorize, execute_step, emit_receipt]
