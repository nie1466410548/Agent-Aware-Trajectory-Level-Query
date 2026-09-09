# Sales Trends and Regional Manager Performance Analysis (2015–2018)

## Executive Summary

This report analyzes sales trends for three major product categories (Office Supplies, Technology, Furniture) from 2015 to 2018, identifies the fastest-growing category each year, and assesses regional manager performance across six regions in China.

---

## 1. Data Overview

The dataset contains **9,959 order line items** spanning **4,321 unique orders** from **January 2015 to December 2018**. Six regions are managed by individual Regional Managers:

| Region | Regional Manager | Total Orders | Total Sales | Total Profit |
|--------|---------|-------------|-------------|-------------|
| East China | Hong Guang | 1,226 | $4,684,506 | $607,219 |
| Central South | Fan Cai | 1,095 | $4,137,415 | $670,885 |
| Northeast | Chu Jie | 752 | $2,681,567 | $242,192 |
| North China | Yin Lian | 601 | $2,447,301 | $431,053 |
| Southwest | Bai Dewei | 414 | $1,303,125 | $97,637 |
| Northwest | Yang Jian | 233 | $815,040 | $98,553 |

---

## 2. Category Sales Trends (2015–2018)

### 2.1 Sales Growth by Category

All three categories experienced substantial growth over the four-year period, with **Furniture** showing the highest Compound Annual Growth Rate (CAGR):

| Category | 2015 Sales | 2018 Sales | Total Growth | CAGR |
|----------|-----------|-----------|-------------|------|
| **Furniture** | $1,036,266 | $1,987,756 | **+91.82%** | **24.25%** |
| **Technology** | $944,943 | $1,810,064 | **+91.55%** | **24.19%** |
| **Office Supplies** | $949,848 | $1,664,618 | **+75.25%** | **20.56%** |

![Category Sales Trends](work/category_sales_trends.png)

*Figure 1: Left — Absolute sales trends; Center — Year-over-year growth rates; Right — Profit margins by category.*

### 2.2 Fastest-Growing Category Each Year

| Year | Fastest-Growing Category | YoY Growth | Runner-Up | Growth |
|------|------------------------|-----------|-----------|-------|
| **2016** | **Furniture** | **+25.22%** | Technology | +23.77% |
| **2017** | **Office Supplies** | **+33.35%** | Technology | +32.05% |
| **2018** | **Furniture** | **+40.71%** | Office Supplies | +29.40% |

**Key observations:**
- **Furniture** was the fastest-growing category in 2 out of 3 years (2016 and 2018), with an especially strong surge of **+40.71% in 2018**.
- **Office Supplies** led in 2017 with +33.35%, driven by a significant expansion in order volume (from 4,529 to 5,644 units).
- **Technology** consistently ranked second in 2016 and 2017, but dropped to third in 2018 (+17.2%), suggesting possible market saturation or competitive pressure.

### 2.3 Category Sales Share Evolution

![Category Share](work/category_share.png)

*Figure 2: Year-over-year category sales share breakdown.*

The category sales mix remained relatively stable, with Furniture increasing its share from 35.4% in 2015 to 36.4% in 2018, Technology growing from 32.2% to 33.1%, and Office Supplies declining slightly from 32.4% to 30.5%.

### 2.4 Profitability by Category

| Category | Total Sales | Total Profit | Profit Margin |
|----------|------------|-------------|--------------|
| **Office Supplies** | $3,963,590 | $757,640 | **19.12%** |
| **Technology** | $3,866,601 | $751,163 | **19.43%** |
| **Furniture** | $4,723,422 | $638,736 | **13.53%** |

Technology and Office Supplies have strong profit margins (~19%), while Furniture lags at 13.53% despite leading in sales volume. This suggests Furniture's rapid growth may come at the cost of margin compression.

---

## 3. Regional Manager Performance Assessment

![Regional Manager Performance](work/regional_manager_performance.png)

*Figure 3: Four-panel view of regional manager performance metrics: total sales, profit margin, return rate, and growth.*

### 3.1 Sales Volume & Growth

| Rank | Region | Manager | 2015 Sales | 2018 Sales | Growth 2015→2018 | Avg Order Value |
|------|--------|---------|-----------|-----------|-----------------|----------------|
| 1 | Northeast | Chu Jie | $500,006 | $951,004 | **+90.20%** | $3,566 |
| 2 | Southwest | Bai Dewei | $223,253 | $386,098 | **+72.94%** | $3,148 |
| 3 | North China | Yin Lian | $558,297 | $875,118 | **+56.74%** | $4,072 |
| 4 | Northwest | Yang Jian | $181,431 | $270,876 | **+49.30%** | $3,498 |
| 5 | East China | Hong Guang | $767,158 | $1,567,687 | **+104.32%** | $3,821 |
| 6 | Central South | Fan Cai | $700,912 | $1,411,656 | **+101.38%** | $3,778 |

**Absolute growth leaders:** Hong Guang (East China) and Fan Cai (Central South) drove the highest absolute sales increases, adding over $800K and $700K respectively from 2015 to 2018.

**Relative growth leaders:** Hong Guang's East China region leads with **+104.32%** total growth, followed closely by Fan Cai's Central South at +101.38%. Chu Jie's Northeast also showed strong relative growth at +90.20%.

### 3.2 Profitability & Efficiency

| Rank | Region | Manager | Profit Margin | Avg Profit/Order | Avg Discount |
|------|--------|---------|-------------|-----------------|-------------|
| 1 | **North China** | **Yin Lian** | **17.61%** | **$717.23** | **5.41%** |
| 2 | Central South | Fan Cai | 16.22% | $612.68 | 8.99% |
| 3 | East China | Hong Guang | 12.96% | $495.28 | 11.25% |
| 4 | Northwest | Yang Jian | 12.09% | $422.98 | 11.17% |
| 5 | Northeast | Chu Jie | 9.03% | $322.06 | 14.09% |
| 6 | Southwest | Bai Dewei | 7.49% | $235.84 | 14.57% |

**Yin Lian (North China)** stands out with the highest profit margin (17.61%) and lowest discount rate (5.41%), suggesting a premium pricing strategy with disciplined discounting. Despite having lower total sales volume, North China achieves the highest per-order profit ($717).

**Bai Dewei (Southwest)** has the lowest profit margin (7.49%) and highest discount rate (14.57%), pointing to a volume-focused strategy with heavy discounting that depresses profitability.

### 3.3 Return Rates

| Region | Manager | Return Rate |
|--------|---------|-----------|
| Northwest | Yang Jian | 13.30% |
| Southwest | Bai Dewei | 11.59% |
| Northeast | Chu Jie | 11.17% |
| East China | Hong Guang | 10.85% |
| Central South | Fan Cai | 10.50% |
| **North China** | **Yin Lian** | **9.82%** |

Yin Lian (North China) also achieves the lowest return rate (9.82%), consistent with the high-margin, low-discount approach. The smaller regions (Northwest, Southwest) have higher return rates, possibly due to logistics challenges or customer satisfaction issues.

### 3.4 Year-over-Year Growth Consistency

| Region | Manager | 2016 YoY | 2017 YoY | 2018 YoY | Consistency |
|--------|---------|---------|---------|---------|------------|
| East China | Hong Guang | +32.23% | +31.62% | +17.41% | **Steady growth** |
| North China | Yin Lian | -26.26% | +46.27% | +45.32% | **Strong recovery after 2016 dip** |
| Central South | Fan Cai | +50.22% | -7.70% | +45.25% | **Volatile** |
| Northeast | Chu Jie | -4.82% | +58.58% | +26.02% | **Strong recovery** |
| Southwest | Bai Dewei | +41.23% | +20.04% | +2.01% | **Declining growth momentum** |
| Northwest | Yang Jian | -10.91% | +24.41% | +34.70% | **Accelerating** |

Hong Guang (East China) shows the most consistent year-over-year growth, with all three years positive and above 17%. Both Yin Lian (North China) and Chu Jie (Northeast) experienced negative growth in 2016 but staged strong recoveries. Bai Dewei's Southwest region shows a concerning deceleration from +41.23% to just +2.01%.

### 3.5 Statistical Assessment

A one-way ANOVA comparing average order sales across regions yielded **F(5, 4315) = 2.137, p = 0.058**, indicating that the observed differences in average order value across regions are **marginally non-significant at α = 0.05**. However, a non-parametric Kruskal-Wallis test (which is more robust to the skewed distribution of order values) shows **H = 13.53, p = 0.019**, suggesting that **statistically significant differences exist** across regions when accounting for the full distribution.

![Category by Region](work/category_by_region.png)

*Figure 4: Sales composition by category across regions, showing Technology's strong presence in Central South and Northeast.*

---

## 4. Integrated Findings

### Category Growth Conclusion
- **Furniture** was the fastest-growing category overall (CAGR 24.25%), leading in 2016 and 2018, driven by the 2018 surge (+40.71%).
- **Office Supplies** led in 2017 (+33.35%) with consistent volume growth.
- **Technology** lagged in 2018 growth, suggesting a maturing market.

### Manager Performance Summary

| Manager | Region | Sales Rank | Growth Rank | Margin Rank | Return Rate Rank | Overall Assessment |
|---------|--------|-----------|------------|------------|----------------|------------------|
| **Hong Guang** | East China | **1st** | **1st** | 3rd | 4th | **Top performer** — highest sales, best growth, moderate margin |
| **Fan Cai** | Central South | **2nd** | **2nd** | **2nd** | 5th | **Strong performer** — high volume, excellent margin, volatile growth |
| **Yin Lian** | North China | 4th | 4th | **1st** | **1st** | **Efficiency leader** — highest margin, lowest returns, solid growth |
| **Chu Jie** | Northeast | 3rd | 3rd | 5th | 3rd | **Solid growth, room for margin improvement** |
| **Yang Jian** | Northwest | 6th | 5th | 4th | 6th | **Small but improving** — accelerating growth, manageable scale |
| **Bai Dewei** | Southwest | 5th | 6th | 6th | 2nd | **Needs attention** — high discounting, low margin, growth deceleration |

### Key Insights

1. **Hong Guang (East China)** is the top overall performer, generating the highest total sales ($4.68M) and achieving the highest absolute growth (+$800K), while maintaining above-average profitability (12.96% margin).

2. **Yin Lian (North China)** is the efficiency champion — highest profit margin (17.61%), lowest discount rate (5.41%), and lowest return rate (9.82%). This suggests excellent pricing discipline and customer satisfaction.

3. **Bai Dewei (Southwest)** shows the weakest performance metrics: lowest profit margin (7.49%), highest discount rate (14.57%), and a concerning growth deceleration from +41.23% (2016) to just +2.01% (2018). This region may require strategic intervention.

4. **Manager vs. Region confound**: Since each manager oversees exactly one region, it is impossible to statistically separate the manager's individual contribution from inherent regional characteristics (market size, economic conditions, logistics infrastructure). The performance differences reflect the combined effect of manager skill and regional factors.

---

## 5. Limitations

- **Confounding of manager and region**: Each manager is assigned to only one region, so we cannot isolate manager-specific effects from regional market conditions.
- **No customer satisfaction data**: Return rates are used as a proxy, but direct satisfaction metrics are unavailable.
- **No cost data**: Profit is calculated as `Sales - Cost`, but the underlying cost structure is not available for deeper margin analysis.
- **Observational data**: Causal conclusions about what drove growth or margin differences cannot be drawn without experimental controls.
- **Small sample regions**: Northwest (233 orders) and Southwest (414 orders) have limited data, making their metrics less reliable.

---

## 6. Recommendations

1. **Investigate and replicate Yin Lian's (North China) pricing discipline** across other regions to improve overall profitability.
2. **Provide support to Bai Dewei (Southwest)** to address the high discount rates, low margins, and growth deceleration — possibly through training, pricing guidelines, or market analysis.
3. **Leverage Hong Guang's (East China)** growth strategies as a benchmark for other regions.
4. **Analyze Furniture's rapid growth** to understand whether it represents sustainable demand or unsustainable discounting that may compress future margins.
5. **Monitor Technology's deceleration in 2018** — the category may need renewed marketing or product strategy to maintain growth momentum.