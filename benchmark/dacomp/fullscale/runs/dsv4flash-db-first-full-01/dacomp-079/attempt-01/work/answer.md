# In-Depth Analysis of the "Single-Feature-Use" User Segment

## Executive Summary

The "single-feature-use" segment comprises **1,184 users (14.8%** of 8,000 total) — users with >60 active days who clicked on fewer than 5 distinct features. This segment exhibits a profoundly different engagement pattern: **normal daily event counts but drastically reduced time per session, coupled with significantly lower NPS ratings.** The behavior is a "high frequency, shallow depth" pattern that correlates with lower satisfaction but not necessarily with short-term churn.

---

## 1. Segment Definition & Prevalence

| Metric | Single-Feature Heavy | Other Users |
|---|---|---|
| **Segment size** | 1,184 (14.8%) | 6,816 (85.2%) |
| **Avg. distinct features** | 2.56 | 8.66 |
| **Avg. active days** | 121.3 | 64.6 |
| **Avg. active months** | 3.57 | 1.86 |

The segment's 14.8% share matches the reported ~15% observation. Within the segment, the distribution of feature counts is fairly even: 1 feature (294 users), 2 (258), 3 (310), and 4 (322).

---

## 2. Which Features Do They Primarily Focus On?

### Top 12 Features by Single-Feature User Count

| Feature | Product Area | Single-Feature Users | Total Clicks |
|---|---|---|---|
| logout | authentication | 76 | 3,697 |
| contact_support | support | 72 | 3,970 |
| view_analytics | analytics | 71 | 3,619 |
| user_profile | user_management | 71 | 3,730 |
| mentions | collaboration | 70 | 3,201 |
| trend_analysis | analytics | 70 | 4,159 |
| subscription_manage | billing | 70 | 3,271 |
| billing_info | billing | 69 | 3,495 |
| export_api | integration | 68 | 3,573 |
| user_roles | admin | 68 | 3,403 |
| permissions | admin | 67 | 3,623 |
| widgets_config | dashboard | 67 | 3,390 |

### Product Area Allocation

The user base is spread relatively evenly across all 10 product areas:

![Product areas](fig5_product_areas.png)

### Feature Concentration

Single-feature users show **extremely high concentration** on their dominant feature:

| Distinct Features | Users | Avg. Dominant Feature Share |
|---|---|---|
| 1 | 294 | 100% |
| 2 | 258 | 67.3% |
| 3 | 310 | 51.9% |
| 4 | 322 | 41.0% |

![Feature concentration](fig6_concentration.png)

**Interpretation:** Even when they do use multiple features, over half their clicks go to a single feature. The primary features span all product areas — no single product area dominates — suggesting the behavior is a **user trait** rather than a feature-specific issue.

---

## 3. average_daily_minutes Anomaly

### Dramatic and Consistent Deficit

| Metric | Single-Feature Heavy | Other Users | Difference | p-value (MW) |
|---|---|---|---|---|
| **Avg. daily minutes** | 32.47 | 60.90 | −28.43 | **< 1e-300** |
| **Avg. daily events** | 29.19 | 29.90 | −0.71 | 0.057 (not significant) |
| **Minutes per event** | 1.38 | 2.51 | −1.13 | **< 1e-170** |

![Daily minutes distribution](fig1_daily_minutes.png)

Key findings:
- **The daily minutes deficit is NOT a side effect of fewer active days.** Even controlling for active-day bins (60–90, 90–120, 120–150, 150–200 days), single-feature users average ~32 min/day vs. ~82 min/day for multi-feature heavy users — all p-values < 1e-110.
- **Daily event count is nearly identical** (p = 0.057), meaning these users perform the same number of actions per day but spend **half the time** per action.
- This pattern is **consistent across all browsers, operating systems, and apps** — it is a behavioral trait, not a platform artifact.

### Threshold Effect at 5 Features

There is a sharp discontinuity at 5 distinct features:

| Distinct Features | Users | Avg. Daily Minutes | Avg. NPS |
|---|---|---|---|
| 1 | 294 | 32.34 | 5.53 |
| 2 | 258 | 32.36 | 5.64 |
| 3 | 310 | 32.40 | 5.58 |
| 4 | 322 | 32.74 | 5.59 |
| **5** | **114** | **85.06** | **7.81** |
| 6+ | 800+ | 82–85 | 7.84–8.18 |

This confirms the segment definition (≥5 features) marks a genuine behavioral boundary.

---

## 4. NPS Impact

### Substantially Lower Satisfaction

| Segment | Avg. NPS (Visitor) | Avg. NPS (Account) | NPS Range |
|---|---|---|---|
| Single-feature heavy | **5.58** | 6.92 | 4–7 |
| Other users | **7.28** | 7.04 | 5–10 |
| Multi-feature heavy (>60 days only) | **8.01** | 7.08 | 6–10 |

![NPS distribution](fig2_nps.png)

- The NPS gap of **1.70 points** (visitor-level) is highly significant (p < 1e-239).
- Among heavy users (>60 days): single-feature users rate **2.42 points lower** than multi-feature users (8.01 vs. 5.58).
- The NPS range for single-feature users is 4–7, while multi-feature heavy users range 6–10 — the two groups barely overlap.

**Interpretation:** The narrow feature usage pattern is strongly associated with dissatisfaction. Users who explore the product more broadly (even at the same activity level) rate it significantly higher.

---

## 5. Long-Term Retention Impact

### Complex Picture: High Return Rate but Shallow Engagement

**Retention comparison among heavy users (>60 active days):**

| Metric | Single-Feature Heavy | Multi-Feature Heavy | p-value |
|---|---|---|---|
| **Avg. active days** | 121.3 | 130.4 | < 1e-8 |
| **Avg. active months** | 3.57 | 3.89 | < 1e-9 |
| **Avg. tenure span (days)** | 135.8 | 144.8 | < 1e-8 |
| **Monthly coverage ratio** | 0.78 | 0.79 | n.s. |
| **Events per active day** | 29.19 | 29.96 | 0.057 |

![Retention metrics](fig3_retention.png)

**Key insights:**

1. **Single-feature users are retained longer than the average user** (121 vs. 65 active days, 3.57 vs. 1.86 months). Their high active-day count suggests they keep returning to the product.
2. **However, compared to similarly active multi-feature users, they show slightly lower retention** — 130 vs. 121 active days, 3.89 vs. 3.57 active months. The differences are statistically significant but small in magnitude.
3. **Monthly coverage ratio is nearly identical** (0.78 vs. 0.79), indicating that when they are active, they are active at similar monthly frequencies.
4. **Events per feature are ~5× higher** (1,823 vs. 364) — they pound the same few features repeatedly rather than exploring.

**Retention profile:** The segment shows a "sticky but narrow" retention pattern. They return frequently but never broaden their usage, and their daily time investment is minimal. This pattern is **not a churn risk in the short term** but represents a **missed opportunity for deeper engagement and higher satisfaction.**

---

## 6. Summary of Behavioral Characteristics

| Dimension | Finding |
|---|---|
| **Segment size** | 14.8% of all users (1,184/8,000) |
| **Primary features** | Evenly spread across all product areas; top features include logout, contact_support, view_analytics, user_profile |
| **Feature concentration** | Dominant feature gets 41–100% of clicks; users with 1 feature average 51 clicks, with 4 features average 201 clicks total |
| **Daily minutes** | **Anomalous**: 32.5 min/day vs. 60.9 (all users) or 82.3 (multi-feature heavy users) — p < 1e-300 |
| **Daily events** | **Normal**: 29.2 vs. 29.9 — not statistically different |
| **Minutes per event** | **Anomalous**: 1.38 vs. 2.51 — p < 1e-170 |
| **NPS** | **1.7 points lower** (5.58 vs. 7.28) — p < 1e-239 |
| **Long-term retention** | Higher active days than average users, but slightly lower than equally active multi-feature users; "sticky but shallow" |

### Behavioral Profile

The single-feature-use segment can be characterized as **"frequent but shallow" users**:
- They log in nearly as often as multi-feature heavy users (~121 vs. 130 days)
- They perform the same number of daily events (~29/day)
- But they spend **<40% of the time** per session (~32 min vs. ~82 min)
- They click intensively on 1–4 features only
- They rate the product significantly lower on NPS

This suggests these users may be **task-completers** who come in for specific, repetitive tasks (e.g., checking notifications, running one report, contacting support) rather than **explorers** who engage broadly with the product. The product is a utility for them, not a platform they enjoy spending time in.

---

## Limitations

1. **NPS vs. task claim**: The observed NPS gap (1.7 points) is larger than the 0.8 points referenced in the task description. This may reflect different aggregation methods or a different reference population.
2. **Causality**: The analysis is correlational. Low daily minutes and low NPS could be causes or consequences of single-feature use, or both could be driven by an unobserved confounder (e.g., user role, organizational mandate).
3. **Retention measurement**: All users have `last_event_on = 2025-10-14`, preventing churn analysis based on most-recent activity. Active months and tenure span are used as proxies.
4. **Feature metadata**: Some features have null `app_display_name` and `page_name`, limiting cross-app analysis.

---

## Conclusion

The single-feature-use segment represents a meaningful behavioral cluster (14.8% of users) characterized by **normal event frequency but dramatically reduced time investment per day** (~32 vs. ~82 minutes), **narrow feature focus** (1–4 features), and **substantially lower satisfaction** (NPS 5.58 vs. 8.01 among equally active users). Their retention is "sticky but shallow" — they keep returning but never deepen their engagement. Product interventions should focus on encouraging feature discovery and broadening usage patterns, which may improve both daily minutes and NPS scores.