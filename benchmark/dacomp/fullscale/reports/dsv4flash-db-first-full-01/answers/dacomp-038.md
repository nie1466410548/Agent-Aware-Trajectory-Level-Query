<!-- Reading copy: local artifact links normalized. Original answer is preserved at ../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/answer.md -->

# Strategy Gray Release Analysis Report

## Executive Summary

A gray release of new strategy versions began on **July 4, 2025** (the task reference date of July 5 falls within the gray period). Four strategy families were evaluated: **Search Strategy**, **Caixi Strategy (Guess You Like)**, **Popup Strategy**, and **Renqun Dongcha Strategy**. The analysis compares the new versions against the old versions using a controlled category-level approach: categories that moved to the new version in the gray period (Jul 4–7) are compared against control categories that remained on the old version, with pre-period (Jul 1–3) baselines.

### Recommendations

| Strategy | Old Version | New Version | Recommendation | Confidence |
|---|---|---|---|---|
| **Search Strategy** | v3.6 | v3.7 | **Proceed to full rollout** | Medium |
| **Caixi Strategy (Guess You Like)** | v4.8 | v4.9 | **Proceed to full rollout** (with cost monitoring) | Medium |
| **Popup Strategy** | v2.9 | v2.9.1 | **Proceed to full rollout** | Medium-Low |
| **Renqun Dongcha Strategy** | v3.2 | v3.2.1 | **Hold / Not recommended** | Low |

---

## Market Context

The overall market (all 73 categories from Sheet2) shows a clear weekday vs weekend pattern:

- **Pre-period** (Jul 1–3, Tue–Thu): Higher daily orders (48k–52k) and transaction amounts (1.71M–2.03M Yuan)
- **Gray period** (Jul 4–7, Fri–Mon): Lower daily orders (48k–49k) and transaction amounts (~1.70M–1.73M Yuan)

The market-wide decline of approximately 5–8% in orders and transaction amounts is observed across both test and control groups, confirming the need for a controlled comparison.

![Market Trends](<../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/work/market_trends.png>)

---

## Methodology

For each strategy family, we identified the set of product categories served by the old version during the pre-period (Jul 1–3). During the gray period (Jul 4–7), some categories were moved to the new version while others remained on the old version. We computed **per-category weighted metrics** (CTR, CPC, CPM, orders/day, transaction amount/day) for both periods and tested whether the distribution of deltas (gray − pre) differed between the new-version categories and the old-version control categories using the Mann-Whitney U test.

---

## Strategy-by-Strategy Analysis

### 1. Search Strategy v3.7 (vs v3.6)

| Metric | New Version Cats (N=10) | Old Version Control Cats (N=21) | MWU p-value |
|---|---|---|---|
| **CTR** | −3.2% (weighted) | +1.2% | 0.183 |
| **CPC** | +3.4% | −0.7% | 0.849 |
| **CPM** | +0.1% | +0.4% | 1.000 |
| **Orders/day** | −4.8% | −4.8% | 0.882 |
| **Tx Amt/day** | −8.2% | −10.6% | 0.688 |

**Assessment:** The new version performs at parity with the old version. Order declines are identical to the control group. Transaction amount decline is slightly less (better) for the new version, though not statistically significant. No performance degradation is observed.

**→ Recommendation: Proceed to full rollout.**

### 2. Caixi Strategy v4.9 (Guess You Like) (vs v4.8)

| Metric | New Version Cats (N=11) | Old Version Control Cats (N=12) | MWU p-value |
|---|---|---|---|
| **CTR** | −1.6% (weighted); **+5.3% per-cat mean** | −0.3% | **0.0012*** |
| **CPC** | +10.2% | −0.2% | 0.601 |
| **CPM** | +8.4% | −0.4% | 0.255 |
| **Orders/day** | −3.8% | −3.9% | 0.518 |
| **Tx Amt/day** | −11.6% | −8.8% | 0.926 |

**Assessment:** The per-category CTR improvement is **statistically significant** (p=0.0012) — all 11 categories that moved to v4.9 showed CTR improvement, while the control categories showed near-zero change. However, the weighted CTR decreased slightly because impression mix shifted toward lower-CTR categories. CPC and CPM increased, and transaction amount declined more. The CTR signal is strong and consistent.

**→ Recommendation: Proceed to full rollout with monitoring of cost efficiency (CPC/CPM).**

### 3. Popup Strategy v2.9.1 (vs v2.9)

| Metric | New Version Cats (N=5) | Old Version Control Cats (N=5) | MWU p-value |
|---|---|---|---|
| **CTR** | +0.1% | +0.4% | 0.222 |
| **CPC** | +6.0% | +1.1% | 0.548 |
| **CPM** | +6.0% | +1.5% | 0.548 |
| **Budget Utilization** | −10.5% | +2.0% | 0.095 |
| **Orders/day** | −2.3% | −10.7% | 0.841 |
| **Tx Amt/day** | −7.5% | −17.9% | 0.421 |

**Assessment:** While cost efficiency metrics (CPC, CPM, Budget Utilization) are slightly worse for the new version, **order retention is substantially better**. The old control categories experienced a severe decline (−10.7% orders, −17.9% tx amount), while new-version categories held much better (−2.3%, −7.5%). The small sample size (N=5 per group) limits statistical significance, but the directional signal is strong.

**→ Recommendation: Proceed to full rollout** with caution; monitor cost efficiency closely.

### 4. Renqun Dongcha Strategy v3.2.1 (vs v3.2)

| Metric | New Version Cats (N=5) | Old Version Control Cats (N=4) | MWU p-value |
|---|---|---|---|
| **CTR** | −1.0% | −0.1% | 1.000 |
| **CPC** | −1.1% (better) | +0.9% | 0.730 |
| **CPM** | −2.1% (better) | +0.8% | 0.730 |
| **Orders/day** | −6.7% | −2.0% | 0.191 |
| **Tx Amt/day** | −10.6% | −5.9% | 0.556 |

**Assessment:** Directionally worse than the control group. Order and transaction declines are larger for the new version. While not statistically significant (small N), the consistent negative direction warrants caution.

**→ Recommendation: Hold and gather more data before considering rollout.**

---

## Controlled Comparison Visualization

![Controlled Comparison](<../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/work/final_summary.png>)

The chart shows the percentage change from pre-period to gray period for each metric, comparing new-version categories (blue) against old-version control categories (salmon). Positive values indicate improvement.

---

## Limitations

1. **Small sample sizes**: The Renqun Dongcha and Popup strategies have only 4–5 categories per group, limiting statistical power.
2. **Short observation period**: Only 4 days of gray release data (Jul 4–7) and 3 days of pre-period data (Jul 1–3) are available.
3. **Day-of-week effects**: The pre-period (Tue–Thu) and gray period (Fri–Mon) have different day-of-week compositions, which may affect order patterns.
4. **Category assignment**: Categories were not randomly assigned to old/new versions, so inherent category differences may affect results.
5. **Sheet2 metrics**: The T+0 order metrics are at the category level and do not have a strategy dimension, so they serve as a proxy for overall category performance rather than direct strategy attribution.

---

## Conclusion

| Strategy | Decision | Rationale |
|---|---|---|
| **Search Strategy v3.7** | ✅ Full Rollout | No degradation; performance parity with control |
| **Caixi Strategy v4.9 (Guess You Like)** | ✅ Full Rollout with Monitoring | Significant CTR improvement; watch cost efficiency |
| **Popup Strategy v2.9.1** | ✅ Full Rollout with Caution | Better order retention despite higher costs; small sample |
| **Renqun Dongcha Strategy v3.2.1** | ❌ Hold | Directionally worse; insufficient evidence for rollout |

![Decision Table](<../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/work/decision_table.png>)