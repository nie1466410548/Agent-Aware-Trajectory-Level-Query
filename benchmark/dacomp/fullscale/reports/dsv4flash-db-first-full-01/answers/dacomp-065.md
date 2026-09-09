<!-- Reading copy: local artifact links normalized. Original answer is preserved at ../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/answer.md -->

# Recruitment Data Analysis Report: Company Background, Interview Performance, and Bias Detection

## Executive Summary

This report analyzes 12,000 distinct job applications with 11,928 interview scorecards to assess (1) whether candidates from well-known tech companies perform better in technical interviews, (2) whether this effect persists after controlling for education and experience, and (3) whether systemic biases exist in the interview process.

**Key findings:**
1. FAANG candidates significantly outperform others in technical interviews (avg 7.79/10 vs 7.44 for Major Tech, 7.26 for Traditional; p<0.0001).
2. This advantage persists after controlling for education, experience, skills, and university tier (FAANG coefficient remains ~0.51, p<0.0001).
3. The FAANG premium is **uniform across all scoring dimensions** (technical, problem-solving, communication, culture fit, leadership), suggesting a potential **halo effect** rather than purely superior technical skill.
4. FAANG candidates also have higher conversion rates at every stage of the hiring funnel, compounding the advantage.
5. No significant gender bias was detected in scores or hiring outcomes. Race differences in scores exist but are small and do not persist in controlled models.
6. Female interviewers give slightly higher scores on average than male interviewers (7.66 vs 7.49, p<0.0001).

---

## 1. Data Overview

| Metric | Count |
|--------|-------|
| Total applications (rows) | 18,186 |
| Distinct applications | 12,000 |
| Distinct candidates | 12,000 |
| Interview scorecards (distinct) | 11,928 |
| Distinct applications with interviews | 4,744 |
| Total hired | 1,859 (~15.5% of distinct apps) |

**Company category distribution** (distinct applications):
- **FAANG** (Meta, Apple, Amazon, Netflix, Google/Alphabet): 1,772 (14.8%)
- **Major Tech / Unicorns**: 6,430 (53.6%)
- **Traditional / Non-tech**: 3,798 (31.6%)

---

## 2. Analysis 1: Technical Interview Performance by Company Background

### 2.1 Average Technical Scores

| Company Category | N | Mean Tech Score | Std Dev | Median |
|-----------------|---|----------------|---------|--------|
| **FAANG** | 675 | **7.79** | 1.72 | 8.00 |
| **Major Tech** | 2,548 | **7.44** | 1.82 | 8.00 |
| **Traditional** | 1,521 | **7.26** | 1.89 | 7.75 |

### 2.2 Statistical Significance

- **ANOVA**: F = 20.27, p < 0.0001
- **Kruskal-Wallis**: H = 39.54, p < 0.0001
- **Pairwise t-tests** (all significant):
  - FAANG vs Traditional: t = 6.56, p < 0.0001
  - FAANG vs Major Tech: t = 4.65, p < 0.0001
  - Major Tech vs Traditional: t = 3.11, p = 0.0019

### 2.3 Effect Sizes (Cohen's d)

| Comparison | Cohen's d | Interpretation |
|-----------|-----------|---------------|
| FAANG vs Traditional | 0.29 | Small-medium |
| FAANG vs Major Tech | 0.19 | Small |
| Major Tech vs Traditional | 0.10 | Very small |

### 2.4 Positive Recommendation Rate

| Company Category | % Positive Recommendation | Chi-square p |
|-----------------|--------------------------|-------------|
| FAANG | 84.0% | |
| Major Tech | 82.8% | 0.0059 |
| Traditional | 79.3% | |

![Technical Score by Company Background](<../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/work/tech_score_by_company.png>)

---

## 3. Analysis 2: Controlling for Education and Experience

### 3.1 Regression Models

**Model 1 – Company category only:**
| Variable | Coefficient | Std Err | t | p-value |
|----------|------------|---------|---|---------|
| Intercept (Traditional) | 7.2566 | 0.047 | 154.7 | <0.0001 |
| **FAANG** | **0.5376** | 0.085 | 6.35 | **<0.0001** |
| Major Tech | 0.1875 | 0.059 | 3.16 | 0.0016 |
| R² = 0.0085 | | | | |

**Model 2 – Adding education, experience, skills, university tier:**
| Variable | Coefficient | Std Err | t | p-value |
|----------|------------|---------|---|---------|
| Intercept (Traditional) | 7.3482 | 0.118 | 62.05 | <0.0001 |
| **FAANG** | **0.5084** | 0.089 | 5.74 | **<0.0001** |
| Major Tech | 0.1871 | 0.059 | 3.15 | 0.0016 |
| Education Level | -0.0109 | 0.033 | -0.33 | 0.743 |
| Years of Experience | -0.0144 | 0.008 | -1.91 | 0.057 |
| Skill Count | -0.0053 | 0.016 | -0.32 | 0.747 |
| University Tier | 0.0363 | 0.029 | 1.26 | 0.207 |
| R² = 0.0096 | | | | |

### 3.2 Key Finding

The **FAANG coefficient barely changes** (from 0.538 to 0.508) after controlling for education, experience, skills, and university tier. All controls are non-significant, and the overall R² remains very low (0.0096), meaning company background and these factors explain very little of the variance in interview scores. The FAANG advantage is **not explained by** better education, more experience, or more listed skills.

---

## 4. Analysis 3: Bias Detection

### 4.1 Candidate Demographics and Scores

**By Candidate Gender:**
| Gender | Mean Tech Score | N | p-value |
|--------|---------------|---|---------|
| Male | 7.665 | 954 | |
| Non-binary | 7.540 | 955 | |
| Prefer not to say | 7.503 | 1,176 | |
| Female | 7.501 | 1,192 | |
| **ANOVA p = 0.153** → Not significant | | | |

**By Candidate Race:**
| Race | Mean Tech Score | N | 
|------|---------------|---|
| Asian | **7.728** | 771 |
| Native American | 7.573 | 737 |
| Black | 7.565 | 787 |
| Other | 7.536 | 830 |
| White | 7.421 | 743 |
| Hispanic | **7.347** | 743 |
| **ANOVA p = 0.002** → Significant | | |

However, in the full regression model controlling for company background, education, and experience, **race is not a significant predictor** (p = 0.14). The raw race differences partly reflect the different company backgrounds of candidates.

### 4.2 Hiring Outcomes by Demographics

| Dimension | Chi-square p-value | Significant? |
|-----------|-------------------|-------------|
| Gender × Hired | 0.390 | No |
| Race × Hired | 0.143 | No |

### 4.3 Interviewer Effects

**Female interviewers give higher scores** (7.66) than male interviewers (7.49), t = -4.54, p < 0.0001.

**Male-Male pairing effect:** Male candidates with male interviewers score 7.72, while other gender combinations average ~7.50. However, the formal interaction test is not statistically significant (p = 0.38) due to small sample size.

### 4.4 The Halo Effect: Uniform FAANG Premium Across All Dimensions

When controlling for education, experience, and skills, the FAANG advantage is remarkably **uniform across all five scoring dimensions**:

| Dimension | FAANG Coefficient (controlled) | p-value |
|-----------|------------------------------|---------|
| Problem Solving | 0.590 | <0.0001 |
| Communication | 0.540 | <0.0001 |
| Technical | 0.508 | <0.0001 |
| Culture Fit | 0.451 | <0.0001 |
| Leadership | 0.435 | <0.0001 |

![FAANG Premium by Dimension](<../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/work/bias_quantification.png>)

If the FAANG advantage were purely due to superior technical skills, we would expect the premium to be concentrated in the Technical and Problem Solving dimensions. Instead, the premium is **present and comparable across all dimensions**, including Culture Fit and Leadership, which are subjective and unrelated to technical background. This pattern is consistent with a **halo effect** — a cognitive bias where an interviewer's positive impression of a candidate's company background unconsciously inflates ratings across all dimensions.

### 4.5 Hiring Funnel Analysis

FAANG candidates have **higher conversion rates at every stage** of the hiring process:

| Stage Transition | FAANG | Major Tech | Traditional |
|-----------------|-------|-----------|-------------|
| App Review → Phone Screen | **77.9%** | 65.3% | 62.6% |
| Phone Screen → Tech Interview | **72.2%** | 60.9% | 59.4% |
| Tech Interview → Panel | **69.1%** | 61.3% | 56.7% |
| Panel → Final Interview | **63.3%** | 57.4% | 54.2% |
| Final Interview → Offer | **91.7%** | 88.1% | 88.2% |
| Offer → Hired | **83.8%** | 77.9% | 80.2% |
| **Overall Hire Rate** | **18.9%** | **9.6%** | **8.1%** |

![Hiring Funnel Analysis](<../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/work/funnel_analysis.png>)

The cumulative effect is substantial: FAANG applicants are hired at **2.3× the rate** of Traditional applicants and **2.0× the rate** of Major Tech applicants.

---

## 5. Conclusions and Recommendations

### 5.1 Does Company Background Affect Technical Performance?

**Yes.** FAANG candidates score significantly higher on technical interviews (7.79 vs 7.26 for Traditional, Cohen's d = 0.29). This is a statistically significant but small-to-medium effect.

### 5.2 Does the Company Effect Persist After Controls?

**Yes, strongly.** The FAANG coefficient barely changes when controlling for education, experience, skills, and university tier (0.538 → 0.508). This suggests that the advantage is not explained by observable qualifications.

### 5.3 Evidence of Systemic Bias

**Yes, there are several concerning patterns:**

1. **Halo effect (company prestige bias):** The FAANG premium is uniform across all scoring dimensions — technical, problem-solving, communication, culture fit, and leadership. This is inconsistent with a purely skill-based explanation and suggests that interviewers may be unconsciously influenced by a candidate's company background.

2. **Interviewer gender effects:** Female interviewers give systematically higher scores (by 0.17 points, p < 0.0001). This could lead to inconsistent evaluation standards.

3. **Compounding funnel advantage:** FAANG candidates benefit from higher conversion rates at every stage — from initial screening through final offer — creating a cumulative advantage that goes beyond any single interview score difference.

4. **Race differences in scores:** Asian candidates score highest (7.73) and Hispanic candidates lowest (7.35) on technical evaluations. While this partly reflects company background differences, it warrants monitoring.

### 5.4 Recommendations

1. **Structured interview rubrics:** Implement detailed scoring criteria by dimension to reduce halo effects from company background.
2. **Blind screening:** Remove company name from initial application review stages.
3. **Interviewer calibration:** Address the systematic difference between male and female interviewers through calibration sessions.
4. **Diverse interview panels:** Ensure multiple interviewers with diverse backgrounds evaluate each candidate.
5. **Track conversion rates by company background:** Monitor for funnel disparities and intervene if FAANG/non-FAANG gaps persist after rubric implementation.

---

## Limitations

1. **Demographic data completeness:** ~60% of candidate demographic data is missing, limiting the bias analysis power.
2. **Observational data:** We cannot establish causality — FAANG candidates may genuinely have stronger skills not captured by our control variables.
3. **Low R²:** All models explain <1% of variance, suggesting many unmeasured factors drive interview performance.
4. **Duplicate records:** The database contains duplicate rows that required deduplication, but results may still have minor artifacts.
5. **Company categorization:** The grouping of companies into categories is somewhat arbitrary; individual company-level effects may differ.

---

*All analyses performed using SQLite for data extraction and Python (scipy, numpy, matplotlib) for statistical testing and visualization. Complete code and intermediate results are archived.*