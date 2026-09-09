<!-- Reading copy: local artifact links normalized. Original answer is preserved at ../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/answer.md -->

# Employee Tenure and Retention Analysis

## 1. Overview & Data

The analysis uses the employee snapshot table (`sheet1`) with **1,480 employee records** (1,470 unique employee IDs). **238 employees (16.08%)** left the company (attrition = "Yes"). Average tenure at the company is **7.0 years** (stayers average 7.37 years vs. leavers 5.12 years). Tenure ranges from 0 to 40 years.

## 2. Current Employment Status by Working-Years Intervals

| Tenure band | Employees | % of workforce | Leavers | Attrition rate |
|---|---|---|---|---|
| 0–5 years | 781 | 52.8% | 163 | **20.9%** |
| 6–10 years | 452 | 30.5% | 55 | 12.2% |
| 11–15 years | 108 | 7.3% | 7 | **6.5%** |
| 16–20 years | 73 | 4.9% | 5 | 6.9% |
| 20+ years | 66 | 4.5% | 8 | 12.1% |
| **Total** | **1,480** | 100% | **238** | **16.1%** |

Key observations (see `fig1_tenure_bands.png`):
- The company is **front-loaded with short-tenure employees**: 83% of the workforce has been there < 11 years; only **24.8% (367 employees) have 10+ years**.
- **Attrition is highest in the first 5 years** (20.9%), and by single-year tenure it peaks at **36.4% in year 0 and 34.5% in year 1**, then falls and stabilizes around 10–12% in years 5–9.
- The **6–10 year band is the critical transition zone**: 452 employees sit just below the 10-year mark; losing them (55 already left, 12.2%) prevents them from becoming long-term retained staff.
- Attrition is very low in the 11–15 (6.5%) and 16–20 (6.9%) bands — once employees cross ~10 years, they overwhelmingly stay (the 20+ band bump to 12.1% is based on only 8 of 66 employees).

![Tenure bands: counts and attrition](<../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/work/fig1_tenure_bands.png>)

## 3. Characteristics of Long-Term Retained Employees (10+ years)

The **367 long-term employees (10+ years)** differ sharply from the <10-year group (see `fig2_longterm_comparison.png`):

| Metric | 10+ years | <10 years | Difference |
|---|---|---|---|
| Avg monthly income | **$9,541** | $5,504 | +73% |
| Avg job level (1–5) | 2.84 | 1.81 | +1.0 level |
| Avg years since last promotion | 5.09 | 1.22 | +3.9 yrs |
| Avg years in current role | 8.49 | 2.82 | +5.7 yrs |
| Avg years with current manager | 8.31 | 2.74 | +5.6 yrs |
| Avg total working years | 17.65 | 9.18 | +8.5 yrs |
| Avg companies worked | 2.23 | 2.84 | −0.6 |
| Avg overtime % | 26.4% | 28.8% | −2.4 pp |
| Avg job satisfaction | 2.76 | 2.71 | ≈ same |
| Avg work-life balance | 2.76 | 2.76 | same |

**Profile of a long-term retained employee:** Older (avg 40 vs 36), higher-paid, more senior (job level ~3), promoted into higher roles over time, with a **stable role, stable manager, and fewer prior employers**. Notably, satisfaction scores are *not* higher for long-tenured staff — tenure is driven by structure and progression, not by happiness scores. Department mix is similar (R&D ~63%, Sales ~33%, HR ~4%), and top long-term roles are Sales Executive (26%), Manager (16%), Manufacturing Director and Research Scientist (11% each).

![Long-term vs short-term comparison](<../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/work/fig2_longterm_comparison.png>)

**Income and promotion progression by band** (`fig3_income_promotion.png`) shows retention correlates with tangible career growth: average income climbs from $5,075 (0–5 yrs) → $6,579 (6–10) → $7,729 (11–15) → $10,945 (16–20) → $16,008 (20+), with job level rising from 1.7 to 4.3.

**Correlation with YearsAtCompany** (Pearson, computed in Python): YearsWithCurrManager (0.764), YearsInCurrentRole (0.759), TotalWorkingYears (0.628), YearsSinceLastPromotion (0.619), JobLevel (0.535), MonthlyIncome (0.514), Age (0.311); negative with NumCompaniesWorked (−0.119).

![Income and promotion gap by tenure band](<../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/work/fig3_income_promotion.png>)

## 4. What Actually Drives Attrition (and threats to long-term retention)

Comparing the 238 leavers vs 1,242 stayers across the whole workforce (`fig4_attrition_drivers.png`):

- **Pay:** leavers earn **$4,813** vs stayers **$6,829** (−30%).
- **Overtime:** **53.8% of leavers** worked overtime vs only **23.4% of stayers**.
- **Equity:** **64.7% of leavers** had no stock options vs 38.8% of stayers.
- **Satisfaction:** job satisfaction 2.46 vs 2.78; environment satisfaction 2.47 vs 2.77.

**Overtime × stock-option attrition rates:**
| Overtime | No stock (L0) | Stock L1 | Stock L2 | Stock L3 |
|---|---|---|---|---|
| No | 15.9% | 6.3% | 5.0% | 8.9% |
| Yes | **45.1%** | 17.8% | 15.8% | 34.5% |

Employees who both work overtime **and** hold no equity leave at ~45% — nearly 3× the company average.

**The 6–10 year "at-risk" zone (452 employees, 55 leavers):** leavers vs stayers differ on income ($5,609 vs $6,713), years since last promotion (**3.65 vs 2.47**), overtime (56.4% vs 22.7%), no stock options (58.2% vs 36.0%), job satisfaction (2.62 vs 2.78), and job-hopping history (2.65 vs 2.16 companies). Highest-attrition roles in this band: Research Scientist (17.5%, avg income only $3,622), Laboratory Technician (15.2%, $3,854), Sales Executive (14.6%).

**Even the 10+ retained segment is not immune:** the 38 long-term leavers worked much more overtime (44.7% vs 24.3%), had waited longer for promotion (6.34 vs 4.94 years), earned less ($8,769 vs $9,630), and had lower satisfaction (2.58 vs 2.78 job sat) than long-term stayers — i.e., stagnation and workload erode even deep-tenure retention.

**Role-level warning signs** (attrition rate / avg income): Sales Representative 39.3% / $2,630, Laboratory Technician 23.8% / $3,239, Human Resources 23.1% / $4,236, Research Scientist 16.0% / $3,242, Sales Executive 17.6% / $6,947 — versus Manager 4.9% / $17,182 and Research Director 2.5% / $16,034. Low-paying front-line roles churn fastest.

![Attrition drivers: overtime and stock options](<../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/work/fig4_attrition_drivers.png>)

## 5. Recommended Actions to Increase Employee Tenure

1. **Fix the promotion cadence for 6–10 year employees (highest leverage).** Promotion lag is the clearest differentiator: 6–10 year leavers waited 3.65 years vs 2.47 for stayers; long-term leavers waited 6.3 years. Implement **predictable promotion windows (e.g., 3–4 year cycles) with written career maps**, and a dual technical/managerial track so scientists and technicians can advance without leaving the bench. Target the Research Scientist and Laboratory Technician populations in this band, where 15–17% attrition is concentrated.

2. **Address pay compression in high-turnover roles.** Sales Reps ($2,630), Lab Techs ($3,239), HR ($4,236) and Research Scientists ($3,242) earn far below the stayer average. Conduct market-based pay reviews and salary corrections for these roles — income is one of the strongest tenure correlates (r = 0.51).

3. **Cut and/or compensate overtime.** Overtime is the single strongest behavioral attrition signal (53.8% of leavers vs 23.4% of stayers; 45% attrition when combined with no equity). Redistribute workload, hire or backfill headcount in high-OT teams, cap mandatory OT, and visibly compensate it. This protects both the 6–10 year zone and the 10+ cohort (long-term leavers had 44.7% OT).

4. **Broaden stock-option / equity grants.** Employees without stock options leave at ~2.5× the rate of those with options (no-OT scenario 15.9% vs 6.3%). Extend vesting equity to mid-tenure employees — especially at the 5- and 8-year marks — to create a financial reason to cross the 10-year threshold.

5. **Invest heavily in the first 2 years.** Attrition spikes at 34–36% in years 0–1, the biggest leak in the pipeline. Strengthen onboarding, assign mentors, set early (12-month) pay and role milestones, and track satisfaction quarterly in the first two years to convert new hires into the retained core.

6. **Stabilize managers and roles.** Years with the same manager correlates 0.76 with tenure, and long-term employees have 5+ more years of role/manager stability. Reduce manager churn in the mid-tenure band and avoid disruptive re-orgs/role rotations for employees with 5–9 years of service.

7. **Create a formal "10-year milestone" retention program.** Since 10+ year employees still leave when promoted too slowly and overworked, proactively manage career plateaus: recognition milestones, refresher equity grants, and role enrichment at the 10/15/20-year points to protect the small but valuable long-tenure base (367 people holding most of the organizational memory).

## 6. Limitations

- **Cross-sectional snapshot:** "Attrition" reflects who left during the observation window; tenure is current tenure, so we cannot observe true career-long survival curves or causal effects.
- **Correlational evidence:** e.g., overtime may proxy for team dysfunction rather than directly cause attrition; recommendations are directional, not proven interventions.
- **Small sub-samples:** the 20+ band (66 employees, 8 leavers) and 10+ leavers (38) make their attrition rates noisy.
- **Satisfaction is self-reported** ordinal data; pay/OT/equity patterns are the most robust signals.
- The dataset resembles a single-company snapshot (IBM-style HR analytics data); conclusions are company-specific and should be validated with longitudinal follow-up data.
