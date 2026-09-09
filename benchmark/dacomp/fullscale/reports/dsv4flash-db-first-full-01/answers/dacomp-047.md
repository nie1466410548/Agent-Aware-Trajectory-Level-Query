<!-- Reading copy: local artifact links normalized. Original answer is preserved at ../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/answer.md -->

# Fruit-and-Vegetable Combination Replenishment Recommendations for July 2023

## Executive Summary

Based on a comprehensive analysis of vegetable category interrelationships, single-item sales volumes, seasonal characteristics, and recent 2023 trends, we recommend **three fruit-and-vegetable combinations** for replenishment in July 2023. These combinations are designed to maximize seasonal demand, leverage complementary purchase patterns, and ensure category diversity for balanced replenishment.

---

## Data Overview

| Dataset | Records | Date Range | Items |
|---------|---------|------------|-------|
| Sales Records | 878,503 | 2020-07-01 to 2023-06-30 | 246 items |
| Purchase Price | 55,982 | 2020-07-01 to 2023-06-30 | 251 items |
| Products | 251 | — | 6 categories |

**Categories:** Leafy & variegated (100 items), Edible Fungi (72), Pepper Category (45), Hydroponic Rhizome (19), Eggplant group (10), Cauliflower group (5).

---

## Analytical Approach

### 1. Category-Level Interrelationships

Daily sales correlation between categories reveals strong positive relationships across all categories, indicating that overall demand drives the market. Key correlations:

| Category Pair | Correlation |
|:---|---:|
| Pepper Category ~ Edible Fungi | **0.687** |
| Leafy & variegated ~ Pepper Category | **0.659** |
| Leafy & variegated ~ Cauliflower group | **0.627** |
| Eggplant group ~ Cauliflower group | 0.312 (lowest) |

*Eggplant group is the most independent category, offering diversification benefits.*

![Category Correlation Matrix](<../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/work/category_correlation.png>)

### 2. Item-Level Sales & Seasonality

Items with **July seasonality index > 1.0** (meaning their July daily sales exceed their annual average) are prime candidates for July replenishment:

| Item | Category | July Volume (kg) | July Seasonality |
|:---|---:|---:|---:|
| Sweet Potato Vine Tips | Leafy & variegated | 1,404 | **3.27** |
| Water Spinach | Leafy & variegated | 1,402 | **2.45** |
| Yellow Chinese Cabbage (2) | Leafy & variegated | 1,335 | **1.77** |
| Yunnan Leaf Lettuce (portion) | Leafy & variegated | active in 2023 | **1.05** |
| Yunnan Romaine Lettuce (portion) | Leafy & variegated | active in 2023 | **1.23** |
| Broccoli | Cauliflower group | 2,909 | **1.22** |
| Shanghai Bok Choy | Leafy & variegated | 918 | **1.20** |
| Spiral chili pepper | Pepper Category | 932 | **1.17** |
| Purple Eggplant (2) | Eggplant group | 1,337 | **1.09** |
| Milk Bok Choy (portion) | Leafy & variegated | active in 2023 | **1.22** |
| Green-stem Loose Cauliflower | Cauliflower group | 1,224 | **1.05** |

*Items with July seasonality > 1.0: 63 items identified.*

### 3. Item-Level Correlations (Co-Purchase Patterns)

Pairwise daily sales correlations reveal which items are complementary:

| Strongest Positive Pairs | Correlation |
|:---|---:|
| Sweet Potato Vine Tips ~ Water Spinach | **0.649** |
| Shanghai Bok Choy ~ Yunnan Romaine Lettuce | **0.616** |
| Yunnan Leaf Lettuce ~ Yunnan Romaine Lettuce | **0.593** |
| Bubble Pepper (Premium) ~ Green-stem Loose Cauliflower | **0.573** |
| Peeled Lotus Root (1) ~ Xixia shiitake (1) | **0.540** |

| Notable Negative Pairs (Substitutes) | Correlation |
|:---|---:|
| Bubble Pepper (Premium) ~ Wuhu green pepper (1) | **-0.460** |
| Peeled Lotus Root (1) ~ Water Spinach | **-0.417** |

![Item Correlation Matrix](<../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/work/item_correlation.png>)

### 4. Recent 2023 Trend (Jan–Jun 2023)

Items with **rising June 2023** trend (positive month-over-month change) are well-positioned for July:

| Item | May 2023 (kg/day) | June 2023 (kg/day) | Change |
|:---|---:|---:|---:|
| Yunnan Leaf Lettuce (portion) | 34.23 | 36.83 | **+2.61** |
| Yunnan Romaine Lettuce (portion) | 20.74 | 22.67 | **+1.92** |
| Sweet Potato Vine Tips | 5.03 | 6.34 | **+1.31** |
| Bird's-eye Chili (portion) | 21.69 | 22.87 | **+1.18** |
| Water Spinach | 13.95 | 14.45 | **+0.50** |
| Milk Bok Choy (portion) | 11.86 | 12.06 | **+0.20** |

*Broccoli (14.35 kg/day), Purple Eggplant (15.73 kg/day), and White Button Mushroom (13.37 kg/day) are stable high-volume items.*

### 5. Profitability & Loss Rates

| Item | Avg Retail (yuan/kg) | Avg Margin (yuan/kg) | Loss Rate (%) |
|:---|---:|---:|---:|
| Broccoli | 9.90 | 3.31 | 9.3% |
| Purple Eggplant (2) | 8.68 | 2.95 | 6.1% |
| Shanghai Bok Choy | 7.52 | 3.07 | 14.4% |
| Yunnan Leaf Lettuce (portion) | ~8.08 | ~3.15 | 15.3% |
| Water Spinach | 5.47 | 2.00 | 13.6% |
| Sweet Potato Vine Tips | 5.99 | 2.37 | 8.4% |
| Yellow Chinese Cabbage (2) | 6.75 | 2.84 | 15.6% |
| Milk Bok Choy (portion) | ~7.08 | ~2.63 | 12.8% |

---

## Recommended Three Combinations for July 2023 Replenishment

### Combination 1: Summer Leafy Greens Bundle
**Items:** Yunnan Leaf Lettuce (portion) + Water Spinach + Sweet Potato Vine Tips

| Rationale | Evidence |
|:---|:---|
| **Strong July seasonality** | Water Spinach (2.45), Sweet Potato Vine Tips (3.27), Yunnan Leaf Lettuce (1.05) — all peak in July |
| **Complementary pairs** | Sweet Potato Vine Tips ~ Water Spinach r=0.65 (strongest positive correlation) |
| **Rising 2023 trend** | All three show positive June 2023 growth |
| **High volume** | Combined July historical volume ~5,789 kg |
| **Category** | All Leafy & variegated — these are signature summer vegetables |

**Expected July 2023 daily replenishment:** ~55–65 kg/day total across the three items.

### Combination 2: Cross-Category Staples
**Items:** Broccoli + Yunnan Romaine Lettuce (portion) + Purple Eggplant (2)

| Rationale | Evidence |
|:---|:---|
| **Category diversity** | Cauliflower group + Leafy & variegated + Eggplant group — reduces risk |
| **High July volume** | Broccoli (2,909 kg), Yunnan Romaine Lettuce (1,683 kg), Purple Eggplant (1,337 kg) |
| **Positive seasonality** | Broccoli (1.22), Yunnan Romaine Lettuce (1.23), Purple Eggplant (1.09) |
| **Rising trend** | Yunnan Romaine Lettuce (portion) rising to 22.7 kg/day in June |
| **Profitability** | Broccoli margin 3.31 yuan/kg, Purple Eggplant margin 2.95 yuan/kg, good margins |
| **Low loss rates** | Purple Eggplant 6.1%, Broccoli 9.3% |

**Expected July 2023 daily replenishment:** ~50–60 kg/day total.

### Combination 3: Chinese Greens & Chili Variety
**Items:** Milk Bok Choy (portion) + Yellow Chinese Cabbage (2) + Bird's-eye Chili (portion)

| Rationale | Evidence |
|:---|:---|
| **Strong July seasonality** | Yellow Chinese Cabbage (1.77), Milk Bok Choy (1.22) |
| **Traditional cooking staples** | These are core ingredients in Chinese cuisine with consistent demand |
| **Rising trend** | Milk Bok Choy (portion) rising to 12.1 kg/day, Bird's-eye Chili (portion) rising to 22.9 kg/day in June |
| **Complementary roles** | Leafy greens + chili pepper (condiment) — provides meal variety |
| **High volume** | Bird's-eye Chili (portion) is #3 by 2023 volume (4,844 kg YTD) |

**Expected July 2023 daily replenishment:** ~40–50 kg/day total.

---

## Key Figures

- **Category Correlation Matrix:** Shows strong positive correlations between all categories, with Eggplant group being the most independent.
- **Item Correlation Matrix:** Reveals complementary pairs for co-replenishment.
- **Monthly Seasonality Plot:** Demonstrates July peaks for Water Spinach and Sweet Potato Vine Tips.
- **Final Recommendation Summary:** Four-panel figure with correlation heatmap, seasonality bars, recent trend, and recommendation summary.

![Final Recommendation Summary](<../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/work/final_recommendation.png>)

---

## Limitations

1. **Limited July data for 2023-introduced items:** Portion-size items (introduced mid-2022) have only one partial July observation, so their seasonality was estimated from shorter data spans.
2. **No transaction-level basket data:** Each scan is a single-item basket, preventing traditional market basket analysis. Daily co-occurrence was used as a proxy.
3. **External factors** (weather, holidays, supply chain disruptions) that affect July 2023 demand were not modeled.
4. **Forecast uncertainty:** The 2020–2023 data includes COVID-era demand patterns that may not fully represent 2023 conditions.

## Conclusion

The three recommended combinations balance **seasonal demand** (July-peaking items), **complementary interrelationships** (positively correlated items), **category diversity** (spreading risk across categories), and **recent momentum** (rising 2023 trends). These combinations provide a data-driven replenishment strategy for July 2023 that maximizes expected sales while minimizing replenishment risk.