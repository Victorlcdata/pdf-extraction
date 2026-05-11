"""Phase-3 learning analyzer.

Reads observations.jsonl (the per-fact log accumulated by every successful
extraction) and produces taxonomy_proposals.md — a human-reviewable report
with three sections:

  1. Proposed canonicals — clusters of facts with ``canonical: null`` that
     recur often enough to deserve a canonical entry. The analyzer proposes a
     CamelCase name and the evidence; a human accepts/edits and adds it to
     taxonomy.py.
  2. Mapping inconsistencies — the same ``concept`` mapped to different
     ``canonical`` values across facts. Some are legitimate (e.g. the same
     XBRL tag at beginning vs end of period); others reveal LLM indecision.
  3. Likely hallucinated tags — the most frequent ``concept_valid: false``
     entries, ranked by occurrence. These are tags the LLM is inventing in
     namespaces (us-gaap, ifrs-full, dei) where we have an authoritative
     list, so they're false by definition.

The canonical taxonomy never auto-mutates from this output. A human always
reads the proposals and decides what to add.

Run with:
    learn-taxonomy                                  # default paths
    learn-taxonomy --obs-file path/to/observations.jsonl
    learn-taxonomy --min-frequency 3 --out path/to/proposals.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

DEFAULT_OBS = Path("data/output/observations.jsonl")
DEFAULT_OUT = Path("data/output/taxonomy_proposals.md")


def normalize_label(label: str | None) -> str:
    """Collapse whitespace, lowercase, strip — for grouping similar labels."""
    if not label:
        return ""
    return re.sub(r"\s+", " ", label.strip().lower())


def camel_case_from_concept(concept: str | None) -> str:
    """Suggest a CamelCase canonical name from a ``ns:LocalName`` concept.

    The local name in XBRL is already CamelCase in most cases, so we just
    strip the namespace. For ``custom:`` tags we use the local name unchanged.
    """
    if not concept or ":" not in concept:
        return "TODO"
    return concept.split(":", 1)[1]


def load_observations(path: Path) -> list[dict]:
    """Read all observations from a JSONL file. Silently skips blank lines."""
    if not path.exists():
        sys.exit(f"ERROR: observations file not found: {path}")
    out = []
    for ln in path.read_text().splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            out.append(json.loads(ln))
        except json.JSONDecodeError as e:
            print(f"  [WARN] bad observation line: {e}", file=sys.stderr)
    return out


def cluster_null_canonicals(
    observations: list[dict], min_frequency: int
) -> list[dict]:
    """Group ``canonical: null`` facts by concept and report frequent clusters.

    Each cluster is one ``(concept,)`` group whose total fact count >= the
    threshold. Within a cluster we also surface the distinct labels seen and
    how many filings (distinct ``pdf`` values) contributed.
    """
    by_concept: dict[str, list[dict]] = defaultdict(list)
    for obs in observations:
        if obs.get("canonical") is not None:
            continue
        concept = obs.get("concept") or ""
        if not concept:
            continue
        by_concept[concept].append(obs)

    proposals: list[dict] = []
    for concept, facts in by_concept.items():
        if len(facts) < min_frequency:
            continue
        label_counts = Counter(normalize_label(f.get("label")) for f in facts)
        # Use the most common original-case label as the display label for each cluster
        original_labels: dict[str, Counter] = defaultdict(Counter)
        for f in facts:
            norm = normalize_label(f.get("label"))
            original_labels[norm][f.get("label") or ""] += 1
        labels_display = [
            (original_labels[norm].most_common(1)[0][0], count)
            for norm, count in label_counts.most_common()
        ]
        statements = Counter(f.get("statement") or "?" for f in facts)
        pdfs = {f.get("pdf") for f in facts}
        proposals.append(
            {
                "concept": concept,
                "fact_count": len(facts),
                "pdf_count": len(pdfs),
                "labels": labels_display,
                "statements": statements.most_common(),
                "suggested_name": camel_case_from_concept(concept),
            }
        )
    proposals.sort(key=lambda p: (-p["fact_count"], p["concept"]))
    return proposals


def find_inconsistencies(observations: list[dict]) -> list[dict]:
    """Concepts mapped to >1 distinct non-null canonical across the corpus."""
    by_concept: dict[str, Counter] = defaultdict(Counter)
    for obs in observations:
        concept = obs.get("concept")
        canonical = obs.get("canonical")
        if not concept or canonical is None:
            continue
        by_concept[concept][canonical] += 1

    items: list[dict] = []
    for concept, canon_counter in by_concept.items():
        if len(canon_counter) < 2:
            continue
        items.append(
            {
                "concept": concept,
                "canonicals": canon_counter.most_common(),
                "total_facts": sum(canon_counter.values()),
            }
        )
    items.sort(key=lambda x: -x["total_facts"])
    return items


def find_hallucinated_tags(observations: list[dict], top_n: int = 30) -> list[tuple[str, int]]:
    """Top-N concepts where ``concept_valid is False`` — namespace tracked but tag missing."""
    counter: Counter = Counter()
    for obs in observations:
        if obs.get("concept_valid") is False:
            counter[obs.get("concept") or ""] += 1
    return counter.most_common(top_n)


# ============================================================================
# Markdown rendering
# ============================================================================


def render_report(
    proposals: list[dict],
    inconsistencies: list[dict],
    hallucinations: list[tuple[str, int]],
    *,
    obs_path: Path,
    n_observations: int,
    min_frequency: int,
) -> str:
    lines: list[str] = []
    lines.append("# Taxonomy proposals (Phase-3 learning report)\n")
    lines.append(
        f"Generated from `{obs_path}` — {n_observations:,} observations, "
        f"min-frequency = {min_frequency}.\n"
    )
    lines.append(
        "> This file is *advisory*. Nothing here is applied automatically. "
        "Review each section, decide what to act on, and edit "
        "[`src/pdf_extraction/taxonomy.py`](../../src/pdf_extraction/taxonomy.py) "
        "or [`data/taxonomies/`](../taxonomies/) by hand.\n"
    )

    # 1. Proposed canonicals
    lines.append("## 1. Proposed canonicals\n")
    if not proposals:
        lines.append("_None at the current threshold._\n")
    else:
        lines.append(
            f"Concepts with `canonical: null` seen ≥ {min_frequency} times. "
            "Each block proposes a CamelCase name (derived from the concept's "
            "local part) and the evidence. Add the ones you accept to `TAXONOMY` "
            "in `taxonomy.py`.\n"
        )
        for p in proposals:
            lines.append(f"### `{p['suggested_name']}`  *(suggested)*\n")
            lines.append(f"- **Source concept**: `{p['concept']}`")
            lines.append(
                f"- **Evidence**: {p['fact_count']} fact(s) across {p['pdf_count']} filing(s)"
            )
            stmt_str = ", ".join(f"`{s}` ({n})" for s, n in p["statements"])
            lines.append(f"- **Statements**: {stmt_str}")
            lines.append("- **Labels seen**:")
            for label, count in p["labels"][:6]:
                truncated = label if len(label) <= 90 else label[:87] + "…"
                lines.append(f"    - {truncated!r} ×{count}")
            if len(p["labels"]) > 6:
                lines.append(f"    - … and {len(p['labels']) - 6} more")
            lines.append("")
            lines.append("```python")
            lines.append(
                f'    "{p["suggested_name"]}": "TODO — describe this concept",'
            )
            lines.append("```\n")

    # 2. Inconsistencies
    lines.append("## 2. Mapping inconsistencies\n")
    if not inconsistencies:
        lines.append("_None — every concept maps to a single canonical (or to `null`)._\n")
    else:
        lines.append(
            "The same `concept` was mapped to more than one canonical name. "
            "Some of these are legitimate (e.g. the same XBRL tag legitimately "
            "covers two different canonicals at beginning vs end of period) — "
            "others reveal LLM indecision worth investigating.\n"
        )
        lines.append("| Concept | Canonicals (count) | Total facts |")
        lines.append("|---|---|---|")
        for item in inconsistencies:
            canon_str = ", ".join(
                f"`{c or 'null'}` ({n})" for c, n in item["canonicals"]
            )
            lines.append(f"| `{item['concept']}` | {canon_str} | {item['total_facts']} |")
        lines.append("")

    # 3. Hallucinated tags
    lines.append("## 3. Likely hallucinated XBRL tags\n")
    if not hallucinations:
        lines.append(
            "_None — every emitted concept in a tracked namespace was found in the authoritative list._\n"
        )
    else:
        lines.append(
            "Concepts where `concept_valid` is `false` — i.e. the namespace is tracked "
            "(`us-gaap`, `ifrs-full`, `dei`) but the tag is NOT in the authoritative list "
            "at `data/taxonomies/`. These are LLM inventions. Either the tag really doesn't "
            "exist (and the LLM should have used `custom:*`), or it's a real tag that's "
            "missing from our seed-filer union — extend `scripts/fetch_taxonomies.py` and "
            "re-run if so.\n"
        )
        lines.append("| Hallucinated concept | Count |")
        lines.append("|---|---|")
        for concept, n in hallucinations:
            lines.append(f"| `{concept}` | {n} |")
        lines.append("")

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="learn-taxonomy",
        description=(
            "Analyze observations.jsonl and write taxonomy_proposals.md — "
            "human-reviewable suggestions for new canonicals, mapping "
            "inconsistencies, and likely LLM-hallucinated XBRL tags."
        ),
    )
    parser.add_argument(
        "--obs-file",
        type=Path,
        default=DEFAULT_OBS,
        help=f"Path to observations.jsonl (default: {DEFAULT_OBS})",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT,
        help=f"Path to write the proposals markdown (default: {DEFAULT_OUT})",
    )
    parser.add_argument(
        "--min-frequency",
        type=int,
        default=2,
        help="Minimum count for a null-canonical cluster to be proposed (default: 2)",
    )
    parser.add_argument(
        "--top-hallucinations",
        type=int,
        default=30,
        help="Number of hallucinated tags to list (default: 30)",
    )
    args = parser.parse_args()

    obs = load_observations(args.obs_file)
    print(f"Loaded {len(obs):,} observations from {args.obs_file}")

    proposals = cluster_null_canonicals(obs, min_frequency=args.min_frequency)
    inconsistencies = find_inconsistencies(obs)
    hallucinations = find_hallucinated_tags(obs, top_n=args.top_hallucinations)

    print(
        f"  proposals:        {len(proposals):>4} (concepts with null canonical "
        f"≥ {args.min_frequency}×)"
    )
    print(f"  inconsistencies:  {len(inconsistencies):>4} (concept → multiple canonicals)")
    print(f"  hallucinated tags:{len(hallucinations):>4} (concept_valid is false)")

    report = render_report(
        proposals,
        inconsistencies,
        hallucinations,
        obs_path=args.obs_file,
        n_observations=len(obs),
        min_frequency=args.min_frequency,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(report)
    print(f"  wrote {args.out}")


if __name__ == "__main__":
    main()
