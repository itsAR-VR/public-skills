#!/usr/bin/env python3
"""classify_cluster.py — keyword-based intent cluster classifier.

Maps a free-text user prompt to one of the 18 intent clusters defined in
`cluster-taxonomy.json` from the public-skills-evals-private repo. Used by
`record_event.py` to populate the `intent_cluster` field on a Skill Oracle
preference event.

Algorithm: token-weighted overlap between the prompt and each cluster's
`name + description + example_prompts + anchor_skills`. The highest-scoring
cluster wins; if no cluster's overlap is meaningful, returns
`"catch-all"` (the schema-blessed fallback bucket).

This is intentionally simple — the v1 goal is to start the `n_human_picks`
counter growing. A higher-fidelity LLM-backed classifier can replace this
later without changing the event schema.

CLI:
    python3 classify_cluster.py --taxonomy /path/to/cluster-taxonomy.json \
        --prompt "write a cold email to a Series B founder"
    # -> marketing-content

Library:
    from classify_cluster import classify
    cluster_id = classify(prompt, taxonomy_path)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable

# Words that show up in many clusters; drop them so signal beats noise.
_STOPWORDS = frozenset({
    "a", "about", "all", "an", "and", "any", "are", "as", "at", "be", "build",
    "but", "by", "can", "code", "create", "design", "do", "does", "for", "from",
    "get", "has", "have", "help", "how", "i", "if", "in", "into", "is", "it",
    "its", "just", "let", "like", "make", "me", "my", "need", "new", "no",
    "not", "now", "of", "on", "one", "only", "or", "our", "out", "over",
    "please", "plus", "see", "set", "should", "so", "some", "than", "that",
    "the", "their", "them", "then", "there", "these", "they", "this", "those",
    "to", "too", "up", "us", "use", "using", "want", "was", "we", "what",
    "when", "where", "which", "while", "who", "why", "will", "with", "would",
    "you", "your",
})

# Anchor-skill matches are stronger evidence than description-word matches:
# they are the curated intent-to-skill mappings from cluster-taxonomy.json.
_ANCHOR_WEIGHT = 3.0
_EXAMPLE_WEIGHT = 2.0
_DESCRIPTION_WEIGHT = 1.0
_NAME_WEIGHT = 1.5
# Minimum score to escape the catch-all fallback. Empirically a single
# meaningful keyword hit (e.g., "email" -> marketing-content) should not
# trigger a confident routing, but two or more should.
_CONFIDENCE_FLOOR = 2.0

_WORD_RE = re.compile(r"[a-z0-9][a-z0-9_-]*")


def _tokens(text: str) -> list[str]:
    """Lowercase, strip punctuation, drop stopwords."""
    return [
        t for t in _WORD_RE.findall(text.lower())
        if t not in _STOPWORDS and len(t) > 1
    ]


def _score_cluster(prompt_tokens: set[str], cluster: dict) -> float:
    """Weighted overlap score between prompt tokens and a cluster's text."""
    if not prompt_tokens:
        return 0.0

    score = 0.0

    # Anchor skills: each token-hit weighted heavily.
    for anchor in cluster.get("anchor_skills", []) or []:
        anchor_tokens = set(_tokens(anchor))
        if anchor_tokens & prompt_tokens:
            score += _ANCHOR_WEIGHT * len(anchor_tokens & prompt_tokens)

    # Example prompts: medium weight.
    for example in cluster.get("example_prompts", []) or []:
        ex_tokens = set(_tokens(example))
        score += _EXAMPLE_WEIGHT * len(ex_tokens & prompt_tokens)

    # Name + description: lower weight, broader coverage.
    name_tokens = set(_tokens(cluster.get("name", "")))
    desc_tokens = set(_tokens(cluster.get("description", "")))
    score += _NAME_WEIGHT * len(name_tokens & prompt_tokens)
    score += _DESCRIPTION_WEIGHT * len(desc_tokens & prompt_tokens)

    return score


def _load_taxonomy(taxonomy_path: Path) -> dict:
    if not taxonomy_path.exists():
        raise FileNotFoundError(f"Taxonomy not found: {taxonomy_path}")
    with taxonomy_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def classify(prompt: str, taxonomy_path: Path | str) -> str:
    """Return the cluster `id` whose description best matches `prompt`.

    Falls back to the taxonomy's declared `fallback_cluster` (catch-all in v1)
    when no cluster scores above the confidence floor.
    """
    taxonomy_path = Path(taxonomy_path)
    taxonomy = _load_taxonomy(taxonomy_path)
    fallback = taxonomy.get("fallback_cluster", "catch-all")

    prompt_tokens = set(_tokens(prompt))
    if not prompt_tokens:
        return fallback

    best_id = fallback
    best_score = 0.0
    for cluster in taxonomy.get("clusters", []) or []:
        # Don't let the catch-all cluster "win" on the literal token "catch"
        # appearing in a prompt. It's a fallback bucket only.
        if cluster.get("id") == "catch-all":
            continue
        s = _score_cluster(prompt_tokens, cluster)
        if s > best_score:
            best_score = s
            best_id = cluster.get("id", fallback)

    if best_score < _CONFIDENCE_FLOOR:
        return fallback
    return best_id


def explain(prompt: str, taxonomy_path: Path | str) -> list[dict]:
    """Return per-cluster scores sorted descending. Useful for debugging."""
    taxonomy = _load_taxonomy(Path(taxonomy_path))
    prompt_tokens = set(_tokens(prompt))
    results = []
    for cluster in taxonomy.get("clusters", []) or []:
        results.append({
            "id": cluster.get("id"),
            "name": cluster.get("name"),
            "score": _score_cluster(prompt_tokens, cluster),
        })
    return sorted(results, key=lambda r: r["score"], reverse=True)


def _resolve_default_taxonomy() -> Path | None:
    """Best-effort: find cluster-taxonomy.json wherever the eval repo lives."""
    candidates: Iterable[Path] = (
        Path.home() / ".openclaw" / "public-skills-evals-private" / "cluster-taxonomy.json",
        Path.home() / "Desktop" / "Codespace" / "public-skills-evals-private" / "cluster-taxonomy.json",
        Path.home() / "Desktop" / "codespace" / "public-skills-evals-private" / "cluster-taxonomy.json",
    )
    for c in candidates:
        if c.exists():
            return c
    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--taxonomy",
        type=Path,
        default=None,
        help="Path to cluster-taxonomy.json (auto-detected if omitted).",
    )
    parser.add_argument(
        "--prompt",
        type=str,
        required=True,
        help="The user prompt to classify.",
    )
    parser.add_argument(
        "--explain",
        action="store_true",
        help="Print per-cluster scores instead of the winning cluster id.",
    )
    args = parser.parse_args(argv)

    taxonomy_path = args.taxonomy or _resolve_default_taxonomy()
    if not taxonomy_path or not taxonomy_path.exists():
        print(
            "classify_cluster: taxonomy not found; falling back to 'catch-all'",
            file=sys.stderr,
        )
        print("catch-all")
        return 0

    if args.explain:
        rows = explain(args.prompt, taxonomy_path)
        for r in rows:
            print(f"{r['score']:6.2f}  {r['id']:<28} {r['name']}")
        return 0

    print(classify(args.prompt, taxonomy_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
