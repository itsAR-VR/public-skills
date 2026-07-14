# Service Journey Blueprint

Research date: 2026-05-18

Purpose: make platforms and apps coherent across screens, roles, messages,
states, and handoffs. A single screen can look good while the whole experience
still feels broken.

Use this for apps, platforms, dashboards, onboarding, support flows,
marketplaces, CRM/workflow tools, AI-agent workspaces, admin panels, and any
product where multiple steps or roles touch one outcome.

## Required Fields

- journey_name:
- actors:
- stages:
- entry_point:
- frontstage_UI:
- backstage_systems:
- notifications_or_messages:
- handoffs:
- permission_or_approval_points:
- data_created_or_changed:
- failure_points:
- recovery_paths:
- human_support_or_escalation:
- receipt_or_audit_trail:
- completion_state:
- reentry_or_resume_state:

## Journey Table

| Stage | Actor | Frontstage UI | Backstage/system | Failure risk | Recovery |
| --- | --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD | TBD |

## Design Rules

- Design the before, during, after, and return visit, not only the happy path.
- If a system is doing work in the background, show status and ownership.
- If a person needs to approve, review, or hand off, make that boundary visible.
- Every commitment should create a receipt, confirmation, or audit surface.
- Every failure should tell the user what happened, what to do next, and what
  was or was not changed.

## Proof

- journey_artifact:
- primary_path_checked:
- failure_path_checked:
- role_or_handoff_checked:
- receipt_or_audit_checked:
