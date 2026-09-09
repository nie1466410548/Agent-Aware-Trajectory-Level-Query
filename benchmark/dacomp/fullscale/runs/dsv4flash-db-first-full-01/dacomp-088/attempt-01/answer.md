# Regional Market Performance Analysis — Investment Efficiency Report

## Executive Summary

This report analyzes market performance across all 50 U.S. states using Salesforce opportunity, account, and sales performance data combined with state economic indicators. A composite **Investment Efficiency Score** was constructed from six core metrics, a Competition Intensity Assessment Model, and an Investment Return Prediction Algorithm. The analysis ranks all states and provides a 3-year regional expansion priority recommendation.

**Key Findings:**
- **Oregon** ranks #1 with an Investment Efficiency Score of **68.72**, driven by high average customer revenue ($15.5M) and strong investment return potential.
- **New York (#3, 60.76)** and **California (#4, 59.01)** dominate large-market efficiency.
- **Colorado (#5, 56.81)** and **Washington (#8, 54.09)** show strong balanced performance.
- States with zero current customer footprint (Alaska, Nebraska, Vermont, North Dakota) rank lowest, representing greenfield expansion opportunities.

---

## 1. Core Metrics per State

### 1.1 Customer Acquisition Cost (CAC) per State

**Definition:** CAC = (Total number of sales representatives in the state × $150,000) / Number of new customers in the state

- Sales representatives per state: Count of distinct owner_ids operating in each billing state.
- New customers: Number of distinct accounts with won "New Business" opportunity type per billing state.

**Top States by CAC Efficiency (lowest CAC):**

| State | New Customers | Reps | CAC |
|-------|:------------:|:----:|:---:|
| New Hampshire | 5 | 13 | $390,000 |
| South Dakota | 3 | 9 | $450,000 |
| West Virginia | 3 | 9 | $450,000 |
| Minnesota | 13 | 42 | $484,615 |
| New York | 53 | 192 | $543,396 |

**Highest CAC states:** West Virginia ($1,350,000), Maine ($1,350,000), North Carolina ($1,216,667), Tennessee ($1,200,000), Hawaii ($1,200,000)

### 1.2 Average Customer Value per State

Mean and median of `annual_revenue` for Customer-type accounts per billing state:

| State | Mean Revenue | Median Revenue |
|-------|:-----------:|:--------------:|
| Alabama | $29,827,833 | $6,287,266 |
| California | $12,041,646 | $3,811,056 |
| New York | $7,630,090 | $2,141,660 |
| Oregon | $15,517,663 | $16,605,531 |
| Texas | $13,128,047 | $3,712,503 |

### 1.3 Market Penetration Rate per State

**Definition:** Our number of customers / (State population / 10,000)

| State | Customers | Population | Penetration Rate |
|-------|:---------:|:----------:|:----------------:|
| New Hampshire | 4 | 1,377,529 | 0.029 |
| Oregon | 10 | 4,237,256 | 0.024 |
| Colorado | 10 | 5,773,714 | 0.017 |
| California | 72 | 39,538,223 | 0.018 |
| New York | 40 | 19,453,561 | 0.021 |

### 1.4 Sales Efficiency per State

**Definition:** Average won deal amount / Average sales cycle days × Win probability (state-level average probability)

| State | Avg Won Amount | Avg Cycle Days | Avg Win Prob | Sales Efficiency |
|-------|:------------:|:--------------:|:----------:|:----------------:|
| Oregon | $164,725 | 188.8 | 56.21% | 490.40 |
| New York | $244,341 | 213.1 | 56.09% | 643.30 |
| California | $209,590 | 218.8 | 55.52% | 531.83 |
| Minnesota | $207,619 | 185.0 | 55.24% | 587.86 |
| Colorado | $182,824 | 201.6 | 55.32% | 501.54 |

### 1.5 Industry Concentration per State

**Definition:** Sum of customer share from the top 3 industries within each state

States with highest concentration (share ≥ 0.90): Alabama (1.00), Arizona (0.82), Arkansas (1.00), Colorado (0.90), Connecticut (0.83), Delaware (1.00), Idaho (1.00), Iowa (1.00), Kansas (1.00), Kentucky (0.60), etc.

The top industries overall among our customers are **Technology** (147 customers), **Manufacturing** (105), **Energy** (54), **Agriculture** (50), and **Financial Services** (47).

---

## 2. State Competition Intensity Assessment Model

**Model Design:** This model evaluates the competitive pressure in each state using three normalized components:
- **Inverse Win Probability** (35% weight): 100 − avg(probability) — lower win probability implies higher competition
- **Average Deal Size** (35% weight): Larger deals attract more competition
- **Sales Cycle Length** (30% weight): Longer cycles indicate higher competition

**Formula:** `Competition_Intensity = 0.35 × norm(inv_win_prob) + 0.35 × norm(deal_size) + 0.30 × norm(cycle_days)`

**Top 10 States by Competition Intensity:**

| State | Competition Intensity Score | Key Drivers |
|-------|:--------------------------:|-------------|
| Delaware | 68.26 | Very long cycle (257.7d), large deals |
| Mississippi | 64.18 | Low win probability, long cycle |
| New Mexico | 62.54 | Short cycle, high win probability (low comp) |
| Arkansas | 62.54 | Low win probability (50.39%) |
| South Dakota | 48.96 | Moderate cycle, moderate deal size |

**Lowest Competition States:** New Mexico (18.69), New Hampshire (31.56), West Virginia (36.54), Hawaii (39.10), Montana (40.03)

Higher competition intensity scores indicate markets where our sales team faces more difficult conditions — longer cycles, lower win rates, and larger deal sizes that attract more competitors.

---

## 3. State Investment Return Prediction Algorithm

**Model Design:** Predicts the investment return potential for each state using:
- **GDP per capita** (25%): Economic strength indicator
- **Market Maturity Score** (15%): Market development stage
- **Business Friendliness Index** (20%): Ease of doing business
- **Primary Industry Alignment** (15%): Whether the state's primary industry matches our top industries (Technology, Manufacturing, Financial Services, Energy, Healthcare)
- **Inverse Competition Intensity** (25%): Lower competition → higher return potential

**Formula:** `Investment_Return = 0.25×gdp_score + 0.15×maturity_score + 0.20×biz_score + 0.15×alignment + 0.25×(1−comp_intensity_score)`

**Top 10 States by Investment Return Score:**

| State | Return Score | Key Strengths |
|-------|:----------:|---------------|
| New York | 74.82 | High GDP/capita, strong financial services alignment |
| Wyoming | 74.06 | Low competition, business-friendly |
| California | 71.30 | High GDP, technology alignment |
| Oregon | 70.95 | Strong industry alignment, business-friendly |
| Delaware | 69.28 | Financial services hub, business-friendly |

---

## 4. Investment Efficiency Score — Full Ranking

The composite Investment Efficiency Score weights eight normalized dimensions:

| Component | Weight | Rationale |
|-----------|:-----:|-----------|
| Investment Return Score | 20% | Forward-looking economic potential |
| CAC (inverted) | 15% | Cost efficiency of customer acquisition |
| Market Penetration | 15% | Current market footprint |
| Sales Efficiency | 15% | Deal-making effectiveness |
| Avg Revenue | 10% | Customer value depth |
| Median Revenue | 10% | Customer value consistency |
| Competition Intensity | 10% | Market difficulty |
| Industry Concentration | 5% | Diversification risk |

### Complete State Ranking

| Rank | State | Efficiency Score | CAC ($) | Avg Revenue ($M) | Penetration | Sales Efficiency | Comp Intensity | Return Score |
|:----:|-------|:--------------:|:-------:|:---------------:|:----------:|:---------------:|:------------:|:----------:|
| 1 | Oregon | 68.72 | 705,000 | 15.5 | 0.024 | 490.4 | 47.2 | 70.95 |
| 2 | New Hampshire | 61.86 | 390,000 | 10.6 | 0.029 | 210.8 | 31.6 | 67.03 |
| 3 | New York | 60.76 | 543,396 | 7.6 | 0.021 | 643.3 | 57.6 | 74.82 |
| 4 | California | 59.01 | 573,267 | 12.0 | 0.018 | 531.8 | 53.8 | 71.30 |
| 5 | Colorado | 56.81 | 825,000 | 12.0 | 0.017 | 501.5 | 51.4 | 65.27 |
| 6 | Connecticut | 55.43 | 581,250 | 11.0 | 0.017 | 387.7 | 57.5 | 61.37 |
| 7 | Wyoming | 54.33 | 525,000 | 2.0 | 0.016 | 336.5 | 39.7 | 74.06 |
| 8 | Washington | 54.09 | 667,500 | 5.1 | 0.019 | 544.6 | 55.7 | 64.04 |
| 9 | Minnesota | 53.68 | 484,615 | 4.3 | 0.019 | 587.9 | 54.1 | 65.93 |
| 10 | Texas | 51.81 | 612,857 | 13.1 | 0.021 | 419.2 | 48.6 | 56.51 |
| 11 | Illinois | 51.02 | 850,000 | 12.7 | 0.017 | 463.1 | 51.9 | 57.69 |
| 12 | New Jersey | 50.30 | 785,294 | 6.5 | 0.016 | 428.9 | 55.5 | 60.15 |
| 13 | South Dakota | 50.03 | 450,000 | 16.1 | 0.009 | 661.5 | 49.0 | 38.00 |
| 14 | Delaware | 49.87 | 700,000 | 0.5 | 0.010 | 187.9 | 61.8 | 69.28 |
| 15 | Virginia | 49.84 | 540,000 | 3.4 | 0.014 | 471.7 | 52.8 | 64.96 |
| 16 | Alabama | 48.79 | 728,571 | 29.8 | 0.012 | 838.6 | 44.9 | 43.98 |
| 17 | Pennsylvania | 47.70 | 1,143,750 | 11.8 | 0.024 | 876.1 | 44.0 | 50.54 |
| 18 | Kansas | 46.65 | 975,000 | 19.3 | 0.006 | 1142.3 | 60.2 | 41.89 |
| 19 | Massachusetts | 46.57 | 710,526 | 3.9 | 0.019 | 817.8 | 52.1 | 54.04 |
| 20 | Montana | 46.16 | 330,000 | 1.5 | 0.006 | 701.4 | 40.0 | 64.22 |
| 21 | Ohio | 45.89 | 626,087 | 3.5 | 0.014 | 851.6 | 47.2 | 61.13 |
| 22 | Oklahoma | 45.69 | 990,000 | 7.5 | 0.015 | 534.0 | 46.5 | 55.81 |
| 23 | Maryland | 44.78 | 725,000 | 5.3 | 0.020 | 961.3 | 57.5 | 49.83 |
| 24 | Arizona | 44.70 | 750,000 | 3.8 | 0.015 | 947.7 | 53.8 | 50.54 |
| 25 | Idaho | 44.60 | 1,650,000 | 4.3 | 0.016 | 1437.6 | 58.4 | 53.50 |
| 26 | Michigan | 44.13 | 558,333 | 8.3 | 0.012 | 970.7 | 53.2 | 49.74 |
| 27 | Missouri | 43.80 | 613,636 | 3.5 | 0.014 | 694.8 | 50.5 | 51.11 |
| 28 | Wisconsin | 43.27 | 675,000 | 6.1 | 0.010 | 683.5 | 52.9 | 52.50 |
| 29 | Tennessee | 43.26 | 1,200,000 | 3.5 | 0.015 | 890.7 | 58.7 | 53.69 |
| 30 | Louisiana | 41.85 | 435,000 | 6.7 | 0.009 | 1183.7 | 49.1 | 43.93 |
| 31 | Georgia | 41.54 | 585,000 | 15.9 | 0.013 | 984.2 | 51.2 | 39.44 |
| 32 | Indiana | 41.28 | 675,000 | 4.6 | 0.011 | 671.8 | 45.5 | 51.28 |
| 33 | Nevada | 40.05 | 500,000 | 1.9 | 0.015 | 691.4 | 41.6 | 46.97 |
| 34 | Utah | 39.04 | 1,875,000 | 11.1 | 0.007 | 1789.4 | 47.8 | 53.50 |
| 35 | South Carolina | 38.85 | 637,500 | 8.1 | 0.008 | 615.8 | 50.8 | 40.26 |
| 36 | Rhode Island | 38.85 | — | 9.5 | 0.007 | 0.0 | 35.9 | 68.18 |
| 37 | Florida | 38.63 | 785,714 | 7.3 | 0.010 | 860.5 | 48.7 | 44.43 |
| 38 | Kentucky | 38.55 | 557,143 | 3.9 | 0.008 | 792.7 | 53.1 | 44.22 |
| 39 | Mississippi | 38.34 | 1,200,000 | 6.7 | 0.003 | 295.1 | 64.2 | 46.20 |
| 40 | Arkansas | 37.78 | 562,500 | 2.3 | 0.007 | 1416.0 | 62.5 | 40.15 |
| 41 | North Dakota | 36.13 | — | 0.0 | 0.000 | 5774.4 | 68.7 | 56.58 |
| 42 | North Carolina | 34.29 | 1,216,667 | 6.1 | 0.010 | 557.9 | 43.5 | 42.74 |
| 43 | West Virginia | 33.48 | 450,000 | 5.6 | 0.004 | 980.1 | 36.5 | 33.69 |
| 44 | Iowa | 32.82 | — | 2.3 | 0.013 | 472.1 | 42.6 | 58.12 |
| 45 | Maine | 31.31 | 1,350,000 | 7.7 | 0.007 | 116.5 | 46.8 | 34.79 |
| 46 | New Mexico | 27.14 | — | 7.8 | 0.006 | 337.7 | 18.7 | 51.63 |
| 47 | Hawaii | 26.39 | 1,200,000 | 2.2 | 0.007 | 450.1 | 39.1 | 35.24 |
| 48 | Nebraska | 20.88 | — | 0.0 | 0.000 | 442.9 | 57.7 | 58.23 |
| 49 | Vermont | 13.55 | — | 0.0 | 0.000 | 133.9 | 21.0 | 59.87 |
| 50 | Alaska | 12.99 | — | 0.0 | 0.000 | 34.9 | 25.1 | 57.58 |

*Note: States with "—" CAC have zero new customers (won New Business opportunities) in our data. These represent greenfield expansion opportunities.*

---

## 5. Visualizations

### Full State Ranking
![Full State Ranking](full_ranking.png)

### Top 10 States — Key Metrics Panel
![Top 10 Key Metrics](top10_panel.png)

### Competition Intensity vs Investment Return
![Competition vs Return](comp_return_scatter.png)

### Customer Acquisition Cost vs Market Penetration
![CAC vs Penetration](cac_pen_scatter.png)

---

## 6. 3-Year Regional Expansion Priority Recommendation

Based on the composite Investment Efficiency Score, states are grouped into three tiers:

### Tier 1: High Priority — Aggressive Investment (Ranks 1–10)
**States:** Oregon, New Hampshire, New York, California, Colorado, Connecticut, Wyoming, Washington, Minnesota, Texas

**Strategy:** These states demonstrate high average customer value, strong market penetration, favorable investment return potential, and manageable competition. Recommendations:
- **Year 1:** Increase sales rep allocation by 15–25% in California, New York, and Texas (largest markets with established presence)
- **Year 2:** Expand targeted marketing programs in Colorado, Washington, and Oregon (high-growth technology hubs)
- **Year 3:** Establish regional centers of excellence in New Hampshire, Connecticut, and Minnesota (cost-efficient markets with strong penetration)

### Tier 2: Moderate Priority — Targeted Growth (Ranks 11–25)
**States:** Illinois, New Jersey, South Dakota, Delaware, Virginia, Alabama, Pennsylvania, Kansas, Massachusetts, Montana, Ohio, Oklahoma, Maryland, Arizona, Idaho

**Strategy:** These states show solid fundamentals but have room for improvement in CAC or market penetration. Recommendations:
- **Year 1:** Conduct market deep-dives in Virginia, Maryland, and Arizona (strong return scores, moderate competition)
- **Year 2:** Optimize sales operations in Illinois, Pennsylvania, Ohio (large population but high CAC)
- **Year 3:** Selective investment in Massachusetts, South Dakota, Delaware (niche strengths)

### Tier 3: Monitor/Develop (Ranks 26–50)
**States:** Michigan, Missouri, Wisconsin, Tennessee, Louisiana, Georgia, Indiana, Nevada, Utah, South Carolina, Rhode Island, Florida, Kentucky, Mississippi, Arkansas, North Dakota, North Carolina, West Virginia, Iowa, Maine, New Mexico, Hawaii, Nebraska, Vermont, Alaska

**Strategy:** These states require either operational improvements before scaling (high CAC, low penetration) or are greenfield opportunities with no current customer base. Recommendations:
- **Year 1:** Analyze best-practice transfer from Tier 1 states to Florida, Georgia, and North Carolina (large population centers underperforming)
- **Year 2:** Pilot programs in Nebraska, North Dakota, and Vermont (greenfield states with favorable economic indicators)
- **Year 3:** Reassess remaining states based on Tier 1/2 expansion outcomes

---

## 7. Methodology Notes & Limitations

**Methodology:**
- All metrics are computed at the state level using the supplied Salesforce data and economic indicators.
- CAC uses "New Business" won opportunities as the definition of new customer acquisition.
- Sales representatives are counted per state by the distinct owner_ids operating in each billing state.
- All composite scores use min-max normalization followed by weighted averaging.
- The Competition Intensity Model and Investment Return Prediction Algorithm are custom-designed models using the available data features.

**Limitations:**
- The account data contains a single snapshot date, limiting the ability to track customer acquisition over time.
- "New customers" had to be inferred from won "New Business" opportunities rather than from account creation dates.
- Sales rep state assignment is based on the billing state of accounts they manage, which may not perfectly reflect their physical office location.
- Four states (Alaska, Nebraska, North Dakota, Vermont) have no Customer-type accounts in our data, resulting in undefined CAC and zero market penetration. Their rankings are based primarily on economic indicators and opportunity data.
- The composite score weights are based on analytical judgment and should be calibrated with actual ROI data over time.
- The win probability used in Sales Efficiency is the average `probability` field across all opportunities, which represents forecasted probability rather than actual win rate.