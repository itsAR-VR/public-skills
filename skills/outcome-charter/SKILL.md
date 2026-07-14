---
name: outcome-charter
description: >
  Compile, match, validate, and record reusable outcome charters for
  multi-system, repeated, event-driven, or side-effecting workflows. Use when
  a normal-language request connects authenticated apps such as Drive, CRM,
  Slack, Gmail, Linear, or Calendar and the agent must discover tools, infer
  hidden dependencies, validate schemas, create a cross-app automation, reuse
  a previously verified workflow safely, minimize orchestration context, or
  select a durable runner. Common triggers include "create Linear follow-up
  tasks", "connect multiple apps", "reuse a successful workflow", and "when CI
  fails".
related_skills: [skill-oracle, loop-engineering, verify, ponytail, state-machine]
---

# Outcome Charter

A charter is a validated execution contract between natural-language intent
and deterministic execution. Skill Oracle routes here; this skill owns
compatibility, compilation, approval boundaries, execution receipts, and
promotion of proven charters.

## Architecture

```text
outcome request
  -> authenticated capability discovery
  -> tool/schema validation
  -> compatible-charter match or new compilation
  -> current approval gate when required
  -> direct/checkpointed/durable execution
  -> destination readback
  -> sanitized receipt and aggregate success proof
```

Reuse the recipe, never the old ingredients. A reused charter receives fresh
inputs and current auth. Never replay credentials, OAuth material, source
payloads, old business-object IDs, idempotency keys, or prior approvals.

## 1. Define The Outcome Contract

Resolve these fields from normal language and available context:

- outcome and deliverable
- observable success criteria
- scope and constraints
- side effects and approval boundary
- required inputs and outputs
- concise return shape

Do not force the operator to name internal IDs or implementation steps. Infer
hidden dependencies such as `file name -> file ID -> download` by working
backward from the desired output.

## 2. Discover And Validate Capabilities

Use only tools available to the authenticated operator. Shortlist relevant
operations before loading schemas. Record:

- account/workspace/tenant identity, never credentials
- operation names and read/write scope
- input/output schema digests
- pagination, rate, and size limits
- reversibility and approval classification

The output of every step must satisfy the declared input of its dependents.
Use deterministic calculations for IDs, filters, joins, sorting, and field
selection. Use an LLM only for work requiring judgment or synthesis.

## 3. Match A Proven Charter

Build a query matching `references/charter-schema.json`, then run:

```bash
python3 skills/outcome-charter/scripts/charter_registry.py match \
  --registry /path/to/charters.json \
  --query /path/to/query.json
```

Compatibility is exact across:

- outcome class and charter version
- connector-issued principal/tenant identifiers and scopes
- tool operation names and schema digests
- approval-policy version
- the derived current-approval requirement
- required input and output field names
- runner contract version

The query also carries a fresh auth-validation timestamp. Stale connector proof
cannot authorize reuse.

Semantic similarity may nominate a charter family, but only the deterministic
compatibility fingerprint can authorize reuse.

Interpret the result:

- `compile`: no exact compatible charter or safety proof is insufficient
- `suggest`: one or two verified runs; show the charter as a candidate
- `reuse`: reserved for a runner with trusted signed capability, approval, and
  destination-readback attestations

Automatic reuse requires an external trusted issuer to sign the current
capability snapshot and at least three current-definition destination receipts
that meet the configured minimum item count and 95% success threshold. The
runner verifies Ed25519 signatures using the public-key contract in
`references/trust-store-schema.json`. Private signing keys must remain
unavailable to the planning/execution agent.

Use separate active keys for capability, approval, and receipt issuance.
Retain retired receipt-verification keys with activation and retirement times
so historical success and quarantine evidence survives routine key rotation.
Revoked keys remain listed for audit, but only receipts issued before the
recorded revocation time can remain historical evidence.

Promotion proof is derived from sanitized receipts, never editable counters.
Every verified receipt is bound to the current executable-definition digest,
compatibility fingerprint, allowed verifier identity, and destination-evidence
digest. Any operation, dependency, prompt, retry, or side-effect change creates
a new definition digest and resets promotion proof automatically.

## 4. Compile When Reuse Is Unsafe

Compile a typed step graph containing stable step IDs, dependencies, operation
and connection references, typed inputs, minimal stored outputs, retries,
timeouts, failure behavior, side-effect classification, idempotency, and
verification evidence.

Every loop declares its item collection, concurrency cap, item result schema,
partial-failure policy, and final aggregation. Each write step must be
independently retryable.

Choose the lightest runner that fits:

1. direct tools for short one-off work
2. checkpointed scripts for repeated work needing state and retries
3. Temporal or another durable engine only for long-running, event-triggered,
   high-volume, or crash-resumable workflows

## 5. Gate Side Effects

Historical approval never carries forward. A compatible charter may be the
default plan, but current approval is still required for writes, sends,
publishing, production changes, spending, signing, broad deletion, or
customer-facing commitments. Unknown side-effect classifications are rejected.

Before approval, show the systems/accounts used, expected changes, side-effect
count, rollback path, and returned result.

The runner must call the authorization gate immediately before execution:

```bash
python3 skills/outcome-charter/scripts/charter_registry.py authorize \
  --definition /path/to/charter.json \
  --query /path/to/current-query.json \
  --approval /path/to/current-scoped-approval.json
```

The approval must come from a trusted external approval service and bind the
issuer, operator, exact preview digest, action count, one-time nonce, charter
ID, executable-definition digest, compatibility fingerprint, execution-scope
digest, action, issue time, and expiration. The runner atomically records the
signed one-time nonce before returning authorization, preventing replay.
The runner service owns the canonical trust root at
`/etc/outcome-charter/trust-store.json` and nonce ledger at
`/var/lib/outcome-charter/consumed-approval-nonces.log`; neither path is
selectable by the charter or calling agent. A production runner must protect
both with a separate OS/service identity so the planning agent cannot replace
the trust root or erase the ledger.

## 6. Execute Idempotently

Generate one idempotency key per write:

```bash
python3 skills/outcome-charter/scripts/charter_registry.py idempotency-key \
  --charter-id investor-research-v1 \
  --step-id create-linear-issue \
  --business-object C2-Ventures \
  --input-version sha256:abc123
```

Persist compact typed state outside model context. Retry transient failures
with bounded backoff; do not retry permission, schema, or validation failures
blindly. Redact external payloads and secrets from logs.

## 7. Verify And Record

Completion means the outcome exists in the destination. Read back created or
updated records, confirm identities/counts, and surface partial failures.

Record only a sanitized receipt:

```bash
python3 skills/outcome-charter/scripts/charter_registry.py record \
  --registry /path/to/charters.json \
  --receipt /path/to/sanitized-receipt.json \
  --receipt-log /path/to/receipts.jsonl
```

The recorder rejects unknown fields so raw prompts, API payloads, message
bodies, credentials, and approvals cannot enter the registry accidentally.
Production promotion requires receipts signed by a trusted destination-readback
verifier or retrieved from a verifier-owned append-only store. The local MVP
can record unsigned sanitized evidence for evaluation, but unsigned evidence
never contributes to automatic reuse.

## 8. Compile The Durable Runner Plan

Compile a validated charter into a deterministic Temporal or checkpointed
runner plan outside model context:

```bash
python3 skills/outcome-charter/scripts/durable_plan.py \
  --definition /path/to/charter.json \
  --execution-scope-digest sha256:... \
  --output /path/to/durable-plan.json
```

The plan produces a stable workflow ID, dependency-ordered activities, bounded
retries, non-retryable permission/schema/approval failures, per-write
idempotency and approval gates, destination readback, concurrency limits, and a
signed-receipt completion contract. Temporal owns waiting, retrying, crash
recovery, and durable state. It must not reinterpret the charter with an LLM.

Start the actual worker and submit plans using `scripts/temporal_worker.py` and
`scripts/temporal_submit.py`. The worker loads only the service-owned adapter
defined in `references/adapter-contract.md`; deployment identities and commands
are in `references/deployment.md`.

## Token Discipline

- query the registry outside model context
- return only the top compatible charter ID, mode, proof summary, and reason
- load schemas only for shortlisted operations
- pass field-level outputs between steps
- summarize large sources once and persist the summary
- isolate independent item research contexts
- never send secrets or unrelated prior-step payloads to an LLM

Token savings come from architecture, not weaker reasoning.

## Skill Oracle Contract

Skill Oracle remains the router. It should choose exactly one route:

1. direct skill stack
2. compatible verified charter in suggest/reuse mode
3. compile a new charter

Do not load the registry into the Oracle prompt. Run the deterministic matcher
and pass its compact result to this skill.

## Validation

```bash
python3 -m pytest skills/outcome-charter/tests -q
python3 skills/outcome-charter/scripts/verify_temporal_e2e.py
python3 scripts/validate-skill-frontmatter.py --skills-dir skills --json
python3 scripts/scan-skills-security.py --skills-dir skills --json
python3 scripts/query-skill-graph.py \
  "research prospects from my Drive brief and create follow-up tasks in Linear" \
  --top 8 --precision
```
