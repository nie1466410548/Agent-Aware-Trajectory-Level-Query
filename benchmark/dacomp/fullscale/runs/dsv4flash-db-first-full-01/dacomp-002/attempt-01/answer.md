# Sales Trend Analysis: January–April 2015 and Recommendations for May–August

## 1. Overview

The dataset contains **42,816 sales transactions** from January 1 to April 30, 2015, spanning **15 major categories** with a total sales amount of approximately **¥457,390**. The period includes the **Spring Festival (Chinese New Year, Feb 19, 2015)**, which significantly influenced purchasing patterns.

---

## 2. Overall Monthly Trend

| Month | Total Sales (¥) | Transactions | Unique Customers |
|-------|----------------|-------------|-----------------|
| Jan   | 117,708.72     | 12,300      | 1,225           |
| Feb   | 141,065.00     | 9,951       | 1,059           |
| Mar   | 94,888.77      | 9,847       | 1,058           |
| Apr   | 103,727.90     | 10,718      | 1,134           |

**Key observations:**
- **February** had the highest sales (¥141K) despite lower transaction count, driven by **Spring Festival gifting** (avg unit price spiked in many categories).
- **March** saw a post-festival trough (sales down 33% from Feb).
- **April** showed recovery (up 9% from March) with increasing customer counts.

![Daily Sales Trend](figure6_daily_sales.png)
*Daily sales were highest in the two weeks leading up to Chinese New Year (Feb 19).*

---

## 3. Major Category Growth Trends

### 3.1 Monthly Sales Amount by Category

![Monthly Sales Trend by Major Category](figure1_sales_trend.png)

### 3.2 Month-over-Month Growth Rates

| Category | Jan→Feb | Feb→Mar | Mar→Apr |
|----------|---------|---------|---------|
| **Alcoholic beverages** | **+439.2%** | **-75.5%** | +16.3% |
| **Aquatic Products** | +69.1% | -19.5% | **+138.6%** |
| Daily fresh products | +19.9% | -30.8% | +24.9% |
| Vegetables and fruits | -33.0% | +46.0% | -3.2% |
| Leisure | +36.4% | -41.9% | +7.0% |
| Grain and oil | -10.0% | -30.4% | +0.2% |
| Household & Personal Care | -32.3% | +8.5% | +15.6% |
| Meat and poultry | -36.7% | -15.2% | +12.8% |
| Instant mixes | +91.4% | -62.8% | +2.2% |
| Knitwear | -0.9% | -43.8% | +48.0% |
| Cooked food | -35.1% | +20.9% | +24.0% |
| Home appliances | -57.3% | +13.9% | -85.8% |
| Household | +32.3% | -12.5% | -17.9% |
| Stationery and Sports | -14.9% | -38.3% | -12.5% |
| Baking | -14.6% | -98.8% | 0.0% |

![Growth Rate Heatmap](figure3_growth_heatmap.png)

### 3.3 Market Share Changes

![Market Share by Category](figure2_market_share.png)

| Category | Jan | Feb | Mar | Apr |
|----------|-----|-----|-----|-----|
| **Daily fresh products** | 20.5% | 19.8% | 20.4% | **23.4%** |
| **Vegetables and fruits** | 23.0% | 12.4% | 26.9% | 24.0% |
| **Leisure** | 18.9% | 20.7% | 17.9% | 17.6% |
| **Grain and oil** | 19.7% | 14.3% | 14.8% | 13.7% |
| **Alcoholic beverages** | 6.1% | **26.4%** | 9.6% | 10.3% |
| Household & Personal Care | 11.8% | 6.4% | 10.4% | 11.1% |

---

## 4. How Have Customers' Purchasing Preferences Changed?

### 4.1 Seasonal Festive Gifting (February Peak)

**Alcoholic beverages** exploded in February (+439% MoM), with the share jumping from 6% to 26%. The top subcategories:
- **Domestic Baijiu**: ¥1,650 → ¥16,086 (Feb spike) → ¥2,021 (Apr)
- **Cigarettes**: ¥1,043 → ¥8,164 (Feb) → ¥3,331 (Apr)

This reflects **Spring Festival gifting traditions** — premium baijiu and cigarettes are customary gifts. The average unit price for alcoholic beverages jumped from ¥7.67 (Jan) to ¥21.71 (Feb), confirming a shift to premium products.

### 4.2 Shift Toward Fresh and Convenient Foods

- **Refrigerated Dairy Products** (Daily fresh): +43% growth Jan→Apr (¥2,689 → ¥3,851)
- **Liquid Seasoning** (Grain and oil): +33% growth Jan→Apr (¥1,662 → ¥2,214)
- **Freshly made Chinese flour-based items** (Cooked food): +38% growth Jan→Apr
- **Aquatic Products**: Strong upward trend — chilled (+190%) and frozen (+621%) aquatic products saw massive growth Jan→Apr

### 4.3 Decline in Traditional Staple Categories

- **Grain and oil**: Sales declined 37% from Jan (¥19,493) to Apr (¥12,246). Five grains (-59%) and cooking oil (-33%) both declined significantly.
- **Meat and poultry**: Down 39% from Jan (¥9,085) to Apr (¥5,504). Pork (-38%), beef (-63%), chicken (-16%) all declined.
- **Vegetables**: Vegetables category declined 14% Jan→Apr, while fruit remained stable.

### 4.4 Leisure and Snacks: Post-Festival Decline

- **Puffed snacks**: Down 27% (¥2,050 → ¥1,505)
- **Biscuits**: Down 15% (¥3,427 → ¥2,896)
- **Instant foods** (Instant mixes): Down 27% (¥1,299 → ¥949)

### 4.5 Household & Personal Care: Stable with Seasonal Variation

- Paper products declined 27% (¥3,293 → ¥2,411), possibly due to bulk purchasing in Jan.
- Laundry supplies and hair care remained relatively stable.

### 4.6 Unit Price Trends

![Average Unit Price](figure7_unit_price.png)

The unit price spikes in February across Alcoholic beverages, Daily fresh, Leisure, and Instant mixes indicate **customers purchased premium/higher-value products during the holiday season**, then returned to regular-priced items in March-April.

---

## 5. Promotional Mix

![Promotional Mix by Category](figure5_promotional_mix.png)

- **Regular Price** accounts for ~70-80% of sales across most categories.
- **Full reduction (promotion)** was most effective for Daily fresh products (25.5% of sales) and Alcoholic beverages (11.6% of sales).
- **Limited-time promotions** and **Special offers** were notable in Household & Personal Care and Leisure categories.

---

## 6. Recommendations for May–August

### 6.1 Inventory Adjustments

| Category | Recommendation | Rationale |
|----------|---------------|-----------|
| **Daily fresh products** | **Increase inventory 20-25%** | Strongest upward trend, stable demand, especially refrigerated dairy. Summer heat increases demand for fresh dairy. |
| **Vegetables and fruits** | **Maintain/increase fruit inventory** | Fruit sales stable and resilient; summer is peak season for fruits. Vegetables declining — reduce inventory. |
| **Aquatic Products** | **Significantly increase** | +139% Apr growth; summer is peak season for fresh/frozen aquatic products. Expand chilled and frozen lines. |
| **Alcoholic beverages** | **Reduce Baijiu, maintain beer/juice** | Post-festival decline in baijiu. Summer favors beer (+281% Jan→Feb then stable) and fruit juice beverages. |
| **Meat and poultry** | **Reduce inventory** | Consistent decline across all subcategories. Grilling season may boost some cuts, but overall trend is downward. |
| **Grain and oil** | **Reduce** | Continuous decline. Liquid seasoning is the only bright spot — maintain inventory. |
| **Leisure/Snacks** | **Maintain pastries, reduce biscuits/puffed** | Pastries stable; biscuits and puffed snacks declining. Consider summer-focused snacks (ice cream, etc.). |
| **Household & Personal Care** | **Stable with summer focus** | Maintain laundry supplies, increase personal care products (hair care, skincare) for summer. |
| **Instant mixes** | **Reduce** | Post-festival decline. Summer may see some increase in instant noodles, but overall trend is downward. |
| **Knitwear** | **Reduce significantly** | Seasonal decline in spring; further decline in summer. |

### 6.2 Category Strategy Adjustments

1. **Emphasize Fresh and Chilled Categories**: The shift toward **refrigerated dairy, aquatic products, and fresh produce** is clear. For May-August, expand the chilled/fresh product aisle and invest in cold chain logistics.

2. **Summer Seasonal Products**: 
   - Increase **beer, carbonated beverages, fruit juice, and purified water** inventory (Alcoholic beverages category).
   - Introduce **ice cream and frozen desserts** (currently not prominent in the data).
   - Stock **summer fruits** (watermelon, stone fruits) in the Vegetables and fruits category.

3. **Promotional Strategy**:
   - **Full reduction promotions** were most effective for Daily fresh products (25.5% of sales) — use this for fresh categories in summer.
   - **Limited-time promotions** worked well for Household & Personal Care (11.7%) and Leisure (7.7%).
   - Consider **bundle promotions** (e.g., barbecue meat + beer + condiments).

4. **Reduce Overstock in Declining Categories**:
   - **Grain and oil** (especially five grains and cooking oil) — reduce shelf space.
   - **Meat and poultry** (especially beef and pork) — reduce inventory, focus on grilling-appropriate cuts.
   - **Knitwear** — clear seasonal inventory.

5. **Customer Retention**: Customer count declined from 1,225 (Jan) to 1,058 (Mar), recovering to 1,134 (Apr). For summer, consider:
   - Loyalty programs targeting fresh food buyers.
   - Cross-category promotions (e.g., buy meat, get discount on beer/condiments).
   - Weekend specials to drive traffic.

### 6.3 Key Risks to Monitor

- **Grain and oil** category may continue declining due to changing dietary habits (low-carb trends, etc.).
- **Meat and poultry** demand may recover slightly for summer grilling but the overall trend is negative.
- **Alcoholic beverages** will not see another Feb-level spike until the next major holiday season (Mid-Autumn Festival in September).

---

## 7. Summary of Key Insights

| Metric | Jan | Feb | Mar | Apr | Trend |
|--------|-----|-----|-----|-----|-------|
| Total Sales (¥K) | 117.7 | 141.1 | 94.9 | 103.7 | V-shaped with Spring Festival peak |
| Avg Transaction Value (¥) | 9.57 | 14.18 | 9.64 | 9.68 | Spike in Feb, then normalizes |
| Unique Customers | 1,225 | 1,059 | 1,058 | 1,134 | Recovery in Apr |
| Top Category (share) | Veg&Fruit (23%) | Alcoholic (26%) | Veg&Fruit (27%) | Veg&Fruit (24%) | Seasonal shift |
| Fastest Growing (Apr) | — | Alcoholic (+439%) | Veg&Fruit (+46%) | Aquatic (+139%) | Seasonal rotation |

**The dominant trend is a shift from traditional staple goods (grain, oil, meat) toward fresh, convenient, and refrigerated products.** Summer planning should focus on expanding fresh/chilled categories, seasonal beverages, and targeted promotions for grilling and outdoor dining occasions.

---

*Figures referenced in this report:*
- `figure1_sales_trend.png` — Monthly sales by major category
- `figure2_market_share.png` — Market share changes
- `figure3_growth_heatmap.png` — Month-over-month growth rates
- `figure4_intermediate_trends.png` — Subcategory trends
- `figure5_promotional_mix.png` — Promotional mix by category
- `figure6_daily_sales.png` — Daily sales with Spring Festival
- `figure7_unit_price.png` — Average unit price by category