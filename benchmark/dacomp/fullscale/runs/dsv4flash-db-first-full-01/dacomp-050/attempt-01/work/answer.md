# Suicidal Ideation Among Students: Economic, Academic-Stress, and Diet/Sleep Characteristics, and Relapse-Prevention Implications

## Scope & method
- **Sample:** 18,762 students of 93,800 total records (working professionals excluded); 11,778 (62.8%) answered "Yes" to *Have you ever had suicidal thoughts?* — the rest of the group serves as the comparator.
- **Analyses:** SQL aggregation/grouping of prevalence within the database; Python logistic regression (fitted on student rows pre-filtered in SQL) to quantify independent associations with odds ratios (OR) and 95% CI; visual summaries generated from the SQL aggregate output.
- **Dimensions of interest:** economic (financial stress 1–5), academic (academic stress 1–5, study satisfaction, CGPA, study hours), and diet/sleep (self-reported diet quality, sleep duration).

## 1. Who are the students with suicidal ideation?

### Economic dimension (financial stress)
| Financial stress | Students | % with suicidal thoughts |
|---|---|---|
| Low (1–2) | 7,026 | 50.0% |
| Medium (3) | 3,448 | 63.9% |
| High (4–5) | 8,288 | **73.2%** |

- 44.2% of all students report high financial stress (4–5). Adjusted OR = **1.29 per stress point** (1.26–1.32, p<0.001) — a strong, independent economic gradient.

### Academic-stress dimension
| Academic stress | Students | % with suicidal thoughts |
|---|---|---|
| Low (1–2) | 5,959 | 44.7% |
| Medium (3) | 4,927 | 65.4% |
| High (4–5) | 7,876 | **74.8%** |

- 41.9% report high academic stress. Adjusted OR = **1.42 per stress point** (1.39–1.46, p<0.001) — the single strongest per-unit predictor.
- Supporting signals: low study satisfaction → 67.2% vs high → 58.1% (OR 0.93 per point, protective); study/work hours >9 → 67.9% vs ≤6 → 56.0% (OR 1.06 per hour). **CGPA showed no meaningful gradient (61–64% across all bands)** — distress tracks perceived stress and workload, not achieved grades.

### Diet and sleep dimension
| Diet | % with suicidal thoughts | Sleep duration | % with suicidal thoughts |
|---|---|---|---|
| Healthy | 56.1% | More than 8 h | 57.4% |
| Moderate | 60.7% | 5–6 h | 62.7% |
| Unhealthy | **69.8%** | 7–8 h | 63.7% |
| | | Less than 5 h | **66.0%** |

- 36.8% eat unhealthy; 29.8% sleep <5 h. Adjusted OR: **Unhealthy vs Healthy diet = 1.51 (1.40–1.64)**; **Sleep <5 h vs ≥7 h = 1.19 (1.10–1.28)** — diet is the stronger lifestyle factor, and the two combine multiplicatively (unhealthy diet **and** <5 h sleep = **72.8%** vs 55.5% for healthy diet + ≥5 h sleep).

### Demographic context
- Age gradient: <20 → 69.9%, 20–24 → 66.8%, 25–29 → 62.9%, 30+ → 54.7% (younger students at higher risk; OR 0.97 per year, protective).
- Family history of mental illness: 64.5% vs 61.1% (OR 1.13, 1.06–1.20).
- Gender: no material difference (63.0% male vs 62.5% female).
- Degree: Class-12/pre-university students highest (68.4%); no professional degree stands out.

## 2. Cumulative risk: a clear dose–response

Counting four risk flags — academic stress ≥4, financial stress ≥4, unhealthy diet, sleep <5 h:

| Risk factors | Students | % with suicidal thoughts |
|---|---|---|
| 0 | 3,298 | 42.5% |
| 1 | 6,249 | 56.4% |
| 2 | 5,796 | 70.7% |
| 3 | 2,841 | 79.8% |
| 4 | 569 | **85.1%** |

High academic **and** high financial stress together raise prevalence to **80.8%** (vs 45.9% when neither is high). Logistic-regression scenario predictions: a protective profile (low stress, healthy lifestyle) = **25.6%** predicted probability; high financial stress alone = 58.4%; high academic stress alone = 48.8%; both high = **84.8%**; both high + unhealthy diet + <5 h sleep = **90.9%**; plus family history = **91.9%**.

![Prevalence gradients and risk-factor dose-response](student_suicidal_ideation_characteristics.png)

![Model-predicted probability by risk profile](student_predicted_probability_scenarios.png)

## 3. Devising relapse-prevention strategies

The three dimensions are **additive and actionable**, making them a natural framework for tiered prevention:

1. **Economic support (financial stress, OR 1.29/pt).** Financial-stress screening at enrollment; expand scholarships, fee installment plans, emergency grants, part-time work programs, and financial-literacy workshops. Because 20.9% of students carry *both* high academic and high financial stress (80.8% ideation), financial relief should be prioritized jointly with academic supports.

2. **Academic-stress management (OR 1.42/pt, strongest).** Academic workload is the highest-leverage modifiable factor. Implement realistic credit loads, deadline policies, study-skills and exam-coping workshops, faculty mental-health literacy, and counseling that targets *perceived* stress (independent of CGPA). Routine in-term stress check-ins for students with high study hours (>9 h) and low study satisfaction.

3. **Diet/sleep lifestyle intervention (unhealthy diet OR 1.51, <5 h sleep OR 1.19).** Campus nutrition programs (affordable healthy meal options, food-security support), sleep-hygiene education and scheduling reforms (no early-morning exams after late classes), and screening of students who report both unhealthy diet and short sleep (72.8% ideation). These are low-cost, high-reach relapse-prevention levers.

4. **Tiered risk stratification.** Use the four-factor score as a screening tool: 0–1 factors → universal prevention and psychoeducation; 2 factors → targeted check-ins and lifestyle coaching; 3–4 factors (80–85% ideation) → prioritized psychological evaluation, case management, and family-history-informed monitoring. Because family history (OR 1.13) and younger age further elevate risk, add them as risk-stratification weights.

## Limitations
- Cross-sectional, single self-report survey; association ≠ causation and recall bias possible (notably for "ever had" ideation).
- Stress and satisfaction are ordinal 1–5 self-ratings; diet/sleep are coarse self-report categories with a few data-entry errors (e.g., "Mealy," "Naina"), which were excluded from diet analysis.
- Class-12 (pre-university) students, who show the highest prevalence, are included in the student group but their coursework context differs from tertiary students.
- The logistic model did not test interactions beyond the count-based stratification; the scenario probabilities assume independence of effects.
