#!/usr/bin/env python3
"""
Assemble a claymation explainer with one VO track and trimmed clip windows.

Usage:
  python3 scripts/assemble.py --clips s1.mp4 s2.mp4 --vo vo.wav --out final.mp4
"""

from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def parse_size(value: str) -> tuple[int, int]:
    parts = value.lower().split("x", 1)
    if len(parts) != 2:
        raise ValueError(f"Invalid size spec: {value!r}")
    return int(parts[0]), int(parts[1])


def cover_filter(width: int, height: int, fps: int) -> str:
    return (
        f"scale={width}:{height}:force_original_aspect_ratio=increase,"
        f"crop={width}:{height},fps={fps},setsar=1,format=yuv420p"
    )


def render_clip(clip: Path, out_path: Path, width: int, height: int, fps: int, trim_start: float, duration: float) -> None:
    vf = cover_filter(width, height, fps)
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(trim_start),
        "-t", str(duration),
        "-i", str(clip),
        "-vf", vf,
        "-an",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "20",
        "-movflags", "+faststart",
        str(out_path),
    ]
    run(cmd)


def concat_video(segments: list[Path], out_path: Path) -> None:
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


def build_vo_track(vo: Path, out_path: Path, total_duration: float, delay: float) -> None:
    delay_ms = max(0, int(delay * 1000))
    fade_start = max(0.0, total_duration - 0.9)
    run([
        "ffmpeg", "-y",
        "-i", str(vo),
        "-af", (
            f"adelay={delay_ms}|{delay_ms},"
            f"afade=t=in:st=0:d=0.25,"
            f"afade=t=out:st={fade_start}:d=0.8,"
            f"apad=whole_dur={total_duration}"
        ),
        "-ar", "48000",
        "-ac", "2",
        "-c:a", "aac",
        "-b:a", "192k",
        str(out_path),
    ])


def mux_video_audio(video: Path, audio: Path | None, out_path: Path, total_duration: float) -> None:
    # Keep the final edit length anchored to the planned clip runtime, not VO length.
    if audio is None:
        run([
            "ffmpeg", "-y",
            "-i", str(video),
            "-t", str(total_duration),
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
        "-t", str(total_duration),
        "-movflags", "+faststart",
        str(out_path),
    ])


def main() -> int:
    parser = argparse.ArgumentParser(description="Assemble a claymation explainer")
    parser.add_argument("--clips", nargs="+", required=True, help="Ordered clip files")
    parser.add_argument("--vo", help="Single voiceover WAV/MP3")
    parser.add_argument("--out", required=True, help="Output MP4")
    parser.add_argument("--per-clip", type=float, default=3.0, help="Seconds per clip window")
    parser.add_argument("--trim-start", type=float, default=1.0, help="Trim start offset in each clip")
    parser.add_argument("--vo-delay", type=float, default=0.3, help="Delay applied to the VO track")
    parser.add_argument("--fps", type=int, default=24, help="Target FPS")
    parser.add_argument("--size", default="1280x720", help="Target size WIDTHxHEIGHT")
    args = parser.parse_args()

    width, height = parse_size(args.size)
    clips = [Path(path) for path in args.clips]
    out_path = Path(args.out)

    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        segments: list[Path] = []
        for index, clip in enumerate(clips):
            segment = tmpdir / f"segment_{index:02d}.mp4"
            render_clip(clip, segment, width, height, args.fps, args.trim_start, args.per_clip)
            segments.append(segment)

        concat_path = tmpdir / "concat.mp4"
        concat_video(segments, concat_path)

        total_duration = len(segments) * args.per_clip
        faded_path = tmpdir / "faded.mp4"
        fade_start = max(0.0, total_duration - 0.6)
        run([
            "ffmpeg", "-y",
            "-i", str(concat_path),
            "-vf", f"fade=t=out:st={fade_start}:d=0.6",
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "20",
            "-an",
            str(faded_path),
        ])

        audio_path = None
        if args.vo:
            audio_path = tmpdir / "vo.m4a"
            build_vo_track(Path(args.vo), audio_path, total_duration, args.vo_delay)

        mux_video_audio(faded_path, audio_path, out_path, total_duration)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
