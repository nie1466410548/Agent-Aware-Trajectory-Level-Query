<!-- Reading copy: local artifact links normalized. Original answer is preserved at ../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/answer.md -->

# Analysis Report: Factors Affecting Students' Academic Performance

## Research Question

> *"Some people believe that the higher the parents' level of education, the better their children's academic performance. Do the survey data in the table support this view? Using the data in the table, which factors can be analyzed as having a larger impact on students' academic performance?"*

## Dataset Overview

The dataset contains **1,000 student records** with 15 variables including demographics, lifestyle factors, and exam scores. The average exam score is **69.6 ± 16.9** (range: 18.4–100).

---

## 1. Does Parents' Education Level Affect Exam Scores?

**No, the data does not support this belief.** The relationship is weak, non-monotonic, and statistically insignificant.

### Mean Exam Scores by Parents' Education Level

| Parents' Education | N    | Mean Exam Score | Std Dev |
|-------------------|------|----------------|---------|
| Bachelor          | 355  | 70.69          | 17.11   |
| Missing (NA)      | 89   | 69.90          | 16.72   |
| High School       | 391  | 69.26          | 17.05   |
| Master            | 165  | 67.90          | 16.08   |

### Key Statistical Findings

- **ANOVA test**: F = 1.654, p = 0.192 → **not statistically significant**
- **Kruskal-Wallis test**: H = 4.650, p = 0.098 → **not statistically significant**
- **Effect size (η²)**: 0.0036 — parents' education explains only **0.36%** of the variance in exam scores
- The only pairwise comparison that reached significance (Bachelor vs Master, p = 0.03) shows **Bachelor parents have children with higher scores** (70.69 vs 67.90), which is the **opposite direction** of the hypothesized relationship
- The "Master" group actually has the **lowest** average exam score, contradicting the belief that higher education = better performance

### Visualization

![Boxplots of Exam Scores by Various Factors](<../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/work/figure1_factors_boxplots.png>)

*Figure 1: The top-left panel shows exam scores by parents' education level — the differences are minimal and inconsistent.*

**Conclusion**: The belief that higher parental education improves children's academic performance is **not supported** by this dataset. The effect is negligible and statistically non-significant.

---

## 2. Which Factors Have the Largest Impact on Exam Scores?

A multiple linear regression model was fitted (R² = 0.855, Adjusted R² = 0.852), explaining 85.5% of the variance in exam scores. The table below shows standardized coefficients (beta weights) ranking all factors by relative importance.

### Standardized Regression Coefficients (Ranked by Importance)

![Standardized Coefficients Bar Chart](<../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/work/figure3_standardized_coefficients.png>)

| Rank | Factor                  | Std. Coefficient | Direction | Interpretation |
|------|------------------------|-----------------|-----------|----------------|
| 1    | **Daily study time**   | **+0.825**      | Positive | **Strongest predictor** — more study time dramatically improves scores |
| 2    | **Mental health score**| **+0.311**      | Positive | Better mental health is strongly associated with higher scores |
| 3    | **Exercise frequency** | **+0.175**      | Positive | Regular exercise correlates with better performance |
| 4    | Social media usage     | −0.133          | Negative | More social media use slightly reduces scores |
| 5    | Sleep duration         | +0.132          | Positive | Longer sleep is beneficial |
| 6–17 | All other factors      | \|β\| < 0.03   | —        | Negligible impact |

### Detailed Breakdown of Key Factors

#### 📚 Daily Study Time (r = 0.825)

| Study Time | N    | Avg Exam Score |
|-----------|------|---------------|
| <2 hours  | 133  | 45.56         |
| 2–4 hours | 482  | 65.14         |
| 4–6 hours | 332  | 81.28         |
| 6+ hours  | 53   | 97.39         |

Students who study 6+ hours per day score **more than double** the exam score of those who study less than 2 hours. This is by far the most influential factor.

#### 🧠 Mental Health Score (r = 0.326)

| Mental Health Category | N    | Avg Exam Score |
|------------------------|------|---------------|
| Low (0–3)             | 315  | 63.37         |
| Medium (4–6)          | 312  | 68.07         |
| High (7–10)           | 373  | 76.15         |

Higher mental health scores are strongly associated with better exam performance.

#### 📱 Social Media Usage Time (r = −0.214)

| Social Media Time | N    | Avg Exam Score |
|------------------|------|---------------|
| <1 hour          | 84   | 76.79         |
| 1–3 hours        | 586  | 70.26         |
| 3–5 hours        | 297  | 67.27         |
| 5+ hours         | 33   | 65.52         |

More social media time is associated with lower exam scores.

#### 😴 Sleep Duration (r = 0.122)

| Sleep Duration | N    | Avg Exam Score |
|---------------|------|---------------|
| <5 hours      | 23   | 63.83         |
| 5–7 hours     | 568  | 68.68         |
| 7–9 hours     | 385  | 71.17         |
| 9+ hours      | 24   | 67.43         |

Sleeping 7–9 hours is associated with the best exam performance.

#### 🏃 Exercise Frequency (r = 0.146)

| Exercise (days/week) | N    | Avg Exam Score |
|---------------------|------|---------------|
| 0–1                 | 273  | 66.85         |
| 2–3                 | 472  | 69.63         |
| 4–5                 | 212  | 72.51         |
| 6–7                 | 43   | 71.60         |

More frequent exercise is associated with higher exam scores.

### Scatter Plot Visualizations

![Scatter plots of strongest predictors](<../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/work/figure2_scatter_correlations.png>)

*Figure 2: Daily study time shows a strong positive linear relationship with exam scores. Mental health and social media usage show moderate correlations.*

---

## 3. Summary of Key Findings

### The "Parents' Education" Belief is Not Supported
- **No statistically significant difference** in exam scores across parent education groups (ANOVA p = 0.19, Kruskal-Wallis p = 0.10)
- The effect size is negligible (η² = 0.0036)
- The trend is **non-monotonic**: High School (69.3) < Bachelor (70.7) > Master (67.9), which contradicts the hypothesis

### Factors with the Largest Impact (Ranked)

| Factor                  | Impact    | Type of Influence |
|------------------------|-----------|-------------------|
| 1. Daily study time    | Very High | Positive          |
| 2. Mental health       | High      | Positive          |
| 3. Exercise frequency  | Moderate  | Positive          |
| 4. Social media usage  | Moderate  | Negative          |
| 5. Sleep duration      | Moderate  | Positive          |
| 6. Diet quality        | Weak      | Mixed             |
| 7. Attendance rate     | Weak      | Positive          |
| 8. Parents' education  | Negligible| Non-significant   |
| 9. Gender              | Negligible| Non-significant   |
| 10. Part-time job      | Negligible| Non-significant   |
| 11. Extracurriculars   | Negligible| Non-significant   |
| 12. Internet quality   | Negligible| Non-significant   |

### Practical Recommendations

1. **Increase daily study time** — this is the single most impactful factor a student can control
2. **Support mental health** — higher mental health scores are strongly linked to better performance
3. **Limit social media usage** — excessive use is associated with lower scores
4. **Maintain regular exercise and adequate sleep** — both modestly contribute to better outcomes
5. **Parents' education level** should not be considered a meaningful predictor of children's academic performance based on this dataset

## Limitations

- The data is cross-sectional, so causal conclusions cannot be drawn
- 89 records (8.9%) have missing parents' education level
- The regression model explains 85.5% of variance, leaving 14.5% unaccounted for by the measured factors
- The "Master" category (165 students) may have heterogeneous backgrounds not captured in the data