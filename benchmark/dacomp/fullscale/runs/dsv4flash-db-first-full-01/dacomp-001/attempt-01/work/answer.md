# Credit Risk Analysis and Allocation Plan for SMEs

## 1. Overview

This report analyzes the credit risk of **123 enterprises with credit histories** (ch___ tables) using their existing Credit Ratings, revenue capacity, profit stability, and upstream/downstream dependency. Based on the analysis, we design a credit limit allocation plan for a total annual credit of **RMB 100 million** and an interest rate schedule incorporating churn rate optimization.

### Data Sources
- **ch___company_info**: 123 companies with Credit Ratings (A/B/C/D) and Default status
- **ch___sales_invoices**: 162,484 valid sales invoices (2016–2020)
- **ch___input_invoices**: 210,947 valid input invoices (2016–2020)
- **annual_rate_&_churn**: 29 interest rate tiers with corresponding churn rates for Ratings A, B, C

---

## 2. Quantitative Credit Risk Analysis

### 2.1 Default Rates by Rating

| Rating | Count | Defaults | Default Rate |
|--------|------:|---------:|------------:|
| **A**  | 27    | 0        | **0.00%**   |
| **B**  | 38    | 1        | **2.63%**   |
| **C**  | 34    | 2        | **5.88%**   |
| **D**  | 24    | 24       | **100.00%** |

Rating D comprises entirely defaulted enterprises. The existing credit rating is a strong predictor of default risk.

### 2.2 Financial Metrics by Rating

| Rating | Avg Revenue (RMB) | Avg Profit Margin | Avg Revenue Volatility (CV) | Avg Top-1 Buyer Share | Avg Top-1 Supplier Share | Avg Risk Score |
|--------|------------------:|:-----------------:|:---------------------------:|:---------------------:|:------------------------:|:--------------:|
| **A**  | 330,362,448       | 0.50              | 0.67                        | 0.17                  | 0.39                     | 0.22           |
| **B**  | 57,252,744        | 0.24              | 0.75                        | 0.33                  | 0.43                     | 0.36           |
| **C**  | 111,079,786       | 0.62              | 0.74                        | 0.40                  | 0.50                     | 0.47           |
| **D**  | 3,132,431         | -0.78             | 0.70                        | 0.49                  | 0.45                     | 0.65           |

**Key observations:**
- **Rating A** has the highest revenue, healthy margins, and lowest concentration risk — the safest segment.
- **Rating B** has moderate revenue, lower margins, and higher volatility — medium risk.
- **Rating C** shows mixed characteristics: some have high revenue but with high upstream/downstream dependency.
- **Rating D** has minimal revenue, negative margins, and the highest risk scores — all have defaulted.

### 2.3 Risk Scoring Model

We constructed a composite risk score using six weighted factors:

| Factor | Weight | Rationale |
|--------|:------:|-----------|
| Credit Rating (ordinal) | 30% | Existing rating encodes default history |
| Revenue Capacity (log) | 20% | Higher revenue → better repayment capacity |
| Profit Margin | 15% | Higher margin → sustainable operations |
| Revenue Stability (CV⁻¹) | 15% | Lower CV → more stable earnings |
| Downstream Dependency (Top-1 buyer share) | 10% | High concentration → vulnerability to customer loss |
| Upstream Dependency (Top-1 supplier share) | 10% | High concentration → supply chain vulnerability |

**Validation:** Defaulted companies have significantly higher risk scores (mean 0.63 ± 0.11) vs non-defaulted (mean 0.36 ± 0.11), confirming the model's discriminative power.

![Risk Factor Comparison](risk_factors.png)

### 2.4 Risk Tier Distribution

| Risk Tier | Count | Defaults | Default Rate |
|-----------|------:|---------:|------------:|
| Very Low  | 25    | 0        | 0.0%         |
| Low       | 24    | 1        | 4.2%         |
| Medium    | 25    | 0        | 0.0%         |
| High      | 24    | 5        | 20.8%        |
| Very High | 25    | 21       | 84.0%        |

The five-tier risk classification clearly separates default risk, supporting differentiated pricing.

---

## 3. Interest Rate Optimization with Churn

### 3.1 Churn Rate Analysis

The `annual_rate_&_churn` table provides churn rates for each rating at 29 interest rate levels (4.0%–15.0%). Higher interest rates drive higher customer churn (companies leaving the bank), creating a trade-off:

- **Rate 4.0%**: 0% churn for all ratings (baseline)
- **Rate 4.65% (optimal for A)**: 13.6% churn for A, 13.5% for B, 12.2% for C
- **Rate 5.85% (optimal for B, C)**: 34.7% churn for A, 30.3% for B, 29.0% for C
- **Rate 15.0%**: 92.2% churn for A, 88.6% for B, 89.5% for C

### 3.2 Optimal Interest Rates

The optimal rate maximizes the **expected return rate** = rate × (1 − churn_rate):

| Rating | Optimal Rate | Churn Rate | Expected Return Rate |
|--------|:-----------:|:----------:|:-------------------:|
| **A**  | **4.65%**   | 13.57%     | 4.02%               |
| **B**  | **5.85%**   | 30.29%     | 4.08%               |
| **C**  | **5.85%**   | 29.02%     | 4.15%               |

![Rate Optimization](rate_optimization.png)

**Rationale:** Rating A achieves maximum expected return at a lower rate (4.65%) because A-rated customers are more sensitive to rate increases (churn accelerates faster). Ratings B and C perform best at 5.85% — their higher baseline risk justifies a higher rate, and the churn response is less severe at this level.

### 3.3 Rate Adjustment by Risk Tier (Within Rating)

Within each rating, we apply a premium based on the company's risk tier:

| Risk Tier | Rate Adjustment | Rationale |
|-----------|:--------------:|-----------|
| Very Low  | +0.0%          | Best-in-class risk |
| Low       | +0.5%          | Slightly elevated risk |
| Medium    | +1.0%          | Moderate risk premium |
| High      | +1.5%          | Significant risk premium |
| Very High | +2.0%          | Maximum risk premium |

**Rating D:** All D-rated companies have defaulted. We assign the maximum rate of 15.0% and recommend **denying new credit** to this segment (see Section 5).

---

## 4. Credit Limit Allocation Plan (Revised)

### 4.1 Allocation Logic

Credit limits are allocated proportionally to a **capacity-weighted risk score**:

```
Credit Weight = (1 − Risk Score) × log(1 + Total Revenue)
```

This ensures:
- **Lower risk score** → higher weight (risk-return trade-off)
- **Higher revenue** → higher weight (repayment capacity)
- **Diminishing returns** for ultra-large revenue (log transform)

### 4.2 Revised Plan (Excluding D-Rated)

Since Rating D companies have all defaulted (100% default rate), extending credit to them guarantees principal loss. The revised plan allocates the full RMB 100 million among **99 non-defaulted enterprises** (A + B + C).

**Total allocation by rating:**

| Rating | Total Credit (RMB) | Share | Avg Rate | Expected Income | Expected Loss | Net Return |
|--------|------------------:|:-----:|:--------:|:--------------:|:-------------:|:----------:|
| A      | 35,145,643        | 35.1% | 4.74%    | 1,411,012      | 0             | 1,411,012  |
| B      | 37,609,651        | 37.6% | 6.56%    | 1,464,749      | 1,053,774     | 410,975    |
| C      | 27,244,706        | 27.2% | 7.23%    | 1,020,837      | 1,529,111     | −508,274   |
| **Total** | **100,000,000** | **100%** | **5.91%** | **3,896,597** | **2,582,885** | **1,313,712** |

**Portfolio expected net return: RMB 1,313,712 (1.31% net return rate)**

### 4.3 Detailed Allocation by Rating × Risk Tier

| Rating | Risk Tier | # Firms | Total Credit (万RMB) | Avg Credit (万RMB) | Avg Rate | Expected Income (万RMB) |
|--------|-----------|:------:|:-------------------:|:------------------:|:--------:|:----------------------:|
| **A**  | Very Low  | 23      | 3,111.8             | 135.3              | 4.65%    | 125.1                  |
|       | Low       | 3       | 319.5               | 106.5              | 5.15%    | 12.8                   |
|       | Medium    | 1       | 83.3                | 83.3               | 5.65%    | 3.3                    |
| **B**  | Very Low  | 2       | 261.3               | 130.7              | 5.85%    | 10.7                   |
|       | Low       | 20      | 2,120.2             | 106.0              | 6.35%    | 84.8                   |
|       | Medium    | 14      | 1,220.6             | 87.2               | 6.85%    | 45.3                   |
|       | High      | 2       | 158.8               | 79.4               | 7.35%    | 5.7                    |
| **C**  | Low       | 1       | 102.6               | 102.6              | 6.35%    | 4.2                    |
|       | Medium    | 10      | 993.8               | 99.4               | 6.85%    | 36.9                   |
|       | High      | 19      | 1,416.0             | 74.5               | 7.35%    | 52.8                   |
|       | Very High | 4       | 212.1               | 53.0               | 7.85%    | 8.1                    |

**Top 10 firms by credit limit** (all A-rated, Very Low risk tier, avg credit ~1.36M RMB at 4.65%).

![Credit Analysis](credit_analysis.png)

### 4.4 Rules for Credit Limit Variation with Risk

| Risk Level | Rating | Risk Tier | Limit Range (万RMB) | Interest Rate | Rationale |
|-----------|:------:|:---------:|:-------------------:|:-------------:|-----------|
| **Lowest** | A | Very Low | 120–150 | 4.65% | Maximum capacity, zero defaults, high margins |
| **Low** | A/B | Low | 80–110 | 5.15%–6.35% | Good profile, slight adjustments |
| **Medium** | A/B/C | Medium | 70–100 | 5.65%–6.85% | Moderate risk, moderate rate premium |
| **High** | B/C | High | 50–80 | 7.35% | Elevated risk, higher rate to compensate |
| **Highest** | C | Very High | 30–60 | 7.85% | Highest risk among non-defaulted, smallest limits |
| **Defaulted** | D | Any | **Denied** | 15.0% | All D-rated firms have defaulted; no new credit |

---

## 5. Key Recommendations

1. **Deny new credit to D-rated enterprises** — All 24 D-rated firms have defaulted, making any new lending a guaranteed loss.

2. **Prioritize A-rated (Very Low risk) enterprises** — 23 of 27 A-rated firms fall in the Very Low risk tier, collectively receiving 31.1% of the total credit. Their 0% default rate and 4.65% optimal rate deliver the highest risk-adjusted return.

3. **Apply risk-tier premiums within each rating** — Premiums of 0.5%–2.0% over the base optimal rate for higher-risk companies within the same rating class ensure adequate compensation for elevated risk.

4. **Monitor churn dynamics** — The optimal rate for each rating represents the peak of the expected return curve. Raising rates beyond this point reduces total expected revenue due to excessive customer churn.

5. **Expected portfolio performance** — The revised plan yields RMB 1.31M net expected return (1.31% of total credit), with RMB 3.90M in interest income partially offset by RMB 2.58M in expected losses from B and C-rated defaults.

---

## 6. Limitations

- The risk score model weights are expert-assigned (not empirically optimized via logistic regression) due to the small number of defaults (3 out of 99 non-D-rated firms).
- Churn rates are drawn from the aggregate table and may not capture firm-specific rate sensitivity.
- Revenue volatility (CV) is computed from 2–4 years of data; longer histories would improve stability estimates.
- Upstream/downstream dependency measured by top-1 concentration; a Herfindahl-Hirschman Index over all partners would provide a more refined measure.

---

*Figures: [credit_analysis.png](credit_analysis.png), [rate_optimization.png](rate_optimization.png), [risk_factors.png](risk_factors.png)*