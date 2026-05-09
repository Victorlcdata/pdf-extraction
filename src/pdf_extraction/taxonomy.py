"""
Canonical taxonomy used to give every fact the same name across companies.

This is the master list. Each fact extracted from a PDF gets a `canonical` field
chosen from these names (or null if nothing fits). The original line-item label
and the native taxonomy tag (us-gaap:*, ifrs:*) are kept on every fact, so you
can always trace back to how the company actually labeled it.

To extend: add an entry to TAXONOMY. The key is the canonical name (CamelCase,
no spaces). The value is a short human description that helps the LLM decide
whether a given line item maps to this concept.
"""

TAXONOMY: dict[str, str] = {
    # ===== INCOME STATEMENT =====
    "Revenue":                          "Total revenue / net sales / turnover (top line)",
    "RevenueProducts":                  "Revenue from product sales (if disclosed separately)",
    "RevenueServices":                  "Revenue from services (if disclosed separately)",
    "CostOfRevenue":                    "Total cost of goods/services sold",
    "CostOfRevenueProducts":            "Cost of products sold (if disclosed separately)",
    "CostOfRevenueServices":            "Cost of services sold (if disclosed separately)",
    "GrossProfit":                      "Revenue minus cost of revenue",
    "ResearchAndDevelopmentExpense":    "R&D expense",
    "SellingGeneralAndAdministrative":  "SG&A or operating expenses excluding R&D and COGS",
    "MarketingExpense":                 "Marketing or advertising expense (if separated from SG&A)",
    "DepreciationAndAmortizationOpex":  "D&A reported as an operating expense line",
    "OtherOperatingExpense":            "Other operating expenses, restructuring, impairments",
    "OperatingExpensesTotal":           "Sum of all operating expenses (excluding COGS)",
    "OperatingIncome":                  "Operating income / profit / EBIT",
    "InterestIncome":                   "Interest income",
    "InterestExpense":                  "Interest expense",
    "OtherNonOperatingIncome":          "Other non-operating income/(expense), FX, gains/losses",
    "IncomeBeforeTax":                  "Pretax income / profit before tax",
    "IncomeTaxExpense":                 "Provision for income taxes",
    "NetIncome":                        "Net income / net profit / earnings (bottom line)",
    "NetIncomeAttributableToParent":    "Net income attributable to parent / common shareholders",
    "NetIncomeAttributableToMinority":  "Net income attributable to non-controlling/minority interests",
    "EarningsPerShareBasic":            "Basic EPS",
    "EarningsPerShareDiluted":          "Diluted EPS",
    "WeightedAverageSharesBasic":       "Weighted-average shares used in basic EPS",
    "WeightedAverageSharesDiluted":     "Weighted-average shares used in diluted EPS",
    "DividendsPerShareDeclared":        "Dividends declared per common share",

    # ===== COMPREHENSIVE INCOME =====
    "OtherComprehensiveIncome":         "Total other comprehensive income/(loss), net of tax",
    "ForeignCurrencyTranslation":       "OCI: foreign currency translation, net of tax",
    "UnrealizedGainsLossesDerivatives": "OCI: unrealized gains/losses on derivatives",
    "UnrealizedGainsLossesSecurities":  "OCI: unrealized gains/losses on debt/equity securities",
    "ComprehensiveIncomeTotal":         "Net income + total OCI",

    # ===== BALANCE SHEET — CURRENT ASSETS =====
    "CashAndEquivalents":               "Cash and cash equivalents",
    "ShortTermInvestments":             "Short-term / current marketable securities",
    "AccountsReceivableNet":            "Accounts receivable / trade receivables, net",
    "OtherReceivables":                 "Vendor non-trade receivables, other receivables",
    "Inventory":                        "Inventory / inventories",
    "OtherCurrentAssets":               "Other current assets / prepaid expenses",
    "TotalCurrentAssets":               "Total current assets",

    # ===== BALANCE SHEET — NON-CURRENT ASSETS =====
    "LongTermInvestments":              "Non-current / long-term marketable securities",
    "PropertyPlantAndEquipmentNet":     "PP&E, net of accumulated depreciation",
    "PropertyPlantAndEquipmentGross":   "PP&E gross (before depreciation)",
    "AccumulatedDepreciation":          "Accumulated depreciation on PP&E",
    "Goodwill":                         "Goodwill",
    "IntangibleAssetsNet":              "Intangible assets, net",
    "OperatingLeaseRightOfUseAsset":    "Operating lease right-of-use assets",
    "DeferredTaxAssetsNonCurrent":      "Deferred tax assets, non-current",
    "OtherNonCurrentAssets":            "Other non-current assets",
    "TotalNonCurrentAssets":            "Total non-current assets",
    "TotalAssets":                      "Total assets",

    # ===== BALANCE SHEET — CURRENT LIABILITIES =====
    "AccountsPayable":                  "Accounts payable / trade payables",
    "AccruedExpenses":                  "Accrued expenses / accrued liabilities",
    "ShortTermDebt":                    "Short-term debt / current portion of long-term debt",
    "CommercialPaper":                  "Commercial paper outstanding",
    "DeferredRevenueCurrent":           "Deferred revenue / contract liabilities, current",
    "OperatingLeaseLiabilityCurrent":   "Operating lease liabilities, current",
    "IncomeTaxesPayableCurrent":        "Income taxes payable, current",
    "OtherCurrentLiabilities":          "Other current liabilities",
    "TotalCurrentLiabilities":          "Total current liabilities",

    # ===== BALANCE SHEET — NON-CURRENT LIABILITIES =====
    "LongTermDebt":                     "Long-term debt / non-current portion",
    "DeferredRevenueNonCurrent":        "Deferred revenue / contract liabilities, non-current",
    "OperatingLeaseLiabilityNonCurrent":"Operating lease liabilities, non-current",
    "DeferredTaxLiabilitiesNonCurrent": "Deferred tax liabilities, non-current",
    "PensionBenefitObligation":         "Pension/post-retirement benefit obligation",
    "OtherNonCurrentLiabilities":       "Other non-current liabilities",
    "TotalNonCurrentLiabilities":       "Total non-current liabilities",
    "TotalLiabilities":                 "Total liabilities",

    # ===== BALANCE SHEET — EQUITY =====
    "CommonStockAndAPIC":               "Common stock + additional paid-in capital (combined or separate)",
    "RetainedEarnings":                 "Retained earnings / accumulated deficit",
    "TreasuryStock":                    "Treasury stock",
    "AccumulatedOCI":                   "Accumulated other comprehensive income/(loss)",
    "MinorityInterest":                 "Non-controlling / minority interest",
    "TotalEquity":                      "Total shareholders' / stockholders' equity",
    "TotalLiabilitiesAndEquity":        "Total liabilities and shareholders' equity",
    "CommonSharesIssued":               "Common shares issued",
    "CommonSharesOutstanding":          "Common shares outstanding",
    "CommonSharesAuthorized":           "Common shares authorized",
    "CommonStockParValue":              "Common stock par or stated value per share",

    # ===== CASH FLOW =====
    "DepreciationAndAmortizationCF":    "D&A added back in operating cash flow",
    "ShareBasedCompensationCF":         "Share-based compensation added back in CF",
    "DeferredIncomeTaxesCF":            "Deferred income taxes adjustment in CF",
    "ChangeInAccountsReceivable":       "CF working capital: change in accounts receivable",
    "ChangeInInventory":                "CF working capital: change in inventory",
    "ChangeInAccountsPayable":          "CF working capital: change in accounts payable",
    "OtherWorkingCapitalChanges":       "CF working capital: other / catch-all",
    "CashFromOperations":               "Net cash from operating activities",
    "CapitalExpenditures":              "Payments for property, plant and equipment / capex",
    "AcquisitionsNetOfCash":            "Cash paid for acquisitions, net of cash acquired",
    "PurchasesOfInvestments":           "Purchases of marketable securities / investments",
    "ProceedsFromInvestments":          "Proceeds from sales/maturities of investments",
    "OtherInvestingActivities":         "Other investing activities",
    "CashFromInvesting":                "Net cash from investing activities",
    "DividendsPaidCF":                  "Dividends paid (cash flow)",
    "StockRepurchasesCF":               "Repurchases of common stock (cash flow)",
    "ProceedsFromDebtIssuance":         "Proceeds from issuance of debt",
    "RepaymentsOfDebt":                 "Repayments of debt",
    "OtherFinancingActivities":         "Other financing activities",
    "CashFromFinancing":                "Net cash from financing activities",
    "EffectOfFXOnCash":                 "Effect of exchange rate changes on cash",
    "NetChangeInCash":                  "Net increase/(decrease) in cash",
    "CashBeginningOfPeriod":            "Cash, beginning balance",
    "CashEndOfPeriod":                  "Cash, ending balance",
    "CashPaidForInterest":              "Cash paid for interest (supplemental)",
    "CashPaidForIncomeTaxes":           "Cash paid for income taxes (supplemental)",

    # ===== TAX NOTE =====
    "EffectiveTaxRate":                 "Effective income tax rate",
    "StatutoryTaxRate":                 "Statutory federal/national tax rate",
    "DeferredTaxAssetsGross":           "Total deferred tax assets, before valuation allowance",
    "ValuationAllowance":               "Deferred tax asset valuation allowance",
    "DeferredTaxLiabilitiesGross":      "Total deferred tax liabilities",
    "UnrecognizedTaxBenefits":          "Total gross unrecognized tax benefits",
    "ForeignPretaxEarnings":            "Foreign component of pretax earnings",

    # ===== DEBT NOTE =====
    "TermDebtPrincipal":                "Term/notes principal outstanding (face value)",
    "TermDebtCarryingValue":            "Term debt carrying amount (after premiums/discounts)",
    "TermDebtFairValue":                "Term debt fair value (Level 2)",

    # ===== EQUITY NOTE / SBC =====
    "SharesRepurchased":                "Common shares repurchased during period",
    "ValueOfSharesRepurchased":         "Value of common stock repurchased",
    "ShareRepurchaseAuthorization":     "Authorized repurchase program size",
    "ShareBasedCompensationExpense":    "Share-based compensation expense (income statement view)",
    "UnrecognizedSBCCost":              "Unrecognized share-based comp cost",
    "RSUsOutstanding":                  "RSUs outstanding (number)",
    "RSUsGranted":                      "RSUs granted during period",
    "RSUsVested":                       "RSUs vested during period",

    # ===== SEGMENTS =====
    "SegmentRevenue":                   "Net sales / revenue for a reportable segment (use dimensions to label segment)",
    "SegmentOperatingIncome":           "Operating income for a reportable segment (use dimensions)",
    "GeographicRevenue":                "Net sales by country/region (use dimensions to label country)",
    "GeographicLongLivedAssets":        "Long-lived assets by country/region (use dimensions)",
    "ProductLineRevenue":               "Net sales by product line (use dimensions: iPhone, Mac, etc.)",

    # ===== LEASES =====
    "OperatingLeaseCost":               "Operating lease expense (fixed, P&L)",
    "VariableLeaseCost":                "Variable lease cost",
    "TotalLeaseLiabilities":            "Total lease liabilities (operating + finance)",
    "WeightedAverageLeaseTerm":         "Weighted-average remaining lease term",
    "WeightedAverageLeaseDiscountRate": "Weighted-average discount rate on leases",

    # ===== EMPLOYEES / OPERATIONAL =====
    "NumberOfEmployees":                "Total full-time-equivalent employees",
    "NumberOfShareholdersOfRecord":     "Shareholders of record",
}


def taxonomy_for_prompt() -> str:
    """Render the taxonomy as a string suitable for inclusion in the LLM prompt."""
    return "\n".join(f"  {name}: {desc}" for name, desc in TAXONOMY.items())


def canonical_names() -> set[str]:
    """All valid canonical names — used for output validation."""
    return set(TAXONOMY.keys())
