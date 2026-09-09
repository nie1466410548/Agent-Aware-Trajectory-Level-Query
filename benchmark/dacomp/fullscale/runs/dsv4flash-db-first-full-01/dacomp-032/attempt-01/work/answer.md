# Service Staff Effectiveness for Priority-1 Customers

## Executive Summary

This report analyzes how effectively service staff serve customers with **Contact priority = 1** (the highest-priority segment) by examining their complaint records and ticket-handling performance. Of **105 priority-1 customers**, **41 (39%)** have had either a service ticket or complaint, and **27 (26%)** have had service tickets. The analysis reveals that while priority-1 customers receive slightly faster ticket resolution, their satisfaction scores are notably lower, and they require substantially more second-follow-up attention compared to other customers.

---

## 1. Coverage & Data Linkage

| Customer Group | Total Customers | With Tickets | With Complaints | With Either |
|---|---|---|---|---|
| **Priority 1** | 105 | 27 (25.7%) | 25 (23.8%) | 41 (39.0%) |
| Priority 2 | 100 | 26 (26.0%) | 25 (25.0%) | 45 (45.0%) |
| Priority 3 | 119 | 41 (34.5%) | 30 (25.2%) | 60 (50.4%) |
| Priority 4 | 97 | 31 (32.0%) | 33 (34.0%) | 52 (53.6%) |
| Priority 5 | 106 | 37 (34.9%) | 36 (34.0%) | 59 (55.7%) |

Priority-1 customers have the **lowest service engagement rate** (39%) among all priority groups, suggesting either fewer issues or potential under-reporting.

**Linkage path:** Complaints connect to customers via `complaints_table.Work Order ID` → `sales_follow_up_table.Customer ID`. Tickets connect via `service_ticket_table.Contract ID` → `contracts_table.Customer ID`. Of the 25 priority-1 complaint records, 22 (88%) share work orders with service tickets, showing strong overlap between complaints and tickets.

---

## 2. Ticket Handling Performance

### Key Metrics Comparison

| Metric | Priority 1 (n=27) | Other Priorities (n=135) | p-value |
|---|---|---|---|
| **Avg resolution duration** | 32.85 h | 35.93 h | 0.486 |
| **Median resolution duration** | 32.0 h | 36.0 h | — |
| **Avg satisfaction score** | 2.63 | 3.20 | 0.064 |
| **Second follow-up rate** | 70.4% | 49.6% | 0.078 |
| **Individual agents** | 27 (1:1 ratio) | 135 | — |

![Ticket metrics comparison](work/fig1_ticket_metrics.png)

### Key Findings for Tickets

1. **Resolution speed is comparable** — Priority-1 customers get slightly faster resolution (32.9 h vs 35.9 h), but this difference is not statistically significant (Mann-Whitney U, p=0.486).

2. **Satisfaction gap is marginal** — Priority-1 customers report lower satisfaction (2.63 vs 3.20, p=0.064). The satisfaction distribution reveals that **33% of priority-1 tickets received a score of 1** (worst), compared to only 18.5% for other customers. Conversely, only **11%** of priority-1 tickets received a score of 5, versus 25% for other customers.

3. **Much higher second-follow-up rate** — **70.4%** of priority-1 tickets required a second follow-up, compared to 49.6% for other customers (chi-square, p=0.078). This suggests first-contact resolution is particularly poor for this segment.

4. **Dedicated agent handling** — Each of the 27 priority-1 tickets was handled by a **different agent**, indicating a 1:1 dedicated service model.

### Ticket Performance by Urgency Level (Priority-1)

| Urgency Level | Tickets | Avg Resolution (h) | Avg Satisfaction | Second Follow-up Rate |
|---|---|---|---|---|
| **High** | 10 | 28.9 | 2.50 | 100% |
| **Medium** | 8 | 38.0 | 2.63 | 50% |
| **Low** | 9 | 32.7 | 2.78 | 56% |

![Priority-1 tickets by urgency](work/fig3_urgency.png)

All high-urgency priority-1 tickets required a second follow-up, and these tickets had the lowest average satisfaction (2.5). The Kruskal-Wallis test shows no significant difference in satisfaction across urgency levels (p=0.907), indicating uniformly low satisfaction regardless of urgency.

---

## 3. Complaint Handling Performance

### Key Metrics Comparison

| Metric | Priority 1 (n=25) | Other Priorities (n=124) | p-value |
|---|---|---|---|
| **Avg handling speed** | 38.20 h | 37.03 h | 0.768 |
| **Median handling speed** | 36.0 h | 38.5 h | — |
| **Avg satisfaction score** | 2.76 | 2.92 | 0.619 |
| **Escalation rate** | 4.0% | 7.3% | 0.876 |

![Complaint metrics comparison](work/fig2_complaint_metrics.png)

### Key Findings for Complaints

1. **Handling speed is similar** — Priority-1 complaints are handled in about the same time as others (38.2 h vs 37.0 h, p=0.768).

2. **Satisfaction comparable** — Complaint satisfaction is slightly lower for priority-1 (2.76 vs 2.92) but not statistically significant (p=0.619).

3. **Lower escalation** — Only 4% of priority-1 complaints were escalated, compared to 7.3% for others, suggesting staff may be more proactive in resolving priority-1 complaints internally.

### Complaint Type Analysis for Priority-1

| Complaint Type | Count | Avg Satisfaction | Avg Speed (h) | Escalated |
|---|---|---|---|---|
| 1 | 1 | 4.00 | 61.0 | 0 |
| 2 | 7 | 3.14 | 38.1 | 0 |
| 3 | 5 | 2.20 | 26.4 | 0 |
| 4 | 6 | 3.83 | 47.7 | 0 |
| 5 | 1 | 1.00 | 48.0 | 0 |
| 6 | 5 | 1.60 | 32.2 | 1 |

Complaint types 5 and 6 show the lowest satisfaction for priority-1 customers (1.0 and 1.6 respectively), while type 4 (satisfaction 3.83) and type 2 (3.14) are handled better.

---

## 4. Overlap Analysis: Work Orders with Both Ticket and Complaint

For the 18 work orders that have both a ticket and complaint for priority-1 customers:

| Metric | Value |
|---|---|
| **Avg ticket satisfaction** | 2.50 |
| **Avg complaint satisfaction** | 3.00 |
| **Correlation (ticket vs complaint sat)** | r ≈ 0.00 (Spearman p=0.898) |
| **Avg resolution time** | 34.9 h |
| **Avg complaint speed** | 40.6 h |

![Overlap scatter](work/fig5_overlap_scatter.png)

There is **no correlation** between ticket satisfaction and complaint satisfaction for overlapping work orders, indicating these measure different aspects of service quality. Tickets with an associated complaint have **lower satisfaction** (2.50) than tickets without (2.89) and longer resolution (34.9 h vs 28.8 h).

---

## 5. Satisfaction Distribution Comparison

![Satisfaction distributions](work/fig4_satisfaction_dist.png)

**Ticket satisfaction distribution:**
- Priority-1: 33% score 1, 15% score 2, 19% score 3, 22% score 4, 11% score 5
- Others: 19% score 1, 15% score 2, 20% score 3, 21% score 4, 25% score 5

The distribution is heavily skewed toward low satisfaction for priority-1 customers.

---

## 6. Conclusions on Service Staff Effectiveness

### Strengths
1. **Faster ticket resolution** — Priority-1 customers get resolved slightly faster (32.9 h vs 35.9 h), though not statistically significant.
2. **Dedicated attention** — Each priority-1 ticket is handled by a distinct agent (1:1 ratio), showing allocation of individual resources.
3. **Lower escalation rates** — Complaint escalation is lower (4% vs 7.3%), suggesting staff resolve issues internally for priority clients.
4. **Comparable complaint handling speed** — Priority-1 complaints are handled in about the same time as others.

### Areas for Improvement
1. **Low ticket satisfaction** — Priority-1 customers show consistently lower satisfaction scores (2.63 vs 3.20, p=0.064), with 33% of tickets receiving the lowest satisfaction rating.
2. **Excessive second follow-ups** — 70.4% of priority-1 tickets required a second follow-up, indicating poor first-contact resolution, especially for high-urgency tickets (100% second follow-up rate).
3. **Specific complaint type weaknesses** — Complaint types 5 and 6 are handled poorly for priority-1 customers (satisfaction 1.0 and 1.6), suggesting targeted training needs.
4. **No correlation between ticket and complaint satisfaction** — The absence of correlation suggests fragmented service quality measurement.

### Overall Assessment
Service staff demonstrate **dedicated resource allocation** for priority-1 customers but are **not yet achieving consistently high satisfaction** for this segment. The priority-1 segment receives faster resolution on average, yet the substantially higher second-follow-up rate and lower satisfaction scores indicate that **first-contact resolution quality is the primary gap**. Staff effectiveness in complaint handling is roughly on par with lower-priority customers, missing an opportunity to differentiate service for the highest-priority segment.

### Limitations
- The analysis is limited to the 39% of priority-1 customers who have service records; the remaining 61% may have different service needs.
- The complaint linkage via `sales_follow_up_table` captures 283 of 630 complaints (45%), and the remaining complaints could not be mapped to customers.
- All statistical comparisons use non-parametric tests (Mann-Whitney U, chi-square) appropriate for the ordinal satisfaction data and sample sizes.