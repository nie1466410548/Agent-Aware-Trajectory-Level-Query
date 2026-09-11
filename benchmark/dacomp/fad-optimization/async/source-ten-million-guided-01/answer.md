# South China Monthly Profit Instability Analysis

## 1. Scope and Data Overview

**Data coverage**: Full year 2023 (1 Jan – 31 Dec), 10M rows across 277 destinations, 8 products, 12 months.

**Region definition**: The `Destination` column is formatted as `"Region-Province-City"`. Filtering with `Destination LIKE 'South China%'` yields **3,717,808 orders** (37.2% of total) with **4.84B total profit** — the largest region by volume.

**Region composition (73 destinations)**:
| Province | Profit Share | CV of Monthly Profit | Notes |
|---|---|---|---|
| Guangdong | 42.7% | 8.9% | Core South China |
| Guangxi | 25.8% | 9.7% | Core South China |
| Hainan | 7.8% | 20.0% | Core South China |
| **Henan** | **11.7%** | **16.8%** | **Not South China (Central/North)** |
| **Hubei** | **6.5%** | **22.9%** | **Not South China (Central)** |
| **Hunan** | **5.5%** | **20.1%** | **Debatable (South Central)** |

**Data quality concern**: Henan Province (11.7% of profit) is labeled "South China-Henan Province-*" despite being geographically North/Central China. Hubei (6.5%) is also mislabeled. Together these three provinces contribute **23.7%** of South China's total profit but have substantially higher volatility (CV 17–23%) than Guangdong/Guangxi (CV 9–10%). They appear under **no other region label** — this is a consistent labeling error.

---

## 2. Quantified Monthly Instability

### Summary Statistics (12 monthly observations, population convention)

| Metric | Value |
|---|---|
| Mean monthly profit | 403.4M |
| Std Dev (population, n=12) | 25.02M |
| **Coefficient of Variation** | **6.20%** |
| Range (max–min) | 83.3M (20.6% of mean) |
| Minimum | 349.4M (Feb) |
| Maximum | 432.7M (Dec) |

### Month-to-Month Changes

| Period | Δ Profit | Δ% | Direction |
|---|---|---|---|
| **Jan→Feb** | **−63.1M** | **−15.3%** | Largest drop |
| Feb→Mar | +64.9M | +18.6% | Largest rise |
| Mar→Apr | −39.4M | −9.5% | Second drop |
| Jun→Jul | +53.9M | +14.6% | Second rise |

February is the anomaly month — over 63M below January. The pattern (Jan high → Feb low → Mar recovery → Apr drop) suggests a **seasonal/calendar effect** (Chinese New Year 2023 fell on 22 Jan, disrupting February business activity).

---

## 3. Revenue, Cost, and Volume Explanations

### Profit Structure (Monthly Averages)
- **Revenue**: ~423M/month
- **Cost**: ~28.9M/month (6.8% of revenue)
- **Profit = Revenue − Cost** with cost fraction stable (6.5–7.1%)
- **Margin (Profit/Revenue)**: 93.0–93.8% — extremely stable
- **Discounts**: Only 0.68–0.76% of List Price Revenue — negligible and stable
- **Value-Added Services**: 1.64–1.98% of Revenue — minor and stable

**Conclusion**: Cost-side factors do NOT drive instability. All variation comes from the **revenue side**, which itself is **volume-driven**.

### Volume vs. Per-Order Decomposition

Comparing CVs across the 12 months:

| Measure | CV (Population) |
|---|---|
| Monthly Profit | 6.20% |
| **Order Count** | **5.23%** |
| **Sales Quantity** | **5.53%** |
| Profit per Order | 3.78% |
| Profit per Unit | 2.97% |
| Revenue per Order | 3.50% |

Order count and quantity have **1.4–1.9× the CV of per-order metrics**, establishing volume as the primary source.

### Decomposition of Major Swings (ΔProfit = Volume Effect + Per-Order Effect)

| Swing | Total Δ | **Volume Effect** | Per-Order Effect | Orders Δ% |
|---|---|---|---|---|
| Jan→Feb | −63.1M | **−43.9M (70%)** | −19.1M (30%) | −10.7% |
| Feb→Mar | +64.9M | **+66.9M (103%)** | −2.0M (−3%) | +19.1% |
| Mar→Apr | −39.4M | **−38.0M (96%)** | −1.4M (4%) | −9.2% |
| Jun→Jul | +53.9M | **+34.4M (64%)** | +19.5M (36%) | +9.3% |

**Volume accounts for 64–103% of every major swing.** Per-order profit changes are secondary, contributing materially only in Jan→Feb (−30%) and Jun→Jul (+36%).

---

## 4. Product Composition

### Product Overview (South China, full year)

| Product | Profit Share | CV (Monthly) | Key Role |
|---|---|---|---|
| Bedding set | 19.3% | 9.4% | Largest share, moderate stability |
| Bathroom supplies | 14.9% | 13.8% | Volatile |
| Auto parts | 14.6% | 11.5% | Volatile |
| Home decor items | 13.3% | 12.3% | Moderate volatility |
| **Kitchen Appliances** | **12.6%** | **20.5%** | **Most volatile major product** |
| Bedroom Furniture | 11.9% | 15.4% | High volatility |
| Computer hardware | 11.6% | 14.9% | High volatility |
| Office furniture | 1.8% | 40.9% | Small share, highest CV |

### Product Contribution to Major Monthly Swings

| Product | Jan→Feb | Feb→Mar | Mar→Apr | Jun→Jul |
|---|---|---|---|---|
| **Kitchen Appliances** | **−36.5M (58%)** | +22.5M (35%) | **−20.5M (52%)** | +13.6M (25%) |
| Auto parts | −10.2M (16%) | +17.3M (27%) | −17.4M (44%) | +11.9M (22%) |
| Bedroom Furniture | −7.5M (12%) | +8.6M (13%) | +8.5M | +6.0M (11%) |
| Home decor items | −17.0M (27%) | +2.2M (3%) | +8.2M | +5.5M (10%) |
| Bathroom supplies | +1.2M | +12.8M (20%) | **−21.2M (54%)** | +0.1M |
| Computer hardware | +3.0M | +3.6M (6%) | +11.2M | **+15.0M (28%)** |

**Kitchen Appliances is the single largest contributor to instability**: it accounts for 58% of the Jan→Feb drop, 52% of Mar→Apr drop, and has the highest covariance with total monthly profit variance despite only 12.6% profit share. Its volatility is driven by **volume swings**: Kitchen Appliances quantity dropped from 2.43M units in Jan to 1.39M in Feb (−43%), with per-unit revenue also declining 14%.

Auto parts and Bathroom supplies are the second-tier contributors, each amplifying the Mar→Apr and other swings.

---

## 5. Geography

### Province-Level Volatility

| Province | Profit Share | Monthly CV | Jan→Feb Contribution | Feb→Mar Contribution |
|---|---|---|---|---|
| Guangdong | 42.7% | 8.9% | −10.9M (17%) | −8.9M |
| Guangxi | 25.8% | 9.7% | −19.3M (31%) | +28.4M (44%) |
| **Henan** (mislabeled) | **11.7%** | **16.8%** | **−22.2M (35%)** | +22.0M (34%) |
| Hainan | 7.8% | 20.0% | −9.6M (15%) | +20.5M (32%) |
| Hubei (mislabeled) | 6.5% | 22.9% | −1.0M (2%) | +3.8M (6%) |
| Hunan (debated) | 5.5% | 20.1% | −0.1M | −0.9M |

### Key Geographic Findings

**1. Henan Province (mislabeled) is the #1 geographic contributor to instability.** Despite having only 11.7% of total profit, Henan contributed **−22.2M (35%)** of the Jan→Feb drop — more than any other province. Its 16.8% CV is ~2× that of Guangdong/Guangxi. This is amplified by Kitchen Appliances: Henan's Kitchen Appliances profit collapsed from 17.3M (Jan) to 4.1M (Feb), a −76% decline, vs Guangdong's −29%.

**2. Guangxi is the second-largest geographic contributor.** Its Jan→Feb contribution (−19.3M, 31%) is concentrated in Beihai (CV 20.8%, the largest city by volume in SC). Beihai alone dropped −10.5M in Feb.

**3. Hainan shows high city-level volatility.** Haikou (CV 18.7%) dropped −5.3M in Jan→Feb and Sanya (CV 30.5%) dropped −4.2M, then both recovered strongly in Feb→Mar (+11.8M and +8.6M respectively).

**4. The mislabeling of Henan/Hubei inflates measured South China volatility.** If these provinces were excluded, the aggregate CV of remaining true South China (Guangdong, Guangxi, Hainan = 76.3% of current total) would drop from 6.20% to approximately 5.0-5.5% (estimate based on lower CVs of these provinces).

**City-level detail (top contributors to Jan→Feb drop):**
| City | Contribution | CV |
|---|---|---|
| Anyang (Henan, mislabeled) | −10.9M (17% of total drop) | 37.5% |
| Beihai (Guangxi) | −10.5M (17%) | 20.8% |
| Chaozhou (Guangdong) | −5.5M (9%) | High |
| Haikou (Hainan) | −5.3M (8%) | 18.7% |
| Foshan (Guangdong) | −4.5M (7%) | 38.3% |

---

## 6. Anomaly Verification

**Negative-profit orders**: 128,763 rows (3.46% of SC orders) have negative profit. However:
- Monthly total negative profit is only **−0.4M to −0.6M** (< 0.2% of monthly profit)
- Evenly distributed across months and cities
- **Immaterial to total profit changes** — does not affect any conclusion

**Extreme values**: No rows with Sales Quantity > 1000 or Revenue > 100K at the individual order level. The "Profit Margin" column (range −65.8% to +255.3%) appears to be a per-order calculation that differs from aggregate ratio, but this does not affect the aggregate-level analysis.

---

## 7. Synthesis and Ranked Explanations

### Ranked Drivers of Monthly Profit Instability

| Rank | Factor | Evidence | Quantitative Support |
|---|---|---|---|
| **1** | **Volume (order count) fluctuations** | Volume effect accounts for 64–103% of every major monthly swing. CV(orders)=5.23% vs CV(profit/order)=3.78% | Query 31: Decomposition table; Query 24: CV comparison |
| **2** | **Kitchen Appliances product swings** | Highest covariance with total variance (182.5T); contributes 58% of Jan→Feb drop and 52% of Mar→Apr drop; own CV=20.5% | Query 11: Product contribution to swings; Query 30: Covariance decomposition; Query 21: KA monthly |
| **3** | **Henan Province mislabeling amplifies volatility** | 11.7% of profit but 35% of Jan→Feb drop; CV=16.8% vs 8.9% for Guangdong; Kitchen Appliances in Henan dropped 76% in Feb | Query 15: Province contributions; Query 32: KA by province Feb drop |
| **4** | **Guangxi (esp. Beihai) swings** | 25.8% of profit; CV=9.7%; contributed −19.3M (31%) of Jan→Feb drop and +28.4M (44%) of Feb→Mar rise | Query 15: Province MoM changes; Query 14: City-level MoM changes |
| **5** | **Auto parts and Bathroom supplies secondary volatility** | CV 11.5% and 13.8%; each contributed −10M to −21M in several swing months | Query 11: Product contributions; Query 19: Monthly detail |
| **6** | **Hainan seasonal swings** | CV 20.0%; contributed −9.6M Jan→Feb, +20.5M Feb→Mar; 75% of profit concentrated in Haikou+Sanya | Query 15: Hainan province; Query 12: City CVs |

### Resolving Competing Explanations

- **Volume vs. pricing**: Volume is 2–3× more important (CV 5.2% vs 3.0–3.8%). Per-order effects contributed meaningfully only in Jan→Feb (−30%) and Jun→Jul (+36%).
- **Product vs. geography**: These interact strongly. The Kitchen Appliances volatility is concentrated in Henan (36% of KA Feb drop) and Guangxi (27%), not spread evenly. The product and geographic factors are **complementary**, not competing.
- **Macro pattern**: Jan high → Feb low → Mar recovery → Apr dip is consistent across multiple products and provinces, suggesting a **February holiday effect** (Chinese New Year 2023: 22 Jan) causing reduced business activity in February. However, association alone does not establish this as a causal explanation.

### Limitations

- Analysis performed through SQL queries only; no Python, external calculations, or statistical tests were used. All statistics (mean, SD, CV, covariance) were computed via SQLite expressions.
- The read_result tool returned limited text previews; all numerical evidence is from directly queried aggregate results.
- Causal interpretations (e.g., holiday effect) remain associations; the data cannot distinguish correlation from causation without additional domain information.