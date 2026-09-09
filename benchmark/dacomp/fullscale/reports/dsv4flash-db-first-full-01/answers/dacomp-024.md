<!-- Reading copy: local artifact links normalized. Original answer is preserved at ../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/answer.md -->

# Business Performance Comparison: Four Regions × Three Segments (2015–2017)

## 1. Data & Method
- **Source:** Two tables joined on `Order ID` (`sheet1` = orders/customers/region; `sheet2` = line items with Sales & Profit per Unit). All metrics are computed over line-item revenue (`Quantity × Sales per Unit`) and profit (`Quantity × Profit per Unit`).
- **Scope:** Years 2015, 2016, 2017 (4 regions × 3 segments = 12 region–segment cells × 3 years = 36 cells).
- **Metrics:** Sales, Profit, Profit Margin, Customer/Order counts, YoY growth, customer penetration share (share of all customers), profit per customer, and category-level profitability.
- **Key figures:** All charts are generated in `/work`.

## 2. Overall Region Performance (2015–2017)

| Region | Sales ($M) | Profit ($M) | Margin % | Orders | Customers |
|---|---|---|---|---|---|
| East | 9.06 | 1.09 | 12.0% | 1,140 | 613 |
| West | 8.53 | **1.21** | **14.2%** | 1,298 | **632** |
| Central | 5.47 | 0.69 | 12.6% | 945 | 555 |
| South | 4.41 | 0.55 | 12.6% | 657 | 443 |

- **East** is the sales leader ($9.06M) but only third in margin (12.0%).
- **West** is the profit leader ($1.21M) and has the **highest margin (14.2%)** plus the largest, fastest-growing customer base.
- **Central** and **South** trail in absolute size; South is the smallest and least penetrated (17% customer share in 2017 vs. West's 31%).

![Sales by region](<../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/work/fig1_sales_by_region.png>)
![Margin by region](<../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/work/fig2_margin_by_region.png>)

## 3. Segment Performance (2015–2017)

| Segment | Sales ($M) | Margin % | Customers |
|---|---|---|---|
| Consumer | 14.23 | 12.0% | 408 |
| Corporate | 8.28 | **14.6%** | 234 |
| Home Office | 4.95 | 12.7% | 148 |

Consumer is the largest segment; **Corporate is the most profitable** by margin (14.6%). Consumer grew fastest in absolute profit.

## 4. Region × Segment × Year Analysis (Penetration & Profitability)

### 4.1 Customer penetration (share of customers)
| Region | 2015 | 2016 | 2017 | Trend |
|---|---|---|---|---|
| West | 31.4% | 30.5% | 30.6% | Largest base; absolute customers grew 276→397 |
| East | 28.0% | 28.1% | 27.3% | Stable ~28% |
| Central | 22.9% | 24.2% | **25.0%** | Gaining share (201→325) |
| South | 17.7% | 17.2% | 17.2% | **Under-penetrated; stagnant** |

![Customer penetration](<../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/work/fig6_customer_penetration.png>)

### 4.2 Best-performing region–segment combinations

**By total profit (2015–2017):**
1. **West–Consumer:** $718K profit, 17.0% margin, $4.23M sales — best overall
2. **East–Consumer:** $524K profit, 10.5% margin, $4.99M sales (largest revenue cell)
3. **Central–Corporate:** $410K profit, **20.2% margin** (highest margin combo)
4. **West–Corporate:** $382K profit, 14.8% margin
5. **South–Consumer:** $339K profit, 13.7% margin
6. **East–Home Office:** $313K profit, 18.1% margin

**By 2017 profit margin:**
- **West–Consumer 19.3%**, **West–Corporate 17.6%**, **Central–Home Office 16.8%**, **East–Home Office 15.5%**, East–Consumer 14.2%
- **Worst:** **South–Home Office −8.5% (−$26K loss)**, Central–Consumer 1.0%

![Total profit by region and segment](<../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/work/fig5_total_profit_region_segment.png>)
![Margin heatmap](<../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/work/fig8_margin_heatmap.png>)
![2017 sales by region-segment](<../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/work/fig3_sales_region_segment_2017.png>)
![2017 margin by region-segment](<../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/work/fig4_margin_region_segment_2017.png>)

### 4.3 YoY growth (2015→2017), sales / profit
| Region–Segment | Sales Δ | Profit Δ | Comment |
|---|---|---|---|
| West–Corporate | +159% | **+165%** | Strongest sustained momentum |
| West–Home Office | +199% | +34% | Scaling revenue fast |
| West–Consumer | +50% | **+128%** | Profitable growth engine |
| East–Home Office | +114% | **+135%** | Best East grower |
| South–Corporate | +117% | +127% | South's bright spot |
| East–Consumer | +3% | +84% | Margin recovery |
| Central–Consumer | +1% | **−64%** | Margin collapse (2.9%→1.0%) |
| South–Consumer | +17% | −57% | 2017 margin fell to 6.2% |
| South–Home Office | +437% | **−352%** | Turned into a loss in 2017 |

![Sales growth by region](<../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/work/fig7_sales_growth_region.png>)

### 4.4 Profit per customer (2017) — value quality
Leaders: **West–Corporate $1,861**, **East–Home Office $1,840**, **West–Consumer $1,758**, **East–Consumer $1,445**. Laggards: **Central–Consumer $44**, **South–Home Office −$650**. Central Consumer serves many customers (13.3% of all 2017 customers) at near-zero profit — high volume, no value.

## 5. Category Drivers (for expansion recommendations)

![Category profit by region](<../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/work/fig9_category_profit_region.png>)

- **Technology** is the profit engine in **Central** (27.1% margin, $506K) and **South** (20.6% margin) — powers Central–Corporate and South profitability.
- **Office Supplies** is highly profitable in **West** (25.7%, $709K) and **East** (20.2%) — key to West's success.
- **Furniture** is thin-margin everywhere (0.6–2.9%) and **Appliances lose money in Central (−1.9%)**.

## 6. Conclusions & Expansion Recommendations

**Best-performing combinations:** *West–Consumer* (highest total profit + high margin + strong growth), *Central–Corporate* (highest margin 20%+), *East–Home Office* (fast growing, high margin), *West–Corporate* (best momentum), *South–Consumer* (surprisingly profitable given small base).

**Recommendations:**
1. **Double down on West.** West–Consumer and West–Corporate are the top profit and growth engines (margins 17–19% with profit growth >128%). Expand Office Supplies and Technology offerings here.
2. **Scale South selectively.** South is the least penetrated market (17% share, smallest base). South–Corporate grew +127% profit and South–Consumer still delivers a 13.7% margin — target acquisition here. But **fix South–Home Office** (2017 loss of −$26K) via discount/pricing review before investing further.
3. **Fix, don't grow, Central–Consumer.** It holds a large customer base (13.3% share in 2017) but only a 1.0% margin — likely excessive discounts. Re-price before scaling. Meanwhile, **protect Central–Corporate**, the highest-margin combination (20.2%), and avoid Appliances (negative margin).
4. **Maintain East.** East is the revenue leader and its Home Office segment (+135% profit) and Consumer segment (+84% profit) are recovering well; keep investing but watch the lower 12% margin vs. West.
5. **Product portfolio:** Prioritize Technology and Office Supplies (margins 20–27%) across regions; de-emphasize Furniture (thin margins); fix Central Appliances or exit.

## 7. Limitations
- **No market-potential data** (state/city population or firm counts) exists in the database, so "penetration" is measured as *share of the served customer base* and order/sales share, not penetration of an external addressable market.
- Results are transaction-level aggregates; per-customer counts treat repeat buyers as one customer per year, so penetration reflects unique customers reached per year.
- 2016–2017 volatility in Central–Corporate and South–Home Office suggests some metrics may be sensitive to a few large orders or seasonal effects; deeper order-level analysis would be needed to confirm causality.
