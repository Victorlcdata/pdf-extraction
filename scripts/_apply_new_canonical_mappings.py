"""Update the static concept→canonical map for the 56 new canonicals just added.

The default `build_concept_map.py` re-run would only touch tags not already in
the map (idempotent — by design). But the new canonicals mean some *existing*
entries (currently `canonical: null`) should now map to one of the new names.

This script applies those specific updates directly, much faster and cheaper
than another LLM pass through 3,400 tags. Each entry below is a precise tag →
new-canonical assignment composed by reading the new taxonomy entries against
the candidate us-gaap tags.

Run-and-discard.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from build_concept_map import write_markdown  # noqa: E402
from pdf_extraction.taxonomy import TAXONOMY  # noqa: E402

TAX_DIR = ROOT / "data" / "taxonomies"

# Each entry: (us-gaap tag, new canonical, note)
# Compositional rule: only override entries whose us-gaap tag clearly fits the new canonical.
# We deliberately don't touch ambiguous cases — the LLM's null verdict stays.

US_GAAP_UPDATES: list[tuple[str, str, str]] = [
    # Banking — direct concept name matches
    ("NetInterestIncome", "NetInterestIncome", "Direct match for net interest income."),
    ("InterestAndFeeIncomeLoans", "InterestAndFeeIncomeLoans", "Direct match — interest+fee income on loans."),
    ("InterestAndDividendIncome", "InterestAndDividendIncomeTotal", "Direct match — total interest+dividend income."),
    ("InterestIncomeDeposits", "InterestIncomeFromDeposits", "Interest income on bank-owned deposits."),
    ("InterestExpenseDeposits", "InterestExpenseDeposits", "Direct match — interest paid on deposit liabilities."),
    ("OtherNoninterestIncome", "OtherNoninterestIncome", "Direct match — other non-interest income."),
    ("TrustAndInvestmentManagementIncome", "TrustAndInvestmentManagementIncome", "Direct match — trust/wealth management income."),
    ("OccupancyExpense", "OccupancyExpense", "Direct match — occupancy expense."),
    ("GainLossOnSaleOfLoans", "GainLossOnSaleOfLoans", "Direct match — net gain/loss on sale of loans."),
    ("ProvisionForLoanLeaseAndOtherCreditLosses", "ProvisionForCreditLosses", "Provision for expected credit losses (CECL)."),
    ("AllowanceForCreditLosses", "AllowanceForCreditLosses", "Direct match — allowance for credit losses."),
    ("LoansAndLeasesReceivable", "LoansAndLeasesReceivable", "Direct match — gross loans+leases receivable."),
    ("LoansAndLeasesReceivableHeldForSale", "LoansAndLeasesReceivableHeldForSale", "Direct match — loans held for sale."),
    ("NetLoansAndLeasesReceivable", "NetLoansAndLeasesReceivable", "Direct match — loans net of allowance."),
    ("Deposits", "DepositsTotal", "Total deposit liabilities (bank funding)."),
    ("InterestBearingDeposits", "InterestBearingDeposits", "Direct match — interest-bearing deposits."),
    ("NoninterestBearingDeposits", "NoninterestBearingDeposits", "Direct match — non-interest-bearing deposits."),
    ("FederalHomeLoanBankAdvances", "FederalHomeLoanBankAdvances", "Direct match — FHLB advances."),

    # Sector-specific revenue / expense
    ("LicenseRevenue", "LicenseRevenue", "Software / IP license revenue."),
    ("MaintenanceAndSupportRevenue", "MaintenanceAndSupportRevenue", "Software maintenance/support revenue."),
    ("ProfessionalServicesRevenue", "ProfessionalServicesRevenue", "Consulting/professional services revenue."),
    ("FuelAndOilExpense", "FuelAndOilExpense", "Aircraft fuel and oil expense."),

    # Cross-company gaps
    ("Depreciation", "Depreciation", "Depreciation only (separate from amortization)."),
    ("RestrictedCash", "RestrictedCash", "Restricted cash (period type disambiguates current/noncurrent)."),
    ("ForeignCurrencyTransactionGainLoss", "ForeignCurrencyTransactionGainLoss", "Realized FX gain/loss on P&L."),
    ("WeightedAverageInterestRate", "WeightedAverageInterestRate", "Weighted-average interest rate on debt."),
    ("WorkingCapital", "WorkingCapital", "Working capital (current assets − current liabilities)."),
    ("ContractualObligations", "ContractualObligations", "Total contractual obligations disclosure."),
    ("UnconditionalPurchaseObligations", "PurchaseObligations", "Unconditional purchase commitments."),
    ("CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents", "CashAndCashEquivalentsAndRestrictedCash", "Combined cash + restricted cash (CF reconciliation)."),
    ("CommitmentsAndContingencies", "CommitmentsAndContingencies", "Commitments and contingencies BS line."),
    ("ConstructionInProgress", "ConstructionInProgress", "Construction in progress (PP&E component)."),
    ("Investments", "Investments", "Total investments (bank/insurer BS line)."),
    ("Warrants", "Warrants", "Warrant liability (BS)."),
    ("AvailableForSaleSecurities", "AvailableForSaleSecurities", "Available-for-sale securities BS line."),

    # Cash flow & P&L
    ("ImpairmentOfLongLivedAssets", "ImpairmentOfLongLivedAssets", "Impairment of long-lived assets."),
    ("LaborAndRelatedExpense", "LaborAndRelatedExpense", "Total labor / payroll line on income statement."),
    ("PensionAndOtherPostretirementBenefitExpense", "PensionExpense", "Pension / post-retirement benefit expense."),
    ("PensionPlanContributions", "PensionContributions", "Cash contributions to defined-benefit pension plans."),
    ("DividendIncome", "DividendIncome", "Dividend income (P&L investment income)."),
    ("IncomeLossFromEquityMethodInvestments", "IncomeFromEquityMethodInvestments", "Equity-method income (P&L below the line)."),
    ("GainLossOnSaleOfPropertyAndEquipment", "GainLossOnSaleOfPropertyAndEquipment", "Gain/loss on PP&E disposals."),
    ("InterestCapitalized", "InterestCapitalized", "Capitalized interest."),
    ("RepurchasedAndRetiredStockAveragePricePerShare", "AverageBuybackPricePerShare", "Average price paid per share repurchased."),
    ("IssuerRepurchasesOfEquitySecuritiesAveragePricePaidPerShare", "AverageBuybackPricePerShare", "Average price paid per share repurchased (alias)."),
    ("PaymentsToAcquireCommonStockAveragePricePerShare", "AverageBuybackPricePerShare", "Average price paid per share repurchased (alias)."),

    # NCI / equity activity
    ("CapitalContributionsFromNoncontrollingInterest", "CapitalContributionsFromMinority", "Capital contributions from NCI."),
    ("DistributionsToNoncontrollingInterest", "DistributionsToMinority", "Distributions to NCI."),
    ("DividendsPaidToNoncontrollingInterests", "DividendsPaidToMinority", "Dividends paid to NCI."),
    ("ComprehensiveIncomeNetOfTaxAttributableToParent", "ComprehensiveIncomeAttributableToParent", "Comprehensive income attributable to parent."),
    ("ComprehensiveIncomeNetOfTaxAttributableToNoncontrollingInterest", "ComprehensiveIncomeAttributableToMinority", "Comprehensive income attributable to NCI."),
    ("WithholdingOfStockForTaxPurposes", "SharesWithheldForTaxes", "Shares withheld at vesting for taxes."),
    ("StockIssuedBySubsidiaryOrConsolidatedAffiliateEmployeeTaxShareWithholding", "SharesWithheldForTaxes", "Same concept (alternate us-gaap tag)."),
]


def main() -> None:
    json_path = TAX_DIR / "concept_canonical_map.json"
    cmap = json.loads(json_path.read_text())
    valid_canonicals = set(TAXONOMY.keys())

    # Also extend us-gaap.txt with any tags we're adding to the map that
    # weren't in our seed-filer union. Without this, the validator would
    # flag these tags as "concept_invalid" on future extractions.
    us_gaap_txt_path = TAX_DIR / "us-gaap.txt"
    us_gaap_tags = {t.strip() for t in us_gaap_txt_path.read_text().splitlines() if t.strip()}

    updated = 0
    added = 0
    skipped_bad_canonical = []

    for tag, new_canonical, note in US_GAAP_UPDATES:
        if new_canonical not in valid_canonicals:
            skipped_bad_canonical.append((tag, new_canonical))
            continue
        # Ensure the tag is in our authoritative list
        us_gaap_tags.add(tag)
        entry = cmap.get("us-gaap", {}).get(tag)
        if entry is None:
            cmap.setdefault("us-gaap", {})[tag] = {"canonical": new_canonical, "note": note}
            added += 1
            print(f"  [ADD]      {tag:60s}                                → {new_canonical}")
            continue
        old = entry.get("canonical")
        if old == new_canonical:
            continue  # already correct
        cmap["us-gaap"][tag] = {"canonical": new_canonical, "note": note}
        updated += 1
        print(f"  [REMAP]    {tag:60s}  {old!s:30s} → {new_canonical}")

    # Rewrite us-gaap.txt sorted
    us_gaap_txt_path.write_text("\n".join(sorted(us_gaap_tags)) + "\n")
    print(f"\nus-gaap.txt: {len(us_gaap_tags):,} tags (rewrote with any new additions)")

    json_path.write_text(json.dumps(cmap, indent=2, ensure_ascii=False))
    print()
    print(f"Static map: {updated} re-mapped, {added} newly added in {json_path.relative_to(ROOT)}")
    if skipped_bad_canonical:
        print(f"  [WARN] {len(skipped_bad_canonical)} bad-canonical mapping(s) skipped: {skipped_bad_canonical}")

    # Regenerate markdown
    by_ns = {
        ns: [{"tag": tag, **vals} for tag, vals in cmap.get(ns, {}).items()]
        for ns in ["us-gaap", "ifrs-full", "dei"]
    }
    md_path = TAX_DIR / "concept_canonical_map.md"
    write_markdown(
        by_ns,
        md_path,
        token_totals={ns: {"input_tokens": 0, "output_tokens": 0} for ns in by_ns},
        provider="google/gemini-2.5-pro + claude/opus-4.7 hand-tuned",
        model="(mixed)",
    )
    print(f"  wrote {md_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
