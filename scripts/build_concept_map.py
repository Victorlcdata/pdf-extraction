"""Build the static `concept -> canonical` mapping table.

For each XBRL element name in data/taxonomies/{us-gaap,ifrs-full,dei}.txt,
asks an LLM which canonical (from src/pdf_extraction/taxonomy.py) it best
maps to — or null if no canonical concept fits cleanly. The result is a
deterministic lookup table that:

  1. Lets extractor.py assign `canonical` without re-deriving on every run
     (which is what introduced inconsistency before).
  2. Serves as a human-readable reference (the markdown output) — one batch
     review instead of per-PDF review.

Run once when the canonical taxonomy or the authoritative tag lists change.
Default provider is Google Gemini 2.5 Pro (matches the extraction CLI's
default and reuses the GOOGLE_API_KEY you already have set). Override with
``--provider`` for anthropic or openai.

Approximate cost for all three namespaces (~3,400 tags total):
    google/pro       ~$1-2
    anthropic/sonnet ~$2-3
    openai/gpt5      ~$3-5

Outputs (under data/taxonomies/):
    concept_canonical_map.json    machine-readable, used by xbrl_taxonomies.py
    concept_canonical_map.md      human-readable table, one section per namespace
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pdf_extraction.providers import PROVIDERS  # noqa: E402  (use SDK aliases)
from pdf_extraction.taxonomy import TAXONOMY  # noqa: E402

TAX_DIR = ROOT / "data" / "taxonomies"
DEFAULT_NAMESPACES = ["us-gaap", "ifrs-full", "dei"]
DEFAULT_BATCH_SIZE = 400
DEFAULT_PROVIDER = "google"
DEFAULT_MODEL_PER_PROVIDER = {"google": "pro", "anthropic": "sonnet", "openai": "gpt5"}


# ----------------------------------------------------------------------------
# Prompt
# ----------------------------------------------------------------------------


def build_prompt(namespace: str, tags: list[str]) -> str:
    canonicals_str = "\n".join(f"  {name}: {desc}" for name, desc in TAXONOMY.items())
    tags_str = "\n".join(tags)
    return f"""You are an expert XBRL / financial reporting analyst.

Given a batch of XBRL element names from the `{namespace}` namespace and a
canonical taxonomy of cross-company analytical concepts, map each element to
either:
  - The CANONICAL name from the taxonomy that best fits, OR
  - null  if no canonical concept fits cleanly.

OUTPUT: a JSON array. One object per input tag, in the SAME ORDER as the input.

[
  {{"tag": "<element name>", "canonical": "<CanonicalName>" | null, "note": "<5-20 word rationale>"}},
  ...
]

RULES:
1. Pick a SINGLE best match. Never invent canonical names not in the list.
2. Use null for: structural elements (abstract / axis / domain / member),
   purely textual disclosures, sector-specific concepts with no analog in the
   canonical set, deprecated concepts, and tags more granular than any
   canonical when the broader canonical would mislead.
3. "note" briefly justifies the choice (e.g. "alias for AccountsPayable",
   "axis member - structural, no analytical value", "REIT-only concept, no
   canonical"). Keep it 5-20 words.
4. PRESERVE the exact tag spelling. Do not edit, expand abbreviations, or guess.

CANONICAL TAXONOMY (pick canonical only from these {len(TAXONOMY)} names):

{canonicals_str}

NAMESPACE: {namespace}

TAGS TO MAP ({len(tags)} entries, preserve order):

{tags_str}

Output ONLY the JSON array. No prose, no markdown fences, no leading/trailing commentary.
"""


# ----------------------------------------------------------------------------
# Provider-agnostic text-only completion
# ----------------------------------------------------------------------------


def complete_text(provider_name: str, model: str, prompt: str, max_tokens: int) -> tuple[str, dict[str, int]]:
    """Send a text-only prompt and return (response_text, {input_tokens, output_tokens}).

    Reuses each provider's SDK directly. PDF-upload code paths (extractor.py)
    are bypassed since this is a pure text task.
    """
    if provider_name == "google":
        from google import genai
        from google.genai import types

        client = genai.Client()
        response = client.models.generate_content(
            model=model,
            contents=[prompt],
            config=types.GenerateContentConfig(
                max_output_tokens=max_tokens,
                response_mime_type="application/json",
            ),
        )
        usage = getattr(response, "usage_metadata", None)
        return response.text, {
            "input_tokens": getattr(usage, "prompt_token_count", 0) or 0 if usage else 0,
            "output_tokens": getattr(usage, "candidates_token_count", 0) or 0 if usage else 0,
        }

    if provider_name == "anthropic":
        from anthropic import Anthropic

        client = Anthropic()
        resp = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.content[0].text, {
            "input_tokens": resp.usage.input_tokens,
            "output_tokens": resp.usage.output_tokens,
        }

    if provider_name == "openai":
        from openai import OpenAI

        client = OpenAI()
        resp = client.responses.create(
            model=model,
            input=prompt,
            max_output_tokens=max_tokens,
        )
        return resp.output_text, {
            "input_tokens": resp.usage.input_tokens,
            "output_tokens": resp.usage.output_tokens,
        }

    raise ValueError(f"unknown provider: {provider_name}")


def parse_json_array(raw: str) -> list[dict[str, Any]]:
    """Parse a JSON array, tolerating markdown fences and truncation mid-stream."""
    text = raw.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Salvage: walk character-by-character, track string/escape state, and cut
    # the array at the last complete top-level object boundary.
    if not text.lstrip().startswith("["):
        raise json.JSONDecodeError("not an array", text, 0)
    open_bracket = text.find("[")
    depth_obj = 0
    in_string = False
    escape = False
    last_obj_end = -1
    for i in range(open_bracket + 1, len(text)):
        c = text[i]
        if escape:
            escape = False
            continue
        if c == "\\":
            escape = True
            continue
        if c == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if c == "{":
            depth_obj += 1
        elif c == "}":
            depth_obj -= 1
            if depth_obj == 0:
                last_obj_end = i + 1
    if last_obj_end == -1:
        raise json.JSONDecodeError("no complete objects in truncated array", text, 0)
    head = text[:last_obj_end].rstrip()
    if head.endswith(","):
        head = head[:-1]
    return json.loads(head + "]")


# ----------------------------------------------------------------------------
# Per-namespace pipeline
# ----------------------------------------------------------------------------


def map_namespace(
    namespace: str,
    tags: list[str],
    *,
    provider: str,
    model: str,
    batch_size: int,
    debug_dir: Path,
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    """Map all tags in a namespace via batched LLM calls. Returns (mappings, token_totals)."""
    canonicals_set = set(TAXONOMY.keys())
    out: list[dict[str, Any]] = []
    totals = {"input_tokens": 0, "output_tokens": 0}

    n_batches = (len(tags) + batch_size - 1) // batch_size
    for bi, i in enumerate(range(0, len(tags), batch_size), 1):
        batch = tags[i : i + batch_size]
        print(f"  [{bi}/{n_batches}] {len(batch)} tags...", flush=True)
        prompt = build_prompt(namespace, batch)

        # Output budget: ~80 tokens / row average. Cap so we don't hit provider limits.
        max_tokens = min(64000, max(4000, len(batch) * 80))

        started = time.perf_counter()
        try:
            raw, usage = complete_text(provider, model, prompt, max_tokens)
        except Exception as e:
            print(f"    [ERROR] API call failed: {e}", file=sys.stderr)
            debug_dir.mkdir(parents=True, exist_ok=True)
            (debug_dir / f"{namespace}_batch{bi}.error.txt").write_text(str(e))
            continue
        elapsed = time.perf_counter() - started
        totals["input_tokens"] += usage["input_tokens"]
        totals["output_tokens"] += usage["output_tokens"]
        print(
            f"    {elapsed:.1f}s · in={usage['input_tokens']:,} out={usage['output_tokens']:,}",
            flush=True,
        )

        # Gemini occasionally returns no content (out=0). Skip the batch — it will
        # be retried on the next idempotent re-run.
        if not raw:
            print(f"    [WARN] empty response from provider; skipping batch (retry on next run)")
            continue

        try:
            results = parse_json_array(raw)
        except json.JSONDecodeError as e:
            print(f"    [WARN] JSON parse failed: {e}; raw saved for inspection")
            debug_dir.mkdir(parents=True, exist_ok=True)
            (debug_dir / f"{namespace}_batch{bi}.raw.txt").write_text(raw)
            continue

        # Validate each row: canonical, if present, must be a known name.
        for r in results:
            canonical = r.get("canonical")
            if canonical is not None and canonical not in canonicals_set:
                note = r.get("note", "") or ""
                r["note"] = (note + f" [DROPPED invalid canonical: {canonical}]").strip()
                r["canonical"] = None
        out.extend(results)

    return out, totals


# ----------------------------------------------------------------------------
# Output writers
# ----------------------------------------------------------------------------


def write_json(by_ns: dict[str, list[dict[str, Any]]], path: Path) -> None:
    nested: dict[str, dict[str, dict[str, Any]]] = {}
    for ns, rows in by_ns.items():
        nested[ns] = {
            r["tag"]: {"canonical": r.get("canonical"), "note": r.get("note", "")}
            for r in rows
            if r.get("tag")
        }
    path.write_text(json.dumps(nested, indent=2, ensure_ascii=False))


def write_markdown(
    by_ns: dict[str, list[dict[str, Any]]],
    path: Path,
    *,
    token_totals: dict[str, dict[str, int]],
    provider: str,
    model: str,
) -> None:
    lines: list[str] = []
    lines.append("# Concept → canonical mapping\n")
    lines.append(
        f"Generated by `scripts/build_concept_map.py` using `{provider}/{model}`. "
        "One row per XBRL element name across the namespaces below. Review this "
        "once. To correct specific rows, change the canonical taxonomy (or the "
        "prompt) and re-run — editing this file directly does nothing.\n"
    )
    lines.append("## Summary\n")
    lines.append("| Namespace | Tags | Mapped | Mapped % | Tokens in | Tokens out |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for ns, rows in by_ns.items():
        mapped = sum(1 for r in rows if r.get("canonical"))
        pct = (100 * mapped / len(rows)) if rows else 0.0
        t = token_totals.get(ns, {})
        lines.append(
            f"| `{ns}` | {len(rows):,} | {mapped:,} | {pct:.0f}% | "
            f"{t.get('input_tokens', 0):,} | {t.get('output_tokens', 0):,} |"
        )
    lines.append("")

    for ns, rows in by_ns.items():
        lines.append(f"## `{ns}` ({len(rows):,} tags)\n")
        lines.append("| Tag | Canonical | Note |")
        lines.append("|---|---|---|")
        for r in rows:
            tag = r.get("tag", "")
            canonical = r.get("canonical")
            canonical_md = f"`{canonical}`" if canonical else "_null_"
            note = (r.get("note") or "").replace("|", "/").replace("\n", " ")
            lines.append(f"| `{tag}` | {canonical_md} | {note} |")
        lines.append("")

    path.write_text("\n".join(lines))


# ----------------------------------------------------------------------------
# Entry point
# ----------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--provider",
        choices=sorted(PROVIDERS),
        default=DEFAULT_PROVIDER,
        help=f"LLM provider (default: {DEFAULT_PROVIDER})",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Model alias or full id. Defaults to the strong model for the chosen provider.",
    )
    parser.add_argument(
        "--namespaces",
        nargs="+",
        default=DEFAULT_NAMESPACES,
        help="Which namespaces to map (default: us-gaap ifrs-full dei)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=DEFAULT_BATCH_SIZE,
        help=f"Tags per LLM call (default: {DEFAULT_BATCH_SIZE})",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-map every tag from scratch, ignoring any existing map file. "
        "Default behavior is to skip tags already present in concept_canonical_map.json.",
    )
    args = parser.parse_args()

    # Resolve provider + model
    provider_cls = PROVIDERS[args.provider]
    if not os.environ.get(provider_cls.env_var):
        sys.exit(
            f"ERROR: {provider_cls.env_var} not set for provider '{args.provider}'. "
            "Either export it or run `set -a; source .env; set +a` first."
        )
    model_alias = args.model or DEFAULT_MODEL_PER_PROVIDER[args.provider]
    # Resolve alias → full model id via the provider's `aliases` map
    model = provider_cls.aliases.get(model_alias, model_alias)
    print(f"Provider: {args.provider} · Model: {model}\n")

    TAX_DIR.mkdir(parents=True, exist_ok=True)
    debug_dir = TAX_DIR / "_debug"
    json_path = TAX_DIR / "concept_canonical_map.json"
    md_path = TAX_DIR / "concept_canonical_map.md"

    # Load existing map (idempotent re-runs only process missing tags).
    existing: dict[str, dict[str, dict]] = {}
    if not args.force and json_path.exists():
        try:
            existing = json.loads(json_path.read_text())
            existing_count = sum(len(v) for v in existing.values())
            print(f"Loaded existing map: {existing_count:,} tags already covered (use --force to re-map)\n")
        except (json.JSONDecodeError, OSError) as e:
            print(f"[WARN] couldn't read existing map ({e}); re-mapping from scratch\n")
            existing = {}

    by_ns: dict[str, list[dict[str, Any]]] = {}
    token_totals: dict[str, dict[str, int]] = {}

    for ns in args.namespaces:
        path = TAX_DIR / f"{ns}.txt"
        if not path.exists():
            print(f"  [skip] {ns}: {path} not found")
            continue
        all_tags = [t.strip() for t in path.read_text().splitlines() if t.strip()]
        already = set(existing.get(ns, {}).keys())
        to_map = [t for t in all_tags if t not in already]
        if not to_map:
            print(f"=== {ns}: {len(all_tags):,} tags (all already mapped, skipping) ===\n")
            # Carry the existing rows through to the writers below
            by_ns[ns] = [
                {"tag": tag, **vals} for tag, vals in existing.get(ns, {}).items()
            ]
            token_totals[ns] = {"input_tokens": 0, "output_tokens": 0}
            continue
        print(
            f"=== {ns}: {len(all_tags):,} tags ({len(already):,} already mapped; "
            f"{len(to_map):,} to process) ==="
        )
        rows, totals = map_namespace(
            ns,
            to_map,
            provider=args.provider,
            model=model,
            batch_size=args.batch_size,
            debug_dir=debug_dir,
        )
        # Merge new rows on top of any pre-existing ones (new rows win in case of collision).
        merged: dict[str, dict] = dict(existing.get(ns, {}))
        for r in rows:
            tag = r.get("tag")
            if tag:
                merged[tag] = {"canonical": r.get("canonical"), "note": r.get("note", "")}
        by_ns[ns] = [{"tag": tag, **vals} for tag, vals in merged.items()]
        token_totals[ns] = totals
        print()

    write_json(by_ns, json_path)
    write_markdown(by_ns, md_path, token_totals=token_totals, provider=args.provider, model=model)

    total_tags = sum(len(v) for v in by_ns.values())
    total_mapped = sum(1 for v in by_ns.values() for r in v if r.get("canonical"))
    total_in = sum(t.get("input_tokens", 0) for t in token_totals.values())
    total_out = sum(t.get("output_tokens", 0) for t in token_totals.values())
    pct = (100 * total_mapped / total_tags) if total_tags else 0.0

    print("=" * 60)
    print(f"  Tags processed:   {total_tags:,}")
    print(f"  Mapped:           {total_mapped:,} ({pct:.0f}%)")
    print(f"  Tokens in:        {total_in:,}")
    print(f"  Tokens out:       {total_out:,}")
    print(f"  JSON output:      {json_path.relative_to(ROOT)}")
    print(f"  Markdown output:  {md_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
