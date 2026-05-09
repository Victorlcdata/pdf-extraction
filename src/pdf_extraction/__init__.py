"""pdf_extraction — extract XBRL-style financial facts from annual report PDFs."""

__version__ = "0.1.0"

from .extractor import ExtractionOutcome, process_pdf
from .run_log import RunLogger
from .taxonomy import TAXONOMY, canonical_names, taxonomy_for_prompt

__all__ = [
    "TAXONOMY",
    "canonical_names",
    "taxonomy_for_prompt",
    "process_pdf",
    "ExtractionOutcome",
    "RunLogger",
    "__version__",
]
