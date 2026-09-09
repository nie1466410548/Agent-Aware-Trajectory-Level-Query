# Cohort Analysis Report: High-Engagement Customers with Extended Conversion Cycles

## Executive Summary

This report analyzes a cohort of **850 customers** (out of 4,734 total) who exhibit specific conversion behaviors: marketing-to-sales cycles of 10–20 days, sales-to-support cycles exceeding 30 days, and above-average composite engagement scores. These customers represent a distinctive segment with higher lifetime value, moderate health scores, and diverse multi-platform engagement patterns.

---

## 1. Cohort Definition & Key Metrics

**Definition Criteria:**
- `marketing_to_sales_days` BETWEEN 10 AND 20
- `sales_to_support_days` > 30
- `composite_engagement_score` > overall average (8.9995)

**Cohort Size: 850 customers (18.0% of customer base)**

### RFM Dimension Averages

| RFM Dimension | Cohort Average | Scale |
|---------------|---------------|-------|
| Recency Score | 2.96 | 1–5 |
| Frequency Score | 2.96 | 1–5 |
| Monetary Score | 2.96 | 1–5 |
| Composite Engagement Score | 12.82 | — |

### RFM Segment Distribution

| RFM Segment | Count | % | Avg LTV | Avg Health |
|-------------|-------|---|---------|------------|
| At Risk | 238 | 28.0% | $12,629 | 72.1 |
| Champions | 147 | 17.3% | $9,988 | 72.1 |
| Loyal Customers | 129 | 15.2% | $9,848 | 71.1 |
| New Customers | 118 | 13.9% | $10,950 | 71.4 |
| Customers Needing Attention | 115 | 13.5% | $11,284 | 73.8 |
| Promising | 56 | 6.6% | $12,399 | 71.1 |
| Potential Loyalists | 47 | 5.5% | $13,900 | 71.1 |

The cohort spans all RFM segments, with a notable concentration (28%) in the "At Risk" category despite their above-average engagement scores. This suggests that high engagement does not necessarily translate to optimal recency-frequency-monetary performance.

---

## 2. Lifetime Value Analysis (by Customer Tier)

The cohort consistently shows **higher estimated LTV** compared to non-cohort customers in the same tier:

| Customer Tier | Cohort Count | Cohort Avg LTV | Non-Cohort Tier Avg LTV | LTV Difference |
|---------------|-------------|----------------|------------------------|----------------|
| Basic | 238 | $1,612.54 | $998.87 | **+$613.68** |
| Bronze | 169 | $4,467.06 | $3,193.73 | **+$1,273.33** |
| Gold | 141 | $15,947.01 | $13,718.66 | **+$2,228.35** |
| Platinum | 145 | $33,540.40 | $32,518.10 | **+$1,022.30** |
| Silver | 157 | $9,116.05 | $5,444.98 | **+$3,671.08** |

**Overall average LTV uplift: +$1,647.10** per customer relative to same-tier peers.

![LTV by Tier](fig3_ltv_by_tier.png)

---

## 3. Primary Engagement Channel Distribution

| Channel | Count | Percentage |
|---------|-------|-----------|
| Webinar | 157 | 18.47% |
| Event | 143 | 16.82% |
| Paid Search | 140 | 16.47% |
| Organic Search | 139 | 16.35% |
| Email | 137 | 16.12% |
| Social Media | 134 | 15.76% |

The distribution is remarkably even across channels, with Webinar slightly leading. No single channel dominates, suggesting this cohort is multi-channel engaged.

---

## 4. Zendesk Active Status

| Status | Count | Percentage |
|--------|-------|-----------|
| Not Active (0) | 627 | 73.76% |
| Active (1) | 223 | 26.24% |

Approximately one-quarter of the cohort has active Zendesk support tickets, indicating ongoing support engagement.

---

## 5. Multi-Platform Engagement Patterns & Health Score Impact

### Platform Pattern Distribution

![Platform Pattern Distribution](fig5_platform_dist.png)

The cohort is evenly distributed across all 8 platform engagement combinations:

| Platform Pattern | Count | % | Avg Health Score | Avg LTV |
|-----------------|-------|---|-----------------|---------|
| Stripe+Zendesk | 118 | 13.9% | 70.36 | $11,796 |
| Marketo+Stripe | 116 | 13.6% | 70.98 | $10,385 |
| Marketo+Zendesk | 113 | 13.3% | 71.88 | $10,935 |
| All 3 Platforms | 112 | 13.2% | **74.57** | $10,506 |
| Marketo Only | 110 | 12.9% | 70.77 | $10,807 |
| None | 98 | 11.5% | 71.21 | $12,889 |
| Zendesk Only | 92 | 10.8% | **74.40** | $12,495 |
| Stripe Only | 91 | 10.7% | 71.80 | $11,774 |

**Statistical Analysis (ANOVA):** F(7, 842) = 1.37, p = 0.215 — No statistically significant difference in health scores across platform patterns at α = 0.05.

**Key observation:** While not statistically significant, customers on **all three platforms** and **Zendesk-only** customers show the highest average health scores (74.57 and 74.40 respectively), suggesting that Zendesk engagement correlates with perceived health.

![Health Score by Platform Pattern](fig1_platform_health.png)

### Correlation Analysis

| Variable | Correlation with Health Score |
|----------|------------------------------|
| Composite Engagement Score | **0.433** (moderate positive) |
| Funnel LTV | 0.038 (weak) |
| Cross-Platform Consistency | -0.066 (weak negative) |
| Activity Efficiency | -0.072 (weak negative) |
| Days Since Last Activity | -0.006 (negligible) |
| Churn Probability | 0.032 (negligible) |
| Investment Priority Score | -0.032 (negligible) |

The strongest predictor of health score within the cohort is the **composite engagement score** (r = 0.43), while LTV and other metrics show minimal correlation.

---

## 6. Customer Segment & Lifecycle Stage Distribution

### Customer Segment

| Segment | Count | % |
|---------|-------|---|
| Enterprise | 340 | 40.0% |
| Mid-Market | 259 | 30.5% |
| SMB | 123 | 14.5% |
| Startup | 112 | 13.2% |
| At Risk | 13 | 1.5% |
| Hibernating | 3 | 0.4% |

### Lifecycle Stage

| Stage | Count | % |
|-------|-------|---|
| Opportunity | 149 | 17.5% |
| Lead | 147 | 17.3% |
| Customer | 140 | 16.5% |
| SQL | 138 | 16.2% |
| Champion | 133 | 15.7% |
| MQL | 127 | 14.9% |
| Dormant | 16 | 1.9% |

The cohort is dominated by **Enterprise (40%)** and **Mid-Market (30.5%)** segments, with a relatively even distribution across lifecycle stages from Lead through Champion.

![Segment × Lifecycle Heatmap](fig7_segment_lifecycle.png)

---

## 7. Geographical Distribution

**Note:** The address table (`customer360__address`) uses `customer360_id` identifiers that could not be deterministically mapped to the customer tables (primary_email, marketo_lead_id, etc.) via known hash algorithms. The synthetic data generation process appears to use non-reversible identifiers for the address table. Therefore, country/state analysis at the cohort level is not available.

**Overall address table geography (all customers):** The top country codes represented include France, British Virgin Islands, Malawi, Sweden, Niger, and South Africa. Top states include Haut-Rhin, Brod-Posavina, Toledo, South Australia, Mato Grosso, and Michigan.

---

## 8. Risk & Engagement Velocity Framework

### Risk Level Distribution

| Risk Level | Count | % | Avg Health | Avg LTV |
|------------|-------|---|-----------|---------|
| Critical | 188 | 22.1% | 72.78 | $11,755 |
| Low | 175 | 20.6% | 70.99 | $10,586 |
| Very Low | 162 | 19.1% | 73.28 | $11,592 |
| Medium | 155 | 18.2% | 72.64 | $11,857 |
| High | 154 | 18.1% | 70.77 | $11,425 |
| High Activity Risk | 16 | 1.9% | 63.55 | $9,010 |

### Engagement Velocity Distribution

| Velocity | Count | % | Avg Health | Avg LTV |
|----------|-------|---|-----------|---------|
| Accelerating | 214 | 25.2% | 72.22 | $10,416 |
| Stable | 213 | 25.1% | 72.56 | $12,799 |
| Declining | 211 | 24.8% | 71.42 | $10,176 |
| Volatile | 196 | 23.1% | 72.22 | $12,425 |
| Stagnant | 16 | 1.9% | 63.55 | $9,010 |

### Customer Value Assessment & Risk Identification Framework

Based on the analysis of `activity_risk_level` and `engagement_velocity`, we propose the following multi-dimensional framework:

#### Risk-Velocity Health Score Matrix

![Risk × Velocity Heatmap](fig2_risk_velocity_heatmap.png)

**Key Findings:**
- **Stable velocity + any risk level** yields the highest health scores (72–74)
- **Stagnant velocity + High Activity Risk** is the worst-performing combination (health score 63.6, lowest LTV at $9,010)
- **Critical risk + Volatile velocity** shows high LTV ($13,027) but elevated churn probability (0.538)
- **Very Low risk + Volatile velocity** achieves the highest health score (74.6)

#### Risk Category Distribution

![Risk Category](fig4_risk_category.png)

The cohort's risk categories are distributed as: Critical Risk (34.2%), High Risk (24.9%), Medium Risk (23.4%), and Low Risk (17.5%).

#### Proposed Value-Risk Assessment Matrix

| Segment | Risk Level | Velocity | Avg Health | Avg LTV | Churn Prob | Recommended Action |
|---------|-----------|----------|-----------|---------|-----------|-------------------|
| **High Value / Stable** | Any | Stable | 72.6 | $12,799 | 0.50 | Maintain & upsell |
| **High Value / Volatile** | Critical/High | Volatile | 71.3 | $12,720 | 0.55 | Intervention needed |
| **Growth Potential** | Low/Very Low | Accelerating | 73.1 | $9,766 | 0.47 | Nurture & accelerate |
| **At Risk / Declining** | Critical/High | Declining | 71.4 | $8,776 | 0.52 | Retention campaign |
| **Critical Alert** | High Activity Risk | Stagnant | 63.6 | $9,010 | 0.63 | Immediate outreach |

#### Risk Identification Thresholds

1. **High Priority Alerts (Red):**
   - `activity_risk_level` = "High Activity Risk" AND `engagement_velocity` = "Stagnant"
   - Health score < 65 and LTV > $10,000 (high-value customers at risk)
   - Churn probability > 0.60

2. **Medium Priority (Amber):**
   - `engagement_velocity` = "Declining" and `activity_risk_level` in ("High", "Critical")
   - Cross-platform consistency < 0.70
   - Days since last activity > 90

3. **Low Priority (Green):**
   - `activity_risk_level` in ("Low", "Very Low")
   - `engagement_velocity` in ("Accelerating", "Stable")
   - Health score > 70

#### Statistical Validation

- **ANOVA (Risk Level → Health Score):** F(5, 844) = 1.99, p = 0.078 (marginally significant)
- **ANOVA (Velocity → Health Score):** F(4, 845) = 1.61, p = 0.171 (not significant)
- **ANOVA (Platform Pattern → Health Score):** F(7, 842) = 1.37, p = 0.215 (not significant)

The composite engagement score (r = 0.43) is the strongest individual predictor of health score within the cohort.

---

## 9. Limitations

1. **Address table join:** The `customer360__address` table uses opaque `customer360_id` identifiers that could not be mapped to customer records through known hash functions, preventing cohort-specific geographical analysis.
2. **Synthetic data:** Country and state names in the address table contain synthetic text phrases alongside real locations, limiting geographic interpretation.
3. **Multiple records per customer:** The main tables contain multiple rows per customer (different analysis timestamps). The analysis uses the most recent record per email, which may not capture temporal dynamics.
4. **Statistical power:** The cohort size of 850 provides reasonable estimates, but subgroup analyses (e.g., specific risk-velocity combinations) involve smaller sample sizes.

---

## 10. Conclusions

1. **The cohort of 850 customers** (18% of the base) with moderate marketing-to-sales cycles (10–20 days) and extended sales-to-support periods (>30 days) represents a high-value segment, with LTV premiums of $613–$3,671 across customer tiers.

2. **Multi-platform engagement** is evenly distributed, with all three platforms (Marketo, Stripe, Zendesk) present in 13.2% of the cohort. While not statistically significant, all-three-platform users show the highest average health scores.

3. **The Risk-Velocity Framework** effectively identifies intervention priorities: customers with "Stagnant" velocity and "High Activity Risk" are the most vulnerable (health score 63.6, churn probability 0.63), while "Stable" velocity mitigates risk regardless of the risk level assigned.

4. **Enterprise and Mid-Market segments** dominate the cohort (70.5%), and the lifecycle stage distribution is evenly spread, indicating this cohort spans the full customer journey from Lead to Champion.

5. **Recommended strategic actions:** Focus retention efforts on the "Critical Risk + Declining" segment (avg LTV $9,232), accelerate the "Low Risk + Accelerating" segment (avg LTV $7,792, health 73.5), and monitor the "High Activity Risk + Stagnant" segment as a top priority for immediate intervention.