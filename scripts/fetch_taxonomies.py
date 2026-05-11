"""Fetch authoritative XBRL concept names from SEC EDGAR's companyfacts API.

Why this script exists
----------------------
The pdf-extraction LLM is told to emit a `concept` tag like `us-gaap:Revenues`
or `ifrs-full:Revenue` for every fact. Without an authoritative tag list to
validate against, the LLM can invent plausible-but-nonexistent tags.

This script builds that authoritative list by unioning the concept names that
real filers have actually used in their SEC XBRL submissions. The result is
*not* the full theoretical taxonomy (us-gaap alone has ~15k concepts, most
unused) — it's the empirically-observed working subset, which is what we
actually need for validation.

How it works
------------
The SEC EDGAR /api/xbrl/companyfacts/CIK<10-digit>.json endpoint returns every
concept a given filer has reported, grouped by namespace (us-gaap, ifrs-full,
dei, srt, ...). We fetch a diverse seed set of filers — different sectors,
different accounting standards — union the concepts per namespace, and emit
one plain-text file per namespace plus a provenance record.

Re-run any time to refresh. The endpoint is free and requires no API key, only
a descriptive User-Agent (SEC policy).

Outputs (under data/taxonomies/)
--------------------------------
    us-gaap.txt        one element name per line, sorted
    ifrs-full.txt      same, for IFRS filers
    dei.txt            same, for Document Entity Information tags
    _provenance.json   which CIKs contributed, counts per namespace
"""

from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

# SEC requires a descriptive User-Agent identifying the requester.
# See https://www.sec.gov/os/accessing-edgar-data
USER_AGENT = "pdf-extraction taxonomy-fetcher (victor.lc@omaha-insights.com)"

# Seed set of filers chosen for *sector breadth*, so the unioned concept list
# covers tags from tech, finance, pharma, energy, retail, industrial, etc.
# CIKs are 10-digit zero-padded as required by the endpoint.
US_GAAP_FILERS: list[tuple[str, str]] = [
    ("0000320193", "Apple — tech"),
    ("0000789019", "Microsoft — tech/cloud"),
    ("0001318605", "Tesla — auto"),
    ("0000019617", "JPMorgan Chase — bank"),
    ("0000886982", "Goldman Sachs — investment bank"),
    ("0001067983", "Berkshire Hathaway — conglomerate/insurance"),
    ("0000078003", "Pfizer — pharma"),
    ("0000034088", "ExxonMobil — oil & gas"),
    ("0000080424", "Procter & Gamble — consumer goods"),
    ("0000104169", "Walmart — retail"),
    ("0000012927", "Boeing — aerospace/defense"),
    ("0001403161", "Visa — payments"),
    ("0001018724", "Amazon — retail/cloud"),
]

IFRS_FILERS: list[tuple[str, str]] = [
    ("0001114448", "Novartis — pharma (IFRS)"),
    ("0000901832", "AstraZeneca — pharma (IFRS)"),
    ("0001121404", "Sanofi — pharma (IFRS)"),
]

CACHE_DIR = Path("/tmp/sec_facts_cache")
OUT_DIR = Path(__file__).resolve().parent.parent / "data" / "taxonomies"


def fetch_companyfacts(cik: str) -> dict:
    """Fetch SEC companyfacts JSON for one CIK. Caches under /tmp to avoid re-hitting."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache = CACHE_DIR / f"{cik}.json"
    if cache.exists():
        return json.loads(cache.read_text())

    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())
    cache.write_text(json.dumps(data))
    time.sleep(0.15)  # be polite — SEC rate-limits at ~10 req/s
    return data


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    per_namespace: dict[str, set[str]] = {}
    provenance: dict[str, dict] = {}

    print(f"Fetching {len(US_GAAP_FILERS) + len(IFRS_FILERS)} filers from SEC EDGAR...")
    for cik, label in US_GAAP_FILERS + IFRS_FILERS:
        try:
            data = fetch_companyfacts(cik)
        except urllib.error.HTTPError as e:
            print(f"  [WARN] CIK {cik} ({label}): HTTP {e.code} — skipping", file=sys.stderr)
            continue
        except Exception as e:
            print(f"  [WARN] CIK {cik} ({label}): {e} — skipping", file=sys.stderr)
            continue

        entity = data.get("entityName", "?")
        facts = data.get("facts", {})
        ns_counts: dict[str, int] = {}
        for ns, concepts in facts.items():
            per_namespace.setdefault(ns, set()).update(concepts.keys())
            ns_counts[ns] = len(concepts)
        provenance[cik] = {"label": label, "entity": entity, "counts": ns_counts}
        print(f"  {cik} {entity} → {ns_counts}")

    print()
    for ns in ("us-gaap", "ifrs-full", "dei"):
        tags = sorted(per_namespace.get(ns, ()))
        if not tags:
            print(f"  [skip] {ns}: no concepts collected")
            continue
        out = OUT_DIR / f"{ns}.txt"
        out.write_text("\n".join(tags) + "\n")
        print(f"  wrote {out.relative_to(OUT_DIR.parent.parent)}  ({len(tags)} concepts)")

    # Also surface anything outside the three main namespaces so we don't lose it silently.
    other = {ns: len(t) for ns, t in per_namespace.items() if ns not in {"us-gaap", "ifrs-full", "dei"}}
    if other:
        print(f"  (other namespaces seen, not written: {other})")

    prov_path = OUT_DIR / "_provenance.json"
    prov_path.write_text(json.dumps({
        "user_agent": USER_AGENT,
        "source": "https://data.sec.gov/api/xbrl/companyfacts/",
        "filers": provenance,
        "namespace_totals": {ns: len(t) for ns, t in per_namespace.items()},
    }, indent=2))
    print(f"  wrote {prov_path.relative_to(OUT_DIR.parent.parent)}")


if __name__ == "__main__":
    main()
