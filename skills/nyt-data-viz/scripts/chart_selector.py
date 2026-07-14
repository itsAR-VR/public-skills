#!/usr/bin/env python3
"""Small chart-choice heuristics for NYT-style visualizations."""

from __future__ import annotations


def recommend_chart(
    kind: str = "comparison",
    series_count: int = 1,
    time_series: bool = False,
    diverging: bool = False,
    categorical_count: int = 0,
) -> str:
    kind = (kind or "").lower()
    if time_series or kind in {"time", "trend", "temporal"}:
        return "line"
    if kind in {"distribution", "spread", "density"}:
        return "beeswarm"
    if kind in {"ranking", "rank", "leaderboard"}:
        return "bump"
    if series_count > 5 or categorical_count > 7:
        return "small multiples"
    if diverging:
        return "diverging bar"
    return "bar"


def validate_choice(choice: str, *, time_series: bool = False, series_count: int = 1) -> list[str]:
    warnings: list[str] = []
    choice = (choice or "").lower()
    if choice == "pie":
        warnings.append("Avoid pie charts; use bar or line instead.")
    if choice == "dual y-axis":
        warnings.append("Avoid dual y-axes; split into small multiples.")
    if choice == "connected scatter" and not time_series:
        warnings.append("Connected scatter needs monotonic axes.")
    if series_count > 5 and choice not in {"small multiples", "bump"}:
        warnings.append("Past five series, consider small multiples.")
    return warnings

