# High-Quality, Shrinking-Spend Vendor Analysis Report

## Executive Summary

From the `quickbooks__vendor_performance` table, **342 vendors** were identified as "high-quality, shrinking-spend" — defined by a negative `annual_spend_growth_pct` and an `overall_performance_score` of 7 or higher. These vendors collectively represent **$28.5M in lifetime spend** with an average monthly spend of **$3.94M** (36.5% of total vendor spend). A comprehensive cash flow impact model shows that a 30% reduction in collaboration with these vendors would improve the 18-month cumulative net cash flow by **$3.77M** and reduce the average Liquidity Risk Index by **0.035** (a 26.8% improvement).

---

## 1. Vendor Identification & Core Metrics

### Selection Criteria
- `annual_spend_growth_pct` **< 0** (negative growth)
- `overall_performance_score` **>= 7** (high quality)

| Metric | Value |
|--------|-------|
| Number of qualifying vendors | **342** |
| Total lifetime spend | **$28,472,327.29** |
| Total avg monthly spend | **$3,941,552.02** |
| Share of all-vendor monthly spend | **36.5%** |
| Share of GL transaction outflow | **23.2%** |

### Performance Score Distribution
| Score | Count | Avg Growth % |
|-------|-------|-------------|
| 7 | 125 | -15.45% |
| 8 | 136 | -16.82% |
| 9 | 81 | -15.61% |

### Vendor Tier Breakdown
| Tier | Vendors | |
|------|---------|---|
| Preferred Vendor | 92 | |
| Strategic Vendor | 85 | |
| Standard Vendor | 83 | |
| Tactical Vendor | 82 | |

### Spend Volatility Coefficient
**Formula:** `spend_volatility / total_lifetime_spend`

| Statistic | Value |
|-----------|-------|
| Mean | **0.9448** |
| Median | **0.2485** |
| Min | **0.0008** |
| Max | **28.8445** |

The distribution is right-skewed. The median of 0.2485 indicates that for a typical vendor, spend volatility is about 25% of lifetime spend. The high mean (0.94) is driven by a small number of vendors with very high volatility relative to their low lifetime spend.

### Composite Risk Score
**Formula:** `payment_completion_rate × 0.4 + (business_value_score / 10) × 0.6`

| Statistic | Value |
|-----------|-------|
| Mean | **0.7815** |
| Min | **0.4623** |
| Max | **0.9394** |

Higher scores indicate better vendors (higher payment completion and business value). The mean of 0.78 reflects these vendors' high-quality profile.

![Vendor Metrics Distribution](fig1_vendor_metrics.png)

---

## 2. Account-Type Spend Change Rate Analysis

Using the `quickbooks__general_ledger` transaction records for the 342 selected vendors, spend change rates were calculated as the percentage change in **magnitude-based spend volume** (sum of absolute amounts) between the last 12 months (2024-10-15 to 2025-10-14) and the prior 12 months (2023-10-15 to 2024-10-15).

### Per-Account-Type Magnitude-Based Spend Change

| Account Type | Avg Change% | **Median Change%** | P25 | P75 | Total Vol Last 12M | Total Vol Prior 12M | Volume Change% |
|-------------|:-----------:|:------------------:|:---:|:---:|:------------------:|:-------------------:|:--------------:|
| **Asset** | +69.7% | **-4.1%** | -45.9% | +72.5% | $119.56M | $124.03M | **-3.6%** |
| **Expense** | +171.2% | **-7.0%** | -50.7% | +73.0% | $58.52M | $61.12M | **-4.2%** |
| **Liability** | +51.6% | **-0.5%** | -43.8% | +60.9% | $40.00M | $41.09M | **-2.7%** |
| **Revenue** | +65.1% | **+0.4%** | -42.9% | +60.8% | $40.20M | $39.70M | **+1.3%** |

**Key Interpretations:**
- The **median** (rather than mean) is the more reliable measure here due to the presence of extreme outliers (e.g., Expense min -22,160%, Revenue max +2,781%).
- **Expense accounts** (the primary vendor spend outflows) show a median decline of **-7.0%**, consistent with the shrinking-spend profile.
- **Liability accounts** show a near-zero median change (-0.5%), indicating stable payment obligations.
- **Revenue accounts** are the only category with a positive median change (+0.4%), suggesting some vendor-related income is slightly increasing.
- **Overall magnitude-based volume** across all account types declined by **-2.88%**, confirming the spend reduction trend.

### Transaction Frequency Density

**Formula:** `number of transactions / number of active days` (per vendor-account-type pair)

| Account Type | Mean Density | Median Density |
|-------------|:-----------:|:--------------:|
| Asset | 1.0047 | 1.0000 |
| Expense | 1.0054 | 1.0000 |
| Liability | 1.0050 | 1.0000 |
| Revenue | 1.0061 | 1.0000 |

The transaction frequency density is consistently ~1.0 across all account types, meaning most vendors typically have about one transaction per active day per account type. The slight variation above 1.0 suggests occasional days with multiple transactions but this is minimal.

![Account-Type Analysis](fig2_account_type_analysis.png)

---

## 3. Cash Flow Impact Model

### Model Assumptions

1. **Vendor outflow share**: 23.18% of total company outflows (derived from the GL — selected vendors' Expense+Liability transactions as a share of total company Expense+Liability transactions over 24 months).
2. **30% reduction in collaboration**: Reduces the selected vendor portion of outflows by 30%, i.e., total outflow reduction = 30% × 23.18% = **6.95%**.
3. **Adjusted monthly outflow** = `forecasted_outflows × (1 − 0.30 × 0.2318)` = `forecasted_outflows × 0.9305`.

### Liquidity Risk Index (LRI)

**Definition:** For each month, LRI = `max(0, −net_cash_flow) / forecasted_inflows` (the proportion of monthly inflows consumed by a cash deficit). The overall LRI is the average across all 18 forecast months.

### Results

| Metric | Baseline | Adjusted (30% Reduction) | Change |
|--------|:--------:|:------------------------:|:------:|
| **Total outflow (18 months)** | $54,185,988.66 | $50,417,895.01 | **−$3,768,093.65** |
| **Cumulative net cash flow (18 months)** | **$923,210.35** | **$4,691,304.01** | **+$3,768,093.66** |
| **Average Liquidity Risk Index** | **0.1299** | **0.0951** | **−0.0348 (26.8% improvement)** |
| Months with deficit (net negative) | 8 of 18 | 7 of 18 | −1 month |

### Monthly Detail (Selected Months)

| Month | Baseline Outflow | Adjusted Outflow | Vendor Reduction | Baseline Net | Adjusted Net | Baseline LRI | Adjusted LRI |
|-------|:---------------:|:----------------:|:----------------:|:------------:|:------------:|:------------:|:------------:|
| 2025-10 | $2,002,561 | $1,863,302 | $139,258 | -$24,981 | $114,277 | 0.013 | 0.000 |
| 2025-11 | $3,389,818 | $3,154,090 | $235,728 | -$124,748 | $110,980 | 0.038 | 0.000 |
| 2025-12 | $1,665,966 | $1,550,115 | $115,851 | $1,924,278 | $2,040,129 | 0.000 | 0.000 |
| 2026-04 | $2,863,181 | $2,664,076 | $199,106 | -$680,292 | -$481,186 | 0.312 | 0.220 |
| 2026-09 | $2,715,564 | $2,526,724 | $188,840 | -$751,287 | -$562,446 | 0.382 | 0.286 |
| 2026-12 | $4,555,179 | $4,238,477 | $316,702 | -$1,595,506 | -$1,278,804 | 0.539 | 0.432 |
| 2027-02 | $4,528,910 | $4,213,747 | $315,163 | -$885,115 | -$569,952 | 0.243 | 0.156 |

### Key Observations
- **The 30% collaboration reduction** converts the 18-month cumulative net cash flow from barely positive ($923K) to a healthy $4.69M.
- **Deficit months** (where outflows exceed inflows) see their deficit magnitudes reduced by 23-36%.
- **The Liquidity Risk Index** drops from 0.130 to 0.095, representing a meaningful improvement in the company's cash flow risk profile.
- **The largest absolute improvements** occur in months with already-high forecasted outflows (2026-12, 2027-01, 2027-02), where the vendor reduction provides the most relief.

![Cash Flow Impact Model](fig3_cash_flow_impact.png)

---

## 4. Risk Profile of Selected Vendors

### Payment Risk Level
| Level | Count |
|-------|-------|
| Medium Risk | 98 |
| High Risk | 92 |
| Critical Risk | 80 |
| Low Risk | 72 |

### Dependency Level
| Level | Count |
|-------|-------|
| Critical Dependency | 101 |
| Low Dependency | 85 |
| High Dependency | 82 |
| Medium Dependency | 74 |

### Performance Rating
| Rating | Count |
|--------|-------|
| Good | 94 |
| Poor | 83 |
| Fair | 83 |
| Excellent | 82 |

Despite being "high-quality" (score ≥ 7), a significant portion of these vendors carry **Critical** or **High** payment risk, and many are **Critical Dependency** vendors. This means the 30% collaboration reduction strategy must be implemented carefully, potentially with phased transitions or alternative sourcing.

---

## 5. Conclusions & Recommendations

1. **342 vendors** qualify as high-quality, shrinking-spend, with a combined $3.94M/month spend.
2. The **spend volatility coefficient** (median 0.25) indicates moderate spend volatility relative to lifetime spend for most vendors.
3. The **composite risk score** (mean 0.78) confirms these are generally high-quality vendors, though individual scores range from 0.46 to 0.94.
4. **Expense account spend is declining** (median -7.0%), confirming the shrinking-spend pattern, while Revenue accounts show slight growth (+0.4%).
5. **A 30% reduction** in collaboration with these vendors would:
   - Save **$3.77M** in outflows over 18 months
   - Improve the cumulative net cash flow from **$0.92M to $4.69M**
   - Reduce the **Liquidity Risk Index by 26.8%**
   - Eliminate 1 deficit month and reduce severity in the remaining 7

### Limitations
- The cash flow impact model assumes the vendor outflow share (23.18%) is constant across all forecast months, which may not reflect seasonal variations.
- The 30% reduction is applied uniformly; real-world implementation would consider vendor-specific dependencies and transition costs.
- The Liquidity Risk Index is a constructed metric; the `liquidity_risk_level` categorical field in the original data maps to the same ordinal risk levels but shows no change because the 6.95% improvement is not large enough to cross categorical thresholds.
- Transaction frequency density is near-perfectly 1.0, suggesting limited granularity in the daily transaction data.

### Figures

| Figure | Description | File |
|--------|-------------|------|
| 1 | Vendor metrics distributions (volatility coefficient, composite risk, growth vs performance, top 20 vendors) | [fig1_vendor_metrics.png](fig1_vendor_metrics.png) |
| 2 | Account-type spend change rates and transaction frequency density | [fig2_account_type_analysis.png](fig2_account_type_analysis.png) |
| 3 | Cash flow impact model (monthly outflows, net cash flows, cumulative trajectory, monthly improvement) | [fig3_cash_flow_impact.png](fig3_cash_flow_impact.png) |