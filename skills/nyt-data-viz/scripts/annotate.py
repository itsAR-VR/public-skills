#!/usr/bin/env python3
"""Annotation helpers for NYT-style pages."""

from __future__ import annotations

from html import escape


HALO_CSS = (
    ".anno,.anno-sub,.headline,.source{paint-order:stroke fill;"
    "stroke:var(--panel,#f4f1ea);stroke-width:3px;stroke-linejoin:round;}"
)


def headline(title: str, subtitle: str = "", source: str = "") -> str:
    parts = [f'<div class="headline">{escape(title)}</div>']
    if subtitle:
        parts.append(f'<div class="subtitle">{escape(subtitle)}</div>')
    if source:
        parts.append(f'<div class="source">{escape(source)}</div>')
    return "\n".join(parts)


def source_line(source: str) -> str:
    return f'<div class="source">{escape(source)}</div>'


def endpoint_label(text: str, x: float | int | None = None, y: float | int | None = None, align: str = "start") -> str:
    attrs = []
    if x is not None:
        attrs.append(f'data-x="{x}"')
    if y is not None:
        attrs.append(f'data-y="{y}"')
    attrs.append(f'data-align="{escape(align)}"')
    return f'<div class="anno" {" ".join(attrs)}>{escape(text)}</div>'


def note(text: str) -> str:
    return f'<div class="anno-sub">{escape(text)}</div>'

