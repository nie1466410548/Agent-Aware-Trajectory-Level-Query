<!-- Reading copy: local artifact links normalized. Original answer is preserved at ../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/answer.md -->

# High-CTR / Low-CVR Ad Group Analysis — Google Ads

## 1. Objective & Method

Using the `google_ads__ad_group_report` table (10,000 daily rows, 4,324 unique ad groups, 1,000 campaigns, Jan 2021–Dec 2024), each ad group was aggregated over the full period to compute:

- **CTR** = clicks / impressions
- **CVR** = conversions / clicks
- **Intent Match Ratio (IMR)** = Actual CVR / Expected CVR, where Expected CVR is the **campaign-level CVR** (conversions/clicks aggregated per campaign). An IMR < 1 means the ad group converts worse than its own campaign average, i.e. a mismatch between the intent of the clicked traffic and the ad/landing page.

**Problematic ad groups** were flagged as: **CTR > 75th percentile AND CVR < 25th percentile**.

| Metric | Threshold |
|---|---|
| CTR 75th percentile | 3.5876% |
| CVR 25th percentile | 3.8462% |
| **Problematic ad groups** | **271 / 4,324 (6.3%)** |

![CTR vs CVR scatter](<../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/work/ctr_cvr_scatter.png>)

The problematic quadrant (red) is clearly visible: these ad groups attract above-average click volume per impression but fail to convert the resulting traffic.

## 2. Intent Match Ratio (IMR) — the core symptom

The defining characteristic of problematic ad groups is a severely depressed Intent Match Ratio:

| Group | Mean IMR | Median IMR | % with IMR < 0.5 | % with IMR < 0.7 |
|---|---|---|---|---|
| **Problematic (n=271)** | **0.476** | **0.458** | **57.9%** | **87.5%** |
| Non-problematic (n=4,053) | 1.115 | 1.038 | 10.4% | 33.5% |

![IMR histograms](<../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/work/imr_histogram.png>)

**Interpretation:** Problematic ad groups convert at less than **half** the rate expected from their own campaigns. The clicks they generate are high-volume but low-intent — users are engaged enough to click the ad (hence high CTR) but are not actually seeking what the ad/landing page delivers (hence near-zero conversion). 88% of problematic groups underperform their campaign benchmark by at least 30%.

IMR is uniformly low across all channels (Search 0.48, Brand 0.45, Display 0.49, Shopping 0.46, Performance 0.49), confirming this is a systemic traffic-quality problem rather than a single-campaign issue.

## 3. Traffic Quality Assessment

Problematic ad groups generate **more expensive and less valuable** traffic:

| Metric | Problematic (mean) | Non-problematic (mean) | Gap |
|---|---|---|---|
| Cost per click (CPC) | $2.75 | $2.75 | ~equal |
| **Cost per mille (CPM)** | **$112.63** | $76.71 | **+47%** |
| **Conversion value per click** | **$2.82** | **$6.27** | **−55%** |
| **ROAS** (conv value / spend) | **1.41** | **2.83** | **−50%** |
| **CPA** (spend / conversion) | **$122.65** | $57.06 | **+115%** |
| Clicks per ad group | 61.6 | 44.5 | +38% |

**Economic impact:** The 271 problematic groups consumed **$47,630 (8.8% of total spend)** but produced only **3.9% of conversions**, i.e. a spend-to-conversion ratio of **$112.9 vs $50.0 overall** — they are roughly **2.3× less efficient** at turning budget into conversions. CPC is normal, so the issue is not bid inflation but **poor conversion of the high-CPC click traffic**.

## 4. Common Characteristics of Problematic Ad Groups

**4.1 Keyword content (intent mismatch driver).** Analyzing the `google_ads__keyword_report` for the 246 problematic ad groups that have keyword data:

- **57% of keywords** (312 of 547) contain low-intent / informational words: `free`, `cheap`, `discount`, `buy`, `price`, `sale`, `review`, `warranty`, `support`, `delivery`.
- These low-intent keywords account for **54.8% of all impressions** in problematic groups.
- Top high-impression examples: `support buy free` (2,965 imps, CVR ~5%), `cloud free`, `warranty buy`, `top enterprise price online`, `buy business software solution`.
- Keyword **match-type mix is statistically identical** to non-problematic groups (Broad/BMM/Exact/Phrase all ~25%), so the problem is *what* the keywords say, not how they are matched.

**4.2 Search-term queries.** The same generic research-stage queries dominate problematic ad groups: `discount prices`, `analytics tools`, `buy online cheap`, `professional services`, `customer support`, `free delivery`, `training courses`. These are top-of-funnel, price/informational searches with high click propensity but low purchase intent.

**4.3 Channel & structure.** Problem rates are similar across channels (Shopping 6.8%, Search 6.6%, Video 6.2%, Multi-channel 6.1%, Display 5.6%). Smart-bidding subtypes (SMART, 6.9%) are slightly more affected than STANDARD (5.5%), and Display/Remarketing (7.6%) and Shopping (6.4%) campaign families lead in problem rate. Status mix (ENABLED/PAUSED/REMOVED) mirrors the overall account, i.e. many of these are still active.

**4.4 Account concentration.** Problem rates vary by account from 0% to **17.8%** (Professional Travel Solutions), 16.3% (Premium Sports Corp), 14.7% (Smart Real Estate Group) — indicating recurring keyword/landing-page patterns per advertiser.

## 5. Root-Cause Synthesis

The data supports a **click-intent vs. landing-page intent mismatch**:
1. High CTR shows the ads are **eye-catching/relevant enough to earn clicks** from high-volume generic searches.
2. Low IMR (0.48) shows those clicks **do not match the transactional content** on the landing page or the product offering.
3. High CPM + normal CPC + much lower conversion value per click indicate the account is paying a premium to attract casual/research-stage traffic that the landing experience cannot convert.

## 6. Targeted Optimization Recommendations

### A. Keyword strategy
1. **Audit and pause low-intent keywords** — isolate the ~312 keywords containing `free`, `cheap`, `discount`, `buy`, `review`, `support`, `warranty`, `delivery` that drive 54.8% of problematic impressions. Pause or move them to a separate "research" campaign with strict budgets.
2. **Add negative keywords** for price-research and informational intents (free, cheap, price, review, coupon, "how to", "vs", "download") at the ad-group level, and add the corresponding search terms observed in the search-term report.
3. **Shift budget to commercial-intent terms** — exact/phrase match on product + "buy", "for sale", "price", "quote", "sign up" terms; prioritize the non-problematic keyword set which already demonstrates IMR ≈ 1.
4. **Remove duplicate-word / junk keywords** observed in problematic groups (`management management`, `cloud cloud`, `discount discount`) which indicate poor keyword hygiene.

### B. Audience targeting
1. **Layer in-market and remarketing audiences** (exclude site visitors who already converted; target users showing purchase-stage behavior) to filter out the "discount / free / cheap" clickers.
2. **Use demographic and device exclusions** where the problematic accounts show concentration, and segment problematic campaigns by audience so generic searchers get a brand/reassurance experience rather than a conversion-focused one.
3. **Audience observation data** should be captured on the 17 accounts with >10% problem rates to re-target only engaged, high-intent visitors (e.g., cart-abandoners) instead of all clickers.

### C. Landing page experience
1. **Align landing pages with the clicked intent** — the high-CTR/low-CVR pattern implies landing pages promise more than they deliver; match ad copy promise to the landing page value proposition for the 271 flagged ad groups.
2. **Improve relevance & speed** (below-the-fold content, page load time, mobile experience) since clicks are already earned but the page fails to convert; measure via view-through conversions and bounce metrics.
3. **Strengthen conversion signals** — add clear CTA, trust signals, pricing transparency, and lead forms above the fold; use A/B testing on the highest-spend problematic ad groups (e.g., AD_96446107848 with $1,344 spend and 0.67 ROAS, AD_39762713814 with $1,177 and 0.21 ROAS).
4. **Use dedicated landing pages per ad-group theme** rather than a single generic page, so research-stage searchers (who click at high rates) land on content that either educates-and-captures or redirects them to the conversion path.

## 7. Expected Impact

Correcting keyword intent (step A) and landing-page alignment (step C) for the 271 ad groups would recover up to **$47,630 of spend (8.8% of total) currently converting at roughly half the expected rate**, potentially raising overall ROAS from ~2.8 toward the non-problematic benchmark while reducing wasted clicks from low-intent search terms.

## 8. Limitations

- **Expected CVR definition:** The IMR uses campaign-level CVR as the "expected" benchmark (a standard proxy). No true external/statistical baseline was available, so IMR values are relative, not absolute.
- **Aggregation window:** Percentiles and metrics were computed over the entire 2021–2024 period per ad group; seasonality and short-lived experiments could distort groups with few observations.
- **Search-term coverage:** Only 14 distinct search terms appear in the `search_term_report`, so the query-level analysis covers only a subset of actual queries.
- **URL/landing page data:** The `google_ads__url_report` had no overlapping rows for the flagged ad groups, so landing-page findings are inferred from campaign naming and performance patterns rather than direct URL analysis.
- **CVR denominator:** CVR = conversions/clicks; ad groups with very few clicks (e.g., 1–2 clicks) have noisy CVR estimates, though all 4,324 groups had ≥1 click and ≥9 impressions.
