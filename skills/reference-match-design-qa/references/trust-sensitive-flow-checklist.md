# Trust-Sensitive Flow Checklist

Research date: 2026-05-18

Purpose: make high-trust screens harder to get wrong. Use this for payments,
subscriptions, billing, auth, onboarding with permissions, healthcare, legal,
finance, privacy, agent approvals, destructive actions, account settings, and
any flow where a confusing UI could cost money, access, data, or trust.

## Trust Rules

- The user must know what will happen before they click the primary action.
- Prices, totals, renewal terms, trial terms, permissions, risk, and reversibility
  must be visible before commitment.
- A destructive or irreversible action needs confirmation, recovery language,
  and a calm visual hierarchy.
- Errors need plain-English recovery steps, not only red text.
- Agent/autonomous actions need approval boundaries, tool status, receipts, and
  a visible way to stop or inspect work.

## Required Fields

- trust_flow_type:
- commitment_or_risk:
- primary_commitment_copy:
- total_or_permission_summary:
- review_before_submit_needed:
- confirmation_or_receipt_state:
- cancellation_or_recovery_path:
- failure_states:
- privacy_or_security_copy:
- audit_or_receipt_surface:
- proof_screenshots:

## Product-Specific Checks

| Flow | Must show |
| --- | --- |
| Checkout/payment | Item, quantity, tax/shipping/fees, total, billing interval, payment error, receipt. |
| Subscription | Plan, renewal timing, trial end, cancellation path, downgrade/upgrade effect. |
| Auth/account | Why credentials are needed, recovery, session/permission limits, rate/error states. |
| Agent approval | Tool/action name, data touched, risk, approve/deny, stop/cancel, receipt. |
| Destructive action | What is deleted/changed, whether it can be undone, confirmation copy, after-state. |
| Personal/private data | What is collected, where it goes, why it is needed, and how to change/remove it. |

## Done Gate

- trust_summary_visible:
- commitment_clear_before_action:
- failure_recovery_visible:
- receipt_or_audit_visible:
- no_dark_pattern_language:
- mobile_commitment_view_checked:

If these are not true, the UI may look polished but still fails the design job.
