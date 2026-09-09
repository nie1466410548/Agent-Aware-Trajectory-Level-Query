# Customer Health Score Model & Operational Strategy Report

## Executive Summary

A 0–100 health score was computed for **10,000 customer accounts** from the Salesforce customer 360 view using the specified weighted dimensions. The portfolio splits into **836 low-health accounts (<50, 8.4%)**, **7,764 medium-health accounts (50–79, 77.6%)**, and **1,400 high-health accounts (80+, 14.0%)**. The risk warning matrix identifies **Healthcare/Manufacturing Small Business** as the highest-risk segments (50% of each segment), driven almost entirely by engagement decay (67 days since last activity on average) rather than poor contact data. A 6-month revenue contribution model projects **$456B** total contribution, with **90.8% concentrated in the top revenue quintile (Tier 1)**. Differentiated success strategies are proposed per health band and company size.

---

## 1. Health Score Model Construction

The health score is a weighted composite of four normalized 0–100 sub-scores, computed entirely in SQL:

| Dimension | Weight | Sub-score construction |
|---|---|---|
| **Activity** | 40% | 50% recency: `max(0, 100 − days_since_last_activity × 1.667)` (60+ days → 0); 50% volume: `min(100, total_activities_30d × 1.667)` (60+ activities → 100) |
| **Contact Quality** | 30% | `contacts_with_email / total_contacts × 100` (portfolio range 75–100) |
| **Business Value** | 20% | 50% `log10(annual_revenue)` normalized on a $1M–$10B scale; 50% `log10(total_won_amount+1)` normalized on a $1B scale |
| **Account Scale** | 10% | 50% segment score (Small Business=25, Mid-Market=50, Large=75, Enterprise=100); 50% `log10(number_of_employees)` normalized over observed 13–49,805 range |

**Health Score = 0.4×Activity + 0.3×Contact + 0.2×Value + 0.1×Scale**

**Distribution** (mean 66.4, median 65.0, range 38.1–96.1):

![Health score distribution](health_score_distribution.png)

| Health Band | Accounts | Share |
|---|---|---|
| Low (<50) | 836 | 8.4% |
| Medium (50–79) | 7,764 | 77.6% |
| High (80+) | 1,400 | 14.0% |

The distribution is heavily influenced by scale and activity: Enterprise accounts average 88.0, while Small Business averages 52.0; Education (all Enterprise, zero days inactivity) scores 94.9–96.1, while Retail (no Enterprise/Small-Business mix) clusters mid-band (max 72.6).

---

## 2. Analysis 1 — Customer Risk Warning Matrix (Industry × Size, Health < 50)

![Risk warning matrix](risk_warning_matrix.png)

### Risk concentration (% of each industry × size segment with Health < 50)

| Segment | Small Business | Mid-Market | Large | Enterprise |
|---|---|---|---|---|
| **Healthcare** | **50.0%** (300) | 0% | 14.0% (84) | 0% |
| **Manufacturing** | **50.0%** (100) | **25.0%** (100) | 0% | 0% |
| **Technology** | 18.0% (108) | 0% | 7.7% (100) | 0% |
| **Financial Services** | 0% | 0% | 4.9% (44) | 0% |
| **Education / Retail** | – | – | – | 0% |

**Size dimension dominates risk:** Small Business = 29.9% of accounts at risk, Large = 7.6%, Mid-Market = 2.7%, Enterprise = 0%. 836 at-risk accounts hold **$6.9B in historical won revenue and $5.7B in open pipeline** that would be at risk of churn.

### Common characteristics of at-risk accounts (Health < 50) vs. healthy accounts

| Metric | Low (<50) | Medium (50–79) | High (80+) |
|---|---|---|---|
| Avg days since last activity | **67.0 days** | 15.7 | 9.4 |
| Avg activities in 30 days | **2.2** | 16.0 | 140.1 |
| Avg activity sub-score | **5.8** | 46.0 | 88.6 |
| Avg contact email ratio | 95.4% | 91.7% | 90.7% |
| Avg annual revenue | $91M | $453M | $4,953M |
| Avg total won amount | $9.3M | $48.1M | $366.5M |

**Key finding:** at-risk accounts are not data-quality problems — their contact quality is actually *excellent* (95.5%). The dominant failure mode is **engagement abandonment** (activity sub-score ~6/100): long inactivity combined with near-zero recent activities. Lower business value compounds this, but activity is the primary lever.

---

## 3. Analysis 2 — 6-Month Revenue Contribution Prediction Model

**Model formulation** (transparent, interpretable, uses only health score, historical won amount, and current pipeline):

```
Predicted 6-mo Contribution = Renewal Base + Pipeline Upside

Renewal Base   = (Health/100) × (Total Won Amount / Account Age in Months) × 6
Pipeline Upside= (Health/100) × (Win Rate %) × Current Pipeline Amount
```

- **Renewal Base** = the run-rate of historical won revenue over 6 months, discounted by health (at-risk accounts are assumed to retain less of their base).
- **Pipeline Upside** = the expected conversion of current open pipeline, discounted by health and the account's historical win rate.

**Results:**

| Statistic | Value |
|---|---|
| Total predicted 6-month contribution | **$456.1B** |
| Mean per account | $45.6M (median $4.5M) |
| Renewal-base share | $156.4B (34.3%) |
| Pipeline-upside share | $299.7B (65.7%) |
| Low-health (<50) total contribution | **$1.45B (0.3%)** |

**Revenue tiers** (quintiles of predicted contribution):

| Tier | Predicted 6-mo range | Accounts | Share of predicted revenue |
|---|---|---|---|
| **Tier 1 (Highest)** | > $25.97M | 2,000 | **90.8%** |
| Tier 2 | $8.26M – $25.97M | 1,998 | 6.2% |
| Tier 3 | $2.68M – $8.26M | 2,002 | 2.1% |
| Tier 4 | $0.87M – $2.68M | 2,000 | 0.7% |
| Tier 5 (Lowest) | < $0.87M | 2,000 | 0.1% |

![Revenue prediction](revenue_prediction.png)

Tier 1 accounts have a mean health of 85 and mean annual revenue of $4.3B — they are the Enterprise/large high-value accounts to defend and expand. Tiers 4–5 (mean health 53–61) contribute only 0.8% of projected revenue and are the natural targets for **cost-efficient recovery/self-service** programs. Low-health accounts are essentially revenue-neutral in the forecast, reinforcing that their value is defensive (preventing base erosion, not capturing upside).

---

## 4. Analysis 3 — Differentiated Customer Success Strategies

![Strategy matrix](strategy_matrix.png)

Portfolio distribution by health band × size: Low-health = 508 Small Business, 228 Large, 100 Mid-Market, 0 Enterprise; High-health = 1,300 Enterprise + 100 Large; Medium-health dominates Mid-Market (3,600) and Large (2,650).

### A. Low Health (<50) — Recovery & Retention Priority (836 accounts)
Primary goal: **stop revenue leakage and re-engage before churn**.

| Size | Strategy |
|---|---|
| **Small Business (508)** | Low-touch **win-back playbook**: reactivation email/phone campaigns on dormant contacts (95.5% have valid emails), offer on-demand webinars and quick-start health checks. Automate alerts at 30/45/60 days of inactivity. Low cost per account; success metric = re-engage within 14 days, raise activity score above threshold. |
| **Mid-Market (100)** | **Named CSM intervention**: executive business review within 30 days, identify feature-underuse or support issues causing disengagement, offer success-plan refresh and 90-day adoption goals. Discounted onboarding/renewal incentives contingent on usage. |
| **Large (228)** | **Executive sponsor escalation + risk review board**: CEO/CRO engagement, root-cause analysis of the engagement cliff (avg 67 days idle), dedicated health recovery plan, staged mitigation (renewal protection clauses, multi-year contract options, fast-track support SLAs). Highest retention ROI given their scale (Healthcare Large alone = 84 accounts, 14% of segment). |
| **Cross-cutting** | Because the failure driver is *engagement* (not contact data), the primary lever is **re-activation of activity**: re-engage stale contacts, refresh ownership, restart account-level cadences, and monitor weekly activity. |

### B. Medium Health (50–79) — Stabilize & Expand (7,764 accounts)
Primary goal: **move to high-health and grow share of wallet**.

| Size | Strategy |
|---|---|
| **Small Business (1,187)** | **Adoption coaching + upsell path**: usage health checks, email-based training, product-qualified-lead handoff to sales for starter expansions. |
| **Mid-Market (3,600)** | **CSM-led expansion motion**: quarterly business reviews, identify unused licenses/features, cross-sell adjacent modules, target +1 tier in predicted contribution (avg $17.1M → move to $26M+). |
| **Large (2,650)** | **Account-plan expansion**: dedicated success plans, joint roadmap sessions, renewal forecasting with pipeline-assist (their pipeline averages $43.8M), reference/case-study programs. |
| **Enterprise (300)** | **Strategic partnership**: customer advisory boards, co-innovation, executive alignment on ROI, expansion into new business units. |

### C. High Health (80+) — Defend & Monetize (1,400 accounts)
Primary goal: **protect the $414B Tier-1 revenue base and accelerate expansion**.

| Size | Strategy |
|---|---|
| **Enterprise (1,300)** | **White-glove CSM + executive sponsors**: proactive QBRs, early-warning on product roadmaps, loyalty rewards, advocacy/referral programs, multi-year/early renewal incentives. These accounts drive ~90% of predicted revenue — dedicate 50%+ of CS capacity to them. |
| **Large (100)** | **Rapid expansion**: fast-track upsell/cross-sell with sales-looped account teams, leverage their high win rates and $561M avg pipeline to convert pipeline to won at above-average probability. |
| **All** | **Champion development & NPS**: expand contact coverage beyond the email-dominant profile, build multi-threaded relationships, and use their high win rates (30.2%) as a scaling benchmark. |

---

## 5. Limitations

1. **Normalization choices** (activity caps at 60 days/60 activities; log scales for revenue/employees) are analyst-defined; percentile-based or company-benchmarked normalization could shift scores but not the relative ordering.
2. **Revenue model** is a transparent heuristic (run-rate + health-weighted pipeline conversion), not a fitted regression; it assumes historical won run-rate and win rates persist and that health linearly discounts retention/conversion. Future-data validation is recommended.
3. **Contact-quality score is compressed** (75–100) because every account has strong email coverage; it contributes little to separating risk — real contact depth (multi-threaded relationships) is not captured.
4. Account scale (10%) mechanically penalizes small businesses; the risk matrix therefore conflates "small" with "at-risk" — recovery programs for Small Business should be cost-calibrated accordingly.
5. Industry × size cells for Education (all Enterprise) and Retail (no Small Business/Enterprise) have zero risk by construction of the data distribution, not by proven immunity.

## 6. Files

- `health_score_distribution.png` — health score histogram with risk thresholds
- `risk_warning_matrix.png` — industry × size risk heatmap (Health < 50)
- `revenue_prediction.png` — health vs. predicted 6-month revenue and tier boxplots
- `strategy_matrix.png` — health band × size segment account distribution
- `customer_health_scores.csv` — full per-account scored dataset (10,000 rows)
