#!/usr/bin/env python3
"""NYT chrome + interaction primitives for D3 dashboards."""

from __future__ import annotations

from html import escape

from typography import font_links, css_vars, headline_css, numeric_css
from annotate import HALO_CSS


INTERACTIVE_CSS = """
:root{
  --panel:#f4f1ea;
  --ink:#111111;
  --muted:#5b5b57;
  --line:#1111111f;
  --hero:#1f4d7a;
  --paper:#f4f1ea;
}
body{
  margin:0;
  background:var(--panel);
  color:var(--ink);
  font-family:var(--nyt-sans);
}
.page{
  max-width:1240px;
  margin:0 auto;
  padding:28px 22px 64px;
}
.chart-shell{
  position:relative;
  background:linear-gradient(180deg,#fff,rgba(255,255,255,.82));
  border:1px solid var(--line);
  border-radius:24px;
  padding:18px;
  box-shadow:0 18px 50px rgba(0,0,0,.06);
}
.chart{position:relative}
.tooltip{
  position:fixed;
  opacity:0;
  transform:translate(-50%,calc(-100% - 12px));
  transition:opacity 140ms ease,left 200ms cubic-bezier(.22,.61,.36,1),top 200ms cubic-bezier(.22,.61,.36,1);
  pointer-events:none;
  z-index:1000;
  background:#111;
  color:#fff;
  padding:10px 12px;
  border-radius:12px;
  font-family:var(--nyt-sans);
  font-size:13px;
  line-height:1.35;
  max-width:280px;
}
.tooltip .kicker{font-family:var(--nyt-mono);font-size:10px;letter-spacing:.18em;text-transform:uppercase;opacity:.72}
.axis text,.tick text{font-family:var(--nyt-sans);fill:var(--muted)}
.grid line{stroke:var(--line)}
.series-label{font-family:var(--nyt-sans);font-size:13px;font-weight:600}
""" + headline_css() + numeric_css() + HALO_CSS


HELPER_JS = """
function tipAtNode(node, html){
  const tip = window.__nytTip || (window.__nytTip = document.querySelector('.tooltip'));
  if(!tip || !node) return;
  const r = node.getBoundingClientRect();
  tip.innerHTML = html;
  tip.style.left = (r.left + r.width / 2) + 'px';
  tip.style.top = r.top + 'px';
  tip.style.opacity = 1;
}

function hideTip(){
  const tip = window.__nytTip || document.querySelector('.tooltip');
  if (tip) tip.style.opacity = 0;
}

function voronoiHover(g, pts, nodes, w, h, onEnter, onLeave){
  const del = d3.Delaunay.from(pts, p => p[0], p => p[1]);
  g.append('rect')
    .attr('width', w)
    .attr('height', h)
    .attr('fill', 'transparent')
    .on('mousemove', function(ev){
      const p = d3.pointer(ev, this);
      const i = del.find(p[0], p[1]);
      const datum = pts[i][2];
      onEnter(datum, i, nodes ? nodes[i] : null, p);
    })
    .on('mouseleave', function(){ onLeave(); });
}
"""

PREPUBLISH_CHECKLIST = """
1. Domain from `d3.max` covers the max.
2. Hover overlay lives in the same translated `<g>` as the marks.
3. Delaunay or equivalent proximity hover is present.
4. Tooltip is anchored and gliding, not teleporting.
5. Annotation text has a halo and any trough labels have a leader line.
6. Connected scatter is used only when both axes are monotonic.
7. Extract inline JS and run a syntax check before publishing.
8. Screenshot desktop and mobile widths before shipping.
9. Cut editorial text to half the first-draft instinct.
"""


def scaffold(title: str, body_html: str, extra_js: str = "", head_extra: str = "") -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
{font_links()}
<script src="https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@observablehq/plot@0.6/dist/plot.umd.min.js"></script>
<style>
{css_vars()}
{INTERACTIVE_CSS}
</style>
{head_extra}
</head>
<body>
<div class="page">
  <div class="chart-shell">
    {body_html}
    <div class="tooltip"></div>
  </div>
</div>
<script>
{HELPER_JS}
{extra_js}
</script>
</body>
</html>"""

