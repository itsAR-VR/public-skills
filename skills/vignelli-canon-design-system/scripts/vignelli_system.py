#!/usr/bin/env python3
"""
Deterministic token generator for the Vignelli Canon design system.

Usage:
  python3 scripts/vignelli_system.py --primary "#F04E23" --base 16 --format css
  python3 scripts/vignelli_system.py --format json --signage
"""

from __future__ import annotations

import argparse
import colorsys
import json
from typing import Dict, Tuple


GRID_LIBRARY: Dict[str, Tuple[int, int]] = {
    "2x4": (2, 4),
    "5x4": (5, 4),
    "3x6": (3, 6),
    "6x6": (6, 6),
    "4x8": (4, 8),
}

SIGNAGE_TABLE = [
    {
        "level": "Identification",
        "cap_height": "largest",
        "panel": "signal-blue",
        "text": "white Helvetica",
        "note": "station name / destination blind",
    },
    {
        "level": "Directional",
        "cap_height": "medium",
        "panel": "signal-blue",
        "text": "white Helvetica",
        "note": "overhead arrows and routes",
    },
    {
        "level": "Information",
        "cap_height": "small",
        "panel": "white",
        "text": "signal-blue Helvetica",
        "note": "rules, exits, amenities",
    },
]


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def normalize_hex(value: str) -> str:
    value = value.strip().lstrip("#")
    if len(value) == 3:
        value = "".join(ch * 2 for ch in value)
    if len(value) != 6:
        raise ValueError(f"Expected hex color, got {value!r}")
    return f"#{value.upper()}"


def hex_to_rgb(value: str) -> Tuple[int, int, int]:
    value = normalize_hex(value).lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def tint(hex_color: str, amount: float) -> str:
    rgb = hex_to_rgb(hex_color)
    h, l, s = colorsys.rgb_to_hls(*(channel / 255 for channel in rgb))
    l = clamp(l + amount)
    out = colorsys.hls_to_rgb(h, l, s)
    return rgb_to_hex(tuple(round(channel * 255) for channel in out))


def shade(hex_color: str, amount: float) -> str:
    return tint(hex_color, -abs(amount))


def build_tokens(primary: str, base: int, grid: str, signage: bool) -> dict:
    primary = normalize_hex(primary)
    primary_rgb = hex_to_rgb(primary)
    cols, rows = GRID_LIBRARY.get(grid, GRID_LIBRARY["4x8"])
    return {
        "palette": {
            "primary": primary,
            "primary_light": tint(primary, 0.22),
            "primary_deep": shade(primary, 0.18),
            "ink": "#0A0A0A",
            "paper": "#F4F1EA",
            "white": "#FFFFFF",
            "signal_blue": "#0039A6",
            "signal_yellow": "#FFCC00",
        },
        "type_scale": {
            "base": base,
            "body": base,
            "heading": base * 2,
        },
        "grid": {
            "preset": grid,
            "columns": cols,
            "rows": rows,
            "tight_gutter": "1em",
        },
        "rules": {
            "major": "2px",
            "minor": "1px",
        },
        "signage": SIGNAGE_TABLE if signage else [],
        "primary_rgb": primary_rgb,
    }


def emit_css(tokens: dict) -> str:
    palette = tokens["palette"]
    scale = tokens["type_scale"]
    grid = tokens["grid"]
    rules = tokens["rules"]
    lines = [
        ":root {",
        f"  --v-primary: {palette['primary']};",
        f"  --v-primary-light: {palette['primary_light']};",
        f"  --v-primary-deep: {palette['primary_deep']};",
        f"  --v-ink: {palette['ink']};",
        f"  --v-paper: {palette['paper']};",
        f"  --v-white: {palette['white']};",
        f"  --v-signal-blue: {palette['signal_blue']};",
        f"  --v-signal-yellow: {palette['signal_yellow']};",
        f"  --v-base: {scale['base']}px;",
        f"  --v-body-size: {scale['body']}px;",
        f"  --v-heading-size: {scale['heading']}px;",
        f"  --v-grid-preset: '{grid['preset']}';",
        f"  --v-grid-columns: {grid['columns']};",
        f"  --v-grid-rows: {grid['rows']};",
        f"  --v-grid-gutter: {grid['tight_gutter']};",
        f"  --v-rule-major: {rules['major']};",
        f"  --v-rule-minor: {rules['minor']};",
        '  --v-face: "Liberation Sans", "Helvetica Neue", Helvetica, Arial, sans-serif;',
        "}",
    ]
    if tokens["signage"]:
        lines.append("")
        lines.append("/* Signage module: identification, directional, information */")
        for item in tokens["signage"]:
            lines.append(f"/* {item['level']}: {item['cap_height']} cap height, {item['panel']} panel */")
    return "\n".join(lines)


def emit_scss(tokens: dict) -> str:
    palette = tokens["palette"]
    scale = tokens["type_scale"]
    grid = tokens["grid"]
    rules = tokens["rules"]
    lines = [
        f"$v-primary: {palette['primary']};",
        f"$v-primary-light: {palette['primary_light']};",
        f"$v-primary-deep: {palette['primary_deep']};",
        f"$v-ink: {palette['ink']};",
        f"$v-paper: {palette['paper']};",
        f"$v-white: {palette['white']};",
        f"$v-signal-blue: {palette['signal_blue']};",
        f"$v-signal-yellow: {palette['signal_yellow']};",
        f"$v-base: {scale['base']}px;",
        f"$v-body-size: {scale['body']}px;",
        f"$v-heading-size: {scale['heading']}px;",
        f"$v-grid-preset: '{grid['preset']}';",
        f"$v-grid-columns: {grid['columns']};",
        f"$v-grid-rows: {grid['rows']};",
        f"$v-grid-gutter: {grid['tight_gutter']};",
        f"$v-rule-major: {rules['major']};",
        f"$v-rule-minor: {rules['minor']};",
    ]
    return "\n".join(lines)


def emit_json(tokens: dict) -> str:
    payload = {
        "palette": tokens["palette"],
        "type_scale": tokens["type_scale"],
        "grid": tokens["grid"],
        "rules": tokens["rules"],
        "signage": tokens["signage"],
    }
    return json.dumps(payload, indent=2, sort_keys=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Vignelli design tokens")
    parser.add_argument("--primary", default="#F04E23", help="Primary identifier color")
    parser.add_argument("--base", type=int, default=16, help="Base type size in px")
    parser.add_argument("--format", choices=["css", "scss", "json"], default="css")
    parser.add_argument("--grid", default="4x8", choices=sorted(GRID_LIBRARY.keys()))
    parser.add_argument("--signage", action="store_true", help="Include railway signage guidance")
    args = parser.parse_args()

    tokens = build_tokens(args.primary, args.base, args.grid, args.signage)
    if args.format == "css":
        print(emit_css(tokens))
    elif args.format == "scss":
        print(emit_scss(tokens))
    else:
        print(emit_json(tokens))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
