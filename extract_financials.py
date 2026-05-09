"""DEPRECATED shim — kept so old `python3 extract_financials.py ...` invocations still work.

The real CLI lives in src/pdf_extraction/cli.py. Install the package with
`pip install -e .` and use the `extract-financials` console script, or run
`python -m pdf_extraction ...`.
"""

import sys
from pathlib import Path

# Make src/ importable when running this file without `pip install -e .`
sys.path.insert(0, str(Path(__file__).parent / "src"))

from pdf_extraction.cli import main

if __name__ == "__main__":
    main()
