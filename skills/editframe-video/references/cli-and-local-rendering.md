# Editframe CLI And Local Rendering

Official docs: https://editframe.com/docs/cli/render and https://editframe.com/docs/composition/rendering

## Scaffold

```bash
npm create @editframe@latest
cd my-video
npm start
```

Choose `html` for custom elements or `react` for TypeScript + React. The preview server opens locally with hot reload and a scrubber.

## Local CLI Render

```bash
npx editframe render -o output.mp4
```

By default, this renders `index.html` in the current directory to `output.mp4`.

Useful variants:

```bash
npx editframe render path/to/composition.html -o output.mp4
npx editframe render --url http://localhost:4321 -o output.mp4
npx editframe render -o output.mp4 --fps 60
npx editframe render -o output.mp4 --to-ms 5000
npx editframe render -o output.mp4 --from-ms 2000 --to-ms 7000
npx editframe render -o output.mp4 --data '{"title":"Launch Update"}'
npx editframe render -o output.mp4 --data-file data/render.json
```

Local rendering uses headless Chrome and FFmpeg. If rendering fails with a missing encoder/tool error, check:

```bash
node --version
ffmpeg -version
which ffmpeg
```

Install FFmpeg on macOS with:

```bash
brew install ffmpeg
```

## Browser-Side Render

Use browser-side rendering when the app itself should let a user export an MP4.

```js
const timegroup = document.getElementById("root");
const buffer = await timegroup.renderToVideo({
  fps: 30,
  codec: "avc",
  onProgress: ({ progress }) => {
    console.log(`${Math.round(progress * 100)}%`);
  },
});

const blob = new Blob([buffer], { type: "video/mp4" });
const url = URL.createObjectURL(blob);
const a = Object.assign(document.createElement("a"), {
  href: url,
  download: "output.mp4",
});
a.click();
```

For React, keep a ref to the root timegroup or use `TimelineRoot` so render cloning works correctly.

## Verification

After rendering:

```bash
ls -lh output.mp4
ffprobe -v error -show_entries stream=width,height,duration -of default=noprint_wrappers=1 output.mp4
open output.mp4
```

Confirm the file exists, duration is expected, dimensions match the requested format, and the first/last frames are not blank.
