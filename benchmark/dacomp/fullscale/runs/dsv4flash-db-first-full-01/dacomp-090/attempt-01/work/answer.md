# Comprehensive Risk Analysis Report: Customer Payment Deterioration

## Executive Summary

This report identifies **399 high-risk customers** (14.25% of 2,800 total customers) exhibiting payment deterioration — defined as a payment rate below 75% combined with outstanding balances exceeding $15,000. These customers collectively hold **$42.86M in outstanding balances** (64.7% of total $66.23M), with an average composite risk score of **53.65 out of 100**. The collection rate has been declining over the past 33 months (from 51.94% to 45.76%), and the cashflow forecast signals a critical liquidity trajectory. A risk warning model estimates potential losses of **$23.1M–$30.0M** over the next 6 months.

---

## 1. High-Risk Customer Identification and Risk Score

### Filter Criteria
- **Payment rate percentage < 75%**
- **Outstanding balance > $15,000**

**Result**: 399 customers identified.

### Composite Risk Score Calculation

$$ \text{Risk Score} = (100 - \text{payment\_rate\_pct}) \times 0.4 + \frac{850 - \text{credit\_score}}{850} \times 100 \times 0.4 + (100 - \text{business\_stability\_score}) \times 0.2 $$

| Metric | High-Risk (n=399) | Normal (n=2,401) |
|:---|:---:|:---:|
| Avg Risk Score | **53.65** (range: 29.4–76.7) | — |
| Avg Payment Rate | **38.04%** | 91.51% |
| Avg Outstanding Balance | **$107,413.63** | $9,734.09 |
| Avg Credit Score | **467.49** | 773.35 |
| Avg Business Stability Score | **45.70** | 84.65 |

### Risk Score Tier Breakdown

| Risk Tier | Score Range | Customers | Outstanding Balance | Avg Risk Score |
|:---|---:|---:|---:|---:|
| Low (30–40) | 30–40 | 24 | $2,459,074 | 36.01 |
| Medium (40–50) | 40–50 | 130 | $13,325,950 | 45.15 |
| High (50–60) | 50–60 | 129 | $14,471,948 | 54.46 |
| Critical (60+) | 60+ | 116 | $12,601,064 | 65.91 |

![Risk Score Distribution and Tier Breakdown](risk_tier_breakdown.png)

![Risk Analysis Comparison](risk_analysis_1.png)

---

## 2. Gross Profit Contribution Analysis

Using the `quickbooks__profitability_analysis` table, the proportion of high-risk customers' gross profit to total profit is:

| Group | Total Gross Profit | Proportion |
|:---|---:|---:|
| High-Risk Customers | **-$345,457,724.29** | **13.81%** |
| Normal Customers | -$2,156,070,067.17 | 86.19% |
| **All Customers** | **-$2,501,527,791.46** | **100%** |

The high-risk group's proportion (13.81%) is closely aligned with their customer count share (14.25%), indicating that their negative profitability is roughly proportional to their representation. However, their risk-adjusted profit is -$175,070,009.60 (14.14% of total), suggesting slightly higher risk per dollar of profit.

### Profitability Tier Distribution

| Profitability Tier | High-Risk (Invoices) | High-Risk % | Normal (Invoices) | Normal % |
|:---|---:|---:|---:|---:|
| Loss Making | 1,117 | 99.20% | 6,847 | 99.61% |
| Break Even | 7 | 0.62% | 20 | 0.29% |
| Highly Profitable | 1 | 0.09% | 0 | 0.00% |
| Profitable | 1 | 0.09% | 1 | 0.01% |

**Key finding**: Both groups are overwhelmingly concentrated in the "Loss Making" tier, indicating that the synthetic dataset's COGS structure inflates costs. The distribution pattern is similar between groups.

![Profitability Tier Distribution](profitability_tier_dist.png)

---

## 3. Collection Rate Month-over-Month Trend Analysis

### Full Period Trend (Jan 2023 – Sep 2025)

The collection rate has declined from **51.94%** (Jan 2023) to **45.76%** (Sep 2025), a net decline of **6.18 percentage points** over 33 months.

### Last 12 Months Detailed Analysis (Oct 2024 – Sep 2025)

| Month | Collection Rate | MoM Change | Status |
|:---|---:|---:|:---|
| Oct 2024 | 47.11% | — | Baseline |
| Nov 2024 | 52.05% | +4.94pp | Improvement |
| Dec 2024 | 50.58% | −1.47pp | **Decline** |
| Jan 2025 | 48.64% | −1.94pp | **Decline** |
| Feb 2025 | 47.32% | −1.32pp | **Decline** |
| Mar 2025 | 47.85% | +0.53pp | Recovery |
| Apr 2025 | 50.59% | +2.74pp | Improvement |
| May 2025 | 47.64% | −2.95pp | Decline |
| Jun 2025 | 51.54% | +3.90pp | Improvement |
| Jul 2025 | 50.97% | −0.57pp | **Decline** |
| Aug 2025 | 46.06% | −4.91pp | **Decline** |
| Sep 2025 | 45.76% | −0.30pp | **Decline** |

### Consecutive Deterioration Streaks

1. **Dec 2024 – Feb 2025**: 3 consecutive months of decline, cumulative drop of **−4.73pp** (50.58% → 47.32%)
2. **Jul 2025 – Sep 2025** (ongoing): 3 consecutive months of decline, cumulative drop of **−5.78pp** (50.97% → 45.76%)

The most recent streak (Jul–Sep 2025) has the **largest magnitude of decline** (−5.78pp), with the single steepest monthly drop in August 2025 (−4.91pp). The average monthly decline in the last 3 months is **−2.61pp/month**.

![Collection Rate Trend](collection_rate_trend.png)

---

## 4. Distribution Characteristics: High-Risk vs Normal Customers

### Statistical Comparison (Mann-Whitney U Test)

| Metric | High-Risk Mean | Normal Mean | p-value | Significant? |
|:---|---:|---:|---:|:---:|
| Payment Timeliness Score | 47.56 | 88.08 | **8.1e-221** | ✅ Yes |
| Credit Score | 467.49 | 773.35 | **1.8e-220** | ✅ Yes |
| Payment Rate % | 38.04% | 91.51% | **3.5e-220** | ✅ Yes |
| Business Stability Score | 45.70 | 84.65 | **2.1e-219** | ✅ Yes |
| Outstanding Balance | $107,413.63 | $9,734.09 | **2.9e-211** | ✅ Yes |
| Revenue Growth 12m % | 59.02% | 40.13% | **0.015** | ✅ Yes |
| Avg Payment Days 12m | 99.97 | 109.03 | 0.086 | No |
| Customer Lifespan Days | 911.82 | 931.81 | 0.463 | No |
| Total Invoices | 38.38 | 39.51 | 0.371 | No |
| Avg Invoice Amount | $20,815.66 | $20,325.81 | 0.590 | No |
| Active Months | 2.72 | 2.74 | 0.734 | No |

### Key Distribution Findings

1. **Strongly Differentiating Factors** (p < 0.001): Credit score, payment timeliness, business stability, and payment rate are the core drivers separating high-risk from normal customers. The high-risk group has drastically lower credit scores (avg 467 vs 773) and stability scores (avg 46 vs 85).

2. **Non-Differentiating Factors** (p > 0.05): Customer lifespan, total invoices, average invoice amount, active months, overdue count, and monthly revenue are statistically similar between groups. This suggests the risk is **behavioral and credit-driven** rather than related to customer size or tenure.

3. **Activity Status**: High-risk customers show a higher proportion of "Lost" and "Inactive" statuses (62.9% combined vs 61.4% for normal), but the difference is modest.

4. **Lifecycle Stage**: Distribution is similar between groups, with "Cannot Lose Them" (23.3%), "Lost Customer" (21.6%), and "New Customer" (21.1%) being the top stages for high-risk.

5. **Credit Grade**: All high-risk customers are in grades C–D (C: 25.8%, C+: 21.6%, C−: 23.3%, D: 29.3%), while normal customers are predominantly A/A+/A− (75.7%).

---

## 5. Risk Warning Model and Potential Loss Assessment

### Framework

Using the cashflow forecast data (Oct 2025 – Mar 2026) and the composite risk scores, we built a multi-scenario risk warning model to estimate potential losses.

### Cashflow Forecast Outlook

| Month | Forecasted Net Cash Flow | Liquidity Status |
|:---|---:|:---|
| Oct 2025 | $125,000.50 | Stable |
| Nov 2025 | $98,000.75 | Stable |
| Dec 2025 | $87,500.25 | **At Risk** |
| Jan 2026 | $65,000.00 | **At Risk** |
| Feb 2026 | $42,000.50 | **Critical** |
| Mar 2026 | $25,000.00 | **Critical** |

The cashflow forecast shows a **declining trajectory** from $125K to $25K, with liquidity status deteriorating from "Stable" to "Critical" over 6 months. The total forecasted net cash flow over 6 months is only **$442,502** — far insufficient to cover the $42.86M in high-risk outstanding balances.

![Cashflow Forecast](cashflow_forecast.png)

### Scenario Analysis Results

| Scenario | Estimated Loss | Recovery | Methodology |
|:---|---:|---:|:---|
| **Base** (Current Rate) | **$23.25M** | $19.61M | Loss = outstanding × (1 − current collection rate 45.76%) |
| **Risk-Weighted** | **$23.06M** | $19.80M | Loss = Σ(outstanding × risk_score/100) |
| **Pessimistic** (Declining) | **$29.94M** | $12.91M | Collection rate drops to 30.13% (extrapolating −2.61pp/mo decline) |
| **Worst-Case** (Combined) | **$27.00M** | $15.86M | Risk-weighted loss escalated by decline trend factor |

**Key Insight**: The risk-weighted expected loss of **$23.06M** (53.8% of outstanding) is roughly equivalent to the base scenario. However, if the declining collection rate trend continues, the projected loss could reach **$29.94M** (69.9% of outstanding), exceeding the total 6-month forecasted cash flow of $442,502 by over **67 times**.

![Risk Warning Model](risk_warning_model.png)

---

## 6. Tiered Customer Management and Risk Control Strategies

### Tier Classification Based on Risk Score

| Risk Tier | Criteria | Count | Total Outstanding | Recommended Strategy |
|:---|---:|---:|---:|:---|
| **Critical (60+)** | Risk Score ≥ 60 | 116 | $12.60M | **Immediate Intervention** |
| **High (50–60)** | Risk Score 50–60 | 129 | $14.47M | **Intensive Monitoring** |
| **Medium (40–50)** | Risk Score 40–50 | 130 | $13.33M | **Enhanced Collection** |
| **Low (30–40)** | Risk Score 30–40 | 24 | $2.46M | **Standard Collection** |

### Proposed Strategic Actions

#### Tier 1: Critical (116 customers, $12.6M outstanding)
- **Immediate escalation**: Place accounts with legal/collections agency within 15 days
- **Personal outreach**: Assign dedicated account manager for direct negotiation
- **Payment restructuring**: Offer 30–50% discount on principal for lump-sum settlement
- **Credit hold**: Suspend further credit/services until arrears are resolved
- **Priority**: Highest ROI — average outstanding per customer is $108,630

#### Tier 2: High (129 customers, $14.47M outstanding)
- **Intensified collection**: Dunning sequences every 5 days with escalating urgency
- **Payment plans**: Offer structured 3–6 month installment agreements
- **Deposit requirements**: Require 50% upfront payment for any new services
- **Regular reviews**: Bi-weekly portfolio review with dedicated collections team
- **Risk flag**: Mark accounts for manual review before any credit extension

#### Tier 3: Medium (130 customers, $13.33M outstanding)
- **Automated reminders**: Email + SMS reminders at 7, 3, and 1 days before due date
- **Incentive programs**: Offer 2–5% early payment discount
- **Quarterly reassessment**: Review risk score and payment behavior quarterly
- **Self-service portal**: Encourage online payment with automated reconciliation

#### Tier 4: Low (24 customers, $2.46M outstanding)
- **Standard monitoring**: Regular monthly statements
- **Preventive education**: Send payment behavior improvement tips
- **Watchlist**: Flag for monitoring if payment rate drops below 50% or overdue count increases

### Cross-Organizational Risk Mitigation

1. **Cashflow hedge**: Given the forecasted cashflow decline of 80% (from $125K to $25K), the company should establish a **$2M–$3M liquidity reserve** to cover the expected collection shortfall over the next 6 months.

2. **Collection process optimization**: The current collection rate of 45.76% is critically low. Implementing automated payment reminders, late fee structures, and tiered escalation could improve recovery by 5–10 percentage points, potentially recovering an additional **$2.1M–$4.3M**.

3. **Credit policy reform**: Tighten credit approval criteria — require minimum credit score of 600 (currently 467 avg for high-risk) and business stability score of 60+ (currently 46 avg) for new customers.

4. **Early warning system**: Implement real-time monitoring of payment rate, overdue count, and payment timeliness score. Any customer whose payment rate drops below 75% should trigger an automatic review, long before balances reach $15,000.

5. **Customer segmentation for outreach**: Prioritize high-risk customers with:
   - High outstanding balance × high risk score (top 20% represent $17.2M in exposure)
   - Recent activity (active in last 3 months) — these customers are still reachable
   - "Cannot Lose Them" lifecycle stage — these are valuable relationships to salvage

---

## Limitations

1. **Data Quality**: The gross profit figures in `quickbooks__profitability_analysis` show extreme negative values (avg margin −4,388%), indicating the COGS data may be synthetic or the cost allocation method inflates costs. This limits the reliability of the profit contribution analysis.

2. **Forecast Data Sparsity**: The `quickbooks__cashflow_forecast` table contains only `forecasted_net_cash_flow` and `liquidity_status` columns; other forecast columns (inflows, outflows, risk-adjusted, confidence) are NULL, limiting multi-dimensional cashflow modeling.

3. **Correlation vs Causation**: The statistical analysis identifies significant differences between groups but cannot establish causality. The deteriorating payment behavior may be a symptom of broader economic conditions rather than customer-specific factors.

4. **Scenario Limitations**: The pessimistic scenario assumes a linear decline of −2.61pp/month, which may not hold as collection rates have natural floors and organizations typically respond to deteriorating trends.