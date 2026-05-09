"""LLM prompt builder. Pure function — no side effects."""

from .taxonomy import taxonomy_for_prompt


def build_prompt(pdf_filename: str) -> str:
    """Build the extraction prompt for a given source PDF filename."""
    return f"""You are an expert financial-data extractor. The attached PDF is an annual or interim financial report (10-K, 10-Q, 20-F, IFRS annual report, or similar). Extract every financial fact from it into a single XBRL-style JSON object.

OUTPUT SCHEMA (return exactly this structure, nothing else):

{{
  "entity": {{
    "name":                 "<legal name>",
    "ticker":               "<ticker if shown, else null>",
    "exchange":             "<NASDAQ, NYSE, LSE, Euronext, TSE, ... or null>",
    "cik":                  "<10-digit CIK if SEC filer, else null>",
    "country":              "<country of incorporation>",
    "fiscal_year_end":      "<MM-DD>",
    "reporting_currency":   "<USD/EUR/JPY/GBP/...>",
    "accounting_standard":  "<US-GAAP / IFRS / Other>"
  }},
  "filing": {{
    "form":           "<10-K, 20-F, Annual Report, etc.>",
    "fiscal_year":    <int>,
    "period_end":     "<YYYY-MM-DD>",
    "filing_date":    "<YYYY-MM-DD or null>",
    "auditor":        "<audit firm name or null>",
    "source_pdf":     "{pdf_filename}"
  }},
  "periods": {{
    "<period_id>": {{"type": "duration", "start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}},
    "<period_id>": {{"type": "instant",  "date":  "YYYY-MM-DD"}}
  }},
  "facts": [
    {{
      "canonical":  "<one of the canonical names listed below, or null>",
      "concept":    "<us-gaap:Revenues | ifrs:Revenue | custom:NetSalesIPhone>",
      "label":      "<line-item label EXACTLY as printed, in the original language>",
      "value":      <number, signs preserved>,
      "unit":       "<USD | EUR | JPY | shares | pure | percent | years | USD/share | ...>",
      "scale":      "<millions | thousands | billions | actual>",
      "period":     "<period_id from periods dict>",
      "statement":  "<IncomeStatement | BalanceSheet | CashFlow | ComprehensiveIncome | ShareholdersEquity | Note_<n>_<topic>>",
      "page":       <PDF page where the fact appears>,
      "dimensions": {{"<axis>": "<member>"}}     // optional
    }}
  ]
}}

NAMING RULES (THIS IS CRITICAL):
1. `canonical` — pick the BEST match from the canonical taxonomy below. If
   no canonical concept fits (e.g. company-specific KPI, niche disclosure),
   set `canonical` to null. Do NOT invent canonical names not in the list.
2. `concept` — the native taxonomy tag the company would use:
     us-gaap:* for US GAAP filings
     ifrs:*    for IFRS filings
     custom:*  for company-specific items (segments, product lines, non-GAAP)
3. `label` — the EXACT text printed in the report, including the original
   language (don't translate "Chiffre d'affaires" to "Revenue").

CANONICAL TAXONOMY (pick `canonical` only from these names):
{taxonomy_for_prompt()}

OTHER RULES:
4. Periods: define ONCE in the `periods` dict, then reference by id in each
   fact. Use ids like FY2024, FY2023, Q4_2024, instant_2024-09-28.
5. Values: preserve sign (negatives stay negative). Preserve the scale the
   report uses ('millions', 'thousands', 'billions', or 'actual'). NEVER
   multiply or normalize — keep the number EXACTLY as printed.
6. Statements: use one of the standard names above. For notes use
   `Note_<n>_<short_topic>` (e.g. Note_2_Revenue, Note_7_IncomeTaxes).
7. Dimensions: use for any axis that disaggregates a concept — segments,
   geography, product line, hedge designation. Omit the field if no
   dimensions apply.
8. Coverage: extract every numeric line in the primary statements AND every
   numeric table in the notes. Don't summarize.
9. Output ONLY the JSON. No prose, no markdown fences.
"""
