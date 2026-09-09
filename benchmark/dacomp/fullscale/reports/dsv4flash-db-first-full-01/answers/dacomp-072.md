<!-- Reading copy: local artifact links normalized. Original answer is preserved at ../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/answer.md -->

# Hiring Manager Performance Evaluation Report

## Executive Summary

A composite efficiency score was calculated for all 235 hiring managers in the `lever__hiring_manager_scorecard` table (all had `total_requisitions_owned >= 5`, making them eligible). The score is based on four weighted dimensions:

| Dimension | Weight | Condition | Score Contribution |
|---|---|---|---|
| Candidate Hire Rate | 30% | `candidate_hire_rate × 100` (continuous 0–100) | Continuous |
| Avg Days to Hire < 45 | 25% | Boolean: 100 if met, 0 otherwise | 0 or 100 |
| Avg Candidate Experience > 3.5 | 25% | Boolean: 100 if met, 0 otherwise | 0 or 100 |
| Feedback Completion Rate > 85% | 20% | Boolean: 100 if met, 0 otherwise | 0 or 100 |

**Final Score** = 0.30 × (hire_rate × 100) + 0.25 × (days_ok) + 0.25 × (exp_ok) + 0.20 × (feedback_ok)

**Tier thresholds:** Excellent (≥80), Good (60–80), Needs Improvement (<60).

---

## Overall Results

| Metric | Value |
|---|---|
| Total Eligible Managers | 235 |
| Min Composite Score | 6.94 |
| Max Composite Score | 89.39 |
| Mean Composite Score | 40.30 |
| Standard Deviation | 21.04 |

### Tier Distribution

| Tier | Count | Percentage | Score Range | Avg Score |
|---|---|---|---|---|
| **Excellent** | 13 | 5.5% | 80.19 – 89.39 | 84.57 |
| **Good** | 37 | 15.7% | 60.08 – 79.86 | 64.35 |
| **Needs Improvement** | 185 | 78.7% | 6.94 – 59.67 | 32.38 |

![Tier distribution pie chart](<../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/work/tier_breakdown_pie.png>)

![Score distribution histogram](<../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/work/score_distribution_histogram.png>)

---

## Top 13 Excellent Managers

All 13 Excellent-tier managers achieved all three boolean criteria (days < 45, experience > 3.5, feedback > 85%), differentiating themselves primarily through their hire rate score:

| Rank | Manager Name | Reqs Owned | Hire Rate Score | Days (<45) | Experience (>3.5) | Feedback (>85%) | Composite |
|---|---|---|---|---|---|---|---|
| 1 | Lorraine Gibbs | 25 | 64.63 | ✓ | ✓ | ✓ | **89.39** |
| 2 | Melissa Russell | 31 | 62.31 | ✓ | ✓ | ✓ | **88.69** |
| 3 | Kyle Andrews | 16 | 56.21 | ✓ | ✓ | ✓ | **86.86** |
| 4 | Erin Walters | 11 | 55.12 | ✓ | ✓ | ✓ | **86.54** |
| 5 | Victoria Valdez | 17 | 53.41 | ✓ | ✓ | ✓ | **86.02** |
| 6 | William Tran | 38 | 50.20 | ✓ | ✓ | ✓ | **85.06** |
| 7 | Andrew Gonzales | 34 | 46.24 | ✓ | ✓ | ✓ | **83.87** |
| 8 | Keith Stephens MD | 18 | 45.95 | ✓ | ✓ | ✓ | **83.79** |
| 9 | Mr. James Duncan | 28 | 43.31 | ✓ | ✓ | ✓ | **82.99** |
| 10 | Kelly Foster | 23 | 42.60 | ✓ | ✓ | ✓ | **82.78** |
| 11 | Kim Stewart | 30 | 39.49 | ✓ | ✓ | ✓ | **81.85** |
| 12 | Michelle Sullivan | 20 | 38.05 | ✓ | ✓ | ✓ | **81.42** |
| 13 | Johnathan Smith | 9 | 33.55 | ✓ | ✓ | ✓ | **80.19** |

> **Note:** Only 6 managers (2.6%) achieved all four dimensions at a strong level (hire rate ≥ 50% and all three boolean criteria met). All 13 Excellent managers met all boolean criteria.

---

## Good Tier (Sample: Top 10 of 37)

Many Good-tier managers met the boolean criteria for days and experience but failed the feedback threshold, pulling their scores below 80:

| Manager Name | Reqs | Hire Rate | Days | Exp | Feedback | Score |
|---|---|---|---|---|---|---|
| David Bird | 19 | 32.85 | ✓ | ✓ | ✓ | 79.86 |
| Michael Hoffman | 60 | 65.00 | ✓ | ✓ | ✗ | 69.50 |
| Brenda Levy | 43 | 64.32 | ✓ | ✓ | ✗ | 69.30 |
| David Espinoza | 25 | 64.31 | ✓ | ✓ | ✗ | 69.29 |
| Anne Castillo | 16 | 64.27 | ✓ | ✓ | ✗ | 69.28 |
| Matthew Fox | 48 | 62.12 | ✓ | ✓ | ✗ | 68.64 |
| Christopher Walker | 43 | 55.59 | ✓ | ✓ | ✗ | 66.68 |
| Dr. Kimberly Henderson | 15 | 54.81 | ✓ | ✓ | ✗ | 66.44 |
| Ana Sanders | 31 | 54.53 | ✓ | ✓ | ✗ | 66.36 |
| Jessica Mcdonald | 38 | 53.69 | ✓ | ✓ | ✗ | 66.11 |

---

## Needs Improvement (Bottom 5)

| Manager Name | Reqs | Hire Rate | Days | Exp | Feedback | Score |
|---|---|---|---|---|---|---|
| Michael Hamilton | 44 | 23.14 | ✗ | ✗ | ✗ | 6.94 |
| Zachary Cole | 29 | 25.63 | ✗ | ✗ | ✗ | 7.69 |
| Dr. Sara Hoffman DDS | 35 | 25.70 | ✗ | ✗ | ✗ | 7.71 |
| Robert Miller | 42 | 26.58 | ✗ | ✗ | ✗ | 7.97 |
| Donald Ellis | 27 | 26.71 | ✗ | ✗ | ✗ | 8.01 |

These managers failed all three boolean criteria and had low hire rates.

---

## Criterion Pass Rates (All 235 Managers)

| Criterion | Managers Meeting | Percentage |
|---|---|---|
| Avg Days to Hire < 45 days | 115 | 48.9% |
| Avg Candidate Experience > 3.5 | 86 | 36.6% |
| Feedback Completion > 85% | 58 | 24.7% |
| Hire Rate ≥ 50% (≥50 score) | 92 | 39.1% |
| **All three boolean criteria met** | **13** | **5.5%** |

The feedback completion rate > 85% criterion is the most restrictive (only 24.7% pass), while the days-to-hire < 45 criterion is the most commonly met (48.9%).

---

## Component Score Analysis by Tier

![Component scores by tier](<../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/work/component_scores_by_tier.png>)

Key observations:
- **Excellent** managers average 100 on all three boolean criteria and 48.6 on hire rate.
- **Good** managers average 91.9 on days, 81.1 on experience, but only 29.7 on feedback — the feedback threshold is the main barrier preventing them from reaching Excellent.
- **Needs Improvement** managers underperform on all dimensions, especially experience (23.2 avg) and feedback (18.4 avg).

---

## Score vs. Requisition Volume

| Requisitions Bucket | Count | Avg Score | Avg Hire Rate |
|---|---|---|---|
| 5–19 | 42 | 48.30 | 47.12 |
| 20–39 | 94 | 43.27 | 46.36 |
| 40+ | 99 | 34.09 | 46.61 |

Managers with fewer requisitions tend to have slightly higher composite scores, though hire rates are similar across all volume groups. The difference likely stems from smaller managers having more time per requisition, leading to better candidate experience and faster hiring.

---

## Hire Rate vs. Composite Score

![Hire rate vs composite score scatter](<../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/work/hire_rate_vs_composite.png>)

The scatter plot shows that a high hire rate does not guarantee a high composite score — managers must also satisfy the boolean criteria on days, experience, and feedback. Conversely, managers with even moderate hire rates (~40–50) can reach Excellent if they satisfy all three boolean criteria.

---

## Methodology

1. **Filter:** Only managers with `total_requisitions_owned >= 5` (all 235 managers qualified).
2. **Score Calculation:**
   - `hire_rate_score = candidate_hire_rate × 100`
   - `days_score = 100` if `avg_total_days_to_hire < 45`, else `0`
   - `experience_score = 100` if `avg_candidate_experience_score > 3.5`, else `0`
   - `feedback_score = 100` if `feedback_completion_rate_managed > 85`, else `0`
   - `composite_score = 0.30×hire_rate_score + 0.25×days_score + 0.25×experience_score + 0.20×feedback_score`
3. **Tier Classification:**
   - **Excellent:** composite_score ≥ 80
   - **Good:** 60 ≤ composite_score < 80
   - **Needs Improvement:** composite_score < 60

All computation was performed in the database via SQL using CTEs, CASE expressions, and window functions. Visualizations were generated in Python (matplotlib/seaborn) using the computed results.

---

## Limitations

- The boolean criteria (days < 45, experience > 3.5, feedback > 85%) are binary thresholds that do not reward gradual improvement; a manager with 44.9 days scores 100, while one with 45.1 days scores 0.
- The feedback completion rate > 85% is the most restrictive criterion and likely dominates tier classification.
- Candidate hire rate is weighted continuously (30%), which is good, but its impact is diluted by the three boolean criteria.
- The score distribution is heavily left-skewed (78.7% in Needs Improvement), suggesting the thresholds may need calibration for a more balanced evaluation.
- The dataset does not include industry or department adjustments, which could affect fair comparison across different hiring contexts.

---

## Figures

- [Score Distribution Histogram](<../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/work/score_distribution_histogram.png>)
- [Tier Breakdown Pie Chart](<../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/work/tier_breakdown_pie.png>)
- [Hire Rate vs. Composite Score Scatter](<../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/work/hire_rate_vs_composite.png>)
- [Component Scores by Tier](<../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/work/component_scores_by_tier.png>)