from __future__ import annotations

import copy
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from durable_plan import compile_plan  # noqa: E402
from charter_registry import CharterError  # noqa: E402
from test_charter_registry import BASE  # noqa: E402


def test_temporal_plan_has_deterministic_workflow_and_safety_gates() -> None:
    scope = "sha256:" + "9" * 64
    first = compile_plan(copy.deepcopy(BASE), scope)
    second = compile_plan(copy.deepcopy(BASE), scope)
    assert first == second
    assert first["runner_mode"] == "temporal"
    assert first["workflow_id"].startswith("charter:")
    write = next(item for item in first["activities"] if item["activity_id"] == "create-linear")
    assert write["requires_idempotency_key"] is True
    assert write["requires_approval_gate"] is True
    assert write["requires_destination_readback"] is True
    assert "PermissionDenied" in write["retry"]["non_retryable"]


def test_read_activity_does_not_require_write_gates() -> None:
    plan = compile_plan(copy.deepcopy(BASE), "sha256:" + "8" * 64)
    read = next(item for item in plan["activities"] if item["activity_id"] == "find-brief")
    assert read["requires_idempotency_key"] is False
    assert read["requires_approval_gate"] is False


def test_plan_stably_topologically_sorts_shuffled_steps() -> None:
    definition = copy.deepcopy(BASE)
    definition["steps"].reverse()
    plan = compile_plan(definition, "sha256:" + "7" * 64)
    ids = [item["activity_id"] for item in plan["activities"]]
    assert ids.index("find-brief") < ids.index("create-linear")


@pytest.mark.parametrize(("field", "value"), [("timeout_seconds", -1), ("maximum_attempts", True), ("maximum_attempts", 101)])
def test_plan_rejects_unbounded_or_invalid_step_policy(field: str, value) -> None:
    definition = copy.deepcopy(BASE)
    definition["steps"][0][field] = value
    with pytest.raises(CharterError):
        compile_plan(definition, "sha256:" + "7" * 64)


def test_plan_rejects_malformed_scope_digest() -> None:
    with pytest.raises(CharterError, match="sha256"):
        compile_plan(copy.deepcopy(BASE), "sha256:not-a-real-digest")
