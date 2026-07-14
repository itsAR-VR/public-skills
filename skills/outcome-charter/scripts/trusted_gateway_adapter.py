#!/usr/bin/env python3
"""Reference runner adapter backed by isolated signed capability services."""

from __future__ import annotations

import asyncio
import json
import os
import ssl
import urllib.request
from typing import Any
from urllib.parse import urlparse

from attestations import verify_attestation
from charter_registry import canonical_value, default_trust_store, require_digest, sha256_label
from runner_core import validate_activity_result, validate_plan


def service_url(name: str) -> str:
    value = os.environ.get(name)
    if not value or urlparse(value).scheme != "https":
        raise RuntimeError(f"{name} must be a runner-owned HTTPS service URL")
    return value.rstrip("/")


def tls_context() -> ssl.SSLContext:
    context = ssl.create_default_context(cafile=os.environ.get("OUTCOME_CHARTER_MTLS_CA"))
    certificate = os.environ.get("OUTCOME_CHARTER_MTLS_CERT")
    private_key = os.environ.get("OUTCOME_CHARTER_MTLS_KEY")
    if not certificate or not private_key:
        raise RuntimeError("runner mTLS certificate and key are required")
    context.load_cert_chain(certificate, private_key)
    return context


def post_json(base_env: str, path: str, payload: dict[str, Any]) -> dict[str, Any]:
    request = urllib.request.Request(
        service_url(base_env) + path,
        data=json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8"),
        headers={"content-type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, context=tls_context(), timeout=30) as response:
        body = response.read(1_000_001)
    if len(body) > 1_000_000:
        raise RuntimeError("trusted gateway response exceeds one megabyte")
    value = json.loads(body)
    if not isinstance(value, dict):
        raise RuntimeError("trusted gateway response must be a JSON object")
    return value


def verified_response(value: dict[str, Any], usage: str) -> tuple[dict[str, Any], dict[str, str]]:
    attestation = value.get("attestation")
    subject = {field: value[field] for field in sorted(value) if field != "attestation"}
    trust_store = default_trust_store(required=True)
    assert trust_store is not None
    verified = verify_attestation(subject, attestation, trust_store, usage)
    return subject, verified


async def preflight(submission: dict[str, Any]) -> dict[str, Any]:
    value = await asyncio.to_thread(post_json, "OUTCOME_CHARTER_CAPABILITY_GATEWAY", "/v1/charters/preflight", submission)
    subject, _ = verified_response(value, "capability")
    if subject["submission_digest"] != sha256_label(submission):
        raise RuntimeError("capability gateway signed the wrong submission")
    plan = subject["trusted_plan"]
    validate_plan(plan)
    if sha256_label(plan) != submission["plan_ref"]:
        raise RuntimeError("trusted plan content does not match plan_ref")
    if plan["workflow_id"] != submission["workflow_id"]:
        raise RuntimeError("capability gateway returned the wrong workflow identity")
    if plan["charter_id"] != submission["charter_id"]:
        raise RuntimeError("capability gateway returned the wrong charter identity")
    if plan["definition_digest"] != submission["definition_digest"]:
        raise RuntimeError("capability gateway returned the wrong definition")
    if plan["execution_scope_digest"] != submission["execution_scope_digest"]:
        raise RuntimeError("capability gateway returned the wrong execution scope")
    if subject["inputs_ref"] != submission["inputs_ref"]:
        raise RuntimeError("capability gateway returned the wrong input reference")
    for field in ("plan_ref", "capability_ref"):
        if subject[field] != submission[field]:
            raise RuntimeError(f"capability gateway returned the wrong {field}")
    if plan["workflow_type"] != submission["workflow_type"] or plan["task_queue"] != submission["task_queue"]:
        raise RuntimeError("capability gateway returned the wrong runner routing")
    if plan["overall_timeout_seconds"] != submission["overall_timeout_seconds"]:
        raise RuntimeError("capability gateway returned the wrong execution timeout")
    return {"trusted_plan": plan, "inputs_ref": subject["inputs_ref"]}


async def authorize(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["submission"]["approval_ref"] is None:
        raise RuntimeError("trusted plan requires an approval reference")
    request = {
        "workflow_id": payload["trusted_plan"]["workflow_id"],
        "definition_digest": payload["trusted_plan"]["definition_digest"],
        "execution_scope_digest": payload["trusted_plan"]["execution_scope_digest"],
        "preview_digest": payload["submission"]["preview_digest"],
        "approval_ref": payload["submission"]["approval_ref"],
        "action_manifest_digest": sha256_label(canonical_value(payload["actions"])),
    }
    value = await asyncio.to_thread(post_json, "OUTCOME_CHARTER_APPROVAL_SERVICE", "/v1/approvals/claim", request)
    subject, _ = verified_response(value, "approval")
    for field in ("workflow_id", "definition_digest", "execution_scope_digest", "preview_digest", "approval_ref", "action_manifest_digest"):
        if subject[field] != request[field]:
            raise RuntimeError(f"authorization grant {field} does not match")
    require_digest(subject["authorization_grant_ref"], "authorization_grant_ref")
    return {"authorization_grant_ref": subject["authorization_grant_ref"]}


async def execute_step(payload: dict[str, Any]) -> dict[str, Any]:
    value = await asyncio.to_thread(post_json, "OUTCOME_CHARTER_CAPABILITY_GATEWAY", "/v1/operations/execute", payload)
    return validate_activity_result(value, payload["activity"]["activity_id"])


async def emit_receipt(payload: dict[str, Any]) -> dict[str, Any]:
    actual_manifest_digest = sha256_label(payload["result_envelopes"])
    if payload["result_manifest_digest"] != actual_manifest_digest:
        raise RuntimeError("result manifest digest does not match result envelopes")
    by_id = {item["activity_id"]: item for item in payload["result_envelopes"]}
    for activity_id in payload["required_readbacks"]:
        if activity_id not in by_id or not by_id[activity_id]["destination_readback"]:
            raise RuntimeError(f"required destination readback missing for {activity_id}")
    value = await asyncio.to_thread(post_json, "OUTCOME_CHARTER_VERIFIER_SERVICE", "/v1/receipts/emit", payload)
    subject, _ = verified_response(value, "receipt")
    require_digest(subject["receipt_ref"], "receipt_ref")
    attempted = sum(item["attempted_items"] for item in payload["result_envelopes"])
    successful = sum(item["successful_items"] for item in payload["result_envelopes"])
    if subject["attempted_items"] != attempted or subject["successful_items"] != successful:
        raise RuntimeError("signed receipt totals do not match result envelopes")
    expected = {
        "workflow_id": payload["submission"]["workflow_id"],
        "charter_id": payload["submission"]["charter_id"],
        "definition_digest": payload["submission"]["definition_digest"],
        "execution_scope_digest": payload["submission"]["execution_scope_digest"],
        "result_manifest_digest": actual_manifest_digest,
        "required_readbacks_digest": sha256_label(sorted(payload["required_readbacks"])),
    }
    for field, expected_value in expected.items():
        if subject[field] != expected_value:
            raise RuntimeError(f"signed receipt {field} does not match this execution")
    if subject.get("required_readbacks_verified") is not True:
        raise RuntimeError("signed receipt did not verify every required destination readback")
    return {
        "receipt_ref": subject["receipt_ref"],
        "attempted_items": attempted,
        "successful_items": successful,
    }
