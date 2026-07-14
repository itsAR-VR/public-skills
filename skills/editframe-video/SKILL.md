---
name: editframe-video
description: Build, preview, render, or automate programmatic video with Editframe. Use when the user mentions Editframe, editframe.com, @editframe/api, @editframe/react, npx editframe, cloud renders, browser-side video rendering, HTML/CSS video compositions, React video compositions, or asks to build video with Editframe.
metadata:
  version: 1.0.0
  tags: editframe, video, programmatic-video, html, css, react, rendering
---

# Editframe Video

Use Editframe when the requested output is a programmatic video built from HTML, CSS, JavaScript, or React, especially when the user wants templates, data-driven videos, browser preview, local MP4 rendering, cloud rendering, or reusable video tooling.

## First Decision

Pick the rendering path before writing code:

| Need | Use |
| --- | --- |
| Fast prototype or one-off local MP4 | Editframe CLI local render |
| Interactive browser export | `renderToVideo` in the browser |
| Server-side/batch production output | `@editframe/api` cloud render |
| Existing React app or typed components | `@editframe/react` |
| Plain web output that agents can edit easily | HTML custom elements |

## Workflow

1. Confirm the video brief: audience, format, duration, aspect ratio, assets, and whether output should be local or cloud-rendered.
2. Check local prerequisites: Node 22+, a browser-capable environment, and FFmpeg for local CLI rendering.
3. Scaffold or adapt an Editframe project.
4. Build the composition around a root `ef-timegroup` or React `Timegroup`.
5. Preview before rendering. Scrub the timeline and inspect frame boundaries.
6. Render with the chosen path.
7. Verify the output by confirming the MP4 exists, opens, and matches duration/aspect ratio.

## Quick Commands

```bash
npm create @editframe@latest
cd my-video
npm start
npx editframe render -o output.mp4
```

For an existing project:

```bash
npm install @editframe/react
npm install @editframe/api
```

## References

- For HTML custom elements, React composition patterns, timegroups, and layout, read [references/composition.md](references/composition.md).
- For previewing and local MP4 rendering, read [references/cli-and-local-rendering.md](references/cli-and-local-rendering.md).
- For `@editframe/api`, cloud rendering, uploads, webhooks, and URL signing, read [references/server-api.md](references/server-api.md).

## Guardrails

- Never expose `EDITFRAME_API_KEY` in browser code, client bundles, examples, logs, or committed files.
- Prefer local render for quick proofs and cloud render for production/batch jobs.
- Do not claim a render succeeded until the output file or cloud render status is checked.
- If a user asks for generic AI video generation, use the broader video-generation skills. Use this skill only when Editframe is named or clearly the right programmatic-video tool.
