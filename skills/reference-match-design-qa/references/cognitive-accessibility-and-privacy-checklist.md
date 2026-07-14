# Cognitive Accessibility And Privacy Checklist

Research date: 2026-05-18

Purpose: extend the accessibility and trust layer beyond color contrast. Use
this when a flow asks users to understand choices, remember information, grant
permissions, share data, pay money, approve actions, recover from errors, or
complete multi-step work.

## Sources To Prefer

- W3C COGA usable content: https://www.w3.org/TR/coga-usable/
- WCAG 2.2 understanding docs: https://www.w3.org/WAI/WCAG22/Understanding/
- U.S. Web Design System accessibility: https://designsystem.digital.gov/documentation/accessibility/
- Apple privacy guidance: https://developer.apple.com/design/human-interface-guidelines/privacy

## Required Fields

- plain_language_checked:
- memory_load_risk:
- visible_steps_or_progress:
- labels_remain_visible:
- help_in_context:
- undo_or_back_path:
- timeout_or_data_loss_risk:
- interruption_risk:
- personalization_or_simplification_needed:
- screen_reader_status_messages:
- keyboard_path:
- focus_return:
- target_size:
- reduced_motion:
- permission_or_data_request:
- permission_rationale:
- data_collection_summary:
- opt_out_or_revoke_path:
- privacy_receipt_or_settings_path:

## Design Rules

- Keep labels, progress, and important previous choices visible when users need
  them.
- Prefer recognition over memory: visible options beat hidden instructions.
- Do not make users lose work because of timeouts, navigation mistakes, or
  unclear back behavior.
- Ask for permission at the point of value, explain why, and show how to change
  the choice later.
- Privacy copy should be plain, specific, and placed before the user commits.

## Proof

- keyboard_check:
- screen_reader_or_status_note:
- zoom_or_text_spacing_check:
- reduced_motion_check:
- privacy_permission_check:
- cognitive_load_risk_remaining:
