# Campaign Health Diagnostic Report

## 1. Executive Summary

This report analyzes 79 email campaigns (flows) from the Klaviyo dataset spanning January–August 2023. The framework evaluates campaign health through Open Rate (OR) and Click-to-Open Rate (CTOR) anomaly detection, template governance, send-time optimization, and copy-theme effectiveness. All campaigns fall into the <10k audience size bucket.

**Key finding: Copy theme (Variant A/B/C) is the single strongest performance driver, with Variant C outperforming Variant A by 38–71% in CTOR across all campaign types.**

---

## 2. Campaign Type Performance

| Campaign Type | Category | N | Mean OR | Mean CTOR | OR Std | CTOR Std |
|---|---|---|---|---|---|---|
| Onboarding | New Product | 12 | 0.3580 | 0.2299 | 0.0285 | 0.0342 |
| Cart Recovery | Promotional | 12 | 0.3755 | 0.2467 | 0.0249 | 0.0523 |
| Browse Abandonment | Promotional | 10 | 0.3928 | 0.2582 | 0.0277 | 0.0527 |
| Post-Purchase | Storytelling | 9 | 0.4101 | 0.2199 | 0.0309 | 0.0346 |
| Winback | Promotional | 9 | 0.4301 | 0.2500 | 0.0214 | 0.0347 |
| Seasonal | Promotional | 9 | 0.4634 | 0.2233 | 0.0263 | 0.0530 |
| VIP Loyalty | Storytelling | 9 | 0.4500 | 0.2668 | 0.0309 | 0.0528 |
| Product Discovery | New Product | 9 | 0.4866 | 0.2400 | 0.0263 | 0.0346 |

**Figure 1: Campaign type performance**  
![Campaign Type Performance](campaign_type_performance.png)

Product Discovery (New Product) leads in Open Rate (0.4866), while VIP Loyalty (Storytelling) leads in CTOR (0.2668). Onboarding (Welcome Series) trails in both metrics.

---

## 3. Anomaly Detection

### 3.1 Metric Anomaly Detection (Mean ± 2σ)

**Historical baseline** was computed from the last 6 months (2023-02-27 to 2023-08-27, N=61 campaigns) per campaign type × audience bucket.

**Result: No campaign exceeds the strict ±2σ threshold.** The maximum OR z-score is 1.966 (FLOW-1006, Cart Recovery Variant C) and the minimum is −1.697 (FLOW-1070, Product Discovery Variant A).

### 3.2 Near-Anomaly Campaigns (|z| > 1.5)

Six campaigns approach the anomaly boundary and warrant attention:

| Flow ID | Campaign Name | Type | Variant | OR | OR z | CTOR | CTOR z | Send Time |
|---|---|---|---|---|---|---|---|---|
| FLOW-1004 | Cart Recovery Variant A | Cart Recovery | A | 0.3402 | −1.68 | 0.1799 | −1.26 | Weekend PM |
| FLOW-1006 | Cart Recovery Variant C | Cart Recovery | C | 0.4180 | +1.97 | 0.3002 | +1.01 | Weekday PM |
| FLOW-1013 | Winback Variant A | Winback | A | 0.4000 | −1.53 | 0.2102 | −1.11 | Weekend AM |
| FLOW-1021 | Seasonal Variant C | Seasonal | C | 0.5079 | +1.69 | 0.2901 | +1.26 | Weekday PM |
| FLOW-1036 | Post-Purchase Variant C | Post-Purchase | C | 0.4541 | +1.56 | 0.2599 | +1.12 | Weekday AM |
| FLOW-1070 | Product Discovery Variant A | Product Discovery | A | 0.4420 | −1.70 | 0.2001 | −1.15 | Weekday PM |

**Root cause analysis:** All 6 near-anomaly campaigns are driven by **copy theme** (variant letter), not send time or template reuse frequency. The underperformers are all Variant A; the outperformers are all Variant C.

### 3.3 High-Frequency Update Anomaly

**No campaigns detected.** The minimum interval between consecutive `updated_at` timestamps is 61.25 hours (well above the 24-hour threshold). The mean interval is 96.1 hours (≈4 days). The correlation between `hours_since_prev` and OR (r=0.43) and CTOR (r=0.34) suggests that longer gaps between updates are modestly associated with better performance.

**Figure 2: Near-anomaly campaign scatter**  
![Near-Anomaly Scatter](near_anomaly_scatter.png)

---

## 4. Copy Theme Analysis (Variant A/B/C)

The variant letter (parsed from `flow_name`) serves as a proxy for copy theme, since `source_relation` is uniformly "klaviyo".

### Overall Performance by Variant

| Variant | N | Mean OR | Mean CTOR |
|---|---|---|---|
| **A** | 27 | **0.3863** | **0.1926** |
| B | 26 | 0.4171 | 0.2427 |
| **C** | 26 | **0.4468** | **0.2920** |

### Performance Gap: Variant C vs Variant A

| Campaign Type | OR Gain | OR % Improvement | CTOR Gain | CTOR % Improvement |
|---|---|---|---|---|
| Onboarding | +0.0629 | +19.3% | +0.0801 | +42.2% |
| Cart Recovery | +0.0554 | +15.9% | +0.1204 | +67.0% |
| Browse Abandonment | +0.0600 | +16.5% | +0.1199 | +57.0% |
| Post-Purchase | +0.0679 | +18.1% | +0.0800 | +44.4% |
| Winback | +0.0479 | +11.8% | +0.0801 | +38.2% |
| VIP Loyalty | +0.0680 | +16.4% | +0.1198 | +59.8% |
| Seasonal | +0.0579 | +13.3% | +0.1202 | +70.8% |
| Product Discovery | +0.0579 | +12.7% | +0.0799 | +39.9% |

**Variant C consistently outperforms Variant A across every campaign type**, with CTOR improvements ranging from 38% to 71%. This is the most actionable finding in the dataset.

---

## 5. Template Governance Analysis

- **No template exceeds 50% share** within its campaign type. The highest reuse is VAR-007 (Browse Abandonment Variant A) at 40%. All other templates are used at 30–33.3% within their type.
- **Overall template balance is good** — each of the 24 variation_ids is used 3–4 times across the 79 campaigns (3.8–5.1% of total).
- **No governance issue from over-reuse**, but the quality gap between templates is stark.

**Figure 3: Template reuse vs performance**  
![Template Reuse vs Performance](template_reuse_performance.png)

The scatter plot shows that the key differentiator is not how often a template is reused, but **which variant (A, B, or C) is used** — Variant C templates cluster in the top-right (high OR, high CTOR), while Variant A templates cluster in the bottom-left.

---

## 6. Send Time Analysis

### Performance by Time Slot

| Time Slot | N | Mean OR | Mean CTOR |
|---|---|---|---|
| Weekday Morning | 24 | 0.4205 | 0.2337 |
| Weekday Afternoon | 32 | 0.4141 | 0.2463 |
| Weekend Morning | 11 | 0.4170 | 0.2400 |
| Weekend Afternoon | 12 | 0.4135 | 0.2475 |

**Figure 4: Send time slot heatmap**  
![Send Time Slot](send_time_slot.png)

**Send time has minimal impact** on performance. The OR range across all 4 slots is only 0.4135–0.4205 (a 1.7% spread), and CTOR ranges 0.2337–0.2475 (a 5.9% spread). Differences are not statistically significant given the small sample sizes.

---

## 7. Improvement Directions

### 7.1 Theme Optimization (Highest Priority)

**Recommendation:** Replace all Variant A copy themes with Variant C-style messaging.

- **Current state:** Variant A campaigns average OR=0.3863, CTOR=0.1926
- **Target state:** Adopting Variant C patterns across all campaigns
- **Estimate:** 12–19% increase in Open Rate, 38–71% increase in CTOR
- **Action:** Audit the specific copy elements (subject lines, body content, CTAs) used in Variant C and replicate across Variant A/B templates

### 7.2 Template Governance

**Recommendation:** Maintain the current reuse balance (no template >50%), but systematically retire or redesign low-performing templates.

- **Retire candidates:** VAR-001 (Onboarding A, OR=0.3265, CTOR=0.1897), VAR-004 (Cart Recovery A, OR=0.3491, CTOR=0.1799), VAR-010 (Post-Purchase A, OR=0.3761, CTOR=0.1799)
- **Estimate:** Replacing these with Variant C equivalents could improve overall portfolio OR by 5–10% and CTOR by 15–25%

### 7.3 Sending Cadence

**Recommendation:** No immediate changes needed — the minimum gap between campaigns is 61.25 hours (>2.5 days). However, as volume grows, enforce a **minimum 24-hour gap** between deployments to prevent audience fatigue. The moderate positive correlation (r=0.34–0.43) between update interval and performance suggests that spacing out campaigns further could benefit engagement.

---

## 8. Proposed A/B Test Plan

### Test: Variant A → Variant C Copy Theme Replacement

**Hypothesis:** Replacing the copy theme of Variant A templates with Variant C-style messaging will increase both Open Rate and Click-to-Open Rate.

**Test Design:**
- **Control Group:** Continue sending current Variant A messages (e.g., VAR-001 for Onboarding, VAR-004 for Cart Recovery, VAR-010 for Post-Purchase)
- **Treatment Group:** Replace Variant A copy elements with Variant C patterns (subject lines, preheader text, body copy, CTA buttons, visual design)
- **Sample Size:** 3 campaign types × 2 variants each = 6 test campaigns, with at least 3 sends per variant
- **Duration:** 4 weeks (minimum 2 sends per campaign type)

**Metrics to Track:**
- Primary: Open Rate, Click-to-Open Rate
- Secondary: Conversion Rate, Revenue per Recipient, Unsubscribe Rate

**Projected Gains:**
| Metric | Control (Variant A) | Expected Treatment (Variant C) | Improvement |
|---|---|---|---|
| Open Rate | 0.386 | 0.424–0.447 | +10–16% |
| Click-to-Open Rate | 0.193 | 0.267–0.292 | +38–51% |

**Conservative estimate (accounting for novelty effect and audience differences):**
- **Open Rate: +5–10%** (projected range: 0.405–0.425)
- **Click-to-Open Rate: +15–25%** (projected range: 0.222–0.241)

---

## 9. Limitations

1. **Small dataset:** Only 79 campaigns; statistical power for anomaly detection at ±2σ is limited.
2. **No true anomalies detected:** The strict ±2σ threshold with small group sizes (n=3–4 per template) means only extreme deviations would be flagged.
3. **Uniform source_relation:** All campaigns are from "klaviyo", preventing copy-theme categorization by source.
4. **Person-level data sparse:** Only 4 persons in `klaviyo__person_campaign_flow`, limiting cross-validation of campaign metrics.
5. **Synthetic data:** The stark performance gap between variants (A vs C) may be amplified in this dataset; real-world differences are typically smaller.
6. **No EMAIL_TEMPLATE_ID column:** The `variation_id` is used as a proxy for template ID.
7. **Single audience bucket:** All campaigns are <10k recipients; the 10k–100k and >100k buckets are empty.

---

## 10. Conclusion

The campaign health framework reveals a healthy portfolio with no extreme anomalies. The primary area for improvement is **copy theme optimization** — Variant C dramatically outperforms Variant A across all eight campaign types. The proposed A/B test to replace Variant A copy with Variant C patterns is expected to yield 5–10% improvement in Open Rate and 15–25% improvement in Click-to-Open Rate. Template reuse and sending cadence are well-managed and require only minor governance adjustments.