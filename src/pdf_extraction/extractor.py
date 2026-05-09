"""Core extraction pipeline: PDF → LLM → validated JSON file."""

from __future__ import annotations

import json
import re
from pathlib import Path

from .prompt import build_prompt
from .providers import Provider
from .taxonomy import canonical_names


def _find_outermost_json_object(text: str) -> str | None:
    """Locate the outermost {...} block in `text`, ignoring braces inside strings.

    Returns the matched substring, or None if no balanced object is found.
    Used as a fallback when the model wraps its JSON in prose or markdown
    despite the prompt asking for raw JSON only.
    """
    start = text.find("{")
    if start == -1:
        return None
    depth = 0
    in_string = False
    escape = False
    for i in range(start, len(text)):
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
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return text[start : i + 1]
    return None


def _salvage_truncated_facts(text: str) -> str | None:
    """Best-effort recovery when the model ran out of tokens mid-array.

    The schema's `facts` array is the largest field; truncation almost always
    happens inside it. This walks `text` to find the last `}` that closes a
    complete fact, drops everything after it, and re-closes the array + object.

    Returns a parseable JSON string, or None if recovery isn't possible.
    """
    facts_marker = '"facts":'
    facts_at = text.find(facts_marker)
    if facts_at == -1:
        return None
    # Find the opening '[' of the facts array
    open_bracket = text.find("[", facts_at)
    if open_bracket == -1:
        return None

    # Walk through the array, tracking depth and string state, recording the
    # position right after each complete top-level `}` (a complete fact).
    depth_obj = 0
    in_string = False
    escape = False
    last_fact_end = -1
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
                last_fact_end = i + 1  # position right after the closing brace
        elif c == "]" and depth_obj == 0:
            # The array ended cleanly; nothing to salvage
            return None

    if last_fact_end == -1:
        return None

    # Reconstruct: text up through the last complete fact, close the array,
    # close the outer object. Drop a trailing comma if present.
    head = text[:last_fact_end].rstrip()
    if head.endswith(","):
        head = head[:-1]
    return head + "\n  ]\n}"


def parse_response(raw: str) -> dict:
    """Parse the model's text response as JSON.

    Tries, in order:
      1. Direct json.loads on the trimmed text
      2. Strip ```json``` markdown fences and retry
      3. Extract the outermost balanced {...} block and parse that
      4. Salvage truncated output by closing the facts array at the last complete fact

    Raises json.JSONDecodeError if none succeed.
    """
    text = raw.strip()

    # 1. Direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # 2. Strip ```json fences
    fenced = re.sub(r"^```(?:json)?\s*", "", text)
    fenced = re.sub(r"\s*```$", "", fenced)
    if fenced != text:
        try:
            return json.loads(fenced)
        except json.JSONDecodeError:
            pass

    # 3. Extract outermost { ... }
    extracted = _find_outermost_json_object(text)
    if extracted is not None:
        try:
            return json.loads(extracted)
        except json.JSONDecodeError:
            pass

    # 4. Salvage truncated output
    salvaged = _salvage_truncated_facts(text)
    if salvaged is not None:
        try:
            data = json.loads(salvaged)
            data["_truncated"] = True
            return data
        except json.JSONDecodeError:
            pass

    raise json.JSONDecodeError("No parseable JSON object found in response", text, 0)


def validate_canonicals(data: dict, valid_names: set[str]) -> list[str]:
    """Return any invalid canonical names found in the facts list."""
    bad = set()
    for fact in data.get("facts", []):
        name = fact.get("canonical")
        if name is not None and name not in valid_names:
            bad.add(name)
    return sorted(bad)


def safe_filename(entity: dict, filing: dict, fallback: str) -> str:
    """Build a friendly output filename from entity/filing metadata."""
    base = entity.get("ticker") or entity.get("name") or fallback
    base = re.sub(r"[^A-Za-z0-9]+", "_", base).strip("_")[:40]
    fy = filing.get("fiscal_year")
    return f"{base}_FY{fy}.facts.json" if fy else f"{base}.facts.json"


def process_pdf(
    pdf_path: Path,
    provider: Provider,
    model: str,
    out_dir: Path,
    max_tokens: int = 32000,
    log=print,
) -> dict | None:
    """Process one PDF end-to-end. Returns parsed dict on success, None on failure."""
    size_mb = pdf_path.stat().st_size / 1e6
    log(f"  → reading PDF ({size_mb:.1f} MB) via {provider.name}/{model}...")

    prompt = build_prompt(pdf_path.name)

    try:
        raw = provider.extract(pdf_path, prompt, model, max_tokens)
    except Exception as e:
        log(f"  ! API error: {type(e).__name__}: {e}")
        return None

    try:
        data = parse_response(raw)
    except json.JSONDecodeError as e:
        log(f"  ! JSON parse failed: {e}")
        debug_dir = out_dir / "_debug"
        debug_dir.mkdir(exist_ok=True)
        debug_path = debug_dir / f"{pdf_path.stem}.raw_response.txt"
        debug_path.write_text(raw)
        log(f"  → wrote raw response to _debug/{debug_path.name} for inspection")
        return None

    if data.pop("_truncated", False):
        log(f"  ⚠ response was truncated (max-tokens reached). Recovered the complete facts; "
            f"re-run with --max-tokens 64000 to get the full set.")

    bad = validate_canonicals(data, canonical_names())
    if bad:
        log(f"  ⚠ {len(bad)} unknown canonical name(s): {bad[:5]}")

    facts = data.get("facts", []) or []
    n_canonical = sum(1 for f in facts if f.get("canonical"))
    entity = data.get("entity", {}) or {}
    filing = data.get("filing", {}) or {}

    log(
        f"  ✓ {entity.get('name', '?')}"
        f" {filing.get('form', '')}"
        f" FY{filing.get('fiscal_year', '?')}"
        f" — {len(facts)} facts ({n_canonical} canonical-mapped)"
    )

    out_path = out_dir / safe_filename(entity, filing, pdf_path.stem)
    out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    log(f"  → wrote {out_path.name}")
    return data
