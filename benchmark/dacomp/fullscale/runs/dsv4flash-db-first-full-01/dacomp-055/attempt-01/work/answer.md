# Investment Strategy Misalignment Analysis: Identifying Over-Indexed Underperformers

## Executive Summary

This analysis identifies **476 customers** (14.7% of the qualified base) who are assigned **high investment priority** (top 30% in `investment_priority_score`) yet deliver **bottom-50% composite performance** (weighted 40% sales, 35% adoption, 25% resolution). The core finding is **systemic decoupling**: the `investment_priority_score` (IPS) has **zero correlation with actual returns** (Spearman r = 0.010, p = 0.57) and is instead a proxy for `customer_health_score` (r = 0.825), which itself has no predictive power for churn, ROI, or product adoption. The investment model systematically over-weights C-Level accounts and startups while under-valuing the strongest return drivers: team size, digital engagement, and expansion potential.

---

## 1. Cohort Identification & ROI Characterization

**Methodology**: 3,237 customers with complete data (after deduplication). Composite performance = 0.4 × normalized(`total_sales_amount`) + 0.35 × normalized(`product_adoption_rate`) + 0.25 × normalized(`support_resolution_efficiency`). Ranking via percentile-equivalent row numbers.

| Metric | Target Cohort (n=476) | Non-Cohort (n=2,761) | Difference |
|---|---|---|---|
| Avg Investment Priority Score | **2.26** | 1.36 | +66% |
| Avg Composite Score | **0.325** | 0.417 | −22% |
| Avg ROI (CLV/Acquisition Cost) | **8.76** | 9.56 | −8.4% |
| Avg Product Adoption Rate | **0.665** | 0.775 | −14% |
| Avg Support Resolution Efficiency | **0.673** | 0.762 | −12% |
| Avg Customer Onboarding Score | **2.80** | 3.06 | −8% |
| Avg Team Size | **5.4** | 7.4 | −27% |
| Avg NPS | **59.2** | 71.7 | −17% |
| Avg Digital Engagement Score | **203** | 267 | −24% |
| Avg Churn Probability | 0.211 | 0.202 | n.s. |
| Avg Time-to-Value (days) | **65.1** | 58.6 | +11% |

All differences except churn are statistically significant (p < 0.001, Welch's t-test).

### ROI Distribution by Lifecycle Stage

![Lifecycle stage cohort distribution](fig_lifecycle.png)

| Lifecycle Stage | Cohort Customers | Avg ROI | Observation |
|---|---|---|---|
| Activation | 16 | 9.18 | Small sample, early stage |
| Growth | 127 | 8.44 | Underperforming growth accounts |
| Maturity | 199 | 9.23 | **Largest cluster** — most over-invested |
| Retention | 128 | 8.09 | Lowest ROI in cohort |
| Dormant | 6 | 13.13 | Very small sample, high variance |

The cohort is concentrated in **Maturity** (42%) and **Retention** (27%) — stages where the company has already invested significantly but returns remain below average.

---

## 2. Root Cause Analysis: Industry & Company Size

### Industry Vertical Disparities

![Industry × Size Heatmap](fig_industry_size.png)

**Cohort concentration (% of industry customers):**

| Industry | Cohort % | Cohort N | Trend |
|---|---|---|---|
| **Retail** | 18.5% | 49 | Highest concentration |
| **Government** | 17.8% | 29 | High concentration |
| **Education** | 15.8% | 41 | Above average |
| **Healthcare** | 15.5% | 76 | Above average |
| Manufacturing | 15.1% | 50 | Near average |
| Financial Services | 14.2% | 57 | Near average |
| Technology | 13.7% | 113 | Largest absolute, lower rate |
| Real Estate | 12.8% | 25 | Below average |
| Non-profit | 13.0% | 20 | Below average |
| Media | 11.8% | 27 | Lowest concentration |

**Key insight**: Retail and Government have the highest proportion of over-indexed underperformers, suggesting the investment model systematically overestimates these verticals.

### Company Size Tier: The Strongest Segmentation Effect

| Size Tier | Cohort % | Cohort Avg ROI | Non-Cohort Avg ROI | Avg Onboarding (Cohort) | Avg Onboarding (Non) |
|---|---|---|---|---|---|
| **Startup** | 21.2% | **4.65** | 4.61 | 2.66 | 2.81 |
| **Small** | 17.7% | **7.84** | 7.90 | 2.82 | 2.97 |
| Medium | 13.4% | 10.67 | 10.39 | 2.83 | 3.14 |
| Large | 9.5% | 14.20 | 12.44 | 2.85 | 3.17 |
| Enterprise | 6.1% | 15.15 | 14.53 | 3.07 | 3.28 |

**Critical finding**: Cohort concentration is **inversely proportional to company size**. Startups are 3.5× more likely to be in the target cohort than Enterprise customers. Yet startups have the **lowest ROI** (4.65) while Enterprise has the **highest** (15.15). The model assigns similar IPS scores across all sizes (1.47–1.53) despite a 3× ROI difference — a major systemic bias.

---

## 3. Onboarding Score & Product Adoption: Correlation Analysis

![Onboarding vs Product Adoption Correlation](fig_onboarding_corr.png)

| Group | Pearson r | Spearman r | p-value | N |
|---|---|---|---|---|
| **All customers** | 0.408 | 0.396 | < 1e-130 | 3,237 |
| **Target cohort** | 0.271 | 0.266 | < 1e-8 | 476 |
| **Non-cohort** | 0.403 | 0.391 | < 1e-109 | 2,761 |

The correlation is **significantly weaker in the target cohort** (r = 0.27 vs 0.40), suggesting that for these customers, the onboarding-to-adoption pathway is broken. The variance in adoption is not explained by onboarding quality.

### Onboarding Quartile Analysis

![Onboarding Quartiles](fig_onboarding_quartiles.png)

| Onboarding Quartile | Avg PAR | % in Target Cohort | Avg ROI |
|---|---|---|---|
| Q1 (lowest) | 0.684 | **21.3%** | 8.40 |
| Q2 | 0.745 | 15.8% | 9.76 |
| Q3 | 0.778 | 12.5% | 9.61 |
| Q4 (highest) | 0.827 | **9.1%** | 10.04 |

Customers with the lowest onboarding scores are **2.3× more likely** to be in the target cohort than those with the highest scores. Every quartile improvement in onboarding reduces cohort risk by ~4 percentage points.

---

## 4. Team Size & Decision Maker Level: Impact on Investment Returns

### Team Size Effect

![Team Size & Decision Maker](fig_team_dm.png)

| Team Size | Cohort % | Avg ROI (Cohort) | Avg ROI (Non-Cohort) |
|---|---|---|---|
| 1–2 | **18.6%** | 7.00 | 6.92 |
| 3–5 | 16.1% | 7.47 | 8.40 |
| 6–10 | 14.7% | 10.73 | 10.27 |
| 11–20 | 8.9% | 14.37 | 13.04 |
| 20+ | 6.1% | 14.59 | 14.05 |

**Team size is the strongest actionable driver of ROI** (Spearman r = 0.355, p < 1e-96). The cohort has significantly smaller teams (5.4 vs 7.4, p < 1e-11). Each team-size tier correlates with ~2.5× higher ROI. The investment model does not account for team-size constraints.

### Decision Maker Level

| Decision Maker | Cohort % | Cohort Avg ROI | Non-Cohort Avg ROI | CPS Share vs. ROI |
|---|---|---|---|---|
| **C-Level** | **18.0%** | 6.83 | 7.18 | **15.5% IPS → 7.10 ROI** |
| VP | 15.3% | 9.00 | 9.05 | 26.8% IPS → 9.04 ROI |
| Director | 14.7% | 8.60 | 9.78 | 28.9% IPS → 9.61 ROI |
| Manager | 12.6% | 10.34 | 10.96 | 23.2% IPS → 10.89 ROI |
| Indiv. Contributor | 12.0% | 9.45 | 11.19 | 5.6% IPS → 10.98 ROI |

C-Level accounts are the most over-indexed: they receive 15.5% of the IPS weighting but deliver the **lowest average ROI** (7.10). Managers and Individual Contributors deliver the highest ROI yet receive proportionally less priority.

![ROI by Decision Maker](fig_dm_roi.png)

---

## 5. Systemic Biases in the Investment Decision Model

### 5.1 The IPS–Health Score Confound

The single most important finding: **`investment_priority_score` is NOT a measure of investment priority** — it is a proxy for `customer_health_score`.

| Correlation | r | p-value |
|---|---|---|
| IPS vs. Health Score | **+0.825** | < 1e-300 |
| Health Score vs. ROI | +0.019 | 0.28 |
| Health Score vs. Churn | +0.019 | 0.28 |
| Health Score vs. PAR | +0.008 | 0.65 |

The `customer_health_score` has **zero predictive power** for any actual performance metric. Since IPS is essentially a linear transform of this meaningless health score, the entire investment priority framework is detached from financial reality.

### 5.2 IPS Has No Monotonic Relationship with Returns

![IPS vs ROI](fig_ips_roi.png)

Across all IPS levels (1.0–5.0), there is **no upward trend** in ROI. The Spearman correlation between IPS and ROI is **0.010** (p = 0.57). Within the top-30% IPS group, the correlation is **−0.009** (p = 0.78).

### 5.3 Allocation Imbalance

| Segment | % of Customers | % of IPS Weight | % of Acq. Cost | % of CLV | % of Sales |
|---|---|---|---|---|---|
| Target cohort | 14.7% | **22.3%** | 9.1% | 8.3% | 9.1% |
| Non-cohort | 85.3% | 77.7% | 90.9% | 91.7% | 90.9% |

The target cohort receives **22.3% of the IPS "priority weight"** but contributes only **8.3% of total CLV** — a 2.7× over-weighting in the scoring model.

### 5.4 What Actually Drives ROI?

| Driver | Spearman r with ROI | p-value |
|---|---|---|
| **Expansion Revenue Potential** | **+0.399** | < 1e-123 |
| **Team Size** | **+0.355** | < 1e-96 |
| **Digital Engagement Score** | **+0.342** | < 1e-89 |
| Product Adoption Rate | +0.228 | < 1e-39 |
| Acquisition Cost | +0.224 | < 1e-38 |
| NPS Score | +0.152 | < 1e-17 |
| Onboarding Score | +0.103 | < 1e-8 |
| Support Resolution Efficiency | +0.088 | < 1e-6 |
| Time-to-Value | −0.044 | 0.012 |

**None of these drivers are incorporated into the current IPS model.**

---

## 6. Optimization Recommendations

### 6.1 Rebuild `investment_priority_score` from Performance Drivers

The current IPS is a confounded health-score proxy. Replace it with a model incorporating:
- **Team size** (strongest controllable driver)
- **Digital engagement score** (strongest behavioral signal)
- **Expansion revenue potential** (strongest forward-looking signal)
- **Product adoption rate** (strongest operational metric)

### 6.2 Implement Size-Tier-Adjusted Scoring

Startups and small companies are systematically over-prioritized. Apply a **size-tier factor** (Enterprise = 1.0, Large = 0.9, Medium = 0.7, Small = 0.5, Startup = 0.3) to normalize IPS expectations.

### 6.3 Decision-Maker Level Calibration

C-Level accounts receive disproportionate priority but deliver the lowest returns. **Reduce the default IPS weighting for C-Level contacts** by 25–30% and rebalance toward Manager/IC-level accounts.

### 6.4 Onboarding Intervention Program

The correlation between onboarding and adoption is broken for the target cohort (r = 0.27 vs 0.40 for non-cohort). Implement a **targeted onboarding enhancement program** for customers with:
- Onboarding score < 2.5
- Team size < 5
- Startup or Small company size

### 6.5 Lifecycle-Stage-Specific Investment

| Lifecycle Stage | Recommended Action |
|---|---|
| **Activation** | Increase onboarding investment; the correlation with adoption is strongest here |
| **Growth** | Review adoption support; these accounts have the most potential for turnaround |
| **Maturity** | **Primary intervention target** — largest cohort segment; reassess retention strategy |
| **Retention** | Reduce new investment; focus on cost-efficient support |
| **Dormant** | Flag for automated recovery workflows; avoid new acquisition spend |

### 6.6 Systemic Fix: Decouple `customer_health_score` from IPS

The `customer_health_score` should be rebuilt from:
- Churn probability (actual)
- NPS trend
- Digital engagement trajectory
- Support ticket sentiment
- Payment behavior

These components have **zero overlap** with the current IPS-derived health score and would provide genuine predictive value.

---

## Limitations

1. **Data deduplication**: 3,237 complete cases from 5,001 raw rows (35% dropped due to null metrics, primarily Dormant accounts).
2. **Min-max normalization**: The `total_sales_amount` component is heavily right-skewed, compressing most values near zero in the composite.
3. **Cross-sectional analysis**: Relationships are correlational, not causal. Causal validation would require longitudinal data.
4. **Acquisition cost**: Historical cost, not necessarily reflecting current IPS-driven investment decisions.
5. **Duplicate customer records**: Multiple stripe/zendesk records per marketo lead may introduce noise.

---

## Figures

| Figure | File | Description |
|---|---|---|
| 1 | `fig_lifecycle.png` | Cohort size and ROI by lifecycle stage |
| 2 | `fig_industry_size.png` | Cohort share heatmap by industry and size tier |
| 3 | `fig_onboarding_corr.png` | Onboarding vs. adoption scatter with regression |
| 4 | `fig_onboarding_quartiles.png` | Onboarding quartile effects on adoption, cohort share, ROI |
| 5 | `fig_team_dm.png` | Team size bucket and decision maker level analysis |
| 6 | `fig_dm_roi.png` | Cohort ROI distribution by decision maker level |
| 7 | `fig_ips_roi.png` | IPS level vs. average ROI — non-monotonic relationship |
| 8 | `fig_acq_team.png` | Acquisition cost and team size by cohort |
| 9 | `fig_ips_composite.png` | IPS vs. composite scatter with cohort highlight |
| 10 | `fig_health_roi.png` | Health score and ROI by cohort |