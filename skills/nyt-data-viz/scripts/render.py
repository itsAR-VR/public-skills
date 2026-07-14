#!/usr/bin/env python3
"""Render a standalone NYT-style HTML page for a chart or dashboard."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from interactive import scaffold


def render_from_spec(spec: dict) -> str:
    title = spec.get("title", "NYT Data Visualization")
    body_html = spec.get("body_html", '<div id="chart" class="chart"></div>')
    extra_js = spec.get("extra_js", "")
    head_extra = spec.get("head_extra", "")
    return scaffold(title, body_html, extra_js=extra_js, head_extra=head_extra)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a standalone NYT-style HTML page")
    parser.add_argument("spec", help="Path to JSON spec")
    parser.add_argument("--out", help="Output HTML path")
    args = parser.parse_args()

    spec_path = Path(args.spec)
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    html = render_from_spec(spec)

    output = Path(args.out) if args.out else Path(spec.get("output") or spec_path.with_suffix(".html"))
    if not output.is_absolute():
        output = (spec_path.parent / output).resolve()
    output.write_text(html, encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
