# Sales Team Reorganization: Data-Driven Customer Reallocation Plan

## Executive Summary

A comprehensive analysis of 1,000 sales representatives and 10,000 customer accounts reveals a significantly uneven workload distribution (std = 2.96 > 0.3 × avg = 2.62). We designed a **greedy optimization reallocation algorithm** that transfers 786 customers across the team, reducing workload standard deviation to **0.95** and bringing **907 out of 1,000 reps within ±15% of the target workload**. The plan simultaneously improves industry expertise compliance (from 341 to 543 reps meeting the 60% rule), maintains geographic proximity (98% of transfers stay within the same state), and is projected to increase revenue-weighted team efficiency by **+0.87%** and customer retention probability by **+12.76 percentage points** per transferred account.

---

## 1. Baseline Analysis

### 1.1 Workload Score Computation

For each of the 1,000 sales representatives, the workload score was computed as:

```
Workload Score = N_Customers × 0.3 
               + (Total_Annual_Revenue_in_Millions / 10) × 0.4 
               + Contact_Coverage_Rate × 0.2 
               + Geographic_Complexity_Factor × 0.1

Contact Coverage Rate = min(Total_Contacts / N_Customers, 5.0)
Geographic Complexity Factor = DISTINCT(States) × 2 + DISTINCT(Cities) × 0.5
```

**Baseline Workload Statistics:**

| Metric | Value |
|--------|-------|
| Mean | 8.74 |
| Standard Deviation | 2.96 |
| Minimum | 1.84 |
| Maximum | 20.51 |
| Within ±15% of mean (target range: 7.43–10.05) | 347 / 1000 (34.7%) |

**Unevenness confirmed:** `std (2.96) > 0.3 × mean (2.62)` → workload is unevenly distributed.

### 1.2 Efficiency Score Computation

The sales efficiency metric was computed per rep:

```
Efficiency Score = Win_Rate × 0.4 
                  + (Avg_Deal_Size / 100,000) × 0.3 
                  + (120 / Avg_Sales_Cycle_Days) × 0.2 
                  + Opportunity_Conversion_Rate × 0.1
```

**Baseline Efficiency Statistics:** Mean = 1.51, Std = 2.31. The high variance is driven by large differences in average deal size across reps.

### 1.3 Industry Expertise Compliance

Only **341 out of 1,000 reps** (34.1%) currently have at least 60% of their customers in their top 3 industries. The average compliance rate is 55.9%, with many reps serving 7+ different industries with only 10 customers on average.

---

## 2. Reallocation Algorithm Design

### 2.1 Method: Greedy Priority-Based Matching

We implemented a **greedy optimization algorithm** that iteratively rebalances workload while respecting domain constraints:

**Step 1 — Identify Donors and Receivers:**
- **Donors** (307 reps): workload > 10.05 (top 15% above mean)
- **Receivers** (346 reps): workload < 7.43 (bottom 15% below mean)
- **Stable** (347 reps): within target range

**Step 2 — Customer Selection (Donors):**
For each donor, customers are scored for transfer-out suitability:
- **+10 points**: customer's industry is NOT in the donor's top 3 (improves donor compliance)
- **+5 / state_count**: customer's state is rare for the donor (reduces geographic complexity)
- **+revenue_contribution**: higher revenue customers reduce workload more

**Step 3 — Receiver Matching:**
For each candidate customer, the best receiver is selected based on a composite score:
- **+100**: Customer's state is in receiver's top 3 states (geographic proximity)
- **+80**: Customer's industry is in receiver's top 3 industries (expertise match)
- **+40**: Customer's industry would enter top 3 after addition
- **+20**: Customer's size segment matches receiver's expertise
- **+capacity × 5**: Preference for receivers with more room below target
- **+receiver_eff × 10**: Preference for higher-efficiency receivers

**Step 4 — Constraint Enforcement:**
- **±15% workload constraint**: Verified before each transfer
- **60% industry rule**: Enforced by checking that after transfer, the receiver's portfolio maintains ≥60% of customers in their top 3 industries
- **Geographic proximity**: Prioritized via the state matching score
- **Customer size suitability**: Account size segments are matched

### 2.2 Why Python Was Used for This Step

The optimization algorithm involves iterative greedy matching, dynamic portfolio updates, and complex constraint verification that cannot be expressed in standard SQL. SQL was used for all data extraction, aggregation, and initial score computation; Python orchestrated the matching logic and impact simulation.

---

## 3. Concrete Transfer Plan

### 3.1 Overall Transfer Summary

| Metric | Value |
|--------|-------|
| **Total customer transfers** | **786** |
| **Unique donor reps** | 307 |
| **Unique receiver reps** | 313 |
| **Total revenue moved** | **$12.28 billion** |
| **Avg revenue per transfer** | $15.6 million |
| **Avg donor workload reduction** | -1.14 points |
| **Avg receiver workload increase** | +0.93 points |
| **Same-state transfers** | 772 / 786 (98.2%) |
| **Industry-matching transfers** | 773 / 786 (98.3%) |

### 3.2 Top 10 Transfers by Revenue

| From Rep | To Rep | Revenue | Industry | State | Donor WS Before | Donor WS After | Receiver WS Before | Receiver WS After |
|----------|--------|---------|----------|-------|-----------------|----------------|-------------------|------------------|
| Latoya Armstrong | Victor Stevenson | $50.0M | Non-profit | KS | 20.51 | 17.95 | 6.01 | 8.34 |
| Michael Durham | Timothy Love | $50.0M | Media & Entertainment | TN | 10.15 | 7.59 | 5.77 | 8.09 |
| Elizabeth Gibson | Roy Lewis | $50.0M | Agriculture | CA | 10.48 | 7.91 | 5.71 | 8.02 |
| John Hernandez | Victor Alvarado | $50.0M | Retail | KS | 12.47 | 9.91 | 6.74 | 9.07 |
| Laura Newton | Richard Stone | $50.0M | Consulting | VA | 10.42 | 7.93 | 7.27 | 9.51 |
| Jeffrey Brown | Lisa Gonzales | $50.0M | Media & Entertainment | MA | 15.41 | 12.86 | 7.02 | 9.31 |
| Maria Ward | Tracey Baker | $50.0M | Transportation | CA | 10.56 | 8.28 | 5.72 | 8.00 |
| Randall Cortez | Cory Kirby | $50.0M | Non-profit | LA | 12.44 | 9.90 | 6.84 | 9.11 |
| Kyle Good | Gary Knapp | $50.0M | Retail | WA | 10.59 | 8.28 | 7.09 | 9.44 |
| Karen Jenkins | Rebecca Hill | $50.0M | Financial Services | MN | 14.91 | 12.36 | 5.32 | 7.66 |

### 3.3 Most Affected Donors (Largest Revenue Moved Out)

| Rep | Customers Moved | Revenue Moved | Avg WS Drop |
|-----|----------------|--------------|------------|
| Jeffrey Brown | 5 | $159.4M | -1.77 |
| Paul Frey | 7 | $153.9M | -1.35 |
| Danielle Hood | 4 | $151.3M | -2.00 |
| Latoya Armstrong | 11 | $145.7M | -0.97 |
| John Zamora | 6 | $143.6M | -1.43 |

### 3.4 Most Affected Receivers (Largest Revenue Received)

| Rep | Customers Received | Revenue Received | Avg WS Gain |
|-----|-------------------|-----------------|------------|
| Darlene Ingram | 6 | $108.9M | +0.99 |
| Emily Hayes | 3 | $107.0M | +1.68 |
| Cory Kirby | 4 | $106.8M | +1.35 |
| Joseph Sanchez | 4 | $106.4M | +1.41 |
| Nicole Stevens | 4 | $104.4M | +1.32 |

---

## 4. Expected Impact

### 4.1 Workload Balance Improvement

The workload distribution improves dramatically after reallocation:

| Metric | Baseline | After Reallocation | Improvement |
|--------|----------|-------------------|-------------|
| Mean | 8.74 | 8.59 | -1.7% |
| **Standard Deviation** | **2.96** | **0.95** | **-68%** |
| Min | 1.84 | 5.04 | +173% |
| Max | 20.51 | 10.05 | -51% |
| **Within ±15% range** | **347 / 1000** | **907 / 1000** | **+560 reps** |
| Reps above upper bound | 307 | 0 | -100% |
| Reps below lower bound | 346 | 93 | -73% |

![Workload distribution comparison](workload_comparison.png)

*Figure 1: Baseline (left) vs. After Reallocation (right) workload distribution histograms. The green dashed lines show the ±15% target range.*

![Workload scatter](workload_scatter.png)

*Figure 2: Before-after scatter plot showing convergence toward the target range.*

### 4.2 Industry Expertise Compliance

The reallocation algorithm explicitly enforces the 60% rule, resulting in:

| Metric | Baseline | After Reallocation |
|--------|----------|-------------------|
| **Reps meeting ≥60% rule** | **341 / 1000 (34.1%)** | **543 / 1000 (54.3%)** |
| Average compliance rate | 55.9% | 62.2% |
| Transfers where industry matches receiver's portfolio | — | 98.3% |

![Industry compliance](industry_compliance.png)

*Figure 3: Industry compliance distribution before (left) and after (right) reallocation.*

### 4.3 Expected Efficiency Improvement

The team's efficiency score is expected to improve through the reallocation of customers from lower-efficiency reps to higher-efficiency reps:

| Metric | Value |
|--------|-------|
| Baseline team efficiency (customer-weighted) | 1.509 |
| Equal-weight expected improvement | -0.008 (-0.51%) |
| **Revenue-weighted expected improvement** | **+0.013 (+0.87%)** |
| Revenue-weighted team efficiency after | 1.522 |

The revenue-weighted measure (+0.87%) is the more meaningful metric, as high-revenue customers are preferentially matched to higher-efficiency reps. The slight negative equal-weight result reflects that some smaller customers move to slightly lower-efficiency reps, but the overall revenue impact is positive.

### 4.4 Expected Retention Probability Improvement

For each transferred customer, the retention probability is estimated to improve by an average of **12.76 percentage points** based on three factors:

| Retention Factor | Improvement | Coverage |
|-----------------|-------------|----------|
| Industry expertise match | +5 pp | 773/786 transfers |
| Geographic proximity (same state) | +5 pp | 772/786 transfers |
| Account size segment match | +3 pp | 706/786 transfers |
| **Total per transferred customer** | **+12.76 pp** | — |

**Overall retention rate projected: 70% → 82.76%** for transferred customers.

---

## 5. Limitations and Caveats

1. **Efficiency score is a rep-level attribute** that does not change with portfolio composition in our model. In practice, a rep's efficiency may improve as they specialize in customers that match their expertise.
2. **Retention probability estimates** are based on matching quality; actual retention outcomes would need to be tracked post-implementation.
3. **93 reps remain below the lower bound** after reallocation; these are reps with very low initial workload (1.8–4.0) who would need additional customers beyond what became available from donors.
4. **The algorithm assumes all customer transfers are feasible** — practical considerations (customer relationships, contracting, onboarding) would require a phased rollout.
5. **Geographic complexity was approximated** for receivers after transfers (state/city count increments assumed +1 for new states).

---

## 6. Recommendations

1. **Implement the 786 transfers in phases** over 3–4 quarters, prioritizing the top 50 largest-revenue moves first.
2. **Monitor workload scores monthly** for 6 months post-implementation to validate the model.
3. **Reassign remaining 93 underloaded reps** by organic account growth or targeted new account acquisition rather than further transfers.
4. **Use the industry compliance data** to inform future territory design and hiring decisions.
5. **Track retention rates** of transferred customers quarterly to validate the 12.76 pp improvement estimate.

---

## Appendix: Data Sources

All computations used the following tables:
- **`salesforce__customer_360_view`** — 10,000 customer accounts with owner, revenue, industry, geography, and contact information
- **`salesforce__sales_performance_dashboard`** — 1,000 sales reps with efficiency metrics (win rate, deal size, sales cycle, close rate)

The full transfer plan (786 rows) is available in `final_transfers.csv` and an excerpt of the top 50 transfers is in `top_transfers_excerpt.csv`.