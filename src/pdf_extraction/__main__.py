"""Allow `python -m pdf_extraction ...` as an alternative to the `extract-financials` script."""

from .cli import main

if __name__ == "__main__":
    main()
