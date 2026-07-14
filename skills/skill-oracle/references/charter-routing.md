# Charter Reuse Branch (Step 4.5 detail)

Load this file only when Step 4.5's trigger fires: the routed task is
multi-system, repeated, event-driven, long-running, or side-effecting.

After selecting the smallest skill stack, choose one route:

1. direct skill stack
2. reuse or suggest an exactly compatible verified charter
3. compile a new charter

Do not load a charter registry into model context. Normalize the outcome and
run the deterministic matcher against the operator-configured registry —
outcome-charter defines no global default registry location; the registry
path and query file are deployment-supplied (see
`skills/outcome-charter/references/deployment.md`). If no registry is
configured in this deployment, the branch resolves to compile-or-direct; a
missing registry is a routing outcome, not an error:

```bash
python3 skills/outcome-charter/scripts/charter_registry.py match \
  --registry "$CHARTER_REGISTRY_PATH" \
  --query "$CHARTER_QUERY_PATH"
```

The matcher, not semantic similarity, decides compatibility across auth
account/tenant identifiers, tool-operation schema digests, approval-policy
version, derived approval requirements, required inputs/outputs, charter
version, runner contract, and the immutable executable-definition digest.

- `compile` -> activate `outcome-charter` in compile mode.
- `suggest` -> present the prior charter as a candidate; do not auto-run.
- `reuse` -> activate `outcome-charter` in reuse mode only when a trusted runner
  has verified signed capability, approval, and destination-readback
  attestations.

Reuse eligibility thresholds (capability snapshot, trusted destination-readback
receipt count, minimum item count, item success rate, family-level quarantine)
are owned and enforced by `outcome-charter` — see `skills/outcome-charter/SKILL.md`
and its `charter_registry.py` implementation; this router does not re-state or
re-derive them. Historical credentials, payloads, IDs, idempotency keys, and
approvals never carry forward. The runner must call
`charter_registry.py authorize` immediately before any gated side effect;
Oracle routing metadata alone never authorizes execution.

Event-triggered recovery and repeated self-healing tasks must compose
`outcome-charter` with `loop-engineering`: the charter owns the typed execution
contract while loop-engineering owns stop conditions, non-convergence, and
escalation.

This branch chooses the execution contract; it does not turn Skill Oracle into
the workflow runner. `outcome-charter` owns compilation, receipts, and runner
selection. Temporal or another durable engine is warranted only when
event-triggering, long duration, concurrency, or crash recovery requires it.
