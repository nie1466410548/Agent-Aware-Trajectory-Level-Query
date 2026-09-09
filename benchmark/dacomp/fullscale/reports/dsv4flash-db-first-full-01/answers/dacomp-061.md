<!-- Reading copy: local artifact links normalized. Original answer is preserved at ../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/answer.md -->

# Speed vs Stability: Are Fast-Delivery, High-Turnover Projects Truly Healthy?

## Executive Summary

This analysis investigates the phenomenon of projects with very short average close times (<15 days) but low team stability. These projects—specifically **Data Analytics Delta** (avg close 12.6 days) and **Mobile App Delta** (avg close 13.7 days)—exhibit a troubling pattern: **rapid delivery masks severe quality and sustainability issues**. The speed is achieved at the cost of dramatically higher rework, lower lifecycle quality, and unsustainable team pressure. These projects are **not healthy by any multi-dimensional measure**.

---

## 1. Data Sources & Methodology

### 1.1 Database Tables Used

| Table | Purpose |
|---|---|
| `jira__project_enhanced` | Project-level delivery metrics (avg_close_time_days, etc.) |
| `jira__issue_intelligence_analytics` | Issue-level quality metrics (~14M issues across 70 project names) |
| `jira__team_performance_dashboard` | Team member performance & stability indicators |

### 1.2 Identifying Fast Projects

From 200 project instances across 70 project names, **5 instances** have `avg_close_time_days < 15`:

| Project ID | Project Name | Avg Close (days) | Closed Issues | Lead |
|---|---|---|---|---|
| PRO93596447857 | Data Analytics Delta | 5.0 | 224 | William Martin |
| PRO80531791573 | Mobile App Delta | 11.0 | 103 | Lisa Williams |
| PRO70946189959 | Mobile App Delta | 12.0 | 68 | Robert Davis |
| PRO31658659931 | Data Analytics Delta | 12.0 | 116 | Emily Rodriguez |
| PRO25091014613 | Data Analytics Delta | 13.0 | 182 | Jennifer Garcia |

These aggregate to **Data Analytics Delta** (avg 12.6d) and **Mobile App Delta** (avg 13.7d) at the project-name level.

### 1.3 Redefining Team Stability

The task notes that the current `team_stability_percentage` metric shows 100% for all projects — a clearly broken indicator. I redefined it using actual signals from the `jira__team_performance_dashboard`:

- **Simple Stability (%)** = 100 × (1 − churn_risk_members / total_team_members)
- **Weighted Stability (%)** = Simple Stability × (avg_consistency / 100) — incorporates engagement consistency

---

## 2. Key Findings

### 2.1 Team Stability: Fast Projects Are the Least Stable

| Project | Avg Close | Team Size | Churn Risk | Simple Stability | Weighted Stability | Avg Consistency |
|---|---|---|---|---|---|---|
| **Data Analytics Delta** | 12.6d | 12 | **4 (33.3%)** | **66.7%** | **37.9%** | 56.8% |
| **Mobile App Delta** | 13.7d | 15 | **3 (20.0%)** | **80.0%** | **60.1%** | 75.1% |
| Mobile App Gamma | 19d | 8 | 1 (12.5%) | 87.5% | 50.2% | 57.4% |
| API Gateway V3 | 67d | 10 | 1 (10.0%) | 90.0% | 65.2% | 72.5% |
| User Management V3 | 51d | 4329 | 763 (17.6%) | 82.4% | 68.0% | 82.6% |

**Data Analytics Delta has the lowest stability of all projects** — one in three team members is at churn risk.

![Team Stability by Project](<../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/work/team_stability_by_project.png>)

![Team Stability Redefined Metrics](<../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/work/team_stability_detailed.png>)

### 2.2 Regression / Rework: The Most Striking Quality Deficit

The most significant finding is the **regression ratio** — a measure of how much issues cycle back through rework.

| Metric | Fast Projects | Other Projects | Statistical Significance |
|---|---|---|---|
| **Avg Regression Ratio** | **0.133** | **0.065** | **p < 0.001** |
| Issues with zero regression | **0.0%** | 36.3% | Chi²: p < 0.001 |
| Issues with high regression (0.2) | **33.4%** | 1.1% | |

**Every single issue** in the fast projects has a non-zero regression ratio, compared to only 63.7% in other projects. The proportion of issues with high regression (0.2) is **30× higher** in fast projects.

![Regression Ratio Distribution](<../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/work/regression_distribution.png>)

![Regression Ratio vs Speed](<../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/work/quality_metrics_vs_speed.png>)

This suggests a "close fast, rework later" pattern — issues are quickly marked as done but require significant rework, negating the velocity advantage.

### 2.3 Lifecycle Quality: Significantly Lower

| Metric | Fast Projects | Other Projects | p-value |
|---|---|---|---|
| **Avg Lifecycle Quality Score** | **6.46** | **7.71** | **p < 0.001** |
| Lifecycle Deviation Ratio | 18.37 | 15.02 | p = 0.15 (not significant) |

The fast projects have lifecycle quality scores about **1.25 points lower** (on a 3–10 scale), representing a ~16% deficit. The lifecycle quality distribution shows a distinct left-shift toward lower scores.

![Lifecycle Quality Distribution](<../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/work/lifecycle_quality_distribution.png>)

### 2.4 Other Quality Indicators: Not Significantly Different

| Indicator | Fast Projects | Other Projects | p-value |
|---|---|---|---|
| Bug Rate | 0.171 | 0.195 | 0.52 |
| Blocked Rate | 0.189 | 0.197 | 0.82 |
| Unusually Fast Rate | 0.242 | 0.225 | 0.68 |
| Statistical Outlier Rate | 0.067 | 0.061 | 0.89 |
| Avg Risk Score | 99.62 | 99.34 | 0.62 |
| Avg Intelligence | 49.91 | 49.96 | 0.47 |

Bug rates, blocked rates, and risk scores are statistically indistinguishable. The quality differences are concentrated in **regression/rework** and **lifecycle quality**.

### 2.5 Workload Concentration on At-Risk Members

A critical sustainability concern: churn-risk members carry disproportionate workloads.

| Project | At-Risk Members | At-Risk Workload Share | Team Size |
|---|---|---|---|
| **Data Analytics Delta** | 4 (33%) | **31.7%** | 12 |
| **Mobile App Delta** | 3 (20%) | **22.9%** | 15 |
| API Gateway V3 | 1 (10%) | 15.6% | 10 |
| Mobile App Gamma | 1 (12.5%) | 12.1% | 8 |
| User Management V3 | 763 (17.6%) | 18.1% | 4329 |

In Data Analytics Delta, the 4 at-risk members handle nearly a third of the workload. If these members churn, the project faces severe knowledge loss and delivery disruption.

---

## 3. Summary Visualization

![Speed vs Stability vs Quality](<../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/work/speed_stability_quality_summary.png>)

The three-panel chart above shows:
1. **Speed vs Stability**: Fast projects have the lowest team stability
2. **Speed vs Regression**: Clear negative correlation (r = -0.47, p < 0.001) — faster projects have more rework
3. **Speed vs Lifecycle Quality**: Clear positive correlation (r = 0.47, p < 0.001) — faster projects have lower quality

---

## 4. Conclusion: Are These Projects Healthy?

**No — these projects are not healthy.** The rapid delivery is a mirage achieved through:

1. **Sacrificing Process Quality**: Issues are closed quickly but with extremely high regression rates (100% of issues show rework). The "velocity" is not genuine productivity — it's rework disguised as progress.

2. **Unsustainable Team Dynamics**: Data Analytics Delta has a 33% churn risk rate — the highest of any project with team data. The at-risk members carry 31.7% of the workload, creating a vicious cycle where pressure to deliver fast drives people to churn risk, and losing them would cripple delivery.

3. **Lower Lifecycle Quality**: The average lifecycle quality score is 16% below the norm, indicating fundamental process issues.

4. **No Countervailing Benefits**: Bug rates, blocked rates, and risk scores are not better — they're the same as other projects. The speed is not accompanied by any measured quality advantage.

### 4.1 Recommendations

- **Redefine the team stability metric** to incorporate churn risk signals (at_churn_risk, consistency_percentage) rather than showing a flat 100%.
- **Investigate the "close fast, rework" pattern** in Data Analytics Delta and Mobile App Delta — the 100% regression rate suggests a systemic process issue (perhaps premature closure, insufficient testing, or pressure to close tickets).
- **Reduce workload on at-risk team members** before they churn. The 31.7% workload concentration on churn-risk individuals in Data Analytics Delta is a single point of failure.
- **Use a balanced scorecard** that weights velocity alongside quality (regression ratio, lifecycle quality) and stability metrics, rather than optimizing for speed alone.

### 4.2 Limitations

- Team performance data is only available for 5 of 70 project names, limiting the stability comparison.
- The regression_ratio is a coarse metric (0.0, 0.1, or 0.2 only), which may obscure finer-grained rework patterns.
- The project-level analysis aggregates by project_name, which combines multiple instances with potentially different characteristics under the same name.
- The "fast projects" here are limited to two project names; broader sampling would strengthen the findings.

---

## Appendix: Figures

| Figure | Description |
|---|---|
| [quality_metrics_vs_speed.png](<../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/work/quality_metrics_vs_speed.png>) | Scatter plots of quality metrics vs project speed |
| [regression_distribution.png](<../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/work/regression_distribution.png>) | Regression ratio distribution: fast vs other projects |
| [lifecycle_quality_distribution.png](<../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/work/lifecycle_quality_distribution.png>) | Lifecycle quality score distribution comparison |
| [team_stability_by_project.png](<../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/work/team_stability_by_project.png>) | Simple team stability by project |
| [team_stability_detailed.png](<../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/work/team_stability_detailed.png>) | Three levels of redefined stability metrics |
| [speed_stability_quality_summary.png](<../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/work/speed_stability_quality_summary.png>) | Summary: speed vs stability, regression, and quality |
| [fast_vs_other_quality.png](<../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/work/fast_vs_other_quality.png>) | Bar chart: quality indicators comparison |
| [fast_vs_other_detailed.png](<../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/work/fast_vs_other_detailed.png>) | Detailed bar chart: multiple metrics |
| [risk_profile_comparison.png](<../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/work/risk_profile_comparison.png>) | Risk and opportunity score comparison |