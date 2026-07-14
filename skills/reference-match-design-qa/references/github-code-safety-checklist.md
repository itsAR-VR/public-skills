# GitHub Code Safety Checklist

Research date: 2026-05-18

Purpose: one canonical safety checklist for using public GitHub/component code
inside design work. the user has approved GitHub code use for this design-skill
work, so license anxiety should not block useful sources when he has explicitly
approved the source. Safety and product fit still matter.

## Before Running Any Code

- Inspect `package.json`, lockfiles, install scripts, `postinstall`, CLIs, and
  setup commands.
- Inspect dependency graph for unusual packages, install-time binaries, or
  packages with broad filesystem/network behavior.
- Do not run unknown setup scripts just to inspect a component.

## Before Copying Any Code

- Check network calls, analytics, trackers, telemetry, remote scripts, and
  remote assets.
- Check auth, payment, credentials, cookies, tokens, sessions, localStorage,
  and browser storage behavior.
- Check file-system, clipboard, camera, microphone, geolocation, notifications,
  and other browser/device APIs.
- Check dangerous execution: `eval`, `new Function`, dynamic script injection,
  obfuscated code, shell commands, code generation, and hidden side effects.
- Check upload, payment, webhook, email, and external API boundaries.
- Check fake logos, fake metrics, fake testimonials, unsupported claims, and
  copied brand styling.

## Copy Rules

- Copy the smallest useful component, behavior, or layout slice.
- Rewrite into local imports, tokens, accessibility behavior, states, copy, and
  proof.
- Replace demo data with truthful product data or clearly labeled placeholders.
- Preserve keyboard/focus behavior, labels, contrast, reduced motion, and
  responsive behavior.
- Do not adopt the whole starter repo unless the task explicitly requires that
  stack and the safety review passes.

## Proof Rules

- Record source URL and what was copied.
- Record what was rewritten locally.
- Capture desktop/mobile proof or a blocker.
- For risky sources, name the scripts/dependencies reviewed.
