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

DEFAULT_MODEL_PER_PROVIDER = {
    "anthropic": "sonnet",
    "google":    "flash",
    "openai":    "gpt5mini",
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
    parser.add_argument(
        "folder",
        help="Folder containing input PDF files",
    )
    parser.add_argument(
        "--provider",
        choices=sorted(PROVIDERS),
        default="anthropic",
        help="LLM provider (default: anthropic)",
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


def main() -> None:
    args = _build_arg_parser().parse_args()

    folder = Path(args.folder).expanduser().resolve()
    if not folder.is_dir():
        sys.exit(f"ERROR: not a folder: {folder}")

    if args.out_dir:
        out_dir = Path(args.out_dir).expanduser().resolve()
    elif folder.name == "input" and (folder.parent / "output").parent == folder.parent:
        # Convention: data/input/ → data/output/
        out_dir = folder.parent / "output"
    else:
        out_dir = folder
    out_dir.mkdir(parents=True, exist_ok=True)

    model_alias = args.model or DEFAULT_MODEL_PER_PROVIDER[args.provider]

    pdfs = sorted(folder.glob("*.pdf"))
    if not pdfs:
        sys.exit(f"No PDFs found in {folder}")

    print(f"Found {len(pdfs)} PDF(s) in {folder}")
    print(f"Output dir: {out_dir}")
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

    successes, failures, skipped = 0, 0, 0
    started = time.time()

    for i, pdf in enumerate(pdfs, 1):
        print(f"[{i}/{len(pdfs)}] {pdf.name}", flush=True)

        if args.skip_existing:
            existing = list(out_dir.glob(f"{pdf.stem}*.facts.json"))
            if existing:
                print(f"  (skipped — {existing[0].name} exists)", flush=True)
                skipped += 1
                continue

        result = process_pdf(pdf, provider, model, out_dir, args.max_tokens)
        if result is not None:
            successes += 1
        else:
            failures += 1

    elapsed = time.time() - started
    print()
    print(f"Done in {elapsed:.0f}s. {successes} succeeded, {failures} failed, {skipped} skipped.")
    if failures:
        sys.exit(1)


if __name__ == "__main__":
    main()
