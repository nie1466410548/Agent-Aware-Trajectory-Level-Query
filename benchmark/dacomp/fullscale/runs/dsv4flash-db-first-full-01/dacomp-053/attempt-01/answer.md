# Health-Value Inversion: An In-Depth Analysis of Project Metrics

## Executive Summary

This report investigates the "health-value inversion" phenomenon where some high-health-score projects deliver poor ROI while lower-health projects generate substantial business value. Using 500 projects from the `asana__project_analytics` table, we identify the root causes as a **mismatch between the health scoring system (completion-driven) and actual value delivery (scheduling-driven)**. Key dimensions—schedule forecast, time management, management priority, and complexity—interact to produce systematic inversion patterns.

---

## 1. Health Grade Performance Profiles

| Health Grade | Count | Avg ROI Efficiency | Avg Completion % | % Exceeding Duration >20% |
|:------------:|:-----:|:------------------:|:----------------:|:-------------------------:|
| A            | 45    | 0.9277             | 96.0%            | 33.3%                     |
| B            | 46    | 0.7561             | 72.4%            | 26.1%                     |
| C            | 68    | 0.3920             | 50.1%            | 45.6%                     |
| D            | 115   | 0.1844             | 40.5%            | 58.3%                     |
| F            | 226   | 0.0621             | 28.8%            | 96.0%                     |

**Observation:** While health grades generally correlate with ROI, the dispersion is wide. Grade D projects have a maximum ROI of **2.08** (higher than any grade A average), and grade B projects have ROI as low as **0.26**. This signals the inversion.

---

## 2. Root Cause: The Correlation Disconnect

![Health vs ROI Scatter](health_roi_scatter.png)

The scatter plot reveals the inversion: some projects with health scores >75 sit below the ROI=0.5 line, while projects with health scores <65 reach ROI above 0.5.

### What Drives Health vs. What Drives ROI?

![Correlation Matrix](correlation_heatmap.png)

| Metric | Correlation with Health Score | Correlation with ROI |
|--------|:----------------------------:|:--------------------:|
| Completion % | **0.79** | 0.59 |
| Efficiency Score | **0.73** | 0.55 |
| Time Management Score | 0.70 | **0.59** |
| Completion Rate/Day | 0.66 | **0.76** |
| Risk % | -0.76 | -0.61 |
| Collaboration Score | 0.02 | -0.08 |
| Elapsed/Planned Ratio | -0.52 | -0.44 |

**The core insight:** The health score is dominated by **completion percentage** (r=0.79) and **efficiency score** (r=0.73), while ROI is most strongly predicted by **completion rate per day** (r=0.76) and **time management score** (r=0.59). A project can be 100% complete but took 3x longer than planned—high health, low ROI. Conversely, a project at 30% completion that is far ahead of schedule has low health but high projected ROI.

---

## 3. Inversion Patterns: HHLV and LHHV Profiles

### Group Classification
- **HHLV** (High Health, Low Value): health_grade A/B, ROI < 0.5 (n=11)
- **HH_HV** (High Health, High Value): health_grade A/B, ROI ≥ 0.5 (n=80, baseline)
- **LHHV** (Low Health, High Value): health_grade D/F, ROI > 0.3 (n=5)
- **LH_LV** (Low Health, Low Value): health_grade D/F, ROI < 0.1 (n=206, baseline)

![Group Comparison](group_comparison.png)

### HHLV Profile: "Healthy but Underperforming"

| Metric | HHLV (n=11) | HH_HV (n=80) | Difference |
|--------|:-----------:|:------------:|:----------:|
| Avg Health Score | 77.4 | 84.9 | -7.5 |
| Avg ROI | 0.38 | 0.90 | **-0.52** |
| Completion % | 75.0% | 85.3% | -10.3% |
| Time Management | **66.4** | **77.9** | **-11.5 (p<0.001)** |
| Collaboration | **91.8** | 86.1 | **+5.7 (p<0.01)** |
| Complexity | 1.85 | 1.55 | Higher |
| Elapsed/Planned | **1.33** | 0.92 | **+0.41** |
| Behind Schedule | **90.9%** | 23.8% | **+67.1%** |
| Low Mgmt Priority | **100%** | 100% | Same |
| Minimal Risk | 54.5% | 95.0% | -40.5% |

**Characteristic combination:** These are **complex, behind-schedule projects with low management priority**. Despite high collaboration scores (91.8) and good efficiency (80.1), they have poor time management (66.4) and have significantly overrun their planned durations (elapsed/planned = 1.33). The health score is inflated by high completion % and collaboration, but the schedule overrun destroys ROI.

> **Example:** Project "Cloud Migration v1.5.0" (Grade A, health 86) has 100% completion and 95 collaboration score, but took 236 days vs 189 planned (25% overrun), yielding ROI of only 0.43.

### LHHV Profile: "Underestimated but High-Value"

| Metric | LHHV (n=5) | LH_LV (n=206) | Difference |
|--------|:----------:|:-------------:|:----------:|
| Avg Health Score | 63.0 | 45.5 | +17.5 |
| Avg ROI | **0.75** | **0.05** | **+0.70** |
| Completion % | 37.2% | 26.9% | +10.3% |
| Time Management | **80.6** | **52.6** | **+28.0 (p<0.001)** |
| Efficiency | 67.4 | 66.9 | +0.5 |
| Collaboration | 85.4 | 87.1 | Similar |
| Complexity | 1.78 | 1.54 | Higher |
| Elapsed/Planned | **0.51** | 4.97 | **-4.46** |
| Ahead of Schedule | **100%** | 3.9% | **+96.1%** |
| Medium Mgmt Priority | **100%** | 1.0% | **+99.0%** |
| Minimal Risk | **100%** | 6.8% | **+93.2%** |

**Characteristic combination:** These are **early-stage, ahead-of-schedule projects with medium management priority**. They have low completion % (37.2%) which drags down their health score, but excellent time management (80.6) and schedule adherence (elapsed/planned = 0.51). They are progressing at a rate that will deliver far ahead of plan, yielding high ROI. The health score system penalizes them for being "incomplete" despite outstanding schedule performance.

> **Example:** Project "Data Warehouse v2.4.3" (Grade D, health 62) is only 41.5% complete, but has used only 30 of 274 planned days (11% of allocated time). It is ahead of schedule with minimal risk, yielding an ROI of **2.08**—the highest in the entire dataset.

![Inversion Summary](inversion_summary.png)

---

## 4. Key Factor Dimensions Driving the Inversion

### Dimension 1: Schedule Forecast
- **Ahead-of-schedule projects**: Avg ROI = 0.67, but avg health = 69.5 (low completion % drags health down)
- **Behind-schedule projects**: Avg ROI = 0.14, avg health = 53.2
- Schedule performance is the single strongest differentiator between HHLV and LHHV groups

### Dimension 2: Time Management Score
- The most significant differentiator between HHLV and HH_HV (p<0.001)
- LHHV projects have time management scores (80.6) comparable to healthy A-grade projects (77.4)
- LH_LV projects have the lowest time management scores (52.6)

### Dimension 3: Management Priority (Reactive, Not Predictive)
- **Low priority** projects (n=108): Avg health 82.1, avg ROI 0.79 — they are healthy and high-value
- **High priority** projects (n=306): Avg health 49.3, avg ROI 0.09 — they are failing
- **Medium priority** projects (n=86): Avg health 62.8, avg ROI 0.30
- **Interpretation:** Management assigns "high priority" reactively to projects already in trouble. The label is a distress signal, not a driver of success.

### Dimension 4: Project Complexity
- HHLV projects have higher complexity (1.85) than their healthy peers (1.55)
- Complex projects with poor time management are disproportionately likely to become HHLV
- LHHV projects also have high complexity (1.78) but pair it with excellent time management

### Dimension 5: Team Size & Project Size
- Large teams (n=68): Higher collaboration but lower efficiency; collaborate more but may coordinate inefficiently
- Small teams (n=202): Slightly higher ROI (0.30 vs 0.27) but more behind-schedule projects
- Team size alone is not a strong predictor; its interaction with time management matters more

---

## 5. Recommendations for Optimizing the Evaluation System

### 5.1 Incorporate Schedule Performance into Health Scoring
The current health score is **completion-biased**. We recommend adding a **schedule performance factor**:

- **Schedule Adherence Index (SAI):** `planned_duration / elapsed_days` (capped at 2.0 for early projects)
- Projects ahead of schedule should receive a health score **bonus**, not a penalty
- A project at 30% completion that is 50% ahead of schedule is healthier than a project at 90% completion that is 30% behind

### 5.2 Weight Time Management More Heavily
Time management score is the strongest differentiator between HHLV and healthy projects (p<0.001). Increase its weight in the health formula from the current ~0.70 correlation to match or exceed completion percentage's weight.

### 5.3 Introduce a "Schedule Risk" Component
Projects with elapsed/planned ratio > 1.2 should automatically be flagged for health grade downgrade, regardless of completion percentage. Currently, 33% of A-grade projects exceed their planned duration by >20%.

### 5.4 Separate "Early Stage" and "Mature" Evaluation Tracks
Projects in early stages (completion < 40%) should be evaluated primarily on:
- Schedule adherence (elapsed vs planned)
- Completion rate per day (velocity)
- Risk level and time management score

Projects in mature stages (completion > 60%) should be evaluated on:
- Remaining work vs remaining time
- Quality metrics
- ROI efficiency

### 5.5 Re-examine Management Priority Assignment
The inverse correlation between "high priority" and performance suggests the label is reactive. Implement a **proactive priority system** that identifies high-potential projects (like LHHV) early and allocates resources to sustain their trajectory, rather than only flagging already-failing projects.

### 5.6 Targeted Interventions by Inversion Type
- **HHLV prevention:** For complex projects (complexity > 1.8) with large teams, implement tighter time management controls and schedule monitoring from the start. Assign dedicated time management resources.
- **LHHV support:** Early-stage projects showing strong schedule performance should receive increased management attention and resources to maintain their momentum, rather than being overlooked due to low completion %.

---

## 6. Limitations

- The classification thresholds (ROI < 0.5 for HHLV, > 0.3 for LHHV) are based on observed distributions and may not generalize.
- Causal inference is limited; the analysis identifies correlations and patterns, not causative mechanisms.
- Management priority appears to be a reactive label; its true relationship with project outcomes requires longitudinal data.
- Sample sizes for extreme groups (HHLV n=11, LHHV n=5) are small, though group differences are statistically significant.

---

## 7. Conclusion

The health-value inversion is a systemic issue caused by a **completion-centric health evaluation system** that undervalues schedule performance and time management. Projects that are "ahead of schedule but early in completion" (LHHV) are systematically undervalued, while projects that are "complete but overdue" (HHLV) are overvalued. By recalibrating the health score to incorporate schedule velocity, time management, and a lifecycle-aware evaluation framework, organizations can achieve a more accurate and actionable project assessment system.