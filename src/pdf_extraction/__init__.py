"""pdf_extraction — extract XBRL-style financial facts from annual report PDFs."""

__version__ = "0.1.0"

from .taxonomy import TAXONOMY, canonical_names, taxonomy_for_prompt
from .extractor import process_pdf

__all__ = ["TAXONOMY", "canonical_names", "taxonomy_for_prompt", "process_pdf", "__version__"]
