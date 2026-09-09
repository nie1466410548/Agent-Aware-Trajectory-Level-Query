# Intercom Customer Engagement Metrics Dashboard
## Structural Analysis of Conversation & Product Usage Behavior Among Paying Customers

### Executive Summary

This report analyzes 6,703 conversations across 2,508 paying customers (Jan–Jun 2024) to uncover structural differences in engagement behavior by customer segmentation (new_contract, renewal, churn_watch, expansion) and account size (seat count, ARR bucket). Key findings reveal that **churn_watch customers** (which are exclusively high-value, large-account companies) exhibit the **lowest retention rates** (60% weekly, 45% monthly) and the **highest bot response dependency** (34.2%), while **expansion customers** (small accounts) show the highest retention (74% weekly, 69% monthly). A clear inverse relationship exists between account size and retention, suggesting that high-value accounts require differentiated engagement strategies.

---

### 1. Data Overview & Methodology

| Metric | Value |
|--------|-------|
| Total companies | 2,509 (2,508 distinct) |
| Total contacts | 2,707 |
| Total conversations | 6,703 |
| Conversational companies | 2,323 |
| Data period | Jan 8 – Jun 15, 2024 |
| Outliers excluded | 131 conversations (duration >P99 1030min) |

**Outlier Thresholds:** Response time P1=11min, P99=42min; Duration P1=91min, P99=1030min. Conversations outside these bounds were excluded, yielding 6,572 valid conversations across 2,308 companies.

**Timezone Handling:** All timestamps are stored as UTC (`YYYY-MM-DD HH:MM:SS` format). No timezone offsets were detected; assumed UTC throughout.

---

### 2. Segmentation & Account Size Structure

The customer segments map to non-overlapping account size tiers:

| Segment | Companies | ARR Range | Seat Range | Description |
|---------|-----------|-----------|------------|-------------|
| **expansion** | 627 | <30k (mostly) | under_60 – 60_129 | Low-value, small accounts |
| **new_contract** | 628 | 65k–200k | 130–419 | Mid-value, recently acquired |
| **renewal** | 627 | 30k–110k | 60–259 | Mid-value, established relationships |
| **churn_watch** | 627 | 110k–200k+ | 260–420+ | **High-value, at-risk accounts** |

**Critical structural finding:** All customers with ARR >200k and seats >420 belong exclusively to the churn_watch segment. This confound means that the "churn_watch" label correlates with the highest-value customers.

---

### 3. Core Metrics Dashboard

#### 3.1 Message Response Delay (minutes)

| Segment | Avg Delay | Min | Max |
|---------|-----------|-----|-----|
| **new_contract** | 25.88 | 11 | 42 |
| **renewal** | 26.09 | 11 | 42 |
| **expansion** | 26.18 | 11 | 42 |
| **churn_watch** | 25.90 | 11 | 42 |
| **Overall** | **26.01** | 11 | 42 |

Response delays are nearly uniform across segments (~26 min), suggesting consistent staffing. However, **bot first responses** are systematically faster (23.0 min) than human responses (27.5 min).

#### 3.2 First Response Bot Ratio

| Segment | Bot % | Human % |
|---------|-------|---------|
| **churn_watch** | **34.15%** | 65.85% |
| **new_contract** | 33.08% | 66.92% |
| **expansion** | 32.83% | 67.17% |
| **renewal** | 32.32% | 67.68% |
| **Overall** | **33.09%** | 66.91% |

Churn_watch segment has the highest bot dependency. Bot responses are 4.5 min faster on average but correlate with slightly lower retention (see section 4).

#### 3.3 Conversation-to-Feature-Usage Conversion Rate

Proxy definition: Customer has a contact with `last_activity_ts` within 72 hours after a conversation ended.

| Segment | Customers | Converted | Conversion Rate |
|---------|-----------|-----------|-----------------|
| **new_contract** | 628 | 19 | **3.03%** |
| **expansion** | 626 | 18 | **2.88%** |
| **renewal** | 627 | 18 | **2.87%** |
| **churn_watch** | 627 | 12 | **1.91%** |
| **Overall** | **2,508** | **67** | **2.67%** |

New_contract customers show the highest post-conversation feature engagement. Churn_watch customers have the lowest conversion, indicating conversations are less likely to drive subsequent product usage.

#### 3.4 Retention Rates

| Segment | Weekly Retention | Monthly Retention | Avg Active 7d Contacts | Avg Active 30d Contacts |
|---------|-----------------|-------------------|----------------------|-----------------------|
| **expansion** | **73.98%** | **69.48%** | 31.2 | 47.4 |
| **renewal** | **70.98%** | **64.31%** | 50.1 | 78.1 |
| **new_contract** | **65.97%** | **55.48%** | 87.5 | 145.4 |
| **churn_watch** | **59.98%** | **45.32%** | 148.1 | 264.8 |
| **Overall** | **67.73%** | **58.65%** | 79.2 | 133.9 |

**Retention declines sharply with account size.** The highest-value customers (churn_watch) have the lowest retention despite having the most active contacts. This is a critical risk signal.

---

### 4. Account Size Analysis

#### 4.1 Retention by ARR Bucket

| ARR Bucket | Weekly Retention | Monthly Retention | Gradient |
|------------|-----------------|-------------------|----------|
| <30k | 73.57% | 69.07% | Highest |
| 30k–65k | 71.71% | 65.24% | ↓ |
| 65k–110k | 67.70% | 58.52% | ↓ |
| 110k–200k | 63.25% | 50.85% | ↓ |
| **200k+** | **59.95%** | **45.28%** | **Lowest** |

**Monotonic inverse relationship:** As ARR increases, retention decreases. The 200k+ ARR bucket has 13.6pp lower weekly retention than the <30k bucket.

#### 4.2 Retention by Seat Bucket

| Seat Bucket | Weekly Retention | Monthly Retention |
|-------------|-----------------|-------------------|
| under_60 | 73.84% | 69.35% |
| 60–129 | 72.46% | 66.81% |
| 130–259 | 68.52% | 59.96% |
| 260–419 | 63.91% | 52.05% |
| **420+** | **59.90%** | **45.08%** |

Same pattern: larger accounts → lower retention.

---

### 5. Operational Touchpoints & Feature Paths

#### 5.1 Conversation Topic Distribution

| Topic | Total Conversations | Bot % |
|-------|-------------------|-------|
| onboarding | 671 | 33.4% |
| billing | 671 | 33.4% |
| feature_request | 671 | 33.2% |
| usage_insight | 670 | 33.3% |
| security | 670 | 33.4% |
| renewal | 670 | 33.3% |
| adoption | 670 | 33.3% |
| escalation | 670 | 33.4% |
| integration | 670 | 33.3% |
| success_plan | 670 | 33.3% |

Topics are evenly distributed, but for **churn_watch (high-value)** customers, the top topics are:
1. **Integration** (103 conversations) – highest volume
2. **Feature Request** (93) 
3. **Security** (90)
4. **Renewal** (87)
5. **Escalation** (87)

#### 5.2 SLA Performance

| SLA Status | % of Conversations | Avg Response (min) | Avg Duration (min) |
|------------|-------------------|-------------------|-------------------|
| Breached | **75.0%** | 29.1 | 502 |
| Warning | 22.2% | 17.4 | 468 |
| Met | 2.8% | 11.0 | 178 |

**75% of conversations breach SLA targets.** Churn_watch has slightly lower breach rate (74.2%) than new_contract (75.2%), but the difference is marginal.

#### 5.3 Bot vs Human Response Characteristics

| Responder | Response Time | Duration | SLA Breach % |
|-----------|--------------|----------|-------------|
| Bot | 23.0 min | 477 min | **66.7%** |
| Human | 27.5 min | 489 min | **79.1%** |

Bot responses are faster and have a 12.4pp lower SLA breach rate, but within the churn_watch segment, **companies with lower bot ratios have slightly higher retention** (60.3% for 0-25% bot vs 59.8% for 75-100% bot).

#### 5.4 Monthly Trends

| Month | Conversations | Bot % | Avg Response |
|-------|--------------|-------|-------------|
| Jan | 970 | 33.3% | 25.9 |
| Feb | 1,196 | 32.9% | 26.1 |
| Mar | 1,275 | 33.3% | 25.9 |
| Apr | 1,239 | 32.9% | 26.1 |
| May | 1,271 | 33.2% | 26.0 |
| Jun | 621 | 32.7% | 25.9 |

Conversation volume is stable (1,100–1,300/month) except for June (partial month). Bot ratio and response times are remarkably consistent.

---

### 6. Correlation Analysis

Company-level correlations between conversation metrics and retention:

| Metric | Weekly Retention (r) | Monthly Retention (r) |
|--------|---------------------|----------------------|
| Number of conversations | 0.005 | 0.004 |
| Avg response delay | 0.022 | 0.028 |
| Avg duration | 0.012 | 0.010 |
| Bot ratio | **-0.040** | **-0.030** |
| SLA breach ratio | 0.019 | 0.023 |
| Product tour ratio | **-0.040** | **-0.030** |
| Usage insight ratio | 0.022 | 0.019 |
| Adoption ratio | -0.005 | 0.015 |
| Escalation ratio | 0.011 | 0.004 |

Correlations are weak overall, but **bot ratio and product tour ratio show a consistent negative relationship** with retention (p≈0.056), suggesting that over-reliance on automated responses may correlate with lower customer engagement.

---

### 7. Key Operational Touchpoints & Recommendations

#### 7.1 High-Value Customer Retention Crisis

The data reveals a **retention inversion**: the most valuable customers (churn_watch, 200k+ ARR, 420+ seats) have the lowest retention rates. This is the single most critical finding.

**Recommended actions:**
- **Dedicated account management** for ARR 200k+ customers to reduce churn_watch trigger
- **Proactive integration health checks** – integration is the top conversation topic for churn_watch
- **Reduce bot dependency** for high-value escalations – bot ratio correlates negatively with retention

#### 7.2 Feature Paths for Post-Conversion Activity

The Conversation-to-Feature-Usage conversion rate is low overall (2.67%) but varies by segment:
- **new_contract (3.03%)** and **expansion (2.88%)** show higher conversion
- **churn_watch (1.91%)** shows the lowest conversion

**Recommended actions:**
- **Post-conversation feature nudges** for churn_watch customers after integration/usage_insight topics
- **Adoption topic conversations** should trigger immediate onboarding/follow-up resources
- **Feature request conversations** represent a critical touchpoint for retention – route to product teams

#### 7.3 Response Strategy Optimization

- **Bot responses are faster** (23 vs 27.5 min) and have lower SLA breach rates (66.7% vs 79.1%)
- But high bot ratio correlates with slightly lower retention
- **Recommendation:** Use bots for first-level triage on low-complexity topics (billing, usage_insight) but escalate quickly for high-value customers on integration/security/escalation topics

#### 7.4 SLA Performance

**75% of conversations breach SLA targets.** This is a systemic issue. The warning rate is 22.2% and only 2.8% meet SLA. 

**Recommended actions:**
- Review SLA target feasibility for the observed response patterns
- Implement automated escalation when SLA breach is imminent
- Prioritize SLA compliance for churn_watch segment where each conversation carries higher retention risk

---

### 8. Limitations

1. **Feature event proxy:** No explicit feature event table exists. `last_activity_ts` from contacts was used as a proxy, which only captures the latest activity timestamp, not all events. This likely underestimates the true conversion rate.
2. **Retention metric:** The `registration_retention_7d/30d` from company_metrics are pre-computed snapshot values, not cohort-based retention calculations. The contact-level `retained_7d/30d` flags are also snapshots (100% correlation with active flags).
3. **Timezone assumption:** All timestamps treated as UTC; no explicit timezone offsets were detected in the data.
4. **Segmentation confound:** Segment and account size are structurally correlated (all 200k+ ARR customers are churn_watch), making it impossible to fully separate the effects.
5. **Outlier exclusion:** Duration outliers (131 conversations >1030 min) were excluded. Response time had no outliers outside the P1-P99 range.
6. **Correlation, not causation:** The observed relationships between conversation metrics and retention are correlational.

---

### 9. Reproducibility

All metrics are computed from the supplied SQLite database using reproducible SQL queries. The pipeline is:
1. Parse `all_company_tags` for segment, seat_bucket, arr_bucket dimensions
2. Join conversations to companies via `all_contact_company_names`
3. Filter outliers (response time 11-42 min, duration 91-1030 min)
4. Aggregate by dimension and compute metrics
5. Compute retention from `company_metrics.registration_retention_*`
6. Compute conversion rate using contact `last_activity_ts` within 72h of conversation `last_close_at`

### Figures

![Comprehensive Dashboard](comprehensive_dashboard.png)
*Figure 1: Multi-panel dashboard showing all key metrics by segment*

![Retention by ARR](arr_analysis.png)
*Figure 2: Retention rates and active contacts by ARR bucket*

![Retention by Seat](seat_analysis.png)
*Figure 3: Retention rates and active contacts by seat bucket*

![Correlation Heatmap](correlation_heatmap.png)
*Figure 4: Correlation matrix between conversation metrics and retention*