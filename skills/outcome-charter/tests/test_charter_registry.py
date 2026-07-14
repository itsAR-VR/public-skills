from __future__ import annotations

import copy
import base64
import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
SCRIPT = SCRIPTS / "charter_registry.py"
sys.path.insert(0, str(SCRIPTS))

from charter_registry import (  # noqa: E402
    CharterError,
    authorize_execution,
    authorize_and_consume,
    compatibility_fingerprint,
    definition_digest,
    idempotency_key,
    match_charter,
    proof_stats,
    receipt_log_contains,
    record_run,
    sha256_label,
    validate_definition,
)
from attestations import canonical_bytes, subject_digest  # noqa: E402


ISSUERS = {"capability": "capability-registry", "approval": "approval-service", "receipt": "destination-readback-v1"}
PRIVATE_KEYS = {usage: Ed25519PrivateKey.generate() for usage in ISSUERS}
TRUST_STORE = {
    "trust_store_version": "1.0",
    "keys": {
        f"{usage}-key-1": {
            "issuer": ISSUERS[usage],
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
        for usage, private in PRIVATE_KEYS.items()
    },
}


AUTH = [
    {"provider": "drive", "principal_id": "user:mo", "tenant_id": "workspace:PROJECT", "scopes": ["files.read"]},
    {"provider": "linear", "principal_id": "user:mo", "tenant_id": "workspace:PROJECT", "scopes": ["issues.write"]},
]
SCHEMAS = {
    "drive.find": {
        "schema_digest": "sha256:" + "1" * 64,
        "provider": "drive",
        "required_scopes": ["files.read"],
        "side_effect": "read",
    },
    "linear.create": {
        "schema_digest": "sha256:" + "2" * 64,
        "provider": "linear",
        "required_scopes": ["issues.write"],
        "side_effect": "write",
    },
}
BASE = {
    "charter_id": "investor-research-v1",
    "outcome_class": "investor_research_to_linear",
    "charter_version": "1.0",
    "auth_context": AUTH,
    "tool_schemas": SCHEMAS,
    "approval_policy_version": "2026-07",
    "requires_current_approval": True,
    "required_inputs": ["brief_name", "count", "tier"],
    "required_outputs": ["linear_task_link", "name"],
    "runner_contract_version": "1.0",
    "allowed_verifiers": ["destination-readback-v1"],
    "minimum_promotion_items": 10,
    "runner": {
        "mode": "temporal",
        "workflow_type": "OutcomeCharterWorkflow",
        "task_queue": "outcome-charters",
        "max_concurrency": 5,
        "overall_timeout_seconds": 3600,
    },
    "steps": [
        {
            "step_id": "find-brief",
            "operation": "drive.find",
            "depends_on": [],
            "input_fields": ["brief_name"],
            "side_effect": "read",
            "auth": {"provider": "drive", "principal_id": "user:mo", "tenant_id": "workspace:PROJECT", "required_scopes": ["files.read"]},
        },
        {
            "step_id": "create-linear",
            "operation": "linear.create",
            "depends_on": ["find-brief"],
            "input_fields": [],
            "side_effect": "write",
            "idempotency_required": True,
            "auth": {"provider": "linear", "principal_id": "user:mo", "tenant_id": "workspace:PROJECT", "required_scopes": ["issues.write"]},
        },
    ],
    "receipts": [],
}


def now_iso(offset: timedelta = timedelta()) -> str:
    return (datetime.now(timezone.utc) + offset).isoformat()


def attest(value: dict, nonce: str) -> dict:
    usage = "receipt" if "run_id" in value else "approval" if "approval_id" in value else "capability"
    subject = {field: value[field] for field in sorted(value) if field != "attestation"}
    envelope = {
        "issuer": ISSUERS[usage],
        "key_id": f"{usage}-key-1",
        "issued_at": now_iso(timedelta(seconds=-1)),
        "expires_at": now_iso(timedelta(minutes=5)),
        "nonce": nonce,
        "subject_digest": subject_digest(subject),
    }
    envelope["signature"] = base64.b64encode(PRIVATE_KEYS[usage].sign(canonical_bytes(envelope))).decode()
    value["attestation"] = envelope
    return value


def query(**patch) -> dict:
    value = {field: copy.deepcopy(BASE[field]) for field in (
        "outcome_class",
        "charter_version",
        "auth_context",
        "tool_schemas",
        "approval_policy_version",
        "requires_current_approval",
        "required_inputs",
        "required_outputs",
        "runner_contract_version",
    )}
    value.update(
        auth_validated_at=now_iso(),
        auth_max_age_seconds=900,
        operator_id="user:mo",
        approval_scope_digest="sha256:" + "5" * 64,
        preview_digest="sha256:" + "6" * 64,
        action_count=5,
    )
    value.update(patch)
    return value


def registry_with(definition: dict = BASE) -> dict:
    return {"registry_version": "1.0", "charters": [copy.deepcopy(definition)]}


def receipt(definition: dict = BASE, **patch) -> dict:
    value = {
        "run_id": "run-1",
        "charter_id": definition["charter_id"],
        "definition_digest": definition_digest(definition),
        "compatibility_fingerprint": compatibility_fingerprint(definition),
        "verifier_id": "destination-readback-v1",
        "evidence_digest": "sha256:" + "a" * 64,
        "completed_at": now_iso(timedelta(seconds=-2)),
        "verified": True,
        "destination_readback": True,
        "attempted_items": 5,
        "successful_items": 5,
        "policy_violation": False,
    }
    value.update(patch)
    return value


def definition_with_receipts(count: int, attempted: int = 5, successful: int = 5) -> dict:
    definition = copy.deepcopy(BASE)
    for index in range(count):
        definition["receipts"].append(
            receipt(definition, run_id=f"run-{index}", attempted_items=attempted, successful_items=successful)
        )
    return definition


def approval(definition: dict = BASE, **patch) -> dict:
    value = {
        "approval_id": "approval-1",
        "operator_id": "user:mo",
        "charter_id": definition["charter_id"],
        "definition_digest": definition_digest(definition),
        "compatibility_fingerprint": compatibility_fingerprint(definition),
        "scope_digest": "sha256:" + "5" * 64,
        "preview_digest": "sha256:" + "6" * 64,
        "action_count": 5,
        "approved_action": "execute",
        "approved_at": now_iso(timedelta(minutes=-1)),
        "expires_at": now_iso(timedelta(minutes=10)),
    }
    value.update(patch)
    return value


def test_no_match_compiles() -> None:
    assert match_charter({"registry_version": "1.0", "charters": []}, query())["mode"] == "compile"


def test_one_verified_receipt_only_suggests() -> None:
    assert match_charter(registry_with(definition_with_receipts(1)), query())["mode"] == "suggest"


def test_three_verified_receipts_remain_suggest_only_without_trusted_attestations() -> None:
    result = match_charter(registry_with(definition_with_receipts(3, attempted=20, successful=19)), query())
    assert result["mode"] == "suggest"
    assert result["reason"] == "exact_compatibility_but_trusted_attestation_adapter_required"
    assert result["approval_required"] is True
    assert result["approval_carried_forward"] is False


def test_signed_capability_and_receipts_promote_to_reuse() -> None:
    definition = copy.deepcopy(BASE)
    for index in range(3):
        definition["receipts"].append(attest(receipt(definition, run_id=f"trusted-{index}"), f"receipt-{index}"))
    current_query = attest(query(), "capability-1")
    result = match_charter(registry_with(definition), current_query, TRUST_STORE)
    assert result["mode"] == "reuse"
    assert result["proof"]["trusted_verified_runs"] == 3


def test_trusted_policy_violation_quarantines_the_charter_family() -> None:
    definition = copy.deepcopy(BASE)
    definition["receipts"].append(
        attest(
            receipt(
                definition,
                run_id="policy-failure",
                verified=False,
                destination_readback=False,
                policy_violation=True,
                successful_items=0,
            ),
            "receipt-policy-failure",
        )
    )
    result = match_charter(registry_with(definition), attest(query(), "capability-quarantine"), TRUST_STORE)
    assert result["mode"] == "compile"
    assert result["reason"] == "charter_family_quarantined_after_policy_violation"


def test_preloaded_receipt_issuer_must_match_declared_verifier() -> None:
    definition = copy.deepcopy(BASE)
    definition["allowed_verifiers"] = ["claimed-verifier"]
    forged_identity = attest(receipt(definition, verifier_id="claimed-verifier"), "receipt-wrong-issuer")
    definition["receipts"].append(forged_identity)
    stats = proof_stats(definition, TRUST_STORE)
    assert stats["verified_runs"] == 1
    assert stats["trusted_verified_runs"] == 0


@pytest.mark.parametrize(
    ("field", "replacement"),
    [
        ("auth_context", [{"provider": "drive", "principal_id": "other", "tenant_id": "workspace:PROJECT", "scopes": ["files.read"]}]),
        ("tool_schemas", {"drive.find": {"schema_digest": "sha256:" + "9" * 64, "provider": "drive", "required_scopes": ["files.read"], "side_effect": "read"}}),
        ("approval_policy_version", "2026-08"),
        ("requires_current_approval", False),
        ("required_outputs", ["name"]),
    ],
)
def test_compatibility_changes_reject_reuse(field: str, replacement) -> None:
    definition = definition_with_receipts(3)
    result = match_charter(registry_with(definition), query(**{field: replacement}))
    assert result["mode"] == "compile"
    assert field in result["near_matches"][0]["mismatched_fields"]


def test_auth_proof_must_be_fresh() -> None:
    with pytest.raises(CharterError, match="not fresh"):
        match_charter(registry_with(), query(auth_validated_at=now_iso(timedelta(hours=-2))))


def test_fingerprint_is_order_independent_for_sets_and_maps() -> None:
    reordered = query()
    reordered["auth_context"].reverse()
    reordered["required_inputs"].reverse()
    reordered["tool_schemas"] = dict(reversed(list(reordered["tool_schemas"].items())))
    assert compatibility_fingerprint(query()) == compatibility_fingerprint(reordered)


def test_write_send_publish_delete_spend_sign_and_deploy_require_approval_and_idempotency() -> None:
    for side_effect in ("write", "send", "publish", "delete", "spend", "sign", "deploy"):
        definition = copy.deepcopy(BASE)
        definition["steps"][1]["side_effect"] = side_effect
        definition["tool_schemas"]["linear.create"]["side_effect"] = side_effect
        definition["requires_current_approval"] = False
        with pytest.raises(CharterError, match="requires_current_approval"):
            validate_definition(definition)
        definition["requires_current_approval"] = True
        definition["steps"][1]["idempotency_required"] = False
        with pytest.raises(CharterError, match="must require idempotency"):
            validate_definition(definition)


def test_unknown_side_effect_is_rejected() -> None:
    definition = copy.deepcopy(BASE)
    definition["steps"][1]["side_effect"] = "email-the-customer"
    with pytest.raises(CharterError, match="unknown side_effect"):
        validate_definition(definition)


def test_changed_step_graph_resets_proof() -> None:
    definition = definition_with_receipts(3)
    assert proof_stats(definition)["verified_runs"] == 3
    definition["steps"][1]["operation"] = "linear.create_v2"
    definition["tool_schemas"]["linear.create_v2"] = definition["tool_schemas"].pop("linear.create")
    assert proof_stats(definition)["verified_runs"] == 0
    assert match_charter(registry_with(definition), query())["mode"] == "compile"


def test_external_step_operation_requires_a_schema_digest() -> None:
    definition = copy.deepcopy(BASE)
    definition["steps"][1]["operation"] = "linear.unvalidated_create"
    with pytest.raises(CharterError, match="missing schema digests"):
        validate_definition(definition)


def test_external_step_requires_matching_connector_identity_and_scope() -> None:
    wrong_principal = copy.deepcopy(BASE)
    wrong_principal["steps"][1]["auth"]["principal_id"] = "user:attacker"
    with pytest.raises(CharterError, match="not in the charter auth context"):
        validate_definition(wrong_principal)
    missing_scope = copy.deepcopy(BASE)
    missing_scope["steps"][1]["auth"]["required_scopes"] = ["issues.admin"]
    with pytest.raises(CharterError, match="lacks required scopes"):
        validate_definition(missing_scope)
    wrong_provider = copy.deepcopy(BASE)
    wrong_provider["steps"][1]["auth"] = copy.deepcopy(wrong_provider["steps"][0]["auth"])
    with pytest.raises(CharterError, match="provider does not match"):
        validate_definition(wrong_provider)


def test_unverified_receipts_do_not_affect_promotion_rate() -> None:
    definition = definition_with_receipts(3)
    definition["receipts"].append(receipt(definition, run_id="failed", verified=False, destination_readback=False, attempted_items=100, successful_items=0))
    stats = proof_stats(definition)
    assert stats["verified_attempted_items"] == 15
    assert stats["success_rate"] == 1.0


@pytest.mark.parametrize("bad", [True, 1.5, "5", -1, 1_000_000_001])
def test_invalid_numeric_counts_are_rejected(bad) -> None:
    with pytest.raises(CharterError, match="attempted_items"):
        record_run(registry_with(), receipt(attempted_items=bad, successful_items=0))


def test_verified_receipt_requires_destination_readback_and_evidence() -> None:
    with pytest.raises(CharterError, match="destination_readback"):
        record_run(registry_with(), receipt(destination_readback=False))
    with pytest.raises(CharterError, match="evidence_digest"):
        record_run(registry_with(), receipt(evidence_digest="not-proof"))


def test_receipt_rejects_private_payload_fields() -> None:
    with pytest.raises(CharterError, match="forbidden fields"):
        record_run(registry_with(), receipt(raw_api_payload={"token": "never"}))


def test_receipt_must_match_current_definition_and_allowed_verifier() -> None:
    with pytest.raises(CharterError, match="definition_digest"):
        record_run(registry_with(), receipt(definition_digest="sha256:" + "f" * 64))
    with pytest.raises(CharterError, match="verifier_id"):
        record_run(registry_with(), receipt(verifier_id="self-asserted"))


def test_duplicate_receipt_is_idempotent_but_same_run_id_across_charters_is_distinct() -> None:
    # Idempotency requires byte-equivalent content: two receipt() calls carry
    # fresh timestamps and would (correctly) be rejected as conflicting.
    original = receipt()
    registry, first = record_run(registry_with(), copy.deepcopy(original))
    registry, second = record_run(registry, copy.deepcopy(original))
    assert first["recorded"] is True
    assert second["recorded"] is False
    other = copy.deepcopy(BASE)
    other["charter_id"] = "other-charter"
    registry["charters"].append(other)
    registry, third = record_run(registry, receipt(other))
    assert third["recorded"] is True


def test_receipt_log_identity_includes_charter_and_definition(tmp_path: Path) -> None:
    log = tmp_path / "receipts.jsonl"
    current = receipt()
    log.write_text(json.dumps(current) + "\n", encoding="utf-8")
    assert receipt_log_contains(log, (current["charter_id"], current["definition_digest"], current["run_id"]))
    assert not receipt_log_contains(log, ("other", current["definition_digest"], current["run_id"]))


def test_execution_boundary_requires_current_scoped_approval() -> None:
    with pytest.raises(CharterError, match="capability"):
        authorize_execution(BASE, query(), None)
    signed_query = attest(query(), "capability-execute")
    with pytest.raises(CharterError, match="current scoped approval"):
        authorize_execution(BASE, signed_query, None, TRUST_STORE)
    signed_approval = attest(approval(), "approval-execute")
    result = authorize_execution(BASE, signed_query, signed_approval, TRUST_STORE, set())
    assert result["authorized"] is True
    nonce_key = sha256_label("approval-execute")
    assert result["approval_nonce_key"] == nonce_key
    with pytest.raises(CharterError, match="already been consumed"):
        authorize_execution(BASE, signed_query, signed_approval, TRUST_STORE, {nonce_key})


def test_read_only_charter_authorizes_without_approval() -> None:
    definition = copy.deepcopy(BASE)
    definition["steps"] = [definition["steps"][0]]
    definition["requires_current_approval"] = False
    readonly_query = attest(query(requires_current_approval=False), "capability-readonly")
    assert authorize_execution(definition, readonly_query, None, TRUST_STORE) == {
        "authorized": True,
        "approval_required": False,
        "approval_id": None,
    }


def test_idempotency_key_is_stable_and_input_sensitive() -> None:
    first = idempotency_key("c1", "s1", "object-1", "v1")
    assert first == idempotency_key("c1", "s1", "object-1", "v1")
    assert first != idempotency_key("c1", "s1", "object-1", "v2")


def test_cli_failure_is_compact_json(tmp_path: Path) -> None:
    registry_path = tmp_path / "registry.json"
    query_path = tmp_path / "query.json"
    registry_path.write_text(json.dumps(registry_with()), encoding="utf-8")
    bad_query = query()
    bad_query["auth_max_age_seconds"] = "900"
    query_path.write_text(json.dumps(bad_query), encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "match", "--registry", str(registry_path), "--query", str(query_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "Traceback" not in result.stdout + result.stderr
    assert json.loads(result.stdout)["error"]


def test_runner_owned_nonce_store_consumes_signed_approval_once(tmp_path: Path) -> None:
    use_log = tmp_path / "approval-use.log"
    signed_query = attest(query(), "capability-cli")
    signed_approval = attest(approval(), "approval-cli")
    first = authorize_and_consume(BASE, signed_query, signed_approval, TRUST_STORE, use_log)
    assert first["authorized"] is True
    with pytest.raises(CharterError, match="already been consumed"):
        authorize_and_consume(BASE, signed_query, signed_approval, TRUST_STORE, use_log)
    assert use_log.read_text(encoding="utf-8").splitlines() == [sha256_label("approval-cli")]


def test_concurrent_cli_writers_preserve_both_receipts(tmp_path: Path) -> None:
    registry_path = tmp_path / "registry.json"
    receipt_log = tmp_path / "receipts.jsonl"
    registry_path.write_text(json.dumps(registry_with()), encoding="utf-8")
    receipt_paths = []
    for run_id in ("concurrent-1", "concurrent-2"):
        path = tmp_path / f"{run_id}.json"
        path.write_text(json.dumps(receipt(run_id=run_id)), encoding="utf-8")
        receipt_paths.append(path)

    processes = [
        subprocess.Popen(
            [
                sys.executable,
                str(SCRIPT),
                "record",
                "--registry",
                str(registry_path),
                "--receipt",
                str(path),
                "--receipt-log",
                str(receipt_log),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        for path in receipt_paths
    ]
    results = [process.communicate(timeout=10) + (process.returncode,) for process in processes]

    assert all(returncode == 0 for _, _, returncode in results), results
    saved = json.loads(registry_path.read_text(encoding="utf-8"))
    assert {item["run_id"] for item in saved["charters"][0]["receipts"]} == {
        "concurrent-1",
        "concurrent-2",
    }
    logged = [json.loads(line) for line in receipt_log.read_text(encoding="utf-8").splitlines()]
    assert {item["run_id"] for item in logged} == {"concurrent-1", "concurrent-2"}


def test_definition_digest_covers_executable_graph() -> None:
    changed = copy.deepcopy(BASE)
    changed["steps"][1]["depends_on"] = []
    assert definition_digest(BASE) != definition_digest(changed)
    assert sha256_label(BASE).startswith("sha256:")


def test_none_declaration_on_contracted_write_operation_is_rejected() -> None:
    definition = copy.deepcopy(BASE)
    step = definition["steps"][1]
    assert step["operation"] == "linear.create"
    step["side_effect"] = "none"
    definition["requires_current_approval"] = False
    with pytest.raises(CharterError, match="side_effect does not match its operation contract"):
        validate_definition(definition)


def test_conflicting_receipt_content_for_same_run_identity_is_rejected() -> None:
    registry = registry_with(definition_with_receipts(1))
    conflicting = receipt(run_id="run-0", verified=False, successful_items=0, policy_violation=True)
    with pytest.raises(CharterError, match="conflicting receipt content"):
        record_run(registry, conflicting)


def test_byte_equivalent_receipt_stays_idempotent() -> None:
    definition = definition_with_receipts(1)
    registry = registry_with(definition)
    duplicate = copy.deepcopy(definition["receipts"][0])
    _, outcome = record_run(registry, duplicate)
    assert outcome == {"recorded": False, "reason": "duplicate_receipt_identity", "run_id": "run-0"}


def test_suggestable_charter_outranks_compile_only_candidate() -> None:
    suggestable = definition_with_receipts(1)
    compile_only = copy.deepcopy(BASE)
    compile_only["charter_id"] = "z-lexicographically-later-v1"
    for item in compile_only["receipts"]:
        item["charter_id"] = compile_only["charter_id"]
    registry = {"registry_version": "1.0", "charters": [copy.deepcopy(suggestable), compile_only]}
    result = match_charter(registry, query())
    assert result["mode"] == "suggest"
    assert result["charter_id"] == suggestable["charter_id"]


def test_disabled_charter_cannot_authorize_execution() -> None:
    definition = copy.deepcopy(BASE)
    definition["disabled"] = True
    with pytest.raises(CharterError, match="disabled"):
        authorize_execution(definition, attest(query(), "cap-disabled"), None, TRUST_STORE)


def test_quarantined_charter_cannot_authorize_execution() -> None:
    definition = copy.deepcopy(BASE)
    definition["receipts"].append(receipt(definition, run_id="run-bad", verified=False, successful_items=0, policy_violation=True))
    with pytest.raises(CharterError, match="quarantine"):
        authorize_execution(definition, attest(query(), "cap-quarantined"), None, TRUST_STORE)


def test_signed_failures_dilute_promotion_success_rate() -> None:
    definition = copy.deepcopy(BASE)
    for index in range(3):
        definition["receipts"].append(
            attest(receipt(definition, run_id=f"run-ok-{index}", attempted_items=5, successful_items=5), f"ok-{index}")
        )
    for index in range(3):
        definition["receipts"].append(
            attest(
                receipt(definition, run_id=f"run-fail-{index}", verified=False, attempted_items=5, successful_items=0),
                f"fail-{index}",
            )
        )
    stats = proof_stats(definition, TRUST_STORE)
    assert stats["trusted_verified_runs"] == 3
    assert stats["trusted_attempted_items"] == 30
    assert stats["trusted_successful_items"] == 15
    result = match_charter(registry_with(definition), attest(query(), "cap-diluted"), TRUST_STORE)
    assert result["mode"] != "reuse"


def test_receipt_attestation_envelope_schema_enforced_without_trust_store() -> None:
    smuggled = receipt()
    smuggled["attestation"] = {"issuer": "x", "raw_api_payload": {"token": "never"}}
    with pytest.raises(CharterError, match="attestation"):
        record_run(registry_with(), smuggled)
