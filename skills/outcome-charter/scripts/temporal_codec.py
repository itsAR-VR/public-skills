#!/usr/bin/env python3
"""Mandatory AES-GCM Temporal payload codec with retained decryption keys."""

from __future__ import annotations

import base64
import json
import os
from dataclasses import replace
from pathlib import Path
from typing import Sequence

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from temporalio.api.common.v1 import Payload
from temporalio.converter import DataConverter, PayloadCodec


DEFAULT_KEYRING = Path("/etc/outcome-charter/temporal-codec-keyring.json")
ENCODING = b"binary/aes-gcm"


def load_keyring(path: Path) -> tuple[str, dict[str, bytes]]:
    if path.is_symlink() or not path.is_file():
        raise RuntimeError("Temporal codec keyring must be a regular non-symlink file")
    if path.stat().st_mode & 0o077:
        raise RuntimeError("Temporal codec keyring must not grant group/world permissions")
    value = json.loads(path.read_text(encoding="utf-8"))
    active = value.get("active_key_id")
    records = value.get("keys")
    if not isinstance(active, str) or not isinstance(records, dict) or active not in records:
        raise RuntimeError("Temporal codec keyring requires an active key present in keys")
    keys: dict[str, bytes] = {}
    for key_id, encoded in records.items():
        if not isinstance(key_id, str) or not isinstance(encoded, str):
            raise RuntimeError("Temporal codec keyring entries must be strings")
        try:
            raw = base64.b64decode(encoded, validate=True)
        except ValueError as exc:
            raise RuntimeError(f"Temporal codec key {key_id} is not valid base64") from exc
        if len(raw) != 32:
            raise RuntimeError(f"Temporal codec key {key_id} must be 32 bytes")
        keys[key_id] = raw
    return active, keys


class AesGcmPayloadCodec(PayloadCodec):
    def __init__(self, active_key_id: str, keys: dict[str, bytes]) -> None:
        self.active_key_id = active_key_id
        self.keys = keys

    async def encode(self, payloads: Sequence[Payload]) -> list[Payload]:
        key = AESGCM(self.keys[self.active_key_id])
        key_id = self.active_key_id.encode("utf-8")
        encoded = []
        for payload in payloads:
            nonce = os.urandom(12)
            ciphertext = key.encrypt(nonce, payload.SerializeToString(), ENCODING + key_id)
            encoded.append(Payload(metadata={"encoding": ENCODING, "key-id": key_id}, data=nonce + ciphertext))
        return encoded

    async def decode(self, payloads: Sequence[Payload]) -> list[Payload]:
        decoded = []
        for payload in payloads:
            if payload.metadata.get("encoding") != ENCODING:
                raise RuntimeError("unencrypted Temporal payload rejected")
            key_id_bytes = payload.metadata.get("key-id")
            if not key_id_bytes:
                raise RuntimeError("encrypted Temporal payload missing key ID")
            key_id = key_id_bytes.decode("utf-8")
            raw_key = self.keys.get(key_id)
            if raw_key is None:
                raise RuntimeError(f"Temporal payload key {key_id} is unavailable")
            plaintext = AESGCM(raw_key).decrypt(payload.data[:12], payload.data[12:], ENCODING + key_id_bytes)
            restored = Payload()
            restored.ParseFromString(plaintext)
            decoded.append(restored)
        return decoded


def data_converter(keyring_path: Path = DEFAULT_KEYRING) -> DataConverter:
    active, keys = load_keyring(keyring_path)
    return replace(DataConverter.default, payload_codec=AesGcmPayloadCodec(active, keys))
