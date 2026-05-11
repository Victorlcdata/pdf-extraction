"""Command-line entry point."""

from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

from . import __version__
from .extractor import process_pdf
from .providers import PROVIDERS
from .run_log import RunLogger, utc_now_iso_ms

DEFAULT_MODEL_PER_PROVIDER = {
    "anthropic": "sonnet",
    "google": "pro",
    "openai": "gpt5mini",
}

API_KEY_HELP = """\
  Anthropic: https://console.anthropic.com
  Google:    https://aistudio.google.com/apikey
  OpenAI:    https://platform.openai.com/api-keys"""


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="extract-financials",
        description="Batch-extract XBRL-style financial facts from a folder of annual report PDFs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("folder", help="Folder containing input PDF files")
    parser.add_argument(
        "--provider",
        choices=sorted(PROVIDERS),
        default="google",
        help="LLM provider (default: google)",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Model alias (e.g. opus/sonnet/haiku, pro/flash, gpt5/gpt5mini) "
        "or a full model id. Defaults to the cheap-but-capable option for the chosen provider.",
    )
    parser.add_argument(
        "--out-dir",
        default=None,
        help="Output folder. Default: if input folder is named 'input', use sibling 'output' folder; "
        "otherwise write JSON next to the source PDFs.",
    )
    parser.add_argument(
        "--log-file",
        default=None,
        help="Path to JSONL run log (one record appended per PDF). "
        "Default: <out_dir>/run_log.jsonl",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip PDFs whose .facts.json already exists in the output folder",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List PDFs without calling any API",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=32000,
        help="Max output tokens per filing (default: 32000). Bump to 64000 "
        "for very dense filings where the response gets truncated.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def _resolve_paths(args: argparse.Namespace) -> tuple[Path, Path, Path]:
    """Resolve input folder, output dir, and log file from CLI args."""
    folder = Path(args.folder).expanduser().resolve()
    if not folder.is_dir():
        sys.exit(f"ERROR: not a folder: {folder}")

    if args.out_dir:
        out_dir = Path(args.out_dir).expanduser().resolve()
    elif folder.name == "input" and (folder.parent / "output").parent == folder.parent:
        out_dir = folder.parent / "output"
    else:
        out_dir = folder
    out_dir.mkdir(parents=True, exist_ok=True)

    log_path = (
        Path(args.log_file).expanduser().resolve() if args.log_file else out_dir / "run_log.jsonl"
    )
    return folder, out_dir, log_path


def _print_summary(summary: dict, log_path: Path, last_rate_limit: dict | None) -> None:
    print()
    print("=" * 60)
    print(f"Run summary  ({summary['pdfs_processed']} PDFs processed)")
    print("=" * 60)
    print(f"  Succeeded:        {summary['succeeded']}")
    print(f"  Failed:           {summary['failed']}")
    print(f"  Skipped:          {summary['skipped']}")
    print(f"  Total elapsed:    {summary['total_elapsed_s']:.0f}s")
    print(f"  Total tokens in:  {summary['total_tokens_in']:,}")
    print(f"  Total tokens out: {summary['total_tokens_out']:,}")
    print(f"  Total tokens:     {summary['total_tokens']:,}")
    print(
        f"  Total facts:      {summary['total_facts']:,} ({summary['total_canonical']:,} canonical-mapped)"
    )
    print(
        f"  Concept-invalid:  {summary['total_concept_invalid']:,} "
        f"(tags not in authoritative XBRL list — see data/taxonomies/)"
    )
    print(
        f"  From concept map: {summary['total_canonical_from_map']:,} canonicals "
        f"set by static map ({summary['total_canonical_disagreements']:,} LLM disagreements)"
    )
    print(f"  Run log:          {log_path}")

    if last_rate_limit:
        print()
        print("Rate-limit window after final request (current minute):")
        for key, value in last_rate_limit.items():
            print(f"  {key + ':':22s} {value}")
        print()
        print("ℹ Account credit balance is not exposed by Anthropic / Google / OpenAI APIs.")
        print("  Check your provider billing dashboard for remaining account credit.")


def main() -> None:
    args = _build_arg_parser().parse_args()
    folder, out_dir, log_path = _resolve_paths(args)
    model_alias = args.model or DEFAULT_MODEL_PER_PROVIDER[args.provider]

    pdfs = sorted(folder.glob("*.pdf"))
    if not pdfs:
        sys.exit(f"No PDFs found in {folder}")

    print(f"Found {len(pdfs)} PDF(s) in {folder}")
    print(f"Output dir: {out_dir}")
    print(f"Log file:   {log_path}")
    print(f"Provider:   {args.provider}")
    print(f"Model:      {model_alias}")
    print()

    if args.dry_run:
        for pdf in pdfs:
            print(f"  {pdf.name} ({pdf.stat().st_size / 1e6:.1f} MB)")
        return

    provider_cls = PROVIDERS[args.provider]
    if not os.environ.get(provider_cls.env_var):
        sys.exit(f"ERROR: {provider_cls.env_var} not set.\n{API_KEY_HELP}")

    provider = provider_cls()
    model = provider.resolve_model(model_alias)
    print(f"Resolved model: {model}\n", flush=True)

    run_logger = RunLogger(log_path)
    last_rate_limit: dict | None = None
    started = time.time()

    for i, pdf in enumerate(pdfs, 1):
        print(f"[{i}/{len(pdfs)}] {pdf.name}", flush=True)

        if args.skip_existing:
            existing = list(out_dir.glob(f"{pdf.stem}*.facts.json"))
            if existing:
                print(f"  (skipped — {existing[0].name} exists)", flush=True)
                run_logger.record(
                    pdf=pdf.name,
                    pdf_size_bytes=pdf.stat().st_size,
                    provider=args.provider,
                    model=model,
                    started_at=utc_now_iso_ms(),
                    status="skipped",
                    elapsed_seconds=0,
                    facts_total=0,
                    facts_canonical=0,
                    facts_dimensioned=0,
                    tokens_input=0,
                    tokens_output=0,
                    tokens_total=0,
                    rate_limit={},
                    output_file=existing[0].name,
                    truncated=False,
                    error=None,
                )
                continue

        outcome = process_pdf(pdf, provider, model, out_dir, args.max_tokens, run_logger=run_logger)
        if outcome.rate_limit:
            last_rate_limit = outcome.rate_limit

    elapsed = time.time() - started
    summary = run_logger.summarize()
    summary["total_elapsed_s"] = round(elapsed, 2)
    _print_summary(summary, log_path, last_rate_limit)

    if summary["failed"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
