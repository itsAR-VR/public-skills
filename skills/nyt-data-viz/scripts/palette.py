#!/usr/bin/env python3
"""NYT-style palette helpers."""

from __future__ import annotations

from typing import Sequence


NYT_GREYS = [
    "#111111",
    "#3A3A3A",
    "#6B6B6B",
    "#9A9A9A",
    "#C8C8C8",
    "#E5E5E5",
    "#F3F3F3",
]

NYT_HERO = "#1F4D7A"
NYT_ACCENT = "#D94E1F"
NYT_DIVIDING = "#C8C3B7"
NYT_CHASE = NYT_GREYS[3]


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.strip().lstrip("#")
    if len(value) == 3:
        value = "".join(ch * 2 for ch in value)
    if len(value) != 6:
        raise ValueError(f"Expected hex color, got {value!r}")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb: Sequence[int]) -> str:
    return "#{:02X}{:02X}{:02X}".format(*rgb[:3])


def mix(a: str, b: str, t: float) -> str:
    ar, ag, ab = hex_to_rgb(a)
    br, bg, bb = hex_to_rgb(b)
    return rgb_to_hex((
        round(ar + (br - ar) * clamp(t)),
        round(ag + (bg - ag) * clamp(t)),
        round(ab + (bb - ab) * clamp(t)),
    ))


def sequential_scale(hero: str = NYT_HERO, steps: int = 5) -> list[str]:
    steps = max(2, steps)
    ramp = []
    for index in range(steps):
        t = index / max(1, steps - 1)
        # lightest near paper, darkest at the hero color
        ramp.append(mix("#F4F1EA", hero, t))
    return ramp


def diverging_scale(left: str, right: str, steps: int = 5, midpoint: str = "#F4F1EA") -> list[str]:
    steps = max(3, steps)
    left_count = steps // 2
    right_count = steps - left_count - 1
    scale = [mix(left, midpoint, i / max(1, left_count)) for i in range(left_count)]
    scale.append(midpoint)
    scale.extend(mix(midpoint, right, i / max(1, right_count)) for i in range(1, right_count + 1))
    return scale


def categorical_palette(count: int = 7) -> list[str]:
    base = [
        NYT_HERO,
        NYT_ACCENT,
        "#2C6E49",
        "#7C5CDB",
        "#B56A00",
        "#4E72B8",
        "#8C4B5D",
    ]
    if count <= len(base):
        return base[:count]
    out = list(base)
    while len(out) < count:
        out.append(mix(base[len(out) % len(base)], "#FFFFFF", 0.35))
    return out


def hero_rule(index: int = 0, total: int = 1, hero_index: int = 0) -> str:
    """Pick the hero series and keep everything else grey."""
    total = max(1, total)
    if index < 0 or index >= total:
        raise ValueError("index out of range")
    if hero_index < 0 or hero_index >= total:
        raise ValueError("hero_index out of range")
    return NYT_HERO if index == hero_index else NYT_CHASE
