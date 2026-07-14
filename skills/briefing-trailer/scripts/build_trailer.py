#!/usr/bin/env python3
"""
OOM-safe trailer assembler for briefing-trailer.

Expected cutsheet shape:
{
  "output": "trailer.mp4",
  "size": [1920, 1080],
  "fps": 30,
  "letterbox": 132,
  "grade": {"brightness": 0.02, "saturation": 1.05},
  "audio": {"mode": "synth_tension", "ambient_from": "clips/roomtone.mp4"},
  "shots": [
    {"type": "card", "image": "cards/opening.png", "duration": 1.8},
    {"type": "footage", "source": "clips/c1.mp4", "in": 1.0, "out": 3.0, "caption": "cards/c1.png"},
    {"type": "insert", "image": "stills/email.png", "duration": 1.7}
  ]
}

Footage shots accept the documented in/out window or the older start/duration
pair. When both are present, in/out defines the trimmed window.
If audio.ambient_from is set and mode is synth_tension, the clip is looped and
mixed quietly under the synth bed.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def resolve(path: str | None, base: Path) -> Path | None:
    if not path:
        return None
    resolved = Path(path)
    return resolved if resolved.is_absolute() else (base / resolved).resolve()


def parse_size(value) -> tuple[int, int]:
    if isinstance(value, (list, tuple)) and len(value) == 2:
        return int(value[0]), int(value[1])
    if isinstance(value, str) and "x" in value:
        width, height = value.lower().split("x", 1)
        return int(width), int(height)
    return 1920, 1080


def contain_vf(width: int, height: int, fps: int, duration: float, fade: float = 0.20) -> str:
    fade_out = max(0.0, duration - fade)
    return ",".join([
        f"scale={width}:{height}:force_original_aspect_ratio=decrease",
        f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=black",
        f"fps={fps}",
        f"fade=t=in:st=0:d={fade}",
        f"fade=t=out:st={fade_out}:d={fade}",
        "format=yuv420p",
        "setsar=1",
    ])


def cover_vf(width: int, height: int, fps: int, duration: float, fade: float = 0.20) -> str:
    fade_out = max(0.0, duration - fade)
    return ",".join([
        f"scale={width}:{height}:force_original_aspect_ratio=increase",
        f"crop={width}:{height}",
        f"fps={fps}",
        f"fade=t=in:st=0:d={fade}",
        f"fade=t=out:st={fade_out}:d={fade}",
        "format=yuv420p",
        "setsar=1",
    ])


def parse_footage_window(shot: dict, default_duration: float = 1.8) -> tuple[float, float]:
    start_value = shot.get("in", shot.get("start", 0.0))
    start = float(start_value)
    out_value = shot.get("out")
    if out_value is not None:
        duration = float(out_value) - start
    else:
        duration = float(shot.get("duration", default_duration))
    if duration <= 0:
        raise ValueError(f"Footage shot has an invalid window: start={start!r}, duration={duration!r}")
    return start, duration


def render_image_segment(image: Path, out_path: Path, width: int, height: int, fps: int, duration: float, mode: str = "contain", caption: Path | None = None) -> None:
    base_vf = contain_vf(width, height, fps, duration) if mode == "contain" else cover_vf(width, height, fps, duration)
    if caption is None:
        run([
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", str(image),
            "-t", str(duration),
            "-vf", base_vf,
            "-an",
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "20",
            "-movflags", "+faststart",
            str(out_path),
        ])
        return

    filter_complex = (
        f"[0:v]{base_vf}[base];"
        f"[1:v]scale=iw:ih,format=rgba[cap];"
        f"[base][cap]overlay=0:0:format=auto[vout]"
    )
    run([
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", str(image),
        "-loop", "1",
        "-i", str(caption),
        "-t", str(duration),
        "-filter_complex", filter_complex,
        "-map", "[vout]",
        "-an",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "20",
        "-movflags", "+faststart",
        str(out_path),
    ])


def render_footage_segment(source: Path, out_path: Path, width: int, height: int, fps: int, start: float, duration: float, caption: Path | None = None) -> None:
    base_vf = cover_vf(width, height, fps, duration)
    if caption is None:
        run([
            "ffmpeg", "-y",
            "-ss", str(start),
            "-t", str(duration),
            "-i", str(source),
            "-vf", base_vf,
            "-an",
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "20",
            "-movflags", "+faststart",
            str(out_path),
        ])
        return

    # Keep the captioned segment bounded by the trimmed footage window.
    filter_complex = (
        f"[0:v]{base_vf}[base];"
        f"[1:v]scale=iw:ih,format=rgba[cap];"
        f"[base][cap]overlay=0:0:shortest=1:format=auto[vout]"
    )
    run([
        "ffmpeg", "-y",
        "-ss", str(start),
        "-t", str(duration),
        "-i", str(source),
        "-loop", "1",
        "-i", str(caption),
        "-filter_complex", filter_complex,
        "-map", "[vout]",
        "-an",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "20",
        "-movflags", "+faststart",
        str(out_path),
    ])


def concat_segments(segments: list[Path], out_path: Path) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        list_file = Path(tmp) / "concat.txt"
        list_file.write_text("".join(f"file '{segment.as_posix()}'\n" for segment in segments), encoding="utf-8")
        run([
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", str(list_file),
            "-c", "copy",
            str(out_path),
        ])


def build_synth_audio(duration: float, out_path: Path, ambient_source: Path | None = None) -> None:
    boom_duration = min(0.9, max(0.35, duration * 0.08))
    boom_delay_ms = max(0, int((duration - boom_duration - 0.35) * 1000))
    fade_out = max(0.0, duration - 0.85)
    if ambient_source is not None and not ambient_source.exists():
        raise FileNotFoundError(f"Ambient source not found: {ambient_source}")

    # Keep the synthesized bed dominant and tuck room tone underneath when asked.
    inputs = [
        "-f", "lavfi", "-t", str(duration),
        "-i", f"sine=frequency=55:sample_rate=48000:duration={duration}",
        "-f", "lavfi", "-t", str(duration),
        "-i", f"sine=frequency=110:sample_rate=48000:duration={duration}",
        "-f", "lavfi", "-t", str(boom_duration),
        "-i", f"sine=frequency=44:sample_rate=48000:duration={boom_duration}",
    ]
    if ambient_source is not None:
        inputs.extend(["-stream_loop", "-1", "-i", str(ambient_source)])

    filter_complex = (
        "[0:a][1:a]amix=inputs=2:normalize=0,volume=0.16,lowpass=f=1200,"
        "tremolo=f=4:d=0.55,afade=t=in:st=0:d=0.9,"
        f"afade=t=out:st={fade_out}:d=0.85[base];"
        f"[2:a]adelay={boom_delay_ms}|{boom_delay_ms},volume=0.85[boom];"
    )
    if ambient_source is not None:
        filter_complex += (
            f"[3:a]atrim=0:{duration},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo,"
            "highpass=f=80,lowpass=f=1400,volume=0.16,afade=t=in:st=0:d=0.8,"
            f"afade=t=out:st={fade_out}:d=0.8[amb];"
            "[base][boom][amb]amix=inputs=3:duration=first:normalize=0:weights='1 1 0.8',alimiter=limit=0.92[aout]"
        )
    else:
        filter_complex += "[base][boom]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.92[aout]"

    run([
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", "[aout]",
        "-ar", "48000",
        "-ac", "2",
        str(out_path),
    ])


def grade_video(video: Path, out_path: Path, letterbox: int, brightness: float, saturation: float) -> None:
    vf_parts = [
        f"eq=brightness={brightness}:saturation={saturation}",
        "vignette",
    ]
    if letterbox > 0:
        vf_parts.append(f"drawbox=x=0:y=0:w=iw:h={letterbox}:color=black:t=fill")
        vf_parts.append(f"drawbox=x=0:y=ih-{letterbox}:w=iw:h={letterbox}:color=black:t=fill")
    vf_parts.extend(["format=yuv420p", "setsar=1"])
    run([
        "ffmpeg", "-y",
        "-i", str(video),
        "-vf", ",".join(vf_parts),
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-an",
        str(out_path),
    ])


def mux_audio(video: Path, audio: Path | None, out_path: Path) -> None:
    if audio is None:
        run([
            "ffmpeg", "-y",
            "-i", str(video),
            "-c", "copy",
            str(out_path),
        ])
        return
    run([
        "ffmpeg", "-y",
        "-i", str(video),
        "-i", str(audio),
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-movflags", "+faststart",
        str(out_path),
    ])


def load_shots(spec: dict) -> list[dict]:
    shots = spec.get("shots")
    if shots is None:
        if isinstance(spec, list):
            return spec
        return [spec]
    return shots


def main() -> int:
    parser = argparse.ArgumentParser(description="Assemble a briefing-trailer cutsheet")
    parser.add_argument("cutsheet", help="JSON cutsheet")
    args = parser.parse_args()

    spec_path = Path(args.cutsheet)
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    base = spec_path.parent
    width, height = parse_size(spec.get("size", (1920, 1080)))
    fps = int(spec.get("fps", 30))
    output = resolve(spec.get("output", "trailer.mp4"), base)
    letterbox = int(spec.get("letterbox", 132))
    grade = spec.get("grade", {})
    brightness = float(grade.get("brightness", 0.02))
    saturation = float(grade.get("saturation", 1.05))
    audio_spec = (spec.get("audio", {}) or {})
    ambient_from = resolve(audio_spec.get("ambient_from"), base)
    audio_mode = audio_spec.get("mode") or ("synth_tension" if ambient_from else "none")

    shots = load_shots(spec)

    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        segments: list[Path] = []
        total_duration = 0.0
        for idx, shot in enumerate(shots):
            shot_type = (shot.get("type") or "card").lower()
            duration = float(shot.get("duration", 1.8))
            segment = tmpdir / f"segment_{idx:02d}.mp4"
            caption = resolve(shot.get("caption"), base)
            if shot_type in {"card", "endcard", "insert"}:
                source_image = resolve(shot.get("image") or shot.get("source"), base)
                if source_image is None:
                    raise ValueError(f"Shot {idx} ({shot_type}) needs an image/source")
                mode = "contain" if shot_type == "card" else "cover"
                render_image_segment(source_image, segment, width, height, fps, duration, mode=mode, caption=caption)
            elif shot_type == "footage":
                source_video = resolve(shot.get("video") or shot.get("source"), base)
                if source_video is None:
                    raise ValueError(f"Shot {idx} ({shot_type}) needs a source video")
                start, duration = parse_footage_window(shot, duration)
                render_footage_segment(source_video, segment, width, height, fps, start, duration, caption=caption)
            else:
                raise ValueError(f"Unknown shot type: {shot_type!r}")
            segments.append(segment)
            total_duration += duration

        concat_path = tmpdir / "concat.mp4"
        concat_segments(segments, concat_path)

        graded_path = tmpdir / "graded.mp4"
        grade_video(concat_path, graded_path, letterbox, brightness, saturation)

        audio_path: Path | None = None
        if audio_mode == "synth_tension":
            audio_path = tmpdir / "bed.wav"
            build_synth_audio(total_duration, audio_path, ambient_source=ambient_from)

        mux_audio(graded_path, audio_path, output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
