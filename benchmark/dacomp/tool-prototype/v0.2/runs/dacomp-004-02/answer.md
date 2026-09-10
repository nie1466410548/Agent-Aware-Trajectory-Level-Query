# Monthly Top Products Analysis

## 1. Monthly Top Product by Sales Amount

For each of the four months in the dataset (January–April 2015), the product with the highest total Sales Amount is:

| Sales Month | Product Code | Product Description | Sales Amount |
|-------------|-------------|-------------------|:------------:|
| 2015-01 | **DW-1001040125** | Pork bones (sold loose by weight) – Fresh food | **2,836.46** |
| 2015-02 | **DW-2316020016** | Domestic cigarettes (out-of-province, 20 sticks) – General merchandise | **5,600.00** |
| 2015-03 | **DW-1203130446** | Other fruits (sold loose by weight) – Fresh food | **4,893.62** |
| 2015-04 | **DW-1518040045** | Tetra Pak brick acidified milk drink (205ml) – General merchandise | **1,400.30** |

---

## 2. Cross-Month Performance of the Top Products

Each product's monthly sales and rank among all products (out of ~2,800–3,200 products per month):

| Product Code | Category | 2015-01 | 2015-02 | 2015-03 | 2015-04 | Total Sales |
|-------------|----------|:-------:|:-------:|:-------:|:-------:|:----------:|
| **DW-1001040125** | Pork bones (Fresh food) | **2,836.46** (Rank 1/3198) | 711.01 (Rank 24/3047) | 1,220.88 (Rank 3/2841) | 1,180.53 (Rank 4/2955) | **5,948.88** |
| **DW-2316020016** | Domestic cigarettes (out-of-province) | — | **5,600.00** (Rank 1/3047, 2 transactions) | — | — | **5,600.00** |
| **DW-1203130446** | Other fruits (Fresh food) | 797.79 (Rank 14/3198) | 1,095.26 (Rank 12/3047) | **4,893.62** (Rank 1/2841) | 598.16 (Rank 17/2955) | **7,384.83** |
| **DW-1518040045** | Acidified milk drink (205ml) | — | — | — | **1,400.30** (Rank 1/2955) | **1,400.30** |

**Key observations:**
- **DW-1203130446 (Other fruits)** was the most consistently high-performing product, present in all four months and achieving the highest cumulative sales (7,384.83). It ranked #1 in March and placed in the top 20 in all other months. It also had the broadest customer base (227 distinct customers).
- **DW-1001040125 (Pork bones)** was also present in all four months, with strong sales in January (#1), March (#3) and April (#4), though it had a dip in February (rank #24). It served 104 distinct customers.
- **DW-2316020016 (Cigarettes)** had a remarkable sales spike in February (5,600.00) from only **2 transactions** (2 customers), suggesting a very high unit price or bulk purchase. It appeared in no other month.
- **DW-1518040045 (Acidified milk drink)** appeared only in April, with 36 transactions across 34 customers, achieving the top rank but with a much lower absolute sales amount than the other monthly winners.

---

## 3. Relationship Between Repurchase Rate and Sales Amount

Two complementary definitions of repurchase rate are used:

**Definition A – Customer-level repurchase rate:**  
% of customers who purchased the product in ≥2 distinct months.

**Definition B – Transaction-level repeat purchase ratio:**  
% of purchase events (rows) that are repeat purchases by the same customer (i.e., the customer had bought the same product in a prior month).

| Product Code | Total Sales | Total Customers | Customer-Level Repurchase Rate | Transaction-Level Repeat Ratio | Months Active |
|-------------|:----------:|:--------------:|:----------------------------:|:----------------------------:|:-------------:|
| DW-1203130446 (Other fruits) | **7,384.83** | 227 | **12.33%** (28/227) | **34.01%** (117/344) | 4 |
| DW-1001040125 (Pork bones) | **5,948.88** | 104 | **7.69%** (8/104) | **12.61%** (15/119) | 4 |
| DW-2316020016 (Cigarettes) | 5,600.00 | 2 | **0.00%** (0/2) | **0.00%** (0/2) | 1 |
| DW-1518040045 (Milk drink) | 1,400.30 | 34 | **0.00%** (0/34) | **5.56%** (2/36) | 1 |

**Analysis of the relationship:**

1. **Positive correlation between scale and repurchase rate:**  
   Products active across multiple months (DW-1203130446 and DW-1001040125) had both the highest total sales and the highest repurchase rates. The fruit product, with the broadest customer base (227 customers) and longest presence (4 months), exhibited the strongest repurchase behavior (12.33% of customers repurchased across months; 34.01% of all purchase events were repeat purchases).

2. **One-time-high-volume products show no repurchase:**  
   DW-2316020016 (cigarettes) and DW-1518040045 (milk drink) appeared in only one month each, giving them zero opportunity for cross-month repurchase. The cigarette product's very high sales (5,600.00) came from just 2 customers, suggesting a high-value bulk transaction rather than a repeat-purchase dynamic.

3. **Transaction-level vs. customer-level differences:**  
   For DW-1203130446, the transaction-level repeat ratio (34.01%) is much higher than the customer-level repurchase rate (12.33%), indicating that repurchasing customers tend to buy more frequently (multiple transactions per month or across months). This pattern suggests strong customer loyalty for the fruit product.

4. **Overall pattern:**  
   High cumulative sales are associated with both a large customer base and a meaningful repurchase rate. Products that can sustain repeat purchases across months (like the fruit product) achieve the highest total sales. Products with a single-month sales spike from a few high-value transactions can achieve a high peak but lack the sustained customer base of repeat-purchase products.

**Limitations:** This analysis is limited to tabular data; no Python or figure generation tools were available. The dataset covers only four months (Jan–Apr 2015), so repurchase opportunities are limited. The repurchase rate can only capture cross-month repeat behavior, not within-month repeat purchases. A longer time series would provide a more complete picture.