<!-- Reading copy: local artifact links normalized. Original answer is preserved at ../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/answer.md -->

# Integrated Ranking of Production Employees & Next-Recruit Profile

## 1. Data & Method

**Data**: 6 daily-record sheets (Apr–May 2025) covering **68 unique employees** across 3 production teams (Group 1: 24, Group 2: 22, Group 3: 22), ~3,000 daily records. Fields used: Standard Working Hours (8h), Total Time Away ("XminYs" parsed), Units Produced, Pass Rate (%), Age, Gender, Education Level, Hire-Date tenure, Base Salary, Disciplinary Issue, Company Accommodation.

**Integrated ranking**: For each employee we computed
- **Effective Working Hours** = Σ(8h − daily time away),
- **Overall Units Produced** = Σ daily units,
- **Production Quality** = mean Pass Rate (%),

then min-max normalized each component to 0–1 and averaged with equal weights (composite score, rank 1–68). The ranking is robust: under 5 alternative weightings (quality‑/output‑/time‑focused, per‑day averages), the same **core five employees (Cai Yan, Lu Ying, Feng Ting, Li Jing, Han Hong)** always remain in the Top 10; **Cai Yan is #1 under every scheme** (Jaccard overlap with baseline Top-10: 0.54–1.00).

## 2. Who Are the Current Top Employees?

| Rank | Employee | Gender | Age | Education | Tenure (mo) | Avg Units/day | Pass Rate | Salary | Accommodation |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Cai Yan | F | 27 | Junior college | 9 | 144.2 | 73.8% | 3,975 | Yes |
| 2 | Lu Ying | F | 26 | High School | 6 | 147.6 | 74.1% | 3,896 | Yes |
| 3 | Feng Ting | F | 23 | Junior college | 6 | 118.3 | 74.2% | 4,300 | Yes |
| 4 | Li Jing | F | 22 | High School | 5 | 145.1 | 73.0% | 4,729 | Yes |
| 5 | Han Hong | F | 24 | Tech. secondary | 10 | 128.2 | 74.6% | 5,121 | Yes |
| 6 | Zheng Mei | F | 24 | High School | 14 | 136.2 | 73.9% | 4,758 | Yes |
| 7 | Zhong Ling | F | 23 | High School | 2 | 106.4 | 71.9% | 5,104 | No |
| 8 | Li Na | F | 23 | Junior college | 14 | 123.7 | 74.6% | 4,489 | Yes |
| 9 | Wei Juan | F | 22 | Junior college | 22 | 128.6 | 71.8% | 4,839 | No |
| 10 | Zhou Ying | F | 22 | High School | 5 | 145.6 | 73.4% | 4,048 | Yes |

**Statistical characteristics of Top-10 vs. the rest (t-tests):**
- **All 10 are female** (top 20: 16 F / 4 M; best male rank = 15). Females outperform males in *every* team and *every* education group.
- **Young**: mean age 23.6 vs. 25.0 (p=0.073); age band 22–27.
- **Shorter tenure**: 9.3 vs. 14.5 months (p=0.027) — top performance is achievable by recent hires.
- **Education**: High School (5) + Junior college (4) + Technical secondary (1); **no Junior-high-school graduate** made the Top 10.
- **Both output AND quality higher**: 132 vs. 99 units/day and 73.5% vs. 71.2% pass rate (both p<0.001). No output↔quality tradeoff (r=+0.37 overall; top producers also pass at higher rates).
- **Attendance/focus**: top-10 employees average 18.3 units per effective hour vs. ~15.2 workforce mean; they spend 7.16 effective hours/day on station (vs. 6.36 for males), with fewer away-from-station events (5.2 vs. 7.1/day).
- **Company accommodation**: 80% of Top 10 use company accommodation vs. 45% of the rest.
- **Discipline**: only 2/10 Top-10 had any disciplinary record vs. 21/58 of the rest; 29 of 34 disciplinary incidents were male (phone/smoking/games/videos on the line, quarrels).
- **Salary**: no link with performance (r = −0.10; Top-10 mean 4,526 vs. 4,510, n.s.).

**Performance stability**: April→May output correlation r=0.93 and pass-rate r=0.88; top performers are consistently top in both months (see `/work/scatter_analysis.png`, `/work/employee_profile_analysis.png`, `/work/top10_vs_rest_profile.png`, `/work/gender_discipline_summary.png`, `/work/component_scores_comparison.png`).

## 3. Recommendations — Candidate Profile to Recruit Next

Based on the observed characteristics of the current top performers:

1. **Demographic screen**: Young adult, **age 22–27**; all evidence points to **female candidates** being strongly associated with top performance (statistically significant and consistent across all teams/education levels — see `/work/gender_discipline_summary.png`). Because gender-based screening may raise fairness concerns, translate this into the *behavioural* traits below and treat it as a weighting signal rather than a hard filter.
2. **Education**: prefer **High School or Junior college** education; **Junior high school alone is associated with the weakest performance** and no top-10 representative. Technical secondary school is acceptable but less represented at the top.
3. **Attendance / station presence** (the actionable core of "Effective Working Hours"): recruit candidates with a demonstrated record of **low away-from-station time and few breaks** — this is the single clearest operational lever (top performers are away ~0.8 h/day vs. 1.6 h/day for lower performers).
4. **Behavioural integrity**: screen for **no disciplinary history** (no phone use, smoking, or off-task behaviour on the line) — top performers are essentially discipline-free.
5. **No prior-experience requirement**: recent hires (2–10 months tenure) rank at the very top, so **fresh hires can be fast-tracked**; do not over-weight long tenure in screening.
6. **Housing/logistics**: candidates able to take **company accommodation** correlate with higher ranks (80% of Top 10); prioritise accommodation-supported hires to reduce commute-related absence.
7. **Target the Group 2 production benchmark** (5 of Top 10 come from Group 2, the strongest-performing team) and replicate its coaching/onboarding practices when the new hire joins.

## 4. Limitations
- Analysis is observational; the strong gender–productivity association may reflect unmeasured factors (task assignment, workstation, experience) and should not be applied as a hard exclusion criterion.
- Only two months of data; single production plant context (electrical appliance assembly).
- Pass Rate is coarse (integer percent values 70–77%), limiting quality discrimination.
- "Effective Working Hours" assumes all non-away time is productive; productivity-per-hour differences (females 16.9 vs. males 13.3 units/h) show that time-on-station alone does not explain performance.
