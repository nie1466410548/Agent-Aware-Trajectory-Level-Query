<!-- Reading copy: local artifact links normalized. Original answer is preserved at ../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/answer.md -->

# Engineering Department Conversion Rate Analysis

## Executive Summary

The Engineering department's application-to-interview conversion rate declined from **29.6% in Q3 2024 to 25.1% in Q4 2024**, a drop of 4.5 percentage points. Meanwhile, Marketing maintained a stable **~53% conversion rate** over the same period. The decline is driven by a combination of **severe role-specific drops**, **systematically low-performing hiring managers**, and a **month-over-month time trend** that affects all roles.

---

## 1. Role-Level Conversion Declines

| Role | Q3 2024 (%) | Q4 2024 (%) | Change (pp) |
|------|:-----------:|:-----------:|:-----------:|
| **Machine Learning** | 34.63 | 26.84 | **−7.79** |
| **DevOps** | 32.92 | 26.05 | **−6.87** |
| **Data Engineer** | 32.93 | 26.38 | **−6.54** |
| Frontend | 25.28 | 21.12 | −4.15 |
| Full Stack | 31.94 | 27.82 | −4.13 |
| Mobile | 25.79 | 21.70 | −4.09 |
| Backend | 29.20 | 27.86 | −1.34 |
| QA | 22.91 | 21.93 | −0.98 |

**Three roles experienced the most severe decline:**
- **Machine Learning** (−7.8 pp, largest drop): fell from the highest Q3 rate (34.6%) to 26.8%.
- **DevOps** (−6.9 pp): dropped from 32.9% to 26.1%.
- **Data Engineer** (−6.5 pp): dropped from 32.9% to 26.4%.

These three roles collectively account for **41% of Engineering applications** and drove the majority of the overall decline.

![Role Conversion Rates](<../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/work/role_conversion.png>)

---

## 2. Hiring Manager Analysis

### Quarterly Conversion by Manager

| Hiring Manager | Q3 2024 (%) | Q4 2024 (%) | Change (pp) | Overall Avg Rate |
|---------------|:-----------:|:-----------:|:-----------:|:----------------:|
| **David Thompson** | 23.05 | 19.43 | −3.62 | **20.78%** |
| **Mike Rodriguez** | 23.89 | 20.41 | −3.48 | **22.13%** |
| Alex Turner | 28.50 | 24.89 | −3.60 | 26.52% |
| Jennifer Kim | 29.86 | 25.11 | −4.75 | 27.56% |
| Sarah Chen | 34.49 | 28.18 | −6.32 | 31.27% |
| **Lisa Wang** | 37.50 | 30.58 | −6.92 | **33.92%** |

![Manager Conversion Rates](<../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/work/manager_conversion.png>)

### Key Findings

- **David Thompson** has the **lowest systematic conversion rate** (20.78% overall, 19.43% in Q4). His Q4 rate is more than 10 percentage points below the Engineering average.
- **Mike Rodriguez** is the second lowest (22.13% overall). Both managers' jobs consistently underperform.
- **Lisa Wang** has the highest rates (33.92% overall) but experienced the largest absolute decline (−6.9 pp).
- **Sarah Chen** also shows strong performance (31.27% overall) but with a notable decline.
- The OLS regression (R² = 0.78) confirms that hiring manager identity is the **single strongest predictor** of conversion rate after controlling for other factors:
  - David Thompson: **−5.7 pp** (p < 0.001)
  - Mike Rodriguez: **−4.7 pp** (p < 0.001)
  - Lisa Wang: **+7.3 pp** (p < 0.001)
  - Sarah Chen: **+4.5 pp** (p < 0.001)

![Manager Boxplot](<../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/work/manager_boxplot.png>)

---

## 3. Quantified Impact of Factors

### Regression Model (OLS, n = 154 Engineering jobs, R² = 0.78)

| Factor | Coefficient | Standard Error | p-value | Interpretation |
|--------|:-----------:|:--------------:|:-------:|----------------|
| **Intercept** | 45.39 | 2.80 | <0.001 | Baseline rate |
| **Created Month** | **−1.54** | 0.14 | <0.001 | Each month later → 1.5 pp lower conversion |
| **Number of Interviewers** | **−1.12** | 0.49 | 0.024 | 2 interviewers → 1.1 pp lower than 1 |
| **Avg Job Rating** | −1.15 | 0.54 | 0.035 | Higher-rated jobs slightly more selective |
| **Total Applications** | +0.02 | 0.01 | 0.042 | Larger applicant pools convert slightly higher |
| Hiring Manager (ref: Alex Turner) | — | — | — | See above |

### Number of Interviewers

- Engineering jobs have either **1 or 2 interviewers** (recruiters assigned per job).
- Jobs with 1 interviewer: mean rate = **27.0%**; with 2 interviewers: mean rate = **27.1%** — no raw difference.
- After controlling for hiring manager identity and time trend, each additional interviewer is associated with **−1.1 percentage points** (p = 0.024). This suggests that managers who tend to use more interviewers may also be assigned more complex or challenging roles, but the effect is small.

### Time Trend (Proxy for Systemic Decline)

- The **strongest factor** is the job creation month: each successive month in 2024 sees conversion drop by **−1.5 pp**.
- This is a uniform decline affecting all managers and roles, indicating a systemic issue rather than isolated problems.

![Monthly Trend](<../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/work/monthly_trend.png>)

![Scatter: Month vs Rate](<../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/work/scatter_month_interviewers.png>)

### Hiring Manager "Years of Experience"

**No direct "years of experience" field exists** in the database schema. The available proxies were examined:

| Proxy | Finding |
|-------|---------|
| Months active (Jul–Dec 2024) | All 6 managers active all 6 months — no differentiation |
| Number of distinct job titles managed | Ranges 17–21, no correlation with rate |
| Number of jobs managed | Ranges 23–28, no correlation with rate |
| Number of applications processed | Ranges 1,876–2,441, no monotonic relationship |

The manager dummy variables in the regression capture **all manager-specific effects** (including unobserved experience, skill, or process differences). The significant differences between managers (e.g., David Thompson −5.7 pp vs. Lisa Wang +7.3 pp) suggest that manager-level factors are highly influential, but the specific contribution of "years of experience" cannot be isolated from the available data.

---

## 4. Comparison with Marketing Department

| Metric | Engineering Q3→Q4 | Marketing Q3→Q4 |
|--------|:-----------------:|:----------------:|
| Application-to-Interview Rate | 29.6% → 25.1% | 53.0% → 53.6% |
| Hire Rate | 23.1% → 19.5% | 42.5% → 41.4% |
| Number of Hiring Managers | 6 | 2 |
| Managers with declining rates | 6/6 declining | 0/2 declining |

Marketing's conversion rate is **stable and roughly double** Engineering's. Both Marketing hiring managers (Emily Davis ~57.6%, Robert Johnson ~48.9%) have consistent rates across quarters, suggesting the Engineering decline is department-specific.

---

## 5. Recommendations

1. **Investigate David Thompson and Mike Rodriguez's hiring processes** — they have the lowest systematic conversion rates (20.8% and 22.1% overall). Audit their screening criteria, job descriptions, and interviewer training.
2. **Focus on Machine Learning, DevOps, and Data Engineer roles** — these experienced the steepest declines (6.5–7.8 pp) and together account for 41% of applications.
3. **Study Lisa Wang and Sarah Chen's best practices** — their consistently higher rates (33.9% and 31.3%) suggest more effective screening-to-interview pipelines.
4. **Address the systemic month-over-month decline** (−1.5 pp per month) affecting all roles and managers. This may indicate process fatigue, increasing competition, or changing market conditions.
5. **Review the two-interviewer model** — while the effect is small, having 2 interviewers is associated with slightly lower conversion rates. Consider whether the screening process can be streamlined.

---

## Limitations

- **"Years of experience"** is not directly available in the database schema. Manager-level differences are captured through dummy variables, but the specific contribution of experience cannot be quantified.
- **Only 2 quarters of data** (Q3 and Q4 2024) are available, limiting trend analysis.
- The **number of interviewers** is derived from the comma-separated `recruiters` field in `greenhouse__job_enhanced`, which may not perfectly capture the actual interviewer panel composition.