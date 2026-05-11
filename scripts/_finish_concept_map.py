"""One-off completion script for the concept map.

The Gemini-driven main run (scripts/build_concept_map.py) couldn't close the
last ~222 tags due to its empty-response glitch. Rather than set up a second
LLM provider just to finish a small tail, these mappings were composed
directly by Claude (Opus 4.7) reading the unmapped tags against
src/pdf_extraction/taxonomy.py.

Run-and-discard — once merged, this file isn't needed again. The remaining
mappings get written into data/taxonomies/concept_canonical_map.json and the
markdown is regenerated.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from build_concept_map import write_markdown  # noqa: E402

TAX_DIR = ROOT / "data" / "taxonomies"

# (canonical, note). canonical=None means no clean canonical fit.
# Notes are short (5-20 words) for human spot-check.

US_GAAP: dict[str, tuple[str | None, str]] = {
    # AvailableForSaleSecurities — gain/loss disclosure detail, no canonical
    "AvailableForSaleSecuritiesGrossRealizedLosses": (None, "AFS gain/loss detail, too granular for the canonical set"),
    "AvailableForSaleSecuritiesGrossUnrealizedGains": (None, "AFS unrealized gain disclosure detail"),
    "AvailableForSaleSecuritiesGrossUnrealizedLoss": (None, "AFS unrealized loss disclosure detail"),
    "AvailableForSaleSecuritiesGrossUnrealizedLosses1": (None, "AFS unrealized loss disclosure detail (alternate form)"),
    "AvailableForSaleSecuritiesNoncurrent": ("LongTermInvestments", "Non-current AFS securities are long-term investments"),
    "AvailableforsaleSecuritiesContinuousUnrealizedLossPosition12MonthsOrLongerAggregateLosses1": (None, "Continuous-loss-position aging disclosure"),
    "AvailableforsaleSecuritiesContinuousUnrealizedLossPosition12MonthsOrLongerAggregateLosses2": (None, "Continuous-loss-position aging disclosure"),
    "AvailableforsaleSecuritiesContinuousUnrealizedLossPositionAggregateLosses1": (None, "Continuous-loss-position aggregate disclosure"),
    "AvailableforsaleSecuritiesContinuousUnrealizedLossPositionAggregateLosses2": (None, "Continuous-loss-position aggregate disclosure"),
    "AvailableforsaleSecuritiesContinuousUnrealizedLossPositionLessThan12MonthsAggregateLosses1": (None, "Continuous-loss-position aging disclosure"),
    "AvailableforsaleSecuritiesContinuousUnrealizedLossPositionLessThan12MonthsAggregateLosses2": (None, "Continuous-loss-position aging disclosure"),
    "AvailableforsaleSecuritiesGrossRealizedGainLossExcludingOtherThanTemporaryImpairments": (None, "AFS gain/loss excluding OTTI — disclosure detail"),
    "AvailableforsaleSecuritiesGrossRealizedLossesExcludingOtherThanTemporaryImpairments": (None, "AFS realized loss excluding OTTI — disclosure detail"),
    "AvailableforsaleSecuritiesGrossUnrealizedGain": (None, "AFS unrealized gain disclosure detail"),

    # Banking / sector-specific
    "BankingRegulationCountercyclicalCapitalBuffer": (None, "Bank capital buffer — sector-specific, no canonical"),
    "BankingRegulationGlobalSystemicallyImportantBankGsibSurcharge": (None, "G-SIB surcharge — bank-specific"),
    "CommonEquityTierOneCapital": (None, "Tier 1 capital — bank regulatory, no canonical"),

    # Securitization detail
    "CashFlowsBetweenSecuritizationSpecialPurposeEntitySPEAndTransferorOtherCashFlowsReceivedOnRetainedInterests": (None, "Securitization SPE cash flow disclosure"),
    "CashFlowsBetweenSecuritizationSpecialPurposeEntitySPEAndTransferorPurchasesOfDelinquentOrForeclosedAssets": (None, "Securitization SPE disclosure detail"),
    "CashFlowsBetweenSecuritizationSpecialPurposeEntitySPEAndTransferorServicingFeesReceived": (None, "Securitization servicing fee disclosure"),
    "CashFlowsBetweenTransferorAndTransfereeBeneficialInterest": (None, "Securitization transfer disclosure"),

    # Discontinued operations split
    "CashProvidedByUsedInFinancingActivitiesDiscontinuedOperations": (None, "Discontinued ops only — no separate canonical from continuing"),
    "CashProvidedByUsedInInvestingActivitiesDiscontinuedOperations": (None, "Discontinued ops only — no separate canonical"),
    "CashProvidedByUsedInOperatingActivitiesDiscontinuedOperations": (None, "Discontinued ops only — no separate canonical"),

    # Reserves / regulatory deposits
    "CashReserveDepositRequiredAndMade": (None, "Regulatory reserve deposit — sector-specific"),
    "CashSurrenderValueOfLifeInsurance": ("OtherNonCurrentAssets", "Cash-value life insurance is a non-current other asset"),

    # Insurance ceded premiums
    "CededPremiumsEarnedPropertyAndCasualty": (None, "Insurance P&C ceded premium — sector-specific"),
    "CededPremiumsWritten": (None, "Insurance ceded premium — sector-specific"),
    "CededPremiumsWrittenPropertyAndCasualty": (None, "Insurance P&C ceded premium — sector-specific"),

    # Acquired loans accounting (banking)
    "CertainLoansAcquiredInTransferNotAccountedForAsDebtSecuritiesAccretableYield": (None, "Acquired-loan disclosure (bank)"),
    "CertainLoansAcquiredInTransferNotAccountedForAsDebtSecuritiesAccretableYieldAccretion": (None, "Acquired-loan accretion (bank)"),
    "CertainLoansAcquiredInTransferNotAccountedForAsDebtSecuritiesAccretableYieldReclassificationsToNonaccretableDifference": (None, "Acquired-loan reclassification (bank)"),
    "CertainLoansAcquiredInTransferNotAccountedForAsDebtSecuritiesAllowanceForLoanLosses": (None, "Acquired-loan allowance (bank)"),
    "CertainLoansAcquiredInTransferNotAccountedForAsDebtSecuritiesCarryingAmountNet": (None, "Acquired-loan carrying amount (bank)"),
    "CertainLoansAcquiredInTransferNotAccountedForAsDebtSecuritiesConsumerOutstandingBalance": (None, "Acquired-loan consumer balance (bank)"),
    "CertainLoansAcquiredInTransferNotAccountedForAsDebtSecuritiesOutstandingBalance": (None, "Acquired-loan outstanding balance (bank)"),
    "CertainLoansAndDebtSecuritiesAcquiredInTransferAllowanceForCreditLossesDueToSubsequentImpairment": (None, "Acquired-loan impairment allowance (bank)"),

    # Hedge accounting details
    "ChangeInUnrealizedGainLossOnFairValueHedgingInstruments": (None, "Hedge accounting disclosure detail"),
    "ChangeInUnrealizedGainLossOnFairValueHedgingInstruments1": (None, "Hedge accounting disclosure detail"),
    "ChangeInUnrealizedGainLossOnHedgedItemInFairValueHedge": (None, "Hedge accounting disclosure detail"),
    "ChangeInUnrealizedGainLossOnHedgedItemInFairValueHedge1": (None, "Hedge accounting disclosure detail"),

    # Warrants
    "ClassOfWarrantOrRightExercisePriceOfWarrantsOrRights": (None, "Warrant strike price disclosure"),
    "ClassOfWarrantOrRightExercisePriceOfWarrantsOrRights1": (None, "Warrant strike price disclosure"),

    # Commitments
    "CommitmentsFairValueDisclosure": (None, "Commitment fair-value disclosure, too granular"),

    # Common-stock detail
    "CommonStockCapitalSharesReservedForFutureIssuance": (None, "Shares reserved disclosure — granular"),
    "CommonStockDividendsPerShareCashPaid": ("DividendsPerShareDeclared", "Cash dividends per share — closest match (declared vs paid usually equal)"),
    "CommonStockDividendsPerShareDeclared": ("DividendsPerShareDeclared", "Direct match for dividends declared per share"),
    "CommonStockHeldInTrust": (None, "Common stock in employee/grantor trust — granular"),
    "CommonStockIncludingAdditionalPaidInCapital": ("CommonStockAndAPIC", "Combined common stock + APIC line"),
    "CommonStockIssuedEmployeeTrustDeferred": (None, "Employee trust deferred shares — granular"),
    "CommonStockNoParValue": (None, "Marker that stock has no par value — disclosure"),
    "CommonStockParOrStatedValuePerShare": ("CommonStockParValue", "Direct match for par/stated value per share"),
    "CommonStockSharesAuthorized": ("CommonSharesAuthorized", "Direct match for authorized common shares"),
    "CommonStockSharesHeldInEmployeeTrustShares": (None, "Employee trust share count — granular"),
    "CommonStockSharesIssued": ("CommonSharesIssued", "Direct match for issued common shares"),
    "CommonStockSharesOutstanding": ("CommonSharesOutstanding", "Direct match for outstanding common shares"),
    "CommonStockValue": ("CommonStockAndAPIC", "Common stock at par/stated value — fits the combined CS+APIC canonical"),

    # Equity-method investments
    "EquityMethodInvestmentDividendsOrDistributions": (None, "Equity-method dividend received — disclosure"),
    "EquityMethodInvestmentOtherThanTemporaryImpairment": (None, "Equity-method OTTI — disclosure"),
    "EquityMethodInvestmentOwnershipPercentage": (None, "Ownership % in equity-method investee — disclosure"),
    "EquityMethodInvestmentRealizedGainLossOnDisposal": (None, "Equity-method disposal gain/loss — disclosure"),
    "EquityMethodInvestmentSoldCarryingAmount": (None, "Equity-method sold carrying amount — disclosure"),
    "EquityMethodInvestmentSummarizedFinancialInformationCurrentAssets": (None, "Summary financials of investee — disclosure"),
    "EquityMethodInvestmentSummarizedFinancialInformationCurrentLiabilities": (None, "Summary financials of investee — disclosure"),
    "EquityMethodInvestmentSummarizedFinancialInformationGrossProfitLoss": (None, "Summary financials of investee — disclosure"),
    "EquityMethodInvestmentSummarizedFinancialInformationIncomeLossFromContinuingOperationsBeforeExtraordinaryItems": (None, "Summary financials of investee — disclosure"),
    "EquityMethodInvestmentSummarizedFinancialInformationNetIncomeLoss": (None, "Summary financials of investee — disclosure"),
    "EquityMethodInvestmentSummarizedFinancialInformationNoncurrentAssets": (None, "Summary financials of investee — disclosure"),
    "EquityMethodInvestmentSummarizedFinancialInformationNoncurrentLiabilities": (None, "Summary financials of investee — disclosure"),
    "EquityMethodInvestmentSummarizedFinancialInformationRedeemablePreferredStock": (None, "Summary financials of investee — disclosure"),
    "EquityMethodInvestmentSummarizedFinancialInformationRevenue": (None, "Summary financials of investee — disclosure"),
    "EquityMethodInvestments": ("LongTermInvestments", "Equity-method investments are non-current investments"),
    "EquityMethodInvestmentsFairValueDisclosure": (None, "Equity-method investments fair-value disclosure"),

    # Equity securities FVNI
    "EquitySecuritiesFVNINoncurrent": ("LongTermInvestments", "Non-current equity securities at fair value"),
    "EquitySecuritiesFvNi": (None, "Equity securities FVNI without current/noncurrent split — ambiguous"),
    "EquitySecuritiesFvNiCost": (None, "Cost basis of FVNI equity securities — disclosure"),
    "EquitySecuritiesFvNiCurrentAndNoncurrent": (None, "Combined current+noncurrent FVNI — ambiguous"),
    "EquitySecuritiesFvNiGainLoss": (None, "Gain/loss on FVNI equity securities — P&L disclosure"),
    "EquitySecuritiesFvNiRealizedGainLoss": (None, "Realized gain/loss on FVNI — disclosure"),
    "EquitySecuritiesFvNiUnrealizedGainLoss": (None, "Unrealized gain/loss on FVNI — disclosure"),
    "EquitySecuritiesWithoutReadilyDeterminableFairValueAmount": (None, "Equity securities without RDFV — disclosure"),
    "EquitySecuritiesWithoutReadilyDeterminableFairValueDownwardPriceAdjustmentAnnualAmount": (None, "Price-adjustment disclosure"),
    "EquitySecuritiesWithoutReadilyDeterminableFairValueDownwardPriceAdjustmentCumulativeAmount": (None, "Price-adjustment disclosure"),
    "EquitySecuritiesWithoutReadilyDeterminableFairValueUpwardPriceAdjustmentAnnualAmount": (None, "Price-adjustment disclosure"),
    "EquitySecuritiesWithoutReadilyDeterminableFairValueUpwardPriceAdjustmentCumulativeAmount": (None, "Price-adjustment disclosure"),

    "EscrowDeposit": (None, "Escrow deposit — situational, no canonical"),
    "ExcessOfReplacementOrCurrentCostsOverStatedLIFOValue": (None, "LIFO reserve disclosure"),

    "IncreaseDecreaseInAccountsPayableTrade": ("ChangeInAccountsPayable", "Cash-flow change in trade AP"),

    "LiabilitiesNoncurrent": ("TotalNonCurrentLiabilities", "Total non-current liabilities — direct match"),
    "LiabilitiesOfAssetsHeldForSale": (None, "Held-for-sale liabilities — situational"),
    "LiabilitiesOfDisposalGroupIncludingDiscontinuedOperation": (None, "Disposal-group liabilities — situational"),
    "LiabilitiesOfDisposalGroupIncludingDiscontinuedOperationCurrent": (None, "Disposal-group liabilities — situational"),
    "LiabilitiesOfDisposalGroupIncludingDiscontinuedOperationNoncurrent": (None, "Disposal-group liabilities — situational"),
    "LiabilitiesRelatedToInvestmentContractsFairValueDisclosure": (None, "Investment-contract liability fair-value — insurance"),
    "LiabilityForAsbestosAndEnvironmentalClaimsNet": (None, "Specific litigation liability — situational"),

    # Non-cash acquisition
    "NoncashOrPartNoncashAcquisitionNoncashFinancialOrEquityInstrumentConsiderationSharesIssued": (None, "Non-cash acquisition disclosure"),
    "NoncashOrPartNoncashAcquisitionOtherAssetsAcquired1": (None, "Non-cash acquisition disclosure"),
    "NoncashOrPartNoncashAcquisitionValueOfAssetsAcquired1": (None, "Non-cash acquisition disclosure"),

    # Derivatives notional
    "NotionalAmountOfDerivatives": (None, "Notional amount disclosure — derivatives footnote"),
    "NotionalAmountOfForeignCurrencyDerivativeInstrumentsNotDesignatedAsHedgingInstruments": (None, "FX derivatives notional disclosure"),
    "NotionalAmountOfForeignCurrencyDerivatives": (None, "FX derivatives notional disclosure"),

    # OCI components
    "OtherComprehensiveIncomeLossDerivativeExcludedComponentIncreaseDecreaseAdjustmentsBeforeTax": (None, "OCI excluded-component detail — disclosure"),
    "OtherComprehensiveIncomeLossTaxPortionAttributableToParent": (None, "OCI tax-portion disclosure"),
    "OtherComprehensiveIncomeLossTaxPortionAttributableToParent1": (None, "OCI tax-portion disclosure"),
    "OtherComprehensiveIncomeMinimumPensionLiabilityNetAdjustmentNetOfTax": (None, "OCI pension-minimum-liability adjustment"),

    # Preferred stock — no preferred-specific canonicals in current taxonomy
    "PreferredStockDividendsPerShareDeclared": (None, "Preferred dividend per share — no preferred-specific canonical"),
    "PreferredStockIncludingAdditionalPaidInCapitalNetOfDiscount": (None, "Preferred stock + APIC — no preferred-specific canonical"),
    "PreferredStockLiquidationPreferenceValue": (None, "Preferred liquidation preference — no canonical"),
    "PreferredStockParOrStatedValuePerShare": (None, "Preferred par value — no canonical"),
    "PreferredStockRedemptionAmount": (None, "Preferred redemption amount — no canonical"),
    "PreferredStockRedemptionDiscount": (None, "Preferred redemption discount — no canonical"),
    "PreferredStockRedemptionPremium": (None, "Preferred redemption premium — no canonical"),
    "PreferredStockRedemptionPricePerShare": (None, "Preferred redemption price — no canonical"),
    "PreferredStockSharesAuthorized": (None, "Preferred shares authorized — no canonical"),
    "PreferredStockSharesIssued": (None, "Preferred shares issued — no canonical"),
    "PreferredStockSharesOutstanding": (None, "Preferred shares outstanding — no canonical"),
    "PreferredStockValue": (None, "Preferred stock value — no canonical"),
    "PreferredStockValueOutstanding": (None, "Preferred stock value outstanding — no canonical"),

    # Insurance premiums earned/written
    "PremiumsEarnedNetPropertyAndCasualty": (None, "Insurance P&C net premiums earned — sector-specific"),
    "PremiumsWrittenNetPropertyAndCasualty": (None, "Insurance P&C net premiums written — sector-specific"),

    # Prepaid expenses
    "PrepaidExpenseAndOtherAssetsCurrent": ("OtherCurrentAssets", "Combined prepaid + other current assets fits OtherCurrentAssets"),
    "PrepaidExpenseCurrent": ("OtherCurrentAssets", "Prepaid expenses are a category of other current assets"),
    "PrepaidExpenseOtherNoncurrent": ("OtherNonCurrentAssets", "Non-current prepaid expense fits OtherNonCurrentAssets"),

    "PrescriptionDrugBenefitReductionInAccumulatedPostretirementBenefitObligationForSubsidy": (None, "Specific Medicare Part D subsidy disclosure"),
    "PrincipalAmountOutstandingOfLoansHeldInPortfolio": (None, "Bank loan portfolio disclosure"),
    "PrincipalAmountOutstandingOnLoansSecuritized": (None, "Securitized loan disclosure"),
    "PrincipalInvestmentGainsLosses": (None, "Principal-investment gain/loss — broker-dealer specific"),
    "PrincipalTransactionsRevenue": (None, "Principal-transactions revenue — broker-dealer specific"),

    # Proceeds (financing/investing)
    "ProceedsFromCollectionOfAdvanceToAffiliate": (None, "Intercompany advance collection — situational"),
    "ProceedsFromCollectionOfFinanceReceivables": (None, "Finance-receivable collection — sector-specific"),
    "ProceedsFromCollectionOfLoansReceivable": (None, "Loan-receivable collection — sector-specific"),
    "ProceedsFromContributionInAidOfConstruction": (None, "Utility CIAC — sector-specific"),
    "ProceedsFromContributionsFromAffiliates": (None, "Intercompany contribution — situational"),
    "ProceedsFromConvertibleDebt": ("ProceedsFromDebtIssuance", "Convertible debt issuance proceeds"),
    "ProceedsFromDebtMaturingInMoreThanThreeMonths": ("ProceedsFromDebtIssuance", "Long-term debt proceeds"),
    "ProceedsFromDebtNetOfIssuanceCosts": ("ProceedsFromDebtIssuance", "Debt proceeds net of issuance costs"),
    "ProceedsFromDivestitureOfBusinesses": ("OtherInvestingActivities", "Divestiture proceeds — no exact canonical, fits Other Investing"),
    "ProceedsFromDivestitureOfBusinessesNetOfCashDivested": ("OtherInvestingActivities", "Divestiture net of cash divested — fits Other Investing"),
    "ProceedsFromEquityMethodInvestmentDividendsOrDistributionsReturnOfCapital": (None, "Equity-method distribution return-of-capital — disclosure"),
    "ProceedsFromHedgeFinancingActivities": ("OtherFinancingActivities", "Hedge financing proceeds — Other Financing"),
    "ProceedsFromIncomeTaxRefunds": (None, "Income tax refund — disclosure, no canonical"),
    "ProceedsFromIssuanceInitialPublicOffering": ("OtherFinancingActivities", "IPO proceeds — Other Financing"),
    "ProceedsFromIssuanceOfCommercialPaper": ("ProceedsFromDebtIssuance", "Commercial paper is debt"),
    "ProceedsFromIssuanceOfCommonStock": ("OtherFinancingActivities", "Common stock issuance proceeds — Other Financing"),
    "ProceedsFromIssuanceOfConvertiblePreferredStock": ("OtherFinancingActivities", "Convertible preferred issuance — Other Financing"),
    "ProceedsFromIssuanceOfDebt": ("ProceedsFromDebtIssuance", "Direct match for debt issuance proceeds"),
    "ProceedsFromIssuanceOfLongTermDebt": ("ProceedsFromDebtIssuance", "Long-term debt issuance proceeds"),

    # Restricted cash
    "RestrictedCashAndCashEquivalentsNoncurrent": ("OtherNonCurrentAssets", "Restricted non-current cash fits OtherNonCurrentAssets"),
    "RestrictedCashAndInvestments": (None, "Restricted cash+investments without current/noncurrent split — ambiguous"),
    "RestrictedCashAndInvestmentsCurrent": ("OtherCurrentAssets", "Current restricted cash+investments fits OtherCurrentAssets"),
    "RestrictedCashCurrent": ("OtherCurrentAssets", "Current restricted cash fits OtherCurrentAssets"),
    "RestrictedCashNoncurrent": ("OtherNonCurrentAssets", "Non-current restricted cash fits OtherNonCurrentAssets"),
    "RestrictedInvestments": (None, "Restricted investments — ambiguous current/noncurrent"),
    "RestrictedInvestmentsCurrent": ("OtherCurrentAssets", "Current restricted investments fit OtherCurrentAssets"),

    # Share-based comp plan-level disclosures
    "ShareBasedCompensationArrangementByShareBasedPaymentAwardEquityInstrumentsOtherThanOptionsNonvestedNumber": ("RSUsOutstanding", "Non-vested non-option awards (RSUs) outstanding"),
    "ShareBasedCompensationArrangementByShareBasedPaymentAwardEquityInstrumentsOtherThanOptionsNonvestedWeightedAverageGrantDateFairValue": (None, "Weighted-avg grant-date FV — disclosure"),
    "ShareBasedCompensationArrangementByShareBasedPaymentAwardEquityInstrumentsOtherThanOptionsVestedInPeriod": ("RSUsVested", "RSUs vested in period"),
    "ShareBasedCompensationArrangementByShareBasedPaymentAwardEquityInstrumentsOtherThanOptionsVestedInPeriodTotalFairValue": (None, "Total FV of RSUs vested — disclosure"),
    "ShareBasedCompensationArrangementByShareBasedPaymentAwardEquityInstrumentsOtherThanOptionsVestedInPeriodWeightedAverageGrantDateFairValue": (None, "Weighted-avg grant-date FV of vested RSUs"),
    "ShareBasedCompensationArrangementByShareBasedPaymentAwardFairValueAssumptionsExpectedDividendRate": (None, "Option-pricing model assumption"),
    "ShareBasedCompensationArrangementByShareBasedPaymentAwardFairValueAssumptionsExpectedTerm": (None, "Option-pricing model assumption"),
    "ShareBasedCompensationArrangementByShareBasedPaymentAwardFairValueAssumptionsExpectedVolatilityRate": (None, "Option-pricing model assumption"),
    "ShareBasedCompensationArrangementByShareBasedPaymentAwardFairValueAssumptionsExpectedVolatilityRateMaximum": (None, "Option-pricing model assumption"),
    "ShareBasedCompensationArrangementByShareBasedPaymentAwardFairValueAssumptionsExpectedVolatilityRateMinimum": (None, "Option-pricing model assumption"),
    "ShareBasedCompensationArrangementByShareBasedPaymentAwardFairValueAssumptionsRiskFreeInterestRate": (None, "Option-pricing model assumption"),
    "ShareBasedCompensationArrangementByShareBasedPaymentAwardFairValueAssumptionsRiskFreeInterestRateMaximum": (None, "Option-pricing model assumption"),
    "ShareBasedCompensationArrangementByShareBasedPaymentAwardFairValueAssumptionsRiskFreeInterestRateMinimum": (None, "Option-pricing model assumption"),
    "ShareBasedCompensationArrangementByShareBasedPaymentAwardFairValueAssumptionsWeightedAverageExpectedDividend": (None, "Option-pricing model assumption"),
    "ShareBasedCompensationArrangementByShareBasedPaymentAwardOptionsVestedAndExpectedToVestExercisableNumber": (None, "Option-disclosure tabular"),
    "ShareBasedCompensationArrangementByShareBasedPaymentAwardOptionsVestedAndExpectedToVestExercisableWeightedAverageExercisePrice": (None, "Option-disclosure tabular"),
    "ShareBasedCompensationArrangementByShareBasedPaymentAwardOptionsVestedAndExpectedToVestExercisableWeightedAverageRemainingContractualTerm": (None, "Option-disclosure tabular"),
    "ShareBasedCompensationArrangementByShareBasedPaymentAwardOptionsVestedAndExpectedToVestOutstandingAggregateIntrinsicValue": (None, "Option-disclosure tabular"),
    "ShareBasedCompensationArrangementByShareBasedPaymentAwardOptionsVestedAndExpectedToVestOutstandingNumber": (None, "Option-disclosure tabular"),
    "ShareBasedCompensationArrangementByShareBasedPaymentAwardOptionsVestedAndExpectedToVestOutstandingWeightedAverageExercisePrice": (None, "Option-disclosure tabular"),
    "ShareBasedCompensationArrangementByShareBasedPaymentAwardOptionsVestedAndExpectedToVestOutstandingWeightedAverageRemainingContractualTerm": (None, "Option-disclosure tabular"),
    "ShareBasedCompensationArrangementByShareBasedPaymentAwardOptionsVestedInPeriodFairValue": (None, "Option-disclosure tabular"),
    "ShareBasedCompensationArrangementByShareBasedPaymentAwardPlanModificationIncrementalCompensationCost": (None, "Plan-modification disclosure"),

    "TransferInvestments": (None, "Transfer between investment classifications — disclosure"),
    "TransferOfFinancialAssetsAccountedForAsSalesAmountDerecognized": (None, "Securitization derecognition disclosure"),
    "TransfersAccountedForAsSecuredBorrowingsAssetsCarryingAmount": (None, "Secured-borrowing transfer disclosure"),
    "TransfersAccountedForAsSecuredBorrowingsAssociatedLiabilitiesCarryingAmount": (None, "Secured-borrowing transfer disclosure"),
    "TransfersOfFinancialAssetsAccountedForAsSaleInitialFairValueOfAssetsObtainedAsProceeds": (None, "Transfer-as-sale FV disclosure"),

    # Translation adjustments
    "TranslationAdjustmentForNetInvestmentHedgeIncreaseDecreaseNetOfTax": (None, "Net-investment-hedge translation — hedge accounting detail"),
    "TranslationAdjustmentForNetInvestmentHedgeLossGainOnReclassifiedOfEarningsNetOfTax": (None, "Net-investment-hedge reclass — hedge accounting detail"),
    "TranslationAdjustmentForNetInvestmentHedgeNetOfTax": (None, "Net-investment-hedge translation — hedge accounting detail"),
    "TranslationAdjustmentFunctionalToReportingCurrencyIncreaseDecreaseGrossOfTax": ("ForeignCurrencyTranslation", "FX translation of functional → reporting currency"),
    "TranslationAdjustmentFunctionalToReportingCurrencyNetOfTaxPeriodIncreaseDecrease": ("ForeignCurrencyTranslation", "FX translation period change, net of tax"),

    "TreasuryStockAcquiredAverageCostPerShare": (None, "Avg cost per share for treasury — disclosure"),
    "TreasuryStockCommonShares": ("TreasuryStock", "Treasury stock (common shares)"),

    # Valuation allowance schedule (Schedule II)
    "ValuationAllowancesAndReservesBalance": ("ValuationAllowance", "Valuation allowance schedule balance"),
    "ValuationAllowancesAndReservesChargedToCostAndExpense": (None, "Schedule II movement — disclosure"),
    "ValuationAllowancesAndReservesDeductions": (None, "Schedule II movement — disclosure"),
    "ValuationAllowancesAndReservesRecoveries": (None, "Schedule II movement — disclosure"),

    "VariableInterestEntityEntityMaximumLossExposureAmount": (None, "VIE max-loss-exposure disclosure"),
}

IFRS_FULL: dict[str, tuple[str | None, str]] = {
    "OtherCashPaymentsToAcquireEquityOrDebtInstrumentsOfOtherEntitiesClassifiedAsInvestingActivities": ("OtherInvestingActivities", "Other investing activity — non-controlling stake purchase"),
    "OtherCashPaymentsToAcquireInterestsInJointVenturesClassifiedAsInvestingActivities": ("OtherInvestingActivities", "JV-stake purchase — Other Investing"),
    "OtherCashReceiptsFromSalesOfEquityOrDebtInstrumentsOfOtherEntitiesClassifiedAsInvestingActivities": ("OtherInvestingActivities", "Other investing receipt — stake sale"),
    "OtherCashReceiptsFromSalesOfInterestsInJointVenturesClassifiedAsInvestingActivities": ("OtherInvestingActivities", "JV-stake sale — Other Investing"),
    "OtherComprehensiveIncome": ("OtherComprehensiveIncome", "Direct match for total OCI"),
    "ShorttermRestructuringProvision": ("OtherCurrentLiabilities", "Short-term restructuring provision is a current liability"),
    "SocialSecurityContributions": (None, "Employee social-security expense — sub-component of compensation, no canonical"),
    "SubordinatedLiabilities": ("LongTermDebt", "Subordinated debt is long-term debt"),
    "SurplusDeficitInPlan": (None, "Pension plan surplus/deficit — actuarial disclosure"),
    "TaxBenefitArisingFromPreviouslyUnrecognisedTaxLossTaxCreditOrTemporaryDifferenceOfPriorPeriodUsedToReduceCurrentTaxExpense": (None, "Tax-reconciliation footnote"),
    "TaxBenefitArisingFromPreviouslyUnrecognisedTaxLossTaxCreditOrTemporaryDifferenceOfPriorPeriodUsedToReduceDeferredTaxExpense": (None, "Tax-reconciliation footnote"),
    "TaxEffectFromChangeInTaxRate": (None, "Tax-rate-change effect — tax footnote"),
    "TaxEffectOfExpenseNotDeductibleInDeterminingTaxableProfitTaxLoss": (None, "Tax-reconciliation footnote"),
    "TaxEffectOfForeignTaxRates": (None, "Tax-reconciliation footnote"),
    "TaxEffectOfRevenuesExemptFromTaxation2011": (None, "Tax-reconciliation footnote (dated)"),
    "TaxEffectOfTaxLosses": (None, "Tax-reconciliation footnote"),
    "TaxExpenseIncomeAtApplicableTaxRate": (None, "Statutory-rate baseline in tax reconciliation"),
    "TaxRateEffectFromChangeInTaxRate": (None, "Tax-reconciliation footnote (rate form)"),
    "TaxRateEffectOfAdjustmentsForCurrentTaxOfPriorPeriods": (None, "Tax-reconciliation footnote (rate form)"),
    "TaxRateEffectOfExpenseNotDeductibleInDeterminingTaxableProfitTaxLoss": (None, "Tax-reconciliation footnote (rate form)"),
    "UnusedProvisionReversedOtherProvisions": (None, "Provision-rollforward disclosure"),
    "UnusedTaxLossesForWhichNoDeferredTaxAssetRecognised": (None, "Unrecognised tax-loss disclosure"),
    "WagesAndSalaries": (None, "Wages and salaries — compensation sub-component, no canonical"),
    "WeightedAverageLesseesIncrementalBorrowingRateAppliedToLeaseLiabilitiesRecognisedAtDateOfInitialApplicationOfIFRS16": (None, "IFRS-16 transition disclosure"),
    "WeightedAverageShares": (None, "Generic weighted-avg shares — taxonomy has Basic/Diluted separately"),
    "WorkInProgress": ("Inventory", "WIP is a component of inventory"),
    "WritedownsReversalsOfInventories": (None, "Inventory write-down adjustment — non-cash CF item"),
    "WritedownsReversalsOfPropertyPlantAndEquipment": (None, "PP&E write-down adjustment — non-cash CF item"),
}


def main() -> None:
    json_path = TAX_DIR / "concept_canonical_map.json"
    cmap = json.loads(json_path.read_text())

    added = {"us-gaap": 0, "ifrs-full": 0}
    for ns, ours in [("us-gaap", US_GAAP), ("ifrs-full", IFRS_FULL)]:
        ns_map = cmap.setdefault(ns, {})
        for tag, (canonical, note) in ours.items():
            if tag in ns_map:
                continue  # don't overwrite — idempotent
            ns_map[tag] = {"canonical": canonical, "note": note}
            added[ns] += 1
    print(f"Added: {added}")

    # Write JSON
    json_path.write_text(json.dumps(cmap, indent=2, ensure_ascii=False))
    print(f"  wrote {json_path.relative_to(ROOT)}")

    # Regenerate markdown
    by_ns = {
        ns: [{"tag": tag, **vals} for tag, vals in cmap.get(ns, {}).items()]
        for ns in ["us-gaap", "ifrs-full", "dei"]
    }
    write_markdown(
        by_ns,
        TAX_DIR / "concept_canonical_map.md",
        token_totals={ns: {"input_tokens": 0, "output_tokens": 0} for ns in by_ns},
        provider="google/gemini-2.5-pro + claude/opus-4.7 tail",
        model="(mixed)",
    )
    print(f"  wrote {(TAX_DIR / 'concept_canonical_map.md').relative_to(ROOT)}")

    # Final coverage check
    print()
    for ns in ["us-gaap", "ifrs-full", "dei"]:
        all_tags = set(t.strip() for t in (TAX_DIR / f"{ns}.txt").read_text().splitlines() if t.strip())
        covered = set(cmap.get(ns, {}).keys())
        mapped = sum(1 for m in cmap.get(ns, {}).values() if m.get("canonical"))
        missing = all_tags - covered
        print(
            f"  {ns}: {len(covered)}/{len(all_tags)} covered "
            f"({100*len(covered)/len(all_tags):.1f}%), "
            f"{mapped} have canonical, {len(missing)} still missing"
        )


if __name__ == "__main__":
    main()
