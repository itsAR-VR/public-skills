# Runner-owned capability adapter contract

The Temporal worker loads exactly one module named by the service-owned
`OUTCOME_CHARTER_ADAPTER_MODULE` environment variable. The planning agent and
charter cannot override this setting.

The module exposes three asynchronous functions:

```python
async def preflight(payload: dict) -> dict: ...
async def authorize(payload: dict) -> dict: ...
async def execute_step(payload: dict) -> dict: ...
async def emit_receipt(payload: dict) -> dict: ...
```

## `preflight`

Before any activity, verify the signed capability snapshot against the
runner-owned trust root, confirm live connector principals/tenants/scopes, and
confirm every operation schema digest still matches. Return only compact
typed metadata. Never return credentials or raw connector payloads.

The preflight response must be signed by the capability issuer and echo the
content-addressed plan, input, and capability references. Reconstruct the plan
from the signed definition/capability record; never trust gate booleans or
operation metadata supplied by the planner.

## `authorize`

Atomically claim the approval once into a durable grant bound to workflow ID,
definition digest, execution scope, preview digest, and the exact action
manifest. Repeating the identical claim returns the same grant. A different
workflow or manifest cannot reuse it. Derive activity-bound action tokens from
that grant so multiple approved writes and Temporal retries are idempotent.

## `execute_step`

Resolve the operation only from the runner-owned capability registry. Reject
unknown operations even if a charter contains them. For a gated side effect:

1. verify the durable grant and activity-bound action identity when gated;
2. load only the declared input fields and dependency result references;
3. execute with the supplied deterministic idempotency key;
4. store the full result outside Temporal history;
5. read the destination back immediately;
6. return only the sanitized result reference, evidence digest, counts, and
   readback flag.

Permission, schema, validation, and approval failures must use the
non-retryable error types declared in the durable plan. Transient connector
failures may raise retryable errors.

## `emit_receipt`

Aggregate attempted/successful items and destination readbacks. A separate
verifier identity signs the sanitized receipt. The executor must not possess
the receipt-signing private key. Store the signed receipt in the verifier-owned
append-only evidence store before returning it to Temporal.

## Isolation

Run the adapter and Temporal worker under the runner service identity. The
planning agent must not be able to modify the adapter module, environment,
trust root, nonce database, receipt store, or signer services.
