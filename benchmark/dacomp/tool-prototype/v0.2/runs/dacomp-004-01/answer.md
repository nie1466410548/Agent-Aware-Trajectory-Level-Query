# Monthly Top Products Analysis

## 1. Overview
The dataset spans **4 months** (January–April 2015) with **42,816 transactions**, **6,142 distinct products**, and **2,612 customers**.

## 2. Top Product by Sales Amount per Month

| Month | Product Code | Product Description | Sales Amount |
|-------|-------------|-------------------|:------------:|
| 2015-01 | DW-1001040125 | **Pork bones** (meat & poultry, fresh food, sold loose by kg) | **$2,836.46** |
| 2015-02 | DW-2316020016 | **Domestic cigarettes (out-of-province)** (alcoholic drinks, 20 sticks/bag) | **$5,600.00** |
| 2015-03 | DW-1203130446 | **Other fruits** (fruits & vegetables, fresh food, sold loose by kg) | **$4,893.62** |
| 2015-04 | DW-1518040045 | **Tetra Pak brick acidified milk drink** (daily-delivered chilled, 205ml, box) | **$1,400.30** |

### Competition Runners-Up

| Month | Rank | Product | Sales |
|:-----:|:----:|---------|:-----:|
| Jan | 2 | DW-1203090210 (Other vegetables) | $1,966.86 |
| Jan | 3 | DW-1521010005 (Unknown) | $1,813.06 |
| Feb | 2 | DW-2311010018 (Cigarettes) | $5,340.00 |
| Feb | 3 | DW-2311010015 (Cigarettes) | $3,540.00 |
| Mar | 2 | DW-1521010005 (Unknown) | $1,558.49 |
| Mar | 3 | DW-1001040125 (Pork bones) | $1,220.88 |
| Apr | 2 | DW-1203070022 (Other vegetables) | $1,241.44 |
| Apr | 3 | DW-1203130449 (Other fruits) | $1,232.69 |

*Note: All top products were sold at "Full price" (no promotional discount).*

## 3. Cross-Month Performance of the Top Products

### DW-1001040125 (Pork bones) — Consistent Performer
| Month | Sales | Rank | Orders | Customers |
|:-----:|:-----:|:----:|:------:|:---------:|
| Jan | $2,836.46 | **#1** | 48 | 45 |
| Feb | $711.01 | #24 | 15 | 15 |
| Mar | $1,220.88 | **#3** | 26 | 24 |
| Apr | $1,180.53 | **#4** | 30 | 28 |
| **Total** | **$5,948.88** | | **119** | **104** |

This product was the **only one to rank in the top 5 in three different months** (Jan #1, Mar #3, Apr #4), demonstrating consistent strong demand.

### DW-1203130446 (Other fruits) — Seasonal Peak
| Month | Sales | Rank | Orders | Customers |
|:-----:|:-----:|:----:|:------:|:---------:|
| Jan | $797.79 | #14 | 41 | 28 |
| Feb | $1,095.26 | #12 | 55 | 47 |
| Mar | **$4,893.62** | **#1** | 222 | 161 |
| Apr | $598.16 | #17 | 26 | 24 |
| **Total** | **$7,384.83** | | **344** | **227** |

This product had the **highest total sales across all four products** ($7,384.83) and the **largest customer base** (227 customers). Its explosive March performance (222 orders, 161 customers) drove it to the top.

### DW-2316020016 (Cigarettes) — One-Time Bulk Purchase
| Month | Sales | Rank | Orders | Customers |
|:-----:|:-----:|:----:|:------:|:---------:|
| Feb | **$5,600.00** | **#1** | 2 | 2 |
| **Total** | **$5,600.00** | | **2** | **2** |

This is an **outlier**: only 2 orders from 2 customers, each averaging $2,800. It appears in only one month, suggesting a large wholesale/bulk transaction rather than regular retail demand.

### DW-1518040045 (Acidified milk drink) — Single-Month Appearance
| Month | Sales | Rank | Orders | Customers |
|:-----:|:-----:|:----:|:------:|:---------:|
| Apr | **$1,400.30** | **#1** | 36 | 34 |
| **Total** | **$1,400.30** | | **36** | **34** |

This product appeared **only in April** yet still claimed the top spot. It had a moderate but sufficient customer base of 34.

## 4. Repurchase Rate vs. Sales Amount Analysis

### Definition
**Repurchase rate** = (Customers who bought the product **≥2 times**) / (Total customers who bought the product). This measures customer loyalty at the product level.

### Top Products' Repurchase Metrics

| Product | Total Sales | Customers | Repurchasers | Repurchase Rate | Multi-Month Buyers |
|---------|:-----------:|:---------:|:------------:|:---------------:|:------------------:|
| DW-1203130446 (Other fruits) | **$7,384.83** | 227 | 60 | **26.43%** | 28 (12.33%) |
| DW-1001040125 (Pork bones) | $5,948.88 | 104 | 14 | **13.46%** | 8 (7.69%) |
| DW-2316020016 (Cigarettes) | $5,600.00 | 2 | 0 | **0.00%** | 0 (0.00%) |
| DW-1518040045 (Milk drink) | $1,400.30 | 34 | 2 | **5.88%** | 0 (0.00%) |

**Key observations:**
- **DW-1203130446** (Other fruits) has the **highest repurchase rate (26.43%)** and the **highest total sales ($7,384.83)** — a loyal customer base buying frequently.
- **DW-1001040125** (Pork bones) has a moderate repurchase rate (13.46%) with consistent monthly demand.
- **DW-2316020016** (Cigarettes) has 0% repurchase rate — both customers were one-time buyers, and the product only appeared in one month.
- **DW-1518040045** (Milk drink) has a low repurchase rate (5.88%) and zero cross-month buyers, suggesting it was a new/seasonal product.

### Broader Correlation Analysis (All 6,142 Products)

Products were grouped into sales amount buckets to examine the relationship at scale:

| Sales Bucket | Products | Avg Repurchase Rate | Avg Sales | Avg Customers |
|:------------:|:--------:|:-------------------:|:---------:|:-------------:|
| < $100 | 5,337 | **3.76%** | $26.08 | 3.0 |
| $100–$500 | 666 | **9.52%** | $196.20 | 16.4 |
| $500–$1,000 | 80 | **12.09%** | $682.67 | 61.4 |
| $1,000–$2,000 | 35 | **12.57%** | $1,405.22 | 72.7 |
| $2,000–$5,000 | 19 | **12.55%** | $2,834.93 | 75.7 |
| **≥ $5,000** | **5** | **15.20%** | **$5,971.68** | **151.6** |

**Pearson correlation coefficient (r)**: **0.098** — a very weak positive correlation.

**Interpretation:**
- There is a **slight upward trend**: products with higher total sales tend to have modestly higher repurchase rates on average.
- The **correlation is very weak** (r ≈ 0.1), meaning sales amount alone is a poor predictor of repurchase rate.
- The **lowest bucket** (<$100) has a notably lower repurchase rate (3.76%), likely because these are niche products with few customers (avg 3.0), making repurchase statistically unlikely.
- Beyond the $500 threshold, the average repurchase rate stabilizes around 12–13%, suggesting a **diminishing marginal effect** of sales volume on customer loyalty.
- The **top bucket** (≥$5,000, only 5 products) shows the highest average repurchase rate (15.20%), but the small sample size limits statistical significance.

## 5. Summary

1. **Monthly top products** vary across categories: fresh food (pork, fruits), cigarettes, and dairy each dominated different months.
2. **DW-1001040125 (pork bones)** was the most consistent top performer, ranking in the top 5 across three months.
3. **DW-1203130446 (other fruits)** had the highest total sales and highest repurchase rate, suggesting a loyal customer base for fresh fruit purchases.
4. The **relationship between repurchase rate and Sales Amount** is **positive but weak** (r = 0.098). Higher-selling products tend to have slightly higher repurchase rates, but the effect is small and many exceptions exist (e.g., high-volume bulk purchases with zero repurchase).

### Limitations
- No Python/figure generation available; all analysis is SQL-based.
- The 4-month window limits detection of long-term repurchase patterns.
- "Customer ID" values appear sequential, which may affect repurchase rate accuracy if they are not true customer identifiers.
- The broad repurchase rate analysis (all 6,142 products) is dominated by the 5,337 products with <$100 sales, which may skew the overall correlation.