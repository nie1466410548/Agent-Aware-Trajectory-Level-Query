# Cash Flow Crisis Early-Warning Analysis

## Executive Summary

This report analyzes the historical cash flow trajectories of 10 subsidiaries that transitioned to a "High" cash flow risk level between July–September 2023. The analysis focuses on the 6-month period *before* each subsidiary entered the High risk state, comparing their indicator trajectories against financially healthy (Low risk) periods of the same subsidiaries. Three dimensions were examined: revenue recognition, accounts receivable management, and expense control. The goal is to identify a combination of key indicators and threshold settings that can provide **2–3 months of early warning** for cash flow crises.

---

## 1. Data Overview

- **10 subsidiaries**, all of which eventually transitioned to High cash flow risk
- **18 monthly dashboard periods** (2023-01-31 to 2024-06-24)
- **180 dashboard observations** (10 × 18), **1,800 income statement records**
- **First High risk entry dates**: 3 subsidiaries in July 2023, 5 in August 2023, 2 in September 2023
- **Healthy comparison group**: 37 observations where `cash_flow_risk_level = 'Low'`
- **Pre-High analysis window**: 6 dashboard periods immediately preceding each subsidiary's first High-risk month (60 observations total)

---

## 2. Revenue Recognition — Monthly Revenue Fluctuation

**Definition**: Frequency of month-over-month revenue changes exceeding 20% in absolute value.

| Metric | Pre-High (6mo) | Healthy (Low risk) | 2–3 mo Before High |
|--------|:--------------:|:------------------:|:------------------:|
| Revenue fluctuation > 20% | **43.3%** | 35.1% | **45.0%** |
| Revenue decline > 10% | **35.0%** | 29.7% | **45.0%** |
| Revenue decline > 20% | 18.3% | 16.2% | 20.0% |

**Finding**: Revenue volatility is moderately elevated in the pre-High window. The first revenue fluctuation > 20% typically appears **4–6 months before High**. However, revenue fluctuation alone has limited specificity (65%) — it also occurs in healthy periods.

---

## 3. Accounts Receivable Management

### 3.1 Weighted Average Days Outstanding (DSO)

**Key finding**: The task-suggested threshold of **DSO > 45 days has zero sensitivity** in the pre-High window — it only fires at the exact transition month. A **revised threshold of DSO > 35 days** is far more effective.

| Metric | Pre-High (6mo) | Healthy (Low risk) | 2–3 mo Before High |
|--------|:--------------:|:------------------:|:------------------:|
| DSO > 45 days | **0.0%** | 0.0% | 0.0% |
| DSO > 35 days | **45.0%** | **0.0%** | **50.0%** |
| DSO > 40 days | **21.7%** | 0.0% | 30.0% |
| DSO jump > 5 in one month | **28.3%** | 8.1% | **45.0%** |
| Mean DSO | 34.2 days | 29.0 days | 34.5 days |

**Critical insight**: **DSO > 35 days is the single best early-warning indicator** — it achieves 50% sensitivity in the 2–3 month warning window with **100% specificity** (never observed in healthy periods). Healthy subsidiaries' DSO values are capped at 34.7, while pre-High subsidiaries' DSO reaches 40–45.

**DSO progression by risk level**:
- Low risk: mean 29.0, max 34.7
- Medium risk: mean 40.4, max 44.9 (the "bridge" state)
- High risk: mean 64.6 at transition

### 3.2 Overdue Percentage

| Metric | Pre-High (6mo) | Healthy (Low risk) | 2–3 mo Before High |
|--------|:--------------:|:------------------:|:------------------:|
| Overdue > 5% | 65.0% | 64.9% | 70.0% |
| Overdue > 7% | 23.3% | 24.3% | 25.0% |
| Overdue > 10% | **0.0%** | 0.0% | 0.0% |
| Overdue jump > 1pp | 30.0% | 29.7% | 20.0% |
| 3 consecutive months overdue rise | 6.7% | 8.1% | 5.0% |

**Finding**: The overdue percentage does **not** provide useful early warning. Absolute levels, jumps, and consecutive-rise patterns are statistically indistinguishable between pre-High and healthy periods. Overdue % only becomes elevated (> 15%) at the exact transition month.

---

## 4. Expense Control — Expense vs. Revenue Growth Divergence

| Metric | Pre-High (6mo) | Healthy (Low risk) |
|--------|:--------------:|:------------------:|
| Expense growth > Revenue growth | **50.0%** | 43.2% |
| Mean divergence (exp - rev growth) | **+2.3 pp** | -1.6 pp |
| Divergence > 20 pp | 28.3% | 21.6% |
| Expense up, Revenue down | 26.7% | 24.3% |
| Expense/Revenue ratio | 0.597 | 0.650 |

**Expense category breakdown** (MoM growth):

| Expense Category | Pre-High | Healthy |
|-----------------|:--------:|:-------:|
| Administrative Expense | **+13.0%** | +3.4% |
| Marketing Expense | **+24.3%** | +8.4% |
| R&D Expense | **+13.5%** | +10.9% |
| Travel Expense | +21.4% | **+24.5%** |

**Finding**: The expense-revenue divergence is a **weak individual discriminator** (50% sensitivity, 57% specificity). However, when combined with other signals, it adds incremental value. Administrative and Marketing expenses show notably higher growth rates in the pre-High period compared to healthy periods.

---

## 5. Recommended Early-Warning Framework

### 5.1 Tiered Trigger System

| Tier | Trigger Rule | Sensitivity (2–3mo) | Specificity | Lead Time |
|------|-------------|:-------------------:|:-----------:|:---------:|
| **Tier 1 — ALERT** | **DSO > 35 days** | **50%** | **100%** | 2–6 months |
| **Tier 1 — ALERT** | Revenue MoM fluctuation > 20% | 45% | 65% | 4–6 months |
| **Tier 1 — BROAD** | **DSO > 35 OR RevFluc > 20%** | **65%** | **65%** | 5 months (median) |
| **Tier 2 — ESCALATE** | **DSO > 35 AND (RevFluc > 20% OR DSO jump > 5)** | **45%** | **100%** | 2–4 months |
| **Tier 2 — ESCALATE** | Composite score ≥ 3 of 4 signals¹ | 20% | 97% | 2–4 months |
| **Tier 3 — CRISIS** | DSO > 45 OR Overdue > 10% | — | — | Concurrent (0 months) |

¹ *Four signals: DSO > 35, RevFluc > 20%, Overdue jump > 1pp, Expense growth > Revenue growth*

### 5.2 Recommended Implementation

**Recommended primary early-warning rule:**
```
IF DSO > 35 days OR Revenue MoM fluctuation > 20% THEN issue ALERT
```
- **Captures 65% of pre-crisis months** with 2–6 months lead time
- **False alarm rate**: 35% (acceptable for a broad alert)
- **First trigger**: Median 5 months before High

**Recommended escalation rule:**
```
IF DSO > 35 days AND (RevFluc > 20% OR DSO jump > 5 days) THEN issue ESCALATION
```
- **45% of pre-crisis months** identified
- **Zero false alarms** (100% specificity)
- Confirms the warning with 2–4 months lead time

### 5.3 Cash Flow Forecasting Implications

Net cash flow shows a clear deterioration pattern in the pre-High window:
- At T-3 (3 months before High): **$654K** (mean)
- At T-2: **$593K** (−9.3%)
- At T-1: **$599K** (−8.4%)
- At T0 (transition): **$285K** (−56.4%)

The early-warning signals (DSO > 35, revenue fluctuation) appear **before** the cash flow deterioration becomes severe, providing a genuine forecasting advantage.

---

## 6. Summary of Key Findings

| Dimension | Best Indicator | Threshold | Sensitivity | Specificity | Lead Time |
|-----------|---------------|-----------|:-----------:|:-----------:|:---------:|
| Revenue | MoM fluctuation | > 20% | 45% | 65% | 4–6 months |
| AR Management | Days Outstanding | **> 35 days** | **50%** | **100%** | **2–6 months** |
| AR Management | DSO monthly jump | > 5 days | 45% | 92% | 2–4 months |
| Expense Control | Exp > Rev growth | any | 50% | 57% | 2–4 months |
| **Combined Best** | **DSO > 35 OR RevFluc > 20%** | — | **65%** | **65%** | **5 months** |

**The most actionable early-warning combination is DSO > 35 days** — it provides a perfect specificity (zero false alarms in healthy periods) with reasonable sensitivity, and typically fires 2–6 months before the cash flow crisis fully materializes.

---

## 7. Limitations

1. **Small sample**: 10 subsidiaries, all of which eventually transitioned to High risk. No subsidiary remained healthy throughout, limiting the "healthy" comparison group.
2. **Overlapping definitions**: The 6-month pre-High window naturally includes some Low/Medium risk periods (the gradual deterioration), so the "pre-High" and "healthy" groups are not fully independent.
3. **Monthly granularity**: The dashboard data provides monthly snapshots, so signals within a month are not captured.
4. **No external validation**: The recommended thresholds (DSO > 35, RevFluc > 20%) should be validated on out-of-sample data before operational deployment.
5. **Causal inference**: The analysis identifies correlations, not causal relationships. The DSO increase and revenue fluctuation may be symptoms of deeper issues rather than independent predictors.

---

## Figures

- **Comparison of key metrics**: ![Comparison](comparison_metrics.png)
- **Trajectory plots**: ![Trajectories](trajectories.png)
- **Risk-level boxplots**: ![Risk levels](risk_levels_boxes.png)
- **Signal strength analysis**: ![Signal analysis](early_warning_analysis.png)
- **Final framework**: ![Framework](final_framework.png)