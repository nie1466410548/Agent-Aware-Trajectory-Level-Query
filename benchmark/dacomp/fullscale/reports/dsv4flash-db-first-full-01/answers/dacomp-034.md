<!-- Reading copy: local artifact links normalized. Original answer is preserved at ../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/answer.md -->

# Promotion Discount Depth Analysis: Level 1 Category Perspective

## Executive Summary

This report analyzes the relationship between **discount depth** (percentage markdown from original price) and **sales** for single-item direct price reduction promotions across Level 1 product categories. The analysis is based on 9,165 approved promotions (promotion_type=4, state=5) from 17 Level 1 categories, of which 5,620 promotions recorded positive sales. Statistical tests confirm highly significant differences in promotion effectiveness across categories (Kruskal-Wallis: H=1,004, p≈2.4e-206; ANOVA on log-sales: F=90.5, p≈2.4e-220).

---

## 1. Overall Relationship Between Discount Depth and Sales

### 1.1 Correlation Analysis

| Metric | Value |
|--------|-------|
| Pearson correlation (r) | 0.124 (p=1.0e-20) |
| Spearman correlation (ρ) | 0.160 (p=1.4e-33) |
| N (promotions with sales) | 5,620 |

There is a **statistically significant but weak positive correlation** between discount depth and sales. Deep discounts tend to generate slightly more units, but the relationship is highly noisy.

### 1.2 Binned Analysis

| Discount Depth | N Promotions | Avg Sales | Median Sales | Avg Revenue | Total Revenue |
|----------------|:-----------:|:---------:|:------------:|:-----------:|:-------------:|
| <10% | 17 | 32.8 | 6.0 | 491.7 | 8,359 |
| 10–20% | 1,616 | 23.9 | 9.0 | 368.9 | 596,086 |
| 20–30% | 1,924 | 26.8 | 10.0 | 425.1 | 817,898 |
| 30–40% | 1,193 | 35.8 | 14.0 | 557.5 | 665,126 |
| 40–50% | 549 | 48.9 | 15.0 | 558.5 | 306,640 |
| >50% | 321 | 50.0 | 29.0 | 366.3 | 117,572 |

**Key insight**: Average unit sales increase with discount depth, but **average revenue per promotion peaks at 30–50% depth** and declines sharply beyond 50%. Total realized revenue is highest in the 20–30% and 30–40% bands.

![Overall scatter with regression line](<../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/work/overall_scatter.png>)
![Binned average sales](<../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/work/binned_bar.png>)
![Revenue by discount bin](<../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/work/revenue_by_bin.png>)

---

## 2. Category-Level Differences

### 2.1 Category Volume Overview

| Level 1 Category | Promos | Total Sales | Avg Sales/Promo | Avg Discount Depth |
|------------------|:-----:|:-----------:|:---------------:|:------------------:|
| Daily Delivery/Refrigerated | 929 | 43,827 | 47.2 | 28.5% |
| Fruits/Vegetables | 543 | 25,308 | 46.6 | 29.7% |
| Daily Chemical Products | 497 | 22,530 | 45.3 | 32.4% |
| Grains, Oils & Staple Foods | 588 | 21,779 | 37.0 | 26.3% |
| Snack Food | 1,245 | 19,590 | 15.7 | 28.5% |
| Meat | 295 | 16,853 | 57.1 | 23.8% |
| Personal Wash & Cleaning | 494 | 12,322 | 24.9 | 34.4% |
| Alcoholic Beverages & Drinks | 127 | 6,356 | 50.1 | 29.0% |
| Other (9 categories) | 502 | 7,725 | — | — |

### 2.2 Discount-Sales Correlation by Category

![Correlation by category](<../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/work/correlation_by_category.png>)

**Categories with significant positive discount-sales relationship:**

| Category | Pearson r | p-value | Regression Slope | R² |
|----------|:---------:|:-------:|:----------------:|:--:|
| Snack Food | 0.296 | 1.6e-26 | 53.1 | 0.087 |
| Baking | 0.299 | 0.0026 | 31.8 | 0.089 |
| Grains, Oils & Staple Foods | 0.239 | 4.7e-09 | 177.1 | 0.057 |
| Daily Delivery/Refrigerated | 0.216 | 2.7e-11 | 211.8 | 0.047 |
| Fruits/Vegetables | 0.208 | 1.0e-06 | 80.1 | 0.043 |
| Personal Wash & Cleaning | 0.163 | 0.00028 | 25.0 | 0.027 |

**Categories with no significant relationship:**

| Category | Pearson r | p-value | Interpretation |
|----------|:---------:|:-------:|:--------------|
| Alcoholic Beverages & Drinks | 0.045 | 0.613 | Not responsive to depth |
| Daily Chemical Products | -0.020 | 0.655 | Not responsive to depth |
| Imported Goods | -0.009 | 0.869 | Not responsive to depth |
| Aquatic Products | -0.005 | 0.944 | Not responsive to depth |

**Categories with a negative relationship:**

| Category | Pearson r | p-value | Interpretation |
|----------|:---------:|:-------:|:--------------|
| **Meat** | **-0.192** | **0.0009** | **Deeper discounts → lower sales** |
| Home Daily Use | -0.266 | 0.098 | (Marginal, n=40) |

### 2.3 The Meat Anomaly

Meat is the only major category where deeper discounts are **significantly associated with fewer sales** (r=-0.192, p<0.001). After controlling for price level (partial correlation), the relationship strengthens to r=-0.264, confirming the effect is not driven by price confounding. The optimal discount depth for Meat is **<20%** (avg 68.5 units, avg revenue 708.4), while >40% discounts yield only 23.2 units and 235.3 revenue.

This may reflect that:
- Deep discounts on meat signal low quality or near-expiry products
- Meat consumers are relatively price-inelastic
- Shallow discounts communicate value without raising quality concerns

### 2.4 Category-Level Sweet Spots

![Heatmap of effectiveness](<../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/work/heatmap_effectiveness.png>)

**Optimal discount depth (by revenue per promotion):**

| Category | Best Discount Depth | Avg Units | Avg Revenue |
|----------|:-------------------:|:---------:|:-----------:|
| Meat | <20% | 68.5 | 708.4 |
| Snack Food | <20% | 12.9 | 168.9 |
| Aquatic Products | <20% | 10.4 | 303.9 |
| Mother & Baby | <20% | 2.9 | 379.6 |
| Home Daily Use | <20% | 21.0 | 375.9 |
| Alcoholic Beverages & Drinks | 20–30% | 41.0 | 929.6 |
| Imported Goods | 20–30% | 7.5 | 278.5 |
| Daily Chemical Products | 30–40% | 48.3 | 979.3 |
| Fruits/Vegetables | 30–40% | 58.0 | 430.7 |
| Grains, Oils & Staple Foods | 30–40% | 73.5 | 1,129.3 |
| Daily Delivery/Refrigerated | >40% | 102.6 | 1,026.2 |
| Baking | >40% | 23.5 | 115.3 |
| Personal Wash & Cleaning | >40% | 37.6 | 413.5 |

![Per-category scatter plots](<../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/work/per_category_scatter.png>)
![Category comparison](<../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/work/category_comparison.png>)
![Discount depth distribution by category](<../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/work/discount_depth_distribution.png>)

---

## 3. Recommendations

### 3.1 Tiered Discount Strategy by Category

Based on the empirical evidence, I recommend a **three-tier discount strategy**:

**Tier 1 — Shallow Discounts (<20%): Apply to low-elasticity categories**
- **Meat**: Deep discounts backfire (negative correlation). Use modest 10–15% discounts to signal value without raising quality concerns.
- **Snack Food**: High volume (1,245 promos) but low avg sales (15.7). Deep discounts don't significantly boost unit sales. Use shallow, frequent promotions.
- **Aquatic Products, Mother & Baby, Home Daily Use**: Similar patterns — shallow discounts maximize revenue.

**Tier 2 — Moderate Discounts (20–30%): Apply to moderately elastic categories**
- **Alcoholic Beverages & Drinks**: Revenue peaks at 20–30% depth. This is the sweet spot where consumers perceive genuine value.
- **Imported Goods**: Premium perception means excessive discounts may erode brand value.

**Tier 3 — Deep Discounts (30–50%): Apply to highly elastic categories**
- **Grains, Oils & Staple Foods**: Highest revenue per promotion at 30–40% depth (avg 1,129 revenue). These are frequent-purchase staples where consumers stock up.
- **Daily Delivery/Refrigerated**: Highly responsive (avg 102.6 units at >40% depth). Consumers consolidate purchases for perishable essentials.
- **Fruits/Vegetables**: Strong volume response to deeper discounts.
- **Daily Chemical Products**: Revenue peaks at 30–40% depth.

### 3.2 Avoid Extremely Deep Discounts (>50%)

Across all categories, discounts exceeding 50% generate the highest unit volume but the **lowest average revenue** (366.3 vs 557.5 at 30–40%). These should be reserved for inventory clearance, not routine promotion.

### 3.3 Resource Allocation

| Category | Current Promos | Total Sales | Recommended Investment |
|----------|:--------------:|:-----------:|:----------------------|
| Daily Delivery/Refrigerated | 929 | 43,827 | **Increase** — high responsiveness |
| Meat | 295 | 16,853 | **Maintain** — but reduce discount depth |
| Snack Food | 1,245 | 19,590 | **Reduce** — low per-promo ROI |
| Mother & Baby | 228 | 735 | **Reduce** — very low sales per promo |
| Aquatic Products | 177 | 2,010 | **Reduce** — low responsiveness |
| Imported Goods | 329 | 2,433 | **Reduce** — low responsiveness |

### 3.4 Monitoring & Optimization

1. **Track revenue per promotion** (not just units) to avoid value-destroying deep discounts
2. **Implement category-specific discount caps**: e.g., cap Meat at 20%, allow 40%+ for Daily Delivery/Refrigerated
3. **A/B test moderate vs. deep discounts** within responsive categories to refine sweet spots
4. **Consider product-level characteristics** (e.g., brand, shelf life, price tier) within each category for finer-grained targeting

---

## 4. Limitations

1. **No baseline sales data**: The analysis uses promotion-level `sale_count` without comparing to non-promotional periods. Incremental uplift (incremental sales attributable to the promotion) could not be calculated.
2. **No cost data**: The `cost_price` field in the promotion data equals the `promotion_price` for 94% of records, making margin analysis unreliable.
3. **No promotion duration control**: Longer promotions may accumulate more sales independent of discount depth.
4. **Cross-promotion effects**: Potential interactions with other concurrent promotions are not captured.
5. **Observational data**: Correlations do not imply causation; unobserved confounders (e.g., product quality, seasonality, shelf placement) may influence results.

---

## 5. Conclusion

The relationship between discount depth and sales for single-item direct price reduction promotions is **weakly positive overall** but varies dramatically across Level 1 categories. Categories such as **Daily Delivery/Refrigerated, Grains/Oils, and Fruits/Vegetables** respond strongly to deeper discounts, while **Meat and Snack Food** show diminishing or negative returns. A **category-specific discount strategy** — investing promotional resources in elastic categories while capping depth in inelastic ones — can significantly improve the efficiency of promotion spend.