<!-- Reading copy: local artifact links normalized. Original answer is preserved at ../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/answer.md -->

# Market Analysis: Watch Count & Showings Factors

## Overview

This report analyzes 29,975 home listings to identify the top-10 combinations of **Floor Plan, Decoration, Floor, and Orientation** that attract the highest **Watch Count**, and investigates which factors affect **Showings**.

---

## Part 1: Top 10 Combinations by Average Watch Count

The table below shows the top-10 home feature combinations ranked by average Watch Count (minimum 5 listings per combination). The overall market average Watch Count is **5.85**.

| Floor Plan | Decoration | Floor | Orientation | Listings | Avg Watch | Med Watch | Max Watch | Avg Showings |
|---|---|---|---|---|---|---|---|---|
| 4 bedrooms, 2 living rooms | High-quality renovation | 18th floor | North | 6 | **56.50** | 12.5 | 275 | 5.00 |
| 3 bedrooms 2 living rooms | Simple renovation | 17th floor | East | 6 | **43.50** | 38.5 | 106 | 1.33 |
| 2 bedrooms, 2 living rooms | High-quality renovation | 30th floor | North | 5 | **30.60** | 20.0 | 81 | 1.60 |
| 2 bedrooms, 1 living room | High-quality renovation | 6-story building | North | 10 | **30.50** | 13.0 | 119 | 2.50 |
| 3 bedrooms 2 living rooms | High-quality renovation | 34th floor | Southwest | 6 | **29.67** | 3.5 | 127 | 3.33 |
| 2 bedrooms, 2 living rooms | High-quality renovation | 5th floor | West | 5 | **28.00** | 8.0 | 104 | 1.60 |
| 3 bedrooms 2 living rooms | High-quality renovation | 7th floor | North | 5 | **25.20** | 11.0 | 58 | 2.40 |
| 1 bedroom 1 living room | Simple renovation | 8 Floors | South | 5 | **25.00** | 6.0 | 104 | 2.40 |
| 3 bedrooms 2 living rooms | Unfinished | 40th Floor | South | 6 | **23.33** | 1.5 | 110 | 3.33 |
| 2 bedrooms, 2 living rooms | High-quality renovation | 16th floor | Southeast | 5 | **23.20** | 20.0 | 65 | 5.40 |

**Key observations:**
- The top combinations average **23–57 Watch Counts**, 4–10× the market average of 5.85.
- **High-quality renovation** dominates (7 of 10 combos).
- **North-facing** and **East-facing** orientations appear disproportionately in the top combos.
- Specific floor levels (e.g., 18th, 17th, 30th, 34th) appear frequently.
- The top-10 combos are niche (59 listings, 0.20% of market), suggesting high watch counts are achieved by rare, specific combinations.

![Top 10 combinations by average Watch Count](<../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/work/fig1_top10_combos.png>)

---

## Part 2: Factors Affecting Showings

### 2.1 Univariate Analysis

**By Decoration** (ANOVA p=0.61 — not significant):
| Decoration | Avg Showings | Listings |
|---|---|---|
| Simple renovation | 2.87 | 9,002 |
| Unfinished | 2.82 | 2,780 |
| High-quality renovation | 2.80 | 17,903 |
| Luxuriously renovated | 2.71 | 287 |

**By Orientation** (ANOVA p=5.9×10⁻¹⁷ — highly significant):
| Orientation | Avg Showings | Listings |
|---|---|---|
| **South** | **2.94** | 23,342 |
| Southeast | 2.57 | 924 |
| East | 2.46 | 1,348 |
| Northeast | 2.45 | 778 |
| Northwest | 2.43 | 857 |
| Southwest | 2.37 | 824 |
| West | 2.36 | 1,022 |
| North | 2.18 | 877 |

**By Floor Category** (ANOVA p=1.4×10⁻¹⁶ — highly significant):
| Floor Category | Avg Showings | Listings |
|---|---|---|
| **High floor** (≥19) | **3.13** | 8,438 |
| Mid floor (7–18) | 2.74 | 13,374 |
| Building total | 2.73 | 6,597 |
| Low floor (≤6) | 2.33 | 1,563 |

**By Bedrooms** (ANOVA p=6.0×10⁻²⁹ — highly significant):
| Bedrooms | Avg Showings | Listings |
|---|---|---|
| **3** | **3.05** | 13,966 |
| 2 | 2.81 | 7,892 |
| 4 | 2.68 | 5,692 |
| 1 | 2.06 | 1,479 |
| 5 | 1.84 | 729 |

**Watch Count vs Showings** (Spearman ρ=0.077, p=2.2×10⁻⁴⁰):
As watch count increases, showings rise:
- 0 watches: 2.05 showings
- 1–2 watches: 2.55 showings
- 3–5 watches: 3.14 showings
- 6–10 watches: 3.24 showings
- 11–20 watches: 3.35 showings
- 21–50 watches: 3.41 showings
- 51–100 watches: 4.24 showings
- 100+ watches: 4.29 showings

### 2.2 Multivariate OLS Regression (R²=0.039)

Controlling for all factors simultaneously, the significant predictors of Showings (p<0.01) are:

| Factor | Coefficient | Effect Direction |
|---|---|---|
| South orientation | +0.592 | **Strong positive** |
| Decoration: Unfinished | +0.418 | Positive |
| Living rooms | +0.393 | Positive |
| Decoration: Simple renovation | +0.281 | Positive |
| Bedrooms | +0.174 | Positive |
| **Watch Count** | **+0.043** | **Positive (each +1 watch → +0.043 showings)** |
| **Floor level** | **+0.036** | **Positive (higher floor → more showings)** |
| Area (sqm) | −0.013 | Negative (larger area → fewer showings, controlling for rooms) |
| Luxuriously renovated | −0.054 | Not significant |
| North, Northeast, Northwest, etc. | varied | Not significant vs. baseline |

Notable: **Featured** listings (not in the original four factors but a strong confounder) average 8.19 watches and 7.58 showings vs. 5.68 and 2.48 for non-featured.

![Factors affecting Showings](<../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/work/fig2_showings_factors.png>)

![Watch Count by factors](<../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/work/fig3_watch_factors.png>)

![Watch Count vs Showings scatter](<../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/work/fig4_watch_vs_showings.png>)

---

## Summary of Findings

### Top-10 Watch Count Combinations
The highest-watched combinations are specific, rare, and share these traits:
- **High-quality renovation** or **Simple renovation** (not luxury)
- **Non-standard orientations** (North, East, Southwest) — less common than South, thus more distinctive
- **Mid-to-high floor levels** or notable floors (e.g., 18th, 30th, 34th, 40th)
- **3–4 bedroom** floor plans

### Factors Affecting Showings
1. **South orientation** is the strongest positive factor (+0.59 showings vs. baseline).
2. **Higher floor levels** increase showings (+0.036 per floor).
3. **More bedrooms and living rooms** increase showings.
4. **Unfinished or Simple renovation** (vs. High-quality) yields slightly more showings.
5. **Watch Count** has a small but significant positive effect on showings (0.043 per watch).
6. **Larger area** (controlling for room count) reduces showings, possibly because larger homes are more expensive or less in demand.
7. **Featured status** is a major confounder: featured listings receive 3.05× more showings on average.

### Limitations
- The overall OLS model explains only 3.9% of Showings variance, indicating many unobserved factors (location, price, marketing, seasonality) matter greatly.
- The top-10 combinations represent only 0.20% of the market; larger-sample combinations are more representative.
- **Date Published** is a confounder: older listings accumulate more watches but newer ones get more active showings.
- The **Floor** field mixes unit floor levels and building total floors, requiring parsing that may lose nuance.