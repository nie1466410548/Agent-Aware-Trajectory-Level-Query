<!-- Reading copy: local artifact links normalized. Original answer is preserved at ../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/answer.md -->

# Interactive Impact of Email Delivery Timing Windows and Subject Line Themes on Engagement and Retention

## Executive Summary

This analysis evaluates how the combination of **sending time windows** (weekday/weekend, morning/afternoon, holiday proximity) and **subject line themes** (discount-related, new product launch, storytelling) influences email open rates, click rates, and subsequent active retention. The analysis is performed on campaign-person touch data from the Klaviyo dataset. Due to limited campaign-event data (N=4 person-campaign touches), the findings are descriptive and illustrative of the analytical framework rather than statistically conclusive.

---

## 1. Data Sources and Integration

### Tables Used
| Table | Description | Rows |
|-------|-------------|------|
| `klaviyo__person_campaign_flow` | Per-person campaign touch metrics (open rate, click rate, net revenue) | 4 |
| `klaviyo__events` | Campaign metadata (campaign name, subject line, send timestamps) | 4 |
| `klaviyo__persons` | Person-level demographics and retention metrics | 1,192 |

### Data Integration Strategy
The analysis unit is a **person-campaign touch** (row in `klaviyo__person_campaign_flow`). Each touch was joined to:
- Campaign metadata from `klaviyo__events` to obtain campaign name and subject line
- Person-level retention metrics from `klaviyo__persons` (active_retention_rate_week, active_retention_rate_month)
- Timing features derived from `first_event_at` (campaign send timestamp)

### Subject Line Theme Classification
Subject lines were classified by keyword matching:
| Keyword Rule | Theme | Examples |
|-------------|-------|---------|
| Contains "launch" | **new_product_launch** | "Unlock Product Launch Offers" |
| Contains "offer", "sale", "discount", "deal", "save" | **discount** | "Unlock Seasonal Offers" |
| Contains "story", "journey", "behind" | **storytelling** | (none in dataset) |
| No match | **unknown** | CMP0012 (no subject line in events) |

### Timing Window Segmentation
| Window | Definition | SQL Implementation |
|--------|-----------|-------------------|
| **Weekday vs Weekend** | Mon–Fri vs Sat–Sun | `strftime('%w', send_at)` |
| **Morning vs Afternoon** | 0–12h vs 12–24h | `strftime('%H', send_at)` |
| **Holiday proximity** | 3 days before vs 3 days after a US federal holiday | Nearest holiday from curated list (2022–2024) |

---

## 2. Analysis Dataset

| Campaign | Person | Subject Theme | Day Part | Time Half | Holiday Window | Open Rate | Click Rate | Retention Week | Retention Month |
|----------|--------|--------------|----------|-----------|---------------|-----------|------------|----------------|-----------------|
| CMP0002 | 59bc05… | discount | weekday | morning | neutral | 0.536 | 0.400 | 1.000 | 1.000 |
| CMP0001 | 01F366… | new_product_launch | weekday | morning | neutral | 0.462 | 0.333 | 0.943 | 0.889 |
| CMP0016 | 59bc05… | discount | **weekend** | morning | neutral | 0.446 | 0.341 | 1.000 | 1.000 |
| CMP0012 | 01F366… | **unknown** | weekday | morning | **post_holiday** | 0.344 | 0.318 | 0.943 | 0.889 |

**Key observation:** All four sends occurred during the **morning** (07:45–10:05). Only one send was on a **weekend** (CMP0016, Saturday). Only one send fell within the holiday proximity window (CMP0012, sent on Labor Day 2023).

---

## 3. Descriptive Results

### 3.1 Overall Metrics (N=4)

| Metric | Mean | SD | Min | Max |
|--------|------|-----|-----|-----|
| Open Rate | 0.447 | 0.079 | 0.344 | 0.536 |
| Click Rate | 0.348 | 0.037 | 0.318 | 0.400 |
| Retention Week | 0.971 | 0.033 | 0.943 | 1.000 |
| Retention Month | 0.944 | 0.064 | 0.889 | 1.000 |

Comparatively, the broader population (N=1,192) has:
- Average email open rate: **0.354**
- Average weekly retention: **0.787**
- Average monthly retention: **0.803**

The two campaign-exposed persons have above-average metrics.

### 3.2 Cross-Tabulation: Theme × Day Part

#### Open Rate
| Theme | Weekday | Weekend |
|-------|---------|---------|
| **discount** | 0.536 | 0.446 |
| **new_product_launch** | 0.462 | — |
| **unknown** | 0.344 | — |

**Discount-themed subject lines** on weekdays achieved the highest open rate (0.536), followed by new product launch (0.462). The discount theme on weekend showed a lower open rate (0.446).

#### Click Rate
| Theme | Weekday | Weekend |
|-------|---------|---------|
| **discount** | 0.400 | 0.341 |
| **new_product_launch** | 0.333 | — |
| **unknown** | 0.318 | — |

Click rates follow a similar pattern, with discount-themed weekday sends achieving the highest click rate (0.400).

### 3.3 Holiday Proximity

Only one touch fell within the holiday proximity window:
- **CMP0012** (unknown theme): Sent on Labor Day (Sep 4, 2023) → **post_holiday** window
- Open rate: 0.344 (lowest of the four)
- Click rate: 0.318 (lowest)

This may suggest that sending on a holiday (or within the post-holiday window) is associated with lower engagement, though N=1 prevents generalization.

### 3.4 Retention Rates by Theme × Day Part

| Theme | Day Part | Retention Week | Retention Month |
|-------|----------|---------------|-----------------|
| discount | weekday | 1.000 | 1.000 |
| discount | weekend | 1.000 | 1.000 |
| new_product_launch | weekday | 0.943 | 0.889 |
| unknown | weekday | 0.943 | 0.889 |

Retention differences are entirely driven by the **person-level** variation (two distinct persons, one with perfect retention and one with 0.889 monthly retention), not by campaign timing or theme.

---

## 4. Visualization

### Interaction Analysis: Metrics by Theme × Day Part

![Interaction Analysis](<../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/work/interaction_analysis.png>)

*Figure 1: Bar charts showing mean open rate, click rate, retention rates, and net revenue by subject theme and day part. The discount theme on weekdays shows the highest open and click rates, while the unknown theme (sent on Labor Day) shows the lowest.*

### Analysis Dataset Table

![Analysis Dataset](<../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/work/analysis_dataset_table.png>)

*Figure 2: Complete analysis dataset with all 4 person-campaign touch observations, showing campaign identifiers, timing windows, theme classification, and outcome metrics.*

---

## 5. Design Discussion: Analytical Framework for Full-Scale Implementation

Given the limited data, the following framework is proposed for a robust evaluation with sufficient data:

### 5.1 Recommended Statistical Model

**Two-Way Factorial ANOVA** (or regression with interaction terms):
```
Metric ~ Theme + Timing_Window + Theme × Timing_Window
```
Where `Metric` ∈ {open_rate, click_rate, active_retention_rate_week, active_retention_rate_month}

For each of the three timing dimensions:
1. **Theme × Weekday/Weekend**
2. **Theme × Morning/Afternoon**
3. **Theme × Pre-Holiday/Post-Holiday**

### 5.2 Required Sample Size

With 3 theme categories × 2 timing conditions per dimension = 6 groups, a minimum of **10–15 observations per cell** (60–90 total person-campaign touches) is needed for sufficient statistical power.

### 5.3 Holiday Proximity Enhancement

The holiday window analysis requires:
- A comprehensive holiday calendar (observed dates, not just federal)
- Consideration of "holiday season" effects (e.g., Thanksgiving–Christmas period)
- Adjustment for industry-specific holidays (e.g., retail vs B2B)

### 5.4 Confounding Controls

In a full-scale analysis, the following should be controlled:
- **Person-level fixed effects** (baseline engagement propensity)
- **Campaign-specific effects** (creative quality, call-to-action strength)
- **Time-of-year seasonality** (e.g., Q4 holiday season effects)
- **Send frequency** (email fatigue from multiple sends)

### 5.5 Implementation Strategy

1. **Data Pipeline**: Build a campaign-person touch table from event data, deriving timestamps from campaign send events
2. **Feature Engineering**: Compute timing windows and subject line theme classifications via keyword/rule-based or NLP classifier
3. **Modeling**: Run separate OLS regressions for each outcome metric with interaction terms
4. **Post-Hoc**: Conduct Tukey HSD pairwise comparisons for significant interaction effects
5. **Visualization**: Interaction plots (as in Figure 1) with confidence intervals

---

## 6. Limitations

1. **Extremely small sample size** (N=4 person-campaign touches). No statistical significance testing is meaningful.
2. **No afternoon sends** exist in the data, preventing analysis of the morning/afternoon interaction.
3. **Only one holiday-proximity observation** (post-holiday, Labor Day), with insufficient contrast.
4. **No storytelling-themed subject lines** present in the campaign data.
5. **Confounding of person identity with theme**: Person 59bc05… received only discount-themed emails; person 01F366… received product launch and unknown. Observed differences may reflect person-level engagement rather than theme effects.
6. **CMP0012 lacks a subject line** in the events table, classified as "unknown" and excluded from theme comparisons.
7. **Retention is a person-level attribute** (not campaign-specific), so observed retention differences are attributable to the person, not the campaign touch.

---

## 7. Conclusions

| Timing Window | Discount Theme | New Product Launch Theme | Storytelling Theme |
|---------------|---------------|------------------------|-------------------|
| **Weekday Morning** | Highest open (0.536) & click (0.400) | Moderate open (0.462) & click (0.333) | No data |
| **Weekend Morning** | Moderate open (0.446) & click (0.341) | No data | No data |
| **Post-Holiday** | No data | No data | No data |

**Tentative patterns (descriptive only):**
- Discount-themed emails sent on **weekday mornings** achieved the highest engagement metrics
- Weekend morning sends showed lower engagement than weekday for the same discount theme
- The single post-holiday send (Labor Day, unknown theme) exhibited the lowest engagement
- Both persons exposed to campaigns had above-average retention compared to the general population

**Recommended next step:** Collect additional campaign data (at least 60+ person-campaign touches) and apply the factorial ANOVA framework to quantify the interactive effects of timing and subject line themes.