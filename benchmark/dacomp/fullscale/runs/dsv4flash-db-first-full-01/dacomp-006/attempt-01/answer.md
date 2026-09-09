# Root Causes of Monthly Profit Instability in South China (2023)

## Executive Summary

The monthly total profit in South China ranged from **637.7k to 789.7k** (mean: 736.1k), with a coefficient of variation (CV) of **6.5%** and month-over-month swings as large as **±15–19%**. The instability is driven primarily by **revenue volatility** (profit correlates with revenue at r=0.999), which in turn is driven by **sales quantity fluctuations** (r=0.88) across specific product categories and provinces. The following sections identify the key contributing aspects.

---

## 1. Product-Level Drivers

Products vary dramatically in their monthly profit volatility and contribution to total variance:

| Product Category | Monthly Profit CV | Share of Total Variance | Annual Profit Share |
|---|---|---|---|
| Kitchen Appliances | **21.4%** | **26.7%** | 12.6% |
| Auto parts | 12.0% | **18.7%** | 14.6% |
| Bedroom Furniture | 16.1% | **16.8%** | 11.9% |
| Bathroom supplies | 14.4% | 12.8% | 14.9% |
| Bedding set | 9.8% | 11.2% | 19.3% |
| Home decor items | 12.8% | 8.0% | 13.3% |
| Computer hardware | 15.6% | 4.6% | 11.6% |
| Office furniture | 40.9% | 1.3% | 1.8% |

**Kitchen Appliances** is the single largest contributor: despite comprising only 12.6% of annual profit, it drives **26.7% of monthly profit variance**. Its monthly profit range spans 60.7k–127.4k (CV 21.4%). The February 2023 drop (the largest single-month swing) was driven disproportionately by Kitchen Appliances, which fell **66.7k** (from 127.4k to 60.7k) – a 52% decline in profit from this category alone.

![Product variance share](sc_variance_share_bar.png)

**Figure 1: Variance share by product category (left) and province (right).**

---

## 2. Province-Level Drivers

The "South China" region in this dataset spans six provinces. Their contributions to instability differ markedly:

| Province | Monthly Profit CV | Share of Total Variance | Annual Profit Share |
|---|---|---|---|
| **Guangdong** | 8.9% | **33.6%** | 42.7% |
| **Guangxi** | 9.8% | **29.3%** | 25.8% |
| Hainan | 20.9% | 13.8% | 7.8% |
| Hubei | 23.9% | 13.7% | 6.5% |
| Henan | 17.4% | 12.9% | 11.7% |
| Hunan | 20.1% | –3.2% (negative) | 5.5% |

Guangdong and Guangxi, the two largest provinces (68.5% of total profit), contribute **62.9% of the total variance** due to their large absolute size. The smaller provinces (Hainan, Hubei, Henan) are individually more volatile (CV 17–24%) and collectively contribute another 40.4% of variance. Hunan's profit has a negative covariance with the total, meaning it acts as a partial hedge.

![Province contributions](sc_province_change_contrib.png)

**Figure 2: Province contribution to month-over-month profit changes.**

---

## 3. Customer Segment Drivers

**Gender:**
- **Male customers** contribute **67.8%** of monthly profit variance despite only 47% of annual profit. Their monthly profit CV is 11.1% vs. 6.6% for females.
- Female customers are more stable in both absolute and relative terms.

**Age Range:**
- **50–59** age group contributes **37.3%** of total variance (CV 13.6%).
- **30–39** contributes **25.0%** (CV 12.2%).
- **40–49** contributes **23.2%** (CV 9.3%).
- **60–69** has the highest CV (22.9%) but contributes negligibly (–0.7% share) due to small size.

The older age groups (50–59) and male customers exhibit the most erratic month-to-month purchasing behavior, amplifying the overall profit instability.

![Age and gender variance](sc_age_gender_variance.png)

**Figure 3: Variance share by age range and customer gender.**

---

## 4. Revenue vs. Cost Decomposition

Profit = Total Logistics Revenue – Total Logistics Cost. The data show:

| Metric | CV | Correlation with Profit |
|---|---|---|
| Total Logistics Revenue | 6.4% | **0.999** |
| Total Logistics Cost | 6.3% | 0.750 |
| Sales Quantity | 5.8% | **0.876** |
| Order Count | 5.5% | 0.802 |
| Avg Profit Margin | 16.5% | 0.163 |
| Avg Unit Price | 2.2% | 0.495 |

**Key insight:** Profit instability is essentially **revenue instability** (r=0.999). Costs are small (~7% of revenue) and do not materially offset the swings. Revenue components are stable: discounts are a constant 0.7% of list price, and VAS revenue is a steady 1.7–1.9%.

![Revenue and cost components](sc_revenue_cost_components.png)

**Figure 4: Monthly revenue and cost components.**

---

## 5. Volume vs. Per-Order Profit Decomposition

The month-over-month swings are predominantly **volume-driven**:

| Transition | Total Change | Volume Effect | Per-Order Profit Effect |
|---|---|---|---|
| Jan→Feb (drop) | –115k | **–80k (70%)** | –35k (30%) |
| Feb→Mar (recovery) | +118k | **+122k (103%)** | –4k (–3%) |
| Mar→Apr (drop) | –72k | **–69k (96%)** | –3k (4%) |
| Jun→Jul (recovery) | +98k | **+63k (64%)** | +36k (36%) |

The February drop: 512 orders vs. 573 in January (–11% fewer orders). The per-order profit also declined from 1,314 to 1,246 (–5.2%). Combined, the volume decline accounts for 70% of the total profit drop.

---

## 6. The February 2023 Drop: A Case Study

The largest single-month swing (–115k, –15.3%) was driven by:

| Product | Jan Profit | Feb Profit | Change | Contribution |
|---|---|---|---|---|
| Kitchen Appliances | 127.4k | 60.7k | **–66.7k** | **58%** of drop |
| Home decor items | 120.9k | 89.9k | –31.0k | 27% |
| Auto parts | 113.4k | 94.8k | –18.7k | 16% |
| Bedroom Furniture | 74.6k | 61.0k | –13.7k | 12% |
| *(Offset by)* Bedding set | 137.3k | 141.6k | +4.3k | –4% |

For Kitchen Appliances specifically: orders dropped from 87 to 57 (–34%), quantity from 4,438 to 2,537 (–43%), and unit price from 30.34 to 24.51 (–19%) – a triple hit to volume, size, and pricing.

---

## Conclusions

The monthly profit instability in South China is caused by **five interacting aspects**:

1. **Product mix concentration in volatile categories** – Kitchen Appliances (26.7% variance share, CV 21.4%) is the dominant destabilizer, followed by Auto parts (18.7%) and Bedroom Furniture (16.8%).

2. **Provincial disparities** – Guangdong and Guangxi contribute the most absolute variance, while Hainan, Hubei, and Henan are individually more volatile (CV 17–24%).

3. **Customer segment heterogeneity** – Male customers (67.8% variance share, CV 11.1%) and the 50–59 age group (37.3% share) exhibit the most erratic purchasing patterns.

4. **Volume-driven demand fluctuations** – 64–103% of month-over-month profit changes are attributable to order count changes rather than price or margin adjustments. Revenue (r=0.999) drives profit directly.

5. **Concentrated one-month shocks** – The Feb 2023 drop (–115k) was 58% attributable to a single product category (Kitchen Appliances), which simultaneously experienced lower order volume, smaller order sizes, and lower unit prices.

### Limitations

- The data covers only one year (2023), limiting the ability to distinguish seasonal patterns from idiosyncratic shocks.
- "South China" in this dataset includes Henan, Hubei, and Hunan provinces, which are geographically Central China – the regional classification may not match common geographical definitions.
- Two anomalous rows (negative revenue) slightly distort the October average profit margin.
- The analysis is correlational; causal factors (e.g., marketing campaigns, competitive activity, supply chain disruptions) are not available in the data.