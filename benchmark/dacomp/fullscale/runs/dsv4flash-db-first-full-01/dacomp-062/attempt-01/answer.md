# Cross-Functional Collaboration Effectiveness Analysis

## Executive Summary

This report investigates whether stakeholders with high `direct_network_connections` drive better project outcomes, focusing on `complexity_risk_score` and `success_probability`. The analysis reveals a **critical structural limitation**: the two tables (`jira__stakeholder_engagement_insights` and `jira__project_risk_assessment`) share **no common key** to link specific stakeholders to specific projects. Consequently, a direct causal test of the central question is **not possible** with the available data. What follows is the best-supported evidence from each domain independently, along with the implications.

---

## 1. Data Overview

| Table | Records | Key Columns |
|---|---|---|
| `jira__stakeholder_engagement_insights` | 4,524 stakeholders | `direct_network_connections`, `cross_functional_projects`, `total_engagement_score`, `influence_level`, `stakeholder_archetype` |
| `jira__project_risk_assessment` | 200 projects | `complexity_risk_score`, `success_probability`, `total_risk_score`, `trajectory_status` |

**Structural gap:** No `project_id` or `stakeholder_id` column exists in the opposite table, and no junction table is present. A search for "PRO" (project ID prefix) across all stakeholder text fields returned zero matches. Stakeholder–project involvements are recorded only as aggregate counts (`total_projects_involved`, `cross_functional_projects`).

---

## 2. Stakeholder Network Analysis

### 2.1 Distribution of Direct Network Connections

- **Range:** 2 – 65 connections
- **Median:** 13 | **IQR:** 7 – 21
- **Right-skewed distribution** (most stakeholders have fewer connections, a long tail of highly connected individuals)

![Distribution of stakeholder network connections](analysis_plots.png)

### 2.2 Strong Correlations with Engagement & Influence

| Metric | Pearson r | p-value |
|---|---|---|
| Engagement Breadth Score | **+0.90** | ~0 |
| Total Outbound Influence | **+0.81** | ~0 |
| Cross-Functional Projects | **+0.79** | ~0 |
| Engagement Impact Score | **+0.72** | ~0 |
| Total Engagement Score | **+0.68** | ~0 |
| Engagement Quality Score | **+0.67** | ~0 |
| Strategic Value Score | **+0.61** | ~0 |
| Total Projects Involved | **+0.40** | ~0 |
| Engagement Depth Score | **−0.001** | 0.93 (not significant) |
| Avg Outbound Influence Strength | **+0.008** | 0.59 (not significant) |

**Interpretation:** Stakeholders with more direct network connections are overwhelmingly the same individuals who:
- Participate in more cross-functional projects (r=0.79)
- Have broader engagement breadth (r=0.90)
- Exercise greater outbound influence (r=0.81)
- Achieve higher engagement quality and impact scores
- Are rated higher in strategic value

However, high-connection stakeholders do **not** have deeper engagement depth (r≈0) —their influence is wide, not deep.

### 2.3 Archetypes with Highest Connections

| Stakeholder Archetype | Avg Connections | Avg Cross-Functional Projects | Count |
|---|---|---|---|
| Cross-functional Coordinator | **45.1** | 8.8 | 169 |
| Product Manager | **37.5** | 8.0 | 254 |
| Technical Lead | **29.4** | 6.8 | 346 |
| Engineering Manager | **24.4** | 5.4 | 203 |
| Business Analyst | **20.0** | 5.4 | 341 |
| Junior Developer | **5.0** | 2.0 | 1,360 |

### 2.4 Engagement Risk Status by Connection Level

| Connection Group | Low Risk | Medium Risk | High Risk |
|---|---|---|---|
| High (>20 connections) | **809 (66%)** | 422 (34%) | **0 (0%)** |
| Mid (6–20) | 390 (16%) | 1,527 (62%) | 571 (23%) |
| Low (≤5) | 0 (0%) | 190 (24%) | **615 (76%)** |

**Critical finding:** No stakeholder with >20 direct network connections is classified as "High Risk" for engagement. Meanwhile, 76% of low-connection stakeholders are High Risk. This is a very strong signal that high network connectivity is associated with healthy engagement.

---

## 3. Project Outcome Analysis

### 3.1 Project Risk Profiles

![Project risk profiles and clusters](project_analysis.png)

### 3.2 Complexity Risk Score

- **Range:** 15 – 79 (out of 100)
- **Median:** 49 | **IQR:** 27 – 62
- **Not strongly correlated** with any other project metric except `total_risk_score` (r=0.99), indicating that complexity is a primary driver of the overall risk composite.

### 3.3 Success Probability

- **Range:** 0.49 – 0.95
- **Median:** 0.900 | **IQR:** 0.698 – 0.950
- **Right-skewed:** 52% of projects have success probability ≥ 0.90; 43% are capped at 0.95
- **43 distinct values** across 200 projects

### 3.4 Complexity Risk vs. Success Probability

| Correlation | r = **−0.005** | p = 0.95 (not significant) |
|---|---|---|

**The two metrics are essentially independent.** A project's complexity risk score does not predict its success probability. This is an important finding: high-complexity projects are not inherently less likely to succeed.

### 3.5 Risk Sub-Score Correlation Matrix

| | Complexity | Health | Schedule | Resource | Scope | Total Risk | Success Prob |
|---|---|---|---|---|---|---|---|
| Complexity | 1.000 | −0.056 | −0.067 | −0.010 | −0.083 | **0.986** | −0.005 |
| Success Prob | −0.005 | −0.022 | −0.018 | −0.078 | −0.079 | 0.006 | 1.000 |

All risk sub-scores are **mutually uncorrelated** (r near 0), except each correlates strongly with `total_risk_score`. The `total_risk_score` is **not** a simple sum of sub-scores (max difference = 381, correlation with sum = 0.19).

### 3.6 Project Clusters

Hierarchical clustering of the five risk sub-scores identified three distinct project profiles:

| Cluster | n | Complexity | Health | Schedule | Resource | Scope | Success Prob | Description |
|---|---|---|---|---|---|---|---|---|
| **1 (High Risk)** | 78 | 39.3 | 67.3 | 72.5 | 63.1 | 76.9 | 0.822 | High health/schedule/scope risk; mostly Medium/High Risk category |
| **2 (Complexity-Driven)** | 41 | 54.2 | 47.1 | 53.5 | 45.8 | 60.6 | 0.798 | Highest complexity; mostly Medium Risk |
| **3 (Low Risk)** | 81 | 47.0 | 30.5 | 34.3 | 26.3 | 40.8 | 0.843 | Low across all sub-scores; mostly Low Risk category |

Cluster 2 (high complexity) has the **lowest** average success probability (0.798), while Cluster 3 (lowest overall risk) has the highest (0.843). However, these differences are modest (range 0.045).

### 3.7 Project Trajectory & Risk

| Trajectory | n | Avg Complexity | Avg Success | Avg Total Risk |
|---|---|---|---|---|
| Stable | 99 | 49.1 | 0.807 | 49.7 |
| Critical | 4 | 48.5 | 0.810 | 48.8 |
| Improving | 40 | 41.7 | 0.845 | 42.4 |
| Declining | 57 | 41.6 | 0.846 | 42.9 |

Counterintuitively, "Declining" projects have **lower** complexity risk and **higher** success probability than "Stable" projects. The trajectory status appears driven by health/schedule/scope risk rather than complexity.

---

## 4. Can We Answer the Central Question?

**Question:** *Do stakeholders with high direct_network_connections lead to better project outcomes (lower complexity risk, higher success probability)?*

### What the Data Supports

1. **Stakeholder level:** High-connection stakeholders are **clearly more effective collaborators** — they have broader engagement, higher influence, more cross-functional involvement, and zero engagement risk.

2. **Project level:** Complexity risk and success probability are **independent dimensions**. Neither correlates meaningfully with any available project attribute.

### What the Data Cannot Support

There is **no join key** between the two tables. The evidence chain is broken:

- We cannot identify which projects a given stakeholder participates in.
- We cannot compute project-level metrics for "stakeholder network density."
- We cannot test whether projects with high-connection stakeholders have better outcomes.

**Total stakeholder-project involvements: 24,339** across 4,524 stakeholders and 200 projects (avg 5.4 projects per stakeholder, avg 122 stakeholders per project). Without a mapping table, any attribution would be speculation.

---

## 5. Conclusion & Recommendations

### Key Findings

1. **High-connection stakeholders are unquestionably more effective collaborators** (r=0.79 with cross-functional projects, r=0.68 with engagement, zero engagement risk). The network connection metric is a strong proxy for cross-functional coordination capability.

2. **Project complexity risk and success probability are independent** (r=−0.005). A project can be complex yet successful, or simple yet struggling.

3. **The data infrastructure does not support cross-table analysis.** The project–stakeholder relationship is recorded only as aggregate counts, preventing empirical validation of the central hypothesis.

### Recommendations

| Recommendation | Rationale |
|---|---|
| **Implement a stakeholder–project mapping table** (e.g., `project_stakeholders`) | Essential for linking individual contributors to project outcomes and enabling the analysis requested |
| **Leverage high-connection stakeholders** for cross-functional initiatives | These individuals (Cross-functional Coordinators, Product Managers, Technical Leads) show the strongest engagement breadth and influence, with no engagement risk |
| **Monitor complexity risk separately from success probability** | They are uncorrelated — a single metric cannot capture both dimensions |
| **Investigate why "Declining" trajectory projects have lower risk scores** | The inverse relationship between trajectory status and risk sub-scores warrants deeper investigation |

### Limitations

- No direct join between stakeholder and project tables
- `success_probability` is right-skewed with a ceiling effect at 0.95
- 43 unique success probability values across 200 projects indicate limited granularity
- Causal inference is not possible with observational data even with a join

---

*Figures: `analysis_plots.png` (stakeholder distributions and scatter plots), `project_analysis.png` (project risk profiles and clustering).*