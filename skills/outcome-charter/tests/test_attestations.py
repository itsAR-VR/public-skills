from __future__ import annotations

import base64
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from attestations import AttestationError, canonical_bytes, subject_digest, verify_attestation  # noqa: E402


def fixture():
    privates = {usage: Ed25519PrivateKey.generate() for usage in ("capability", "approval", "receipt")}
    store = {
        "trust_store_version": "1.0",
        "keys": {
            f"{usage}-key-1": {
                "issuer": f"{usage}-service",
                "public_key": base64.b64encode(
                    private.public_key().public_bytes(
                        encoding=serialization.Encoding.Raw,
                        format=serialization.PublicFormat.Raw,
                    )
                ).decode(),
                "usages": [usage],
                "status": "active",
                "activated_at": "2026-01-01T00:00:00+00:00",
            }
            for usage, private in privates.items()
        },
    }
    store["keys"]["approval-key-1"]["issuer"] = "approval-service"
    return privates["approval"], store


def signed(subject, private, **patch):
    now = datetime.now(timezone.utc)
    envelope = {
        "issuer": "approval-service",
        "key_id": "approval-key-1",
        "issued_at": (now - timedelta(seconds=1)).isoformat(),
        "expires_at": (now + timedelta(minutes=5)).isoformat(),
        "nonce": "one-time-approval-1",
        "subject_digest": subject_digest(subject),
    }
    envelope.update(patch)
    envelope["signature"] = base64.b64encode(private.sign(canonical_bytes(envelope))).decode()
    return envelope


def test_valid_trusted_attestation() -> None:
    private, store = fixture()
    subject = {"charter_id": "investor-research-v1", "action": "execute"}
    result = verify_attestation(subject, signed(subject, private), store, "approval")
    assert result["issuer"] == "approval-service"
    assert result["nonce"] == "one-time-approval-1"


def test_tampered_subject_is_rejected() -> None:
    private, store = fixture()
    original = {"action": "execute"}
    with pytest.raises(AttestationError, match="subject_digest"):
        verify_attestation({"action": "delete"}, signed(original, private), store, "approval")


def test_wrong_usage_and_forged_signature_are_rejected() -> None:
    private, store = fixture()
    subject = {"action": "execute"}
    envelope = signed(subject, private)
    with pytest.raises(AttestationError, match="not trusted for capability"):
        verify_attestation(subject, envelope, store, "capability")
    forged = dict(envelope, signature=base64.b64encode(b"x" * 64).decode())
    with pytest.raises(AttestationError, match="signature is invalid"):
        verify_attestation(subject, forged, store, "approval")


def test_historical_receipt_can_be_verified_after_envelope_expiry() -> None:
    private, store = fixture()
    subject = {"run_id": "historical-1"}
    now = datetime.now(timezone.utc)
    envelope = signed(
        subject,
        private,
        issued_at=(now - timedelta(days=2)).isoformat(),
        expires_at=(now - timedelta(days=1)).isoformat(),
    )
    with pytest.raises(AttestationError, match="not currently valid"):
        verify_attestation(subject, envelope, store, "approval")
    result = verify_attestation(subject, envelope, store, "approval", allow_expired=True)
    assert result["subject_digest"] == subject_digest(subject)


def test_retired_receipt_key_remains_valid_for_pre_retirement_history() -> None:
    _, store = fixture()
    retired_private = Ed25519PrivateKey.generate()
    store["keys"]["receipt-key-retired"] = {
        "issuer": "receipt-service-old",
        "public_key": base64.b64encode(
            retired_private.public_key().public_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PublicFormat.Raw,
            )
        ).decode(),
        "usages": ["receipt"],
        "status": "retired",
        "activated_at": "2026-01-01T00:00:00+00:00",
        "retired_at": "2026-06-01T00:00:00+00:00",
    }
    subject = {"run_id": "old-run"}
    envelope = {
        "issuer": "receipt-service-old",
        "key_id": "receipt-key-retired",
        "issued_at": "2026-05-01T00:00:00+00:00",
        "expires_at": "2026-05-02T00:00:00+00:00",
        "nonce": "old-receipt",
        "subject_digest": subject_digest(subject),
    }
    envelope["signature"] = base64.b64encode(retired_private.sign(canonical_bytes(envelope))).decode()
    result = verify_attestation(subject, envelope, store, "receipt", allow_expired=True)
    assert result["key_id"] == "receipt-key-retired"
