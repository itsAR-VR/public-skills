# Editframe Composition

Official docs: https://editframe.com/docs and https://editframe.com/docs/getting-started

## Mental Model

An Editframe composition is a web page that acts like a video timeline. The core container is a timegroup:

- `ef-timegroup` sets duration, layout mode, FPS, and canvas dimensions.
- Child elements include `ef-video`, `ef-audio`, `ef-image`, `ef-text`, `ef-captions`, `ef-waveform`, and normal HTML.
- CSS controls layout and animation. Treat the canvas as fixed-size for final video output.
- Preview controls usually live inside `ef-preview` with a scrubber, play toggle, and time display.

## Minimal HTML Composition

```html
<ef-preview>
  <ef-timegroup id="root" mode="fixed" duration="5s">
    <ef-text class="headline">Hello from Editframe</ef-text>
  </ef-timegroup>
  <ef-scrubber></ef-scrubber>
  <ef-time-display></ef-time-display>
  <ef-toggle-play></ef-toggle-play>
</ef-preview>

<style>
  #root {
    width: 1920px;
    height: 1080px;
    background: #111827;
    display: grid;
    place-items: center;
  }

  .headline {
    color: white;
    font-size: 120px;
    font-weight: 800;
  }
</style>
```

## Common Timegroup Patterns

Use `mode="fixed"` when the segment has a known duration. Use `mode="contain"` when duration should come from a media child. Use `mode="sequence"` when child timegroups or clips should play one after another.

```html
<ef-timegroup id="root" mode="sequence" class="canvas">
  <ef-timegroup mode="fixed" duration="4s">
    <ef-video src="/assets/intro.mp4" sourceout="4s"></ef-video>
    <ef-text class="lower-third">Opening</ef-text>
  </ef-timegroup>

  <ef-timegroup mode="fixed" duration="4s">
    <ef-image src="/assets/chart.png"></ef-image>
    <ef-text class="title">Q2 results</ef-text>
  </ef-timegroup>
</ef-timegroup>
```

## React Composition

Use React when the project already uses React or when TypeScript props make repeated templates easier to maintain.

```tsx
import { Timegroup, Text, Video } from "@editframe/react";

export function ProductUpdateVideo() {
  return (
    <Timegroup mode="sequence" className="w-[1920px] h-[1080px] bg-black">
      <Timegroup mode="fixed" duration="5s" className="relative w-full h-full">
        <Video
          src="/assets/demo.mp4"
          sourceIn="2s"
          sourceOut="7s"
          className="size-full"
          style={{ objectFit: "cover" }}
        />
        <Text className="absolute bottom-16 left-16 text-white text-7xl font-bold">
          New workflow
        </Text>
      </Timegroup>
    </Timegroup>
  );
}
```

React props use camelCase for attributes that are lowercase or hyphenated in HTML. For example, HTML `sourcein` and `sourceout` become React `sourceIn` and `sourceOut`.

## Composition Checklist

- Set exact pixel dimensions on the root canvas: `1920x1080`, `1080x1920`, or `1080x1080`.
- Keep text inside safe margins for social formats.
- Prefer local assets or uploaded Editframe file IDs for stable production renders.
- If using uploaded files from Editframe, wrap the composition in `ef-configuration` and reference media with `file-id`.
- Preview before rendering and scrub scene boundaries, intro/outro, and audio sync.
