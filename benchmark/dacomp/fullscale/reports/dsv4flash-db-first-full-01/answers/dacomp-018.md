<!-- Reading copy: local artifact links normalized. Original answer is preserved at ../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/answer.md -->

# Fashion Category — User Profile Analysis

## Executive Summary

**Primary recommendation: Focus on Female customers.** Female customers are the highest-value user profile for the Fashion category. They represent 50.9% of Fashion customers but generate **55.0% of total profit**, with an average profit per customer of **$3,374** — 18% higher than male customers ($2,865). This advantage is consistent across all customer segments, age groups, and geographies. The difference is statistically significant (Mann‑Whitney U test, p = 1.65×10⁻¹⁴).

---

## 1. Overall Fashion Category Performance

| Metric | Value |
|---|---|
| Total orders | 30,775 |
| Total customers | 795 |
| Total sales | $5,212,097 |
| Total profit | $2,483,955 |
| Avg profit per order | $80.71 |
| Avg profit per customer | $3,124 |

Fashion is the leading category on the platform (59% of all orders, 62% of all profit).

---

## 2. Gender — The Critical Differentiator

### Profit & Volume

| Gender | Customers | Orders | Total Profit | Profit per Customer | Orders per Customer |
|---|---|---|---|---|---|
| **Female** | 405 (50.9%) | 16,833 (54.7%) | **$1,366,499 (55.0%)** | **$3,374** | 41 |
| Male | 390 (49.1%) | 13,942 (45.3%) | $1,117,457 (45.0%) | $2,865 | 35 |

### Engagement Rates (per order)

| Engagement Metric | Female | Male | Ratio |
|---|---|---|---|
| Add-to-Cart rate | **0.84** | 0.45 | 1.86× |
| Like rate | **0.76** | 0.30 | 2.56× |
| Share rate | **0.72** | 0.20 | 3.57× |
| Browsing time per order | **21.2 min** | 13.1 min | 1.61× |

Female customers are dramatically more engaged with Fashion products. Higher engagement strongly correlates with higher profit (Pearson r = 0.73–0.77, all p < 10⁻⁸⁰).

### Top 20% Most Profitable Customers

- **69.2% are Female** (110 of 159 top customers)
- Female over-representation in the top quintile is highly significant

### Gender × Segment Interaction

| Gender | Segment | Customers | Profit per Customer | Orders per Customer |
|---|---|---|---|---|
| Female | Corporate | 126 | **$3,443** | 41 |
| Female | Consumer | 204 | **$3,347** | 41 |
| Female | Home Office | 75 | **$3,333** | 40 |
| Male | Consumer | 205 | $2,870 | 36 |
| Male | Home Office | 73 | $2,867 | 35 |
| Male | Corporate | 112 | $2,856 | 35 |

**Key insight:** Every female segment outperforms every male segment. Within the same gender, segment differences are small. Gender is the primary driver of customer value.

![Profit by gender and segment](<../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/work/fig1_gender_segment_profit.png>)

![Engagement rates by gender](<../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/work/fig2_engagement_by_gender.png>)

---

## 3. Product Preferences

Female customers order more of every Fashion product. The highest female-to-male order ratios are:

| Product | Female Orders | Male Orders | F/M Ratio | Profit per Order |
|---|---|---|---|---|
| Formal Shoes | 1,608 | 1,187 | **1.35×** | $113.9 |
| Titak watch | 1,578 | 1,217 | **1.30×** | $127.1 |
| Jeans | 1,553 | 1,241 | **1.25×** | $118.8 |
| Shirts | 1,549 | 1,245 | **1.24×** | $98.6 |
| Suits | 1,534 | 1,261 | **1.22×** | $19.2 |

The profit per order is nearly identical between genders for each product; the revenue difference comes from **higher order volume** from female customers.

![Product preference by gender](<../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/work/fig5_product_gender_preference.png>)

---

## 4. Other Demographic Dimensions

### Customer Segment
- **Consumer** (409 customers, $1,271K profit, $3,108/customer)
- **Corporate** (238 customers, $754K profit, $3,166/customer)
- **Home Office** (148 customers, $459K profit, $3,103/customer)

Segments are relatively balanced in profit per customer. Consumer has the largest absolute profit pool due to higher customer count.

### Age
- Majority of customers are 18–34 years old (567 of 795, 71%)
- Profit per customer is stable across age groups ($3,008–$3,520)
- Age distribution is similar between genders (mean female age ~31.5, male ~32.3)

### Education Level
- Bachelor's (223 customers), High School (160), Doctorate (146), Associate Degree (134), Master (132)
- Profit per customer ranges $3,037–$3,254 — no meaningful differentiation

### Marital Status
- Married: 428 customers, $3,120/customer
- Single: 367 customers, $3,130/customer

### Geography
- **Highest profit per customer:** Central Asia ($3,448), North Asia ($3,400), Caribbean ($3,179)
- **Top countries by profit per customer:** India ($3,563), China ($3,426), Brazil ($3,291)
- **Top by total profit:** United States ($479K), France ($191K), Australia ($181K)

![Age distribution](<../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/work/fig7_age_distribution.png>)

---

## 5. Profit Concentration

The top 20% of customers (quintile 1) generate **29.0%** of total profit, while the bottom 20% generate only **12.2%**.

| Quintile | Customers | Profit | % of Total |
|---|---|---|---|
| Q1 (top) | 159 | $719,906 | **29.0%** |
| Q2 | 159 | $562,128 | 22.6% |
| Q3 | 159 | $487,603 | 19.6% |
| Q4 | 159 | $410,728 | 16.5% |
| Q5 (bottom) | 159 | $303,590 | 12.2% |

![Profit concentration](<../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/work/fig3_profit_concentration.png>)

---

## 6. Seasonality & Discount Sensitivity

### Monthly Trends
- Monthly profit is relatively stable ($190K–$217K)
- Slight peaks in **August** ($217K) and **December** ($215K)
- Female customers consistently generate more profit than males every month

### Discount Sensitivity
- All orders receive small discounts (1%–5%)
- Higher discounts reduce profit per order for both genders
- Female customers are more numerous across all discount levels, maintaining their profit advantage

![Monthly seasonality](<../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/work/fig6_monthly_seasonality.png>)

---

## 7. Conclusion & Recommendations

### Target User Profile

**Primary focus: Female customers, across all segments (Consumer, Corporate, Home Office).**

Within the female audience, the following sub-profiles deliver the highest returns:

| Priority | Profile | Profit per Customer | Rationale |
|---|---|---|---|
| **1** | Female, Corporate | $3,443 | Highest profit per customer |
| **2** | Female, Consumer | $3,347 | Largest segment (204 customers, $683K total profit) |
| **3** | Female, Home Office | $3,333 | Strong per-customer value (75 customers) |

### Secondary Demographic Indicators
- **Age:** 18–34 (71% of customers, strong across all ages)
- **Geography:** Central Asia, North Asia, India, China, Brazil (high profit per customer)
- **Marital Status:** Both married and single are equally valuable

### Strategic Recommendations

1. **Target female shoppers** with personalized marketing, product recommendations, and loyalty programs. Female customers are 1.86× more likely to add to cart and browse 62% longer per order.

2. **Curate product mix** around high-profit items that appeal to women: **Formal Shoes, Titak watches, Jeans, and Shirts** — these have the highest female-to-male order ratios and above-average profit per order.

3. **Leverage engagement** — female customers' high like/share/add-to-cart rates suggest they are strong brand advocates. Encourage user-generated content and social sharing.

4. **Focus on the top 20%** of customers (disproportionately female) who generate 29% of total profit. Implement VIP programs for high-frequency buyers (41+ orders).

5. **Maintain low discount strategy** (1–3% optimal) since higher discounts erode margins without evidence of driving additional volume.

6. **Peak season preparation** — August and December show the highest demand; plan inventory and promotions accordingly.

### Limitations
- All Fashion orders use Standard Class shipping, so shipping preferences could not be analyzed
- The dataset contains 3 years of data (2022–2025); long-term trends may differ
- Customer geography is global; local market conditions may vary