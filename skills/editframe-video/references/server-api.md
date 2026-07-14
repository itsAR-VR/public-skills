# Editframe Server API

Official docs: https://editframe.com/skills/editframe-api

## When To Use

Use `@editframe/api` when renders, uploads, or media access need to happen on a server:

- batch or cloud video rendering
- uploading video, image, or caption files
- generating transcriptions
- downloading completed renders
- creating signed URLs for browser playback without exposing an API key

## Setup

```bash
npm install @editframe/api
```

Set the API key outside source control:

```bash
export EDITFRAME_API_KEY="..."
```

Never place this key in frontend code. The API client is server-side only.

## Cloud Render

```ts
import { Client, createRender, getRenderProgress, downloadRender } from "@editframe/api";
import { writeFile } from "node:fs/promises";

const client = new Client(process.env.EDITFRAME_API_KEY);

const render = await createRender(client, {
  html: `
    <ef-timegroup mode="fixed" duration="5s" class="w-[1920px] h-[1080px] bg-black">
      <ef-text class="text-white text-8xl">Hello from Editframe</ef-text>
    </ef-timegroup>
  `,
  width: 1920,
  height: 1080,
  fps: 30,
});

for await (const event of await getRenderProgress(client, render.id)) {
  console.log(`render ${render.id}: ${event.progress}%`);
}

const response = await downloadRender(client, render.id);
await writeFile("output.mp4", Buffer.from(await response.arrayBuffer()));
```

## Files And Media Pipeline

Use uploaded files when production compositions need durable media references.

```ts
import { Client, upload, getFileProcessingProgress } from "@editframe/api/node";

const client = new Client(process.env.EDITFRAME_API_KEY);
const { file, uploadIterator } = await upload(client, "assets/demo.mp4");

for await (const event of uploadIterator) {
  console.log(`upload: ${event.progress}%`);
}

for await (const event of await getFileProcessingProgress(client, file.id)) {
  console.log(`processing: ${event.progress}%`);
}
```

Reference uploaded files in a composition with `file-id`:

```html
<ef-configuration api-host="https://editframe.com">
  <ef-timegroup mode="contain" class="w-[1920px] h-[1080px]">
    <ef-video file-id="uploaded-video-file-id"></ef-video>
    <ef-image file-id="uploaded-image-file-id" class="w-24 h-24"></ef-image>
  </ef-timegroup>
</ef-configuration>
```

## URL Signing

If browser code needs private Editframe media, create a server route that calls `createURLToken` and configure the frontend with a signing URL. This keeps the API key on the server while allowing the browser to request short-lived access.

## Reliability Notes

- Handle missing `EDITFRAME_API_KEY` before making a request.
- Use retry/backoff for rate-limit responses when bulk-uploading or creating many renders.
- Poll or stream progress until completion before downloading.
- Record render IDs in logs so failed jobs can be inspected later without rerunning everything.
