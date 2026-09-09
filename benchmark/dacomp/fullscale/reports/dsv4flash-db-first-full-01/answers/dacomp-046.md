<!-- Reading copy: local artifact links normalized. Original answer is preserved at ../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/answer.md -->

# Marketing Characteristics Analysis by Age Segment & Differentiated Strategy Recommendations

## Executive Summary

This report analyzes **337 users** across four age segments (`<25`, `25-35`, `36-50`, `50+`) using data from user profiles, tagging, campaign interactions, and shopping cart operations. The study focuses on **churn risk, share rate, and feedback rating** to design age-differentiated product and campaign recommendations.

**Key findings:**
- Younger users (<25) have the highest churn risk (62.5%) and the lowest feedback rating (2.33/5), yet high conversion (0.40).
- Mature users (50+) have the lowest churn risk (47.2%), higher shares (26.0 avg), and the best usage rate (84.9%).
- No strong correlation between feedback rating and shares exists overall (r=0.03), suggesting distinct engagement drivers by age.
- Women consistently show higher churn risk across all age groups except 50+.

---

## 1. Churn Risk Analysis

### 1.1 Churn Risk by Age Group

| Age Group | Users | At-Risk Users | Churn Risk Rate |
|-----------|-------|---------------|-----------------|
| **<25**   | 56    | 35            | **62.5%**       |
| **25-35** | 69    | 37            | **53.6%**       |
| **36-50** | 106   | 52            | **49.1%**       |
| **50+**   | 106   | 50            | **47.2%**       |

![Churn risk, shares, and feedback rating by age group](<../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/work/fig1_age_group_churn_share_rating.png>)

**Observation:** Churn risk decreases monotonically with age. The **<25 group** is the most vulnerable (62.5%), while the **50+ group** is the most stable (47.2%).

### 1.2 Churn Risk by Gender

| Age Group | Female Risk | Male Risk |
|-----------|-------------|-----------|
| **<25**   | **66.7%**   | 58.6%     |
| **25-35** | **62.5%**   | 41.4%     |
| **36-50** | **57.4%**   | 40.4%     |
| **50+**   | 42.2%       | **50.8%** |

![Churn risk by gender and membership](<../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/work/fig5_churn_by_gender_membership.png>)

**Insight:** Females in the <25–36-50 range have **15–21 percentage points higher churn risk** than males of the same age. Only in the 50+ group are males riskier.

### 1.3 Churn Risk by Membership Level

| Age Group | Regular | Gold  | Platinum | Diamond |
|-----------|---------|-------|----------|---------|
| **<25**   | 70.8%   | 54.5% | 58.3%    | 55.6%   |
| **25-35** | 68.2%   | 61.1% | 38.5%    | 37.5%   |
| **36-50** | 57.7%   | 45.5% | 55.0%    | 40.7%   |
| **50+**   | 55.6%   | 40.9% | 46.2%    | 45.2%   |

**Insight:** Higher-tier memberships (Platinum/Diamond) generally correlate with lower churn risk, especially in the 25-35 group. However, **Regular members are consistently at highest risk** across all ages.

### 1.4 Churn Risk by Income Level

| Age Group | <50k      | 50k–100k | 100-200k | 200k+     |
|-----------|-----------|----------|----------|-----------|
| **<25**   | 70.6%     | 53.3%    | 56.3%    | **41.7%** |
| **25-35** | 70.6%     | 66.7%    | 46.2%    | 43.3%     |
| **36-50** | 38.5%     | 58.8%    | 54.2%    | **40.9%** |
| **50+**   | 46.2%     | 41.4%    | 59.1%    | 44.8%     |

**Insight:** Low-income users (<50k) in the <25 and 25-35 groups have the highest churn risk (70.6%). High-income users (200k+) consistently show lower churn risk.

---

## 2. Campaign Engagement Metrics

### 2.1 Share Rate & Feedback Rating by Age

| Age Group | Avg Shares | Share Rate* | Avg Feedback Rating | Avg Conversion | Avg Dwell |
|-----------|-----------|-------------|---------------------|---------------|-----------|
| **<25**   | 22.36     | 0.82%       | **2.33**            | 0.40          | 300s      |
| **25-35** | 23.13     | 0.99%       | 2.46                | 0.38          | 320s      |
| **36-50** | 25.09     | **1.08%**   | **2.55**            | 0.37          | 300s      |
| **50+**   | **26.02** | 0.97%       | 2.49                | 0.39          | 303s      |

*Share rate = total shares / total participants

![Conversion rate and dwell time](<../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/work/fig2_age_group_conv_dwell.png>)

**Observation:** The 36-50 group has the highest share rate (1.08%) and feedback rating (2.55). The <25 group has the lowest feedback rating (2.33) but the highest conversion rate (0.40), suggesting they engage differently — they act on campaigns without necessarily rating or sharing them highly.

### 2.2 Campaign Feedback Rating Heatmap

![Campaign feedback rating heatmap](<../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/work/fig3_campaign_rating_heatmap.png>)

**Top-rated campaigns by age group:**

| Age Group | #1 (Rating) | #2 (Rating) | #3 (Rating) |
|-----------|-------------|-------------|-------------|
| **<25**   | New-Year Red Packet (3.00) | Group-buy Coupon Grab (2.98) | Flash Sale (2.90) |
| **25-35** | **Holiday Treat (4.22)** | New-Year Red Packet (2.92) | Group-buy Coupon Grab (2.92) |
| **36-50** | New-Year Red Packet (3.17) | Flash Sale (2.81) | Spend-and-Save (2.80) |
| **50+**   | **Double-11 Mega Sale (3.07)** | Spend-and-Save (2.68) | Points Doubling (2.67) |

### 2.3 Correlation Analysis

| Metric Pair | Overall | <25  | 25-35 | 36-50 | 50+   |
|-------------|---------|------|-------|-------|-------|
| Rating ↔ Shares | 0.03 | 0.06 | 0.25 | 0.06 | -0.16 |
| Rating ↔ Conv | -0.01 | 0.07 | -0.12 | 0.04 | -0.03 |
| Shares ↔ Conv | -0.05 | 0.10 | -0.14 | -0.09 | -0.02 |

**Key Insight:** Correlations are weak across the board. The **25-35 group** shows a modest positive correlation between rating and shares (r=0.25), meaning they share what they like. The **50+ group** shows a slight negative correlation (r=-0.16), indicating they may share out of obligation rather than satisfaction.

### 2.4 Campaign Usage by Age

| Age Group | Used Campaigns | Blocked Events | Checkout Rate (Cart) |
|-----------|---------------|----------------|---------------------|
| **<25**   | 75.0%         | 0.0%           | 37.5%               |
| **25-35** | 75.4%         | 4.3%           | 34.8%               |
| **36-50** | 84.0%         | 3.8%           | 33.0%               |
| **50+**   | **84.9%**     | 1.9%           | **44.3%**           |

![Cart checkout rate](<../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/work/fig6_cart_checkout.png>)

**Observation:** The 50+ group has the highest campaign usage (84.9%) and checkout rate (44.3%), confirming they are the most reliable transaction group. The 25-35 group has the highest event blocking rate (4.3%).

---

## 3. Product & Preference Analysis

### 3.1 Browsing Preferences

![Browsing preferences](<../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/work/fig4_browsing_preferences.png>)

| Age Group | Top Browsing Category | 2nd Category | 3rd Category |
|-----------|----------------------|-------------|-------------|
| **<25**   | Home Appliances (12) | Beauty & Makeup (11) | Apparel (10) |
| **25-35** | Beauty & Makeup (18) | Home Appliances (15) | Apparel (14) |
| **36-50** | Apparel (26) | Digital Products (22) | Beauty & Makeup (20) |
| **50+**   | Beauty & Makeup (27) | Home Appliances (24) | Digital Products (17) |

### 3.2 Purchase Preferences

![Purchase preferences](<../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/work/fig4b_purchase_preferences.png>)

| Age Group | Top Purchase | 2nd | 3rd |
|-----------|-------------|-----|-----|
| **<25**   | Shoes & Bags (15) | Fresh Produce (14) | Digital Products (11) |
| **25-35** | Fresh Produce (20) | Digital Products (13) | Department Store (10) |
| **36-50** | Shoes & Bags (24) | Fresh Produce (20) | Department Store (19) |
| **50+**   | Digital Products (27) | Fresh Produce (20) | Shoes & Bags (19) |

### 3.3 Price Sensitivity & Spending Power

![Price sensitivity and spending power](<../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/work/fig7_price_spending.png>)

| Age Group | Price Sensitivity Mode | Spending Power Mode |
|-----------|----------------------|-------------------|
| **<25**   | **Low (42.9%)**      | Medium (35.7%)    |
| **25-35** | Medium (39.1%)       | Medium (40.6%)    |
| **36-50** | **High (36.8%)**     | Medium (37.7%)    |
| **50+**   | Medium (41.5%)       | **Strong (39.6%)** |

---

## 4. Differentiated Strategy Recommendations

### Segment 1: `<25` — "Young Explorers" (56 users, 62.5% churn risk)

**Profile:** Low income (<50k: 42.9%), Regular/Gold members, low price sensitivity, medium spending power, male-dominated (51.8%), high conversion rate but low engagement.

**Challenges:**
- Highest churn risk (62.5%), especially females (66.7%)
- Lowest feedback rating (2.33) and lowest share rate (0.82%)
- Low campaign usage (75%) but zero blocked events

**Product Strategy:**
- **Affordable bundled products** in Shoes & Bags and Fresh Produce categories
- **Trendy, low-price digital products** for entry-level tech adoption
- Loyalty-building tiered rewards (convert Regular → Gold)

**Campaign Strategy:**
- **Group-buy Coupon Grab** (rating 2.98, 100% used) — leverage social sharing
- **New-Year Red Packet** (rating 3.00) — gamified rewards
- **Flash Sale** (rating 2.90, 87.5% used) — urgency-driven, aligns with their high conversion orientation
- **Avoid** Brand-Day Special Offer (rating 1.70, 0.51% share rate)

### Segment 2: `25-35` — "Established Aspirers" (69 users, 53.6% churn risk)

**Profile:** High income (200k+: 43.5%), Gold/Regular members, medium price sensitivity, strong female presence (58.0%), **highest dwell time (320s)**.

**Challenges:**
- Female churn risk is 21pp higher than males (62.5% vs 41.4%)
- High event blocking (4.3%) — most sensitive to irrelevant campaigns
- Low usage rate (75.4%) despite high engagement

**Product Strategy:**
- **Fresh Produce & Beauty & Makeup** — female-centric daily essentials
- **Mid-to-high-end Home Appliances** for home-building life stage
- **Premium digital products** leveraging income strength

**Campaign Strategy:**
- **Holiday Treat** (rating 4.22) — best performing campaign across all segments; invest in lifestyle-themed events
- **Year-End Clearance** (rating 2.89, 100% used, 1.34% share rate) — high-value clearance events
- **Members Only** (rating 2.80, 100% used) — exclusive membership perks
- **Avoid** Brand-Day Special Offer (rating 1.48) and Points Doubling (rating 1.75)

### Segment 3: `36-50` — "Mature Buyers" (106 users, 49.1% churn risk)

**Profile:** Highest education diversity, high income (200k+: 20.8%), Gold/Diamond members, **highest share rate (1.08%)**, balanced gender.

**Challenges:**
- Female churn risk is 17pp higher than males (57.4% vs 40.4%)
- Moderate conversion rate (0.37) — considerate purchasers

**Product Strategy:**
- **Apparel (top browsing) + Shoes & Bags (top purchase)** — fashion-forward
- **Digital Products** — tech-savvy segment
- **Department Store style variety** — one-stop shopping

**Campaign Strategy:**
- **New-Year Red Packet** (rating 3.17, 88.9% used) — cultural embeddedness
- **Flash Sale** (rating 2.81, 81.8% used) — limited-time deals
- **Spend-and-Save Promotion** (rating 2.80, 91.7% used) — value-driven bundling
- **Members Only** (rating 2.49, 92.3% used) — loyalty program emphasis

### Segment 4: `50+` — "Loyal Valuers" (106 users, 47.2% churn risk)

**Profile:** Strongest spending power (39.6%), highest Diamond membership (29.2%), balanced income distribution, **highest usage rate (84.9%)**, **highest checkout rate (44.3%)**.

**Challenges:**
- Male churn (50.8%) exceeds female (42.2%) — reverse of other segments
- Slight negative correlation between rating and shares (r=-0.16)

**Product Strategy:**
- **Digital Products (top purchase, 27 users)** — mid-to-high-end electronics
- **Beauty & Makeup (top browsing, 27 users)** — anti-aging and wellness
- **Home Appliances** — home improvement and comfort

**Campaign Strategy:**
- **Double-11 Mega Sale** (rating 3.07, 86.7% used) — flagship event investment
- **Points Doubling** (rating 2.67, 84.6% used) — loyalty reinforcement
- **Spend-and-Save Promotion** (rating 2.68, 75% used, 1.28% share rate) — high share rate
- **Flash Sale** (100% used) — high reliability

---

## 5. Cross-Segment Recommendations

### 5.1 Targeted Retention by At-Risk Profiles

- **At-risk females (<25 to 36-50):** Personalized beauty & apparel campaigns with SMS marketing (78.1% of at-risk <25 subscribed to SMS)
- **At-risk low-income youth (<50k, <25, 25-35):** Budget-oriented bundles, coupon-based campaigns
- **At-risk Regular members (all ages):** Upgrade incentives, free trial of premium features

### 5.2 Campaign Optimization

| Campaign Type | Best Age Segment | Worst Age Segment |
|---------------|-----------------|-------------------|
| Holiday Treat | **25-35 (4.22)** | <25 (1.60) |
| Year-End Clearance | 25-35 (2.89) | 50+ (2.43) |
| Members Only | 36-50 (92.3% used) | 50+ (80.0% used) |
| Double-11 Mega Sale | **50+ (3.07)** | 25-35 (2.10) |
| New-Year Red Packet | **36-50 (3.17)** | 50+ (1.54) |

### 5.3 Cross-Selling Opportunities

- **25-35 → 36-50:** Fresh Produce purchasers → Shoes & Bags (rising demand)
- **36-50 → 50+:** Apparel browsers → Digital Products (life-stage transition)
- **<25 → 25-35:** Shoes & Bags purchasers → Beauty & Makeup (age progression)

---

## 6. Limitations

1. **Small sample size** (337 users) limits statistical power for subgroup analysis.
2. **No temporal data** was available to analyze churn over time or campaign sequence effects.
3. **Correlation analysis** shows weak linear relationships, suggesting non-linear or categorical drivers of campaign success.
4. **The <25 group** has the smallest sample (56 users), making segment-specific findings less robust.
5. **Network environment data** could not be cleanly joined to users due to missing key relationships.

---

## 7. Conclusion

The four age segments exhibit distinct churn risk profiles, campaign engagement patterns, and product preferences. The **50+ group** is the most valuable (lowest churn, highest usage, highest checkout rate) and should be prioritized for loyalty programs. The **<25 group** requires the most urgent churn intervention through gamified, social campaigns. The **25-35 group** responds best to lifestyle-themed premium events, while the **36-50 group** values cultural and limited-time offers. Differentiated strategies across these dimensions can significantly improve retention, share rates, and overall campaign ROI.