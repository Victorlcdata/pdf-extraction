"""Build XBRL-style JSON facts from Apple FY2024 10-K.

All values are as-reported (raw, not standardized). Numbers preserved at the
scale the company reported them ('millions', 'thousands', 'dollars', 'percent',
'shares', 'years'). Each fact has:
    concept   – tag name (us-gaap-style where reasonable, custom: prefix otherwise)
    label     – Apple's line-item label as printed
    value     – the numeric value (negative where parentheses were shown)
    unit      – USD / shares / pure (ratio) / percent / years / EUR
    scale     – millions / thousands / actual
    period    – key into the periods dict
    statement – which financial statement / note the fact came from
    page      – PDF page (filing page, as printed)
"""

import json
from pathlib import Path

OUT = Path("/sessions/zen-nice-carson/mnt/pdf extraction/apple_fy2024_10k_facts.json")

doc = {
    "entity": {
        "name": "Apple Inc.",
        "cik": "0000320193",
        "ticker": "AAPL",
        "exchange": "NASDAQ",
        "irs_employer_id": "94-2404110",
        "state_of_incorporation": "California",
        "address": "One Apple Park Way, Cupertino, California 95014",
        "phone": "(408) 996-1010",
        "fiscal_year_end_month_day": "09-28",
    },
    "filing": {
        "form": "10-K",
        "accession_number": "0000320193-24-000123",
        "fiscal_year": 2024,
        "filing_date": "2024-11-01",
        "period_end": "2024-09-28",
        "auditor": "Ernst & Young LLP",
        "auditor_since": 2009,
        "auditor_location": "San Jose, California",
        "auditor_report_date": "2024-11-01",
        "shareholders_of_record_date": "2024-10-18",
        "shareholders_of_record": 23301,
        "source_pdf": "Apple Inc. 2024 Form 10-K (121 pages)",
    },
    "periods": {
        "FY2024": {
            "type": "duration",
            "start": "2023-10-01",
            "end": "2024-09-28",
            "weeks": 52,
        },
        "FY2023": {
            "type": "duration",
            "start": "2022-09-25",
            "end": "2023-09-30",
            "weeks": 53,
        },
        "FY2022": {
            "type": "duration",
            "start": "2021-09-26",
            "end": "2022-09-24",
            "weeks": 52,
        },
        "Q4_2024": {"type": "duration", "start": "2024-06-30", "end": "2024-09-28"},
        "instant_2024-09-28": {"type": "instant", "date": "2024-09-28"},
        "instant_2023-09-30": {"type": "instant", "date": "2023-09-30"},
        "instant_2022-09-24": {"type": "instant", "date": "2022-09-24"},
        "instant_2021-09-25": {"type": "instant", "date": "2021-09-25"},
        # Stock performance (calendar)
        "instant_2019-09": {"type": "instant", "date": "2019-09-27"},
        "instant_2020-09": {"type": "instant", "date": "2020-09-25"},
        "instant_2021-09": {"type": "instant", "date": "2021-09-24"},
        "instant_2022-09": {"type": "instant", "date": "2022-09-23"},
        "instant_2023-09": {"type": "instant", "date": "2023-09-29"},
        "instant_2024-09": {"type": "instant", "date": "2024-09-27"},
    },
    "facts": [],
}

facts = doc["facts"]


def add(concept, label, value, unit, scale, period, statement, page, dim=None):
    """Append a fact. dim is an optional dict of axis: member pairs (segments etc.)."""
    f = {
        "concept": concept,
        "label": label,
        "value": value,
        "unit": unit,
        "scale": scale,
        "period": period,
        "statement": statement,
        "page": page,
    }
    if dim:
        f["dimensions"] = dim
    facts.append(f)


# =====================================================================
# CONSOLIDATED STATEMENTS OF OPERATIONS  (page 29)
# =====================================================================
S = "IncomeStatement"
P = 29
# (concept, label, FY24, FY23, FY22)
income_rows = [
    (
        "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTaxProducts",
        "Net sales - Products",
        294866,
        298085,
        316199,
    ),
    (
        "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTaxServices",
        "Net sales - Services",
        96169,
        85200,
        78129,
    ),
    ("us-gaap:Revenues", "Total net sales", 391035, 383285, 394328),
    ("us-gaap:CostOfGoodsSold", "Cost of sales - Products", 185233, 189282, 201471),
    ("us-gaap:CostOfServicesSold", "Cost of sales - Services", 25119, 24855, 22075),
    ("us-gaap:CostOfRevenue", "Total cost of sales", 210352, 214137, 223546),
    ("us-gaap:GrossProfit", "Gross margin", 180683, 169148, 170782),
    (
        "us-gaap:ResearchAndDevelopmentExpense",
        "Research and development",
        31370,
        29915,
        26251,
    ),
    (
        "us-gaap:SellingGeneralAndAdministrativeExpense",
        "Selling, general and administrative",
        26097,
        24932,
        25094,
    ),
    ("us-gaap:OperatingExpenses", "Total operating expenses", 57467, 54847, 51345),
    ("us-gaap:OperatingIncomeLoss", "Operating income", 123216, 114301, 119437),
    (
        "us-gaap:NonoperatingIncomeExpense",
        "Other income/(expense), net",
        269,
        -565,
        -334,
    ),
    (
        "us-gaap:IncomeLossFromContinuingOperationsBeforeIncomeTaxes",
        "Income before provision for income taxes",
        123485,
        113736,
        119103,
    ),
    (
        "us-gaap:IncomeTaxExpenseBenefit",
        "Provision for income taxes",
        29749,
        16741,
        19300,
    ),
    ("us-gaap:NetIncomeLoss", "Net income", 93736, 96995, 99803),
]
for c, lbl, v24, v23, v22 in income_rows:
    add(c, lbl, v24, "USD", "millions", "FY2024", S, P)
    add(c, lbl, v23, "USD", "millions", "FY2023", S, P)
    add(c, lbl, v22, "USD", "millions", "FY2022", S, P)

# EPS and share counts
eps_rows = [
    (
        "us-gaap:EarningsPerShareBasic",
        "Earnings per share - Basic",
        6.11,
        6.16,
        6.15,
        "USD/share",
        "actual",
    ),
    (
        "us-gaap:EarningsPerShareDiluted",
        "Earnings per share - Diluted",
        6.08,
        6.13,
        6.11,
        "USD/share",
        "actual",
    ),
    (
        "us-gaap:WeightedAverageNumberOfSharesOutstandingBasic",
        "Shares used in computing EPS - Basic",
        15343783,
        15744231,
        16215963,
        "shares",
        "thousands",
    ),
    (
        "us-gaap:WeightedAverageNumberOfDilutedSharesOutstanding",
        "Shares used in computing EPS - Diluted",
        15408095,
        15812547,
        16325819,
        "shares",
        "thousands",
    ),
]
for c, lbl, v24, v23, v22, u, sc in eps_rows:
    add(c, lbl, v24, u, sc, "FY2024", S, P)
    add(c, lbl, v23, u, sc, "FY2023", S, P)
    add(c, lbl, v22, u, sc, "FY2022", S, P)


# =====================================================================
# CONSOLIDATED STATEMENTS OF COMPREHENSIVE INCOME (page 30)
# =====================================================================
S = "ComprehensiveIncome"
P = 30
oci_rows = [
    ("us-gaap:NetIncomeLoss", "Net income", 93736, 96995, 99803),
    (
        "us-gaap:OtherComprehensiveIncomeForeignCurrencyTransactionAndTranslationAdjustmentNetOfTax",
        "Change in foreign currency translation, net of tax",
        395,
        -765,
        -1511,
    ),
    (
        "us-gaap:OtherComprehensiveIncomeUnrealizedGainLossOnDerivativesArisingDuringPeriodNetOfTax",
        "Change in fair value of derivative instruments",
        -832,
        323,
        3212,
    ),
    (
        "us-gaap:OtherComprehensiveIncomeLossReclassificationAdjustmentFromAOCIOnDerivativesNetOfTax",
        "Adjustment for net (gains)/losses realized and included in net income (derivatives)",
        -1337,
        -1717,
        -1074,
    ),
    (
        "custom:TotalChangeInUnrealizedGainsLossesOnDerivatives",
        "Total change in unrealized gains/losses on derivative instruments",
        -2169,
        -1394,
        2138,
    ),
    (
        "us-gaap:OtherComprehensiveIncomeUnrealizedHoldingGainLossOnSecuritiesArisingDuringPeriodNetOfTax",
        "Change in fair value of marketable debt securities",
        5850,
        1563,
        -12104,
    ),
    (
        "us-gaap:OtherComprehensiveIncomeLossReclassificationAdjustmentFromAOCIForSaleOfSecuritiesNetOfTax",
        "Adjustment for net (gains)/losses realized and included in net income (debt securities)",
        204,
        253,
        205,
    ),
    (
        "custom:TotalChangeInUnrealizedGainsLossesOnMarketableDebtSecurities",
        "Total change in unrealized gains/losses on marketable debt securities",
        6054,
        1816,
        -11899,
    ),
    (
        "us-gaap:OtherComprehensiveIncomeLossNetOfTax",
        "Total other comprehensive income/(loss)",
        4280,
        -343,
        -11272,
    ),
    (
        "us-gaap:ComprehensiveIncomeNetOfTax",
        "Total comprehensive income",
        98016,
        96652,
        88531,
    ),
]
for c, lbl, v24, v23, v22 in oci_rows:
    add(c, lbl, v24, "USD", "millions", "FY2024", S, P)
    add(c, lbl, v23, "USD", "millions", "FY2023", S, P)
    add(c, lbl, v22, "USD", "millions", "FY2022", S, P)


# =====================================================================
# CONSOLIDATED BALANCE SHEETS (page 31)
# =====================================================================
S = "BalanceSheet"
P = 31
bs_rows = [
    # current assets
    (
        "us-gaap:CashAndCashEquivalentsAtCarryingValue",
        "Cash and cash equivalents",
        29943,
        29965,
    ),
    (
        "us-gaap:MarketableSecuritiesCurrent",
        "Marketable securities - current",
        35228,
        31590,
    ),
    ("us-gaap:AccountsReceivableNetCurrent", "Accounts receivable, net", 33410, 29508),
    ("custom:VendorNonTradeReceivables", "Vendor non-trade receivables", 32833, 31477),
    ("us-gaap:InventoryNet", "Inventories", 7286, 6331),
    ("us-gaap:OtherAssetsCurrent", "Other current assets", 14287, 14695),
    ("us-gaap:AssetsCurrent", "Total current assets", 152987, 143566),
    # non-current
    (
        "us-gaap:MarketableSecuritiesNoncurrent",
        "Marketable securities - non-current",
        91479,
        100544,
    ),
    (
        "us-gaap:PropertyPlantAndEquipmentNet",
        "Property, plant and equipment, net",
        45680,
        43715,
    ),
    ("us-gaap:OtherAssetsNoncurrent", "Other non-current assets", 74834, 64758),
    ("us-gaap:AssetsNoncurrent", "Total non-current assets", 211993, 209017),
    ("us-gaap:Assets", "Total assets", 364980, 352583),
    # current liabilities
    ("us-gaap:AccountsPayableCurrent", "Accounts payable", 68960, 62611),
    ("us-gaap:OtherLiabilitiesCurrent", "Other current liabilities", 78304, 58829),
    (
        "us-gaap:ContractWithCustomerLiabilityCurrent",
        "Deferred revenue - current",
        8249,
        8061,
    ),
    ("us-gaap:CommercialPaper", "Commercial paper", 9967, 5985),
    ("us-gaap:LongTermDebtCurrent", "Term debt - current", 10912, 9822),
    ("us-gaap:LiabilitiesCurrent", "Total current liabilities", 176392, 145308),
    # non-current liabilities
    ("us-gaap:LongTermDebtNoncurrent", "Term debt - non-current", 85750, 95281),
    (
        "us-gaap:OtherLiabilitiesNoncurrent",
        "Other non-current liabilities",
        45888,
        49848,
    ),
    ("us-gaap:LiabilitiesNoncurrent", "Total non-current liabilities", 131638, 145129),
    ("us-gaap:Liabilities", "Total liabilities", 308030, 290437),
    # equity
    (
        "us-gaap:CommonStocksIncludingAdditionalPaidInCapital",
        "Common stock and additional paid-in capital",
        83276,
        73812,
    ),
    ("us-gaap:RetainedEarningsAccumulatedDeficit", "Accumulated deficit", -19154, -214),
    (
        "us-gaap:AccumulatedOtherComprehensiveIncomeLossNetOfTax",
        "Accumulated other comprehensive loss",
        -7172,
        -11452,
    ),
    ("us-gaap:StockholdersEquity", "Total shareholders' equity", 56950, 62146),
    (
        "us-gaap:LiabilitiesAndStockholdersEquity",
        "Total liabilities and shareholders' equity",
        364980,
        352583,
    ),
]
for c, lbl, v24, v23 in bs_rows:
    add(c, lbl, v24, "USD", "millions", "instant_2024-09-28", S, P)
    add(c, lbl, v23, "USD", "millions", "instant_2023-09-30", S, P)

# share information from balance sheet header
add(
    "us-gaap:CommonStockSharesAuthorized",
    "Common stock shares authorized",
    50400000,
    "shares",
    "thousands",
    "instant_2024-09-28",
    S,
    P,
)
add(
    "us-gaap:CommonStockSharesAuthorized",
    "Common stock shares authorized",
    50400000,
    "shares",
    "thousands",
    "instant_2023-09-30",
    S,
    P,
)
add(
    "us-gaap:CommonStockSharesIssued",
    "Common stock shares issued and outstanding",
    15116786,
    "shares",
    "thousands",
    "instant_2024-09-28",
    S,
    P,
)
add(
    "us-gaap:CommonStockSharesIssued",
    "Common stock shares issued and outstanding",
    15550061,
    "shares",
    "thousands",
    "instant_2023-09-30",
    S,
    P,
)
add(
    "us-gaap:CommonStockParOrStatedValuePerShare",
    "Common stock par value per share",
    0.00001,
    "USD/share",
    "actual",
    "instant_2024-09-28",
    S,
    P,
)
add(
    "us-gaap:CommonStockParOrStatedValuePerShare",
    "Common stock par value per share",
    0.00001,
    "USD/share",
    "actual",
    "instant_2023-09-30",
    S,
    P,
)


# =====================================================================
# STATEMENT OF SHAREHOLDERS' EQUITY (page 32)
# =====================================================================
S = "ShareholdersEquity"
P = 32
# Total equity rollforward
eq_rows = [
    # (concept, label, FY24, FY23, FY22)
    (
        "custom:TotalShareholdersEquityBeginning",
        "Total shareholders' equity, beginning balance",
        62146,
        50672,
        63090,
    ),
    # Common stock & APIC
    (
        "custom:CommonStockAPICBeginning",
        "Common stock and APIC, beginning",
        73812,
        64849,
        57365,
    ),
    (
        "us-gaap:StockIssuedDuringPeriodValueNewIssues",
        "Common stock issued",
        1423,
        1346,
        1175,
    ),
    (
        "custom:CommonStockWithheldNetShareSettlement",
        "Common stock withheld related to net share settlement of equity awards (APIC impact)",
        -3993,
        -3521,
        -2971,
    ),
    (
        "us-gaap:ShareBasedCompensation",
        "Share-based compensation (APIC)",
        12034,
        11138,
        9280,
    ),
    (
        "custom:CommonStockAPICEnding",
        "Common stock and APIC, ending",
        83276,
        73812,
        64849,
    ),
    # Retained earnings / accumulated deficit
    (
        "custom:RetainedEarningsBeginning",
        "Retained earnings/(Accumulated deficit), beginning",
        -214,
        -3068,
        5562,
    ),
    ("us-gaap:NetIncomeLoss", "Net income (RE rollforward)", 93736, 96995, 99803),
    (
        "us-gaap:DividendsCommonStockCash",
        "Dividends and dividend equivalents declared",
        -15218,
        -14996,
        -14793,
    ),
    (
        "custom:CommonStockWithheldRESettlement",
        "Common stock withheld related to net share settlement of equity awards (RE impact)",
        -1612,
        -2099,
        -3454,
    ),
    (
        "us-gaap:StockRepurchasedAndRetiredDuringPeriodValue",
        "Common stock repurchased (RE impact)",
        -95846,
        -77046,
        -90186,
    ),
    (
        "custom:RetainedEarningsEnding",
        "Retained earnings/(Accumulated deficit), ending",
        -19154,
        -214,
        -3068,
    ),
    # AOCI
    (
        "custom:AOCIBeginning",
        "Accumulated other comprehensive income/(loss), beginning",
        -11452,
        -11109,
        163,
    ),
    (
        "us-gaap:OtherComprehensiveIncomeLossNetOfTax",
        "Other comprehensive income/(loss) (equity rollforward)",
        4280,
        -343,
        -11272,
    ),
    (
        "custom:AOCIEnding",
        "Accumulated other comprehensive income/(loss), ending",
        -7172,
        -11452,
        -11109,
    ),
    (
        "custom:TotalShareholdersEquityEnding",
        "Total shareholders' equity, ending balance",
        56950,
        62146,
        50672,
    ),
]
for c, lbl, v24, v23, v22 in eq_rows:
    add(c, lbl, v24, "USD", "millions", "FY2024", S, P)
    add(c, lbl, v23, "USD", "millions", "FY2023", S, P)
    add(c, lbl, v22, "USD", "millions", "FY2022", S, P)

# Dividends per share
add(
    "us-gaap:CommonStockDividendsPerShareDeclared",
    "Dividends and dividend equivalents declared per share or RSU",
    0.98,
    "USD/share",
    "actual",
    "FY2024",
    S,
    P,
)
add(
    "us-gaap:CommonStockDividendsPerShareDeclared",
    "Dividends and dividend equivalents declared per share or RSU",
    0.94,
    "USD/share",
    "actual",
    "FY2023",
    S,
    P,
)
add(
    "us-gaap:CommonStockDividendsPerShareDeclared",
    "Dividends and dividend equivalents declared per share or RSU",
    0.90,
    "USD/share",
    "actual",
    "FY2022",
    S,
    P,
)


# =====================================================================
# CONSOLIDATED STATEMENTS OF CASH FLOWS (page 33)
# =====================================================================
S = "CashFlow"
P = 33
cf_rows = [
    (
        "us-gaap:CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents",
        "Cash, cash equivalents, and restricted cash and cash equivalents - beginning",
        30737,
        24977,
        35929,
    ),
    ("us-gaap:NetIncomeLoss", "Net income (CF)", 93736, 96995, 99803),
    (
        "us-gaap:DepreciationDepletionAndAmortization",
        "Depreciation and amortization",
        11445,
        11519,
        11104,
    ),
    (
        "us-gaap:ShareBasedCompensation",
        "Share-based compensation expense (CF)",
        11688,
        10833,
        9038,
    ),
    (
        "custom:OtherAdjustmentsToNetIncome",
        "Other adjustments to net income",
        -2266,
        -2227,
        1006,
    ),
    (
        "us-gaap:IncreaseDecreaseInAccountsReceivable",
        "Change in accounts receivable, net",
        -3788,
        -1688,
        -1823,
    ),
    (
        "custom:IncreaseDecreaseInVendorNonTradeReceivables",
        "Change in vendor non-trade receivables",
        -1356,
        1271,
        -7520,
    ),
    (
        "us-gaap:IncreaseDecreaseInInventories",
        "Change in inventories",
        -1046,
        -1618,
        1484,
    ),
    (
        "custom:IncreaseDecreaseInOtherCurrentAndNonCurrentAssets",
        "Change in other current and non-current assets",
        -11731,
        -5684,
        -6499,
    ),
    (
        "us-gaap:IncreaseDecreaseInAccountsPayable",
        "Change in accounts payable",
        6020,
        -1889,
        9448,
    ),
    (
        "custom:IncreaseDecreaseInOtherCurrentAndNonCurrentLiabilities",
        "Change in other current and non-current liabilities",
        15552,
        3031,
        6110,
    ),
    (
        "us-gaap:NetCashProvidedByUsedInOperatingActivities",
        "Cash generated by operating activities",
        118254,
        110543,
        122151,
    ),
    # Investing
    (
        "us-gaap:PaymentsToAcquireMarketableSecurities",
        "Purchases of marketable securities",
        -48656,
        -29513,
        -76923,
    ),
    (
        "us-gaap:ProceedsFromMaturitiesPrepaymentsAndCallsOfAvailableForSaleSecurities",
        "Proceeds from maturities of marketable securities",
        51211,
        39686,
        29917,
    ),
    (
        "us-gaap:ProceedsFromSaleOfAvailableForSaleSecurities",
        "Proceeds from sales of marketable securities",
        11135,
        5828,
        37446,
    ),
    (
        "us-gaap:PaymentsToAcquirePropertyPlantAndEquipment",
        "Payments for acquisition of property, plant and equipment",
        -9447,
        -10959,
        -10708,
    ),
    (
        "custom:OtherInvestingActivities",
        "Other investing activities",
        -1308,
        -1337,
        -2086,
    ),
    (
        "us-gaap:NetCashProvidedByUsedInInvestingActivities",
        "Cash generated by/(used in) investing activities",
        2935,
        3705,
        -22354,
    ),
    # Financing
    (
        "custom:PaymentsForTaxesNetShareSettlement",
        "Payments for taxes related to net share settlement of equity awards",
        -5441,
        -5431,
        -6223,
    ),
    (
        "us-gaap:PaymentsOfDividendsCommonStock",
        "Payments for dividends and dividend equivalents",
        -15234,
        -15025,
        -14841,
    ),
    (
        "us-gaap:PaymentsForRepurchaseOfCommonStock",
        "Repurchases of common stock",
        -94949,
        -77550,
        -89402,
    ),
    (
        "us-gaap:ProceedsFromIssuanceOfLongTermDebt",
        "Proceeds from issuance of term debt, net",
        0,
        5228,
        5465,
    ),
    (
        "us-gaap:RepaymentsOfLongTermDebt",
        "Repayments of term debt",
        -9958,
        -11151,
        -9543,
    ),
    (
        "custom:NetProceedsRepaymentsCommercialPaper",
        "Proceeds from/(Repayments of) commercial paper, net",
        3960,
        -3978,
        3955,
    ),
    ("custom:OtherFinancingActivities", "Other financing activities", -361, -581, -160),
    (
        "us-gaap:NetCashProvidedByUsedInFinancingActivities",
        "Cash used in financing activities",
        -121983,
        -108488,
        -110749,
    ),
    (
        "us-gaap:CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsPeriodIncreaseDecreaseIncludingExchangeRateEffect",
        "Increase/(Decrease) in cash, cash equivalents, and restricted cash",
        -794,
        5760,
        -10952,
    ),
    (
        "us-gaap:CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsEnding",
        "Cash, cash equivalents, and restricted cash - ending",
        29943,
        30737,
        24977,
    ),
    (
        "us-gaap:IncomeTaxesPaidNet",
        "Cash paid for income taxes, net",
        26102,
        18679,
        19573,
    ),
]
for c, lbl, v24, v23, v22 in cf_rows:
    add(c, lbl, v24, "USD", "millions", "FY2024", S, P)
    add(c, lbl, v23, "USD", "millions", "FY2023", S, P)
    add(c, lbl, v22, "USD", "millions", "FY2022", S, P)


# =====================================================================
# NOTE 2 — REVENUE (page 35)
# =====================================================================
S = "Note2_Revenue"
P = 35
# Revenue by product/service line
rev_lines = [
    ("custom:NetSalesIPhone", "iPhone", 201183, 200583, 205489),
    ("custom:NetSalesMac", "Mac", 29984, 29357, 40177),
    ("custom:NetSalesIPad", "iPad", 26694, 28300, 29292),
    (
        "custom:NetSalesWearables",
        "Wearables, Home and Accessories",
        37005,
        39845,
        41241,
    ),
    ("custom:NetSalesServices", "Services", 96169, 85200, 78129),
    ("us-gaap:Revenues", "Total net sales", 391035, 383285, 394328),
]
for c, lbl, v24, v23, v22 in rev_lines:
    add(c, lbl, v24, "USD", "millions", "FY2024", S, P, dim={"ProductOrServiceAxis": lbl})
    add(c, lbl, v23, "USD", "millions", "FY2023", S, P, dim={"ProductOrServiceAxis": lbl})
    add(c, lbl, v22, "USD", "millions", "FY2022", S, P, dim={"ProductOrServiceAxis": lbl})

# Deferred revenue color
add(
    "us-gaap:ContractWithCustomerLiability",
    "Total deferred revenue",
    12800,
    "USD",
    "millions",
    "instant_2024-09-28",
    S,
    P,
)
add(
    "us-gaap:ContractWithCustomerLiability",
    "Total deferred revenue",
    12100,
    "USD",
    "millions",
    "instant_2023-09-30",
    S,
    P,
)
add(
    "custom:RevenueRecognizedFromOpeningDeferredRevenue",
    "Revenue recognized that was in deferred revenue at start of period",
    7700,
    "USD",
    "millions",
    "FY2024",
    S,
    P,
)
add(
    "custom:RevenueRecognizedFromOpeningDeferredRevenue",
    "Revenue recognized that was in deferred revenue at start of period",
    8200,
    "USD",
    "millions",
    "FY2023",
    S,
    P,
)
add(
    "custom:RevenueRecognizedFromOpeningDeferredRevenue",
    "Revenue recognized that was in deferred revenue at start of period",
    7500,
    "USD",
    "millions",
    "FY2022",
    S,
    P,
)
# Performance obligation maturity
add(
    "custom:DeferredRevenueExpectedRecognitionLessThan1Yr",
    "Deferred revenue expected to be realized in less than 1 year",
    0.64,
    "pure",
    "actual",
    "instant_2024-09-28",
    S,
    P,
)
add(
    "custom:DeferredRevenueExpectedRecognition1To2Yr",
    "Deferred revenue expected to be realized within 1-2 years",
    0.25,
    "pure",
    "actual",
    "instant_2024-09-28",
    S,
    P,
)
add(
    "custom:DeferredRevenueExpectedRecognition2To3Yr",
    "Deferred revenue expected to be realized within 2-3 years",
    0.09,
    "pure",
    "actual",
    "instant_2024-09-28",
    S,
    P,
)
add(
    "custom:DeferredRevenueExpectedRecognitionGreaterThan3Yr",
    "Deferred revenue expected to be realized in greater than 3 years",
    0.02,
    "pure",
    "actual",
    "instant_2024-09-28",
    S,
    P,
)


# =====================================================================
# NOTE 3 — EARNINGS PER SHARE (page 35)
# =====================================================================
S = "Note3_EPS"
P = 35
add(
    "us-gaap:NetIncomeLoss",
    "Numerator: Net income",
    93736,
    "USD",
    "millions",
    "FY2024",
    S,
    P,
)
add(
    "us-gaap:NetIncomeLoss",
    "Numerator: Net income",
    96995,
    "USD",
    "millions",
    "FY2023",
    S,
    P,
)
add(
    "us-gaap:NetIncomeLoss",
    "Numerator: Net income",
    99803,
    "USD",
    "millions",
    "FY2022",
    S,
    P,
)
add(
    "us-gaap:WeightedAverageNumberOfSharesOutstandingBasic",
    "Weighted-average basic shares outstanding",
    15343783,
    "shares",
    "thousands",
    "FY2024",
    S,
    P,
)
add(
    "us-gaap:WeightedAverageNumberOfSharesOutstandingBasic",
    "Weighted-average basic shares outstanding",
    15744231,
    "shares",
    "thousands",
    "FY2023",
    S,
    P,
)
add(
    "us-gaap:WeightedAverageNumberOfSharesOutstandingBasic",
    "Weighted-average basic shares outstanding",
    16215963,
    "shares",
    "thousands",
    "FY2022",
    S,
    P,
)
add(
    "us-gaap:IncrementalCommonSharesAttributableToShareBasedPaymentArrangements",
    "Effect of dilutive share-based awards",
    64312,
    "shares",
    "thousands",
    "FY2024",
    S,
    P,
)
add(
    "us-gaap:IncrementalCommonSharesAttributableToShareBasedPaymentArrangements",
    "Effect of dilutive share-based awards",
    68316,
    "shares",
    "thousands",
    "FY2023",
    S,
    P,
)
add(
    "us-gaap:IncrementalCommonSharesAttributableToShareBasedPaymentArrangements",
    "Effect of dilutive share-based awards",
    109856,
    "shares",
    "thousands",
    "FY2022",
    S,
    P,
)
add(
    "us-gaap:WeightedAverageNumberOfDilutedSharesOutstanding",
    "Weighted-average diluted shares",
    15408095,
    "shares",
    "thousands",
    "FY2024",
    S,
    P,
)
add(
    "us-gaap:WeightedAverageNumberOfDilutedSharesOutstanding",
    "Weighted-average diluted shares",
    15812547,
    "shares",
    "thousands",
    "FY2023",
    S,
    P,
)
add(
    "us-gaap:WeightedAverageNumberOfDilutedSharesOutstanding",
    "Weighted-average diluted shares",
    16325819,
    "shares",
    "thousands",
    "FY2022",
    S,
    P,
)
add(
    "us-gaap:EarningsPerShareBasic",
    "Basic EPS",
    6.11,
    "USD/share",
    "actual",
    "FY2024",
    S,
    P,
)
add(
    "us-gaap:EarningsPerShareBasic",
    "Basic EPS",
    6.16,
    "USD/share",
    "actual",
    "FY2023",
    S,
    P,
)
add(
    "us-gaap:EarningsPerShareBasic",
    "Basic EPS",
    6.15,
    "USD/share",
    "actual",
    "FY2022",
    S,
    P,
)
add(
    "us-gaap:EarningsPerShareDiluted",
    "Diluted EPS",
    6.08,
    "USD/share",
    "actual",
    "FY2024",
    S,
    P,
)
add(
    "us-gaap:EarningsPerShareDiluted",
    "Diluted EPS",
    6.13,
    "USD/share",
    "actual",
    "FY2023",
    S,
    P,
)
add(
    "us-gaap:EarningsPerShareDiluted",
    "Diluted EPS",
    6.11,
    "USD/share",
    "actual",
    "FY2022",
    S,
    P,
)
add(
    "us-gaap:AntidilutiveSecuritiesExcludedFromComputationOfEarningsPerShareAmount",
    "RSUs excluded as antidilutive",
    24,
    "shares",
    "millions",
    "FY2023",
    S,
    P,
)


# =====================================================================
# NOTE 4 — FINANCIAL INSTRUMENTS (pages 36-38)
# =====================================================================
S = "Note4_FinancialInstruments"
# 2024 investment portfolio (page 36)
P = 36
inv24 = [
    # (label, adj_cost, unrealized_gain, unrealized_loss, fair_value, cce, current_ms, noncurrent_ms)
    ("Cash", 27199, 0, 0, 27199, 27199, 0, 0),
    ("Money market funds (Level 1)", 778, 0, 0, 778, 778, 0, 0),
    ("Mutual funds (Level 1)", 515, 105, -3, 617, 0, 617, 0),
    ("Level 1 subtotal", 1293, 105, -3, 1395, 778, 617, 0),
    ("U.S. Treasury securities (Level 2)", 16150, 45, -516, 15679, 212, 4087, 11380),
    ("U.S. agency securities (Level 2)", 5431, 0, -272, 5159, 155, 703, 4301),
    (
        "Non-U.S. government securities (Level 2)",
        17959,
        93,
        -484,
        17568,
        1158,
        10810,
        5600,
    ),
    (
        "Certificates of deposit and time deposits (Level 2)",
        873,
        0,
        0,
        873,
        387,
        478,
        8,
    ),
    ("Commercial paper (Level 2)", 1066, 0, 0, 1066, 28, 1038, 0),
    ("Corporate debt securities (Level 2)", 65622, 270, -1953, 63939, 26, 16027, 47886),
    ("Municipal securities (Level 2)", 412, 0, -7, 405, 0, 190, 215),
    (
        "Mortgage- and asset-backed securities (Level 2)",
        24595,
        175,
        -1403,
        23367,
        0,
        1278,
        22089,
    ),
    ("Level 2 subtotal", 132108, 583, -4635, 128056, 1966, 34611, 91479),
    ("Total investments", 160600, 688, -4638, 156650, 29943, 35228, 91479),
]
for label, ac, ug, ul, fv, cce, cms, nms in inv24:
    dim = {"InvestmentSecurityCategory": label}
    add(
        "us-gaap:AvailableForSaleSecuritiesAmortizedCost",
        f"{label} - Adjusted Cost",
        ac,
        "USD",
        "millions",
        "instant_2024-09-28",
        S,
        P,
        dim,
    )
    add(
        "us-gaap:AvailableForSaleSecuritiesAccumulatedGrossUnrealizedGainBeforeTax",
        f"{label} - Unrealized Gains",
        ug,
        "USD",
        "millions",
        "instant_2024-09-28",
        S,
        P,
        dim,
    )
    add(
        "us-gaap:AvailableForSaleSecuritiesAccumulatedGrossUnrealizedLossBeforeTax",
        f"{label} - Unrealized Losses",
        ul,
        "USD",
        "millions",
        "instant_2024-09-28",
        S,
        P,
        dim,
    )
    add(
        "us-gaap:AvailableForSaleSecurities",
        f"{label} - Fair Value",
        fv,
        "USD",
        "millions",
        "instant_2024-09-28",
        S,
        P,
        dim,
    )
    add(
        "us-gaap:CashAndCashEquivalentsAtCarryingValueComponent",
        f"{label} - Cash and Cash Equivalents",
        cce,
        "USD",
        "millions",
        "instant_2024-09-28",
        S,
        P,
        dim,
    )
    add(
        "us-gaap:MarketableSecuritiesCurrentComponent",
        f"{label} - Current Marketable Securities",
        cms,
        "USD",
        "millions",
        "instant_2024-09-28",
        S,
        P,
        dim,
    )
    add(
        "us-gaap:MarketableSecuritiesNoncurrentComponent",
        f"{label} - Non-current Marketable Securities",
        nms,
        "USD",
        "millions",
        "instant_2024-09-28",
        S,
        P,
        dim,
    )

# 2023 portfolio (page 37)
P = 37
inv23 = [
    ("Cash", 28359, 0, 0, 28359, 28359, 0, 0),
    ("Money market funds (Level 1)", 481, 0, 0, 481, 481, 0, 0),
    ("Mutual funds and equity securities (Level 1)", 442, 12, -26, 428, 0, 428, 0),
    ("Level 1 subtotal", 923, 12, -26, 909, 481, 428, 0),
    ("U.S. Treasury securities (Level 2)", 19406, 0, -1292, 18114, 35, 5468, 12611),
    ("U.S. agency securities (Level 2)", 5736, 0, -600, 5136, 36, 271, 4829),
    (
        "Non-U.S. government securities (Level 2)",
        17533,
        6,
        -1048,
        16491,
        0,
        11332,
        5159,
    ),
    (
        "Certificates of deposit and time deposits (Level 2)",
        1354,
        0,
        0,
        1354,
        1034,
        320,
        0,
    ),
    ("Commercial paper (Level 2)", 608, 0, 0, 608, 0, 608, 0),
    ("Corporate debt securities (Level 2)", 76840, 6, -5956, 70890, 20, 12627, 58243),
    ("Municipal securities (Level 2)", 628, 0, -26, 602, 0, 192, 410),
    (
        "Mortgage- and asset-backed securities (Level 2)",
        22365,
        6,
        -2735,
        19636,
        0,
        344,
        19292,
    ),
    ("Level 2 subtotal", 144470, 18, -11657, 132831, 1125, 31162, 100544),
    ("Total investments", 173752, 30, -11683, 162099, 29965, 31590, 100544),
]
for label, ac, ug, ul, fv, cce, cms, nms in inv23:
    dim = {"InvestmentSecurityCategory": label}
    add(
        "us-gaap:AvailableForSaleSecuritiesAmortizedCost",
        f"{label} - Adjusted Cost",
        ac,
        "USD",
        "millions",
        "instant_2023-09-30",
        S,
        P,
        dim,
    )
    add(
        "us-gaap:AvailableForSaleSecuritiesAccumulatedGrossUnrealizedGainBeforeTax",
        f"{label} - Unrealized Gains",
        ug,
        "USD",
        "millions",
        "instant_2023-09-30",
        S,
        P,
        dim,
    )
    add(
        "us-gaap:AvailableForSaleSecuritiesAccumulatedGrossUnrealizedLossBeforeTax",
        f"{label} - Unrealized Losses",
        ul,
        "USD",
        "millions",
        "instant_2023-09-30",
        S,
        P,
        dim,
    )
    add(
        "us-gaap:AvailableForSaleSecurities",
        f"{label} - Fair Value",
        fv,
        "USD",
        "millions",
        "instant_2023-09-30",
        S,
        P,
        dim,
    )
    add(
        "us-gaap:CashAndCashEquivalentsAtCarryingValueComponent",
        f"{label} - Cash and Cash Equivalents",
        cce,
        "USD",
        "millions",
        "instant_2023-09-30",
        S,
        P,
        dim,
    )
    add(
        "us-gaap:MarketableSecuritiesCurrentComponent",
        f"{label} - Current Marketable Securities",
        cms,
        "USD",
        "millions",
        "instant_2023-09-30",
        S,
        P,
        dim,
    )
    add(
        "us-gaap:MarketableSecuritiesNoncurrentComponent",
        f"{label} - Non-current Marketable Securities",
        nms,
        "USD",
        "millions",
        "instant_2023-09-30",
        S,
        P,
        dim,
    )

# Restricted balances
add(
    "custom:RestrictedCashEscrow",
    "Cash held in escrow (State Aid)",
    2600,
    "USD",
    "millions",
    "instant_2024-09-28",
    S,
    36,
)
add(
    "custom:RestrictedMarketableSecuritiesEscrow",
    "Marketable securities held in escrow",
    13200,
    "USD",
    "millions",
    "instant_2024-09-28",
    S,
    36,
)
add(
    "custom:RestrictedMarketableSecuritiesEscrow",
    "Marketable securities held in escrow",
    13800,
    "USD",
    "millions",
    "instant_2023-09-30",
    S,
    36,
)

# Derivative notional amounts (page 37)
P = 37
add(
    "us-gaap:DerivativeNotionalAmount",
    "FX contracts (designated as accounting hedges)",
    64069,
    "USD",
    "millions",
    "instant_2024-09-28",
    S,
    P,
    {"HedgingDesignation": "Designated", "Type": "FX"},
)
add(
    "us-gaap:DerivativeNotionalAmount",
    "FX contracts (designated as accounting hedges)",
    74730,
    "USD",
    "millions",
    "instant_2023-09-30",
    S,
    P,
    {"HedgingDesignation": "Designated", "Type": "FX"},
)
add(
    "us-gaap:DerivativeNotionalAmount",
    "Interest rate contracts (designated as accounting hedges)",
    14575,
    "USD",
    "millions",
    "instant_2024-09-28",
    S,
    P,
    {"HedgingDesignation": "Designated", "Type": "InterestRate"},
)
add(
    "us-gaap:DerivativeNotionalAmount",
    "Interest rate contracts (designated as accounting hedges)",
    19375,
    "USD",
    "millions",
    "instant_2023-09-30",
    S,
    P,
    {"HedgingDesignation": "Designated", "Type": "InterestRate"},
)
add(
    "us-gaap:DerivativeNotionalAmount",
    "FX contracts (not designated)",
    91493,
    "USD",
    "millions",
    "instant_2024-09-28",
    S,
    P,
    {"HedgingDesignation": "NotDesignated", "Type": "FX"},
)
add(
    "us-gaap:DerivativeNotionalAmount",
    "FX contracts (not designated)",
    104777,
    "USD",
    "millions",
    "instant_2023-09-30",
    S,
    P,
    {"HedgingDesignation": "NotDesignated", "Type": "FX"},
)

# Hedged item carrying amounts
add(
    "custom:HedgedAssetMarketableSecuritiesFairValueHedge",
    "Marketable securities in fair value hedge - carrying amount",
    0,
    "USD",
    "millions",
    "instant_2024-09-28",
    S,
    P,
)
add(
    "custom:HedgedAssetMarketableSecuritiesFairValueHedge",
    "Marketable securities in fair value hedge - carrying amount",
    14433,
    "USD",
    "millions",
    "instant_2023-09-30",
    S,
    P,
)
add(
    "custom:HedgedLiabilityTermDebtFairValueHedge",
    "Term debt in fair value hedge - carrying amount",
    -13505,
    "USD",
    "millions",
    "instant_2024-09-28",
    S,
    P,
)
add(
    "custom:HedgedLiabilityTermDebtFairValueHedge",
    "Term debt in fair value hedge - carrying amount",
    -18247,
    "USD",
    "millions",
    "instant_2023-09-30",
    S,
    P,
)

# Concentrations
add(
    "custom:CellularCarrierTradeReceivablesConcentration",
    "Third-party cellular carrier % of trade receivables",
    0.38,
    "pure",
    "actual",
    "instant_2024-09-28",
    S,
    38,
)
add(
    "custom:CellularCarrierTradeReceivablesConcentration",
    "Third-party cellular carrier % of trade receivables",
    0.41,
    "pure",
    "actual",
    "instant_2023-09-30",
    S,
    38,
)
add(
    "custom:VendorConcentration1NonTradeReceivables",
    "Top vendor % of vendor non-trade receivables",
    0.44,
    "pure",
    "actual",
    "instant_2024-09-28",
    S,
    38,
)
add(
    "custom:VendorConcentration2NonTradeReceivables",
    "2nd vendor % of vendor non-trade receivables",
    0.23,
    "pure",
    "actual",
    "instant_2024-09-28",
    S,
    38,
)
add(
    "custom:VendorConcentration1NonTradeReceivables",
    "Top vendor % of vendor non-trade receivables",
    0.48,
    "pure",
    "actual",
    "instant_2023-09-30",
    S,
    38,
)
add(
    "custom:VendorConcentration2NonTradeReceivables",
    "2nd vendor % of vendor non-trade receivables",
    0.23,
    "pure",
    "actual",
    "instant_2023-09-30",
    S,
    38,
)


# =====================================================================
# NOTE 5 — PROPERTY, PLANT AND EQUIPMENT (page 39)
# =====================================================================
S = "Note5_PPE"
P = 39
ppe = [
    ("us-gaap:LandAndBuildings", "Land and buildings", 24690, 23446),
    (
        "us-gaap:MachineryAndEquipmentGross",
        "Machinery, equipment and internal-use software",
        80205,
        78314,
    ),
    ("us-gaap:LeaseholdImprovementsGross", "Leasehold improvements", 14233, 12839),
    (
        "us-gaap:PropertyPlantAndEquipmentGross",
        "Gross property, plant and equipment",
        119128,
        114599,
    ),
    (
        "us-gaap:AccumulatedDepreciationDepletionAndAmortizationPropertyPlantAndEquipment",
        "Accumulated depreciation",
        -73448,
        -70884,
    ),
    (
        "us-gaap:PropertyPlantAndEquipmentNet",
        "Total property, plant and equipment, net",
        45680,
        43715,
    ),
]
for c, lbl, v24, v23 in ppe:
    add(c, lbl, v24, "USD", "millions", "instant_2024-09-28", S, P)
    add(c, lbl, v23, "USD", "millions", "instant_2023-09-30", S, P)
add(
    "us-gaap:Depreciation",
    "Depreciation expense on PPE",
    8200,
    "USD",
    "millions",
    "FY2024",
    S,
    P,
)
add(
    "us-gaap:Depreciation",
    "Depreciation expense on PPE",
    8500,
    "USD",
    "millions",
    "FY2023",
    S,
    P,
)
add(
    "us-gaap:Depreciation",
    "Depreciation expense on PPE",
    8700,
    "USD",
    "millions",
    "FY2022",
    S,
    P,
)


# =====================================================================
# NOTE 6 — CONSOLIDATED FINANCIAL STATEMENT DETAILS (page 39)
# =====================================================================
S = "Note6_StatementDetails"
P = 39
ona = [
    ("us-gaap:DeferredIncomeTaxAssetsNet", "Deferred tax assets", 19499, 17852),
    (
        "custom:OtherNonCurrentAssetsRemainder",
        "Other non-current assets (residual)",
        55335,
        46906,
    ),
    ("us-gaap:OtherAssetsNoncurrent", "Total other non-current assets", 74834, 64758),
]
for c, lbl, v24, v23 in ona:
    add(
        c,
        lbl,
        v24,
        "USD",
        "millions",
        "instant_2024-09-28",
        S,
        P,
        {"BalanceSheetLocation": "OtherNonCurrentAssets"},
    )
    add(
        c,
        lbl,
        v23,
        "USD",
        "millions",
        "instant_2023-09-30",
        S,
        P,
        {"BalanceSheetLocation": "OtherNonCurrentAssets"},
    )
ocl = [
    (
        "us-gaap:AccruedIncomeTaxesCurrent",
        "Income taxes payable - current",
        26601,
        8819,
    ),
    (
        "custom:OtherCurrentLiabilitiesRemainder",
        "Other current liabilities (residual)",
        51703,
        50010,
    ),
    (
        "us-gaap:OtherLiabilitiesCurrent",
        "Total other current liabilities",
        78304,
        58829,
    ),
]
for c, lbl, v24, v23 in ocl:
    add(
        c,
        lbl,
        v24,
        "USD",
        "millions",
        "instant_2024-09-28",
        S,
        P,
        {"BalanceSheetLocation": "OtherCurrentLiabilities"},
    )
    add(
        c,
        lbl,
        v23,
        "USD",
        "millions",
        "instant_2023-09-30",
        S,
        P,
        {"BalanceSheetLocation": "OtherCurrentLiabilities"},
    )
onl = [
    (
        "us-gaap:AccruedIncomeTaxesNoncurrent",
        "Income taxes payable - non-current",
        9254,
        15457,
    ),
    (
        "custom:OtherNonCurrentLiabilitiesRemainder",
        "Other non-current liabilities (residual)",
        36634,
        34391,
    ),
    (
        "us-gaap:OtherLiabilitiesNoncurrent",
        "Total other non-current liabilities",
        45888,
        49848,
    ),
]
for c, lbl, v24, v23 in onl:
    add(
        c,
        lbl,
        v24,
        "USD",
        "millions",
        "instant_2024-09-28",
        S,
        P,
        {"BalanceSheetLocation": "OtherNonCurrentLiabilities"},
    )
    add(
        c,
        lbl,
        v23,
        "USD",
        "millions",
        "instant_2023-09-30",
        S,
        P,
        {"BalanceSheetLocation": "OtherNonCurrentLiabilities"},
    )


# =====================================================================
# NOTE 7 — INCOME TAXES (pages 39-41)
# =====================================================================
S = "Note7_IncomeTaxes"
P = 40
# Provision for income taxes - by jurisdiction and current/deferred
tax = [
    ("custom:CurrentFederalIncomeTax", "Federal current", 5571, 9445, 7890),
    ("custom:DeferredFederalIncomeTax", "Federal deferred", -3080, -3644, -2265),
    ("us-gaap:CurrentFederalTaxExpenseBenefit", "Federal total", 2491, 5801, 5625),
    ("custom:CurrentStateIncomeTax", "State current", 1726, 1570, 1519),
    ("custom:DeferredStateIncomeTax", "State deferred", -298, -49, 84),
    ("us-gaap:CurrentStateAndLocalTaxExpenseBenefit", "State total", 1428, 1521, 1603),
    ("us-gaap:CurrentForeignTaxExpenseBenefit", "Foreign current", 25483, 8750, 8996),
    (
        "us-gaap:DeferredForeignIncomeTaxExpenseBenefit",
        "Foreign deferred",
        347,
        669,
        3076,
    ),
    ("custom:TotalForeignIncomeTax", "Foreign total", 25830, 9419, 12072),
    (
        "us-gaap:IncomeTaxExpenseBenefit",
        "Provision for income taxes",
        29749,
        16741,
        19300,
    ),
]
for c, lbl, v24, v23, v22 in tax:
    add(c, lbl, v24, "USD", "millions", "FY2024", S, P)
    add(c, lbl, v23, "USD", "millions", "FY2023", S, P)
    add(c, lbl, v22, "USD", "millions", "FY2022", S, P)

add(
    "us-gaap:IncomeLossFromContinuingOperationsBeforeIncomeTaxesForeign",
    "Foreign pretax earnings",
    77300,
    "USD",
    "millions",
    "FY2024",
    S,
    P,
)
add(
    "us-gaap:IncomeLossFromContinuingOperationsBeforeIncomeTaxesForeign",
    "Foreign pretax earnings",
    72900,
    "USD",
    "millions",
    "FY2023",
    S,
    P,
)
add(
    "us-gaap:IncomeLossFromContinuingOperationsBeforeIncomeTaxesForeign",
    "Foreign pretax earnings",
    71300,
    "USD",
    "millions",
    "FY2022",
    S,
    P,
)

# ETR reconciliation
recon = [
    (
        "us-gaap:IncomeTaxReconciliationIncomeTaxExpenseBenefitAtFederalStatutoryIncomeTaxRate",
        "Computed expected tax",
        25932,
        23885,
        25012,
    ),
    (
        "us-gaap:IncomeTaxReconciliationStateAndLocalIncomeTaxes",
        "State taxes, net of federal effect",
        1162,
        1124,
        1518,
    ),
    (
        "custom:IncomeTaxReconStateAidImpact",
        "Impact of the State Aid Decision",
        10246,
        0,
        0,
    ),
    (
        "us-gaap:IncomeTaxReconciliationForeignIncomeTaxRateDifferential",
        "Earnings of foreign subsidiaries",
        -5311,
        -5744,
        -4366,
    ),
    (
        "us-gaap:IncomeTaxReconciliationTaxCreditsResearch",
        "R&D credit, net",
        -1397,
        -1212,
        -1153,
    ),
    (
        "custom:IncomeTaxReconExcessTaxBenefitsEquityAwards",
        "Excess tax benefits from equity awards",
        -893,
        -1120,
        -1871,
    ),
    ("us-gaap:IncomeTaxReconciliationOtherAdjustments", "Other", 10, -192, 160),
    (
        "us-gaap:IncomeTaxExpenseBenefit",
        "Provision for income taxes (recon)",
        29749,
        16741,
        19300,
    ),
]
for c, lbl, v24, v23, v22 in recon:
    add(c, lbl, v24, "USD", "millions", "FY2024", S, P)
    add(c, lbl, v23, "USD", "millions", "FY2023", S, P)
    add(c, lbl, v22, "USD", "millions", "FY2022", S, P)
add(
    "us-gaap:EffectiveIncomeTaxRateContinuingOperations",
    "Effective tax rate",
    0.241,
    "pure",
    "actual",
    "FY2024",
    S,
    P,
)
add(
    "us-gaap:EffectiveIncomeTaxRateContinuingOperations",
    "Effective tax rate",
    0.147,
    "pure",
    "actual",
    "FY2023",
    S,
    P,
)
add(
    "us-gaap:EffectiveIncomeTaxRateContinuingOperations",
    "Effective tax rate",
    0.162,
    "pure",
    "actual",
    "FY2022",
    S,
    P,
)
add(
    "us-gaap:FederalIncomeTaxRateContinuingOperations",
    "Statutory federal rate",
    0.21,
    "pure",
    "actual",
    "FY2024",
    S,
    P,
)
add(
    "us-gaap:FederalIncomeTaxRateContinuingOperations",
    "Statutory federal rate",
    0.21,
    "pure",
    "actual",
    "FY2023",
    S,
    P,
)
add(
    "us-gaap:FederalIncomeTaxRateContinuingOperations",
    "Statutory federal rate",
    0.21,
    "pure",
    "actual",
    "FY2022",
    S,
    P,
)

# Deferred tax components
P = 41
dta = [
    ("custom:DTACapitalizedRD", "DTA: Capitalized R&D", 10739, 6294),
    (
        "us-gaap:DeferredTaxAssetsTaxCreditCarryforwards",
        "DTA: Tax credit carryforwards",
        8856,
        8302,
    ),
    (
        "custom:DTAAccruedLiabsAndReserves",
        "DTA: Accrued liabilities and other reserves",
        6114,
        6365,
    ),
    ("custom:DTADeferredRevenue", "DTA: Deferred revenue", 3413, 4571),
    ("us-gaap:DeferredTaxAssetsLeaseLiabilities", "DTA: Lease liabilities", 2410, 2421),
    ("custom:DTAUnrealizedLosses", "DTA: Unrealized losses", 1173, 2447),
    ("custom:DTAOther", "DTA: Other", 2168, 2343),
    (
        "us-gaap:DeferredTaxAssetsGross",
        "Total deferred tax assets - gross",
        34873,
        32743,
    ),
    (
        "us-gaap:DeferredTaxAssetsValuationAllowance",
        "Valuation allowance",
        -8866,
        -8374,
    ),
    ("us-gaap:DeferredTaxAssetsNet", "Total deferred tax assets, net", 26007, 24369),
    ("custom:DTLDepreciation", "DTL: Depreciation", 2551, 1998),
    ("custom:DTLRightOfUseAssets", "DTL: Right-of-use assets", 2125, 2179),
    (
        "custom:DTLMinimumTaxOnForeignEarnings",
        "DTL: Minimum tax on foreign earnings",
        1674,
        1940,
    ),
    ("custom:DTLUnrealizedGains", "DTL: Unrealized gains", 0, 511),
    ("custom:DTLOther", "DTL: Other", 455, 490),
    ("us-gaap:DeferredTaxLiabilities", "Total deferred tax liabilities", 6805, 7118),
    (
        "us-gaap:DeferredTaxAssetsLiabilitiesNet",
        "Net deferred tax assets",
        19202,
        17251,
    ),
]
for c, lbl, v24, v23 in dta:
    add(c, lbl, v24, "USD", "millions", "instant_2024-09-28", S, P)
    add(c, lbl, v23, "USD", "millions", "instant_2023-09-30", S, P)
add(
    "custom:ForeignTaxCreditCarryforwardsIreland",
    "Foreign tax credit carryforwards (Ireland)",
    5100,
    "USD",
    "millions",
    "instant_2024-09-28",
    S,
    P,
)
add(
    "custom:CaliforniaRDCreditCarryforwards",
    "California R&D credit carryforwards",
    3600,
    "USD",
    "millions",
    "instant_2024-09-28",
    S,
    P,
)

# UTP rollforward
utp = [
    ("us-gaap:UnrecognizedTaxBenefits", "UTB beginning balance", 19454, 16758, 15477),
    (
        "us-gaap:UnrecognizedTaxBenefitsIncreasesResultingFromPriorPeriodTaxPositions",
        "UTB increases - prior years",
        1727,
        2044,
        2284,
    ),
    (
        "us-gaap:UnrecognizedTaxBenefitsDecreasesResultingFromPriorPeriodTaxPositions",
        "UTB decreases - prior years",
        -386,
        -1463,
        -1982,
    ),
    (
        "us-gaap:UnrecognizedTaxBenefitsIncreasesResultingFromCurrentPeriodTaxPositions",
        "UTB increases - current year",
        2542,
        2628,
        1936,
    ),
    (
        "us-gaap:UnrecognizedTaxBenefitsDecreasesResultingFromSettlementsWithTaxingAuthorities",
        "UTB settlements",
        -1070,
        -19,
        -28,
    ),
    (
        "us-gaap:UnrecognizedTaxBenefitsReductionsResultingFromLapseOfApplicableStatuteOfLimitations",
        "UTB statute of limitations expirations",
        -229,
        -494,
        -929,
    ),
    ("us-gaap:UnrecognizedTaxBenefits", "UTB ending balance", 22038, 19454, 16758),
]
for c, lbl, v24, v23, v22 in utp:
    add(c, lbl, v24, "USD", "millions", "FY2024", S, P)
    add(c, lbl, v23, "USD", "millions", "FY2023", S, P)
    add(c, lbl, v22, "USD", "millions", "FY2022", S, P)
add(
    "us-gaap:UnrecognizedTaxBenefitsThatWouldImpactEffectiveTaxRate",
    "UTB that would impact ETR",
    10800,
    "USD",
    "millions",
    "instant_2024-09-28",
    S,
    P,
)
add(
    "us-gaap:UnrecognizedTaxBenefitsThatWouldImpactEffectiveTaxRate",
    "UTB that would impact ETR",
    9500,
    "USD",
    "millions",
    "instant_2023-09-30",
    S,
    P,
)

# State Aid Decision
add(
    "custom:StateAidRecoveryAmount",
    "State Aid Decision adjusted recovery amount",
    12.7,
    "EUR",
    "billions",
    "instant_2024-09-28",
    S,
    39,
)
add(
    "custom:StateAidInterest",
    "State Aid Decision interest",
    1.2,
    "EUR",
    "billions",
    "instant_2024-09-28",
    S,
    39,
)
add(
    "custom:StateAidEscrowBalanceEUR",
    "State Aid Decision escrow balance (EUR)",
    14.2,
    "EUR",
    "billions",
    "instant_2024-09-28",
    S,
    39,
)
add(
    "custom:StateAidEscrowBalanceUSD",
    "State Aid Decision escrow balance (USD)",
    15.8,
    "USD",
    "billions",
    "instant_2024-09-28",
    S,
    39,
)
add(
    "custom:StateAidOneTimeChargeNet",
    "State Aid Decision one-time net income tax charge (Q4 FY24)",
    10.2,
    "USD",
    "billions",
    "Q4_2024",
    S,
    39,
)
add(
    "custom:StateAidUSForeignTaxCredit",
    "State Aid - U.S. foreign tax credit offset",
    4.8,
    "USD",
    "billions",
    "Q4_2024",
    S,
    39,
)
add(
    "custom:StateAidDecreaseUTB",
    "State Aid - decrease in unrecognized tax benefits",
    823,
    "USD",
    "millions",
    "Q4_2024",
    S,
    39,
)


# =====================================================================
# NOTE 8 — LEASES (page 42)
# =====================================================================
S = "Note8_Leases"
P = 42
add(
    "us-gaap:OperatingLeaseCost",
    "Lease cost - fixed payments on operating leases",
    2000,
    "USD",
    "millions",
    "FY2024",
    S,
    P,
)
add(
    "us-gaap:OperatingLeaseCost",
    "Lease cost - fixed payments on operating leases",
    2000,
    "USD",
    "millions",
    "FY2023",
    S,
    P,
)
add(
    "us-gaap:OperatingLeaseCost",
    "Lease cost - fixed payments on operating leases",
    1900,
    "USD",
    "millions",
    "FY2022",
    S,
    P,
)
add(
    "us-gaap:VariableLeaseCost",
    "Variable lease cost",
    13800,
    "USD",
    "millions",
    "FY2024",
    S,
    P,
)
add(
    "us-gaap:VariableLeaseCost",
    "Variable lease cost",
    13900,
    "USD",
    "millions",
    "FY2023",
    S,
    P,
)
add(
    "us-gaap:VariableLeaseCost",
    "Variable lease cost",
    14900,
    "USD",
    "millions",
    "FY2022",
    S,
    P,
)
add(
    "us-gaap:OperatingLeasePayments",
    "Fixed cash payments related to operating leases",
    1900,
    "USD",
    "millions",
    "FY2024",
    S,
    P,
)
add(
    "us-gaap:OperatingLeasePayments",
    "Fixed cash payments related to operating leases",
    1900,
    "USD",
    "millions",
    "FY2023",
    S,
    P,
)
add(
    "us-gaap:OperatingLeasePayments",
    "Fixed cash payments related to operating leases",
    1800,
    "USD",
    "millions",
    "FY2022",
    S,
    P,
)
add(
    "us-gaap:RightOfUseAssetObtainedInExchangeForOperatingLeaseLiability",
    "ROU assets obtained for lease liabilities",
    1000,
    "USD",
    "millions",
    "FY2024",
    S,
    P,
)
add(
    "us-gaap:RightOfUseAssetObtainedInExchangeForOperatingLeaseLiability",
    "ROU assets obtained for lease liabilities",
    2100,
    "USD",
    "millions",
    "FY2023",
    S,
    P,
)
add(
    "us-gaap:RightOfUseAssetObtainedInExchangeForOperatingLeaseLiability",
    "ROU assets obtained for lease liabilities",
    2800,
    "USD",
    "millions",
    "FY2022",
    S,
    P,
)

# ROU and lease liabilities
lease_assets = [
    (
        "us-gaap:OperatingLeaseRightOfUseAsset",
        "Operating lease ROU assets",
        10234,
        10661,
    ),
    ("custom:FinanceLeaseROUAssets", "Finance lease ROU assets (in PPE)", 1069, 1015),
    ("custom:TotalROUAssets", "Total ROU assets", 11303, 11676),
    (
        "us-gaap:OperatingLeaseLiabilityCurrent",
        "Operating lease liability - current (in OCL)",
        1488,
        1410,
    ),
    (
        "us-gaap:OperatingLeaseLiabilityNoncurrent",
        "Operating lease liability - non-current",
        10046,
        10408,
    ),
    (
        "us-gaap:FinanceLeaseLiabilityCurrent",
        "Finance lease liability - current",
        144,
        165,
    ),
    (
        "us-gaap:FinanceLeaseLiabilityNoncurrent",
        "Finance lease liability - non-current",
        752,
        859,
    ),
    ("custom:TotalLeaseLiabilities", "Total lease liabilities", 12430, 12842),
]
for c, lbl, v24, v23 in lease_assets:
    add(c, lbl, v24, "USD", "millions", "instant_2024-09-28", S, P)
    add(c, lbl, v23, "USD", "millions", "instant_2023-09-30", S, P)

# Lease liability maturities (operating, finance, total)
maturities = [
    (2025, 1820, 171, 1991),
    (2026, 1914, 131, 2045),
    (2027, 1674, 59, 1733),
    (2028, 1360, 38, 1398),
    (2029, 1187, 36, 1223),
    ("Thereafter", 5563, 837, 6400),
]
for yr, op, fi, tot in maturities:
    suffix = str(yr)
    add(
        f"custom:OperatingLeaseMaturity_{suffix}",
        f"Operating lease maturity {suffix}",
        op,
        "USD",
        "millions",
        "instant_2024-09-28",
        S,
        P,
    )
    add(
        f"custom:FinanceLeaseMaturity_{suffix}",
        f"Finance lease maturity {suffix}",
        fi,
        "USD",
        "millions",
        "instant_2024-09-28",
        S,
        P,
    )
    add(
        f"custom:TotalLeaseMaturity_{suffix}",
        f"Total lease maturity {suffix}",
        tot,
        "USD",
        "millions",
        "instant_2024-09-28",
        S,
        P,
    )
add(
    "us-gaap:LesseeOperatingLeaseLiabilityPaymentsDue",
    "Total undiscounted operating lease liabilities",
    13518,
    "USD",
    "millions",
    "instant_2024-09-28",
    S,
    P,
)
add(
    "us-gaap:FinanceLeaseLiabilityPaymentsDue",
    "Total undiscounted finance lease liabilities",
    1272,
    "USD",
    "millions",
    "instant_2024-09-28",
    S,
    P,
)
add(
    "custom:TotalUndiscountedLeaseLiabilities",
    "Total undiscounted lease liabilities",
    14790,
    "USD",
    "millions",
    "instant_2024-09-28",
    S,
    P,
)
add(
    "us-gaap:LesseeOperatingLeaseLiabilityUndiscountedExcessAmount",
    "Operating lease imputed interest",
    -1984,
    "USD",
    "millions",
    "instant_2024-09-28",
    S,
    P,
)
add(
    "us-gaap:FinanceLeaseLiabilityUndiscountedExcessAmount",
    "Finance lease imputed interest",
    -376,
    "USD",
    "millions",
    "instant_2024-09-28",
    S,
    P,
)
add(
    "us-gaap:OperatingLeaseLiability",
    "Total operating lease liabilities",
    11534,
    "USD",
    "millions",
    "instant_2024-09-28",
    S,
    P,
)
add(
    "us-gaap:FinanceLeaseLiability",
    "Total finance lease liabilities",
    896,
    "USD",
    "millions",
    "instant_2024-09-28",
    S,
    P,
)
add(
    "us-gaap:OperatingLeaseWeightedAverageRemainingLeaseTerm1",
    "Weighted-avg remaining lease term",
    10.3,
    "years",
    "actual",
    "instant_2024-09-28",
    S,
    P,
)
add(
    "us-gaap:OperatingLeaseWeightedAverageRemainingLeaseTerm1",
    "Weighted-avg remaining lease term",
    10.6,
    "years",
    "actual",
    "instant_2023-09-30",
    S,
    P,
)
add(
    "us-gaap:OperatingLeaseWeightedAverageDiscountRatePercent",
    "Weighted-avg discount rate",
    0.031,
    "pure",
    "actual",
    "instant_2024-09-28",
    S,
    P,
)
add(
    "us-gaap:OperatingLeaseWeightedAverageDiscountRatePercent",
    "Weighted-avg discount rate",
    0.030,
    "pure",
    "actual",
    "instant_2023-09-30",
    S,
    P,
)
add(
    "custom:LeasesNotYetCommencedFixedPayments",
    "Fixed payment obligations under leases not yet commenced",
    849,
    "USD",
    "millions",
    "instant_2024-09-28",
    S,
    P,
)


# =====================================================================
# NOTE 9 — DEBT (pages 43-44)
# =====================================================================
S = "Note9_Debt"
P = 43
add(
    "us-gaap:CommercialPaper",
    "Commercial paper outstanding",
    10000,
    "USD",
    "millions",
    "instant_2024-09-28",
    S,
    P,
)
add(
    "us-gaap:CommercialPaper",
    "Commercial paper outstanding",
    6000,
    "USD",
    "millions",
    "instant_2023-09-30",
    S,
    P,
)
add(
    "custom:CommercialPaperWeightedAverageRate",
    "Commercial paper weighted-avg interest rate",
    0.0500,
    "pure",
    "actual",
    "instant_2024-09-28",
    S,
    P,
)
add(
    "custom:CommercialPaperWeightedAverageRate",
    "Commercial paper weighted-avg interest rate",
    0.0528,
    "pure",
    "actual",
    "instant_2023-09-30",
    S,
    P,
)

# Commercial paper cash flows
cp_cf = [
    (
        "custom:CPProceedsRepaymentsLE90Days",
        "CP proceeds/(repayments), maturities ≤90 days",
        3960,
        -1333,
        5264,
    ),
    ("custom:CPProceedsGT90Days", "CP proceeds, maturities >90 days", 0, 0, 5948),
    (
        "custom:CPRepaymentsGT90Days",
        "CP repayments, maturities >90 days",
        0,
        -2645,
        -7257,
    ),
    ("custom:CPNetGT90Days", "CP net, maturities >90 days", 0, -2645, -1309),
    ("custom:CPTotalNet", "Total CP net cash flow", 3960, -3978, 3955),
]
for c, lbl, v24, v23, v22 in cp_cf:
    add(c, lbl, v24, "USD", "millions", "FY2024", S, P)
    add(c, lbl, v23, "USD", "millions", "FY2023", S, P)
    add(c, lbl, v22, "USD", "millions", "FY2022", S, P)

# Term debt
add(
    "us-gaap:LongTermDebtPrincipal",
    "Term debt principal (fixed-rate 0.000%-4.850% notes)",
    97341,
    "USD",
    "millions",
    "instant_2024-09-28",
    S,
    P,
)
add(
    "us-gaap:LongTermDebtPrincipal",
    "Term debt principal (fixed-rate 0.000%-4.850% notes)",
    106572,
    "USD",
    "millions",
    "instant_2023-09-30",
    S,
    P,
)
add(
    "custom:UnamortizedPremiumDiscountIssuanceCosts",
    "Unamortized premium/(discount) and issuance costs, net",
    -321,
    "USD",
    "millions",
    "instant_2024-09-28",
    S,
    P,
)
add(
    "custom:UnamortizedPremiumDiscountIssuanceCosts",
    "Unamortized premium/(discount) and issuance costs, net",
    -356,
    "USD",
    "millions",
    "instant_2023-09-30",
    S,
    P,
)
add(
    "custom:HedgeAccountingFairValueAdjustments",
    "Hedge accounting fair value adjustments",
    -358,
    "USD",
    "millions",
    "instant_2024-09-28",
    S,
    P,
)
add(
    "custom:HedgeAccountingFairValueAdjustments",
    "Hedge accounting fair value adjustments",
    -1113,
    "USD",
    "millions",
    "instant_2023-09-30",
    S,
    P,
)
add(
    "us-gaap:LongTermDebt",
    "Total term debt",
    96662,
    "USD",
    "millions",
    "instant_2024-09-28",
    S,
    P,
)
add(
    "us-gaap:LongTermDebt",
    "Total term debt",
    105103,
    "USD",
    "millions",
    "instant_2023-09-30",
    S,
    P,
)
add(
    "us-gaap:LongTermDebtCurrent",
    "Term debt - current portion",
    10912,
    "USD",
    "millions",
    "instant_2024-09-28",
    S,
    P,
)
add(
    "us-gaap:LongTermDebtCurrent",
    "Term debt - current portion",
    9822,
    "USD",
    "millions",
    "instant_2023-09-30",
    S,
    P,
)
add(
    "us-gaap:LongTermDebtNoncurrent",
    "Term debt - non-current portion",
    85750,
    "USD",
    "millions",
    "instant_2024-09-28",
    S,
    P,
)
add(
    "us-gaap:LongTermDebtNoncurrent",
    "Term debt - non-current portion",
    95281,
    "USD",
    "millions",
    "instant_2023-09-30",
    S,
    P,
)

# Term debt maturity schedule
debt_mat = [
    ("2025", 10930),
    ("2026", 12342),
    ("2027", 9936),
    ("2028", 7800),
    ("2029", 5153),
    ("Thereafter", 51180),
]
for yr, v in debt_mat:
    add(
        f"custom:LongTermDebtPrincipalMaturity_{yr}",
        f"Term debt principal maturity {yr}",
        v,
        "USD",
        "millions",
        "instant_2024-09-28",
        S,
        P,
    )
add(
    "us-gaap:LongTermDebtFairValue",
    "Term debt fair value (Level 2)",
    88400,
    "USD",
    "millions",
    "instant_2024-09-28",
    S,
    44,
)
add(
    "us-gaap:LongTermDebtFairValue",
    "Term debt fair value (Level 2)",
    90800,
    "USD",
    "millions",
    "instant_2023-09-30",
    S,
    44,
)


# =====================================================================
# NOTE 10 — SHAREHOLDERS' EQUITY (page 44)
# =====================================================================
S = "Note10_Equity"
P = 44
add(
    "us-gaap:StockRepurchasedAndRetiredDuringPeriodShares",
    "Common stock repurchased (FY24)",
    499,
    "shares",
    "millions",
    "FY2024",
    S,
    P,
)
add(
    "us-gaap:StockRepurchasedAndRetiredDuringPeriodValue",
    "Common stock repurchased value (FY24)",
    95.0,
    "USD",
    "billions",
    "FY2024",
    S,
    P,
)

# Shares of common stock rollforward
shares_roll = [
    (
        "us-gaap:CommonStockSharesOutstanding",
        "Common stock outstanding, beginning",
        15550061,
        15943425,
        16426786,
    ),
    (
        "us-gaap:StockRepurchasedAndRetiredDuringPeriodShares",
        "Common stock repurchased (rollforward)",
        -499372,
        -471419,
        -568589,
    ),
    (
        "us-gaap:StockIssuedDuringPeriodSharesNewIssues",
        "Common stock issued, net of withheld",
        66097,
        78055,
        85228,
    ),
    (
        "us-gaap:CommonStockSharesOutstanding",
        "Common stock outstanding, ending",
        15116786,
        15550061,
        15943425,
    ),
]
for c, lbl, v24, v23, v22 in shares_roll:
    add(c, lbl, v24, "shares", "thousands", "FY2024", S, P)
    add(c, lbl, v23, "shares", "thousands", "FY2023", S, P)
    add(c, lbl, v22, "shares", "thousands", "FY2022", S, P)


# =====================================================================
# NOTE 11 — SHARE-BASED COMPENSATION (page 44-45)
# =====================================================================
S = "Note11_SBC"
P = 45
add(
    "custom:SharesAuthorized2022Plan",
    "Shares authorized under 2022 Employee Stock Plan",
    1.3,
    "shares",
    "billions",
    "instant_2022-09-24",
    S,
    44,
)

# RSU rollforward
rsu = [
    # (label, period_end, num_thousands, wavg_grant_date_fair_value)
    ("Balance as of September 25, 2021", "instant_2021-09-25", 240427, 75.16),
    ("RSUs granted FY22", "FY2022", 91674, 150.70),
    ("RSUs vested FY22", "FY2022", -115861, 72.12),
    ("RSUs canceled FY22", "FY2022", -14739, 99.77),
    ("Balance as of September 24, 2022", "instant_2022-09-24", 201501, 109.48),
    ("RSUs granted FY23", "FY2023", 88768, 150.87),
    ("RSUs vested FY23", "FY2023", -101878, 97.31),
    ("RSUs canceled FY23", "FY2023", -8144, 127.98),
    ("Balance as of September 30, 2023", "instant_2023-09-30", 180247, 135.91),
    ("RSUs granted FY24", "FY2024", 80456, 173.78),
    ("RSUs vested FY24", "FY2024", -87633, 127.59),
    ("RSUs canceled FY24", "FY2024", -9744, 140.80),
    ("Balance as of September 28, 2024", "instant_2024-09-28", 163326, 158.73),
]
for label, period, num, wavg in rsu:
    add(
        "custom:RSUNumberOfShares",
        label + " - number of RSUs",
        num,
        "shares",
        "thousands",
        period,
        S,
        P,
    )
    add(
        "custom:RSUWeightedAverageGrantDateFairValue",
        label + " - WAGD fair value",
        wavg,
        "USD/share",
        "actual",
        period,
        S,
        P,
    )
add(
    "custom:RSUAggregateFairValue",
    "Aggregate fair value of outstanding RSUs",
    37204,
    "USD",
    "millions",
    "instant_2024-09-28",
    S,
    P,
)
add(
    "custom:RSUVestedFairValue",
    "Fair value of RSUs that vested",
    15800,
    "USD",
    "millions",
    "FY2024",
    S,
    P,
)
add(
    "custom:RSUVestedFairValue",
    "Fair value of RSUs that vested",
    15900,
    "USD",
    "millions",
    "FY2023",
    S,
    P,
)
add(
    "custom:RSUVestedFairValue",
    "Fair value of RSUs that vested",
    18200,
    "USD",
    "millions",
    "FY2022",
    S,
    P,
)
add(
    "custom:RSUSharesWithheldForTaxes",
    "Shares withheld (millions)",
    31,
    "shares",
    "millions",
    "FY2024",
    S,
    P,
)
add(
    "custom:RSUSharesWithheldForTaxes",
    "Shares withheld (millions)",
    37,
    "shares",
    "millions",
    "FY2023",
    S,
    P,
)
add(
    "custom:RSUSharesWithheldForTaxes",
    "Shares withheld (millions)",
    41,
    "shares",
    "millions",
    "FY2022",
    S,
    P,
)
add(
    "custom:PaymentsToTaxAuthoritiesForEmployeeTaxes",
    "Payments to taxing authorities for employee taxes",
    5600,
    "USD",
    "millions",
    "FY2024",
    S,
    P,
)
add(
    "custom:PaymentsToTaxAuthoritiesForEmployeeTaxes",
    "Payments to taxing authorities for employee taxes",
    5600,
    "USD",
    "millions",
    "FY2023",
    S,
    P,
)
add(
    "custom:PaymentsToTaxAuthoritiesForEmployeeTaxes",
    "Payments to taxing authorities for employee taxes",
    6400,
    "USD",
    "millions",
    "FY2022",
    S,
    P,
)
# SBC expense and tax benefit
add(
    "us-gaap:ShareBasedCompensation",
    "Share-based compensation expense",
    11688,
    "USD",
    "millions",
    "FY2024",
    S,
    P,
)
add(
    "us-gaap:ShareBasedCompensation",
    "Share-based compensation expense",
    10833,
    "USD",
    "millions",
    "FY2023",
    S,
    P,
)
add(
    "us-gaap:ShareBasedCompensation",
    "Share-based compensation expense",
    9038,
    "USD",
    "millions",
    "FY2022",
    S,
    P,
)
add(
    "us-gaap:EmployeeBenefitsAndShareBasedCompensationIncomeTaxBenefit",
    "Income tax benefit related to SBC",
    -3350,
    "USD",
    "millions",
    "FY2024",
    S,
    P,
)
add(
    "us-gaap:EmployeeBenefitsAndShareBasedCompensationIncomeTaxBenefit",
    "Income tax benefit related to SBC",
    -3421,
    "USD",
    "millions",
    "FY2023",
    S,
    P,
)
add(
    "us-gaap:EmployeeBenefitsAndShareBasedCompensationIncomeTaxBenefit",
    "Income tax benefit related to SBC",
    -4002,
    "USD",
    "millions",
    "FY2022",
    S,
    P,
)
add(
    "us-gaap:EmployeeServiceShareBasedCompensationNonvestedAwardsTotalCompensationCostNotYetRecognized",
    "Unrecognized compensation cost - RSUs",
    19400,
    "USD",
    "millions",
    "instant_2024-09-28",
    S,
    P,
)
add(
    "us-gaap:EmployeeServiceShareBasedCompensationNonvestedAwardsTotalCompensationCostNotYetRecognizedPeriodForRecognition1",
    "Weighted-avg recognition period for RSUs",
    2.4,
    "years",
    "actual",
    "instant_2024-09-28",
    S,
    P,
)


# =====================================================================
# NOTE 12 — COMMITMENTS, CONTINGENCIES, SUPPLY (page 45)
# =====================================================================
S = "Note12_Commitments"
P = 45
upo = [
    ("2025", 3206),
    ("2026", 2440),
    ("2027", 1156),
    ("2028", 3121),
    ("2029", 633),
    ("Thereafter", 670),
]
for yr, v in upo:
    add(
        f"custom:UnconditionalPurchaseObligation_{yr}",
        f"Unconditional purchase obligations - {yr}",
        v,
        "USD",
        "millions",
        "instant_2024-09-28",
        S,
        P,
    )
add(
    "us-gaap:UnconditionalPurchaseObligation",
    "Total unconditional purchase obligations",
    11226,
    "USD",
    "millions",
    "instant_2024-09-28",
    S,
    P,
)


# =====================================================================
# NOTE 13 — SEGMENT INFORMATION (pages 46-47)
# =====================================================================
S = "Note13_Segments"
P = 47
segments = [
    ("Americas", 167045, 162560, 169658, 67656, 60508, 62683),
    ("Europe", 101328, 94294, 95118, 41790, 36098, 35233),
    ("Greater China", 66952, 72559, 74200, 27082, 30328, 31153),
    ("Japan", 25052, 24257, 25977, 12454, 11888, 12257),
    ("Rest of Asia Pacific", 30658, 29615, 29375, 13062, 12066, 11569),
]
for seg, ns24, ns23, ns22, oi24, oi23, oi22 in segments:
    dim = {"StatementBusinessSegmentsAxis": seg}
    add(
        "custom:SegmentNetSales",
        f"Net sales - {seg}",
        ns24,
        "USD",
        "millions",
        "FY2024",
        S,
        P,
        dim,
    )
    add(
        "custom:SegmentNetSales",
        f"Net sales - {seg}",
        ns23,
        "USD",
        "millions",
        "FY2023",
        S,
        P,
        dim,
    )
    add(
        "custom:SegmentNetSales",
        f"Net sales - {seg}",
        ns22,
        "USD",
        "millions",
        "FY2022",
        S,
        P,
        dim,
    )
    add(
        "custom:SegmentOperatingIncome",
        f"Operating income - {seg}",
        oi24,
        "USD",
        "millions",
        "FY2024",
        S,
        P,
        dim,
    )
    add(
        "custom:SegmentOperatingIncome",
        f"Operating income - {seg}",
        oi23,
        "USD",
        "millions",
        "FY2023",
        S,
        P,
        dim,
    )
    add(
        "custom:SegmentOperatingIncome",
        f"Operating income - {seg}",
        oi22,
        "USD",
        "millions",
        "FY2022",
        S,
        P,
        dim,
    )

# Segment reconciliation
recon_seg = [
    (
        "custom:SegmentOperatingIncomeTotal",
        "Total segment operating income",
        162044,
        150888,
        152895,
    ),
    (
        "us-gaap:ResearchAndDevelopmentExpense",
        "R&D expense (segment recon)",
        -31370,
        -29915,
        -26251,
    ),
    (
        "custom:OtherCorporateExpensesNet",
        "Other corporate expenses, net",
        -7458,
        -6672,
        -7207,
    ),
    (
        "us-gaap:OperatingIncomeLoss",
        "Total operating income (segment recon)",
        123216,
        114301,
        119437,
    ),
]
for c, lbl, v24, v23, v22 in recon_seg:
    add(c, lbl, v24, "USD", "millions", "FY2024", S, P)
    add(c, lbl, v23, "USD", "millions", "FY2023", S, P)
    add(c, lbl, v22, "USD", "millions", "FY2022", S, P)

# Geographic net sales
geo = [
    ("U.S.", 142196, 138573, 147859),
    ("China (incl. HK & Taiwan)", 66952, 72559, 74200),
    ("Other countries", 181887, 172153, 172269),
    ("Total", 391035, 383285, 394328),
]
for country, v24, v23, v22 in geo:
    dim = {"StatementGeographicalAxis": country}
    add(
        "custom:GeographicNetSales",
        f"Net sales - {country}",
        v24,
        "USD",
        "millions",
        "FY2024",
        S,
        P,
        dim,
    )
    add(
        "custom:GeographicNetSales",
        f"Net sales - {country}",
        v23,
        "USD",
        "millions",
        "FY2023",
        S,
        P,
        dim,
    )
    add(
        "custom:GeographicNetSales",
        f"Net sales - {country}",
        v22,
        "USD",
        "millions",
        "FY2022",
        S,
        P,
        dim,
    )

# Long-lived assets by geography
lla = [
    ("U.S.", 35664, 33276),
    ("China (incl. HK & Taiwan)", 4797, 5778),
    ("Other countries", 5219, 4661),
    ("Total", 45680, 43715),
]
for country, v24, v23 in lla:
    dim = {"StatementGeographicalAxis": country}
    add(
        "custom:GeographicLongLivedAssets",
        f"Long-lived assets - {country}",
        v24,
        "USD",
        "millions",
        "instant_2024-09-28",
        S,
        P,
        dim,
    )
    add(
        "custom:GeographicLongLivedAssets",
        f"Long-lived assets - {country}",
        v23,
        "USD",
        "millions",
        "instant_2023-09-30",
        S,
        P,
        dim,
    )


# =====================================================================
# ITEM 5 — Issuer Purchases (page 19)
# =====================================================================
S = "Item5_IssuerPurchases"
P = 19
buyback_q4 = [
    ("June 30, 2024 to August 3, 2024", 35697, 224.11),
    ("August 4, 2024 to August 31, 2024", 42910, 221.39),
    ("September 1, 2024 to September 28, 2024", 33653, 222.86),
]
for period_name, shares, price in buyback_q4:
    dim = {"BuybackPeriod": period_name}
    add(
        "us-gaap:StockRepurchasedDuringPeriodShares",
        f"Buyback shares - {period_name}",
        shares,
        "shares",
        "thousands",
        "Q4_2024",
        S,
        P,
        dim,
    )
    add(
        "us-gaap:TreasuryStockAcquiredAverageCostPerShare",
        f"Buyback avg price - {period_name}",
        price,
        "USD/share",
        "actual",
        "Q4_2024",
        S,
        P,
        dim,
    )
add(
    "us-gaap:StockRepurchasedDuringPeriodShares",
    "Total Q4 2024 buyback shares",
    112260,
    "shares",
    "thousands",
    "Q4_2024",
    S,
    P,
)
add(
    "custom:RepurchaseAuthorizationRemaining",
    "Repurchase authorization remaining (May 2024 program $110B less utilized)",
    89074,
    "USD",
    "millions",
    "instant_2024-09-28",
    S,
    P,
)
add(
    "custom:RepurchaseAuthorizationMay2024",
    "Repurchase program authorized May 2024",
    110000,
    "USD",
    "millions",
    "instant_2024-09-28",
    S,
    P,
)
add(
    "custom:RepurchaseAuthorizationMay2024Used",
    "Utilized under May 2024 repurchase program",
    20900,
    "USD",
    "millions",
    "instant_2024-09-28",
    S,
    P,
)


# =====================================================================
# Stock performance graph (page 20) - $100 invested 9/27/2019
# =====================================================================
S = "StockPerformanceGraph"
P = 20
perf = [
    ("AAPL", 100, 207, 273, 281, 322, 430),
    ("S&P 500 Index", 100, 113, 156, 131, 155, 210),
    ("Dow Jones U.S. Technology Supersector Index", 100, 146, 216, 156, 215, 322),
]
periods = [
    "instant_2019-09",
    "instant_2020-09",
    "instant_2021-09",
    "instant_2022-09",
    "instant_2023-09",
    "instant_2024-09",
]
for index_name, *vals in perf:
    for period, v in zip(periods, vals, strict=True):
        add(
            "custom:CumulativeTotalReturnIndexed100",
            f"5-yr cumulative total return - {index_name}",
            v,
            "USD",
            "actual",
            period,
            S,
            P,
            {"Index": index_name},
        )


# =====================================================================
# ITEM 7 — MD&A: Gross Margin & Operating Expenses split (pages 22-25)
# =====================================================================
S = "Item7_MDA"
# Products vs Services gross margin
P = 24
gm = [
    (
        "custom:ProductsGrossMargin",
        "Products gross margin",
        109633,
        108803,
        114728,
        "USD",
        "millions",
    ),
    (
        "custom:ServicesGrossMargin",
        "Services gross margin",
        71050,
        60345,
        56054,
        "USD",
        "millions",
    ),
    (
        "custom:TotalGrossMargin",
        "Total gross margin",
        180683,
        169148,
        170782,
        "USD",
        "millions",
    ),
    (
        "custom:ProductsGrossMarginPercent",
        "Products gross margin %",
        0.372,
        0.365,
        0.363,
        "pure",
        "actual",
    ),
    (
        "custom:ServicesGrossMarginPercent",
        "Services gross margin %",
        0.739,
        0.708,
        0.717,
        "pure",
        "actual",
    ),
    (
        "custom:TotalGrossMarginPercent",
        "Total gross margin %",
        0.462,
        0.441,
        0.433,
        "pure",
        "actual",
    ),
]
for c, lbl, v24, v23, v22, u, sc in gm:
    add(c, lbl, v24, u, sc, "FY2024", S, P)
    add(c, lbl, v23, u, sc, "FY2023", S, P)
    add(c, lbl, v22, u, sc, "FY2022", S, P)

# Item 7A market risk
P = 27
add(
    "custom:VAR95Pct1Day",
    "VAR (95% confidence, 1-day) on FX derivatives",
    538,
    "USD",
    "millions",
    "instant_2024-09-28",
    "Item7A_MarketRisk",
    P,
)
add(
    "custom:VAR95Pct1Day",
    "VAR (95% confidence, 1-day) on FX derivatives",
    669,
    "USD",
    "millions",
    "instant_2023-09-30",
    "Item7A_MarketRisk",
    P,
)
add(
    "custom:InvestmentPortfolio100bpDecline",
    "Investment portfolio decline if rates +100bp",
    2755,
    "USD",
    "millions",
    "instant_2024-09-28",
    "Item7A_MarketRisk",
    P,
)
add(
    "custom:InvestmentPortfolio100bpDecline",
    "Investment portfolio decline if rates +100bp",
    3089,
    "USD",
    "millions",
    "instant_2023-09-30",
    "Item7A_MarketRisk",
    P,
)
add(
    "custom:TermDebt100bpInterestExpense",
    "Annual interest expense increase on term debt if rates +100bp",
    139,
    "USD",
    "millions",
    "instant_2024-09-28",
    "Item7A_MarketRisk",
    P,
)
add(
    "custom:TermDebt100bpInterestExpense",
    "Annual interest expense increase on term debt if rates +100bp",
    194,
    "USD",
    "millions",
    "instant_2023-09-30",
    "Item7A_MarketRisk",
    P,
)


# =====================================================================
# Final write
# =====================================================================
doc["summary"] = {
    "fact_count": len(facts),
    "concept_count": len({f["concept"] for f in facts}),
    "statements_covered": sorted({f["statement"] for f in facts}),
    "periods_covered": sorted({f["period"] for f in facts}),
}

OUT.write_text(json.dumps(doc, indent=2, default=str))
print(f"Wrote {OUT} -- {len(facts)} facts across {doc['summary']['concept_count']} concepts")
print("Statements:", doc["summary"]["statements_covered"])
print("Periods:", doc["summary"]["periods_covered"])
