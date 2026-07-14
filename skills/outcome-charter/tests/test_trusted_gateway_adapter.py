from __future__ import annotations

import asyncio
import base64
import copy
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import trusted_gateway_adapter as adapter  # noqa: E402
from attestations import canonical_bytes, subject_digest  # noqa: E402
from charter_registry import definition_digest, sha256_label  # noqa: E402
from durable_plan import compile_plan  # noqa: E402
from temporal_submit import submission_scope_digest, submission_workflow_id  # noqa: E402
from test_charter_registry import BASE  # noqa: E402


ISSUERS = {"capability": "capability-registry", "approval": "approval-service", "receipt": "receipt-service"}
KEYS = {usage: Ed25519PrivateKey.generate() for usage in ISSUERS}
TRUST_STORE = {
    "trust_store_version": "1.0",
    "keys": {
        f"{usage}-key": {
            "issuer": ISSUERS[usage],
            "public_key": base64.b64encode(
                key.public_key().public_bytes(
                    encoding=serialization.Encoding.Raw,
                    format=serialization.PublicFormat.Raw,
                )
            ).decode(),
            "usages": [usage],
            "status": "active",
            "activated_at": "2026-01-01T00:00:00+00:00",
        }
        for usage, key in KEYS.items()
    },
}


def signed(subject: dict, usage: str, nonce: str) -> dict:
    now = datetime.now(timezone.utc)
    envelope = {
        "issuer": ISSUERS[usage],
        "key_id": f"{usage}-key",
        "issued_at": (now - timedelta(seconds=1)).isoformat(),
        "expires_at": (now + timedelta(minutes=5)).isoformat(),
        "nonce": nonce,
        "subject_digest": subject_digest(subject),
    }
    envelope["signature"] = base64.b64encode(KEYS[usage].sign(canonical_bytes(envelope))).decode()
    return {**subject, "attestation": envelope}


def fixture():
    submission = {
        "workflow_id": "placeholder",
        "charter_id": BASE["charter_id"],
        "workflow_type": "OutcomeCharterWorkflow",
        "task_queue": "outcome-charters",
        "overall_timeout_seconds": 3600,
        "plan_ref": "placeholder",
        "inputs_ref": "sha256:" + "2" * 64,
        "capability_ref": "sha256:" + "3" * 64,
        "approval_ref": "sha256:" + "4" * 64,
        "definition_digest": definition_digest(BASE),
        "execution_scope_digest": "placeholder",
        "preview_digest": "sha256:" + "7" * 64,
    }
    submission["execution_scope_digest"] = submission_scope_digest(submission)
    plan = compile_plan(copy.deepcopy(BASE), submission["execution_scope_digest"])
    submission["plan_ref"] = sha256_label(plan)
    submission["workflow_id"] = submission_workflow_id(submission)
    plan["workflow_id"] = submission["workflow_id"]
    submission["plan_ref"] = sha256_label(plan)
    return plan, submission


def result_envelope(activity_id: str, *, readback: bool = True) -> dict:
    return {
        "activity_id": activity_id,
        "result_ref": "sha256:" + "9" * 64,
        "evidence_digest": "sha256:" + "a" * 64,
        "attempted_items": 1,
        "successful_items": 1,
        "destination_readback": readback,
    }


def test_signed_gateway_contract_and_idempotent_grant(monkeypatch) -> None:
    plan, submission = fixture()
    monkeypatch.setattr(adapter, "default_trust_store", lambda required: TRUST_STORE)

    def fake_post(_base: str, path: str, payload: dict):
        if path.endswith("/preflight"):
            return signed(
                {
                    "trusted_plan": plan,
                    "inputs_ref": submission["inputs_ref"],
                    "plan_ref": submission["plan_ref"],
                    "capability_ref": submission["capability_ref"],
                    "submission_digest": sha256_label(submission),
                },
                "capability",
                "capability-1",
            )
        if path.endswith("/claim"):
            return signed({**payload, "authorization_grant_ref": "sha256:" + "8" * 64}, "approval", "grant-1")
        if path.endswith("/execute"):
            return result_envelope(payload["activity"]["activity_id"])
        attempted = sum(item["attempted_items"] for item in payload["result_envelopes"])
        successful = sum(item["successful_items"] for item in payload["result_envelopes"])
        return signed(
            {
                "receipt_ref": "sha256:" + "b" * 64,
                "workflow_id": submission["workflow_id"],
                "charter_id": submission["charter_id"],
                "definition_digest": submission["definition_digest"],
                "execution_scope_digest": submission["execution_scope_digest"],
                "result_manifest_digest": payload["result_manifest_digest"],
                "required_readbacks_digest": sha256_label(sorted(payload["required_readbacks"])),
                "required_readbacks_verified": True,
                "attempted_items": attempted,
                "successful_items": successful,
            },
            "receipt",
            "receipt-1",
        )

    monkeypatch.setattr(adapter, "post_json", fake_post)
    preflight = asyncio.run(adapter.preflight(submission))
    assert preflight["trusted_plan"] == plan
    actions = [{"activity_id": "create-linear", "operation": "linear.create", "side_effect": "write"}]
    grant_payload = {"submission": submission, "trusted_plan": plan, "actions": actions}
    first_grant = asyncio.run(adapter.authorize(grant_payload))
    second_grant = asyncio.run(adapter.authorize(grant_payload))
    assert first_grant == second_grant == {"authorization_grant_ref": "sha256:" + "8" * 64}
    write = next(item for item in plan["activities"] if item["requires_destination_readback"])
    execute_result = asyncio.run(adapter.execute_step({"activity": write}))
    receipt_payload = {
        "submission": submission,
        "trusted_plan_digest": plan["definition_digest"],
        "result_envelopes": [execute_result],
        "result_manifest_digest": sha256_label([execute_result]),
        "required_readbacks": [write["activity_id"]],
    }
    receipt = asyncio.run(adapter.emit_receipt(receipt_payload))
    assert receipt["receipt_ref"] == "sha256:" + "b" * 64


def test_preflight_rejects_plan_content_address_mismatch(monkeypatch) -> None:
    plan, submission = fixture()
    monkeypatch.setattr(adapter, "default_trust_store", lambda required: TRUST_STORE)
    wrong = copy.deepcopy(plan)
    wrong["max_concurrency"] += 1
    response = signed(
        {
            "trusted_plan": wrong,
            "inputs_ref": submission["inputs_ref"],
            "plan_ref": submission["plan_ref"],
            "capability_ref": submission["capability_ref"],
            "submission_digest": sha256_label(submission),
        },
        "capability",
        "capability-wrong-plan",
    )
    monkeypatch.setattr(adapter, "post_json", lambda *_args: response)
    with pytest.raises(RuntimeError, match="content does not match"):
        asyncio.run(adapter.preflight(submission))


def test_receipt_rejects_missing_readback_before_signing(monkeypatch) -> None:
    plan, submission = fixture()
    write = next(item for item in plan["activities"] if item["requires_destination_readback"])
    envelope = result_envelope(write["activity_id"], readback=False)
    payload = {
        "submission": submission,
        "trusted_plan_digest": plan["definition_digest"],
        "result_envelopes": [envelope],
        "result_manifest_digest": sha256_label([envelope]),
        "required_readbacks": [write["activity_id"]],
    }
    monkeypatch.setattr(adapter, "post_json", lambda *_args: pytest.fail("verifier must not be called"))
    with pytest.raises(RuntimeError, match="readback missing"):
        asyncio.run(adapter.emit_receipt(payload))


def test_receipt_rejects_signed_evidence_from_another_workflow(monkeypatch) -> None:
    plan, submission = fixture()
    monkeypatch.setattr(adapter, "default_trust_store", lambda required: TRUST_STORE)
    write = next(item for item in plan["activities"] if item["requires_destination_readback"])
    envelope = result_envelope(write["activity_id"])
    payload = {
        "submission": submission,
        "trusted_plan_digest": plan["definition_digest"],
        "result_envelopes": [envelope],
        "result_manifest_digest": sha256_label([envelope]),
        "required_readbacks": [write["activity_id"]],
    }
    response = signed(
        {
            "receipt_ref": "sha256:" + "b" * 64,
            "workflow_id": "charter:" + "f" * 64,
            "charter_id": submission["charter_id"],
            "definition_digest": submission["definition_digest"],
            "execution_scope_digest": submission["execution_scope_digest"],
            "result_manifest_digest": payload["result_manifest_digest"],
            "required_readbacks_digest": sha256_label(payload["required_readbacks"]),
            "required_readbacks_verified": True,
            "attempted_items": 1,
            "successful_items": 1,
        },
        "receipt",
        "receipt-wrong-workflow",
    )
    monkeypatch.setattr(adapter, "post_json", lambda *_args: response)
    with pytest.raises(RuntimeError, match="workflow_id"):
        asyncio.run(adapter.emit_receipt(payload))
