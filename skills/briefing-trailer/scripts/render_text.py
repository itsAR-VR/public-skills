#!/usr/bin/env python3
"""
JSON-driven Pillow text renderer for briefing-trailer.

Expected input shape:
{
  "output_dir": "out",
  "canvas": {"width": 1920, "height": 1080, "background": "#0b0b0f"},
  "items": [
    {
      "name": "statement-01",
      "style": "statement",
      "text": "ONE FOUNDER.\nONE THURSDAY.",
      "subtitle": "Text-only teaser card"
    },
    {
      "name": "data-01",
      "style": "data",
      "kicker": "11:00 AM",
      "title": "RENEWAL CALL",
      "rows": ["TERM SHEET", "REDLINES", "DECISION WINDOW"]
    },
    {
      "name": "caption-01",
      "style": "caption",
      "text": "5:58 AM — the alarm wasn't what woke him.",
      "caption_center_y": 862
    }
  ]
}
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from PIL import Image, ImageColor, ImageDraw, ImageFont


FONT_CANDIDATES = {
    "serif": [
        "/usr/share/fonts/truetype/liberation2/LiberationSerif-Regular.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSerif-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "/Library/Fonts/Times New Roman.ttf",
        "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
    ],
    "sans": [
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/Library/Fonts/Arial.ttf",
        "/Library/Fonts/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ],
    "mono": [
        "/usr/share/fonts/truetype/liberation2/LiberationMono-Regular.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationMono-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
        "/System/Library/Fonts/Supplemental/Courier New.ttf",
        "/Library/Fonts/Courier New.ttf",
    ],
}


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "text"


def hex_rgba(value: str, alpha: int = 255) -> tuple[int, int, int, int]:
    rgb = ImageColor.getrgb(value)
    return rgb[0], rgb[1], rgb[2], alpha


def load_font(size: int, family: str = "sans", bold: bool = False) -> ImageFont.FreeTypeFont:
    family = family if family in FONT_CANDIDATES else "sans"
    candidates = list(FONT_CANDIDATES[family])
    if family == "serif" and bold:
        candidates = [
            "/usr/share/fonts/truetype/liberation2/LiberationSerif-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
            "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",
        ] + candidates
    elif family == "sans" and bold:
        candidates = [
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/Library/Fonts/Arial Bold.ttf",
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        ] + candidates
    elif family == "mono" and bold:
        candidates = [
            "/usr/share/fonts/truetype/liberation2/LiberationMono-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
        ] + candidates

    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size)
            except OSError:
                continue
    return ImageFont.load_default()


def measure_multiline(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, spacing: int) -> tuple[int, int]:
    box = draw.multiline_textbbox((0, 0), text, font=font, spacing=spacing, align="left")
    return box[2] - box[0], box[3] - box[1]


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> str:
    lines: list[str] = []
    for paragraph in text.splitlines() or [""]:
        if not paragraph.strip():
            lines.append("")
            continue
        words = paragraph.split()
        current = ""
        for word in words:
            candidate = word if not current else f"{current} {word}"
            if draw.textbbox((0, 0), candidate, font=font)[2] <= max_width:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
    return "\n".join(lines)


def fit_font(
    draw: ImageDraw.ImageDraw,
    text: str,
    family: str,
    max_width: int,
    max_height: int,
    start: int,
    minimum: int,
    bold: bool = False,
    spacing_ratio: float = 0.18,
) -> tuple[ImageFont.FreeTypeFont, str, int]:
    for size in range(start, minimum - 1, -2):
        font = load_font(size, family=family, bold=bold)
        spacing = max(1, int(size * spacing_ratio))
        wrapped = wrap_text(draw, text, font, max_width)
        width, height = measure_multiline(draw, wrapped, font, spacing)
        if width <= max_width and height <= max_height:
            return font, wrapped, spacing
    font = load_font(minimum, family=family, bold=bold)
    spacing = max(1, int(minimum * spacing_ratio))
    return font, wrap_text(draw, text, font, max_width), spacing


def render_statement(item: dict, canvas: dict) -> Image.Image:
    w = int(canvas.get("width", 1920))
    h = int(canvas.get("height", 1080))
    background = canvas.get("background", item.get("background", "#0b0b0f"))
    image = Image.new("RGBA", (w, h), hex_rgba(background))
    draw = ImageDraw.Draw(image)

    accent = item.get("accent", "#f04e23")
    title = item.get("text") or item.get("title") or ""
    subtitle = item.get("subtitle", "")
    font, wrapped, spacing = fit_font(draw, title, item.get("family", "serif"), int(w * 0.82), int(h * 0.60), int(h * 0.15), 48, bold=True)
    title_w, title_h = measure_multiline(draw, wrapped, font, spacing)
    x = (w - title_w) // 2
    y = (h - title_h) // 2 - 12
    shadow = hex_rgba("#000000", 110)
    draw.multiline_text((x + 4, y + 6), wrapped, font=font, fill=shadow, spacing=spacing, align="center")
    draw.multiline_text((x, y), wrapped, font=font, fill=hex_rgba(item.get("ink", "#f7f3eb")), spacing=spacing, align="center")
    draw.rectangle([int(w * 0.22), int(h * 0.72), int(w * 0.78), int(h * 0.725)], fill=hex_rgba(accent, 200))

    if subtitle:
        mono = load_font(max(18, int(h * 0.028)), family="mono", bold=False)
        sub = wrap_text(draw, subtitle, mono, int(w * 0.70))
        sw, sh = measure_multiline(draw, sub, mono, 6)
        draw.multiline_text(((w - sw) // 2, int(h * 0.78)), sub, font=mono, fill=hex_rgba(item.get("muted", "#a8a39a")), spacing=6, align="center")
    return image


def render_data(item: dict, canvas: dict) -> Image.Image:
    w = int(canvas.get("width", 1920))
    h = int(canvas.get("height", 1080))
    background = canvas.get("background", item.get("background", "#f4f1ea"))
    image = Image.new("RGBA", (w, h), hex_rgba(background))
    draw = ImageDraw.Draw(image)

    ink = item.get("ink", "#111111")
    muted = item.get("muted", "#6b655e")
    accent = item.get("accent", "#f04e23")
    kicker = item.get("kicker", "")
    title = item.get("title", item.get("text", ""))
    rows = item.get("rows") or item.get("lines") or []
    if isinstance(rows, str):
        rows = [line for line in rows.splitlines() if line.strip()]

    kicker_font = load_font(max(18, int(h * 0.03)), family="mono", bold=True)
    title_font, wrapped_title, title_spacing = fit_font(draw, title, item.get("family", "serif"), int(w * 0.80), int(h * 0.35), int(h * 0.11), 34, bold=True, spacing_ratio=0.12)
    body_font = load_font(max(22, int(h * 0.035)), family="mono", bold=False)

    draw.rectangle([int(w * 0.08), int(h * 0.10), int(w * 0.92), int(h * 0.11)], fill=hex_rgba(accent, 220))
    if kicker:
        draw.text((int(w * 0.08), int(h * 0.15)), kicker.upper(), font=kicker_font, fill=hex_rgba(accent))
    draw.multiline_text((int(w * 0.08), int(h * 0.22)), wrapped_title, font=title_font, fill=hex_rgba(ink), spacing=title_spacing)

    y = int(h * 0.58)
    for row in rows:
        row = str(row)
        wrapped = wrap_text(draw, row, body_font, int(w * 0.75))
        draw.multiline_text((int(w * 0.08), y), wrapped, font=body_font, fill=hex_rgba(muted), spacing=6)
        _, row_h = measure_multiline(draw, wrapped, body_font, 6)
        y += row_h + 12
    return image


def render_caption(item: dict, canvas: dict) -> Image.Image:
    w = int(canvas.get("width", 1920))
    h = int(canvas.get("height", 1080))
    image = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    text = item.get("text") or item.get("title") or ""
    accent = item.get("accent", "#f04e23")
    ink = item.get("ink", "#f7f3eb")
    muted = item.get("muted", "#c8c3b8")
    caption_center_y = int(item.get("caption_center_y", canvas.get("caption_center_y", max(720, h - 218))))
    max_width = int(w * 0.72)
    font, wrapped, spacing = fit_font(draw, text, item.get("family", "sans"), max_width - 48, int(h * 0.20), int(h * 0.048), 22, bold=True, spacing_ratio=0.14)
    text_w, text_h = measure_multiline(draw, wrapped, font, spacing)
    box_w = int(min(max_width, text_w + 64))
    box_h = int(text_h + 34)
    x0 = (w - box_w) // 2
    y0 = max(24, caption_center_y - box_h // 2)
    y0 = min(y0, h - box_h - 24)
    draw.rounded_rectangle([x0, y0, x0 + box_w, y0 + box_h], radius=24, fill=(13, 14, 18, 190), outline=(255, 255, 255, 28), width=1)
    draw.rounded_rectangle([x0 + 18, y0 + 17, x0 + 24, y0 + box_h - 17], radius=3, fill=hex_rgba(accent, 240))
    draw.multiline_text((x0 + 38, y0 + 16), wrapped, font=font, fill=hex_rgba(ink), spacing=spacing)
    if item.get("kicker"):
        mono = load_font(max(16, int(h * 0.026)), family="mono", bold=False)
        draw.text((x0 + 38, y0 - 30), str(item["kicker"]).upper(), font=mono, fill=hex_rgba(muted))
    return image


def render_item(item: dict, canvas: dict, output_dir: Path) -> Path:
    style = (item.get("style") or item.get("type") or "statement").lower()
    name = item.get("name") or slugify(item.get("text") or item.get("title") or style)
    image = {
        "statement": render_statement,
        "data": render_data,
        "caption": render_caption,
    }.get(style, render_statement)(item, canvas)
    output = Path(item.get("output") or output_dir / f"{name}.png")
    if not output.is_absolute():
        output = (output_dir / output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)
    return output


def load_spec(path: Path) -> tuple[dict, list[dict], str | None]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return {}, data, None
    if "items" in data:
        return data.get("canvas", {}), data["items"], data.get("output_dir")
    if "cards" in data:
        return data.get("canvas", {}), data["cards"], data.get("output_dir")
    return data.get("canvas", {}), [data], data.get("output_dir")


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Pillow text cards from JSON specs")
    parser.add_argument("spec", help="Path to textspec.json")
    parser.add_argument("--out-dir", help="Output directory (defaults to spec output_dir or spec directory / out)")
    args = parser.parse_args()

    spec_path = Path(args.spec)
    canvas, items, spec_output_dir = load_spec(spec_path)
    out_dir = Path(args.out_dir or spec_output_dir or "out")
    if not out_dir.is_absolute():
        out_dir = (spec_path.parent / out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    outputs = [render_item(item, canvas, out_dir) for item in items]
    for output in outputs:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
