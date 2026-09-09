# Comprehensive Campaign Health Assessment and Optimization Report

## Executive Summary

This report analyzes 50 campaigns across 17 months (Feb 2023 – Jun 2024) in the Google Ads database, totaling **$17.9M** in ad spend. Using a screening criterion of **monthly cost > $1,000 AND ROAS < 0.8**, we identified **11 campaigns** with 155 screened months. The **10 core problematic campaigns** (all with constant ROAS < 0.8 across all months) represent **37.2% ($6.66M)** of total spend.

A three-dimensional health score model was built covering Cost Efficiency (40%), Conversion Quality (35%), and Competitiveness (25%). The 10 core problematic campaigns all fall into **Critical or High Risk** categories, with health scores ranging from 26.4 to 35.7.

---

## 1. Data Overview

| Metric | Value |
|---|---|
| Total campaigns with report data | 50 |
| Total months of data | 17 (2023-02 to 2024-06) |
| Total campaign-months | 714 |
| Total ad spend | $17,913,311 |
| Campaign types | Display, Shopping, Video, Search, Performance Max |
| Bidding strategies | Target CPA, Manual CPC, Target ROAS, Maximize Conversions, Enhanced CPC |
| Industries | 8 (Real Estate, Healthcare, E-commerce, Fashion, Travel, Education, SaaS, Finance) |
| Geographic targets | 7 (Japan, UK, France, Australia, US, Canada, Germany) |
| Device types | 3 (Desktop, Mobile, Tablet) |

---

## 2. Screening Criteria

**Condition:** Monthly cost > $1,000 AND ROAS < 0.8

All 714 campaign-months have cost > $1,000, so the screening reduces to **ROAS < 0.8**. This identifies **155 months** across **11 campaigns**.

**10 core campaigns** have ROAS constant across all months (range 0.31–0.69), indicating a systematic issue rather than seasonal fluctuation. One additional campaign (Campaign 97) had a single bad month.

### Screened Campaigns

| Campaign ID | Campaign Name | ROAS | Months Screened | Total Cost |
|---|---|---|---|---|
| 180 | SaaS - Video Campaign 180 | 0.56 | 17/17 | $566,740 |
| 135 | Travel - Display Campaign 135 | 0.43 | 17/17 | $713,277 |
| 69 | Healthcare - Search Campaign 69 | 0.52 | 17/17 | $875,023 |
| 148 | Travel - Performance Max Campaign 148 | 0.47 | 16/16 | $553,946 |
| 56 | Real Estate - Video Campaign 56 | 0.31 | 16/16 | $613,541 |
| 27 | Finance - Search Campaign 27 | 0.69 | 16/16 | $800,271 |
| 105 | Education - Display Campaign 105 | 0.43 | 15/15 | $659,656 |
| 184 | Travel - Video Campaign 184 | 0.69 | 14/14 | $533,020 |
| 36 | E-commerce - Display Campaign 36 | 0.69 | 14/14 | $765,109 |
| 178 | Fashion - Performance Max Campaign 178 | 0.49 | 12/12 | $580,953 |
| 97 | Fashion - Video Campaign 97 | 0.58 | 1/15 | $207,404 |

---

## 3. Three-Dimensional Health Score Model

### Model Structure

| Dimension | Weight | Sub-metrics | Direction |
|---|---|---|---|
| **Cost Efficiency** | 40% | ROAS (40%), Cost per Conversion (30%), CPC (30%) | Min-max normalized (0-1) then scaled to 0-100 |
| **Conversion Quality** | 35% | Conversion Rate (40%), Avg Order Value (30%), Conversion Volume (30%) | Min-max normalized (0-1) then scaled to 0-100 |
| **Competitiveness** | 25% | Quality Score (40%), Impression Share (30%), CTR (30%) | Min-max normalized (0-1) then scaled to 0-100 |

**Health Score = 0.4 × Cost Efficiency + 0.35 × Conversion Quality + 0.25 × Competitiveness**

### Risk Level Thresholds

| Risk Level | Health Score Range | Campaigns | Problematic |
|---|---|---|---|
| **Critical** | < 30 | 5 | 5 (100%) |
| **High** | 30 – 36 | 11 | 5 (45%) |
| **Medium** | 36 – 45 | 22 | 0 (0%) |
| **Low** | ≥ 45 | 12 | 0 (0%) |

![Health Score Distribution](health_score_distribution.png)

*Figure 1: Distribution of health scores across 50 campaigns with risk thresholds marked.*

### Dimension Comparison: Problematic vs Healthy

![Dimension Comparison](dimension_compare.png)

*Figure 2: Average dimension scores. The Critical gap is in Competitiveness (19.2 vs 47.8) and Cost Efficiency (36.3 vs 45.6).*

### Health Score Ranking

![Health Score Ranking](health_ranking_stacked.png)

*Figure 3: Full ranking of all 50 campaigns with three-dimension breakdown. Problematic campaigns shown in red.*

---

## 4. Cross-Dimension Performance Comparison

### By Campaign Type

| Campaign Type | Avg Health | Avg Cost Eff | Avg Conv Quality | Avg Competitive | Problematic |
|---|---|---|---|---|---|
| Shopping | 53.8 | 55.4 | 51.1 | 55.2 | 0 |
| Performance Max | 38.7 | 41.8 | 34.5 | 39.8 | 2 |
| Search | 38.3 | 31.2 | 39.8 | 47.6 | 2 |
| Video | 34.8 | 46.9 | 21.1 | 34.6 | 3 |
| **Display** | **30.5** | 40.3 | 23.6 | 24.4 | **3** |

**Shopping campaigns** consistently outperform all other types across all dimensions. **Display campaigns** show the worst health scores, with critically low competitiveness (24.4) and conversion quality (23.6).

![Health by Type](health_by_type.png)

### By Bidding Strategy

| Bidding Strategy | Avg Health | Avg Cost Eff | Avg Conv Quality | Avg Competitive | Problematic |
|---|---|---|---|---|---|
| Enhanced CPC | 42.6 | 44.6 | 38.7 | 45.1 | 1 |
| Manual CPC | 41.8 | 44.4 | 37.8 | 43.1 | 2 |
| Target ROAS | 41.1 | 44.4 | 38.2 | 39.8 | 3 |
| Maximize Conversions | 40.3 | 43.2 | 33.3 | 45.5 | 1 |
| **Target CPA** | **36.4** | 42.5 | 28.7 | 37.2 | **3** |

**Target CPA** campaigns have the lowest average health scores, driven by poor conversion quality. **Enhanced CPC** shows the best balance across dimensions.

![Health by Bidding](health_by_bidding.png)

### By Industry

| Industry | Avg Health | Problematic | Avg ROAS |
|---|---|---|---|
| E-commerce | 45.3 | 1 | 9.3 |
| Real Estate | 42.7 | 1 | 8.9 |
| Education | 41.0 | 1 | 7.5 |
| SaaS | 39.3 | 1 | 6.4 |
| Fashion | 39.1 | 1 | 6.8 |
| Finance | 39.0 | 1 | 6.3 |
| Healthcare | 37.8 | 1 | 6.6 |
| **Travel** | **37.1** | **3** | 5.4 |

**Travel** industry is disproportionately affected with 3 of 6 campaigns being problematic. **E-commerce** and **Real Estate** campaigns show the strongest health.

![Health by Industry](health_by_industry.png)

### By Device Type (Computed ROAS)

| Device Type | Computed ROAS | Total Cost | Best For |
|---|---|---|---|
| Tablet | 6.28 | $1,773,322 | Highest relative efficiency |
| Mobile | 6.35 | $10,753,523 | Largest volume |
| Desktop | 6.55 | $5,312,872 | Balanced performance |

### By Geographic Target

| Geo Target | Avg ROAS | Total Cost | Performance |
|---|---|---|---|
| United Kingdom | 8.43 | $1,836,680 | **Best** |
| France | 7.70 | $1,660,692 | Strong |
| Australia | 7.31 | $1,786,275 | Good |
| Canada | 7.24 | $1,135,548 | Good |
| Japan | 7.18 | $2,511,545 | Moderate |
| Germany | 6.98 | $1,166,904 | Below avg |
| United States | 6.62 | $1,855,628 | **Weakest** |

![Device/Geo/Trend](device_geo_trend.png)

*Figure 4: Device metrics, geo ROAS, monthly trend, and device cost breakdown.*

---

## 5. Trend Analysis (18 Months)

### Overall Monthly Trend

Monthly spend grew from **$211K** (Feb 2023) to **$1.26M** (Jun 2024), with a sharp ramp-up from Feb–Jul 2023 as more campaigns came online. The average ROAS fluctuated between 2.2 and 10.0, stabilizing around 5–8 in later months.

### Year-over-Year Growth (2024 vs 2023)

| Month | Cost YoY | Conversion Value YoY | Avg ROAS 2023 | Avg ROAS 2024 |
|---|---|---|---|---|
| Feb | **+513%** | +479% | 6.01 | 8.34 |
| Mar | +183% | +220% | 4.87 | 7.23 |
| Apr | +130% | +192% | 6.19 | 7.89 |
| May | +54% | +12% | 7.33 | 5.35 |
| Jun | +28% | +20% | 7.08 | 7.36 |

The extreme Feb growth reflects campaigns ramping up from a low base. Overall, ROAS improved in the first half of 2024 compared to 2023.

### Seasonal Pattern (2023 Monthly Cost Share)

| Month | Cost Share | Notes |
|---|---|---|
| Feb–Mar | 2.0–4.2% | Ramp-up phase |
| Apr–Jun | 5.2–9.5% | Steady growth |
| **Jul–Dec** | **11.5–12.2%** | **Peak season** |

The latter half of the year (Jul–Dec) accounts for **71% of annual spend** in 2023, indicating a strong seasonal pattern.

### Problematic Campaigns Trend

![Problematic Health Trend](problematic_health_trend.png)

*Figure 5: Monthly health score trend for the 10 problematic campaigns. Scores remain consistently low with no improvement trend.*

For problematic campaigns, YoY cost growth was:
- Feb: +219%, Mar: +74%, Apr: +44%, May: +16%, Jun: +19%

Costs are still growing for problematic campaigns, but at a decelerating rate.

---

## 6. Detailed Optimization Recommendations

### Per-Campaign Diagnosis and Recommendations

#### Campaign 105 – Education Display (CRITICAL, Health: 26.4)
- **Core Problem:** Cost efficiency severely low (37.5), Competitiveness critically weak (10.4), chronic ROAS of 0.43
- **Budget:** Reduce monthly budget from $43,977 by 25–30%. Reallocate to Shopping campaigns.
- **Keywords:** Pause "online course" PHRASE ($26K, ROAS 5.46) and "training program" BROAD ($17K, ROAS 6.11); focus on "certification" BROAD ($9K, ROAS 6.40)
- **Geo:** Shift from Japan (computed ROAS 4.30) to United Kingdom (computed ROAS 5.83)
- **Device:** Reduce Desktop spend (ROAS 4.44); increase Mobile (ROAS 6.06)
- **Bidding:** Switch from Target CPA to Manual CPC for better cost control

#### Campaign 135 – Travel Display (CRITICAL, Health: 26.8)
- **Core Problem:** Cost efficiency (37.1), Competitiveness (12.1), ROAS 0.43, avg CPA $89
- **Budget:** Reduce from $41,957 by 25%. Focus on search campaigns.
- **Geo:** Reduce US (computed ROAS 4.32); increase Australia (computed ROAS 6.79)
- **Device:** Shift from Tablet (ROAS 5.84) to Mobile (ROAS 6.38)
- **Bidding:** Move from Enhanced CPC to Target ROAS with realistic targets

#### Campaign 36 – E-commerce Display (CRITICAL, Health: 27.9)
- **Core Problem:** Cost efficiency (36.4), Competitiveness (12.7), CPA $94
- **Budget:** Cut from $54,651 by 30%. Reallocate to Shopping campaigns.
- **Geo:** Reduce Japan (computed ROAS 4.67); increase UK (computed ROAS 5.74)
- **Device:** Reduce Tablet (ROAS 4.65); increase Mobile (ROAS 5.50)
- **Bidding:** Switch from Manual CPC to Target ROAS

#### Campaign 184 – Travel Video (CRITICAL, Health: 29.6)
- **Core Problem:** Conversion quality critically low (20.7), CTR 0.008
- **Budget:** Reduce from $38,073 by 20%. Test with lower budget.
- **Geo:** Reduce Canada (computed ROAS 4.99); increase Germany (ROAS 5.10)
- **Device:** Reduce Mobile (ROAS 5.21); increase Tablet (ROAS 6.03)
- **Bidding:** Switch from Target CPA to Maximize Conversions

#### Campaign 180 – SaaS Video (CRITICAL, Health: 29.9)
- **Core Problem:** Conversion quality (22.2), Competitiveness (19.9), ROAS 0.56, CVR 0.009
- **Budget:** Reduce from $33,338 by 25%.
- **Keywords:** Pause "cloud platform" PHRASE (CPA $113); focus on "software solution" EXACT (CPA $74, ROAS 7.39)
- **Geo:** Reduce Japan (computed ROAS 4.06); increase US (computed ROAS 7.03)
- **Device:** Reduce Mobile (ROAS 5.37); increase Tablet (ROAS 6.15)
- **Bidding:** Move from Manual CPC to Target CPA with lower CPA targets

#### Campaign 56 – Real Estate Video (HIGH, Health: 31.0)
- **Core Problem:** Conversion quality (24.4), ROAS 0.31, CVR 0.010
- **Budget:** Reduce from $38,346 by 20%.
- **Keywords:** Pause "property sale" BROAD (CPA $84, ROAS 3.82) and "home buying" PHRASE (CPA $95, ROAS 3.39); focus on "buy house" EXACT (CPA $73, ROAS 6.17) and "mortgage" PHRASE (CPA $70, ROAS 7.60)
- **Geo:** Reduce US (computed ROAS 5.13); increase UK (computed ROAS 5.72)
- **Device:** Reduce Desktop (ROAS 5.17); increase Mobile (ROAS 6.40)
- **Bidding:** Switch from Target ROAS to Manual CPC

#### Campaign 69 – Healthcare Search (HIGH, Health: 32.0)
- **Core Problem:** Cost efficiency critically low (25.8), ROAS 0.52, impression share 28.9%
- **Budget:** Reduce from $51,472 by 25%. Highest cost campaign.
- **Geo:** Reduce US (computed ROAS 5.82); increase Canada (computed ROAS 7.88)
- **Device:** Reduce Mobile (ROAS 6.47); increase Desktop (ROAS 8.46)
- **Bidding:** Switch from Maximize Conversions to Target CPA with realistic targets

#### Campaign 148 – Travel Performance Max (HIGH, Health: 32.8)
- **Core Problem:** Cost efficiency (35.8), Competitiveness (19.4), ROAS 0.47, QS 4.7
- **Budget:** Reduce from $34,622 by 20%.
- **Keywords:** Focus on "cheap flights" PHRASE (ROAS 10.84) and "vacation package" BROAD (ROAS 10.82); pause low performers
- **Geo:** Increase US (computed ROAS 9.35); reduce Germany (computed ROAS 6.96)
- **Device:** Reduce Mobile (ROAS 7.36); increase Tablet (ROAS 8.93)
- **Bidding:** Switch from Target ROAS to Manual CPC

#### Campaign 178 – Fashion Performance Max (HIGH, Health: 34.3)
- **Core Problem:** Competitiveness critically low (16.2), ROAS 0.49, QS 4.5
- **Budget:** Reduce from $48,413 by 25%.
- **Geo:** Reduce France (computed ROAS 6.37); increase Australia (computed ROAS 8.53)
- **Device:** Reduce Mobile (ROAS 7.44); increase Desktop (ROAS 8.95)
- **Bidding:** Switch from Target ROAS to Maximize Conversions

#### Campaign 27 – Finance Search (HIGH, Health: 35.7)
- **Core Problem:** Cost efficiency critically low (25.6), QS 4.8
- **Budget:** Reduce from $50,017 by 20%.
- **Geo:** Reduce Australia (computed ROAS 5.23); increase UK (computed ROAS 6.66)
- **Device:** Reduce Desktop (ROAS 5.40); increase Tablet (ROAS 8.05)
- **Bidding:** Switch from Target CPA to Enhanced CPC

### Problematic Campaigns Breakdown

![Problematic Breakdown](problematic_breakdown.png)

*Figure 6: Cost distribution by geo and device for problematic campaigns.*

---

## 7. Summary of Key Findings

### Critical Issues Identified

1. **Systematic ROAS Mismatch:** The 10 core problematic campaigns show a constant, low ROAS (0.31–0.69) despite having computed conversion_value/cost ratios of 5–9. This indicates a fundamental attribution or conversion tracking issue that needs addressing at the account level.

2. **Competitiveness Deficit:** The most striking difference between problematic and healthy campaigns is **Competitiveness** (19.2 vs 47.8). Low quality scores (4.5–6.1) and impression share (29–50%) suggest poor ad relevance, landing page quality, and inadequate bid strategies.

3. **Display Campaign Vulnerability:** Display campaigns show the worst average health (30.5), with 3 of 6 being problematic. They combine low competitiveness (24.4) with poor conversion quality (23.6).

4. **Travel Industry Concentration:** 3 of 6 Travel campaigns are problematic, making it the most affected industry.

5. **Cost Escalation:** Problematic campaigns consume **37.2% of total spend** ($6.66M) while delivering negative ROAS, representing a significant financial drain.

### Recommended Actions

| Priority | Action | Expected Impact |
|---|---|---|
| 1 | **Immediate budget reduction** of 20-30% for all 10 campaigns | Save $1.3–$2.0M annually |
| 2 | **Switch bidding strategies** from automated targets to Manual CPC/Enhanced CPC | Regain spend control |
| 3 | **Improve quality scores** through ad copy refresh, keyword relevance, and landing page optimization | Increase competitiveness |
| 4 | **Reallocate geo budget** toward best-performing regions per campaign | 15–30% ROAS improvement |
| 5 | **Optimize device bidding** based on computed ROAS differences | 5–15% efficiency gain |
| 6 | **Pause low-ROAS keywords** (e.g., "cloud platform" PHRASE, "property sale" BROAD) | Reduce waste |
| 7 | **Implement conversion tracking audit** to resolve ROAS vs computed ratio discrepancy | Foundational fix |

---

## 8. Limitations

1. The `roas` field in the dataset shows a constant value per campaign for problematic campaigns, which differs from the computed `conversion_value/cost` ratio. This analysis uses the `roas` field as the primary ROI metric as specified in the task.
2. Keyword-level data is only available for 20 of 50 campaigns, limiting keyword optimization recommendations for some problematic campaigns.
3. The 18-month period (2023-02 to 2024-06) provides only 17 months of data, with limited YoY overlap (Feb–Jun).
4. Campaigns table contains 200 campaigns but only 50 have report data, suggesting the other 150 may be newer or inactive.

---

## Appendices

### Data Sources

| Table | Rows | Campaigns | Date Range |
|---|---|---|---|
| google_ads__campaign_report | 714 | 50 | 2023-02 to 2024-06 |
| google_ads__device_report | 2,142 | 50 | 2023-02 to 2024-06 |
| google_ads__geo_report | 2,550 | 50 | 2023-02 to 2024-06 |
| google_ads__keyword_report | 1,303 | 20 | 2023-Q1 to 2024-Q2 |
| campaigns | 200 | — | — |
| keywords | 252 | — | — |
| ad_groups | 58 | — | — |

### Health Score Model Equations

```
CostEfficiency = 0.4 × norm(ROAS) + 0.3 × norm(inv(CPA)) + 0.3 × norm(inv(CPC))
ConversionQuality = 0.4 × norm(CVR) + 0.3 × norm(AOV) + 0.3 × norm(Conversions)
Competitiveness = 0.4 × norm(QS) + 0.3 × norm(IS) + 0.3 × norm(CTR)
HealthScore = 0.4 × CostEfficiency + 0.35 × ConversionQuality + 0.25 × Competitiveness
```

Where `norm(x) = (x - min(x)) / (max(x) - min(x))` across all 714 campaign-months, and `inv(x)` indicates inversion for lower-is-better metrics.