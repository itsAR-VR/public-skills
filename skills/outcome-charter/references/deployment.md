# Durable runner deployment

## Required identities

- **Planning agent:** discovers tools and compiles charters; no runner state or
  signing-key access.
- **Runner service:** reads `/etc/outcome-charter/trust-store.json`, consumes
  `/var/lib/outcome-charter/consumed-approval-nonces.log`, and talks to Temporal.
- **Capability issuer:** signs current authenticated capability snapshots.
- **Approval issuer:** signs exact operator-approved execution previews.
- **Destination verifier:** reads destinations and signs sanitized receipts.

Use separate Ed25519 key material for the three issuer roles.

## Worker startup

Install `scripts/requirements.txt` in the runner service environment, install a
runner-owned adapter module, then start:

```bash
OUTCOME_CHARTER_ADAPTER_MODULE=trusted_gateway_adapter \
OUTCOME_CHARTER_CODEC_MODULE=temporal_codec \
python3 scripts/temporal_worker.py \
  --address temporal.internal:7233 \
  --namespace production \
  --task-queue outcome-charters
```

## Workflow submission

Compile the durable plan, write fresh typed inputs, then submit:

```bash
python3 scripts/temporal_submit.py \
  --submission /runner-state/submissions/run-123.json \
  --address temporal.internal:7233 \
  --namespace production \
  --wait
```

Event sources such as Slack, CI/CD, schedules, and webhooks should submit the
same content-addressed plan and fresh opaque input/capability/approval
references with a new execution-scope digest. They do not execute tools
directly. Temporal payload encryption is mandatory via
`/etc/outcome-charter/temporal-codec-keyring.json`; retain old decryption keys
while any workflow history still uses them.
