"""DEPRECATED shim — taxonomy moved to src/pdf_extraction/taxonomy.py.

This file re-exports the public names so any old `from canonical_taxonomy import ...`
imports keep working. New code should import directly from the package:

    from pdf_extraction.taxonomy import TAXONOMY, canonical_names, taxonomy_for_prompt
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from pdf_extraction.taxonomy import (  # noqa: F401  re-export
    TAXONOMY,
    canonical_names,
    taxonomy_for_prompt,
)
