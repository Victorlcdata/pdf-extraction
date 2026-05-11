# Taxonomy proposals (Phase-3 learning report)

Generated from `data/output/observations.jsonl` — 3,647 observations, min-frequency = 2.

> This file is *advisory*. Nothing here is applied automatically. Review each section, decide what to act on, and edit [`src/pdf_extraction/taxonomy.py`](../../src/pdf_extraction/taxonomy.py) or [`data/taxonomies/`](../taxonomies/) by hand.

## 1. Proposed canonicals

Concepts with `canonical: null` seen ≥ 2 times. Each block proposes a CamelCase name (derived from the concept's local part) and the evidence. Add the ones you accept to `TAXONOMY` in `taxonomy.py`.

### `CumulativeTotalReturn`  *(suggested)*

- **Source concept**: `custom:CumulativeTotalReturn`
- **Evidence**: 42 fact(s) across 2 filing(s)
- **Statements**: `Note_5_MarketForRegistrantsCommonEquity` (42)
- **Labels seen**:
    - 'Ribbon Communications Inc.' ×6
    - 'Nasdaq Composite' ×6
    - 'Russell 2000' ×6
    - 'Nasdaq Telecommunications' ×6
    - 'FormFactor, Inc.' ×6
    - 'S&P 500 Index' ×6
    - … and 1 more

```python
    "CumulativeTotalReturn": "TODO — describe this concept",
```

### `RevenueByMarket`  *(suggested)*

- **Source concept**: `custom:RevenueByMarket`
- **Evidence**: 32 fact(s) across 1 filing(s)
- **Statements**: `Note_17_SegmentsAndGeographicInformation` (32)
- **Labels seen**:
    - 'Foundry & Logic' ×8
    - 'DRAM' ×8
    - 'Flash' ×8
    - 'Systems' ×8

```python
    "RevenueByMarket": "TODO — describe this concept",
```

### `RevenueConcentrationPercentage`  *(suggested)*

- **Source concept**: `custom:RevenueConcentrationPercentage`
- **Evidence**: 26 fact(s) across 1 filing(s)
- **Statements**: `Note_NotApplicable_Customers` (23), `Note_NotApplicable_RiskFactors` (3)
- **Labels seen**:
    - 'SK hynix Inc.' ×8
    - 'Total of Customers with > 10% Revenue' ×8
    - 'Intel Corporation' ×5
    - 'One customer represented of total revenues' ×2
    - 'Taiwan Semiconductor Manufacturing Company Ltd.' ×1
    - 'Samsung Electronics Co., Ltd.' ×1
    - … and 1 more

```python
    "RevenueConcentrationPercentage": "TODO — describe this concept",
```

### `GrossMargin`  *(suggested)*

- **Source concept**: `us-gaap:GrossMargin`
- **Evidence**: 26 fact(s) across 3 filing(s)
- **Statements**: `Note_7_MDA` (9), `Note_NotApplicable_GrossMargins` (9), `Note_7_ResultsOfOperations` (8)
- **Labels seen**:
    - 'Gross margin' ×17
    - 'Products' ×3
    - 'Services' ×3
    - 'Total gross margin percentage' ×3

```python
    "GrossMargin": "TODO — describe this concept",
```

### `ContractualObligations`  *(suggested)*

- **Source concept**: `us-gaap:ContractualObligations`
- **Evidence**: 23 fact(s) across 1 filing(s)
- **Statements**: `Note_12_CommitmentsAndContingencies` (23)
- **Labels seen**:
    - 'Operating leases' ×6
    - 'Term loan - principal payments' ×6
    - 'Term loan - interest payments' ×6
    - 'Revolver - commitment fee' ×5

```python
    "ContractualObligations": "TODO — describe this concept",
```

### `PerformanceGraphValue`  *(suggested)*

- **Source concept**: `custom:PerformanceGraphValue`
- **Evidence**: 18 fact(s) across 1 filing(s)
- **Statements**: `Note_5_MarketForRegistrantsCommonEquityRelatedStockholderMattersAndIssuerPurchasesOfEquitySecurities` (18)
- **Labels seen**:
    - 'Valhi common stock' ×6
    - 'S&P 500 Index' ×6
    - 'S&P 500 Industrial Conglomerates' ×6

```python
    "PerformanceGraphValue": "TODO — describe this concept",
```

### `StockPerformance`  *(suggested)*

- **Source concept**: `custom:StockPerformance`
- **Evidence**: 18 fact(s) across 1 filing(s)
- **Statements**: `Note_5_MarketForRegistrantsCommonEquity` (18)
- **Labels seen**:
    - 'Apple Inc.' ×6
    - 'S&P 500 Index' ×6
    - 'Dow Jones U.S. Technology Supersector Index' ×6

```python
    "StockPerformance": "TODO — describe this concept",
```

### `PropertySquareFootage`  *(suggested)*

- **Source concept**: `custom:PropertySquareFootage`
- **Evidence**: 17 fact(s) across 1 filing(s)
- **Statements**: `Note_NotApplicable_Properties` (17)
- **Labels seen**:
    - 'Square Footage' ×17

```python
    "PropertySquareFootage": "TODO — describe this concept",
```

### `IncreaseDecreaseInCommonStock`  *(suggested)*

- **Source concept**: `us-gaap:IncreaseDecreaseInCommonStock`
- **Evidence**: 16 fact(s) across 2 filing(s)
- **Statements**: `ShareholdersEquity` (16)
- **Labels seen**:
    - 'Common stock issued' ×3
    - 'Exercise of stock options' ×3
    - 'Vesting of restricted stock awards and units' ×3
    - 'Vesting of performance-based stock units' ×3
    - 'Shares of restricted stock returned to the Company under net share settlements to satis…' ×3
    - 'Exercise of warrants' ×1

```python
    "IncreaseDecreaseInCommonStock": "TODO — describe this concept",
```

### `InterestIncomeExpenseNet`  *(suggested)*

- **Source concept**: `us-gaap:InterestIncomeExpenseNet`
- **Evidence**: 15 fact(s) across 3 filing(s)
- **Statements**: `IncomeStatement` (11), `Note_7_ResultsOfOperations` (2), `Note_7_ManagementsDiscussionAndAnalysisOfFinancialConditionAndResultsOfOperations` (2)
- **Labels seen**:
    - 'Interest income (expense), net' ×7
    - 'Interest expense, net' ×5
    - 'Interest income' ×3

```python
    "InterestIncomeExpenseNet": "TODO — describe this concept",
```

### `Liabilities`  *(suggested)*

- **Source concept**: `us-gaap:Liabilities`
- **Evidence**: 14 fact(s) across 7 filing(s)
- **Statements**: `BalanceSheet` (14)
- **Labels seen**:
    - 'Total liabilities' ×12
    - 'TOTAL LIABILITIES:' ×2

```python
    "Liabilities": "TODO — describe this concept",
```

### `MaintenanceAndSupportRevenue`  *(suggested)*

- **Source concept**: `us-gaap:MaintenanceAndSupportRevenue`
- **Evidence**: 14 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ResultsOfOperations` (14)
- **Labels seen**:
    - 'Service revenue (maintenance)' ×10
    - 'Maintenance' ×2
    - 'Total' ×2

```python
    "MaintenanceAndSupportRevenue": "TODO — describe this concept",
```

### `ProfessionalServicesRevenue`  *(suggested)*

- **Source concept**: `us-gaap:ProfessionalServicesRevenue`
- **Evidence**: 14 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ResultsOfOperations` (14)
- **Labels seen**:
    - 'Service revenue (professional services)' ×10
    - 'Professional services' ×2
    - 'Total' ×2

```python
    "ProfessionalServicesRevenue": "TODO — describe this concept",
```

### `CashCashEquivalentsAndRestrictedCash`  *(suggested)*

- **Source concept**: `us-gaap:CashCashEquivalentsAndRestrictedCash`
- **Evidence**: 9 fact(s) across 2 filing(s)
- **Statements**: `CashFlow` (6), `Note_18_SupplementalCashFlowInformation` (3)
- **Labels seen**:
    - 'Cash and cash equivalents and restricted cash - beginning of period' ×3
    - 'Cash and cash equivalents and restricted cash - end of period' ×3
    - 'Cash, cash equivalents and restricted cash shown in the statement of cash flows' ×3

```python
    "CashCashEquivalentsAndRestrictedCash": "TODO — describe this concept",
```

### `GrossProfitMargin`  *(suggested)*

- **Source concept**: `us-gaap:GrossProfitMargin`
- **Evidence**: 9 fact(s) across 2 filing(s)
- **Statements**: `Note_7_ManagementDiscussionAndAnalysis` (9)
- **Labels seen**:
    - 'Gross margin' ×6
    - 'Total gross margin percentage' ×3

```python
    "GrossProfitMargin": "TODO — describe this concept",
```

### `OtherNoncashIncomeExpense`  *(suggested)*

- **Source concept**: `us-gaap:OtherNoncashIncomeExpense`
- **Evidence**: 9 fact(s) across 2 filing(s)
- **Statements**: `CashFlow` (9)
- **Labels seen**:
    - 'Other' ×6
    - 'Other adjustments' ×3

```python
    "OtherNoncashIncomeExpense": "TODO — describe this concept",
```

### `EntityFilerCategory`  *(suggested)*

- **Source concept**: `dei:EntityFilerCategory`
- **Evidence**: 8 fact(s) across 3 filing(s)
- **Statements**: `Cover` (8)
- **Labels seen**:
    - 'Large accelerated filer' ×3
    - 'Non-accelerated filer' ×2
    - 'Accelerated filer' ×1
    - 'Smaller reporting company' ×1
    - 'Emerging growth company' ×1

```python
    "EntityFilerCategory": "TODO — describe this concept",
```

### `SecurityPriceHigh`  *(suggested)*

- **Source concept**: `dei:SecurityPriceHigh`
- **Evidence**: 8 fact(s) across 1 filing(s)
- **Statements**: `Note_5_MarketForRegistrantsCommonEquityRelatedStockholderMattersAndIssuerPurchasesOfEquitySecurities` (8)
- **Labels seen**:
    - 'High' ×8

```python
    "SecurityPriceHigh": "TODO — describe this concept",
```

### `SecurityPriceLow`  *(suggested)*

- **Source concept**: `dei:SecurityPriceLow`
- **Evidence**: 8 fact(s) across 1 filing(s)
- **Statements**: `Note_5_MarketForRegistrantsCommonEquityRelatedStockholderMattersAndIssuerPurchasesOfEquitySecurities` (8)
- **Labels seen**:
    - 'Low' ×8

```python
    "SecurityPriceLow": "TODO — describe this concept",
```

### `LaborAndRelatedExpense`  *(suggested)*

- **Source concept**: `us-gaap:LaborAndRelatedExpense`
- **Evidence**: 8 fact(s) across 3 filing(s)
- **Statements**: `IncomeStatement` (6), `Note_7_ManagementDiscussionAndAnalysis` (2)
- **Labels seen**:
    - 'Payroll' ×3
    - 'Salaries and benefits' ×3
    - 'Employee compensation and benefits' ×2

```python
    "LaborAndRelatedExpense": "TODO — describe this concept",
```

### `StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest`  *(suggested)*

- **Source concept**: `us-gaap:StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest`
- **Evidence**: 8 fact(s) across 2 filing(s)
- **Statements**: `BalanceSheet` (4), `ShareholdersEquity` (4)
- **Labels seen**:
    - 'Total equity' ×8

```python
    "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest": "TODO — describe this concept",
```

### `ChangeInSellingGeneralAndAdministrativeExpense`  *(suggested)*

- **Source concept**: `custom:ChangeInSellingGeneralAndAdministrativeExpense`
- **Evidence**: 7 fact(s) across 1 filing(s)
- **Statements**: `Note_NotApplicable_SellingGeneralAndAdministrative` (7)
- **Labels seen**:
    - 'General operating expenses' ×1
    - 'Employee compensation costs' ×1
    - 'Restructuring charges' ×1
    - 'Consulting fees' ×1
    - 'Stock-based compensation expense' ×1
    - 'Commission expenses' ×1
    - … and 1 more

```python
    "ChangeInSellingGeneralAndAdministrativeExpense": "TODO — describe this concept",
```

### `IncreaseDecreaseInAdditionalPaidInCapital`  *(suggested)*

- **Source concept**: `us-gaap:IncreaseDecreaseInAdditionalPaidInCapital`
- **Evidence**: 7 fact(s) across 1 filing(s)
- **Statements**: `ShareholdersEquity` (7)
- **Labels seen**:
    - 'Exercise of stock options' ×3
    - 'Shares of restricted stock returned to the Company under net share settlements to satis…' ×3
    - 'Exercise of warrants' ×1

```python
    "IncreaseDecreaseInAdditionalPaidInCapital": "TODO — describe this concept",
```

### `ProceedsFromSaleOfBusiness`  *(suggested)*

- **Source concept**: `us-gaap:ProceedsFromSaleOfBusiness`
- **Evidence**: 7 fact(s) across 3 filing(s)
- **Statements**: `CashFlow` (7)
- **Labels seen**:
    - 'Proceeds from sale of Sunseeker Resort' ×3
    - 'Sale of MyFitnessPal platform' ×3
    - 'Cash related to sale of business' ×1

```python
    "ProceedsFromSaleOfBusiness": "TODO — describe this concept",
```

### `UnconditionalPurchaseObligations`  *(suggested)*

- **Source concept**: `us-gaap:UnconditionalPurchaseObligations`
- **Evidence**: 7 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ManagementDiscussionAndAnalysis` (4), `Note_7_MDA` (2), `Note_12_Commitments` (1)
- **Labels seen**:
    - 'manufacturing purchase obligations' ×1
    - 'other purchase obligations' ×1
    - 'manufacturing purchase obligations of $53.0 billion' ×1
    - 'with $52.9 billion payable within 12 months' ×1
    - 'other purchase obligations of $12.0 billion' ×1
    - 'with $4.1 billion payable within 12 months' ×1
    - … and 1 more

```python
    "UnconditionalPurchaseObligations": "TODO — describe this concept",
```

### `AgeRangeInYears`  *(suggested)*

- **Source concept**: `custom:AgeRangeInYears`
- **Evidence**: 6 fact(s) across 1 filing(s)
- **Statements**: `Note_2_Properties` (6)
- **Labels seen**:
    - 'Age Range (years)' ×6

```python
    "AgeRangeInYears": "TODO — describe this concept",
```

### `CostOfSalesAsAPercentageOfNetSales`  *(suggested)*

- **Source concept**: `custom:CostOfSalesAsAPercentageOfNetSales`
- **Evidence**: 6 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ManagementDiscussionAndAnalysis` (6)
- **Labels seen**:
    - 'Cost of sales' ×6

```python
    "CostOfSalesAsAPercentageOfNetSales": "TODO — describe this concept",
```

### `GrossProfit`  *(suggested)*

- **Source concept**: `us-gaap:GrossProfit`
- **Evidence**: 6 fact(s) across 1 filing(s)
- **Statements**: `Note_7_MDA` (6)
- **Labels seen**:
    - 'Products' ×3
    - 'Services' ×3

```python
    "GrossProfit": "TODO — describe this concept",
```

### `OperatingMargin`  *(suggested)*

- **Source concept**: `us-gaap:OperatingMargin`
- **Evidence**: 6 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ManagementDiscussionAndAnalysis` (6)
- **Labels seen**:
    - 'Operating income (loss)' ×3
    - 'Operating income' ×3

```python
    "OperatingMargin": "TODO — describe this concept",
```

### `OtherComponentsOfNetPeriodicPensionAndPostretirementBenefitCost`  *(suggested)*

- **Source concept**: `us-gaap:OtherComponentsOfNetPeriodicPensionAndPostretirementBenefitCost`
- **Evidence**: 6 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ManagementDiscussionAndAnalysis` (3), `IncomeStatement` (3)
- **Labels seen**:
    - 'Other Components of Net Periodic Pension and OPEB Expense' ×6

```python
    "OtherComponentsOfNetPeriodicPensionAndPostretirementBenefitCost": "TODO — describe this concept",
```

### `RestrictedCash`  *(suggested)*

- **Source concept**: `us-gaap:RestrictedCash`
- **Evidence**: 6 fact(s) across 3 filing(s)
- **Statements**: `Note_18_SupplementalCashFlowInformation` (3), `BalanceSheet` (2), `CashFlow` (1)
- **Labels seen**:
    - 'Restricted cash' ×5
    - 'Restricted cash - end of period' ×1

```python
    "RestrictedCash": "TODO — describe this concept",
```

### `StockIssuedBySubsidiaryOrConsolidatedAffiliateEmployeeTaxShareWithholding`  *(suggested)*

- **Source concept**: `us-gaap:StockIssuedBySubsidiaryOrConsolidatedAffiliateEmployeeTaxShareWithholding`
- **Evidence**: 6 fact(s) across 1 filing(s)
- **Statements**: `ShareholdersEquity` (6)
- **Labels seen**:
    - 'Common stock withheld related to net share settlement of equity awards' ×6

```python
    "StockIssuedBySubsidiaryOrConsolidatedAffiliateEmployeeTaxShareWithholding": "TODO — describe this concept",
```

### `WithholdingOfStockForTaxPurposes`  *(suggested)*

- **Source concept**: `us-gaap:WithholdingOfStockForTaxPurposes`
- **Evidence**: 6 fact(s) across 1 filing(s)
- **Statements**: `ShareholdersEquity` (6)
- **Labels seen**:
    - 'Common stock withheld related to net share settlement of equity awards' ×6

```python
    "WithholdingOfStockForTaxPurposes": "TODO — describe this concept",
```

### `EmployeeCountByFunction`  *(suggested)*

- **Source concept**: `custom:EmployeeCountByFunction`
- **Evidence**: 5 fact(s) across 1 filing(s)
- **Statements**: `Note_NotApplicable_OurPeople` (5)
- **Labels seen**:
    - 'operations' ×1
    - 'research and development' ×1
    - 'sales and marketing' ×1
    - 'general and administrative' ×1
    - 'corporate functions' ×1

```python
    "EmployeeCountByFunction": "TODO — describe this concept",
```

### `OtherGeneralCorporateItems`  *(suggested)*

- **Source concept**: `custom:OtherGeneralCorporateItems`
- **Evidence**: 5 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ManagementDiscussionAndAnalysis` (5)
- **Labels seen**:
    - 'Corporate expenses' ×4
    - 'Income from settlement of a liability for an environmental remediation site' ×1

```python
    "OtherGeneralCorporateItems": "TODO — describe this concept",
```

### `SalesToChinaPercentage`  *(suggested)*

- **Source concept**: `custom:SalesToChinaPercentage`
- **Evidence**: 5 fact(s) across 1 filing(s)
- **Statements**: `Note_NotApplicable_RiskFactors` (3), `Note_NotApplicable_Business` (2)
- **Labels seen**:
    - 'sale of our products as a percentage of our revenues to customers inside of China' ×3
    - 'sales to customers in China' ×2

```python
    "SalesToChinaPercentage": "TODO — describe this concept",
```

### `FairValueAdjustmentOfWarrants`  *(suggested)*

- **Source concept**: `us-gaap:FairValueAdjustmentOfWarrants`
- **Evidence**: 5 fact(s) across 2 filing(s)
- **Statements**: `CashFlow` (4), `IncomeStatement` (1)
- **Labels seen**:
    - 'Change in fair value of warrant liability' ×3
    - 'Loss on warrant liability' ×2

```python
    "FairValueAdjustmentOfWarrants": "TODO — describe this concept",
```

### `ForeignExchangeGainLoss`  *(suggested)*

- **Source concept**: `us-gaap:ForeignExchangeGainLoss`
- **Evidence**: 5 fact(s) across 1 filing(s)
- **Statements**: `Note_7A_QuantitativeAndQualitativeDisclosuresAboutMarketRisk` (3), `Note_NotApplicable_OtherIncomeExpense` (2)
- **Labels seen**:
    - 'net gain from foreign exchange' ×3
    - 'Foreign exchange gains' ×2

```python
    "ForeignExchangeGainLoss": "TODO — describe this concept",
```

### `AveragePricePaidPerShareForRepurchases`  *(suggested)*

- **Source concept**: `custom:AveragePricePaidPerShareForRepurchases`
- **Evidence**: 4 fact(s) across 1 filing(s)
- **Statements**: `Note_5_MarketForRegistrantsCommonEquityRelatedStockholderMattersAndIssuerPurchasesOfEquitySecurities` (4)
- **Labels seen**:
    - 'Average Price Paid per Share' ×4

```python
    "AveragePricePaidPerShareForRepurchases": "TODO — describe this concept",
```

### `ChangeInResearchAndDevelopmentExpense`  *(suggested)*

- **Source concept**: `custom:ChangeInResearchAndDevelopmentExpense`
- **Evidence**: 4 fact(s) across 1 filing(s)
- **Statements**: `Note_NotApplicable_ResearchAndDevelopment` (4)
- **Labels seen**:
    - 'General operational costs' ×1
    - 'Project material costs' ×1
    - 'Stock-based compensation expense' ×1
    - 'Employee compensation costs' ×1

```python
    "ChangeInResearchAndDevelopmentExpense": "TODO — describe this concept",
```

### `CorporateOtherRevenue`  *(suggested)*

- **Source concept**: `custom:CorporateOtherRevenue`
- **Evidence**: 4 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ManagementsDiscussionAndAnalysisOfFinancialConditionAndResultsOfOperations` (4)
- **Labels seen**:
    - 'Corporate Other' ×4

```python
    "CorporateOtherRevenue": "TODO — describe this concept",
```

### `FactoryStartUpCosts`  *(suggested)*

- **Source concept**: `custom:FactoryStartUpCosts`
- **Evidence**: 4 fact(s) across 1 filing(s)
- **Statements**: `IncomeStatement` (2), `Note_NotApplicable_FactoryStartUpCosts` (2)
- **Labels seen**:
    - 'Factory start-up costs' ×4

```python
    "FactoryStartUpCosts": "TODO — describe this concept",
```

### `LitigationAndRelatedCostsAtNL`  *(suggested)*

- **Source concept**: `custom:LitigationAndRelatedCostsAtNL`
- **Evidence**: 4 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ManagementDiscussionAndAnalysis` (4)
- **Labels seen**:
    - 'litigation and related costs at NL' ×4

```python
    "LitigationAndRelatedCostsAtNL": "TODO — describe this concept",
```

### `NumberOfInServiceAircraft`  *(suggested)*

- **Source concept**: `custom:NumberOfInServiceAircraft`
- **Evidence**: 4 fact(s) across 1 filing(s)
- **Statements**: `Note_2_Properties` (4)
- **Labels seen**:
    - 'Number of In-Service Aircraft' ×3
    - 'Total aircraft' ×1

```python
    "NumberOfInServiceAircraft": "TODO — describe this concept",
```

### `NumberOfShareholdersOfRecord`  *(suggested)*

- **Source concept**: `custom:NumberOfShareholdersOfRecord`
- **Evidence**: 4 fact(s) across 1 filing(s)
- **Statements**: `Note_5_MarketForRegistrantsCommonEquity` (4)
- **Labels seen**:
    - 'Holders' ×4

```python
    "NumberOfShareholdersOfRecord": "TODO — describe this concept",
```

### `PercentageOfTotalEmployees`  *(suggested)*

- **Source concept**: `custom:PercentageOfTotalEmployees`
- **Evidence**: 4 fact(s) across 1 filing(s)
- **Statements**: `Note_1_Business` (4)
- **Labels seen**:
    - 'Percentage of total' ×4

```python
    "PercentageOfTotalEmployees": "TODO — describe this concept",
```

### `ResearchAndDevelopmentExpenseAsAPercentageOfRevenue`  *(suggested)*

- **Source concept**: `custom:ResearchAndDevelopmentExpenseAsAPercentageOfRevenue`
- **Evidence**: 4 fact(s) across 1 filing(s)
- **Statements**: `Note_NotApplicable_ResearchAndDevelopment` (4)
- **Labels seen**:
    - '% of revenues' ×4

```python
    "ResearchAndDevelopmentExpenseAsAPercentageOfRevenue": "TODO — describe this concept",
```

### `SeatingCapacityPerAircraft`  *(suggested)*

- **Source concept**: `custom:SeatingCapacityPerAircraft`
- **Evidence**: 4 fact(s) across 1 filing(s)
- **Statements**: `Note_2_Properties` (4)
- **Labels seen**:
    - 'Seating Capacity (per aircraft)' ×4

```python
    "SeatingCapacityPerAircraft": "TODO — describe this concept",
```

### `SellingGeneralAndAdministrativeExpenseAsAPercentageOfRevenue`  *(suggested)*

- **Source concept**: `custom:SellingGeneralAndAdministrativeExpenseAsAPercentageOfRevenue`
- **Evidence**: 4 fact(s) across 1 filing(s)
- **Statements**: `Note_NotApplicable_SellingGeneralAndAdministrative` (4)
- **Labels seen**:
    - '% of revenues' ×4

```python
    "SellingGeneralAndAdministrativeExpenseAsAPercentageOfRevenue": "TODO — describe this concept",
```

### `EntityTaxIdentificationNumber`  *(suggested)*

- **Source concept**: `dei:EntityTaxIdentificationNumber`
- **Evidence**: 4 fact(s) across 4 filing(s)
- **Statements**: `Cover` (4)
- **Labels seen**:
    - 'I.R.S. Employer Identification No.' ×2
    - '11-3363609' ×1
    - '(I.R.S. Employer Identification No.)' ×1

```python
    "EntityTaxIdentificationNumber": "TODO — describe this concept",
```

### `IssuerRepurchasesOfEquitySecuritiesAveragePricePaidPerShare`  *(suggested)*

- **Source concept**: `us-gaap:IssuerRepurchasesOfEquitySecuritiesAveragePricePaidPerShare`
- **Evidence**: 4 fact(s) across 1 filing(s)
- **Statements**: `Note_5_MarketForRegistrantsCommonEquity` (4)
- **Labels seen**:
    - 'Average Price Paid per Share' ×4

```python
    "IssuerRepurchasesOfEquitySecuritiesAveragePricePaidPerShare": "TODO — describe this concept",
```

### `IssuerRepurchasesOfEquitySecuritiesShares`  *(suggested)*

- **Source concept**: `us-gaap:IssuerRepurchasesOfEquitySecuritiesShares`
- **Evidence**: 4 fact(s) across 1 filing(s)
- **Statements**: `Note_5_MarketForRegistrantsCommonEquity` (4)
- **Labels seen**:
    - 'Total Number of Shares Purchased' ×4

```python
    "IssuerRepurchasesOfEquitySecuritiesShares": "TODO — describe this concept",
```

### `MarketRiskInterestRateRiskExposure`  *(suggested)*

- **Source concept**: `us-gaap:MarketRiskInterestRateRiskExposure`
- **Evidence**: 4 fact(s) across 1 filing(s)
- **Statements**: `Note_7A_QuantitativeAndQualitativeDisclosures` (4)
- **Labels seen**:
    - 'Decline in fair value' ×2
    - 'Increase in annual interest expense' ×2

```python
    "MarketRiskInterestRateRiskExposure": "TODO — describe this concept",
```

### `OccupancyExpense`  *(suggested)*

- **Source concept**: `us-gaap:OccupancyExpense`
- **Evidence**: 4 fact(s) across 2 filing(s)
- **Statements**: `IncomeStatement` (2), `Note_7_ManagementDiscussionAndAnalysis` (2)
- **Labels seen**:
    - 'Occupancy expense, net' ×2
    - 'Occupancy' ×2

```python
    "OccupancyExpense": "TODO — describe this concept",
```

### `OtherNoninterestIncome`  *(suggested)*

- **Source concept**: `us-gaap:OtherNoninterestIncome`
- **Evidence**: 4 fact(s) across 1 filing(s)
- **Statements**: `IncomeStatement` (4)
- **Labels seen**:
    - 'Net gains on other investments' ×2
    - 'Other income' ×2

```python
    "OtherNoninterestIncome": "TODO — describe this concept",
```

### `PensionPlanContributions`  *(suggested)*

- **Source concept**: `us-gaap:PensionPlanContributions`
- **Evidence**: 4 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ManagementDiscussionAndAnalysis` (4)
- **Labels seen**:
    - 'Contributions to all of our defined benefit pension plans' ×3
    - 'Contributions' ×1

```python
    "PensionPlanContributions": "TODO — describe this concept",
```

### `SalariesAndEmployeeBenefits`  *(suggested)*

- **Source concept**: `us-gaap:SalariesAndEmployeeBenefits`
- **Evidence**: 4 fact(s) across 1 filing(s)
- **Statements**: `IncomeStatement` (4)
- **Labels seen**:
    - 'Salaries and wages' ×2
    - 'Employee benefits' ×2

```python
    "SalariesAndEmployeeBenefits": "TODO — describe this concept",
```

### `StockRepurchaseProgramRemainingAmount`  *(suggested)*

- **Source concept**: `us-gaap:StockRepurchaseProgramRemainingAmount`
- **Evidence**: 4 fact(s) across 1 filing(s)
- **Statements**: `Note_5_MarketForRegistrantsCommonEquity` (4)
- **Labels seen**:
    - 'Approximate Dollar Value of Shares that May Yet be Purchased Under the Plans or Programs' ×4

```python
    "StockRepurchaseProgramRemainingAmount": "TODO — describe this concept",
```

### `ValueAtRisk`  *(suggested)*

- **Source concept**: `us-gaap:ValueAtRisk`
- **Evidence**: 4 fact(s) across 1 filing(s)
- **Statements**: `Note_7A_QuantitativeAndQualitativeDisclosures` (2), `Note_7A_QuantitativeAndQualitativeDisclosuresAboutMarketRisk` (2)
- **Labels seen**:
    - 'maximum one-day loss in fair value' ×2
    - 'a maximum one-day loss in fair value of $538 million' ×1
    - 'and $669 million as of September 30, 2023' ×1

```python
    "ValueAtRisk": "TODO — describe this concept",
```

### `AircraftLeaseRentals`  *(suggested)*

- **Source concept**: `custom:AircraftLeaseRentals`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `IncomeStatement` (3)
- **Labels seen**:
    - 'Aircraft lease rentals' ×3

```python
    "AircraftLeaseRentals": "TODO — describe this concept",
```

### `AircraftPreDeliveryDeposits`  *(suggested)*

- **Source concept**: `custom:AircraftPreDeliveryDeposits`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (3)
- **Labels seen**:
    - 'Aircraft pre-delivery deposits' ×3

```python
    "AircraftPreDeliveryDeposits": "TODO — describe this concept",
```

### `AverageAgeInYears`  *(suggested)*

- **Source concept**: `custom:AverageAgeInYears`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `Note_2_Properties` (3)
- **Labels seen**:
    - 'Average Age in Years' ×3

```python
    "AverageAgeInYears": "TODO — describe this concept",
```

### `AveragePricePaidPerShareRepurchased`  *(suggested)*

- **Source concept**: `custom:AveragePricePaidPerShareRepurchased`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `Note_5_MarketForRegistrantsCommonEquity` (3)
- **Labels seen**:
    - 'Average Price Paid per Share' ×3

```python
    "AveragePricePaidPerShareRepurchased": "TODO — describe this concept",
```

### `ChangeInAccruedPilotRetentionBonus`  *(suggested)*

- **Source concept**: `custom:ChangeInAccruedPilotRetentionBonus`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (3)
- **Labels seen**:
    - 'Accrued pilot retention bonus' ×3

```python
    "ChangeInAccruedPilotRetentionBonus": "TODO — describe this concept",
```

### `ChangeInAirTrafficLiability`  *(suggested)*

- **Source concept**: `custom:ChangeInAirTrafficLiability`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (3)
- **Labels seen**:
    - 'Air traffic liability' ×3

```python
    "ChangeInAirTrafficLiability": "TODO — describe this concept",
```

### `ChangeInDeferredMajorMaintenance`  *(suggested)*

- **Source concept**: `custom:ChangeInDeferredMajorMaintenance`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (3)
- **Labels seen**:
    - 'Deferred major maintenance' ×3

```python
    "ChangeInDeferredMajorMaintenance": "TODO — describe this concept",
```

### `ChangeInLoyaltyProgramLiability`  *(suggested)*

- **Source concept**: `custom:ChangeInLoyaltyProgramLiability`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (3)
- **Labels seen**:
    - 'Loyalty program liability' ×3

```python
    "ChangeInLoyaltyProgramLiability": "TODO — describe this concept",
```

### `CostOfSales`  *(suggested)*

- **Source concept**: `custom:CostOfSales`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ManagementDiscussionAndAnalysis` (3)
- **Labels seen**:
    - 'Cost of sales' ×3

```python
    "CostOfSales": "TODO — describe this concept",
```

### `DividendsAndDividendEquivalentsDeclaredPerShareOrRSU`  *(suggested)*

- **Source concept**: `custom:DividendsAndDividendEquivalentsDeclaredPerShareOrRSU`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `ShareholdersEquity` (3)
- **Labels seen**:
    - 'Dividends and dividend equivalents declared per share or RSU' ×3

```python
    "DividendsAndDividendEquivalentsDeclaredPerShareOrRSU": "TODO — describe this concept",
```

### `EmployeeCountByRegion`  *(suggested)*

- **Source concept**: `custom:EmployeeCountByRegion`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `Note_NotApplicable_OurPeople` (3)
- **Labels seen**:
    - 'North America' ×1
    - 'Asia' ×1
    - 'Europe' ×1

```python
    "EmployeeCountByRegion": "TODO — describe this concept",
```

### `FixedFeeContractsRevenue`  *(suggested)*

- **Source concept**: `custom:FixedFeeContractsRevenue`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `IncomeStatement` (3)
- **Labels seen**:
    - 'Fixed fee contracts' ×3

```python
    "FixedFeeContractsRevenue": "TODO — describe this concept",
```

### `GainLossOnIntraEntityForeignCurrencyTransactions`  *(suggested)*

- **Source concept**: `custom:GainLossOnIntraEntityForeignCurrencyTransactions`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `ComprehensiveIncome` (3)
- **Labels seen**:
    - 'Gain (loss) on intra-entity foreign currency transactions' ×3

```python
    "GainLossOnIntraEntityForeignCurrencyTransactions": "TODO — describe this concept",
```

### `GrossMarginPercentageProducts`  *(suggested)*

- **Source concept**: `custom:GrossMarginPercentageProducts`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ManagementDiscussionAndAnalysis` (3)
- **Labels seen**:
    - 'Products' ×3

```python
    "GrossMarginPercentageProducts": "TODO — describe this concept",
```

### `GrossMarginPercentageServices`  *(suggested)*

- **Source concept**: `custom:GrossMarginPercentageServices`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ManagementDiscussionAndAnalysis` (3)
- **Labels seen**:
    - 'Services' ×3

```python
    "GrossMarginPercentageServices": "TODO — describe this concept",
```

### `InternationalSalesPercentage`  *(suggested)*

- **Source concept**: `custom:InternationalSalesPercentage`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `Note_NotApplicable_RiskFactors` (3)
- **Labels seen**:
    - 'international sales as a percentage of our revenues' ×3

```python
    "InternationalSalesPercentage": "TODO — describe this concept",
```

### `LandSales`  *(suggested)*

- **Source concept**: `custom:LandSales`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ManagementDiscussionAndAnalysis` (3)
- **Labels seen**:
    - 'Land sales' ×3

```python
    "LandSales": "TODO — describe this concept",
```

### `MaintenanceAndRepairsExpense`  *(suggested)*

- **Source concept**: `custom:MaintenanceAndRepairsExpense`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `IncomeStatement` (3)
- **Labels seen**:
    - 'Maintenance and repairs' ×3

```python
    "MaintenanceAndRepairsExpense": "TODO — describe this concept",
```

### `OperatingExpensesAsPercentageOfRevenue`  *(suggested)*

- **Source concept**: `custom:OperatingExpensesAsPercentageOfRevenue`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `Note_7_MDA` (3)
- **Labels seen**:
    - 'Percentage of total net sales' ×3

```python
    "OperatingExpensesAsPercentageOfRevenue": "TODO — describe this concept",
```

### `PassengerRevenue`  *(suggested)*

- **Source concept**: `custom:PassengerRevenue`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `IncomeStatement` (3)
- **Labels seen**:
    - 'Passenger' ×3

```python
    "PassengerRevenue": "TODO — describe this concept",
```

### `ProceedsFromSunseekerConstructionFinancingAccount`  *(suggested)*

- **Source concept**: `custom:ProceedsFromSunseekerConstructionFinancingAccount`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (3)
- **Labels seen**:
    - 'Proceeds from Sunseeker construction financing account' ×3

```python
    "ProceedsFromSunseekerConstructionFinancingAccount": "TODO — describe this concept",
```

### `PropertyPlantAndEquipmentAdditionsInAccountsPayable`  *(suggested)*

- **Source concept**: `custom:PropertyPlantAndEquipmentAdditionsInAccountsPayable`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `Note_18_SupplementalCashFlowInformation` (3)
- **Labels seen**:
    - 'Furniture, equipment, software and leasehold improvement additions included in accounts…' ×3

```python
    "PropertyPlantAndEquipmentAdditionsInAccountsPayable": "TODO — describe this concept",
```

### `PurchaseObligations`  *(suggested)*

- **Source concept**: `custom:PurchaseObligations`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `Note_7A_QuantitativeAndQualitativeDisclosuresAboutMarketRisk` (3)
- **Labels seen**:
    - 'Purchase obligations' ×1
    - 'Purchase obligations payable in 2026' ×1
    - 'Purchase obligations payable in 2027/2028' ×1

```python
    "PurchaseObligations": "TODO — describe this concept",
```

### `ResearchAndDevelopmentExpenseAsPercentageOfRevenue`  *(suggested)*

- **Source concept**: `custom:ResearchAndDevelopmentExpenseAsPercentageOfRevenue`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `Note_7_MDA` (3)
- **Labels seen**:
    - 'Percentage of total net sales' ×3

```python
    "ResearchAndDevelopmentExpenseAsPercentageOfRevenue": "TODO — describe this concept",
```

### `ResortAndOtherRevenue`  *(suggested)*

- **Source concept**: `custom:ResortAndOtherRevenue`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `IncomeStatement` (3)
- **Labels seen**:
    - 'Resort and other' ×3

```python
    "ResortAndOtherRevenue": "TODO — describe this concept",
```

### `SellingGeneralAndAdministrativeExpenseAsPercentageOfRevenue`  *(suggested)*

- **Source concept**: `custom:SellingGeneralAndAdministrativeExpenseAsPercentageOfRevenue`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `Note_7_MDA` (3)
- **Labels seen**:
    - 'Percentage of total net sales' ×3

```python
    "SellingGeneralAndAdministrativeExpenseAsPercentageOfRevenue": "TODO — describe this concept",
```

### `ShareRepurchaseRemainingAuthorizationValue`  *(suggested)*

- **Source concept**: `custom:ShareRepurchaseRemainingAuthorizationValue`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `Note_5_MarketForRegistrantsCommonEquityRelatedStockholderMattersAndIssuerPurchasesOfEquitySecurities` (3)
- **Labels seen**:
    - 'Approximate Dollar Value of Shares that May Yet be Purchased Under the Program' ×3

```python
    "ShareRepurchaseRemainingAuthorizationValue": "TODO — describe this concept",
```

### `SpecialChargesCashFlow`  *(suggested)*

- **Source concept**: `custom:SpecialChargesCashFlow`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (3)
- **Labels seen**:
    - 'Special charges' ×3

```python
    "SpecialChargesCashFlow": "TODO — describe this concept",
```

### `StateAidDecisionTaxPayable`  *(suggested)*

- **Source concept**: `custom:StateAidDecisionTaxPayable`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `Note_7_MDA` (2), `Note_7_ManagementDiscussionAndAnalysis` (1)
- **Labels seen**:
    - 'obligation to pay €14.2 billion or $15.8 billion to Ireland' ×2
    - 'State Aid Decision Tax Payable' ×1

```python
    "StateAidDecisionTaxPayable": "TODO — describe this concept",
```

### `StationOperationsExpense`  *(suggested)*

- **Source concept**: `custom:StationOperationsExpense`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `IncomeStatement` (3)
- **Labels seen**:
    - 'Station operations' ×3

```python
    "StationOperationsExpense": "TODO — describe this concept",
```

### `ThirdPartyProductsRevenue`  *(suggested)*

- **Source concept**: `custom:ThirdPartyProductsRevenue`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `IncomeStatement` (3)
- **Labels seen**:
    - 'Third party products' ×3

```python
    "ThirdPartyProductsRevenue": "TODO — describe this concept",
```

### `TiO2ProductionVolumes`  *(suggested)*

- **Source concept**: `custom:TiO2ProductionVolumes`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ManagementDiscussionAndAnalysis` (3)
- **Labels seen**:
    - 'Production volumes' ×3

```python
    "TiO2ProductionVolumes": "TODO — describe this concept",
```

### `TiO2SalesVolumes`  *(suggested)*

- **Source concept**: `custom:TiO2SalesVolumes`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ManagementDiscussionAndAnalysis` (3)
- **Labels seen**:
    - 'Sales volumes' ×3

```python
    "TiO2SalesVolumes": "TODO — describe this concept",
```

### `UnrealizedForeignCurrencyExchangeRateGainLoss`  *(suggested)*

- **Source concept**: `custom:UnrealizedForeignCurrencyExchangeRateGainLoss`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (3)
- **Labels seen**:
    - 'Unrealized foreign currency exchange rate (gain) loss' ×3

```python
    "UnrealizedForeignCurrencyExchangeRateGainLoss": "TODO — describe this concept",
```

### `UtilityAndOtherNetSales`  *(suggested)*

- **Source concept**: `custom:UtilityAndOtherNetSales`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ManagementDiscussionAndAnalysis` (3)
- **Labels seen**:
    - 'Utility and other' ×3

```python
    "UtilityAndOtherNetSales": "TODO — describe this concept",
```

### `DocumentFiscalYearFocus`  *(suggested)*

- **Source concept**: `dei:DocumentFiscalYearFocus`
- **Evidence**: 3 fact(s) across 3 filing(s)
- **Statements**: `Cover` (3)
- **Labels seen**:
    - 'For the fiscal year ended December 31, 2025' ×2
    - 'For the fiscal year ended March 31, 2025' ×1

```python
    "DocumentFiscalYearFocus": "TODO — describe this concept",
```

### `AcquisitionOfPropertyPlantAndEquipmentInExchangeForLiabilities`  *(suggested)*

- **Source concept**: `us-gaap:AcquisitionOfPropertyPlantAndEquipmentInExchangeForLiabilities`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (3)
- **Labels seen**:
    - 'Purchases of property and equipment in accrued liabilities and other' ×3

```python
    "AcquisitionOfPropertyPlantAndEquipmentInExchangeForLiabilities": "TODO — describe this concept",
```

### `AmortizationOfDebtDiscountPremium`  *(suggested)*

- **Source concept**: `us-gaap:AmortizationOfDebtDiscountPremium`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (3)
- **Labels seen**:
    - 'Debt accretion expense' ×3

```python
    "AmortizationOfDebtDiscountPremium": "TODO — describe this concept",
```

### `AmortizationOfDebtDiscountPremiumAndAccretionOfSecurities`  *(suggested)*

- **Source concept**: `us-gaap:AmortizationOfDebtDiscountPremiumAndAccretionOfSecurities`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (3)
- **Labels seen**:
    - 'Noncash interest expense' ×3

```python
    "AmortizationOfDebtDiscountPremiumAndAccretionOfSecurities": "TODO — describe this concept",
```

### `AmortizationOfDebtDiscountPremiumAndDebtIssuanceCosts`  *(suggested)*

- **Source concept**: `us-gaap:AmortizationOfDebtDiscountPremiumAndDebtIssuanceCosts`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (3)
- **Labels seen**:
    - 'Amortization of debt issuance costs and original issue discount' ×3

```python
    "AmortizationOfDebtDiscountPremiumAndDebtIssuanceCosts": "TODO — describe this concept",
```

### `AmortizationOfOperatingLeaseRightOfUseAsset`  *(suggested)*

- **Source concept**: `us-gaap:AmortizationOfOperatingLeaseRightOfUseAsset`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (3)
- **Labels seen**:
    - '(Increase)/Decrease in Operating right-of-use assets' ×3

```python
    "AmortizationOfOperatingLeaseRightOfUseAsset": "TODO — describe this concept",
```

### `CapitalContributionsFromNoncontrollingInterest`  *(suggested)*

- **Source concept**: `us-gaap:CapitalContributionsFromNoncontrollingInterest`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (3)
- **Labels seen**:
    - "Members' contributions" ×3

```python
    "CapitalContributionsFromNoncontrollingInterest": "TODO — describe this concept",
```

### `CashCashEquivalentsAndMarketableSecurities`  *(suggested)*

- **Source concept**: `us-gaap:CashCashEquivalentsAndMarketableSecurities`
- **Evidence**: 3 fact(s) across 2 filing(s)
- **Statements**: `Note_NotApplicable_LiquidityAndCapitalResources` (2), `Note_7_ManagementDiscussionAndAnalysis` (1)
- **Labels seen**:
    - 'cash, cash equivalents and marketable securities' ×2
    - 'The Company believes its balances of unrestricted cash, cash equivalents and marketable…' ×1

```python
    "CashCashEquivalentsAndMarketableSecurities": "TODO — describe this concept",
```

### `CommitmentsAndContingencies`  *(suggested)*

- **Source concept**: `us-gaap:CommitmentsAndContingencies`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ManagementDiscussionAndAnalysis` (3)
- **Labels seen**:
    - 'Credit available under existing facilities' ×1
    - 'Available under Kronos’ global revolving credit facility' ×1
    - 'Available under Valhi’s Contran credit facility' ×1

```python
    "CommitmentsAndContingencies": "TODO — describe this concept",
```

### `CommonStockAndAdditionalPaidInCapital`  *(suggested)*

- **Source concept**: `us-gaap:CommonStockAndAdditionalPaidInCapital`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `ShareholdersEquity` (3)
- **Labels seen**:
    - 'Beginning balances' ×3

```python
    "CommonStockAndAdditionalPaidInCapital": "TODO — describe this concept",
```

### `ComprehensiveIncomeNetOfTaxAttributableToNoncontrollingInterest`  *(suggested)*

- **Source concept**: `us-gaap:ComprehensiveIncomeNetOfTaxAttributableToNoncontrollingInterest`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `ComprehensiveIncome` (3)
- **Labels seen**:
    - 'Comprehensive income attributable to noncontrolling interest' ×3

```python
    "ComprehensiveIncomeNetOfTaxAttributableToNoncontrollingInterest": "TODO — describe this concept",
```

### `ComprehensiveIncomeNetOfTaxAttributableToParent`  *(suggested)*

- **Source concept**: `us-gaap:ComprehensiveIncomeNetOfTaxAttributableToParent`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `ComprehensiveIncome` (3)
- **Labels seen**:
    - 'Comprehensive income (loss) attributable to Valhi stockholders' ×3

```python
    "ComprehensiveIncomeNetOfTaxAttributableToParent": "TODO — describe this concept",
```

### `CostsAndExpenses`  *(suggested)*

- **Source concept**: `us-gaap:CostsAndExpenses`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `IncomeStatement` (3)
- **Labels seen**:
    - 'Total costs and other expense' ×3

```python
    "CostsAndExpenses": "TODO — describe this concept",
```

### `DebtIssuanceCosts`  *(suggested)*

- **Source concept**: `us-gaap:DebtIssuanceCosts`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (3)
- **Labels seen**:
    - 'Debt issuance costs' ×3

```python
    "DebtIssuanceCosts": "TODO — describe this concept",
```

### `DeferredGovernmentAssistance`  *(suggested)*

- **Source concept**: `us-gaap:DeferredGovernmentAssistance`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `BalanceSheet` (2), `Note_12_CommitmentsAndContingencies` (1)
- **Labels seen**:
    - 'Deferred grant' ×3

```python
    "DeferredGovernmentAssistance": "TODO — describe this concept",
```

### `DeferredTaxAssets`  *(suggested)*

- **Source concept**: `us-gaap:DeferredTaxAssets`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `Note_18_SupplementalCashFlowInformation` (3)
- **Labels seen**:
    - 'Deferred tax asset' ×3

```python
    "DeferredTaxAssets": "TODO — describe this concept",
```

### `Depreciation`  *(suggested)*

- **Source concept**: `us-gaap:Depreciation`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (3)
- **Labels seen**:
    - 'Depreciation and amortization of property and equipment' ×3

```python
    "Depreciation": "TODO — describe this concept",
```

### `DistributionsToNoncontrollingInterest`  *(suggested)*

- **Source concept**: `us-gaap:DistributionsToNoncontrollingInterest`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (3)
- **Labels seen**:
    - "Members' distributions" ×3

```python
    "DistributionsToNoncontrollingInterest": "TODO — describe this concept",
```

### `DividendsAndEquivalents`  *(suggested)*

- **Source concept**: `us-gaap:DividendsAndEquivalents`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `ShareholdersEquity` (3)
- **Labels seen**:
    - 'Dividends and dividend equivalents declared' ×3

```python
    "DividendsAndEquivalents": "TODO — describe this concept",
```

### `DividendsPaidToNoncontrollingInterests`  *(suggested)*

- **Source concept**: `us-gaap:DividendsPaidToNoncontrollingInterests`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `ShareholdersEquity` (3)
- **Labels seen**:
    - 'Dividends paid to noncontrolling interest' ×3

```python
    "DividendsPaidToNoncontrollingInterests": "TODO — describe this concept",
```

### `ForeignCurrencyTransactionGainLoss`  *(suggested)*

- **Source concept**: `us-gaap:ForeignCurrencyTransactionGainLoss`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (3)
- **Labels seen**:
    - 'Foreign currency exchange losses (gains)' ×3

```python
    "ForeignCurrencyTransactionGainLoss": "TODO — describe this concept",
```

### `FuelAndOilExpense`  *(suggested)*

- **Source concept**: `us-gaap:FuelAndOilExpense`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `IncomeStatement` (3)
- **Labels seen**:
    - 'Aircraft fuel' ×3

```python
    "FuelAndOilExpense": "TODO — describe this concept",
```

### `GainLossOnSaleOfPropertyAndEquipment`  *(suggested)*

- **Source concept**: `us-gaap:GainLossOnSaleOfPropertyAndEquipment`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (3)
- **Labels seen**:
    - '(Gain) loss on aircraft and other equipment disposals' ×3

```python
    "GainLossOnSaleOfPropertyAndEquipment": "TODO — describe this concept",
```

### `ImpairmentOfLongLivedAssets`  *(suggested)*

- **Source concept**: `us-gaap:ImpairmentOfLongLivedAssets`
- **Evidence**: 3 fact(s) across 2 filing(s)
- **Statements**: `CashFlow` (3)
- **Labels seen**:
    - 'Impairment of assets' ×2
    - 'Fixed asset impairment' ×1

```python
    "ImpairmentOfLongLivedAssets": "TODO — describe this concept",
```

### `IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments`  *(suggested)*

- **Source concept**: `us-gaap:IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `IncomeStatement` (3)
- **Labels seen**:
    - 'Loss before income taxes' ×3

```python
    "IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments": "TODO — describe this concept",
```

### `IncomeTaxBenefitFromStockBasedCompensation`  *(suggested)*

- **Source concept**: `us-gaap:IncomeTaxBenefitFromStockBasedCompensation`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `Note_11_ShareBasedCompensation` (3)
- **Labels seen**:
    - 'Income tax benefit related to share-based compensation expense' ×3

```python
    "IncomeTaxBenefitFromStockBasedCompensation": "TODO — describe this concept",
```

### `IncreaseDecreaseInAccountsPayableRelatedParties`  *(suggested)*

- **Source concept**: `us-gaap:IncreaseDecreaseInAccountsPayableRelatedParties`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (3)
- **Labels seen**:
    - 'Increase/(Decrease) in Accounts payable - related party' ×3

```python
    "IncreaseDecreaseInAccountsPayableRelatedParties": "TODO — describe this concept",
```

### `IncreaseDecreaseInOperatingLeaseLiability`  *(suggested)*

- **Source concept**: `us-gaap:IncreaseDecreaseInOperatingLeaseLiability`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (3)
- **Labels seen**:
    - 'Increase/(Decrease) in Operating lease liabilities' ×3

```python
    "IncreaseDecreaseInOperatingLeaseLiability": "TODO — describe this concept",
```

### `IncreaseDecreaseInReceivablesFromRelatedParties`  *(suggested)*

- **Source concept**: `us-gaap:IncreaseDecreaseInReceivablesFromRelatedParties`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (3)
- **Labels seen**:
    - '(Increase)/Decrease in Accounts receivable - related party' ×3

```python
    "IncreaseDecreaseInReceivablesFromRelatedParties": "TODO — describe this concept",
```

### `IncreaseDecreaseInRetainedEarnings`  *(suggested)*

- **Source concept**: `us-gaap:IncreaseDecreaseInRetainedEarnings`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `ShareholdersEquity` (3)
- **Labels seen**:
    - 'Net income' ×3

```python
    "IncreaseDecreaseInRetainedEarnings": "TODO — describe this concept",
```

### `InsuranceProceeds`  *(suggested)*

- **Source concept**: `us-gaap:InsuranceProceeds`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (3)
- **Labels seen**:
    - 'Insurance proceeds from damage to property & equipment' ×3

```python
    "InsuranceProceeds": "TODO — describe this concept",
```

### `InterestCapitalized`  *(suggested)*

- **Source concept**: `us-gaap:InterestCapitalized`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `IncomeStatement` (3)
- **Labels seen**:
    - 'Capitalized interest' ×3

```python
    "InterestCapitalized": "TODO — describe this concept",
```

### `IssuanceOfStock`  *(suggested)*

- **Source concept**: `us-gaap:IssuanceOfStock`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `Note_10_ShareholdersEquity` (3)
- **Labels seen**:
    - 'Common stock issued, net of shares withheld for employee taxes' ×3

```python
    "IssuanceOfStock": "TODO — describe this concept",
```

### `NoncashInvestingAndFinancingActivitiesChangeInAccrualForPropertyAndEquipment`  *(suggested)*

- **Source concept**: `us-gaap:NoncashInvestingAndFinancingActivitiesChangeInAccrualForPropertyAndEquipment`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (3)
- **Labels seen**:
    - 'Change in accrual for property and equipment' ×3

```python
    "NoncashInvestingAndFinancingActivitiesChangeInAccrualForPropertyAndEquipment": "TODO — describe this concept",
```

### `NoncashInvestingAndFinancingActivitiesDisclosure`  *(suggested)*

- **Source concept**: `us-gaap:NoncashInvestingAndFinancingActivitiesDisclosure`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (3)
- **Labels seen**:
    - 'Right-of-use (ROU) assets acquired' ×3

```python
    "NoncashInvestingAndFinancingActivitiesDisclosure": "TODO — describe this concept",
```

### `OperatingCostsAndExpenses`  *(suggested)*

- **Source concept**: `us-gaap:OperatingCostsAndExpenses`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `IncomeStatement` (3)
- **Labels seen**:
    - 'Total operating expenses' ×3

```python
    "OperatingCostsAndExpenses": "TODO — describe this concept",
```

### `OperatingLeaseRightOfUseAssetObtainedInExchangeForLeaseObligations`  *(suggested)*

- **Source concept**: `us-gaap:OperatingLeaseRightOfUseAssetObtainedInExchangeForLeaseObligations`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `Note_18_SupplementalCashFlowInformation` (3)
- **Labels seen**:
    - 'Lease right-of-use assets obtained in exchange for lease liabilities, net of modificati…' ×3

```python
    "OperatingLeaseRightOfUseAssetObtainedInExchangeForLeaseObligations": "TODO — describe this concept",
```

### `OtherComprehensiveIncomeDefinedBenefitPlansAdjustmentNetOfTax`  *(suggested)*

- **Source concept**: `us-gaap:OtherComprehensiveIncomeDefinedBenefitPlansAdjustmentNetOfTax`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `ComprehensiveIncome` (3)
- **Labels seen**:
    - 'Employee retirement benefits' ×3

```python
    "OtherComprehensiveIncomeDefinedBenefitPlansAdjustmentNetOfTax": "TODO — describe this concept",
```

### `OtherComprehensiveIncomeLossDerivativeInstrumentsGainLossNetOfTaxBeforeReclassification`  *(suggested)*

- **Source concept**: `us-gaap:OtherComprehensiveIncomeLossDerivativeInstrumentsGainLossNetOfTaxBeforeReclassification`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `ComprehensiveIncome` (3)
- **Labels seen**:
    - 'Change in fair value of derivative instruments' ×3

```python
    "OtherComprehensiveIncomeLossDerivativeInstrumentsGainLossNetOfTaxBeforeReclassification": "TODO — describe this concept",
```

### `OtherComprehensiveIncomeLossMarketableSecuritiesNetOfTaxBeforeReclassification`  *(suggested)*

- **Source concept**: `us-gaap:OtherComprehensiveIncomeLossMarketableSecuritiesNetOfTaxBeforeReclassification`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `ComprehensiveIncome` (3)
- **Labels seen**:
    - 'Change in fair value of marketable debt securities' ×3

```python
    "OtherComprehensiveIncomeLossMarketableSecuritiesNetOfTaxBeforeReclassification": "TODO — describe this concept",
```

### `OtherComprehensiveIncomeLossNetOfTax`  *(suggested)*

- **Source concept**: `us-gaap:OtherComprehensiveIncomeLossNetOfTax`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `ShareholdersEquity` (3)
- **Labels seen**:
    - 'Other comprehensive income/(loss)' ×3

```python
    "OtherComprehensiveIncomeLossNetOfTax": "TODO — describe this concept",
```

### `OtherComprehensiveIncomeLossNetOfTaxAttributableToNoncontrollingInterest`  *(suggested)*

- **Source concept**: `us-gaap:OtherComprehensiveIncomeLossNetOfTaxAttributableToNoncontrollingInterest`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `ShareholdersEquity` (3)
- **Labels seen**:
    - 'Other comprehensive loss, net' ×2
    - 'Other comprehensive income, net' ×1

```python
    "OtherComprehensiveIncomeLossNetOfTaxAttributableToNoncontrollingInterest": "TODO — describe this concept",
```

### `OtherComprehensiveIncomePensionAndOtherPostretirementBenefitPlansAdjustmentNetOfTax`  *(suggested)*

- **Source concept**: `us-gaap:OtherComprehensiveIncomePensionAndOtherPostretirementBenefitPlansAdjustmentNetOfTax`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `ComprehensiveIncome` (3)
- **Labels seen**:
    - 'Defined benefit pension plans' ×3

```python
    "OtherComprehensiveIncomePensionAndOtherPostretirementBenefitPlansAdjustmentNetOfTax": "TODO — describe this concept",
```

### `OtherCostOfRevenue`  *(suggested)*

- **Source concept**: `us-gaap:OtherCostOfRevenue`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `IncomeStatement` (3)
- **Labels seen**:
    - 'Medical supplies' ×3

```python
    "OtherCostOfRevenue": "TODO — describe this concept",
```

### `OtherOperatingCostAndExpense`  *(suggested)*

- **Source concept**: `us-gaap:OtherOperatingCostAndExpense`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `IncomeStatement` (3)
- **Labels seen**:
    - 'Other' ×3

```python
    "OtherOperatingCostAndExpense": "TODO — describe this concept",
```

### `OtherOperatingIncomeExpense`  *(suggested)*

- **Source concept**: `us-gaap:OtherOperatingIncomeExpense`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `IncomeStatement` (3)
- **Labels seen**:
    - 'Other' ×3

```python
    "OtherOperatingIncomeExpense": "TODO — describe this concept",
```

### `PaymentOfTaxWithheldOnStockIssued`  *(suggested)*

- **Source concept**: `us-gaap:PaymentOfTaxWithheldOnStockIssued`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (3)
- **Labels seen**:
    - 'Employee taxes paid for shares withheld for income taxes' ×3

```python
    "PaymentOfTaxWithheldOnStockIssued": "TODO — describe this concept",
```

### `PaymentsForTaxWithholdingForShareBasedCompensation`  *(suggested)*

- **Source concept**: `us-gaap:PaymentsForTaxWithholdingForShareBasedCompensation`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (3)
- **Labels seen**:
    - 'Payments for taxes related to net share settlement of equity awards' ×3

```python
    "PaymentsForTaxWithholdingForShareBasedCompensation": "TODO — describe this concept",
```

### `PaymentsToAcquireCommonStockAveragePricePerShare`  *(suggested)*

- **Source concept**: `us-gaap:PaymentsToAcquireCommonStockAveragePricePerShare`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `Note_5_MarketForRegistrantsCommonEquity` (3)
- **Labels seen**:
    - 'Average Price Paid Per Share' ×3

```python
    "PaymentsToAcquireCommonStockAveragePricePerShare": "TODO — describe this concept",
```

### `PensionAndOtherPostretirementBenefitExpense`  *(suggested)*

- **Source concept**: `us-gaap:PensionAndOtherPostretirementBenefitExpense`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (3)
- **Labels seen**:
    - 'Benefit plan expense less than cash funding' ×3

```python
    "PensionAndOtherPostretirementBenefitExpense": "TODO — describe this concept",
```

### `PensionPlanSettlementLoss`  *(suggested)*

- **Source concept**: `us-gaap:PensionPlanSettlementLoss`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (2), `Note_7_ManagementDiscussionAndAnalysis` (1)
- **Labels seen**:
    - 'Settlement loss on pension plan termination and buyout' ×2
    - 'Non-cash settlement loss on the U.S. pension plan termination and buy-out' ×1

```python
    "PensionPlanSettlementLoss": "TODO — describe this concept",
```

### `ProceedsFromIssuanceOfCommonStockUnderEmployeeStockPurchasePlan`  *(suggested)*

- **Source concept**: `us-gaap:ProceedsFromIssuanceOfCommonStockUnderEmployeeStockPurchasePlan`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `ShareholdersEquity` (3)
- **Labels seen**:
    - 'Stock issued under employee stock purchase plan' ×3

```python
    "ProceedsFromIssuanceOfCommonStockUnderEmployeeStockPurchasePlan": "TODO — describe this concept",
```

### `ProceedsFromLoanReceivable`  *(suggested)*

- **Source concept**: `us-gaap:ProceedsFromLoanReceivable`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (3)
- **Labels seen**:
    - 'Proceeds from loan receivable' ×3

```python
    "ProceedsFromLoanReceivable": "TODO — describe this concept",
```

### `ProceedsFromRepaymentsOfCommercialPaper`  *(suggested)*

- **Source concept**: `us-gaap:ProceedsFromRepaymentsOfCommercialPaper`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (3)
- **Labels seen**:
    - 'Proceeds from/(Repayments of) commercial paper, net' ×3

```python
    "ProceedsFromRepaymentsOfCommercialPaper": "TODO — describe this concept",
```

### `ReclassificationOutOfAccumulatedOtherComprehensiveIncomeForDerivativeInstrumentsNetOfTax`  *(suggested)*

- **Source concept**: `us-gaap:ReclassificationOutOfAccumulatedOtherComprehensiveIncomeForDerivativeInstrumentsNetOfTax`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `ComprehensiveIncome` (3)
- **Labels seen**:
    - 'Adjustment for net (gains)/losses realized and included in net income' ×3

```python
    "ReclassificationOutOfAccumulatedOtherComprehensiveIncomeForDerivativeInstrumentsNetOfTax": "TODO — describe this concept",
```

### `ReclassificationOutOfAccumulatedOtherComprehensiveIncomeForMarketableSecuritiesNetOfTax`  *(suggested)*

- **Source concept**: `us-gaap:ReclassificationOutOfAccumulatedOtherComprehensiveIncomeForMarketableSecuritiesNetOfTax`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `ComprehensiveIncome` (3)
- **Labels seen**:
    - 'Adjustment for net (gains)/losses realized and included in net income' ×3

```python
    "ReclassificationOutOfAccumulatedOtherComprehensiveIncomeForMarketableSecuritiesNetOfTax": "TODO — describe this concept",
```

### `RepurchasedAndRetiredStockAveragePricePerShare`  *(suggested)*

- **Source concept**: `us-gaap:RepurchasedAndRetiredStockAveragePricePerShare`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `Note_5_MarketForRegistrantsCommonEquity` (3)
- **Labels seen**:
    - 'Average Price Paid Per Share' ×3

```python
    "RepurchasedAndRetiredStockAveragePricePerShare": "TODO — describe this concept",
```

### `RestrictedCashAndCashEquivalents`  *(suggested)*

- **Source concept**: `us-gaap:RestrictedCashAndCashEquivalents`
- **Evidence**: 3 fact(s) across 2 filing(s)
- **Statements**: `BalanceSheet` (3)
- **Labels seen**:
    - 'Restricted cash equivalents' ×2
    - 'Restricted cash' ×1

```python
    "RestrictedCashAndCashEquivalents": "TODO — describe this concept",
```

### `RestrictedStockUnitsCanceled`  *(suggested)*

- **Source concept**: `us-gaap:RestrictedStockUnitsCanceled`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `Note_11_ShareBasedCompensation` (3)
- **Labels seen**:
    - 'RSUs canceled' ×3

```python
    "RestrictedStockUnitsCanceled": "TODO — describe this concept",
```

### `RevenuesAndOtherIncome`  *(suggested)*

- **Source concept**: `us-gaap:RevenuesAndOtherIncome`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `IncomeStatement` (3)
- **Labels seen**:
    - 'Total revenues and other income' ×3

```python
    "RevenuesAndOtherIncome": "TODO — describe this concept",
```

### `ShareBasedCompensationCapitalized`  *(suggested)*

- **Source concept**: `us-gaap:ShareBasedCompensationCapitalized`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `Note_18_SupplementalCashFlowInformation` (3)
- **Labels seen**:
    - 'Stock-based compensation expense capitalized to software development costs' ×3

```python
    "ShareBasedCompensationCapitalized": "TODO — describe this concept",
```

### `ShareRepurchaseProgramAuthorizedAmount`  *(suggested)*

- **Source concept**: `us-gaap:ShareRepurchaseProgramAuthorizedAmount`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `Note_5_MarketForRegistrantsCommonEquity` (3)
- **Labels seen**:
    - 'Approximate Dollar Value of Shares That May Yet Be Purchased Under the Plans or Programs' ×3

```python
    "ShareRepurchaseProgramAuthorizedAmount": "TODO — describe this concept",
```

### `StockRepurchaseProgramByIssuerShares`  *(suggested)*

- **Source concept**: `us-gaap:StockRepurchaseProgramByIssuerShares`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `Note_5_MarketForRegistrantsCommonEquity` (3)
- **Labels seen**:
    - 'Total Number of Shares Purchased as Part of Publicly Announced Plans or Programs' ×3

```python
    "StockRepurchaseProgramByIssuerShares": "TODO — describe this concept",
```

### `TaxReceivableAgreementLiability`  *(suggested)*

- **Source concept**: `us-gaap:TaxReceivableAgreementLiability`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `Note_18_SupplementalCashFlowInformation` (3)
- **Labels seen**:
    - 'Establishment of liabilities under tax receivable agreement' ×3

```python
    "TaxReceivableAgreementLiability": "TODO — describe this concept",
```

### `UnrealizedGainLossOnSecurities`  *(suggested)*

- **Source concept**: `us-gaap:UnrealizedGainLossOnSecurities`
- **Evidence**: 3 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ManagementDiscussionAndAnalysis` (3)
- **Labels seen**:
    - 'Changes in the Market Value of Valhi Common Stock held by Subsidiaries' ×3

```python
    "UnrealizedGainLossOnSecurities": "TODO — describe this concept",
```

### `WeightedAverageInterestRate`  *(suggested)*

- **Source concept**: `us-gaap:WeightedAverageInterestRate`
- **Evidence**: 3 fact(s) across 2 filing(s)
- **Statements**: `Note_NotApplicable_InterestIncomeAndExpense` (2), `Note_7A_QuantitativeAndQualitativeDisclosuresAboutMarketRisk` (1)
- **Labels seen**:
    - 'Weighted average interest rate on debt' ×2
    - 'Total fixed-rate indebtedness' ×1

```python
    "WeightedAverageInterestRate": "TODO — describe this concept",
```

### `AccruedArbitrationExpenses`  *(suggested)*

- **Source concept**: `custom:AccruedArbitrationExpenses`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ManagementDiscussionAndAnalysis` (2)
- **Labels seen**:
    - 'Total accrued arbitration expenses were $49.7 million and $47.7 million as of December …' ×2

```python
    "AccruedArbitrationExpenses": "TODO — describe this concept",
```

### `AccruedPilotRetentionBonus`  *(suggested)*

- **Source concept**: `custom:AccruedPilotRetentionBonus`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `BalanceSheet` (2)
- **Labels seen**:
    - 'Accrued pilot retention bonus' ×2

```python
    "AccruedPilotRetentionBonus": "TODO — describe this concept",
```

### `AggregateMarketValueByNonAffiliates`  *(suggested)*

- **Source concept**: `custom:AggregateMarketValueByNonAffiliates`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `Other` (2)
- **Labels seen**:
    - 'aggregate market value of the registrant’s Class A Common Stock and Class C Common Stoc…' ×2

```python
    "AggregateMarketValueByNonAffiliates": "TODO — describe this concept",
```

### `CorporateOtherOperatingIncomeLoss`  *(suggested)*

- **Source concept**: `custom:CorporateOtherOperatingIncomeLoss`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ManagementsDiscussionAndAnalysisOfFinancialConditionAndResultsOfOperations` (2)
- **Labels seen**:
    - 'Corporate Other' ×2

```python
    "CorporateOtherOperatingIncomeLoss": "TODO — describe this concept",
```

### `CurrentLoyaltyProgramLiability`  *(suggested)*

- **Source concept**: `custom:CurrentLoyaltyProgramLiability`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `BalanceSheet` (2)
- **Labels seen**:
    - 'Current loyalty program liability' ×2

```python
    "CurrentLoyaltyProgramLiability": "TODO — describe this concept",
```

### `DeemedRepatriationTaxPayable`  *(suggested)*

- **Source concept**: `custom:DeemedRepatriationTaxPayable`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `Note_7_MDA` (1), `Note_7_ManagementDiscussionAndAnalysis` (1)
- **Labels seen**:
    - 'balance of the deemed repatriation tax payable' ×1
    - 'balance of the deemed repatriation tax payable... was $16.5 billion' ×1

```python
    "DeemedRepatriationTaxPayable": "TODO — describe this concept",
```

### `DeferredMajorMaintenanceNet`  *(suggested)*

- **Source concept**: `custom:DeferredMajorMaintenanceNet`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `BalanceSheet` (2)
- **Labels seen**:
    - 'Deferred major maintenance, net of accumulated amortization of $170,226 and $165,333' ×2

```python
    "DeferredMajorMaintenanceNet": "TODO — describe this concept",
```

### `DirectToConsumerRevenue`  *(suggested)*

- **Source concept**: `custom:DirectToConsumerRevenue`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ManagementsDiscussionAndAnalysisOfFinancialConditionAndResultsOfOperations` (2)
- **Labels seen**:
    - 'Direct-to-consumer' ×2

```python
    "DirectToConsumerRevenue": "TODO — describe this concept",
```

### `EmployeeCountBySegment`  *(suggested)*

- **Source concept**: `custom:EmployeeCountBySegment`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `Note_NotApplicable_OurPeople` (2)
- **Labels seen**:
    - 'Probe Cards Segment' ×1
    - 'Systems Segment' ×1

```python
    "EmployeeCountBySegment": "TODO — describe this concept",
```

### `EnvironmentalRemediationCosts`  *(suggested)*

- **Source concept**: `custom:EnvironmentalRemediationCosts`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ManagementDiscussionAndAnalysis` (2)
- **Labels seen**:
    - 'environmental remediation costs' ×1
    - 'costs of environmental remediation' ×1

```python
    "EnvironmentalRemediationCosts": "TODO — describe this concept",
```

### `EnvironmentalRemediationIncome`  *(suggested)*

- **Source concept**: `custom:EnvironmentalRemediationIncome`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ManagementDiscussionAndAnalysis` (2)
- **Labels seen**:
    - 'income of environmental remediation' ×1
    - 'income from environmental remediation' ×1

```python
    "EnvironmentalRemediationIncome": "TODO — describe this concept",
```

### `LsegMarketDataFees`  *(suggested)*

- **Source concept**: `custom:LsegMarketDataFees`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ManagementDiscussionAndAnalysis` (2)
- **Labels seen**:
    - 'LSEG market data fees' ×2

```python
    "LsegMarketDataFees": "TODO — describe this concept",
```

### `MaintenanceRevenueCloudAndEdge`  *(suggested)*

- **Source concept**: `custom:MaintenanceRevenueCloudAndEdge`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ResultsOfOperations` (2)
- **Labels seen**:
    - 'Maintenance' ×2

```python
    "MaintenanceRevenueCloudAndEdge": "TODO — describe this concept",
```

### `MaintenanceRevenueIPOpticalNetworks`  *(suggested)*

- **Source concept**: `custom:MaintenanceRevenueIPOpticalNetworks`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ResultsOfOperations` (2)
- **Labels seen**:
    - 'IP Optical Networks' ×2

```python
    "MaintenanceRevenueIPOpticalNetworks": "TODO — describe this concept",
```

### `MajorCustomerRevenuePercentage`  *(suggested)*

- **Source concept**: `custom:MajorCustomerRevenuePercentage`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ResultsOfOperations` (2)
- **Labels seen**:
    - 'Verizon Communications Inc.' ×2

```python
    "MajorCustomerRevenuePercentage": "TODO — describe this concept",
```

### `MiningProperties`  *(suggested)*

- **Source concept**: `custom:MiningProperties`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `BalanceSheet` (2)
- **Labels seen**:
    - 'Mining properties' ×2

```python
    "MiningProperties": "TODO — describe this concept",
```

### `NoncurrentLoyaltyProgramLiability`  *(suggested)*

- **Source concept**: `custom:NoncurrentLoyaltyProgramLiability`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `BalanceSheet` (2)
- **Labels seen**:
    - 'Noncurrent loyalty program liability' ×2

```python
    "NoncurrentLoyaltyProgramLiability": "TODO — describe this concept",
```

### `OtherRevenue`  *(suggested)*

- **Source concept**: `custom:OtherRevenue`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ManagementDiscussionAndAnalysis` (2)
- **Labels seen**:
    - 'Other' ×2

```python
    "OtherRevenue": "TODO — describe this concept",
```

### `PatientVisits`  *(suggested)*

- **Source concept**: `custom:PatientVisits`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ManagementDiscussionAndAnalysis` (2)
- **Labels seen**:
    - 'Hospital' ×2

```python
    "PatientVisits": "TODO — describe this concept",
```

### `ProfessionalServicesRevenueCloudAndEdge`  *(suggested)*

- **Source concept**: `custom:ProfessionalServicesRevenueCloudAndEdge`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ResultsOfOperations` (2)
- **Labels seen**:
    - 'Professional services' ×2

```python
    "ProfessionalServicesRevenueCloudAndEdge": "TODO — describe this concept",
```

### `ProfessionalServicesRevenueIPOpticalNetworks`  *(suggested)*

- **Source concept**: `custom:ProfessionalServicesRevenueIPOpticalNetworks`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ResultsOfOperations` (2)
- **Labels seen**:
    - 'IP Optical Networks' ×2

```python
    "ProfessionalServicesRevenueIPOpticalNetworks": "TODO — describe this concept",
```

### `SettlementLossPensionPlan`  *(suggested)*

- **Source concept**: `custom:SettlementLossPensionPlan`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ManagementDiscussionAndAnalysis` (2)
- **Labels seen**:
    - 'Settlement loss incurred in the fourth quarter of 2025 related to the termination and b…' ×1
    - 'Settlement loss related to the termination and buy-out of our U.K. pension plan in the …' ×1

```python
    "SettlementLossPensionPlan": "TODO — describe this concept",
```

### `SharesOutstanding`  *(suggested)*

- **Source concept**: `custom:SharesOutstanding`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `Other` (2)
- **Labels seen**:
    - 'Class B Convertible Common Stock' ×1
    - 'Class C Common Stock' ×1

```python
    "SharesOutstanding": "TODO — describe this concept",
```

### `SubscriptionFees`  *(suggested)*

- **Source concept**: `custom:SubscriptionFees`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ManagementDiscussionAndAnalysis` (2)
- **Labels seen**:
    - 'Subscription fees' ×2

```python
    "SubscriptionFees": "TODO — describe this concept",
```

### `TechnologyAndCommunications`  *(suggested)*

- **Source concept**: `custom:TechnologyAndCommunications`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ManagementDiscussionAndAnalysis` (2)
- **Labels seen**:
    - 'Technology and communications' ×2

```python
    "TechnologyAndCommunications": "TODO — describe this concept",
```

### `TransactionFeesAndCommissions`  *(suggested)*

- **Source concept**: `custom:TransactionFeesAndCommissions`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ManagementDiscussionAndAnalysis` (2)
- **Labels seen**:
    - 'Transaction fees and commissions' ×2

```python
    "TransactionFeesAndCommissions": "TODO — describe this concept",
```

### `UnsettledShareRepurchasesAndExciseTaxInOtherLiabilities`  *(suggested)*

- **Source concept**: `custom:UnsettledShareRepurchasesAndExciseTaxInOtherLiabilities`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `Note_18_SupplementalCashFlowInformation` (2)
- **Labels seen**:
    - 'Unsettled share repurchases and excise tax included in other liabilities' ×2

```python
    "UnsettledShareRepurchasesAndExciseTaxInOtherLiabilities": "TODO — describe this concept",
```

### `WeightedAverageYieldOnCashAndInvestments`  *(suggested)*

- **Source concept**: `custom:WeightedAverageYieldOnCashAndInvestments`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `Note_NotApplicable_InterestIncomeAndExpense` (2)
- **Labels seen**:
    - 'Weighted average yield on cash and investments' ×2

```python
    "WeightedAverageYieldOnCashAndInvestments": "TODO — describe this concept",
```

### `WellKnownSeasonedIssuer`  *(suggested)*

- **Source concept**: `custom:WellKnownSeasonedIssuer`
- **Evidence**: 2 fact(s) across 2 filing(s)
- **Statements**: `Cover` (2)
- **Labels seen**:
    - 'Indicate by check mark if the Registrant is a well-known seasoned issuer, as defined in…' ×2

```python
    "WellKnownSeasonedIssuer": "TODO — describe this concept",
```

### `WholesaleRevenue`  *(suggested)*

- **Source concept**: `custom:WholesaleRevenue`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ManagementsDiscussionAndAnalysisOfFinancialConditionAndResultsOfOperations` (2)
- **Labels seen**:
    - 'Wholesale' ×2

```python
    "WholesaleRevenue": "TODO — describe this concept",
```

### `AggregateMarketValueOfVotingAndNonvotingCommonEquityHeldByNonaffiliates`  *(suggested)*

- **Source concept**: `dei:AggregateMarketValueOfVotingAndNonvotingCommonEquityHeldByNonaffiliates`
- **Evidence**: 2 fact(s) across 2 filing(s)
- **Statements**: `Note_NotApplicable_OtherInformation` (1), `CoverPage` (1)
- **Labels seen**:
    - "Aggregate market value of registrant's common stock held by non-affiliates of the regis…" ×1
    - 'The aggregate market value of the voting and non-voting common equity held by non-affil…' ×1

```python
    "AggregateMarketValueOfVotingAndNonvotingCommonEquityHeldByNonaffiliates": "TODO — describe this concept",
```

### `EntityFileNumber`  *(suggested)*

- **Source concept**: `dei:EntityFileNumber`
- **Evidence**: 2 fact(s) across 2 filing(s)
- **Statements**: `Cover` (2)
- **Labels seen**:
    - 'Commission file number' ×1
    - 'Commission File No.' ×1

```python
    "EntityFileNumber": "TODO — describe this concept",
```

### `EntityMarketValue`  *(suggested)*

- **Source concept**: `dei:EntityMarketValue`
- **Evidence**: 2 fact(s) across 2 filing(s)
- **Statements**: `Cover` (2)
- **Labels seen**:
    - 'The aggregate market value of the voting and non-voting stock held by non-affiliates of…' ×1
    - 'The aggregate market value of the 2.4 million shares of voting common stock held by non…' ×1

```python
    "EntityMarketValue": "TODO — describe this concept",
```

### `EntityWellKnownSeasonedIssuer`  *(suggested)*

- **Source concept**: `dei:EntityWellKnownSeasonedIssuer`
- **Evidence**: 2 fact(s) across 2 filing(s)
- **Statements**: `Cover` (2)
- **Labels seen**:
    - 'Indicate by check mark if the registrant is a well-known seasoned issuer, as defined in…' ×2

```python
    "EntityWellKnownSeasonedIssuer": "TODO — describe this concept",
```

### `SecurityExchangeName`  *(suggested)*

- **Source concept**: `dei:SecurityExchangeName`
- **Evidence**: 2 fact(s) across 2 filing(s)
- **Statements**: `Cover` (2)
- **Labels seen**:
    - 'Name of each exchange on which registered' ×2

```python
    "SecurityExchangeName": "TODO — describe this concept",
```

### `TradingSymbol`  *(suggested)*

- **Source concept**: `dei:TradingSymbol`
- **Evidence**: 2 fact(s) across 2 filing(s)
- **Statements**: `Cover` (2)
- **Labels seen**:
    - 'Trading Symbol' ×1
    - 'Trading Symbol(s)' ×1

```python
    "TradingSymbol": "TODO — describe this concept",
```

### `AccountsPayableRelatedPartiesCurrent`  *(suggested)*

- **Source concept**: `us-gaap:AccountsPayableRelatedPartiesCurrent`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `BalanceSheet` (2)
- **Labels seen**:
    - 'Accounts payable - related parties' ×2

```python
    "AccountsPayableRelatedPartiesCurrent": "TODO — describe this concept",
```

### `AccruedDividendsOnPreferredStock`  *(suggested)*

- **Source concept**: `us-gaap:AccruedDividendsOnPreferredStock`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (2)
- **Labels seen**:
    - 'Dividends accrued on preferred stock liability' ×2

```python
    "AccruedDividendsOnPreferredStock": "TODO — describe this concept",
```

### `AdjustmentToAdditionalPaidInCapitalForTransactionsBetweenParentAndNoncontrollingInterest`  *(suggested)*

- **Source concept**: `us-gaap:AdjustmentToAdditionalPaidInCapitalForTransactionsBetweenParentAndNoncontrollingInterest`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `ShareholdersEquity` (2)
- **Labels seen**:
    - 'Equity transactions with noncontrolling interest and other, net' ×2

```python
    "AdjustmentToAdditionalPaidInCapitalForTransactionsBetweenParentAndNoncontrollingInterest": "TODO — describe this concept",
```

### `AllowanceForCreditLosses`  *(suggested)*

- **Source concept**: `us-gaap:AllowanceForCreditLosses`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `BalanceSheet` (2)
- **Labels seen**:
    - 'Allowance for credit losses on loans' ×2

```python
    "AllowanceForCreditLosses": "TODO — describe this concept",
```

### `AmortizationOfAccumulatedGainLossFromCashFlowHedge`  *(suggested)*

- **Source concept**: `us-gaap:AmortizationOfAccumulatedGainLossFromCashFlowHedge`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (2)
- **Labels seen**:
    - 'Amortization of accumulated other comprehensive gain related to interest rate swap' ×2

```python
    "AmortizationOfAccumulatedGainLossFromCashFlowHedge": "TODO — describe this concept",
```

### `AvailableForSaleSecurities`  *(suggested)*

- **Source concept**: `us-gaap:AvailableForSaleSecurities`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `BalanceSheet` (2)
- **Labels seen**:
    - 'Investment securities available-for-sale' ×2

```python
    "AvailableForSaleSecurities": "TODO — describe this concept",
```

### `BuildingsAndImprovementsGross`  *(suggested)*

- **Source concept**: `us-gaap:BuildingsAndImprovementsGross`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `BalanceSheet` (2)
- **Labels seen**:
    - 'Buildings' ×2

```python
    "BuildingsAndImprovementsGross": "TODO — describe this concept",
```

### `CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsAndMarketableSecurities`  *(suggested)*

- **Source concept**: `us-gaap:CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsAndMarketableSecurities`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ManagementDiscussionAndAnalysis` (2)
- **Labels seen**:
    - 'Total cash and cash equivalents, restricted cash and marketable securities' ×2

```python
    "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsAndMarketableSecurities": "TODO — describe this concept",
```

### `CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsPeriodIncreaseDecrease`  *(suggested)*

- **Source concept**: `us-gaap:CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsPeriodIncreaseDecrease`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `Note_NotApplicable_InterestIncomeAndExpense` (2)
- **Labels seen**:
    - 'Weighted average balance of cash and investments' ×2

```python
    "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsPeriodIncreaseDecrease": "TODO — describe this concept",
```

### `ConstructionInProgress`  *(suggested)*

- **Source concept**: `us-gaap:ConstructionInProgress`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `BalanceSheet` (2)
- **Labels seen**:
    - 'Construction in progress' ×2

```python
    "ConstructionInProgress": "TODO — describe this concept",
```

### `CustomerRefundsPayable`  *(suggested)*

- **Source concept**: `us-gaap:CustomerRefundsPayable`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `BalanceSheet` (2)
- **Labels seen**:
    - 'Customer refund liabilities (Note 12)' ×2

```python
    "CustomerRefundsPayable": "TODO — describe this concept",
```

### `DebtInstrumentInterestRateStatedPercentage`  *(suggested)*

- **Source concept**: `us-gaap:DebtInstrumentInterestRateStatedPercentage`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `Note_7A_QuantitativeAndQualitativeDisclosuresAboutMarketRisk` (2)
- **Labels seen**:
    - 'Kronos fixed-rate 9.50% Senior Secured Notes due 2029' ×1
    - 'LandWell bank note payable' ×1

```python
    "DebtInstrumentInterestRateStatedPercentage": "TODO — describe this concept",
```

### `DebtInstrumentUnamortizedPremium`  *(suggested)*

- **Source concept**: `us-gaap:DebtInstrumentUnamortizedPremium`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (2)
- **Labels seen**:
    - 'Premium on issuance of senior secured notes' ×2

```python
    "DebtInstrumentUnamortizedPremium": "TODO — describe this concept",
```

### `DeferredIncomeTaxes`  *(suggested)*

- **Source concept**: `us-gaap:DeferredIncomeTaxes`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `BalanceSheet` (2)
- **Labels seen**:
    - 'Deferred income taxes (Note 18)' ×2

```python
    "DeferredIncomeTaxes": "TODO — describe this concept",
```

### `DeferredRevenue`  *(suggested)*

- **Source concept**: `us-gaap:DeferredRevenue`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `Note_2_Revenue` (2)
- **Labels seen**:
    - 'total deferred revenue' ×2

```python
    "DeferredRevenue": "TODO — describe this concept",
```

### `DeferredTaxLiabilities`  *(suggested)*

- **Source concept**: `us-gaap:DeferredTaxLiabilities`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `BalanceSheet` (2)
- **Labels seen**:
    - 'Deferred income taxes' ×2

```python
    "DeferredTaxLiabilities": "TODO — describe this concept",
```

### `Deposits`  *(suggested)*

- **Source concept**: `us-gaap:Deposits`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `BalanceSheet` (2)
- **Labels seen**:
    - 'Total deposits' ×2

```python
    "Deposits": "TODO — describe this concept",
```

### `DistributionsFromInvestees`  *(suggested)*

- **Source concept**: `us-gaap:DistributionsFromInvestees`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (2)
- **Labels seen**:
    - 'Distributions from (contributions to) TiO2 manufacturing joint venture, net' ×2

```python
    "DistributionsFromInvestees": "TODO — describe this concept",
```

### `DividendIncome`  *(suggested)*

- **Source concept**: `us-gaap:DividendIncome`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `IncomeStatement` (2)
- **Labels seen**:
    - 'Dividends' ×2

```python
    "DividendIncome": "TODO — describe this concept",
```

### `Dividends`  *(suggested)*

- **Source concept**: `us-gaap:Dividends`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `ShareholdersEquity` (2)
- **Labels seen**:
    - 'Cash dividends, $1.20 per share' ×2

```python
    "Dividends": "TODO — describe this concept",
```

### `FairValueAdjustmentOfPreferredStockLiability`  *(suggested)*

- **Source concept**: `us-gaap:FairValueAdjustmentOfPreferredStockLiability`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (2)
- **Labels seen**:
    - 'Change in fair value of preferred stock liability' ×2

```python
    "FairValueAdjustmentOfPreferredStockLiability": "TODO — describe this concept",
```

### `FederalHomeLoanBankAdvances`  *(suggested)*

- **Source concept**: `us-gaap:FederalHomeLoanBankAdvances`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `BalanceSheet` (2)
- **Labels seen**:
    - 'Borrowed funds' ×2

```python
    "FederalHomeLoanBankAdvances": "TODO — describe this concept",
```

### `GainLossOnSaleOfAssets`  *(suggested)*

- **Source concept**: `us-gaap:GainLossOnSaleOfAssets`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (2)
- **Labels seen**:
    - 'Gain from sale of land' ×2

```python
    "GainLossOnSaleOfAssets": "TODO — describe this concept",
```

### `GainLossOnSaleOfLoans`  *(suggested)*

- **Source concept**: `us-gaap:GainLossOnSaleOfLoans`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `IncomeStatement` (2)
- **Labels seen**:
    - 'Net gains on sales of loans held for sale' ×2

```python
    "GainLossOnSaleOfLoans": "TODO — describe this concept",
```

### `GainsLossesOnSalesOfAvailableForSaleSecurities`  *(suggested)*

- **Source concept**: `us-gaap:GainsLossesOnSalesOfAvailableForSaleSecurities`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `IncomeStatement` (2)
- **Labels seen**:
    - 'Net losses on sales of investment securities available-for-sale' ×2

```python
    "GainsLossesOnSalesOfAvailableForSaleSecurities": "TODO — describe this concept",
```

### `IncomeLossFromContinuingOperationsBeforeIncomeTaxesDomestic`  *(suggested)*

- **Source concept**: `us-gaap:IncomeLossFromContinuingOperationsBeforeIncomeTaxesDomestic`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `IncomeStatement` (2)
- **Labels seen**:
    - 'Income before provision for income taxes' ×2

```python
    "IncomeLossFromContinuingOperationsBeforeIncomeTaxesDomestic": "TODO — describe this concept",
```

### `IncreaseDecreaseInIncomeTaxesPayable`  *(suggested)*

- **Source concept**: `us-gaap:IncreaseDecreaseInIncomeTaxesPayable`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (2)
- **Labels seen**:
    - 'Increase/(Decrease) in Accrued income tax expense' ×2

```python
    "IncreaseDecreaseInIncomeTaxesPayable": "TODO — describe this concept",
```

### `IncreaseDecreaseInOperatingCapital`  *(suggested)*

- **Source concept**: `us-gaap:IncreaseDecreaseInOperatingCapital`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `Note_8_CashFlow` (2)
- **Labels seen**:
    - 'Changes in operating assets and liabilities' ×2

```python
    "IncreaseDecreaseInOperatingCapital": "TODO — describe this concept",
```

### `InterestAndDividendIncome`  *(suggested)*

- **Source concept**: `us-gaap:InterestAndDividendIncome`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `IncomeStatement` (2)
- **Labels seen**:
    - 'Total interest and dividend income' ×2

```python
    "InterestAndDividendIncome": "TODO — describe this concept",
```

### `InterestAndFeeIncomeLoans`  *(suggested)*

- **Source concept**: `us-gaap:InterestAndFeeIncomeLoans`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `IncomeStatement` (2)
- **Labels seen**:
    - 'Interest and fees on loans' ×2

```python
    "InterestAndFeeIncomeLoans": "TODO — describe this concept",
```

### `InterestBearingDeposits`  *(suggested)*

- **Source concept**: `us-gaap:InterestBearingDeposits`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `BalanceSheet` (2)
- **Labels seen**:
    - 'Interest bearing' ×2

```python
    "InterestBearingDeposits": "TODO — describe this concept",
```

### `InterestBearingDepositsInOtherFinancialInstitutions`  *(suggested)*

- **Source concept**: `us-gaap:InterestBearingDepositsInOtherFinancialInstitutions`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `BalanceSheet` (2)
- **Labels seen**:
    - 'Interest bearing deposits in banks' ×2

```python
    "InterestBearingDepositsInOtherFinancialInstitutions": "TODO — describe this concept",
```

### `InterestExpenseDeposits`  *(suggested)*

- **Source concept**: `us-gaap:InterestExpenseDeposits`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `IncomeStatement` (2)
- **Labels seen**:
    - 'Interest on deposits' ×2

```python
    "InterestExpenseDeposits": "TODO — describe this concept",
```

### `InterestExpenseSubordinatedDebt`  *(suggested)*

- **Source concept**: `us-gaap:InterestExpenseSubordinatedDebt`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `IncomeStatement` (2)
- **Labels seen**:
    - 'Interest on subordinated notes' ×2

```python
    "InterestExpenseSubordinatedDebt": "TODO — describe this concept",
```

### `InterestIncomeDebtSecuritiesTaxExempt`  *(suggested)*

- **Source concept**: `us-gaap:InterestIncomeDebtSecuritiesTaxExempt`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `IncomeStatement` (2)
- **Labels seen**:
    - 'Tax exempt' ×2

```python
    "InterestIncomeDebtSecuritiesTaxExempt": "TODO — describe this concept",
```

### `InterestIncomeDebtSecuritiesTaxable`  *(suggested)*

- **Source concept**: `us-gaap:InterestIncomeDebtSecuritiesTaxable`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `IncomeStatement` (2)
- **Labels seen**:
    - 'Taxable' ×2

```python
    "InterestIncomeDebtSecuritiesTaxable": "TODO — describe this concept",
```

### `InterestIncomeDeposits`  *(suggested)*

- **Source concept**: `us-gaap:InterestIncomeDeposits`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `IncomeStatement` (2)
- **Labels seen**:
    - 'Interest on interest bearing deposits in banks' ×2

```python
    "InterestIncomeDeposits": "TODO — describe this concept",
```

### `InterestIncomeFederalFundsSoldAndSecuritiesPurchasedUnderAgreementsToResell`  *(suggested)*

- **Source concept**: `us-gaap:InterestIncomeFederalFundsSoldAndSecuritiesPurchasedUnderAgreementsToResell`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `IncomeStatement` (2)
- **Labels seen**:
    - 'Interest on federal funds sold and overnight deposits' ×2

```python
    "InterestIncomeFederalFundsSoldAndSecuritiesPurchasedUnderAgreementsToResell": "TODO — describe this concept",
```

### `InterestIncomeOperating`  *(suggested)*

- **Source concept**: `us-gaap:InterestIncomeOperating`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ManagementDiscussionAndAnalysis` (2)
- **Labels seen**:
    - 'Interest Income and Other' ×2

```python
    "InterestIncomeOperating": "TODO — describe this concept",
```

### `InterestRateFairValueDisclosure`  *(suggested)*

- **Source concept**: `us-gaap:InterestRateFairValueDisclosure`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `Note_7A_QuantitativeAndQualitativeDisclosuresAboutMarketRisk` (2)
- **Labels seen**:
    - 'affected the fair value of our investment portfolio' ×2

```python
    "InterestRateFairValueDisclosure": "TODO — describe this concept",
```

### `Investments`  *(suggested)*

- **Source concept**: `us-gaap:Investments`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `BalanceSheet` (2)
- **Labels seen**:
    - 'Total investments' ×2

```python
    "Investments": "TODO — describe this concept",
```

### `LicenseRevenue`  *(suggested)*

- **Source concept**: `us-gaap:LicenseRevenue`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ManagementsDiscussionAndAnalysisOfFinancialConditionAndResultsOfOperations` (2)
- **Labels seen**:
    - 'License revenues' ×2

```python
    "LicenseRevenue": "TODO — describe this concept",
```

### `LoansAndLeasesReceivable`  *(suggested)*

- **Source concept**: `us-gaap:LoansAndLeasesReceivable`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `BalanceSheet` (2)
- **Labels seen**:
    - 'Loans' ×2

```python
    "LoansAndLeasesReceivable": "TODO — describe this concept",
```

### `LoansAndLeasesReceivableHeldForSale`  *(suggested)*

- **Source concept**: `us-gaap:LoansAndLeasesReceivableHeldForSale`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `BalanceSheet` (2)
- **Labels seen**:
    - 'Loans held for sale' ×2

```python
    "LoansAndLeasesReceivableHeldForSale": "TODO — describe this concept",
```

### `LongTermDebtInterestExpenseChangeInInterestRate100BasisPointIncrease`  *(suggested)*

- **Source concept**: `us-gaap:LongTermDebtInterestExpenseChangeInInterestRate100BasisPointIncrease`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `Note_7A_QuantitativeAndQualitativeDisclosuresAboutMarketRisk` (2)
- **Labels seen**:
    - 'Increase in annual interest expense' ×2

```python
    "LongTermDebtInterestExpenseChangeInInterestRate100BasisPointIncrease": "TODO — describe this concept",
```

### `MachineryAndEquipmentGross`  *(suggested)*

- **Source concept**: `us-gaap:MachineryAndEquipmentGross`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `BalanceSheet` (2)
- **Labels seen**:
    - 'Equipment' ×2

```python
    "MachineryAndEquipmentGross": "TODO — describe this concept",
```

### `MarketableSecuritiesFairValueChangeInInterestRate100BasisPointIncrease`  *(suggested)*

- **Source concept**: `us-gaap:MarketableSecuritiesFairValueChangeInInterestRate100BasisPointIncrease`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `Note_7A_QuantitativeAndQualitativeDisclosuresAboutMarketRisk` (2)
- **Labels seen**:
    - 'Decline in fair value' ×2

```python
    "MarketableSecuritiesFairValueChangeInInterestRate100BasisPointIncrease": "TODO — describe this concept",
```

### `NetInterestIncome`  *(suggested)*

- **Source concept**: `us-gaap:NetInterestIncome`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `IncomeStatement` (2)
- **Labels seen**:
    - 'Net interest income' ×2

```python
    "NetInterestIncome": "TODO — describe this concept",
```

### `NetInterestIncomeAfterProvisionForLoanLeaseAndOtherCreditLosses`  *(suggested)*

- **Source concept**: `us-gaap:NetInterestIncomeAfterProvisionForLoanLeaseAndOtherCreditLosses`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `IncomeStatement` (2)
- **Labels seen**:
    - 'Net interest income after credit loss expense' ×2

```python
    "NetInterestIncomeAfterProvisionForLoanLeaseAndOtherCreditLosses": "TODO — describe this concept",
```

### `NetLoansAndLeasesReceivable`  *(suggested)*

- **Source concept**: `us-gaap:NetLoansAndLeasesReceivable`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `BalanceSheet` (2)
- **Labels seen**:
    - 'Net loans' ×2

```python
    "NetLoansAndLeasesReceivable": "TODO — describe this concept",
```

### `NoninterestBearingDeposits`  *(suggested)*

- **Source concept**: `us-gaap:NoninterestBearingDeposits`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `BalanceSheet` (2)
- **Labels seen**:
    - 'Noninterest bearing' ×2

```python
    "NoninterestBearingDeposits": "TODO — describe this concept",
```

### `OtherAssets`  *(suggested)*

- **Source concept**: `us-gaap:OtherAssets`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `BalanceSheet` (2)
- **Labels seen**:
    - 'Other assets' ×2

```python
    "OtherAssets": "TODO — describe this concept",
```

### `OtherComprehensiveIncomeLossReclassificationAdjustmentForNetLossesOnSecuritiesNetOfTax`  *(suggested)*

- **Source concept**: `us-gaap:OtherComprehensiveIncomeLossReclassificationAdjustmentForNetLossesOnSecuritiesNetOfTax`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `ComprehensiveIncome` (2)
- **Labels seen**:
    - 'Reclassification adjustment for net losses on investment securities available-for-sale …' ×2

```python
    "OtherComprehensiveIncomeLossReclassificationAdjustmentForNetLossesOnSecuritiesNetOfTax": "TODO — describe this concept",
```

### `OtherInvestments`  *(suggested)*

- **Source concept**: `us-gaap:OtherInvestments`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `BalanceSheet` (2)
- **Labels seen**:
    - 'Other investments' ×2

```python
    "OtherInvestments": "TODO — describe this concept",
```

### `PreferredStockValue`  *(suggested)*

- **Source concept**: `us-gaap:PreferredStockValue`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `BalanceSheet` (2)
- **Labels seen**:
    - 'Preferred stock, $0.001 par value:' ×2

```python
    "PreferredStockValue": "TODO — describe this concept",
```

### `ProceedsFromRevolvingCreditFacilities`  *(suggested)*

- **Source concept**: `us-gaap:ProceedsFromRevolvingCreditFacilities`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (2)
- **Labels seen**:
    - 'Borrowings under revolving line of credit' ×2

```python
    "ProceedsFromRevolvingCreditFacilities": "TODO — describe this concept",
```

### `ProvisionForLoanLeaseAndOtherCreditLosses`  *(suggested)*

- **Source concept**: `us-gaap:ProvisionForLoanLeaseAndOtherCreditLosses`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `IncomeStatement` (2)
- **Labels seen**:
    - 'Credit loss expense, net' ×2

```python
    "ProvisionForLoanLeaseAndOtherCreditLosses": "TODO — describe this concept",
```

### `ReceivablesFromRelatedPartiesCurrent`  *(suggested)*

- **Source concept**: `us-gaap:ReceivablesFromRelatedPartiesCurrent`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `BalanceSheet` (2)
- **Labels seen**:
    - 'Accounts receivable - related parties' ×2

```python
    "ReceivablesFromRelatedPartiesCurrent": "TODO — describe this concept",
```

### `ReconciliationOfNetIncomeLossToNetCashProvidedByUsedInOperatingActivities`  *(suggested)*

- **Source concept**: `us-gaap:ReconciliationOfNetIncomeLossToNetCashProvidedByUsedInOperatingActivities`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `Note_8_CashFlow` (2)
- **Labels seen**:
    - 'Adjustments to reconcile net income (loss) to cash flows provided by operating activities' ×2

```python
    "ReconciliationOfNetIncomeLossToNetCashProvidedByUsedInOperatingActivities": "TODO — describe this concept",
```

### `RepaymentsOfRevolvingCreditFacilities`  *(suggested)*

- **Source concept**: `us-gaap:RepaymentsOfRevolvingCreditFacilities`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `CashFlow` (2)
- **Labels seen**:
    - 'Principal payments on revolving line of credit' ×2

```python
    "RepaymentsOfRevolvingCreditFacilities": "TODO — describe this concept",
```

### `RestrictedCashAndCashEquivalentsAtCarryingValue`  *(suggested)*

- **Source concept**: `us-gaap:RestrictedCashAndCashEquivalentsAtCarryingValue`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `BalanceSheet` (2)
- **Labels seen**:
    - 'Restricted cash' ×2

```python
    "RestrictedCashAndCashEquivalentsAtCarryingValue": "TODO — describe this concept",
```

### `ServiceChargesOnDepositAccounts`  *(suggested)*

- **Source concept**: `us-gaap:ServiceChargesOnDepositAccounts`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `IncomeStatement` (2)
- **Labels seen**:
    - 'Service fees' ×2

```python
    "ServiceChargesOnDepositAccounts": "TODO — describe this concept",
```

### `ShareRepurchaseProgramRemainingAuthorizedAmount`  *(suggested)*

- **Source concept**: `us-gaap:ShareRepurchaseProgramRemainingAuthorizedAmount`
- **Evidence**: 2 fact(s) across 2 filing(s)
- **Statements**: `Note_13_StockholdersEquity` (1), `Note_5_MarketForRegistrantsCommonEquity` (1)
- **Labels seen**:
    - 'remained available for future repurchases' ×1
    - 'Approximate Dollar Value of Shares That May Yet Be Purchased Under the Plans or Programs' ×1

```python
    "ShareRepurchaseProgramRemainingAuthorizedAmount": "TODO — describe this concept",
```

### `TaxReceivableAgreementLiabilityAdjustment`  *(suggested)*

- **Source concept**: `us-gaap:TaxReceivableAgreementLiabilityAdjustment`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `Note_7_ManagementDiscussionAndAnalysis` (2)
- **Labels seen**:
    - 'Tax receivable agreement liability adjustment' ×2

```python
    "TaxReceivableAgreementLiabilityAdjustment": "TODO — describe this concept",
```

### `TechnologyAndCommunication`  *(suggested)*

- **Source concept**: `us-gaap:TechnologyAndCommunication`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `IncomeStatement` (2)
- **Labels seen**:
    - 'Equipment expense' ×2

```python
    "TechnologyAndCommunication": "TODO — describe this concept",
```

### `TreasuryStockShares`  *(suggested)*

- **Source concept**: `us-gaap:TreasuryStockShares`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `BalanceSheet` (2)
- **Labels seen**:
    - '471,430 shares at December 31, 2025' ×1
    - '474,075 shares at December 31, 2024' ×1

```python
    "TreasuryStockShares": "TODO — describe this concept",
```

### `TrustAndInvestmentManagementIncome`  *(suggested)*

- **Source concept**: `us-gaap:TrustAndInvestmentManagementIncome`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `IncomeStatement` (2)
- **Labels seen**:
    - 'Wealth management income' ×2

```python
    "TrustAndInvestmentManagementIncome": "TODO — describe this concept",
```

### `Warrants`  *(suggested)*

- **Source concept**: `us-gaap:Warrants`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `BalanceSheet` (2)
- **Labels seen**:
    - 'Warrant liability' ×2

```python
    "Warrants": "TODO — describe this concept",
```

### `WorkingCapital`  *(suggested)*

- **Source concept**: `us-gaap:WorkingCapital`
- **Evidence**: 2 fact(s) across 1 filing(s)
- **Statements**: `Note_NotApplicable_LiquidityAndCapitalResources` (2)
- **Labels seen**:
    - 'working capital' ×2

```python
    "WorkingCapital": "TODO — describe this concept",
```

## 2. Mapping inconsistencies

The same `concept` was mapped to more than one canonical name. Some of these are legitimate (e.g. the same XBRL tag legitimately covers two different canonicals at beginning vs end of period) — others reveal LLM indecision worth investigating.

| Concept | Canonicals (count) | Total facts |
|---|---|---|
| `us-gaap:SalesRevenueNet` | `Revenue` (33), `SegmentRevenue` (15) | 48 |
| `us-gaap:ShareBasedCompensation` | `ShareBasedCompensationExpense` (42), `ShareBasedCompensationCF` (3) | 45 |
| `us-gaap:ProductSales` | `RevenueProducts` (15), `GeographicRevenue` (8) | 23 |
| `custom:VariableRevenue` | `SegmentRevenue` (12), `Revenue` (2) | 14 |
| `custom:FixedRevenue` | `SegmentRevenue` (12), `Revenue` (2) | 14 |
| `us-gaap:Revenue` | `GeographicRevenue` (8), `SegmentRevenue` (4) | 12 |
| `us-gaap:CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents` | `CashEndOfPeriod` (6), `CashBeginningOfPeriod` (3) | 9 |
| `us-gaap:CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsPeriodIncreaseDecrease` | `NetChangeInCash` (6), `CashBeginningOfPeriod` (3) | 9 |

## 3. Likely hallucinated XBRL tags

Concepts where `concept_valid` is `false` — i.e. the namespace is tracked (`us-gaap`, `ifrs-full`, `dei`) but the tag is NOT in the authoritative list at `data/taxonomies/`. These are LLM inventions. Either the tag really doesn't exist (and the LLM should have used `custom:*`), or it's a real tag that's missing from our seed-filer union — extend `scripts/fetch_taxonomies.py` and re-run if so.

| Hallucinated concept | Count |
|---|---|
| `us-gaap:RevenueFromContractWithCustomerByGeographicRegion` | 54 |
| `us-gaap:GrossMargin` | 26 |
| `us-gaap:ProductSales` | 23 |
| `us-gaap:ContractualObligations` | 23 |
| `us-gaap:IncreaseDecreaseInCommonStock` | 16 |
| `us-gaap:IncomeLossFromContinuingOperationsBeforeIncomeTaxExpenseBenefit` | 15 |
| `us-gaap:ServiceRevenue` | 14 |
| `us-gaap:MaintenanceAndSupportRevenue` | 14 |
| `us-gaap:ProfessionalServicesRevenue` | 14 |
| `us-gaap:CostOfProducts` | 14 |
| `us-gaap:SegmentRevenue` | 14 |
| `us-gaap:Revenue` | 12 |
| `us-gaap:NetIncomeLossAttributableToParent` | 12 |
| `us-gaap:RepurchasedShares` | 12 |
| `us-gaap:CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsPeriodIncreaseDecrease` | 11 |
| `us-gaap:RepurchasedAndRetiredStockShares` | 10 |
| `us-gaap:OtherInvestingActivities` | 9 |
| `us-gaap:OtherFinancingActivities` | 9 |
| `us-gaap:CashCashEquivalentsAndRestrictedCash` | 9 |
| `us-gaap:GrossProfitMargin` | 9 |
| `dei:EntityFilerCategory` | 8 |
| `us-gaap:ShareRepurchaseProgramAuthorizedAmount` | 8 |
| `dei:SecurityPriceHigh` | 8 |
| `dei:SecurityPriceLow` | 8 |
| `us-gaap:SegmentReportingProfitLoss` | 8 |
| `us-gaap:CommonStockAndAdditionalPaidInCapital` | 8 |
| `us-gaap:UnconditionalPurchaseObligations` | 7 |
| `us-gaap:ProceedsFromSaleOfBusiness` | 7 |
| `us-gaap:IncreaseDecreaseInAdditionalPaidInCapital` | 7 |
| `us-gaap:DeferredTaxAssets` | 7 |

