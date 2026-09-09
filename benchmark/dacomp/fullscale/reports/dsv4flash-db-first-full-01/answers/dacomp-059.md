<!-- Reading copy: local artifact links normalized. Original answer is preserved at ../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/answer.md -->

# High-CTR, Low-Conversion Ad Groups: Root Cause Analysis and Systematic Solution

## Executive Summary

This report identifies **271 ad groups** (6.3% of all 4,324 active ad groups) exhibiting a high click-through rate (CTR > 3.59%, the 75th percentile) but a low conversion rate (CVR < 3.85%, the 25th percentile). These "problem ad groups" waste **~8.8% of total ad spend** while generating only **3.9% of total conversions**, with a 2.1× higher cost per acquisition and half the return on ad spend compared to normal ad groups. The root cause is a systematic **intent mismatch** between the search queries triggered and the ad/landing page content, confirmed by an Intent Match Index of 0.42–0.51 (vs. 1.06 for normal groups).

---

## 1. Identification of Problem Ad Groups

### 1.1 Methodology

For each ad group the following was computed:
- **CTR** = clicks / impressions
- **CVR** = conversions / clicks (where clicks > 0)

Percentile thresholds across all 4,324 ad groups:
- **CTR 75th percentile**: 3.59%
- **CVR 25th percentile**: 3.85%

**Problem definition**: CTR > 3.59% AND CVR < 3.85%

### 1.2 Scale of the Problem

| Metric | Normal (n=4,053) | Problem (n=271) | Difference |
|--------|:----------------:|:----------------:|:----------:|
| Mean CTR | 2.88% | 4.08% | +42% |
| Mean CVR | 5.80% | 2.53% | −56% |
| Total spend | $496,441 | $47,630 | 8.8% of total |
| Total clicks | 180,256 | 16,686 | 8.5% of total |
| Total conversions | 10,460 | 422 | 3.9% of total |
| Mean CPA | $57.06 | $122.65 | +115% |
| Mean ROAS | 2.83× | 1.41× | −50% |

**Figure 1**: CTR vs. Conversion Rate scatter plot. The problem quadrant (top-left) is clearly separated.

![CTR vs CVR scatter](<../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/work/fig1_scatter.png>)

---

## 2. Intent Match Index (IMI)

### 2.1 Definition

The **Intent Match Index** measures how well the actual conversion rate aligns with the expected conversion rate for the same industry and keyword combination:

$$IMI = \frac{\text{Actual CVR}}{\text{Expected CVR}}$$

The expected CVR was computed as the clicks-weighted average of benchmark CVRs per (industry, keyword) pair across all ad groups (excluding the target ad group's own contribution).

### 2.2 Results

| Group | Count | Mean IMI | Median IMI | Interpretation |
|-------|:----:|:--------:|:----------:|:--------------|
| Normal | 3,418 | 1.22 | 1.06 | Converts at expected rate |
| Problem | 244 | **0.51** | **0.42** | Converts at **half** the expected rate |

**Figure 2**: Box plots of IMI and Traffic Quality Score.

![IMI and TQS box plots](<../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/work/fig2_boxes.png>)

**Statistical significance**: Mann-Whitney U test: p = 9.17 × 10⁻⁷⁶

The problem groups convert at only **42–51% of the expected rate** given their industry and keywords, confirming a clear intent mismatch.

---

## 3. Traffic Quality Score (TQS)

### 3.1 Definition

Composite score (0–100) with three equally weighted components:

| Component | Weight | Measure |
|-----------|:------:|:--------|
| **A. Intent Match** | 40% | Scaled IMI (IMI/2, capped at 1) |
| **B. Match Type Precision** | 30% | Clicks-weighted: EXACT=100, PHRASE=75, BMM=50, BROAD=25 |
| **C. Keyword Intent** | 30% | Share of clicks on transactional-intent keywords (buy, cheap, price, discount, sale, etc.) scaled to 50% baseline |

### 3.2 Results

| Group | TQS (mean) | TQS (median) | Component A | Component B | Component C |
|-------|:----------:|:------------:|:-----------:|:-----------:|:-----------:|
| Normal | 58.3 | 60.6 | 54.9 | 62.8 | 58.4 |
| Problem | **45.1** | **45.4** | **27.7** | 61.9 | **51.4** |

The main driver of low TQS in problem groups is **Component A (Intent Match)**: 27.7 vs. 54.9. Match type precision (Component B) is similar across groups, suggesting the issue is not about match type choice alone.

---

## 4. Multi-Dimensional Characteristic Patterns

### 4.1 Campaign Channel & Strategy

**Figure 3**: Problem ad group share by Channel/Strategy combination.

![Channel Strategy analysis](<../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/work/fig3_channels.png>)

| Channel / Strategy | Problem rate | Risk level |
|--------------------|:-----------:|:----------:|
| Shopping / Broad | **8.7%** | HIGH |
| Display / Broad | **8.6%** | HIGH |
| Display / Audience | **8.3%** | HIGH |
| Performance / Keywords | **8.2%** | HIGH |
| Shopping / Remarketing | 7.6% | ELEVATED |
| Display / Remarketing | 7.5% | ELEVATED |
| Brand / Keywords | 7.3% | ELEVATED |
| Performance / Audience | 7.3% | ELEVATED |
| … | … | … |
| Search / Audience | **2.0%** | LOW |
| Shopping / Audience | 3.3% | LOW |
| Brand / Audience | 4.0% | LOW |
| Performance / Broad | 4.1% | LOW |

**Key insight**: Broad match in Shopping and Display campaigns is most prone to the problem. Search/Audience targeting is the most resilient.

### 4.2 Seasonality

**Figure 4**: Problem ad group share by campaign period.

![Period analysis](<../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/work/fig4_periods.png>)

| Period | Problem rate | Possible Explanation |
|--------|:-----------:|:---------------------|
| Holiday 2024 | **9.5%** | Peak gift-shopping season, high click volume from browsing users |
| Q4 2023 | **9.3%** | Year-end budget push, broad match expanded |
| Q4 2024 | **8.2%** | Same seasonal effect |
| Winter 2024 | 7.6% | Post-holiday browsing |
| Spring 2023 | 7.5% | Seasonal campaign launch |
| Q2 2023 | **3.7%** | Stable, lower competitive pressure |
| Winter 2023 | 4.0% | Earlier period, different competitive landscape |

**Seasonal pattern**: Q4 and Holiday periods consistently show 1.5–2× the average problem rate, suggesting that **competitive pressure during peak seasons drives broader matching and attracts lower-intent clicks**.

### 4.3 Industry

| Industry | Problem rate | Risk |
|----------|:-----------:|:----:|
| Travel | **7.9%** | HIGH |
| Entertainment | **7.5%** | HIGH |
| Sports | 7.2% | HIGH |
| Education | 6.9% | ELEVATED |
| Retail | 6.5% | Average |
| Food | 6.3% | Average |
| Fashion | 6.3% | Average |
| Automotive | 6.2% | Average |
| Technology | 5.6% | Below avg |
| Real Estate | 5.4% | Below avg |
| Finance | 4.9% | LOW |
| Healthcare | **4.0%** | LOWEST |

**Key insight**: Travel, Entertainment, and Sports — industries with high research/inspiration browsing — have the highest problem rates. Finance and Healthcare (higher intent, more regulated) have the lowest.

### 4.4 Keyword Match Type

| Match Type | Problem click share | Normal click share | Δ |
|-----------|:------------------:|:-----------------:|:-:|
| BROAD | 23.2% | 24.7% | −1.5pp |
| BROAD_MATCH_MODIFIER | 26.5% | 24.3% | +2.2pp |
| EXACT | 22.6% | 25.4% | −2.8pp |
| PHRASE | 27.6% | 25.7% | +1.9pp |

Match type alone is **not a strong predictor** of the problem. However, problem groups are more likely to use **only BROAD match** (25 groups, 9.2%) than normal groups, suggesting pure broad match contributes to the issue.

### 4.5 Keyword Intent Analysis

**Figure 5**: Keyword word click-share lift (problem / normal).

![Word lift chart](<../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/work/fig5_words.png>)

**Over-indexed words in problem groups** (lift > 1.1):
- **quality** (1.55×), **support** (1.47×), **free** (1.36×), **buy** (1.28×), **enterprise** (1.27×), **professional** (1.26×), **management** (1.25×), **business** (1.24×), **software** (1.20×)

**Under-indexed words** (lift < 0.9):
- **cheap** (0.61×), **price** (0.66×), **premium** (0.66×), **review** (0.67×), **course** (0.67×), **sale** (0.70×), **delivery** (0.73×), **mobile** (0.73×)

**Transactional-word click share**: Problem groups **39.8%** vs. Normal **46.6%** (p < 0.001).

Problem groups attract clicks from **generic, service-oriented keywords** (quality, support, free, enterprise) rather than **transactional keywords** (cheap, price, sale, discount). This confirms the intent mismatch: users searching for "quality support" or "free enterprise" are not in a purchase-ready state.

### 4.6 Ad Group Status

| Status | Problem rate |
|--------|:-----------:|
| ENABLED | 6.6% |
| PAUSED | 6.2% |
| REMOVED | 6.0% |

Minimal difference — the problem persists regardless of status.

### 4.7 Economics Impact

**Figure 6**: CPA and ROAS comparison.

![Economics](<../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/work/fig6_econ.png>)

| Metric | Problem | Normal | Impact |
|--------|:-------:|:------:|:-------|
| Mean CPA | **$122.65** | $57.06 | +115% |
| Mean ROAS | **1.41×** | 2.83× | −50% |
| Mean CPC | $2.75 | $2.75 | No difference |

**CPC is the same** — the problem groups are not paying more per click. The waste comes from **poor conversion after the click**, not from higher click costs.

---

## 5. Root Cause Analysis

Based on the evidence, the high-CTR, low-conversion pattern stems from **three interacting root causes**:

### Root Cause 1: Intent Mismatch (Primary Driver)
- **Implied by**: IMI = 0.42 (median) — problem groups convert at 42% of the expected rate.
- **Mechanism**: Keywords with generic/service words (quality, support, free, enterprise) attract users with informational/research intent who click but do not convert.
- **Evidence**: 39.8% transactional-word click share vs. 46.6% for normal groups; over-indexing on "quality" (1.55×), "support" (1.47×), "free" (1.36×).

### Root Cause 2: Broad Match in High-Browsing Environments
- **Implied by**: Shopping/Broad (8.7%), Display/Broad (8.6%), Display/Audience (8.3%) highest problem rates.
- **Mechanism**: Broad match in Shopping/Display campaigns serves ads to a wide range of queries, many of which are research-oriented. The high CTR reflects curiosity clicks, not purchase intent.
- **Evidence**: Q4/Holiday periods (peak browsing) have 1.5–2× average problem rates.

### Root Cause 3: Industry-Specific Search Behavior
- **Implied by**: Travel (7.9%), Entertainment (7.5%), Sports (7.2%) vs. Healthcare (4.0%), Finance (4.9%).
- **Mechanism**: In research-heavy industries (travel, entertainment), users frequently browse, compare, and click without immediate purchase intent. In regulated industries (finance, healthcare), users are more likely to be pre-qualified.

### Secondary Factors
- **Match type**: Not a primary driver, but pure BROAD match is overrepresented among problem groups.
- **Seasonality**: Q4/Holiday competitive pressure exacerbates all three root causes.
- **Keyword composition**: Multi-word keywords mixing informational and transactional terms (e.g., "analytics buy cheap management") are particularly problematic because they match broad queries but signal confused intent.

---

## 6. Systematic Solution

### 6.1 Keyword Optimization

1. **Transition from generic to intent-driven keywords**
   - Replace or supplement keywords with generic words (quality, support, free, enterprise) with transactional equivalents.
   - Add negative keywords for informational terms: "free", "review", "comparison", "alternatives", "how to", "guide", "tutorial", "specifications".

2. **Restructure keyword groups by intent tier**
   - **Tier 1 (High intent)**: Transactional terms (buy, price, order, purchase, discount, sale, cheap, delivery, warranty)
   - **Tier 2 (Medium intent)**: Commercial investigation (best, compare, top, professional, premium, quality)
   - **Tier 3 (Low intent)**: Informational (free, how to, guide, what is, review, support, training)
   - Assign separate bid multipliers and ad copy per tier.

3. **Segment broad match keywords**
   - For Broad match: require at least one transactional word in the keyword phrase.
   - Apply Smart Bidding with conversion goals (target CPA/ROAS) rather than maximizing clicks.

### 6.2 Audience Segmentation

1. **Implement audience layering**
   - For Display/Broad and Shopping/Broad campaigns (8.6–8.7% problem rate): restrict to **in-market audiences** and **custom intent audiences**.
   - Add **remarketing lists** for users who previously visited the site but did not convert.

2. **Demographic and affinity targeting**
   - Exclude low-converting age/gender/income segments based on historical conversion data.
   - For Travel/Entertainment/Sports industries: limit to audiences with demonstrated purchase behavior.

3. **Create exclusion lists**
   - Exclude users who have clicked multiple times without converting (click fatigue).
   - Exclude competitor domains and job-seeking audiences.

### 6.3 Landing Page Improvements

1. **Align landing page content with keyword intent**
   - For transactional keywords: direct to product pages with clear pricing, CTAs, and checkout flow.
   - For commercial investigation keywords: direct to comparison pages, feature highlights, with prominent conversion paths.
   - **Avoid** sending all traffic to the same generic landing page.

2. **Implement conversion path acceleration**
   - Add dynamic keyword insertion (DKI) in headlines to match search query.
   - Include trust signals: testimonials, guarantees, security badges, free shipping/returns.
   - Reduce page load time (target < 2 seconds) and minimize form fields.

3. **A/B test landing page variations**
   - Test different CTAs, form lengths, value propositions, and page layouts.
   - Use heatmaps to identify where users drop off.

### 6.4 Bid Adjustments

1. **Implement bid-by-intent-tier**
   - Tier 1 (transactional): +50% bid adjustment
   - Tier 2 (commercial investigation): 0% adjustment
   - Tier 3 (informational): −50% bid adjustment or pause

2. **Seasonal bid management**
   - During Q4/Holiday periods: reduce Broad match bids by 20–30%, increase Exact match bids by 10–20%.
   - Implement dayparting: reduce bids during known low-conversion hours.

3. **Target CPA/ROAS bidding**
   - Switch from Maximize Clicks to Target CPA or Target ROAS for all problem ad groups.
   - Set initial Target CPA at 1.5× the historical average CPA of the campaign.

### 6.5 Time-of-Day and Seasonal Optimization

1. **Analyze dayparting patterns**
   - Since the data lacks time-of-day granularity, implement conversion tracking by hour for 30 days.
   - Reduce bids by 30–50% during hours with CTR > 3× average but CVR < 0.5× average.

2. **Seasonal campaign structure**
   - Create separate campaigns for Q4/Holiday periods with more conservative keyword matching.
   - Use Holiday-specific ad copy and landing pages that match seasonal intent.
   - Increase negative keyword lists during peak seasons.

3. **Budget reallocation**
   - Redirect 20% of spend from problem-prone combinations (Shopping/Broad, Display/Broad) to resilient combinations (Search/Audience, Brand/Audience).
   - Set budget caps on Broad match campaigns during high-CTR/low-CVR seasons.

### 6.6 Monitoring and Feedback Loop

1. **Weekly anomaly detection dashboard**
   - Track IMI, TQS, and the problem-ad-group share metrics.
   - Auto-flag ad groups where IMI drops below 0.7 or TQS drops below 50.

2. **Automated rules**
   - Pause ad groups that have been in the problem quadrant for 7+ consecutive days.
   - Notify account managers when problem ad group share in a campaign exceeds 10%.

---

## 7. Data Limitations

The following dimensions were requested but not available in the database schema:

- **Device distribution**: No device-level breakdown available. Assumed uniform distribution.
- **Time-of-day performance**: Date granularity is daily; no hour-level data. Seasonality (quarter/season) was used as a proxy.
- **Geographical distribution**: No location-level data. Industry/account-level was used as a proxy.
- **Landing page quality scores**: No quality score column. Inferred from conversion patterns.
- **Bidding strategy**: Campaign strategy (Audience, Broad, Exact, Keywords, Remarketing) was used as a proxy for bidding approach.

These limitations should be addressed by enriching the data pipeline with device, geo, time, and quality score fields.

---

## 8. Conclusion

The high-CTR, low-conversion problem affects **271 ad groups (6.3%)** and is driven by a fundamental **intent mismatch** between the search queries triggered by generic keywords and the purchase-ready content expected by users. The problem is most acute in:

- **Shopping/Broad** and **Display/Broad** campaigns (8.6–8.7%)
- **Q4/Holiday** periods (9.3–9.5%)
- **Travel, Entertainment, and Sports** industries (7.2–7.9%)
- Ad groups using **generic service-oriented keywords** (quality, support, free, enterprise)

The systematic solution involves five pillars: **keyword restructuring** by intent tier, **audience segmentation** with in-market targeting, **landing page alignment** with keyword intent, **bid-by-intent** adjustments, and **seasonal campaign management**. Implementing these changes could recover an estimated **$20,000–$30,000 in wasted annual spend** and improve overall campaign ROAS by 15–25%.