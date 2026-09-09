<!-- Reading copy: local artifact links normalized. Original answer is preserved at ../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/answer.md -->

# User Value Scoring Model & Segmentation Analysis Report

## Executive Summary

This report presents a **composite user value scoring model (0-100)** built from 4,422 active users across 10 language groups and 6 geographic regions. The model quantifies user value along three required dimensions — **participation frequency, completion rate, and cross-channel activity** — plus engagement depth. Users are segmented into five tiers (one-time, low, medium, high, power) aligned with the existing `user_cohort_analysis` framework. We identify the key behavioral drivers of the medium→high value transition, analyze differences across languages and regions, and propose a segmentation strategy with personalized incentive plans.

---

## 1. Value Scoring Model

### 1.1 Model Architecture

The composite score is a weighted sum of four normalized dimensions:

| Dimension | Weight | Rationale |
|-----------|--------|-----------|
| **Participation Frequency** | 40 pts | Total distinct survey responses, min-max scaled over [1, 13] |
| **Completion Rate** | 30 pts | Completed surveys / total survey responses |
| **Cross-Channel Activity** | 20 pts | Number of distinct distribution channels used (1-5) |
| **Engagement Depth** | 10 pts | Average survey progress percentage |

**Score = freq_score + completion_score + channel_score + progress_score**

### 1.2 Score Distribution

![Score Distribution](<../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/work/fig1_score_distribution.png>)

- **Mean score:** 41.1 (SD = 13.5)
- **Range:** 4.1 – 84.2
- **Median:** 42.2
- **Percentiles:** P25=32.9, P50=42.2, P75=50.3, P90=57.2, P95=61.5

### 1.3 Tier Segmentation

Tiers are defined by score thresholds, with `one_time` (single participation) as a separate category:

| Tier | Threshold | Users | % of Users | Avg Score | % Responses | % Completed |
|------|-----------|-------|------------|-----------|-------------|-------------|
| **One-Time** | n_surveys = 1 | 368 | 8.3% | 23.0 | 2.1% | 2.0% |
| **Low Value** | Score < 35 | 1,121 | 25.4% | 27.8 | 17.7% | 9.1% |
| **Medium Value** | 35 ≤ Score < 50 | 1,801 | 40.7% | 43.0 | 41.6% | 40.9% |
| **High Value** | 50 ≤ Score < 60 | 855 | 19.3% | 54.4 | 26.8% | 32.5% |
| **Power User** | Score ≥ 60 | 277 | 6.3% | 65.0 | 11.8% | 15.6% |

**Key insight:** Power users (6.3% of the base) contribute **11.8% of all survey responses** and **15.6% of completed surveys**, confirming the stratification described in the cohort analysis.

![Tier Contribution](<../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/work/fig2_tier_contribution.png>)

### 1.4 Score Decomposition

![Score Decomposition](<../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/work/fig6_score_decomposition.png>)

The decomposition shows that the progression from low to high tiers is driven primarily by **participation frequency** and **completion rate** improvements, with cross-channel activity becoming increasingly important at the high-value and power-user levels.

---

## 2. Medium→High Value Transition Drivers

### 2.1 Key Behavioral Characteristics

We compared medium_value (n=1,801) and high_value (n=855) users across 9 behavioral dimensions using Mann-Whitney U tests and Cohen's d effect sizes:

| Dimension | Medium Mean | High Mean | % Improvement | Cohen's d | p-value |
|-----------|------------|-----------|--------------|-----------|---------|
| **Completed Surveys** | 2.01 | 3.37 | **+67.7%** | **2.127** | <0.0001 |
| **Distinct Surveys** | 4.08 | 5.54 | +35.7% | 1.083 | <0.0001 |
| **Survey Responses** | 4.09 | 5.54 | +35.6% | 1.082 | <0.0001 |
| **Active Days** | 4.08 | 5.52 | +35.3% | 1.075 | <0.0001 |
| **Channels Used** | 2.86 | 3.62 | +26.7% | 0.984 | <0.0001 |
| **Active Months** | 13.79 | 16.41 | +19.0% | 0.525 | <0.0001 |
| **Completion Rate** | 0.54 | 0.65 | +20.0% | 0.501 | <0.0001 |
| **Avg Progress** | 49.94 | 52.48 | +5.1% | 0.168 | <0.0001 |
| **Avg Duration** | 402s | 418s | +3.9% | 0.111 | 0.0013 |

**Top 3 transition drivers (by effect size):**
1. 🥇 **Completed surveys** (d=2.13) — the strongest differentiator
2. 🥈 **Participation breadth** (survey variety, active days, response count) (d≈1.08)
3. 🥉 **Cross-channel diversification** (d=0.98)

![Medium vs High Comparison](<../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/work/fig3_medium_vs_high.png>)

### 2.2 Channel-Level Analysis

High-value and power users are **1.5–1.6× more likely** to use each channel compared to lower-tier users:

| Channel | High+Power Usage | Rest Usage | Lift |
|---------|-----------------|------------|------|
| Social | 77.9% | 48.1% | 1.6× |
| Web | 76.7% | 49.1% | 1.6× |
| Email | 75.4% | 48.3% | 1.6× |
| SMS | 74.7% | 48.0% | 1.6× |
| Mobile | 75.3% | 48.6% | 1.5× |

Power users show exceptionally high multi-channel adoption (87–90% for each channel).

---

## 3. Language and Regional Analysis

### 3.1 Language Differences

| Language | Users | Avg Score | High+Power % | Power % | One-Time % |
|----------|-------|-----------|-------------|---------|-----------|
| EN | 379 | 41.8 | 27.7% | 7.4% | 11.1% |
| IT | 430 | 41.7 | 26.3% | 4.9% | 9.1% |
| NL | 456 | 41.6 | 25.4% | 5.7% | 5.9% |
| ES | 411 | 41.5 | 27.7% | 6.8% | 7.8% |
| ZH | 517 | 41.3 | 26.5% | 6.6% | 7.7% |
| JA | 480 | 41.1 | 26.0% | 7.1% | 7.5% |
| KO | 443 | 40.7 | 25.3% | 6.8% | 7.9% |
| FR | 418 | 40.7 | 23.7% | 6.0% | 8.9% |
| PT | 507 | 40.4 | 22.7% | 4.9% | 7.7% |
| DE | 381 | 39.8 | 25.2% | 6.8% | 10.8% |

**Chi-square test: χ² = 33.5, p = 0.587** — Language is **not** a statistically significant differentiator of value tier composition. The differences across languages are small (range 39.8–41.8).

### 3.2 Regional (Continent) Differences

| Continent | Users | Avg Score | High+Power % | Power % | One-Time % |
|-----------|-------|-----------|-------------|---------|-----------|
| Africa | 1,428 | **45.0** | **34.2%** | **10.0%** | 2.2% |
| South America | 393 | 42.1 | 28.8% | 6.4% | 4.3% |
| Europe | 187 | 38.5 | 17.1% | 3.2% | 9.1% |
| North America | 405 | 38.3 | 18.8% | 3.5% | 9.1% |
| Asia | 468 | 37.4 | 18.2% | 4.5% | 12.4% |
| Oceania | 64 | 31.7 | 6.2% | 1.6% | 28.1% |

**Chi-square test: χ² = 299.6, p < 0.0001** — Region is **highly significant** in explaining tier composition.

![Language & Region Scores](<../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/work/fig4_lang_region_scores.png>)

![Tier Heatmap](<../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/work/fig5_tier_heatmap.png>)

### 3.3 Value Transition Paths by Language and Region

The "recipe" for transitioning from medium→high value varies by region:

| Region | Frequency Gap | Completion Gap | Channel Gap | Key Path |
|--------|--------------|---------------|-------------|----------|
| **Europe** | 1.76 (largest) | 0.04 (smallest)* | 1.06 (largest) | **Channel expansion + frequency** |
| **North America** | 1.00 (smallest) | 0.16 (largest) | 0.60 | **Completion rate improvement** |
| **Africa** | 1.46 | 0.12 | 0.75 | Balanced |
| **South America** | 1.43 | 0.10 | 0.83 | Balanced + channels |
| **Asia** | 1.41 | 0.14 | 0.63 | Balanced + completion |

*Note: In Europe, the completion rate gap between medium and high users is **not statistically significant** (p=0.41), meaning European users achieve high value primarily through **frequency and channel diversity**, not completion rate.

![Transition by Region](<../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/work/fig8_transition_by_region.png>)

Across languages, the medium→high score gap is remarkably consistent (10.97–11.93 points), but the composition of the gap differs — e.g., PT users show the largest completion gap (+0.151) while DE users show the largest frequency gap (+1.620).

---

## 4. Cohort Analysis Context

The `user_cohort_analysis` table provides the stratification baseline:

![Cohort Trends](<../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/work/fig7_cohort_trends.png>)

- **Cohort health score** is stable at ~48.7 across 12 months
- **Stable tier proportions:** Power 7.8%, High 14.9%, Medium 34.8%, Low 24.9%, One-Time 17.6%
- Our model produces similar proportions (Power 6.3%, High 19.3%, Medium 40.7%, Low 25.4%, One-Time 8.3%), with the one-time difference attributable to the fact that our population is active respondents only.

---

## 5. User Segmentation Strategy

### 5.1 Segment Profiles

| Segment | Profile | Key Behavior |
|---------|---------|-------------|
| **One-Time Users** | Single survey, 47% completion, 1 channel | Trial engagement only |
| **Low Value** | 2.8 surveys avg, 28% completion, 2.2 channels | Low investment, low completion |
| **Medium Value** | 4.1 surveys avg, 54% completion, 2.9 channels | Regular but moderate engagement |
| **High Value** | 5.5 surveys avg, 65% completion, 3.6 channels | Strong multi-channel engagement |
| **Power Users** | 7.5 surveys avg, 69% completion, 4.3 channels | Exceptional participation leader |

### 5.2 Strategic Recommendations

**1. One-Time → Low: Activation**
- **Trigger:** After first survey completion
- **Action:** Send personalized follow-up within 7 days; offer a survey on a topic of interest
- **Incentive:** Small reward (e.g., gift card) for completing a second survey
- **KPI:** Conversion to 2+ surveys within 30 days

**2. Low → Medium: Habit Formation**
- **Trigger:** Completion rate < 40% or single-channel usage
- **Action:** Targeted email/SMS nudges with progress dashboards; introduce second channel
- **Incentive:** Gamification (points, badges, leaderboards) for consistent participation
- **KPI:** Increase completion rate to > 50%, introduce second channel

**3. Medium → High: Multi-Channel Deepening**
- **Trigger:** Completion rate > 50% but channels < 3
- **Action:** Cross-channel onboarding (invite to mobile/web surveys); personalized topic recommendations
- **Incentive:** Priority access to high-interest surveys; premium content unlocks
- **KPI:** Add 1+ channel, increase active months to 16+

**4. High → Power: Recognition & Leadership**
- **Trigger:** Score > 55, channels ≥ 3, active > 14 months
- **Action:** Invite to exclusive feedback panel; early access to new surveys; community ambassador program
- **Incentive:** Recognition (top contributor badges), monetary rewards, exclusive insights
- **KPI:** Maintain 4+ channels, score increase > 60

### 5.3 Personalized Incentive Plan by Language & Region

**By Region (since region is a significant differentiator):**

| Region | Medium→High Lever | Recommended Incentive |
|--------|------------------|----------------------|
| **Africa** | Balanced (freq + channels) | Cross-channel bundle + frequency rewards |
| **Europe** | **Channels + frequency** (not completion) | Channel-agnostic participation rewards; completion incentives less effective |
| **North America** | **Completion rate** | Incentivize full survey completion over speed |
| **Asia** | Balanced + completion | Targeted completion bonuses + channel expansion |
| **South America** | Channels + frequency | Multi-channel engagement rewards |

**By Language (small differences, but useful for messaging):**

| Language | Characteristic | Incentive Tone |
|----------|---------------|----------------|
| EN/ES | Higher high-value proportion | Competitive leaderboards, achievement badges |
| DE | Higher one-time rate | Strong re-engagement offers, personalized onboarding |
| PT/FR | Lower high-value proportion | More structured incentives, clear progression path |
| JA/KO | Medium-high gap driven by completion | Quality-focused rewards, completion streaks |

### 5.4 Channel Strategy

Based on the channel performance analysis:
- **SMS** has the highest completion rate (51.6%) and efficiency score
- **Email** has the lowest completion rate (50.1%) but highest reach
- For **medium→high transition**, prioritize introducing users to **SMS** and **social** channels (which show the highest lift among high-value users)

---

## 6. Limitations

1. **Synthetic data limitations:** The geographic coordinates in the dataset appear synthetic/distributed, making continent mapping imprecise (~33% of users fall into "Other" catch-all regions).
2. **Cross-sectional design:** The model scores users at a single point in time; true transition path analysis would require longitudinal panel data tracking individual users over time.
3. **One-time user definition:** The response table shows only 8.3% as one-time (single survey), while the cohort table suggests ~17.6% — the difference likely reflects contacts who were sent surveys but never responded.
4. **No survey content data:** The model does not incorporate survey topic, complexity, or user preference data, which could further refine the scoring.
5. **Channel completeness:** The contact table only tracks email and SMS channels; the response table covers all 5 channels but is limited to users who actually responded.

---

## 7. Conclusion

The composite value scoring model successfully stratifies users into meaningful tiers, with power users (6.3%) contributing 15.6% of completed surveys. The medium→high value transition is primarily driven by **completed survey volume** and **multi-channel diversification**, with region-specific transition "recipes" that enable targeted interventions. While language differences are modest, geographic region is a strong predictor of value tier, suggesting that regionally-tailored incentive strategies will be most effective.