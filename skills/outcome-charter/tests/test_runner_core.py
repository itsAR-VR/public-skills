from __future__ import annotations

import copy
import sys
from pathlib import Path

import pytest


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from charter_registry import CharterError  # noqa: E402
from durable_plan import compile_plan  # noqa: E402
from runner_core import activity_layers, step_request, validate_plan  # noqa: E402
from temporal_submit import submission_scope_digest, submission_workflow_id, validate_submission  # noqa: E402
from test_charter_registry import BASE  # noqa: E402


def plan():
    return compile_plan(copy.deepcopy(BASE), "sha256:" + "9" * 64)


def test_layers_preserve_dependencies_and_expose_parallel_reads() -> None:
    layers = activity_layers(plan())
    assert [item["activity_id"] for item in layers[0]] == ["find-brief"]
    assert [item["activity_id"] for item in layers[-1]] == ["create-linear"]


def test_step_request_contains_only_dependency_results_and_stable_idempotency() -> None:
    current = plan()
    write = next(item for item in current["activities"] if item["activity_id"] == "create-linear")
    prior = {
        "find-brief": {
            "activity_id": "find-brief",
            "result_ref": "sha256:" + "1" * 64,
            "evidence_digest": "sha256:" + "2" * 64,
            "attempted_items": 1,
            "successful_items": 1,
            "destination_readback": True,
        }
    }
    first = step_request(current, write, "sha256:" + "3" * 64, prior, "sha256:" + "4" * 64)
    second = step_request(current, write, "sha256:" + "3" * 64, prior, "sha256:" + "4" * 64)
    assert first == second
    assert first["dependency_results"] == prior
    assert first["inputs_ref"] == "sha256:" + "3" * 64
    assert first["input_fields"] == []
    assert first["idempotency_key"].startswith("charter:")
    assert first["authorization_grant_ref"] == "sha256:" + "4" * 64


def test_runner_rejects_tampered_plan() -> None:
    current = plan()
    current["activities"][0]["retry"]["maximum_attempts"] = True
    with pytest.raises(CharterError):
        validate_plan(current)


def test_submission_uses_only_content_addressed_opaque_references() -> None:
    submission = {
        "workflow_id": "placeholder",
        "charter_id": "investor-research-v1",
        "workflow_type": "OutcomeCharterWorkflow",
        "task_queue": "outcome-charters",
        "overall_timeout_seconds": 3600,
        "plan_ref": "sha256:" + "1" * 64,
        "inputs_ref": "sha256:" + "2" * 64,
        "capability_ref": "sha256:" + "3" * 64,
        "approval_ref": "sha256:" + "4" * 64,
        "definition_digest": "sha256:" + "5" * 64,
        "execution_scope_digest": "placeholder",
        "preview_digest": "sha256:" + "7" * 64,
    }
    submission["execution_scope_digest"] = submission_scope_digest(submission)
    submission["workflow_id"] = submission_workflow_id(submission)
    validate_submission(submission)
    tampered = dict(submission, inputs_ref="not-a-digest")
    with pytest.raises(CharterError):
        validate_submission(tampered)


def test_plan_requires_non_retryable_list() -> None:
    current = plan()
    del current["activities"][0]["retry"]["non_retryable"]
    with pytest.raises(CharterError, match="non_retryable"):
        validate_plan(current)
