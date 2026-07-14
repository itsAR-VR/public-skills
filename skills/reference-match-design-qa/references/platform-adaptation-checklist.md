# Platform Adaptation Checklist

Research date: 2026-05-18

Purpose: decide when a web UI should feel web-native, iOS-adapted,
Android-adapted, desktop-app-like, or cross-platform neutral.

Primary sources:

- Apple Human Interface Guidelines: https://developer.apple.com/design/human-interface-guidelines/
- Apple layout guidance: https://developer.apple.com/design/human-interface-guidelines/layout
- Apple right-to-left guidance: https://developer.apple.com/design/human-interface-guidelines/right-to-left
- Material platform adaptation: https://m1.material.io/platforms/platform-adaptation.html
- Framework7: https://framework7.io/

## Platform Modes

- `web-native`: standard browser/product patterns; best for SaaS, dashboards,
  commerce, docs, and public websites.
- `mobile-native-clean`: web UI behaves like a mobile app; use sheets, bottom
  actions, safe areas, large touch targets, and short flows.
- `ios-adapted`: use only when the audience expects iOS conventions or the app
  is wrapped for iOS.
- `android-adapted`: use only when Material/Android conventions are expected.
- `desktop-app-like`: dense panes, menus, keyboard shortcuts, inspectors, and
  persistent workspace chrome.
- `cross-platform-neutral`: consistent web product that avoids platform-specific
  styling but respects each platform's input constraints.

## Required Decisions

- platform_mode:
- safe_area_behavior:
- navigation_model:
- title_toolbar_behavior:
- back_behavior:
- primary_action_location:
- gesture_expectations:
- keyboard_shortcuts:
- touch_target_rule:
- mobile_sheet_behavior:
- desktop_panel_behavior:

## Done Gate

- Mobile primary action reachable.
- Back/cancel/close behavior is obvious.
- Safe-area and bottom actions do not overlap content.
- Platform-specific conventions are used deliberately, not accidentally.
- Gestures are not the only way to complete a critical action.
