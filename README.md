# pdf-extraction

Extract XBRL-style financial facts from a folder of annual report PDFs (US 10-Ks, foreign 20-Fs, IFRS annual reports — anything with financial statements). One JSON file out per PDF in. Works with **Anthropic Claude**, **Google Gemini**, or **OpenAI GPT** as the underlying LLM.

## Project layout

```
pdf-extraction/
├── README.md
├── pyproject.toml             # package metadata + console-script entry point
├── requirements.txt           # alternative install path
├── .env.example               # template for API-key env vars
├── .gitignore
├── src/
│   └── pdf_extraction/        # the importable package
│       ├── __init__.py
│       ├── __main__.py        # enables `python -m pdf_extraction`
│       ├── cli.py             # argparse + batch loop
│       ├── extractor.py       # PDF → LLM → validated JSON file
│       ├── prompt.py          # extraction prompt
│       ├── taxonomy.py        # canonical taxonomy (134 concepts)
│       └── providers/
│           ├── __init__.py    # PROVIDERS registry
│           ├── base.py        # Provider abstract base class
│           ├── anthropic_provider.py
│           ├── google_provider.py
│           └── openai_provider.py
├── data/
│   ├── input/                 # drop your PDFs here
│   │   └── apple_fy2024_10k.pdf
│   └── output/                # JSON files land here
├── examples/
│   └── apple_fy2024_10k_facts.json   # reference output (hand-built)
└── reference/
    └── build_xbrl_json.py     # original Apple-only extractor (historical)
```

The two top-level files `extract_financials.py` and `canonical_taxonomy.py` are thin compatibility shims kept so old commands and imports still work — new code should use the package instead.

## How traceability works

Every fact carries three name fields:

| Field | What it is | Example |
|---|---|---|
| `canonical` | Standardized name from `taxonomy.py`. Same across all companies. **Use this for cross-company analysis.** | `Revenue` |
| `concept` | Native taxonomy tag the company uses (`us-gaap:*` / `ifrs:*` / `custom:*`). | `us-gaap:Revenues` |
| `label` | The line-item label EXACTLY as printed, in the original language. | `Total net sales` (Apple) · `Chiffre d'affaires` (a French filer) |

So if you ask "what's the revenue line for Apple, LVMH, and Toyota?", you can join on `canonical = "Revenue"` and still trace each row back to the original wording in the original report.

## Setup

1. **Install Python 3.10+**: `python3 --version`

2. **Create and activate a virtual environment** in the project folder:

   ```bash
   cd "/path/to/pdf extraction"
   python3 -m venv .venv
   source .venv/bin/activate          # macOS / Linux
   # .venv\Scripts\activate           # Windows PowerShell
   ```

   Your shell prompt should now show `(.venv)` at the start.

3. **Install the package** (in editable mode, with the SDK extras you want):

   ```bash
   pip install -e ".[anthropic]"      # just Anthropic
   pip install -e ".[google]"         # just Gemini
   pip install -e ".[openai]"         # just GPT
   pip install -e ".[all]"            # all three SDKs
   ```

   Editable mode (`-e`) means edits to files in `src/` take effect immediately without reinstalling.

4. **Set your API key(s).** Copy `.env.example` to `.env`, fill in the keys you need, then load them into your shell:

   ```bash
   cp .env.example .env
   # edit .env in your editor and paste the key(s)
   set -a; source .env; set +a       # macOS / Linux — loads .env for this shell session
   ```

   To make a key permanent across sessions, add `export ANTHROPIC_API_KEY=...` to `~/.zshrc` (macOS) or `~/.bashrc` (Linux). On Windows: `setx ANTHROPIC_API_KEY "sk-ant-..."` and reopen the shell.

### Re-using the venv later

```bash
cd "/path/to/pdf extraction"
source .venv/bin/activate
extract-financials data/input --out-dir data/output
```

`deactivate` returns your shell to the system Python.

## Usage

```bash
# Default: Anthropic Claude Sonnet
# If input folder is named 'input', output goes to a sibling 'output' folder.
extract-financials data/input

# Override the output folder explicitly
extract-financials data/input --out-dir my_results/

# Use Gemini Flash (cheapest)
extract-financials data/input --provider google --model flash

# Use GPT-5
extract-financials data/input --provider openai --model gpt5

# See what would run without spending API credits
extract-financials data/input --dry-run

# Resume after a crash — only processes PDFs without an existing JSON
extract-financials data/input --skip-existing

# Bigger output budget for very dense filings (default is 32000)
extract-financials data/input --max-tokens 64000
```

### Output behavior

* On success: writes `<TICKER>_FY<YEAR>.facts.json` to the output folder.
* If the model's response is wrapped in markdown fences or prose, the parser
  strips them and recovers the JSON automatically.
* If the response is **truncated** (model ran out of output budget), the parser
  recovers all complete facts and adds `"_truncated": true` to the file. The
  CLI prints a warning suggesting `--max-tokens 64000`. Re-run that filing
  with the higher budget to get the complete set.
* If the response is fundamentally unparseable, the raw text is dumped to
  `<out_dir>/_debug/<stem>.raw_response.txt` for inspection.

If you skipped step 3 above (`pip install -e .`), you can still run via the module path: `python -m pdf_extraction data/input`.

### Model aliases

| Provider | Aliases | Default | Underlying models |
|---|---|---|---|
| `anthropic` | `opus`, `sonnet`, `haiku` | `sonnet` | claude-opus-4-6, claude-sonnet-4-6, claude-haiku-4-5 |
| `google` | `pro`, `flash` | `flash` | gemini-2.5-pro, gemini-2.5-flash |
| `openai` | `gpt5`, `gpt5mini`, `gpt4o` | `gpt5mini` | gpt-5, gpt-5-mini, gpt-4o |

You can also pass any full model id (e.g. `--model claude-opus-4-6`) for models that aren't aliased.

## Output schema

```json
{
  "entity": {
    "name": "Apple Inc.", "ticker": "AAPL", "exchange": "NASDAQ",
    "cik": "0000320193", "country": "United States",
    "fiscal_year_end": "09-28", "reporting_currency": "USD",
    "accounting_standard": "US-GAAP"
  },
  "filing": {
    "form": "10-K", "fiscal_year": 2024, "period_end": "2024-09-28",
    "filing_date": "2024-11-01", "auditor": "Ernst & Young LLP",
    "source_pdf": "apple_fy2024_10k.pdf"
  },
  "periods": {
    "FY2024": {"type": "duration", "start": "2023-10-01", "end": "2024-09-28"},
    "instant_2024-09-28": {"type": "instant", "date": "2024-09-28"}
  },
  "facts": [
    {
      "canonical": "Revenue",
      "concept":   "us-gaap:Revenues",
      "label":     "Total net sales",
      "value":     391035,
      "unit":      "USD",
      "scale":     "millions",
      "period":    "FY2024",
      "statement": "IncomeStatement",
      "page":      29
    },
    {
      "canonical":  "SegmentRevenue",
      "concept":    "custom:SegmentNetSales",
      "label":      "Americas",
      "value":      167045,
      "unit":       "USD",
      "scale":      "millions",
      "period":     "FY2024",
      "statement":  "Note_13_Segments",
      "page":       47,
      "dimensions": {"Segment": "Americas"}
    }
  ]
}
```

A reference output (985 facts, hand-checked against the printed Apple 10-K) lives in `examples/apple_fy2024_10k_facts.json`.

## Cross-company analysis

The `canonical` field makes this kind of query trivial:

```python
import json, glob

filings = [json.load(open(p)) for p in glob.glob("data/output/*.facts.json")]

for f in filings:
    rev = next((x for x in f["facts"]
                if x["canonical"] == "Revenue"
                and x["period"] == f"FY{f['filing']['fiscal_year']}"
                and "dimensions" not in x), None)
    if rev:
        scale_mult = {"millions": 1e6, "thousands": 1e3, "billions": 1e9, "actual": 1}[rev["scale"]]
        in_currency = rev["value"] * scale_mult
        print(f"{f['entity']['name']:30s} {rev['label']:30s} {in_currency:>20,.0f} {rev['unit']}")
```

The `label` field tells you exactly how each company worded it (in the original language), so you can audit any unexpected match.

## Extending the canonical taxonomy

Open `src/pdf_extraction/taxonomy.py` and add an entry:

```python
TAXONOMY = {
    ...,
    "FreeCashFlow": "Operating cash flow minus capex (often presented in MD&A)",
}
```

The next run will let the LLM choose `FreeCashFlow`. If a fact has no good canonical match, the LLM sets `canonical: null` and you still have `concept` + `label` to work with.

## Cost (rough, per 100-page filing)

| Provider | Model | Cost |
|---|---|---|
| Anthropic | Opus 4.6 | $0.80–$1.50 |
| Anthropic | Sonnet 4.6 | $0.15–$0.40 |
| Anthropic | Haiku 4.5 | $0.03–$0.10 |
| Google | Gemini 2.5 Pro | $0.30–$0.60 |
| Google | Gemini 2.5 Flash | $0.05–$0.15 |
| OpenAI | GPT-5 | $0.50–$1.00 |
| OpenAI | GPT-5-mini | $0.10–$0.25 |

100 filings on Sonnet: ~$25. On Gemini Flash: ~$10.

## Limitations

1. **Output quality varies by provider.** Claude tends to be most thorough on note-level disclosures; Gemini Flash is fast and cheap but more likely to skip non-tabular notes; GPT-5 is in between. For a critical filing, run two providers and diff the outputs.

2. **Large PDFs may exceed per-request limits.** Files over ~32 MB or 200+ pages of dense text can hit provider caps. Split first with `qpdf` or `pdftk`.

3. **Canonical mapping isn't 100% deterministic.** The LLM occasionally picks `null` when a fact would actually fit a canonical name, or maps something inappropriately. The CLI logs any unknown canonical names per filing; spot-check the outputs the first few times.

4. **Errors fail open.** A failed PDF is logged and the batch continues. If the model returns invalid JSON, the raw response is dumped to `<stem>.RAW_RESPONSE.txt` next to the PDF for debugging. Re-run with `--skip-existing` to retry only failures.

## Tips

- Always `--dry-run` first against a new folder to confirm the right files are picked up.
- Default to `--provider google --model flash` for high-volume batches; escalate to `anthropic --model opus` only when you notice quality issues.
- After a batch, sanity-check counts across outputs:
  ```bash
  for f in data/output/*.facts.json; do
    echo -n "$f: "; jq '.facts | length' "$f"
  done
  ```

## Development

```bash
pip install -e ".[dev]"            # adds pytest + ruff
ruff check src/                    # lint
ruff format src/                   # format
```
