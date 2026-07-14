#!/usr/bin/env python3
"""Verify issuer-signed charter attestations with an Ed25519 trust store."""

from __future__ import annotations

import base64
import hashlib
import json
from datetime import datetime, timezone
from typing import Any

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey


class AttestationError(ValueError):
    """A compact attestation validation failure."""


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def subject_digest(subject: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(subject)).hexdigest()


def parse_time(value: Any, label: str) -> datetime:
    if not isinstance(value, str) or not value or len(value) > 80:
        raise AttestationError(f"{label} must be an ISO-8601 timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise AttestationError(f"{label} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise AttestationError(f"{label} must include a timezone")
    return parsed.astimezone(timezone.utc)


def validate_trust_store(store: dict[str, Any]) -> None:
    if store.get("trust_store_version") != "1.0" or not isinstance(store.get("keys"), dict):
        raise AttestationError("trust store must contain trust_store_version 1.0 and a keys object")
    seen_public_keys: set[str] = set()
    active_usages: set[str] = set()
    for key_id, record in store["keys"].items():
        if not isinstance(key_id, str) or not key_id or not isinstance(record, dict):
            raise AttestationError("trust store keys must map non-empty key IDs to objects")
        if not isinstance(record.get("issuer"), str) or not record["issuer"]:
            raise AttestationError(f"trust key {key_id} requires an issuer")
        usages = record.get("usages")
        if not isinstance(usages, list) or len(usages) != 1 or usages[0] not in {"capability", "approval", "receipt"}:
            raise AttestationError(f"trust key {key_id} must have exactly one supported usage")
        status = record.get("status")
        if status not in {"active", "retired", "revoked"}:
            raise AttestationError(f"trust key {key_id} requires active, retired, or revoked status")
        if status in {"retired", "revoked"} and not isinstance(record.get(f"{status}_at"), str):
            raise AttestationError(f"trust key {key_id} requires {status}_at")
        if not isinstance(record.get("activated_at"), str):
            raise AttestationError(f"trust key {key_id} requires activated_at")
        if status == "active":
            if usages[0] in active_usages:
                raise AttestationError(f"trust store has multiple active keys for usage {usages[0]}")
            active_usages.add(usages[0])
        try:
            encoded_key = record.get("public_key", "")
            raw = base64.b64decode(encoded_key, validate=True)
            Ed25519PublicKey.from_public_bytes(raw)
        except (ValueError, TypeError) as exc:
            raise AttestationError(f"trust key {key_id} has an invalid Ed25519 public key") from exc
        if encoded_key in seen_public_keys:
            raise AttestationError("trust store must use distinct key material per usage")
        seen_public_keys.add(encoded_key)
    missing_usages = {"capability", "approval", "receipt"} - active_usages
    if missing_usages:
        raise AttestationError(f"trust store missing issuer keys for: {', '.join(sorted(missing_usages))}")


def verify_attestation(
    subject: dict[str, Any],
    attestation: dict[str, Any],
    trust_store: dict[str, Any],
    usage: str,
    *,
    now: datetime | None = None,
    allow_expired: bool = False,
) -> dict[str, str]:
    validate_trust_store(trust_store)
    required = {"issuer", "key_id", "issued_at", "expires_at", "nonce", "subject_digest", "signature"}
    if not isinstance(attestation, dict) or set(attestation) != required:
        raise AttestationError("attestation fields must exactly match the signed envelope contract")
    for field in required:
        if not isinstance(attestation[field], str) or not attestation[field]:
            raise AttestationError(f"attestation.{field} must be a non-empty string")
    if len(attestation["nonce"]) > 200:
        raise AttestationError("attestation.nonce is too long")
    expected_digest = subject_digest(subject)
    if attestation["subject_digest"] != expected_digest:
        raise AttestationError("attestation subject_digest does not match the subject")
    record = trust_store["keys"].get(attestation["key_id"])
    if record is None:
        raise AttestationError("attestation key_id is not trusted")
    if record["issuer"] != attestation["issuer"]:
        raise AttestationError("attestation issuer does not match the trusted key")
    if usage not in record["usages"]:
        raise AttestationError(f"attestation key is not trusted for {usage}")
    issued_at = parse_time(attestation["issued_at"], "attestation.issued_at")
    expires_at = parse_time(attestation["expires_at"], "attestation.expires_at")
    current = now or datetime.now(timezone.utc)
    activated_at = parse_time(record["activated_at"], f"trust key {attestation['key_id']}.activated_at")
    if issued_at < activated_at:
        raise AttestationError("attestation was issued before its key was activated")
    if issued_at > current or (not allow_expired and expires_at <= current) or expires_at <= issued_at:
        raise AttestationError("attestation is not currently valid")
    status = record["status"]
    if status != "active":
        status_at = parse_time(record[f"{status}_at"], f"trust key {attestation['key_id']}.{status}_at")
        if not allow_expired:
            raise AttestationError(f"attestation key is {status}")
        if issued_at >= status_at:
            raise AttestationError(f"attestation was issued after its key was {status}")
    signed = {field: attestation[field] for field in sorted(attestation) if field != "signature"}
    try:
        signature = base64.b64decode(attestation["signature"], validate=True)
        public_key = Ed25519PublicKey.from_public_bytes(base64.b64decode(record["public_key"], validate=True))
        public_key.verify(signature, canonical_bytes(signed))
    except (ValueError, TypeError, InvalidSignature) as exc:
        raise AttestationError("attestation signature is invalid") from exc
    return {
        "issuer": attestation["issuer"],
        "key_id": attestation["key_id"],
        "nonce": attestation["nonce"],
        "subject_digest": expected_digest,
    }
