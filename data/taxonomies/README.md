# Authoritative XBRL tag lists

These files are the *authoritative* lists of XBRL element names that the
extraction LLM is allowed to emit in the `concept` field of each fact. Anything
emitted that's not in one of these files (and not prefixed `custom:`) is
flagged downstream as a likely hallucination.

## Files

| File | Namespace | Source | Coverage |
|---|---|---|---|
| `us-gaap.txt` | `us-gaap:*` | SEC EDGAR companyfacts API | 2,849 concepts unioned from 13 diverse US filers |
| `ifrs-full.txt` | `ifrs-full:*` | SEC EDGAR companyfacts API | 591 concepts unioned from 3 IFRS-filing 20-F issuers |
| `dei.txt` | `dei:*` | SEC EDGAR companyfacts API | 3 concepts — small because DEI cover-page tags are rarely emitted as facts |
| `_provenance.json` | — | — | Which filers contributed and their concept counts |

## Source

All concept names come from the SEC's free, no-auth XBRL data endpoint:

```
https://data.sec.gov/api/xbrl/companyfacts/CIK{10-digit-cik}.json
```

This endpoint returns every XBRL concept a given filer has actually reported
since they started filing XBRL data with the SEC, grouped by namespace
(`us-gaap`, `ifrs-full`, `dei`, `srt`, `invest`, `ecd`, `ffd`, ...). It is the
authoritative record of *what real filers emit* — which is what we want for
validation. Endpoint reference: <https://www.sec.gov/search-filings/edgar-application-programming-interfaces>.

## How the lists are built

`scripts/fetch_taxonomies.py` does the following:

1. Defines a curated seed list of filer CIKs chosen for **sector breadth** —
   tech (Apple, Microsoft, Amazon), banks (JPMorgan, Goldman), insurance
   conglomerate (Berkshire), pharma (Pfizer; Novartis/AstraZeneca/Sanofi for
   IFRS), oil (ExxonMobil), retail (Walmart), industrial (Boeing), payments
   (Visa), auto (Tesla), consumer goods (P&G).
2. For each CIK, fetches `companyfacts/CIK{cik}.json` from SEC EDGAR with a
   descriptive `User-Agent` header (SEC policy). Responses are cached under
   `/tmp/sec_facts_cache/` to avoid re-hitting the API.
3. For each filer's response, iterates the `facts.{namespace}` object and
   collects the keys (concept names).
4. Unions the concept names per namespace across all filers, sorts
   alphabetically, and writes one element per line to
   `data/taxonomies/{namespace}.txt`.
5. Records who contributed and how many concepts each filer surfaced in
   `_provenance.json`.

## What this list IS

- **An empirically observed subset** of the full XBRL taxonomies — i.e. the
  concepts that real filers have actually used in real SEC filings. For
  validation purposes that is what you want, because it catches LLM
  hallucinations without rejecting tags that companies legitimately emit.

## What this list IS NOT

- **Not the full theoretical taxonomy.** US-GAAP alone defines ~15,000 element
  names; the vast majority are unused. Including all 15k would weaken
  validation (it would accept obscure or deprecated tags that no real filing
  uses).
- **Not a guarantee of currency.** SEC accepts filings using older taxonomy
  versions, so the union may include tags that have since been deprecated in
  newer FASB / IFRS releases. For most extraction work this is fine; for
  strict-period regulatory work, re-fetch and pin to a specific year.
- **Not language-aware.** Concept names are English-only here. Japanese (JGAAP)
  or other national taxonomies would need their own files.

## Refresh

Re-run the fetcher any time. It caches responses under `/tmp/sec_facts_cache/`
to avoid re-hitting the API on repeat runs — delete the cache directory to
force a fresh pull.

```bash
python3 scripts/fetch_taxonomies.py
```

To broaden coverage, edit the `US_GAAP_FILERS` / `IFRS_FILERS` lists in
`scripts/fetch_taxonomies.py` and re-run. Adding a few REITs, insurers, or
foreign issuers usually adds a few hundred more concepts each.
