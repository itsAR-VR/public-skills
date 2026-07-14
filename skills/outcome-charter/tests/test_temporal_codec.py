from __future__ import annotations

import asyncio
import base64
import json
import os
import sys
from pathlib import Path

import pytest


pytest.importorskip("temporalio")
SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from temporalio.api.common.v1 import Payload  # noqa: E402
from temporal_codec import AesGcmPayloadCodec, load_keyring  # noqa: E402


def keyring(tmp_path: Path) -> Path:
    path = tmp_path / "codec.json"
    path.write_text(
        json.dumps({"active_key_id": "k1", "keys": {"k1": base64.b64encode(os.urandom(32)).decode()}}),
        encoding="utf-8",
    )
    path.chmod(0o600)
    return path


def test_codec_encrypts_and_round_trips_payload(tmp_path: Path) -> None:
    active, keys = load_keyring(keyring(tmp_path))
    codec = AesGcmPayloadCodec(active, keys)
    original = Payload(metadata={"encoding": b"json/plain"}, data=b'sensitive-value')
    encrypted = asyncio.run(codec.encode([original]))
    assert b"sensitive-value" not in encrypted[0].data
    restored = asyncio.run(codec.decode(encrypted))
    assert restored[0] == original


def test_codec_rejects_unencrypted_payload(tmp_path: Path) -> None:
    active, keys = load_keyring(keyring(tmp_path))
    codec = AesGcmPayloadCodec(active, keys)
    with pytest.raises(RuntimeError, match="unencrypted"):
        asyncio.run(codec.decode([Payload(metadata={"encoding": b"json/plain"}, data=b"plain")]))
