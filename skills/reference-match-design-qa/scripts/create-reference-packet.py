#!/usr/bin/env python3
"""Create a design packet markdown file from the bundled templates."""
from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True, help="Target route, screen, or component")
    parser.add_argument("--product", required=True, help="Product or repo name")
    parser.add_argument("--mode", default="reference", choices=["reference", "no-reference"])
    parser.add_argument("--reference", help="Screenshot path, Figma link, URL, or reference name")
    parser.add_argument("--match-level", default="close", choices=["exact", "close", "inspired", "pattern-only"])
    parser.add_argument("--product-type", help="Product/build type from the universal pattern library")
    parser.add_argument("--direction-id", help="No-reference direction id")
    parser.add_argument("--source-recipe", help="Source recipe for the product type/direction")
    parser.add_argument("--critical-states", help="Comma-separated critical states to prove")
    parser.add_argument("--proof-focus", help="Desktop/mobile/state/flow proof focus")
    parser.add_argument("--out", required=True, help="Output markdown path")
    args = parser.parse_args()

    skill_dir = Path(__file__).resolve().parent.parent
    if args.mode == "reference" and not args.reference:
        parser.error("--reference is required when --mode reference")

    template_name = "reference-packet.md" if args.mode == "reference" else "no-reference-design-packet.md"
    template = skill_dir / "templates" / template_name
    body = template.read_text(encoding="utf-8")
    body = body.replace("- Target surface:", f"- Target surface: {args.target}")
    body = body.replace("- Product/repo:", f"- Product/repo: {args.product}")
    if args.reference:
        body = body.replace("- Source reference:", f"- Source reference: {args.reference}")
    body = body.replace("- Match level: exact / close / inspired / pattern-only", f"- Match level: {args.match_level}")
    if args.product_type:
        body = body.replace(
            "- Product type: SaaS app / internal tool / AI product / landing page / onboarding / dashboard / ecommerce / calendar / editor / canvas / support / mobile-style app / other",
            f"- Product type: {args.product_type}",
        )
    if args.direction_id:
        body = body.replace("- direction_id:", f"- direction_id: {args.direction_id}")
    if args.source_recipe:
        body = body.replace("- source_recipe:", f"- source_recipe: {args.source_recipe}")
    if args.critical_states:
        body = body.replace("- critical_states_first:", f"- critical_states_first: {args.critical_states}")
        body = body.replace("- Required state screenshots or notes:", f"- Required state screenshots or notes: {args.critical_states}")
    if args.proof_focus:
        body = body.replace("- proof_method:", f"- proof_method: {args.proof_focus}")
        body = body.replace("- Visual review notes required:", f"- Visual review notes required: {args.proof_focus}")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
