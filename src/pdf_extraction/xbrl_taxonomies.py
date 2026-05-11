"""Authoritative XBRL element-name sets, loaded from data/taxonomies/*.txt.

Used to validate the `concept` field emitted by the LLM on each fact, so we can
flag plausible-but-fabricated tags rather than trusting whatever the model
produced. The .txt files are built by scripts/fetch_taxonomies.py from real
SEC filings — see data/taxonomies/README.md for provenance.

Validation semantics (see ``is_valid_concept``):
    True   — namespace is one we ship a list for, and the tag is in the list.
    False  — namespace is one we ship a list for, but the tag is NOT in the
             list (a likely hallucination, worth flagging downstream).
    None   — namespace is not validated here (e.g. ``custom:*``, or a
             namespace we don't currently track). Treat as "unknown".
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

TAXONOMIES_DIR = Path(__file__).resolve().parents[2] / "data" / "taxonomies"
CONCEPT_MAP_PATH = TAXONOMIES_DIR / "concept_canonical_map.json"

# Namespaces for which we ship an authoritative tag list. The keys are the
# namespace prefix as it appears in `concept` strings (e.g. "us-gaap:Foo").
KNOWN_NAMESPACES: frozenset[str] = frozenset({"us-gaap", "ifrs-full", "dei"})

# Some filers (and LLMs) use ``ifrs:Revenue`` as shorthand for
# ``ifrs-full:Revenue``. Treat both as the same namespace for validation.
NAMESPACE_ALIASES: dict[str, str] = {"ifrs": "ifrs-full"}


@lru_cache(maxsize=None)
def load_tag_set(namespace: str) -> frozenset[str]:
    """Return the set of element names for ``namespace`` (e.g. 'us-gaap').

    Returns an empty frozenset if the corresponding file is missing — callers
    can then treat the namespace as "not validated" rather than crashing.
    """
    path = TAXONOMIES_DIR / f"{namespace}.txt"
    if not path.exists():
        return frozenset()
    return frozenset(
        line.strip() for line in path.read_text().splitlines() if line.strip()
    )


def split_concept(concept: str) -> tuple[str, str] | None:
    """Split a 'namespace:Name' string. Returns None if it isn't of that form."""
    if not concept or ":" not in concept:
        return None
    ns, name = concept.split(":", 1)
    return ns, name


def is_valid_concept(concept: str) -> bool | None:
    """Check whether ``concept`` is in the authoritative list for its namespace.

    Args:
        concept: A string like ``"us-gaap:Revenues"`` or ``"custom:SegmentX"``.

    Returns:
        True  if the namespace is tracked and the name is in the list.
        False if the namespace is tracked and the name is NOT in the list.
        None  if the namespace is not tracked (custom:*, unrecognized ns,
              or a string that isn't of the form ``ns:Name``).
    """
    parts = split_concept(concept)
    if parts is None:
        return None
    ns, name = parts
    if ns == "custom":
        return None  # company-specific tags are free-form by design
    ns = NAMESPACE_ALIASES.get(ns, ns)
    if ns not in KNOWN_NAMESPACES:
        return None
    return name in load_tag_set(ns)


def validate_concepts(facts: list[dict]) -> tuple[int, list[str]]:
    """Count facts whose `concept` is in a tracked namespace but unknown there.

    Args:
        facts: The list from ``data["facts"]``.

    Returns:
        (invalid_count, sample_invalid_concepts)
        ``sample_invalid_concepts`` is a sorted, de-duplicated list — useful
        for surfacing what went wrong without spamming the log.
    """
    invalid_count = 0
    invalid_samples: set[str] = set()
    for fact in facts:
        concept = fact.get("concept")
        if is_valid_concept(concept) is False:
            invalid_count += 1
            invalid_samples.add(concept)
    return invalid_count, sorted(invalid_samples)


# ============================================================================
# Static concept → canonical map
# ============================================================================
#
# A deterministic lookup table built once (by scripts/build_concept_map.py)
# that records, for each XBRL element name in our authoritative tag lists,
# the canonical name from taxonomy.py it should map to (or null). When the
# extractor produces a fact whose `concept` is in this map, we override the
# LLM's canonical with the map's answer — making the mapping consistent
# across runs and removing per-extraction re-derivation. See data/taxonomies/
# concept_canonical_map.md for the human-readable table.


@lru_cache(maxsize=1)
def _load_concept_map() -> dict[str, dict[str, dict]]:
    """Load the static concept-canonical map. Returns {} if the file is absent or malformed."""
    if not CONCEPT_MAP_PATH.exists():
        return {}
    try:
        return json.loads(CONCEPT_MAP_PATH.read_text())
    except (json.JSONDecodeError, OSError):
        return {}


def concept_in_map(concept: str | None) -> bool:
    """Whether the static map has an opinion about this concept.

    True means the namespace + tag are present (whether mapped to a canonical
    or explicitly to null). False means the concept isn't covered and we
    should defer to the LLM.
    """
    parts = split_concept(concept)
    if parts is None:
        return False
    ns, name = parts
    if ns == "custom":
        return False  # custom tags are never in the map by design
    ns = NAMESPACE_ALIASES.get(ns, ns)
    cmap = _load_concept_map()
    return ns in cmap and name in cmap[ns]


def lookup_canonical_in_map(concept: str | None) -> str | None:
    """The canonical the static map assigns to this concept.

    Returns None if the concept maps to null OR is not in the map.
    Pair with ``concept_in_map`` to distinguish those two cases.
    """
    parts = split_concept(concept)
    if parts is None:
        return None
    ns, name = parts
    ns = NAMESPACE_ALIASES.get(ns, ns)
    cmap = _load_concept_map()
    return cmap.get(ns, {}).get(name, {}).get("canonical")


def apply_concept_map(
    facts: list[dict],
) -> tuple[int, list[tuple[str, str | None, str | None]]]:
    """Apply the static concept→canonical map to ``facts`` in place.

    For each fact whose ``concept`` is in the static map, sets the fact's
    ``canonical`` to the map's value (overriding whatever the LLM said).

    Returns ``(n_facts_touched, disagreements)`` where ``disagreements`` lists
    ``(concept, llm_canonical, map_canonical)`` tuples for cases the LLM
    didn't already agree with — useful for surfacing the signal that the
    LLM and the map are diverging on certain tags.

    If the map file is absent, this function returns ``(0, [])`` and leaves
    every fact unchanged. The system continues to work without it.
    """
    if not _load_concept_map():
        return 0, []
    touched = 0
    disagreements: list[tuple[str, str | None, str | None]] = []
    for fact in facts:
        concept = fact.get("concept")
        if not concept_in_map(concept):
            continue
        map_canonical = lookup_canonical_in_map(concept)
        llm_canonical = fact.get("canonical")
        if llm_canonical != map_canonical:
            disagreements.append((concept, llm_canonical, map_canonical))
        fact["canonical"] = map_canonical
        touched += 1
    return touched, disagreements
