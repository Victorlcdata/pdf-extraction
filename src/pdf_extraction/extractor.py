"""Core extraction pipeline: PDF → LLM → validated JSON file (+ run-log record)."""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .prompt import build_prompt
from .providers import Provider
from .run_log import RunLogger, utc_now_iso_ms
from .taxonomy import canonical_names
from .xbrl_taxonomies import apply_concept_map, is_valid_concept, validate_concepts

# ============================================================================
# JSON parsing helpers (robust against markdown wrappers and truncation)
# ============================================================================


def _find_outermost_json_object(text: str) -> str | None:
    """Locate the outermost {...} block in `text`, ignoring braces inside strings.

    Returns the matched substring, or None if no balanced object is found.
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
    """Best-effort recovery when the model ran out of tokens mid-array."""
    facts_marker = '"facts":'
    facts_at = text.find(facts_marker)
    if facts_at == -1:
        return None
    open_bracket = text.find("[", facts_at)
    if open_bracket == -1:
        return None

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
                last_fact_end = i + 1
        elif c == "]" and depth_obj == 0:
            return None

    if last_fact_end == -1:
        return None

    head = text[:last_fact_end].rstrip()
    if head.endswith(","):
        head = head[:-1]
    return head + "\n  ]\n}"


def parse_response(raw: str) -> dict:
    """Parse the model's text response as JSON.

    Tries: direct parse → strip ```json fences → extract outermost {...} →
    salvage truncated facts array. Raises json.JSONDecodeError if all fail.
    """
    text = raw.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    fenced = re.sub(r"^```(?:json)?\s*", "", text)
    fenced = re.sub(r"\s*```$", "", fenced)
    if fenced != text:
        try:
            return json.loads(fenced)
        except json.JSONDecodeError:
            pass

    extracted = _find_outermost_json_object(text)
    if extracted is not None:
        try:
            return json.loads(extracted)
        except json.JSONDecodeError:
            pass

    salvaged = _salvage_truncated_facts(text)
    if salvaged is not None:
        try:
            data = json.loads(salvaged)
            data["_truncated"] = True
            return data
        except json.JSONDecodeError:
            pass

    raise json.JSONDecodeError("No parseable JSON object found in response", text, 0)


# ============================================================================
# Validation helpers
# ============================================================================


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


def write_observations(
    facts: list[dict],
    *,
    pdf_name: str,
    started_at: str,
    observations_path: Path,
) -> None:
    """Append one observation per fact to observations.jsonl for the learning loop.

    Each line is a compact JSON record capturing the (concept, label, canonical,
    statement, period, unit) tuple plus a validity tag. Downstream tools
    (Phase 3) aggregate across many runs to propose new canonical entries.
    """
    observations_path.parent.mkdir(parents=True, exist_ok=True)
    with observations_path.open("a", encoding="utf-8") as f:
        for fact in facts:
            concept = fact.get("concept")
            obs = {
                "ts": started_at,
                "pdf": pdf_name,
                "concept": concept,
                "label": fact.get("label"),
                "statement": fact.get("statement"),
                "canonical": fact.get("canonical"),
                "period": fact.get("period"),
                "unit": fact.get("unit"),
                "concept_valid": is_valid_concept(concept) if concept else None,
            }
            f.write(json.dumps(obs, ensure_ascii=False) + "\n")


# ============================================================================
# Per-PDF pipeline
# ============================================================================


@dataclass
class ExtractionOutcome:
    """Summary of one PDF run, used both for return value and log record."""

    status: str
    """One of: success | api_error | parse_error | skipped."""

    pdf: str = ""
    pdf_size_bytes: int = 0
    provider: str = ""
    model: str = ""
    started_at: str = ""
    """ISO-8601 UTC timestamp (ms precision) of when the API call began."""
    elapsed_seconds: float = 0.0
    facts_total: int = 0
    facts_canonical: int = 0
    facts_dimensioned: int = 0
    facts_concept_invalid: int = 0
    """Facts whose ``concept`` is in a tracked namespace but not in the authoritative list."""
    facts_canonical_from_map: int = 0
    """Facts whose ``canonical`` was set (or confirmed) by the static concept→canonical map."""
    facts_canonical_disagreements: int = 0
    """Subset of `facts_canonical_from_map` where the LLM's original choice differed."""
    tokens_input: int = 0
    tokens_output: int = 0
    tokens_total: int = 0
    rate_limit: dict = field(default_factory=dict)
    output_file: str | None = None
    truncated: bool = False
    error: str | None = None
    data: dict | None = None
    """Parsed JSON payload on success; None otherwise."""

    def to_log_record(self) -> dict[str, Any]:
        """Serializable record for RunLogger.record(...)."""
        return {
            "pdf": self.pdf,
            "pdf_size_bytes": self.pdf_size_bytes,
            "provider": self.provider,
            "model": self.model,
            "started_at": self.started_at,
            "elapsed_seconds": round(self.elapsed_seconds, 2),
            "status": self.status,
            "facts_total": self.facts_total,
            "facts_canonical": self.facts_canonical,
            "facts_dimensioned": self.facts_dimensioned,
            "facts_concept_invalid": self.facts_concept_invalid,
            "facts_canonical_from_map": self.facts_canonical_from_map,
            "facts_canonical_disagreements": self.facts_canonical_disagreements,
            "tokens_input": self.tokens_input,
            "tokens_output": self.tokens_output,
            "tokens_total": self.tokens_total,
            "rate_limit": self.rate_limit,
            "output_file": self.output_file,
            "truncated": self.truncated,
            "error": self.error,
        }


def process_pdf(
    pdf_path: Path,
    provider: Provider,
    model: str,
    out_dir: Path,
    max_tokens: int = 32000,
    log=print,
    run_logger: RunLogger | None = None,
) -> ExtractionOutcome:
    """Process one PDF end-to-end.

    Always returns an ExtractionOutcome; check `.status` to discriminate. If
    `run_logger` is provided, a record is appended to the JSONL log on every
    call (success, parse error, or API error).
    """
    size_bytes = pdf_path.stat().st_size
    outcome = ExtractionOutcome(
        status="api_error",  # placeholder — overwritten below
        pdf=pdf_path.name,
        pdf_size_bytes=size_bytes,
        provider=provider.name,
        model=model,
    )

    log(f"  → reading PDF ({size_bytes / 1e6:.1f} MB) via {provider.name}/{model}...")

    prompt = build_prompt(pdf_path.name)
    outcome.started_at = utc_now_iso_ms()
    started = time.perf_counter()

    try:
        result = provider.extract(pdf_path, prompt, model, max_tokens)
    except Exception as e:
        outcome.elapsed_seconds = time.perf_counter() - started
        outcome.error = f"{type(e).__name__}: {e}"
        log(f"  ! API error: {outcome.error}")
        if run_logger:
            run_logger.record(**outcome.to_log_record())
        return outcome

    outcome.elapsed_seconds = time.perf_counter() - started
    outcome.tokens_input = result.input_tokens
    outcome.tokens_output = result.output_tokens
    outcome.tokens_total = result.total_tokens
    outcome.rate_limit = result.rate_limit

    try:
        data = parse_response(result.text)
    except json.JSONDecodeError as e:
        outcome.status = "parse_error"
        outcome.error = str(e)
        log(f"  ! JSON parse failed: {e}")
        debug_dir = out_dir / "_debug"
        debug_dir.mkdir(exist_ok=True)
        debug_path = debug_dir / f"{pdf_path.stem}.raw_response.txt"
        debug_path.write_text(result.text)
        log(f"  → wrote raw response to _debug/{debug_path.name} for inspection")
        if run_logger:
            run_logger.record(**outcome.to_log_record())
        return outcome

    outcome.truncated = bool(data.pop("_truncated", False))
    if outcome.truncated:
        log(
            "  ⚠ response was truncated (max-tokens reached). Recovered the "
            "complete facts; re-run with --max-tokens 64000 to get the full set."
        )

    facts = data.get("facts", []) or []

    # Apply the static concept→canonical map first. For any fact whose `concept`
    # is in the map, this overrides the LLM's `canonical` with the map's answer
    # so the mapping is consistent across runs. No-op when the map file is absent.
    n_from_map, disagreements = apply_concept_map(facts)
    outcome.facts_canonical_from_map = n_from_map
    outcome.facts_canonical_disagreements = len(disagreements)
    if disagreements:
        samples = [
            f"{c} (LLM={llm!r} → map={mp!r})" for c, llm, mp in disagreements[:3]
        ]
        log(f"  ◇ {len(disagreements)} concept-map override(s): {samples}")

    bad = validate_canonicals(data, canonical_names())
    if bad:
        log(f"  ⚠ {len(bad)} unknown canonical name(s): {bad[:5]}")

    outcome.facts_total = len(facts)
    outcome.facts_canonical = sum(1 for f in facts if f.get("canonical"))
    outcome.facts_dimensioned = sum(1 for f in facts if f.get("dimensions"))

    invalid_count, invalid_samples = validate_concepts(facts)
    outcome.facts_concept_invalid = invalid_count
    if invalid_count:
        log(
            f"  ⚠ {invalid_count} concept(s) not in authoritative taxonomy: "
            f"{invalid_samples[:5]}"
        )

    outcome.data = data
    outcome.status = "success"

    entity = data.get("entity", {}) or {}
    filing = data.get("filing", {}) or {}
    log(
        f"  ✓ {entity.get('name', '?')}"
        f" {filing.get('form', '')}"
        f" FY{filing.get('fiscal_year', '?')}"
        f" — {outcome.facts_total} facts ({outcome.facts_canonical} canonical-mapped)"
        f" · {outcome.tokens_total:,} tokens · {outcome.elapsed_seconds:.1f}s"
    )

    out_path = out_dir / safe_filename(entity, filing, pdf_path.stem)
    out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    outcome.output_file = out_path.name
    log(f"  → wrote {out_path.name}")

    write_observations(
        facts,
        pdf_name=pdf_path.name,
        started_at=outcome.started_at,
        observations_path=out_dir / "observations.jsonl",
    )

    if run_logger:
        run_logger.record(**outcome.to_log_record())
    return outcome
