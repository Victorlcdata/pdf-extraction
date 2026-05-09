"""JSONL run log — one self-contained record appended per processed PDF.

The log file is append-only: re-running the CLI keeps history intact so you can
inspect throughput, token spend, and failure patterns over time.

Every record carries TWO timestamps so you can correlate runs precisely:

    started_at  — UTC, ISO-8601 ms precision. When the provider API call began.
                  Use this when joining logs by chronology or computing throughput.
    timestamp   — UTC, ISO-8601 ms precision. When the record was written
                  (essentially started_at + elapsed_seconds).

Canonical record shape:

    {
      "timestamp":         "2026-05-09T13:45:32.418Z",
      "started_at":        "2026-05-09T13:44:45.092Z",
      "pdf":               "apple_fy2024_10k.pdf",
      "pdf_size_bytes":    1093835,
      "provider":          "anthropic",
      "model":             "claude-sonnet-4-6",
      "elapsed_seconds":   47.32,
      "status":            "success",                 // or skipped | api_error | parse_error
      "facts_total":       985,
      "facts_canonical":   612,
      "facts_dimensioned": 80,
      "tokens_input":      32140,
      "tokens_output":     18432,
      "tokens_total":      50572,
      "rate_limit":        { ... },                   // populated from response headers
      "output_file":       "AAPL_FY2024.facts.json",
      "truncated":         false,
      "error":             null
    }

NOTE: providers do NOT expose remaining account credit — only per-request usage
and per-minute rate-limit windows. To see remaining credit, check the provider
billing dashboard directly.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now_iso_ms() -> str:
    """ISO-8601 UTC timestamp with millisecond precision, e.g. 2026-05-09T13:45:32.418Z."""
    now = datetime.now(timezone.utc)
    # `isoformat(timespec="milliseconds")` returns "...+00:00"; replace tz suffix with Z.
    return now.isoformat(timespec="milliseconds").replace("+00:00", "Z")


class RunLogger:
    """Append-only JSONL writer for per-PDF run records."""

    def __init__(self, log_path: Path):
        self.log_path = log_path
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self._records: list[dict[str, Any]] = []

    def record(self, **fields: Any) -> dict[str, Any]:
        """Append a record to the log. Adds a `timestamp` field if not provided."""
        rec = dict(fields)
        rec.setdefault("timestamp", utc_now_iso_ms())
        self._records.append(rec)
        with self.log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        return rec

    @property
    def records(self) -> list[dict[str, Any]]:
        """All records written by this logger instance (does not read prior history)."""
        return list(self._records)

    def summarize(self) -> dict[str, Any]:
        """Aggregate metrics from records written by this instance."""
        successes = [r for r in self._records if r.get("status") == "success"]
        failures = [r for r in self._records if r.get("status") not in ("success", "skipped")]
        return {
            "pdfs_processed": len(self._records),
            "succeeded": len(successes),
            "failed": len(failures),
            "skipped": sum(1 for r in self._records if r.get("status") == "skipped"),
            "total_elapsed_s": round(sum(r.get("elapsed_seconds", 0) for r in self._records), 2),
            "total_tokens_in": sum(r.get("tokens_input", 0) for r in self._records),
            "total_tokens_out": sum(r.get("tokens_output", 0) for r in self._records),
            "total_tokens": sum(r.get("tokens_total", 0) for r in self._records),
            "total_facts": sum(r.get("facts_total", 0) for r in successes),
            "total_canonical": sum(r.get("facts_canonical", 0) for r in successes),
        }
