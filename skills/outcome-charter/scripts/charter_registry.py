#!/usr/bin/env python3
"""Deterministic matching, authorization, and proof for outcome charters."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from attestations import AttestationError, verify_attestation

try:
    import fcntl
except ImportError:  # pragma: no cover - Windows fallback
    fcntl = None
    import msvcrt


COMPATIBILITY_FIELDS = (
    "outcome_class",
    "charter_version",
    "auth_context",
    "tool_schemas",
    "approval_policy_version",
    "requires_current_approval",
    "required_inputs",
    "required_outputs",
    "runner_contract_version",
)
SIDE_EFFECTS = {"none", "read", "write", "send", "publish", "delete", "spend", "sign", "deploy"}
GATED_SIDE_EFFECTS = SIDE_EFFECTS - {"none", "read"}
REQUIRED_QUERY_FIELDS = (
    *COMPATIBILITY_FIELDS,
    "auth_validated_at",
    "auth_max_age_seconds",
    "operator_id",
    "approval_scope_digest",
    "preview_digest",
    "action_count",
)
REQUIRED_DEFINITION_FIELDS = (
    "charter_id",
    *COMPATIBILITY_FIELDS,
    "allowed_verifiers",
    "minimum_promotion_items",
    "runner",
    "steps",
    "receipts",
)
ALLOWED_RECEIPT_FIELDS = {
    "run_id",
    "charter_id",
    "definition_digest",
    "compatibility_fingerprint",
    "verifier_id",
    "evidence_digest",
    "completed_at",
    "verified",
    "destination_readback",
    "attempted_items",
    "successful_items",
    "policy_violation",
    "failure_code",
    "attestation",
}
REQUIRED_RECEIPT_FIELDS = ALLOWED_RECEIPT_FIELDS - {"completed_at", "failure_code", "attestation"}
REQUIRED_APPROVAL_FIELDS = {
    "approval_id",
    "operator_id",
    "charter_id",
    "definition_digest",
    "compatibility_fingerprint",
    "scope_digest",
    "preview_digest",
    "action_count",
    "approved_action",
    "approved_at",
    "expires_at",
}
SHA256_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")
DEFAULT_APPROVAL_USE_LOG = Path("/var/lib/outcome-charter/consumed-approval-nonces.log")
DEFAULT_TRUST_STORE = Path("/etc/outcome-charter/trust-store.json")
SUGGEST_VERIFIED_RUNS = 1
REUSE_VERIFIED_RUNS = 3
REUSE_SUCCESS_RATE = 0.95


class CharterError(ValueError):
    """A compact, safe charter validation failure."""


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CharterError(f"cannot read valid JSON from {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise CharterError(f"{path} must contain a JSON object")
    return value


def canonical_value(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: canonical_value(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        normalized = [canonical_value(item) for item in value]
        if all(isinstance(item, str) for item in normalized):
            return sorted(normalized)
        if all(isinstance(item, dict) and "provider" in item for item in normalized):
            return sorted(normalized, key=lambda item: json.dumps(item, sort_keys=True))
        return normalized
    return value


def canonical_hash(value: Any) -> str:
    payload = json.dumps(canonical_value(value), separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def sha256_label(value: Any) -> str:
    return f"sha256:{canonical_hash(value)}"


def require_fields(value: dict[str, Any], fields, label: str) -> None:
    missing = [field for field in fields if field not in value]
    if missing:
        raise CharterError(f"{label} missing required fields: {', '.join(sorted(missing))}")


def require_string(value: Any, label: str, limit: int = 240) -> None:
    if not isinstance(value, str) or not value or len(value) > limit:
        raise CharterError(f"{label} must be a non-empty string of at most {limit} characters")


def require_digest(value: Any, label: str) -> None:
    if not isinstance(value, str) or not SHA256_PATTERN.fullmatch(value):
        raise CharterError(f"{label} must be a sha256: digest")


def require_integer(value: Any, label: str, *, minimum: int = 0, maximum: int = 1_000_000_000) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise CharterError(f"{label} must be an integer")
    if value < minimum or value > maximum:
        raise CharterError(f"{label} must be between {minimum} and {maximum}")
    return value


def parse_timestamp(value: Any, label: str) -> datetime:
    require_string(value, label, 80)
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise CharterError(f"{label} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise CharterError(f"{label} must include a timezone")
    return parsed.astimezone(timezone.utc)


def validate_auth_context(value: Any, label: str) -> None:
    if not isinstance(value, list) or not value:
        raise CharterError(f"{label} must be a non-empty list")
    identities: set[tuple[str, str, str]] = set()
    for index, connection in enumerate(value):
        if not isinstance(connection, dict):
            raise CharterError(f"{label}[{index}] must be an object")
        require_fields(connection, {"provider", "principal_id", "tenant_id", "scopes"}, f"{label}[{index}]")
        for field in ("provider", "principal_id", "tenant_id"):
            require_string(connection[field], f"{label}[{index}].{field}", 200)
        scopes = connection["scopes"]
        if not isinstance(scopes, list) or not scopes or not all(isinstance(scope, str) and scope for scope in scopes):
            raise CharterError(f"{label}[{index}].scopes must be a non-empty string list")
        if len(scopes) != len(set(scopes)):
            raise CharterError(f"{label}[{index}].scopes must not contain duplicates")
        identity = (connection["provider"], connection["principal_id"], connection["tenant_id"])
        if identity in identities:
            raise CharterError(f"{label} contains a duplicate connector principal")
        identities.add(identity)


def validate_compatibility_contract(value: dict[str, Any], label: str, *, query: bool = False) -> None:
    require_fields(value, REQUIRED_QUERY_FIELDS if query else COMPATIBILITY_FIELDS, label)
    for field in ("outcome_class", "charter_version", "approval_policy_version", "runner_contract_version"):
        require_string(value[field], f"{label}.{field}")
    if not isinstance(value["requires_current_approval"], bool):
        raise CharterError(f"{label}.requires_current_approval must be a boolean")
    validate_auth_context(value["auth_context"], f"{label}.auth_context")
    for field in ("required_inputs", "required_outputs"):
        values = value[field]
        if not isinstance(values, list) or not all(isinstance(item, str) and item for item in values):
            raise CharterError(f"{label}.{field} must be a list of non-empty strings")
        if len(values) != len(set(values)):
            raise CharterError(f"{label}.{field} must not contain duplicates")
    schemas = value["tool_schemas"]
    if not isinstance(schemas, dict) or not schemas:
        raise CharterError(f"{label}.tool_schemas must be a non-empty object")
    for operation, contract in schemas.items():
        require_string(operation, f"{label}.tool_schemas operation")
        if not isinstance(contract, dict):
            raise CharterError(f"{label}.tool_schemas[{operation}] must be an operation contract")
        require_fields(contract, {"schema_digest", "provider", "required_scopes", "side_effect"}, f"{label}.tool_schemas[{operation}]")
        require_digest(contract["schema_digest"], f"{label}.tool_schemas[{operation}].schema_digest")
        require_string(contract["provider"], f"{label}.tool_schemas[{operation}].provider")
        if contract["side_effect"] not in SIDE_EFFECTS:
            raise CharterError(f"{label}.tool_schemas[{operation}].side_effect is invalid")
        if not isinstance(contract["required_scopes"], list) or not all(
            isinstance(scope, str) and scope for scope in contract["required_scopes"]
        ):
            raise CharterError(f"{label}.tool_schemas[{operation}].required_scopes must be a string list")
    if query:
        require_string(value["operator_id"], f"{label}.operator_id")
        for field in ("approval_scope_digest", "preview_digest"):
            require_digest(value[field], f"{label}.{field}")
        require_integer(value["action_count"], f"{label}.action_count", minimum=0)
        max_age = require_integer(value["auth_max_age_seconds"], f"{label}.auth_max_age_seconds", minimum=1, maximum=3600)
        validated_at = parse_timestamp(value["auth_validated_at"], f"{label}.auth_validated_at")
        age = (datetime.now(timezone.utc) - validated_at).total_seconds()
        if age < -60 or age > max_age:
            raise CharterError(f"{label}.auth_validated_at is not fresh")


def compatibility_projection(value: dict[str, Any]) -> dict[str, Any]:
    validate_compatibility_contract(value, "compatibility contract")
    return {field: canonical_value(value[field]) for field in COMPATIBILITY_FIELDS}


def compatibility_fingerprint(value: dict[str, Any]) -> str:
    return sha256_label(compatibility_projection(value))


def validate_steps(steps: Any, auth_context: list[dict[str, Any]]) -> None:
    if not isinstance(steps, list) or not steps:
        raise CharterError("charter definition.steps must be a non-empty list")
    step_ids: list[str] = []
    for index, step in enumerate(steps):
        if not isinstance(step, dict):
            raise CharterError(f"charter definition.steps[{index}] must be an object")
        require_fields(step, {"step_id", "operation", "depends_on", "side_effect", "input_fields"}, f"steps[{index}]")
        require_string(step["step_id"], f"steps[{index}].step_id")
        require_string(step["operation"], f"steps[{index}].operation")
        if not isinstance(step["depends_on"], list) or not all(isinstance(item, str) for item in step["depends_on"]):
            raise CharterError(f"steps[{index}].depends_on must be a string list")
        if not isinstance(step["input_fields"], list) or not all(isinstance(item, str) and item for item in step["input_fields"]):
            raise CharterError(f"steps[{index}].input_fields must be a string list")
        if step["side_effect"] not in SIDE_EFFECTS:
            raise CharterError(f"step {step['step_id']} has unknown side_effect {step['side_effect']!r}")
        if step["side_effect"] in GATED_SIDE_EFFECTS and step.get("idempotency_required") is not True:
            raise CharterError(f"side-effecting step {step['step_id']} must require idempotency")
        if step["side_effect"] != "none":
            auth = step.get("auth")
            if not isinstance(auth, dict):
                raise CharterError(f"external step {step['step_id']} requires an auth binding")
            require_fields(auth, {"provider", "principal_id", "tenant_id", "required_scopes"}, f"step {step['step_id']}.auth")
            required_scopes = auth["required_scopes"]
            if not isinstance(required_scopes, list) or not required_scopes or not all(
                isinstance(scope, str) and scope for scope in required_scopes
            ):
                raise CharterError(f"step {step['step_id']}.auth.required_scopes must be a non-empty string list")
            connection = next(
                (
                    item
                    for item in auth_context
                    if all(item[field] == auth[field] for field in ("provider", "principal_id", "tenant_id"))
                ),
                None,
            )
            if connection is None:
                raise CharterError(f"step {step['step_id']} auth binding is not in the charter auth context")
            missing_scopes = set(required_scopes) - set(connection["scopes"])
            if missing_scopes:
                raise CharterError(f"step {step['step_id']} lacks required scopes: {', '.join(sorted(missing_scopes))}")
        if "timeout_seconds" in step:
            require_integer(step["timeout_seconds"], f"step {step['step_id']}.timeout_seconds", minimum=1, maximum=86_400)
        if "maximum_attempts" in step:
            require_integer(step["maximum_attempts"], f"step {step['step_id']}.maximum_attempts", minimum=1, maximum=100)
        step_ids.append(step["step_id"])
    if len(step_ids) != len(set(step_ids)):
        raise CharterError("charter definition step_id values must be unique")
    known = set(step_ids)
    graph = {step["step_id"]: step["depends_on"] for step in steps}
    for step_id, dependencies in graph.items():
        unknown = set(dependencies) - known
        if unknown:
            raise CharterError(f"step {step_id} has unknown dependencies: {', '.join(sorted(unknown))}")
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(step_id: str) -> None:
        if step_id in visiting:
            raise CharterError("charter definition steps contain a dependency cycle")
        if step_id in visited:
            return
        visiting.add(step_id)
        for dependency in graph[step_id]:
            visit(dependency)
        visiting.remove(step_id)
        visited.add(step_id)

    for step_id in step_ids:
        visit(step_id)


def approval_required_from_steps(steps: list[dict[str, Any]]) -> bool:
    return any(step["side_effect"] in GATED_SIDE_EFFECTS for step in steps)


def definition_digest(definition: dict[str, Any]) -> str:
    executable = {key: value for key, value in definition.items() if key not in {"receipts", "metadata"}}
    return sha256_label(executable)


def validate_receipt(receipt: dict[str, Any]) -> None:
    require_fields(receipt, REQUIRED_RECEIPT_FIELDS, "receipt")
    extra = set(receipt) - ALLOWED_RECEIPT_FIELDS
    if extra:
        raise CharterError(f"receipt contains forbidden fields: {', '.join(sorted(extra))}")
    for field in ("run_id", "charter_id", "verifier_id"):
        require_string(receipt[field], f"receipt.{field}")
    for field in ("definition_digest", "compatibility_fingerprint", "evidence_digest"):
        require_digest(receipt[field], f"receipt.{field}")
    for field in ("verified", "destination_readback", "policy_violation"):
        if not isinstance(receipt[field], bool):
            raise CharterError(f"receipt.{field} must be a boolean")
    attempted = require_integer(receipt["attempted_items"], "receipt.attempted_items")
    successful = require_integer(receipt["successful_items"], "receipt.successful_items")
    if successful > attempted:
        raise CharterError("receipt.successful_items cannot exceed attempted_items")
    if receipt["verified"] and not receipt["destination_readback"]:
        raise CharterError("verified receipts require destination_readback=true")
    if receipt["verified"] and receipt["policy_violation"]:
        raise CharterError("a policy-violating run cannot be verified")
    if receipt["verified"] and attempted == 0:
        raise CharterError("verified receipts require at least one attempted item")
    if "completed_at" in receipt:
        parse_timestamp(receipt["completed_at"], "receipt.completed_at")
    if "failure_code" in receipt:
        require_string(receipt["failure_code"], "receipt.failure_code", 120)
    if "attestation" in receipt:
        envelope = receipt["attestation"]
        if not isinstance(envelope, dict):
            raise CharterError("receipt.attestation must be an object")
        # Enforce the exact envelope schema even when no trust store is
        # present or the receipt is unverified — otherwise arbitrary nested
        # payloads ride into the registry and JSONL log under this key.
        envelope_fields = {"issuer", "key_id", "issued_at", "expires_at", "nonce", "subject_digest", "signature"}
        if set(envelope) != envelope_fields:
            raise CharterError("receipt.attestation must contain exactly the attestation-envelope fields")
        for field in sorted(envelope_fields):
            require_string(envelope[field], f"receipt.attestation.{field}", 2048)
        parse_timestamp(envelope["issued_at"], "receipt.attestation.issued_at")
        parse_timestamp(envelope["expires_at"], "receipt.attestation.expires_at")


def attestation_subject(value: dict[str, Any]) -> dict[str, Any]:
    return {field: value[field] for field in sorted(value) if field != "attestation"}


def trusted_attestation(
    value: dict[str, Any], trust_store: dict[str, Any] | None, usage: str, *, required: bool = False
) -> dict[str, str] | None:
    envelope = value.get("attestation")
    if envelope is None or trust_store is None:
        if required:
            raise CharterError(f"{usage} requires a trusted signed attestation")
        return None
    try:
        verified = verify_attestation(
            attestation_subject(value), envelope, trust_store, usage, allow_expired=usage == "receipt"
        )
        if usage == "receipt":
            if "completed_at" not in value:
                raise CharterError("trusted receipt requires completed_at")
            completed_at = parse_timestamp(value["completed_at"], "receipt.completed_at")
            issued_at = parse_timestamp(envelope["issued_at"], "receipt.attestation.issued_at")
            if issued_at < completed_at or (issued_at - completed_at).total_seconds() > 300:
                raise CharterError("receipt attestation must be issued within five minutes after completion")
        return verified
    except AttestationError as exc:
        raise CharterError(str(exc)) from exc


def validate_definition(definition: dict[str, Any]) -> None:
    require_fields(definition, REQUIRED_DEFINITION_FIELDS, "charter definition")
    validate_compatibility_contract(definition, "charter definition")
    require_string(definition["charter_id"], "charter definition.charter_id")
    validate_steps(definition["steps"], definition["auth_context"])
    missing_schemas = sorted(
        step["operation"]
        for step in definition["steps"]
        if step["side_effect"] != "none" and step["operation"] not in definition["tool_schemas"]
    )
    if missing_schemas:
        raise CharterError(f"external step operations missing schema digests: {', '.join(missing_schemas)}")
    for step in definition["steps"]:
        unknown_inputs = set(step["input_fields"]) - set(definition["required_inputs"])
        if unknown_inputs:
            raise CharterError(f"step {step['step_id']} references unknown input fields")
        contract = definition["tool_schemas"].get(step["operation"])
        if contract is not None and contract["side_effect"] != step["side_effect"]:
            # A step must never out-declare its trusted operation contract:
            # side_effect "none" on a contracted write operation would derive
            # requires_current_approval=false and skip every approval,
            # idempotency, and readback gate downstream.
            raise CharterError(f"step {step['step_id']} side_effect does not match its operation contract")
        if step["side_effect"] == "none":
            continue
        auth = step["auth"]
        if contract["provider"] != auth["provider"]:
            raise CharterError(f"step {step['step_id']} provider does not match its operation contract")
        if set(contract["required_scopes"]) - set(auth["required_scopes"]):
            raise CharterError(f"step {step['step_id']} omits operation-contract scopes")
    derived_approval = approval_required_from_steps(definition["steps"])
    if definition["requires_current_approval"] != derived_approval:
        raise CharterError("requires_current_approval must equal the approval derived from side-effecting steps")
    verifiers = definition["allowed_verifiers"]
    if not isinstance(verifiers, list) or not verifiers or not all(isinstance(item, str) and item for item in verifiers):
        raise CharterError("allowed_verifiers must be a non-empty string list")
    if len(verifiers) != len(set(verifiers)):
        raise CharterError("allowed_verifiers must not contain duplicates")
    require_integer(definition["minimum_promotion_items"], "minimum_promotion_items", minimum=1)
    runner = definition["runner"]
    if not isinstance(runner, dict):
        raise CharterError("runner must be an object")
    require_fields(runner, {"mode", "workflow_type", "task_queue", "max_concurrency", "overall_timeout_seconds"}, "runner")
    if runner["mode"] not in {"direct", "checkpointed", "temporal"}:
        raise CharterError("runner.mode must be direct, checkpointed, or temporal")
    for field in ("workflow_type", "task_queue"):
        require_string(runner[field], f"runner.{field}")
    require_integer(runner["max_concurrency"], "runner.max_concurrency", minimum=1, maximum=1000)
    require_integer(runner["overall_timeout_seconds"], "runner.overall_timeout_seconds", minimum=1, maximum=31_536_000)
    if not isinstance(definition["receipts"], list):
        raise CharterError("receipts must be a list")
    seen: set[tuple[str, str, str]] = set()
    for receipt in definition["receipts"]:
        if not isinstance(receipt, dict):
            raise CharterError("each receipt must be an object")
        validate_receipt(receipt)
        if receipt["charter_id"] != definition["charter_id"]:
            raise CharterError("receipt charter_id does not match its definition")
        key = (receipt["charter_id"], receipt["definition_digest"], receipt["run_id"])
        if key in seen:
            raise CharterError("duplicate receipt identity")
        seen.add(key)


def validate_registry(registry: dict[str, Any]) -> None:
    if registry.get("registry_version") != "1.0":
        raise CharterError("registry_version must be 1.0")
    charters = registry.get("charters")
    if not isinstance(charters, list):
        raise CharterError("registry.charters must be a list")
    seen: set[str] = set()
    for definition in charters:
        if not isinstance(definition, dict):
            raise CharterError("each registry charter must be an object")
        validate_definition(definition)
        if definition["charter_id"] in seen:
            raise CharterError(f"duplicate charter_id: {definition['charter_id']}")
        seen.add(definition["charter_id"])


def proof_stats(definition: dict[str, Any], trust_store: dict[str, Any] | None = None) -> dict[str, Any]:
    current_definition = definition_digest(definition)
    current_compatibility = compatibility_fingerprint(definition)
    current = [
        receipt
        for receipt in definition["receipts"]
        if receipt["definition_digest"] == current_definition
        and receipt["compatibility_fingerprint"] == current_compatibility
        and receipt["verifier_id"] in definition["allowed_verifiers"]
    ]
    verified = [receipt for receipt in current if receipt["verified"]]
    trusted_verified = []
    trusted_all = []
    for receipt in current:
        try:
            verified_attestation = trusted_attestation(receipt, trust_store, "receipt")
            if verified_attestation is not None and verified_attestation["issuer"] == receipt["verifier_id"]:
                trusted_all.append(receipt)
                if receipt["verified"]:
                    trusted_verified.append(receipt)
        except CharterError:
            continue
    attempted = sum(receipt["attempted_items"] for receipt in verified)
    successful = sum(receipt["successful_items"] for receipt in verified)
    return {
        "verified_runs": len(verified),
        "trusted_verified_runs": len(trusted_verified),
        # Item totals cover ALL trusted receipts, including signed failures
        # (verified=false): counting only successes let three good runs among
        # arbitrarily many signed failures present a 100% success rate.
        "trusted_attempted_items": sum(receipt["attempted_items"] for receipt in trusted_all),
        "trusted_successful_items": sum(receipt["successful_items"] for receipt in trusted_all),
        "verified_attempted_items": attempted,
        "verified_successful_items": successful,
        "success_rate": successful / attempted if attempted else 0.0,
        "policy_violations": sum(1 for receipt in current if receipt["policy_violation"]),
    }


def route_for(
    definition: dict[str, Any], trust_store: dict[str, Any] | None = None, *, capability_trusted: bool = False
) -> str:
    stats = proof_stats(definition, trust_store)
    if definition.get("disabled", False) or stats["policy_violations"]:
        return "compile"
    if (
        capability_trusted
        and stats["trusted_verified_runs"] >= REUSE_VERIFIED_RUNS
        and stats["trusted_attempted_items"] >= definition["minimum_promotion_items"]
        and stats["trusted_successful_items"] / stats["trusted_attempted_items"] >= REUSE_SUCCESS_RATE
    ):
        return "reuse"
    if stats["verified_runs"] >= SUGGEST_VERIFIED_RUNS:
        return "suggest"
    return "compile"


def mismatch_fields(definition: dict[str, Any], query: dict[str, Any]) -> list[str]:
    return [field for field in COMPATIBILITY_FIELDS if canonical_value(definition.get(field)) != canonical_value(query.get(field))]


def family_is_quarantined(
    registry: dict[str, Any], outcome_class: str, trust_store: dict[str, Any] | None
) -> bool:
    for definition in registry["charters"]:
        if definition["outcome_class"] != outcome_class:
            continue
        for receipt in definition["receipts"]:
            if not receipt["policy_violation"]:
                continue
            try:
                verified_attestation = trusted_attestation(receipt, trust_store, "receipt")
                if (
                    receipt["verifier_id"] in definition["allowed_verifiers"]
                    and verified_attestation is not None
                    and verified_attestation["issuer"] == receipt["verifier_id"]
                ):
                    return True
            except CharterError:
                continue
    return False


def match_charter(
    registry: dict[str, Any], query: dict[str, Any], trust_store: dict[str, Any] | None = None
) -> dict[str, Any]:
    validate_registry(registry)
    validate_compatibility_contract(query, "query", query=True)
    capability_trusted = trusted_attestation(query, trust_store, "capability") is not None
    fingerprint = compatibility_fingerprint(query)
    if family_is_quarantined(registry, query["outcome_class"], trust_store):
        return {
            "mode": "compile",
            "charter_id": None,
            "compatibility_fingerprint": fingerprint,
            "reason": "charter_family_quarantined_after_policy_violation",
            "near_matches": [],
            "approval_required": query["requires_current_approval"],
        }
    compatible = [definition for definition in registry["charters"] if compatibility_fingerprint(definition) == fingerprint]
    if not compatible:
        near = sorted(
            (
                {"charter_id": definition["charter_id"], "mismatched_fields": mismatch_fields(definition, query)}
                for definition in registry["charters"]
                if definition.get("outcome_class") == query.get("outcome_class")
            ),
            key=lambda item: (len(item["mismatched_fields"]), item["charter_id"]),
        )
        return {
            "mode": "compile",
            "charter_id": None,
            "compatibility_fingerprint": fingerprint,
            "reason": "no_exact_compatible_charter",
            "near_matches": near[:3],
            "approval_required": query["requires_current_approval"],
        }
    mode_rank = {"reuse": 2, "suggest": 1, "compile": 0}
    compatible.sort(
        key=lambda definition: (
            mode_rank[route_for(definition, trust_store, capability_trusted=capability_trusted)],
            proof_stats(definition, trust_store)["trusted_verified_runs"],
            definition["charter_id"],
        ),
        reverse=True,
    )
    best = compatible[0]
    mode = route_for(best, trust_store, capability_trusted=capability_trusted)
    stats = proof_stats(best, trust_store)
    reasons = {
        "reuse": "exact_compatibility_and_proven_success",
        "suggest": (
            "exact_compatibility_but_trusted_attestation_adapter_required"
            if stats["verified_runs"] >= REUSE_VERIFIED_RUNS and stats["success_rate"] >= REUSE_SUCCESS_RATE
            else "exact_compatibility_but_not_enough_verified_runs"
        ),
        "compile": "compatible_charter_lacks_safe_success_proof",
    }
    return {
        "mode": mode,
        "charter_id": best["charter_id"],
        "definition_digest": definition_digest(best),
        "compatibility_fingerprint": fingerprint,
        "reason": reasons[mode],
        "proof": {
            "verified_runs": stats["verified_runs"],
            "trusted_verified_runs": stats["trusted_verified_runs"],
            "verified_attempted_items": stats["verified_attempted_items"],
            "verified_successful_items": stats["verified_successful_items"],
            "success_rate": round(stats["success_rate"], 6),
            "policy_violations": stats["policy_violations"],
        },
        "approval_required": best["requires_current_approval"],
        "approval_carried_forward": False,
    }


def normalized_receipt(receipt: dict[str, Any]) -> dict[str, Any]:
    validate_receipt(receipt)
    value = {field: receipt[field] for field in sorted(receipt)}
    value.setdefault("completed_at", datetime.now(timezone.utc).isoformat())
    return value


def record_run(
    registry: dict[str, Any], receipt: dict[str, Any], trust_store: dict[str, Any] | None = None
) -> tuple[dict[str, Any], dict[str, Any]]:
    validate_registry(registry)
    clean = normalized_receipt(receipt)
    definition = next((item for item in registry["charters"] if item["charter_id"] == clean["charter_id"]), None)
    if definition is None:
        raise CharterError("receipt charter_id not found")
    if clean["definition_digest"] != definition_digest(definition):
        raise CharterError("receipt definition_digest does not match the current executable charter")
    if clean["compatibility_fingerprint"] != compatibility_fingerprint(definition):
        raise CharterError("receipt compatibility_fingerprint does not match the current charter")
    if clean["verifier_id"] not in definition["allowed_verifiers"]:
        raise CharterError("receipt verifier_id is not allowed for this charter")
    if clean["verified"] and trust_store is not None:
        verified_receipt = trusted_attestation(clean, trust_store, "receipt", required=True)
        assert verified_receipt is not None
        if verified_receipt["issuer"] != clean["verifier_id"]:
            raise CharterError("receipt verifier_id does not match the trusted attestation issuer")
    identity = (clean["charter_id"], clean["definition_digest"], clean["run_id"])
    for existing in definition["receipts"]:
        if (existing["charter_id"], existing["definition_digest"], existing["run_id"]) == identity:
            if existing == clean:
                return registry, {"recorded": False, "reason": "duplicate_receipt_identity", "run_id": clean["run_id"]}
            # Only byte-equivalent receipts are idempotent. Silently dropping a
            # differing receipt lets an unsigned duplicate recorded first
            # suppress later signed failure or policy-violation evidence.
            raise CharterError("conflicting receipt content for an existing run identity; refusing to suppress evidence")
    definition["receipts"].append(clean)
    return registry, {"recorded": True, "reason": "new_run", "run_id": clean["run_id"], "receipt": clean}


def authorize_execution(
    definition: dict[str, Any],
    query: dict[str, Any],
    approval: dict[str, Any] | None,
    trust_store: dict[str, Any] | None = None,
    used_approval_nonces: set[str] | None = None,
) -> dict[str, Any]:
    validate_definition(definition)
    # Routing is not an authorization boundary: a direct caller with valid
    # capability and approval data must still be stopped by the kill switch.
    if definition.get("disabled", False):
        raise CharterError("charter is disabled and cannot authorize execution")
    if proof_stats(definition, trust_store)["policy_violations"]:
        raise CharterError("charter family is under policy quarantine and cannot authorize execution")
    validate_compatibility_contract(query, "query", query=True)
    trusted_attestation(query, trust_store, "capability", required=True)
    if compatibility_fingerprint(definition) != compatibility_fingerprint(query):
        raise CharterError("execution query is not compatible with the charter")
    required = approval_required_from_steps(definition["steps"])
    if not required:
        return {"authorized": True, "approval_required": False, "approval_id": None}
    if approval is None:
        raise CharterError("current scoped approval is required for this charter")
    require_fields(approval, REQUIRED_APPROVAL_FIELDS, "approval")
    for field in ("approval_id", "operator_id", "charter_id", "approved_action"):
        require_string(approval[field], f"approval.{field}")
    for field in ("definition_digest", "compatibility_fingerprint", "scope_digest", "preview_digest"):
        require_digest(approval[field], f"approval.{field}")
    require_integer(approval["action_count"], "approval.action_count", minimum=1)
    if approval["charter_id"] != definition["charter_id"]:
        raise CharterError("approval charter_id does not match")
    if approval["definition_digest"] != definition_digest(definition):
        raise CharterError("approval definition_digest does not match")
    if approval["compatibility_fingerprint"] != compatibility_fingerprint(query):
        raise CharterError("approval compatibility_fingerprint does not match")
    if approval["scope_digest"] != query.get("approval_scope_digest"):
        raise CharterError("approval scope_digest does not match the current execution scope")
    if approval["operator_id"] != query["operator_id"]:
        raise CharterError("approval operator_id does not match the current operator")
    if approval["preview_digest"] != query["preview_digest"]:
        raise CharterError("approval preview_digest does not match the exact current preview")
    if approval["action_count"] != query["action_count"]:
        raise CharterError("approval action_count does not match the current execution")
    if approval["approved_action"] != "execute":
        raise CharterError("approval approved_action must be execute")
    now = datetime.now(timezone.utc)
    approved_at = parse_timestamp(approval["approved_at"], "approval.approved_at")
    expires_at = parse_timestamp(approval["expires_at"], "approval.expires_at")
    if approved_at > now or expires_at <= now:
        raise CharterError("approval is not currently valid")
    verified = trusted_attestation(approval, trust_store, "approval", required=True)
    assert verified is not None
    nonce_key = sha256_label(verified["nonce"])
    if used_approval_nonces is not None and nonce_key in used_approval_nonces:
        raise CharterError("approval attestation nonce has already been consumed")
    return {
        "authorized": True,
        "approval_required": True,
        "approval_id": approval["approval_id"],
        "approval_nonce_key": nonce_key,
    }


def write_json_atomic(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            json.dump(value, stream, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except OSError:
            pass
        raise


def append_receipt(path: Path, receipt: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(receipt, sort_keys=True, separators=(",", ":")) + "\n")
        stream.flush()
        os.fsync(stream.fileno())


def receipt_identity(receipt: dict[str, Any]) -> tuple[str, str, str]:
    return receipt["charter_id"], receipt["definition_digest"], receipt["run_id"]


def receipt_log_contains(path: Path, identity: tuple[str, str, str]) -> bool:
    if not path.exists():
        return False
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict) and all(field in value for field in ("charter_id", "definition_digest", "run_id")):
            if receipt_identity(value) == identity:
                return True
    return False


def consumed_nonces(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return {line for line in path.read_text(encoding="utf-8").splitlines() if line}


def consume_nonce(path: Path, nonce: str) -> None:
    require_string(nonce, "approval nonce", 200)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        stream.write(nonce + "\n")
        stream.flush()
        os.fsync(stream.fileno())


def authorize_and_consume(
    definition: dict[str, Any],
    query: dict[str, Any],
    approval: dict[str, Any] | None,
    trust_store: dict[str, Any],
    nonce_store: Path,
) -> dict[str, Any]:
    with registry_lock(nonce_store):
        result = authorize_execution(
            definition,
            query,
            approval,
            trust_store,
            consumed_nonces(nonce_store),
        )
        if result.get("approval_nonce_key"):
            consume_nonce(nonce_store, result["approval_nonce_key"])
        return result


def default_trust_store(*, required: bool) -> dict[str, Any] | None:
    if not DEFAULT_TRUST_STORE.exists():
        if required:
            raise CharterError(f"runner-owned trust store is missing at {DEFAULT_TRUST_STORE}")
        return None
    if DEFAULT_TRUST_STORE.is_symlink() or not DEFAULT_TRUST_STORE.is_file():
        raise CharterError("runner-owned trust store must be a regular non-symlink file")
    if DEFAULT_TRUST_STORE.stat().st_mode & 0o222:
        raise CharterError("runner-owned trust store must be read-only to the runner process")
    if DEFAULT_TRUST_STORE.parent.stat().st_mode & 0o022:
        raise CharterError("runner-owned trust-store directory must not be group/world writable")
    return load_json(DEFAULT_TRUST_STORE)


@contextmanager
def registry_lock(registry_path: Path):
    lock_path = registry_path.with_suffix(registry_path.suffix + ".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+", encoding="utf-8") as stream:
        if fcntl is not None:
            fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
        else:  # pragma: no cover - Windows fallback
            stream.seek(0)
            stream.write("0")
            stream.flush()
            msvcrt.locking(stream.fileno(), msvcrt.LK_LOCK, 1)
        try:
            yield
        finally:
            if fcntl is not None:
                fcntl.flock(stream.fileno(), fcntl.LOCK_UN)
            else:  # pragma: no cover - Windows fallback
                stream.seek(0)
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)


def idempotency_key(charter_id: str, step_id: str, business_object: str, input_version: str) -> str:
    for label, value in (("charter_id", charter_id), ("step_id", step_id), ("business_object", business_object), ("input_version", input_version)):
        require_string(value, label)
    return f"charter:{canonical_hash({'charter_id': charter_id, 'step_id': step_id, 'business_object': business_object, 'input_version': input_version})}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    match_parser = commands.add_parser("match")
    match_parser.add_argument("--registry", required=True, type=Path)
    match_parser.add_argument("--query", required=True, type=Path)
    validate_parser = commands.add_parser("validate")
    validate_parser.add_argument("--registry", type=Path)
    validate_parser.add_argument("--definition", type=Path)
    record_parser = commands.add_parser("record")
    record_parser.add_argument("--registry", required=True, type=Path)
    record_parser.add_argument("--receipt", required=True, type=Path)
    record_parser.add_argument("--receipt-log", required=True, type=Path)
    authorize_parser = commands.add_parser("authorize")
    authorize_parser.add_argument("--definition", required=True, type=Path)
    authorize_parser.add_argument("--query", required=True, type=Path)
    authorize_parser.add_argument("--approval", type=Path)
    key_parser = commands.add_parser("idempotency-key")
    key_parser.add_argument("--charter-id", required=True)
    key_parser.add_argument("--step-id", required=True)
    key_parser.add_argument("--business-object", required=True)
    key_parser.add_argument("--input-version", required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "match":
            result = match_charter(
                load_json(args.registry),
                load_json(args.query),
                default_trust_store(required=False),
            )
        elif args.command == "validate":
            if bool(args.registry) == bool(args.definition):
                raise CharterError("validate requires exactly one of --registry or --definition")
            value = load_json(args.registry or args.definition)
            validate_registry(value) if args.registry else validate_definition(value)
            result = {"valid": True, "type": "registry" if args.registry else "definition"}
        elif args.command == "record":
            with registry_lock(args.registry):
                registry, result = record_run(
                    load_json(args.registry),
                    load_json(args.receipt),
                    default_trust_store(required=False),
                )
                if result["recorded"]:
                    clean = result.pop("receipt")
                    identity = receipt_identity(clean)
                    if not receipt_log_contains(args.receipt_log, identity):
                        append_receipt(args.receipt_log, clean)
                    write_json_atomic(args.registry, registry)
        elif args.command == "authorize":
            trust_store = default_trust_store(required=True)
            assert trust_store is not None
            result = authorize_and_consume(
                load_json(args.definition),
                load_json(args.query),
                load_json(args.approval) if args.approval else None,
                trust_store,
                DEFAULT_APPROVAL_USE_LOG,
            )
        else:
            result = {"idempotency_key": idempotency_key(args.charter_id, args.step_id, args.business_object, args.input_version)}
    except (CharterError, OSError, TypeError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}, sort_keys=True))
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
