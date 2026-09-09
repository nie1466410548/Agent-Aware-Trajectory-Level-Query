# False Prosperity Analysis: Multi-Dimensional Contradiction in Project Health Assessment

## Executive Summary

The Project Management Committee's observation is confirmed in the data. **19 of 200 projects (9.5%)** exhibit a "false prosperity" pattern: they report an excellent `overall_health_score` (>75, mean 83.4) while simultaneously carrying **Critical/High risk category**, high complexity risk (mean 40.4), low success probability (mean 0.34), and adverse lifecycle trajectories. A multi-dimensional re-assessment model shows these projects' **true health score averages only 56.3** — a **+27.2 point overstatement** — while the remaining 181 projects are, if anything, *understated* (−2.8 points). The phenomenon traces to three hidden root-cause clusters: **staffing/resource inefficiency, engagement-quality erosion in the stakeholder network, and workflow/lifecycle deviation**.

---

## 1) Distribution Characteristics of the Contradictory Population

### 1.1 Identification Criteria
A project was classified as "false prosperity" if it satisfied all of:
- `overall_health_score > 75` (surface health excellent)
- `risk_category IN ('Critical Risk','High Risk')` (deep risk contradicts surface)
- `complexity_risk_score > 30` (high complexity risk / issue-intelligence escalation)
- corroborated by `recommended_intervention = 'Immediate Executive Review Required'` (intervention urgency) and the data's own strategic flag `'Critical Priority - Investigate Contradictions'` / `'High Priority - Monitor Hidden Risks'`

### 1.2 Prevalence and Profile
| Metric | False Prosperity (n=19) | Other Projects (n=181) |
|---|---|---|
| Mean reported health score | **83.4** (range 75.2–92.0) | 64.0 |
| Mean total risk score | **174.6** | 142.9 |
| Mean complexity risk | **40.4** | 28.1 |
| Mean success probability | **0.34** | 0.47 |
| Mean value delivery % | **59.7%** | 70.3% |
| Mean resolution velocity change | **+0.9%** | +13.5% |
| Mean net issue growth (30d) | **+6.8 issues** | +4.3 |

Of the 19, **16** require "Immediate Executive Review" — all 16 are Critical Risk, **11 have adverse trajectories** (Declining/Deteriorating/At Risk/Volatile), **10 deliver <60% of value**, **16 have success probability <0.40**, **11 show negative resolution velocity**, and **10 have growing 30-day backlogs**. Risk drivers are split between **Resource Constraints (7), Technical Complexity (6), and Schedule Pressure (6)**. The most extreme contradictions are the five "flagship" projects: *Marketing Campaign Gamma* (health 92 / risk 165 / delivery 47.5%), *Performance Optimization Delta* (91.5 / 194 / 46%), *API Gateway Gamma* (91 / 236 / 44.5%), *Security Enhancement Beta* (90.5 / 228 / 43%) and *Data Analytics V2* (90 / 220 / 41.5%) — all Critical Risk with success probabilities between 0.22 and 0.38.

### 1.3 Radar and Scatter Evidence
The risk-profile radar and health-vs-risk scatter confirm the population is distinct: false-prosperity projects cluster in the upper-right quadrant of the health×risk plane (high health, high risk), which physically cannot occur in a well-calibrated scoring system.

**Figures:** `fig1_health_vs_risk_scatter.png` · `fig2_radar_comparison.png` · `fig6_health_gap.png`

---

## 2) Comprehensive Risk Re-Assessment Model (True Health Score)

### 2.1 Model Construction
Because a single reported score cannot reconcile health and risk, I built a **True Health Score (THS)** from four independent dimensions, each normalized to 0–100 (higher = healthier):

1. **Risk Exposure (weight 35%)** — inversion of the mean of the five sub-scores (`health_risk_score`, `schedule_risk_score`, `resource_risk_score`, `complexity_risk_score`, `scope_risk_score`);
2. **Delivery Effectiveness (25%)** — combination of `value_delivery_percentage` and `success_probability`;
3. **Lifecycle Health (20%)** — `resolution_velocity_change_percent` (velocity trend) and `net_issue_growth_30d` (backlog growth);
4. **Operational Health (20%)** — `team_stability_percentage` and `sprint_adoption_rate`.

`Health Gap = Reported Health − True Health`; positive gap = overrated.

### 2.2 Model Output
| Group | Reported Health | Reassessed True Health | Mean Gap |
|---|---|---|---|
| False Prosperity (n=19) | 83.4 | **56.3** | **+27.2** |
| Other (n=181) | 64.0 | 66.9 | −2.8 |

The most overrated projects (largest gap): **Data Analytics V2 (+58.2)**, **Security Enhancement Beta (+57.2)**, **API Gateway Gamma (+53.4)**, **Performance Optimization Delta (+41.6)**, **Marketing Campaign Gamma (+37.2)** — a re-ranking that moves the "best-looking" projects to among the riskiest. The gap correlates strongly with `total_risk_score` (r=0.56) and negatively with success probability (r=−0.50) and resolution velocity (r=−0.42), validating that the reported health score is systematically decoupled from actual delivery dynamics. Component breakdown shows false-prosperity projects underperform across all four dimensions (Fig 7), with **Risk Exposure** the single largest source of overstatement.

**Figures:** `fig5_true_health_model.png` · `fig7_component_breakdown.png`

---

## 3) Root-Cause Deep-Dive into "False Prosperity"

### 3.1 Workflow & Issue-Lifecycle Deviation
- **Lifecycle Deviation Ratio** (composite of trajectory risk, velocity trend, backlog growth): false-prosperity projects score **58.0 vs 45.7** for others (**p = 0.005**); it correlates with health gap (r=0.43) and total risk (r=0.36).
- **Resolution velocity**: +0.9% vs +13.5% (**p = 0.0006**) — near-zero/negative momentum despite "healthy" labels.
- **Value delivery**: 59.7% vs 70.3% (**p = 0.009**) and **delivered value points** 47.2 vs 71.7 (**p < 0.001**).

### 3.2 Staffing Efficiency & Resource Hidden Factors
- False-prosperity projects invest **366 hours vs 620 hours** (p < 0.0001) and are **~26% smaller in estimated value points** (76.0 vs 102.5, p < 0.0001) — i.e., **thinly staffed, under-invested programs** where resource constraints (the #1 risk driver, 7 of 19) are masked by superficial metrics.
- At the individual level, 36.8% of team members (1,608) score >80 performance; of these high performers, **567 are simultaneously High-Risk stakeholders** (35%), and 56.3% of all 4,524 stakeholders carry `engagement_risk_status = 'High Risk'`.
- Notably, raw performance dashboards show **no** significant difference between High- and Medium-risk stakeholders on performance score, resolution rate, consistency, or estimation accuracy — the "team performance > 80" signal is real on the surface, which is precisely what makes the phenomenon dangerous.

### 3.3 Communication & Collaboration Network Quality
The decisive hidden factor is **engagement quality, not engagement quantity**:
- High-Risk stakeholders have significantly **lower engagement breadth (33.8 vs 45.7), depth (32.8 vs 44.5), quality (34.8 vs 47.0), and impact (35.8 vs 48.3)** — all **p < 0.0001** — yet report **nearly identical** `total_engagement_score` (56.3 vs 55.7, n.s.), direct network connections, and influence measures. Their engagement is **wide in appearance but shallow in substance**.
- **Cross-functional collaboration mismatch**: High-Risk stakeholders show comparable `cross_functional_projects` counts (~2.98 vs 2.99, n.s.) but the mismatch between declared cross-functional breadth and actual engagement quality differs significantly between risk groups (p = 0.004), and no delivery benefit accrues to them — a **disconnect between the collaboration model and real delivery outcomes**, exactly as the committee suspected.

### 3.4 Root-Cause Chain (Synthesis)
1. Projects score high health because **inputs** (sprint adoption, stability, activity) look acceptable, while **outputs** (value delivery, velocity, backlog, success probability) are collapsing → score composition ignores delivery dynamics.
2. Thin staffing (low hours, low value points) concentrates work on few assignees with elevated **assignment-risk** (churn/inactivity/estimation pressure), and resource-constrained programs are classified "healthy" because health does not reflect resource load.
3. Stakeholder networks in these environments are **broad but low-quality** — breadth is generated (cross-functional flags) without depth/quality/impact, leaving high-risk engagement undetected by aggregate engagement scores.

**Figures:** `fig3_team_perf_by_engagement.png` · `fig4_stakeholder_patterns.png` · `fig8_hidden_factors.png`

---

## Recommendations
1. **Replace single health scores with the multi-dimensional THS**; escalate any project where `Health Gap > +15` regardless of reported health.
2. **Add delivery-momentum gates** (velocity change, backlog growth, value delivered) to "healthy" project reviews; a project with negative velocity should never be rated >75.
3. **For the 19 flagged projects**, initiate Immediate Executive Review with a focus on resource reallocation (7/19), technical de-complexing (6/19), and schedule realism (6/19).
4. **Monitor engagement quality metrics** (breadth/depth/quality/impact) rather than total engagement score; investigate stakeholders with high cross-functional flags but low engagement quality as risk carriers.
5. **Track assignment-risk and staffing density** (hours & value points per FTE) to detect under-resourced programs early.

---

## Limitations
- The three source tables have **no direct project↔person join key**; project-level and person-level contradictions were analyzed separately and combined at the portfolio level. Team/stakeholder conclusions describe population patterns rather than per-project attribution.
- Derived metrics (`lifecycle_deviation_ratio`, `assignment_risk_score`, `cross_func_mismatch`, THS) were constructed by the analyst with explicit, documented formulas; other weightings may shift magnitudes but not the qualitative conclusion.
- The dataset appears synthetic; figures reflect the recorded values only.
- No issue-level (individual ticket) table exists, so `high_delay_cost_issues`/`net_issue_growth_30d` were used as lifecycle proxies.
