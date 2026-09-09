<!-- Reading copy: local artifact links normalized. Original answer is preserved at ../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/answer.md -->

# Email Campaign Performance Analysis: Timing × Subject Interaction Effects

## Executive Summary

This report analyzes 184 email campaigns (184 unique campaign IDs, 1192 persons) from a Klaviyo dataset, examining how **send timing** and **subject copy keyword** interact to influence open rate, click-to-open rate (CTOR), GMV, and person-level active retention. The analysis was de-noised by excluding the top/bottom 2% of `count_received_email` outliers (8 records removed), and controlled for audience size (`total_count_unique_people`), archival status (`is_archived`), and send variation (`variation_id`).

---

## 1. Methodology

### Feature Engineering
- **Timing**: Extracted from `campaign_name` using pattern matching — 6 categories: weekday_morning, weekday_afternoon, weekday_evening, weekend_morning, weekend_evening, pre_holiday_afternoon.
- **Subject keyword**: Extracted from `SUBJECT` — 3 groups: discount (限时折扣), new_product (新品上新), storytelling (品牌故事).
- **De-noising**: Excluded 8 records outside the 2nd–98th percentile of `count_received_email`.
- **Controls**: `is_archived` (archived vs non-archived), `variation_id` (single/variant_a/variant_b), `total_count_unique_people` (audience size).

### Statistical Methods
- One-way ANOVA for main effects (timing, subject group, is_archived, variation_id)
- Linear regression for audience size covariate control
- Spearman rank correlation for retention analysis
- Pivot-table interaction analysis for timing × subject combinations

---

## 2. Key Findings

### 2.1 Timing Effect (ANOVA: F=21.76, p<0.0001)

| Timing | Open Rate | CTOR | GMV per Person | N |
|--------|-----------|------|----------------|----|
| **Pre-Holiday Afternoon** | **0.365** | **0.147** | **$1.20** | 26 |
| Weekend Morning | 0.320 | 0.139 | $0.68 | 30 |
| Weekend Evening | 0.305 | 0.134 | $0.67 | 30 |
| Weekday Morning | 0.307 | 0.138 | $0.57 | 31 |
| Weekday Evening | 0.302 | 0.137 | $0.73 | 29 |
| Weekday Afternoon | 0.281 | 0.127 | $0.55 | 30 |

**Pre-holiday afternoon campaigns outperform all others by a large margin** — open rate 16.3% higher than the average, CTOR 7.5% higher, and GMV per person 78% higher.

### 2.2 Subject Keyword Effect (ANOVA: F=87.18, p<0.0001)

| Subject Group | Open Rate | CTOR | GMV per Person | N |
|---------------|-----------|------|----------------|----|
| **Discount** | **0.340** | **0.148** | **$0.93** | 59 |
| New Product | 0.324 | 0.140 | $0.83 | 59 |
| Storytelling | 0.276 | 0.122 | $0.44 | 58 |

**Discount subject lines consistently outperform**, with open rates 23.2% higher than storytelling and 4.9% higher than new product. Storytelling campaigns underperform across all metrics.

### 2.3 Timing × Subject Interaction

The combined heatmap reveals strong interaction effects:

| Timing | Discount | New Product | Storytelling |
|--------|----------|-------------|--------------|
| **Pre-Holiday Afternoon** | **0.402 / 0.161** | 0.376 / 0.152 | 0.319 / 0.129 |
| Weekend Morning | 0.346 / 0.147 | 0.320 / 0.139 | 0.294 / 0.131 |
| Weekend Evening | 0.342 / 0.147 | 0.315 / 0.139 | 0.258 / 0.116 |
| Weekday Evening | 0.327 / 0.151 | 0.321 / 0.142 | 0.259 / 0.119 |
| Weekday Morning | 0.321 / 0.146 | 0.315 / 0.138 | 0.284 / 0.130 |
| Weekday Afternoon | 0.307 / 0.140 | 0.300 / 0.132 | **0.238 / 0.108** |

*Values shown as: Open Rate / CTOR*

**Best combination**: Pre-holiday afternoon × Discount (0.402 open rate, 0.161 CTOR, $1.50 GMV/person)  
**Worst combination**: Weekday afternoon × Storytelling (0.238 open rate, 0.108 CTOR, $0.23 GMV/person)

### 2.4 Archived vs Non-Archived (ANOVA: F=8.78, p=0.0035)

| Status | Open Rate | CTOR | GMV per Person |
|--------|-----------|------|----------------|
| Archived | 0.330 | 0.148 | $0.83 |
| Non-archived | 0.309 | 0.135 | $0.69 |

Archived campaigns show slightly higher performance. However, **archived campaigns are only discount-type** in specific timing slots (weekday morning/evening, weekend evening), so this effect is confounded with subject group — archived campaigns all use discount copy, which inherently performs better.

### 2.5 Variation ID (ANOVA: F=0.27, p=0.767)

| Variation | Open Rate | CTOR | GMV per Person |
|-----------|-----------|------|----------------|
| Single | 0.313 | 0.137 | $0.73 |
| Variant A | 0.314 | 0.137 | $0.72 |
| Variant B | 0.309 | 0.136 | $0.69 |

**No significant difference** between single-send and A/B test variants. Variation ID does not independently affect campaign performance.

### 2.6 Audience Size Control

Linear regression of open rate on audience size (per subject group):

| Subject Group | Slope | r | p-value |
|---------------|-------|---|---------|
| Discount | +7.7e-6 | 0.33 | 0.011 |
| New Product | +8.0e-6 | 0.42 | 0.001 |
| Storytelling | +6.6e-6 | 0.30 | 0.022 |

A weak positive correlation exists but is **largely driven by pre-holiday campaigns having both larger audiences and higher open rates**. The effect size is negligible (open rate increases by ~0.008 per 1,000 additional recipients).

---

## 3. Person-Level Retention Analysis

### 3.1 Retention Patterns

| Metric | Mean | Std | Min | Max |
|--------|------|-----|-----|-----|
| Retention Rate (Week) | 0.549 | 0.132 | 0.333 | 0.792 |
| Retention Rate (Month) | 0.569 | 0.126 | 0.364 | 0.833 |
| Person Open Rate | 0.399 | 0.099 | 0.200 | 0.560 |

### 3.2 Retention Drivers

**Strongest correlates** (Spearman rank correlation with weekly retention):

| Factor | Correlation | p-value |
|--------|-------------|---------|
| **Email Open Rate** | **+0.955** | <0.0001 |
| **Count of Received Emails** | **−0.964** | <0.0001 |
| Count of Placed Orders | +0.797 | <0.0001 |
| Active Days | +0.709 | <0.0001 |

**Key insight**: Higher email volume is strongly associated with LOWER retention, while higher open rate is strongly associated with HIGHER retention. This suggests **email fatigue** — recipients who receive too many emails disengage and have lower retention.

### 3.3 Retention by Timezone (ANOVA: F=11.41, p<0.0001)

| Timezone | N | Retention (Week) | Open Rate | Emails Received |
|----------|---|------------------|-----------|-----------------|
| Asia/Singapore | 149 | 0.586 | 0.419 | 99 |
| Asia/Shanghai | 894 | 0.549 | 0.397 | 108 |
| America/Los Angeles | 149 | 0.514 | 0.377 | 117 |

Singapore-based recipients show highest retention and open rates with lowest email volume. LA-based recipients show the opposite pattern.

### 3.4 Retention by Email Volume Terciles

| Volume Group | N | Retention (Week) | Open Rate | Orders |
|--------------|---|------------------|-----------|--------|
| Low (<85) | 402 | **0.699** | **0.488** | 1.71 |
| Medium (85–130) | 397 | 0.545 | 0.398 | 1.08 |
| High (>130) | 393 | 0.401 | 0.304 | 0.62 |

**Strong inverse relationship**: lowest-volume recipients have 74% higher retention than highest-volume recipients.

---

## 4. Actionable Recommendations

### 4.1 Timing Strategy

1. **Prioritize pre-holiday afternoon sends** for maximum impact — this timing window consistently delivers 16–19% higher open rates and 78% higher GMV per person compared to average.
2. **Avoid weekday afternoon sends** for storytelling campaigns — this is the worst-performing combination (0.238 open rate, 0.108 CTOR).
3. **Weekend mornings are the second-best window** — use for discount and new product campaigns when pre-holiday slots are unavailable.

### 4.2 Subject Copy Strategy

1. **Lead with discount messaging** — discount subject lines outperform new product by 4.9% and storytelling by 23.2% in open rate. The effect is amplified during pre-holiday periods.
2. **Reserve storytelling for high-engagement audiences** — storytelling campaigns underperform overall but may serve brand-building purposes for loyal segments. Consider sending to high-open-rate segments only.
3. **Pair new product launches with weekend morning timing** — this combination achieves 0.320 open rate, close to discount performance.

### 4.3 Retention-Risk Mitigation

1. **Control email frequency** — the strong negative correlation (r=−0.964) between email volume and retention indicates that excessive emailing drives disengagement. Cap sends for high-volume recipients.
2. **Monitor open rate as a leading indicator** — declining open rate strongly predicts retention decline (r=+0.955). Set alerts for segment-level open rate drops.
3. **Segment by timezone** — Singapore recipients show highest retention. Consider timezone-aligned send schedules to optimize engagement.

### 4.4 Campaign Management

1. **Variation ID (A/B testing) has no significant impact** — resources spent on A/B test variants may be better allocated to timing optimization and audience segmentation.
2. **Archived status does not independently drive performance** — the higher metrics for archived campaigns are confounded by their discount-only subject copy. Do not treat archival as a performance lever.

---

## 5. Potential Risks

1. **Email fatigue** — the strongest signal in the data. Pushing higher email volume (especially discount-heavy) risks long-term retention damage. The pre-holiday discount × high volume combination may boost short-term revenue at the cost of long-term retention.
2. **Storytelling campaigns are systematically underperforming** — if brand storytelling is a strategic priority, the current execution needs revision (different timing, smaller segments, or improved copy).
3. **Pre-holiday effect may be seasonal/limited** — the pre-holiday window is inherently constrained (limited number of dates). Over-reliance could lead to campaign timing bottlenecks.
4. **Audience size correlation is weak and confounded** — larger audiences do not inherently drive better performance; the effect is driven by pre-holiday campaigns having larger lists. Scaling audience size without timing optimization will not replicate the effect.
5. **Synthetic data patterns** — the high consistency of metrics within timing × subject cells (e.g., all pre-holiday discount campaigns show exactly 0.402 open rate) suggests the data may be partially synthetic. Real-world variability may be higher.

---

## 6. Limitations

- No direct campaign-person join key exists, limiting causal attribution of campaign-level effects to person-level retention.
- The dataset spans 2023-01 to 2024-07; seasonality effects beyond the observed pre-holiday pattern cannot be fully assessed.
- De-noising removed 8 records (4.3%); results may not generalize to extreme audience sizes.
- All campaigns are in Chinese-language markets (Asia/Shanghai, Asia/Singapore); findings may not generalize to other markets.
- The high consistency of metrics within timing × subject cells may indicate synthetic or pre-computed data, warranting cautious interpretation.

---

## Figures

| Figure | Description |
|--------|-------------|
| ![Heatmap: Open Rate](<../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/work/heatmap_open_rate.png>) | Open rate by timing × subject group |
| ![Heatmap: CTOR](<../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/work/heatmap_ctor.png>) | Click-to-open rate by timing × subject group |
| ![Heatmap: GMV per Person](<../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/work/heatmap_gmv_per_person.png>) | GMV per person by timing × subject group |
| ![Combined Heatmaps](<../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/work/combined_heatmaps.png>) | All three metrics side by side |
| ![Timing Performance](<../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/work/bar_timing_combined.png>) | Campaign performance by send timing |
| ![Subject Performance](<../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/work/bar_subject_english.png>) | Campaign performance by subject keyword |
| ![Audience vs Open](<../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/work/scatter_audience_vs_open.png>) | Open rate vs audience size (colored by subject) |
| ![Retention by Timezone](<../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/work/boxplot_retention_by_tz.png>) | Retention rate distribution by timezone |
| ![Retention vs Engagement](<../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/work/scatter_retention_engagement.png>) | Retention vs email volume and open rate |