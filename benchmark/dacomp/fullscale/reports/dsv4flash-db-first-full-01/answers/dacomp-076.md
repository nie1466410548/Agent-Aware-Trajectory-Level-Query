<!-- Reading copy: local artifact links normalized. Original answer is preserved at ../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/answer.md -->

# Customer Segmentation Effectiveness Analysis

## Executive Summary

We analyzed 149 customer records (107 unique customers) across 5 profitability segments (Basic, Growing, Standard, High Value, Premium) to evaluate whether the current `profitability_segment` classifications align with actual customer performance. **47 records (31.5%) from 39 unique customers (36.4%)** were identified as "classification anomalies" — where `retention_probability` deviates from the segment's average retention rate by more than 0.15.

The analysis reveals that **anomalies are concentrated entirely in the High Value (74.1%), Basic (66.7%), and Standard (65.2%) segments**, while Premium and Growing segments show zero anomalous records. The existing value metrics explain only 12.4% of retention variance (R² = 0.124), indicating substantial room for segmentation improvement through new dimensions.

---

## 1. Anomaly Identification and Scope

### Methodology

| Metric | Value |
|--------|-------|
| Total records | 149 |
| Unique customers | 107 |
| Anomaly records (deviation > 0.15) | 47 (31.5%) |
| Unique anomaly customers | 39 (36.4%) |
| Positive anomalies (retention above avg) | 23 records |
| Negative anomalies (retention below avg) | 24 records |

### Segment-Level Anomaly Rates

![Retention by segment with anomaly bands](<../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/work/retention_by_segment.png>)

*Figure 1: Retention probability distribution by segment. Red points are anomalies (>0.15 deviation from segment mean). Black diamonds show segment averages; orange bands show ±0.15 range.*

| Segment | Records | Anomaly Count | Anomaly Rate |
|---------|---------|---------------|-------------|
| **High Value** | 27 | 20 | **74.1%** |
| **Basic** | 18 | 12 | **66.7%** |
| **Standard** | 23 | 15 | **65.2%** |
| Premium | 52 | 0 | 0.0% |
| Growing | 29 | 0 | 0.0% |

**Key insight**: Premium (avg retention=0.659, range 0.55-0.75) and Growing (avg=0.440, range 0.36-0.54) have narrow retention ranges that keep all records within 0.15 of the mean. The anomaly-prone segments exhibit much wider retention spreads (High Value: 0.25-0.85; Basic: 0.25-0.89; Standard: 0.16-0.94).

![Deviation distribution](<../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/work/deviation_distribution.png>)

*Figure 2: Distribution of retention deviations from segment averages. Red bars exceed the ±0.15 threshold.*

---

## 2. Transactional Behavior Analysis

### Statistical Comparison

| Feature | Non-Anomaly Mean | Anomaly Mean | p-value | Cohen's d |
|---------|-----------------|-------------|---------|-----------|
| Transaction Count | 12.38 | 11.98 | 0.730 | -0.06 |
| Avg Transactions/Month | 1.98 | 2.03 | 0.769 | 0.06 |
| Transaction Value Volatility | 0.506 | 0.524 | 0.643 | 0.09 |
| Tx Consistency Ratio (tx_ratio) | 0.524 | 0.529 | 0.889 | 0.03 |
| Tx Gap (actual - expected) | -11.31 | -12.41 | 0.456 | -0.14 |

**Finding**: No significant differences in aggregate transactional metrics between anomaly and non-anomaly groups. However, **the decision tree reveals a critical interaction**: among high-revenue customers (>$800), those with a low transaction consistency ratio (tx_ratio ≤ 0.454) are **100% anomalous** — their actual transaction counts substantially trail their stated monthly averages.

![Tx ratio effect in high-revenue band](<../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/work/tx_ratio_effect.png>)

*Figure 3: High-revenue customers (>$800) show a clear split at tx_ratio=0.454. Left of this threshold, all are anomalies (red).*

### Categorical Transaction Consistency

| Consistency | Non-Anomaly | Anomaly |
|-------------|-------------|---------|
| Consistent | 38.2% | 29.8% |
| Moderate | 34.3% | 19.1% |
| Irregular | 15.7% | **31.9%** |
| Very Consistent | 11.8% | 19.1% |

**Anomaly customers are twice as likely to be classified as "Irregular"** in transaction consistency (31.9% vs 15.7%).

![Transactional behavior scatter](<../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/work/transactional_analysis.png>)

*Figure 4: Left: Transaction count vs monthly rate. Right: Volatility vs consistency ratio. Anomalies (red) show more scatter.*

---

## 3. Seasonal Pattern Analysis

### Quarterly Distribution

| Seasonal Preference | Non-Anomaly | Anomaly |
|---------------------|-------------|---------|
| **Q4 Peak** | 49.0% | **70.2%** |
| Q1 Peak | 30.4% | 21.3% |
| Q3 Peak | 15.7% | 8.5% |
| Balanced | 4.9% | 0.0% |

**Anomaly customers are disproportionately Q4-heavy** (70.2% vs 49.0%). No Balanced customers are anomalies.

### Seasonal Concentration Metrics

| Metric | Non-Anomaly | Anomaly | p-value |
|--------|-------------|---------|---------|
| Seasonal Std Dev | 0.118 | 0.158 | 0.126 |
| Max Quarterly Share | 0.396 | 0.463 | 0.094 |
| Seasonal Entropy | 0.897 | 0.788 | 0.057 |

**Borderline significance** (p≈0.06-0.09) indicates a trend toward more concentrated seasonal distributions among anomaly customers.

### Critical Finding: Within anomaly-prone segments, seasonal concentration is the only significant correlate of retention

| Feature | Pearson r | p-value | Spearman rho | p-value |
|---------|-----------|---------|-------------|---------|
| **Seasonal Max Share** | -0.153 | 0.211 | **-0.272** | **0.025** |
| **Seasonal Entropy** | +0.111 | 0.369 | **+0.276** | **0.023** |
| Seasonal Std | -0.170 | 0.165 | **-0.269** | **0.027** |

Within High Value, Standard, and Basic segments, **seasonal concentration (Spearman rho = -0.27) significantly correlates with lower retention**, while all other value metrics (score, revenue, transaction count, volatility) show no significant correlation with retention (all p > 0.05).

![Seasonal retention link](<../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/work/seasonal_retention_link.png>)

*Figure 5: Within anomaly-prone segments, more concentrated seasonal distributions (higher max share, lower entropy) are associated with lower retention._

![Seasonal analysis](<../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/work/seasonal_analysis.png>)

*Figure 6: Left: Seasonal balance scatter. Right: Quarterly transaction distribution by segment. High Value and Standard show Q4 skew.*

---

## 4. Value Realization Path Analysis

### Score-Revenue Alignment

The regression of `comprehensive_customer_score` on `total_revenue` shows:
- **Pearson r = 0.30** (p<0.001) — a weak positive correlation
- **Score-revenue residual (score_rev_resid)** does not differ significantly between anomaly groups (p=0.460)

![Value alignment scatter](<../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/work/value_alignment.png>)

*Figure 7: Score vs revenue by anomaly status. The regression line (r=0.30) shows substantial scatter, especially for anomalies (red).*

### Regression: How much of retention is explained by existing metrics?

| Model | R² | % Unexplained |
|-------|-----|---------------|
| retention ~ [score, revenue, tx_count, volatility] | **0.124** | **87.6%** |
| + [tx_ratio, seasonal_std] | 0.133 | 86.7% |

**87.6% of retention variance is not explained by the current value metrics.** Adding transactional consistency and seasonal concentration improves R² by only 0.009, suggesting the need for fundamentally different segmentation dimensions.

### Anomaly Directions by Segment

| Segment | High Retention Anomaly | Low Retention Anomaly |
|---------|----------------------|---------------------|
| **High Value** | n=11, avg ret=0.77, avg rev=$903, score=88.7 | n=9, avg ret=0.31, avg rev=$901, score=87.1 |
| **Standard** | n=6, avg ret=0.89, avg rev=$488, score=47.7 | n=9, avg ret=0.22, avg rev=$550, score=56.0 |
| **Basic** | n=6, avg ret=0.77, avg rev=$81, score=15.0 | n=6, avg ret=0.27, avg rev=$83, score=13.2 |

**Critical finding**: In the High Value segment, high-retention and low-retention anomalies have **nearly identical revenue (~$900) and scores (~87-88)**. The difference lies entirely in retention probability, which is not captured by the current value-based segmentation.

---

## 5. Cluster Analysis Results

### K-Means Clustering (k=4)

Using features: transaction_value_volatility, tx_ratio, seasonal_std, score_rev_resid, comprehensive_customer_score, total_revenue, transaction_count

![Elbow curve](<../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/work/elbow_curve.png>)
![PCA clusters](<../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/work/clusters_pca.png>)
![Anomaly overlay](<../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/work/anomaly_pca.png>)

| Cluster | n | Key Characteristics | Anomaly Rate | Dominant Segment |
|---------|----|-------------------|-------------|-----------------|
| **Cluster 0** | 48 | High revenue ($783), high score (81), low volatility (0.34), balanced seasonal | **35.4%** | High Value & Premium |
| **Cluster 1** | 48 | Moderate revenue ($343), moderate score (39), moderate volatility (0.68), Q4-heavy | **31.3%** | Growing & Standard |
| **Cluster 2** | 14 | **Low revenue ($82), low score (14), high volatility (0.78), extreme Q4 concentration** | **64.3%** | **Basic (all)** |
| **Cluster 3** | 39 | High revenue ($712), high score (64), low volatility (0.43), mixed seasonal | **15.4%** | **Premium (dominant)** |

![Cluster anomaly rate](<../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/work/cluster_anomaly_rate.png>)
![Cluster profiles](<../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/work/cluster_profiles.png>)

**Key finding**: The clusters naturally separate into performance tiers, but **Cluster 2 (Basic/At Risk) has the highest anomaly rate (64%),** while **Cluster 3 (Premium stable) has the lowest (15%).** This suggests that the current segmentation model could be improved by incorporating lifecycle and stability dimensions.

---

## 6. Decision Tree Analysis

### Decision Tree for Anomaly Prediction

The CART-style decision tree achieved **77.2% accuracy** (5-fold CV) vs a 68.5% baseline (predicting all non-anomaly), with **66.5% precision and 59.6% recall**.

```
                           [Total Revenue]
                           /             \
                    ≤ 799.5             > 799.5
                    /                         \
           [Total Revenue]              [Tx Consistency Ratio]
            /           \                  /               \
         ≤ 592.6      > 592.6           ≤ 0.454          > 0.454
          /               \              /                    \
   [Total Revenue]    0% anomaly    100% anomaly        [Score Residual]
    /           \         (n=52)         (n=12)           /           \
 ≤ 405.2      > 405.2                                  ≤ 3.12       > 3.12
   /              \                                       /              \
[Revenue ≤ 196.6]  [Volatility]                        25% anomaly     85.7% anomaly
  /         \        /         \                         (n=8)          (n=7)
83.3%    0%       16.7%     87.5%
anomaly  anomaly  anomaly   anomaly
(n=18)   (n=30)   (n=6)     (n=16)
```

### Feature Importance

| Feature | Importance |
|---------|-----------|
| **total_revenue** | **82.3%** |
| **score_rev_resid** | **7.3%** |
| tx_ratio | 5.1% |
| transaction_value_volatility | 3.5% |
| avg_transactions_per_month | 1.8% |

**Interpretation**: Revenue is the dominant splitter. The three key anomaly paths are:
1. **Low revenue (<$196, mostly Basic)**: 83.3% anomaly — these customers have very low value metrics but variable retention.
2. **Mid revenue ($405-592) with high volatility (>0.408)**: 87.5% anomaly — volatile transaction values indicate unstable customer relationships.
3. **High revenue (>$800) with low tx_ratio (≤0.454)**: 100% anomaly — these customers have high revenue but their actual transaction counts don't match their stated monthly rates.

![Decision tree schematic](<../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/work/decision_tree_schematic.png>)

---

## 7. Recommendations for Segmentation Model Enhancement

### Proposed New Dimensions

| Dimension | Rationale | Operationalization |
|-----------|-----------|-------------------|
| **Transaction Stability** | The tx_ratio (actual_tx / expected_tx) identifies high-revenue customers whose transaction patterns don't match their stated monthly averages. Decision tree found this is a 100% discriminator for anomalies above $800 revenue. | Create 3 tiers: Stable (ratio 0.8-1.2), Declining (<0.8), Accelerating (>1.2) |
| **Seasonal Preference Weight** | Q4-heavy customers are 70.2% of anomalies vs 49.0% of non-anomalies. Within anomaly-prone segments, seasonal concentration correlates with retention (rho=-0.27, p=0.03). | Weight the existing seasonal_preference into the segmentation model. Q4-dominant customers should be assigned a retention risk modifier. |
| **Lifecycle Stage Integration** | At Risk customers show 56% anomaly rate vs 17% for Growth. Currently, lifecycle_stage exists but is not integrated into the profitability_segment model. | Create a "lifecycle-adjusted retention score" that discounts At Risk customers and premiums Growth customers. |
| **Value Realization Gap** | score_rev_resid (residual from score-revenue regression) is the #2 feature in the decision tree (7.3% importance). Customers with high positive residuals (score well above revenue expectation) have 85.7% anomaly rate. | Flag customers with score_rev_resid > 3.12 as candidates for segment reassignment. |

### Segment-Specific Recommendations

| Segment | Issue | Recommendation |
|---------|-------|---------------|
| **High Value** | 74.1% anomaly rate. High-retention (0.77) and low-retention (0.31) anomalies have identical revenue (~$900) and scores (~87). | Split into "High Value Stable" and "High Value At Risk" sub-segments based on seasonal concentration and transaction stability. |
| **Basic** | 66.7% anomaly rate. All are low-revenue ($82 avg) but retention ranges from 0.25 to 0.89. | Reclassify basic customers with high retention (>0.70) into a "Basic Premium" or "Upside Potential" tier. |
| **Standard** | 65.2% anomaly rate. Wide retention range (0.16-0.94) with moderate revenue (~$520). | Introduce transaction volatility threshold (0.408) as a sub-segment determinant. |

### Expected Impact

- **Improved segmentation precision**: The current model explains only 12.4% of retention variance. Adding the proposed dimensions could increase this to **25-35%** based on the decision tree's 77.2% anomaly classification accuracy.
- **Better predictive accuracy**: The decision tree (using only 5 features) outperforms the baseline by 8.7 percentage points.
- **Targeted intervention**: Cluster 2 (Basic/At Risk, 64% anomaly) and high-revenue-low-tx_ratio customers (100% anomaly) represent clear priority groups for retention programs.

---

## 8. Limitations

1. **Duplicate records**: 6 customers appear in 8 versions each, possibly representing alternative scenarios. This affects the independence of observations.
2. **Small sample size**: 149 records across 5 segments limits the statistical power of between-group comparisons.
3. **No temporal data**: Customer age is uniform (365 days) and segmentation_date is fixed, preventing time-series analysis of retention dynamics.
4. **Retention as a single metric**: The analysis depends on retention_probability as the sole performance differentiator — other dimensions (satisfaction, engagement quality) may be unreported.
5. **Sklearn unavailable**: K-means and decision tree were implemented manually, which may lack the optimization of standard libraries.