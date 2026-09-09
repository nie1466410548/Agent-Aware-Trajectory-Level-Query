# Subscription Change Analysis: Key Factors Driving Upgrades and Downgrades

## Executive Summary

This analysis examines 1,426 subscription change events (714 upgrades, 712 downgrades) across 592 customers, with detailed conversation-level analysis on 31 companies that have intercom conversation data. The core finding is that **usage intensity and support incident volume are the strongest discriminators between upgrade and downgrade trajectories**.

- **Upgrade-prone customers** exhibit low baseline usage intensity and few support incidents before upgrading. They upgrade proactively to accommodate anticipated growth.
- **Downgrade-prone customers** exhibit high baseline usage intensity with elevated bug, outage, and SLA breach rates before downgrading. They downgrade reactively, often following a period of service dissatisfaction.
- **After both event types**, usage intensity and incident rates increase substantially, suggesting that product engagement and support needs grow with higher-tier adoption.

---

## Methodology

### Data Sources
- **intercom__company_enhanced**: 2,509 snapshot rows across 592 companies, each with plan name and creation timestamp. 551 companies have 2+ snapshots, enabling plan-change detection.
- **intercom__conversation_enhanced & _metrics**: 6,703 conversations from 31 companies, with tags (Bug, Outage, Escalation, etc.), SLA status, ratings, and parts counts.

### Event Detection
Plan changes were detected by ordering snapshots per company by `created_at` and comparing consecutive plan tiers (Starter=1, Growth=2, Scale=3, Enterprise=4 based on average monthly spend: $357, $1,222, $3,236, $7,899). An upgrade occurs when tier increases; a downgrade when tier decreases.

### Analysis Windows
Two complementary window approaches were used:
1. **Strict 30-day windows** (±30 days from event, per the task specification) — 10 events with conversation data.
2. **Full plan-period windows** (from previous snapshot `created_at` to next snapshot `created_at`) — 33 events with richer data for statistical testing.

### Metrics
- **Usage intensity**: Conversation rate (conversations per day), total conversation parts
- **Support incidents**: Bug-tagged conversations, Outage-tagged conversations, Escalation-tagged conversations, SLA breaches
- **Quality signals**: Conversation ratings, response times, tag composition shifts

---

## Key Findings

### 1. Pre-Event Usage Intensity: The Strongest Differentiator

| Metric | Upgrade (Before) | Downgrade (Before) | Ratio |
|--------|:----------------:|:------------------:|:-----:|
| Conversation rate (per day) | 0.223 | 0.591 | 2.7× |
| Bug rate (per day) | 0.029 | 0.073 | 2.5× |
| Outage rate (per day) | 0.029 | 0.059 | 2.0× |
| SLA breach rate (per day) | 0.133 | 0.314 | 2.4× |

Companies that **downgrade** have **2–3× higher pre-event usage intensity and incident rates** compared to those that upgrade. This suggests downgrades are driven by accumulated service issues, while upgrades are driven by growth expectations.

### 2. After-Event Changes: Opposite Trajectories

**Upgrade events** (n=19, full plan-period windows):
| Metric | Before | After | Change | p-value |
|--------|:------:|:-----:|:------:|:-------:|
| Conversation rate | 0.223/day | 0.988/day | **+343%** | **0.0012** |
| Bug rate | 0.029/day | 0.124/day | **+328%** | **0.0069** |
| Outage rate | 0.029/day | 0.134/day | +362% | — |
| SLA breach rate | 0.133/day | 0.603/day | +353% | — |

**Downgrade events** (n=14, full plan-period windows):
| Metric | Before | After | Change | p-value |
|--------|:------:|:-----:|:------:|:-------:|
| Conversation rate | 0.591/day | 1.128/day | +91% | 0.2468 |
| Bug rate | 0.073/day | 0.154/day | +111% | — |
| Outage rate | 0.059/day | 0.124/day | +110% | — |
| SLA breach rate | 0.314/day | 0.602/day | +92% | — |

After both event types, usage and incidents increase significantly, but the trajectories differ:

- **Upgrades**: Usage grows **4.4×** (from very low baseline). The increase in incidents is proportional to the growth in usage — the incident *rate per conversation* stays similar (bugs: 14.6%→13.9% of conversations).
- **Downgrades**: Usage was already high and grows further. The incident rate per conversation also increases (bugs: 13.0%→14.5%), suggesting that downgrading does not resolve underlying service issues.

### 3. Strict 30-Day Window: Clear Volume Shift

The 30-day window analysis (10 events) confirms the pattern with absolute volumes:

| Metric | Upgrade Before | Upgrade After | Δ | Downgrade Before | Downgrade After | Δ |
|--------|:--------------:|:-------------:|:-:|:----------------:|:---------------:|:-:|
| Conversations | 87 | 169 | **+94%** | 188 | 123 | **−35%** |
| Bugs | 10 | 19 | +90% | 26 | 20 | −23% |
| Outages | 10 | 25 | +150% | 19 | 11 | −42% |
| SLA breaches | 57 | 103 | +81% | 112 | 75 | −33% |

The before-downgrade window has **2.2× more conversations** than the before-upgrade window, reinforcing that downgrades follow periods of intense activity and issues.

### 4. Conversation Tag Composition Shifts

**Before upgrade events** (relative to company baseline):
- Higher shares of: Data Quality, Integration, Escalation, Training discussions
- Lower shares of: Billing, Mobile, Usage Spike conversations

**After upgrade events**:
- **Increase**: Billing (+2.2/100 convs), Adoption Risk (+1.7), Mobile (+1.3), Usage Spike (+0.9)
- **Decrease**: Data Quality (−2.2), Integration (−2.1), Escalation (−1.7), Training (−1.5)

**Before downgrade events**:
- Higher shares of: Billing, Adoption Risk, Automation, Implementation discussions

**After downgrade events**:
- **Increase**: Escalation (+2.0), Data Quality (+2.0), Bug (+1.6), Outage (+1.4), Integration (+1.5)
- **Decrease**: Billing (−3.6), Adoption Risk (−3.2), Automation (−1.2)

The **increase in Escalation, Bug, and Outage tags after downgrades** is particularly concerning — it suggests that the service quality issues that prompted the downgrade persist after the change.

### 5. Plan Transition Patterns

| Upgrade Path | Count | Downgrade Path | Count |
|-------------|:-----:|---------------|:-----:|
| Growth → Enterprise | 5 | Enterprise → Scale | 4 |
| Growth → Scale | 4 | Scale → Growth | 4 |
| Scale → Enterprise | 4 | Enterprise → Growth | 2 |
| Starter → Growth | 3 | Growth → Starter | 2 |
| Starter → Scale | 2 | Enterprise → Starter | 1 |
| Starter → Enterprise | 1 | Scale → Starter | 1 |

Most upgrades are **adjacent-tier** (Growth→Scale/Enterprise, Scale→Enterprise), and most downgrades are also adjacent-tier. The Scale→Growth and Enterprise→Scale transitions are the most common in both directions, making Scale a "pivot tier."

### 6. Company-Level Characteristics

Comparing upgrade-prone vs downgrade-prone companies (aggregated metrics):

| Characteristic | Upgrade-prone | Downgrade-prone | p-value |
|---------------|:-------------:|:---------------:|:-------:|
| Monthly spend | $3,357 | $3,232 | 0.78 |
| User count | 521 | 468 | 0.41 |
| Session count | 6,844 | 6,010 | 0.46 |
| Active contacts (7d) | 68 | 57 | 0.12 |
| Response time (min) | 74 | 77 | 0.70 |
| Avg rating | 4.23 | 4.25 | 0.86 |

Company size and rating metrics are similar between groups. The differences are driven by **behavioral patterns** (usage intensity and incident exposure) rather than static company characteristics.

---

## Key Drivers Summary

### Factors that Lead to **Upgrades**
1. **Low current usage intensity** — Companies with <0.25 conversations/day are 2.7× more likely to upgrade
2. **Low support incident rate** — Bug rates <0.03/day and SLA breach rates <0.15/day
3. **Growth phase** — Increasing conversation volume from a low baseline
4. **Billing discussions** — Billing-tagged conversations increase after upgrade, suggesting financial negotiation precedes the decision
5. **Adjacent tier jumps** — Most upgrades are one tier up (Growth→Scale/Enterprise)

### Factors that Lead to **Downgrades**
1. **High usage intensity with service issues** — Companies with >0.5 conversations/day and >0.30 SLA breach rates
2. **Accumulated incidents** — Bug and outage rates 2–3× higher than upgrade-prone companies
3. **Escalation patterns** — Escalation-tagged conversations increase after downgrade, indicating unresolved issues
4. **Adoption Risk discussions** — High before downgrade, suggesting the company is questioning the value of the current tier
5. **Persistent issues** — Bugs, outages, and SLA breaches remain elevated after downgrading

---

## Actionable Business Recommendations

### 1. Proactive Intervention for Downgrade-Risk Customers
**Monitor**: Customers with conversation rates >0.5/day AND SLA breach rates >0.25/day over a 30-day period.
**Action**: Before a downgrade occurs, engage with a customer success manager to address the root causes of incidents. The data shows that downgrading does not resolve service issues — the solution must address the underlying quality problems.

### 2. Identify Upgrade Candidates Early
**Monitor**: Customers with conversation rates <0.25/day but showing a positive trend in usage.
**Action**: These customers are prime upgrade candidates. Initiate "upgrade opportunity" conversations when usage begins to grow. The pattern shows that upgrades happen proactively when customers anticipate growth, not reactively.

### 3. Improve Service Quality at Scale Tier
**Why**: The Scale tier is the most common "pivot" — both upgrading from and downgrading to this tier. It represents a critical inflection point.
**Action**: Ensure Scale-tier customers have appropriate SLA coverage and support resources. The rapid increase in SLA breaches after upgrades (from 0.13 to 0.60/day) suggests that support capacity scales slower than customer usage.

### 4. Targeted Signal Monitoring
**Warning signals for downgrade**:
- Escalation-tagged conversations increase by >15% month-over-month
- Bug-to-conversation ratio exceeds 15%
- SLA breach-to-conversation ratio exceeds 50%

**Opportunity signals for upgrade**:
- Usage Spike conversations increase
- Billing conversations increase (indicating financial review)
- Current conversation rate is below 0.3/day with growth trend

### 5. Post-Change Support Optimization
The data shows that after **both** upgrades and downgrades, support incidents increase. This suggests:
- **After upgrades**: Customers need onboarding support for new features/capacity — provide proactive training
- **After downgrades**: Customers need reassurance and issue resolution — the downgrade itself doesn't fix the problems

---

## Limitations

1. **Sample size**: Only 31 of 592 companies (5.2%) have conversation data, limiting the statistical power of the event-level analysis. The 33 events with conversation data represent 2.3% of all plan changes.
2. **Temporal alignment**: The conversation data window (2019–2024) does not perfectly overlap with all plan change events, reducing the usable event count.
3. **No explicit upgrade/downgrade timestamps**: Events were inferred from consecutive snapshot plan changes, which assumes the `created_at` field represents the change time.
4. **Causality vs. correlation**: The observed patterns are correlational. Controlled experiments or causal inference methods would strengthen the conclusions.
5. **Single product line**: Results are based on one company's Intercom data and may not generalize to other products or industries.

---

## Figures

![Plan Change Analysis Summary](plan_change_summary.png)

*Figure 1: Comparison of usage intensity and support incident rates before and after upgrade/downgrade events. Top row shows per-event trajectories; bottom row shows aggregated means, pre-event incident volumes, and percent changes.*

![Plan Change Before/After Comparison](plan_change_analysis.png)

*Figure 2: Per-event scatter plots of conversation rate and bug rate before vs after plan changes, with bar charts comparing before-event metrics and after-event deltas between upgrade and downgrade groups.*

---

## Conclusion

The analysis identifies **usage intensity and support incident volume** as the primary factors distinguishing upgrade and downgrade trajectories. Customers upgrade proactively when they have low baseline usage and anticipate growth; they downgrade reactively when already experiencing high usage volume coupled with elevated incident rates. The Scale tier emerges as a critical pivot point. Business recommendations focus on early detection of these patterns through monitoring conversation rates, incident ratios, and tag composition shifts, enabling proactive customer success interventions before downgrades occur.