#!/usr/bin/env python3
"""Typography helpers for NYT-grade chart pages."""

from __future__ import annotations


DISPLAY_STACK = '"Playfair Display", "Iowan Old Style", "Palatino Linotype", Palatino, serif'
SANS_STACK = '"Libre Franklin", "Helvetica Neue", Helvetica, Arial, sans-serif'
BODY_STACK = '"Source Serif 4", "Iowan Old Style", Georgia, serif'
MONO_STACK = '"JetBrains Mono", "SFMono-Regular", Consolas, "Liberation Mono", monospace'


def font_links() -> str:
    return (
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Libre+Franklin:wght@400;500;600;700&family=Source+Serif+4:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">'
    )


def css_vars() -> str:
    return (
        ":root{"
        f"--nyt-display:{DISPLAY_STACK};"
        f"--nyt-sans:{SANS_STACK};"
        f"--nyt-body:{BODY_STACK};"
        f"--nyt-mono:{MONO_STACK};"
        "}"
    )


def tabular_nums_css() -> str:
    return "font-variant-numeric: tabular-nums lining-nums;"


def headline_css() -> str:
    return (
        ".headline{font-family:var(--nyt-display);font-weight:700;line-height:1.05;letter-spacing:-.02em;}"
        ".subtitle,.source,.axis,.tick{font-family:var(--nyt-sans);}"
        ".bodycopy{font-family:var(--nyt-body);line-height:1.55;}"
    )


def numeric_css() -> str:
    return f".num{{{tabular_nums_css()}}}"

