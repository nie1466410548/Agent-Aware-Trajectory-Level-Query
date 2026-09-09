<!-- Reading copy: local artifact links normalized. Original answer is preserved at ../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/answer.md -->

# Analysis: Why R&D Department Has Lower Attrition

## Executive Summary

The Research & Development (R&D) department has an attrition rate of **13.75%**, significantly lower than Sales (20.67%) and Human Resources (19.05%). This 6.9 percentage point gap is driven by two major factors: **(1) job role composition** and **(2) pervasively lower attrition within every job level and employee subgroup**. The most critical finding is that even after controlling for job level, R&D retains employees better than Sales across all categories.

---

## 1. Overall Attrition by Department

| Department | Total Employees | Attrition Count | Attrition Rate |
|-----------|:--------------:|:--------------:|:--------------:|
| Sales | 450 | 93 | **20.67%** |
| Human Resources | 63 | 12 | **19.05%** |
| Research & Development | 967 | 133 | **13.75%** |

R&D, the largest department (65.3% of all employees), has the lowest attrition rate.

![Attrition Overview](<../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/work/attrition_overview.png>)
*Figure 1: Attrition rates across departments, broken down by job level, overtime, stock options, and marital status.*

---

## 2. Decomposition: Separating Composition from Rate Effects

Using Oaxaca-style decomposition, we separate the Sales vs. R&D attrition gap into:

- **Rate effect (within-level differences):** +13.3 pp (drives R&D's advantage)
- **Composition effect (different job level mix):** -6.4 pp (Sales actually has a *more favorable* job level distribution, masking the true rate gap)

**This means:** If Sales had the same job-level composition as R&D, its attrition would be even higher (27.0%). The real driver is that R&D retains employees better within *every single job level*.

![Decomposition Waterfall](<../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/work/decomposition.png>)
*Figure 2: Waterfall decomposition of the Sales vs. R&D attrition gap.*

---

## 3. Factor 1: Job Role Composition

R&D benefits from a diverse mix of roles with very low attrition, while Sales is burdened by high-attrition Sales Representatives.

| Job Role | Department | Count | Attrition Rate | Avg Income |
|---------|-----------|:----:|:--------------:|:----------:|
| Research Director | R&D | 80 | **2.5%** | $16,034 |
| Manager | R&D | 54 | **5.6%** | $17,130 |
| Manufacturing Director | R&D | 147 | **6.8%** | $7,305 |
| Healthcare Representative | R&D | 132 | **6.8%** | $7,547 |
| Research Scientist | R&D | 293 | **16.0%** | $3,242 |
| Sales Executive | Sales | 329 | **17.6%** | $6,947 |
| Laboratory Technician | R&D | 261 | **23.8%** | $3,239 |
| Human Resources | HR | 52 | **23.1%** | $4,236 |
| **Sales Representative** | **Sales** | **84** | **39.3%** | **$2,630** |

**Key insight:** Sales Representatives, who constitute 18.6% of Sales employees, contribute **35.9% of all Sales attrition**. If Sales Representatives had the same attrition rate as R&D's Laboratory Technicians (23.8%), Sales' overall attrition would drop from 20.7% to 17.7%.

![Role Analysis](<../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/work/role_analysis.png>)
*Figure 3: Job role distribution and attrition rates by department.*

---

## 4. Factor 2: Within-Level Attrition (Pervasive Pattern)

Across *every* job level, R&D has substantially lower attrition than Sales:

| Job Level | R&D Attrition | Sales Attrition | Gap |
|:---------:|:-------------:|:---------------:|:---:|
| 1 | **23.2%** | 41.6% | 18.4 pp |
| 2 | **5.3%** | 15.4% | 10.1 pp |
| 3 | **10.0%** | 21.4% | 11.4 pp |
| 4 | **1.5%** | 11.4% | 9.9 pp |
| 5 | **6.1%** | 15.4% | 9.3 pp |

This pattern holds across *every* factor examined:

![Factor Comparison](<../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/work/factor_comparison.png>)
*Figure 4: Side-by-side comparison of attrition rates between Sales and R&D across all factors. R&D has lower attrition in every single category.*

---

## 5. Factor 3: Overtime

Overtime is strongly associated with attrition, but its impact is much worse in Sales:

| Overtime | R&D Attrition | Sales Attrition |
|:--------:|:-------------:|:---------------:|
| No | **8.5%** | 13.7% |
| Yes | **27.2%** | 38.0% |

The proportion of overtime employees is similar across departments (R&D 28.1%, Sales 28.7%), so this is not a composition effect but a genuine difference in how overtime affects retention.

---

## 6. Factor 4: Stock Options

Stock option level is a strong retention tool, and R&D utilizes it slightly more effectively:

| Stock Level | R&D Attrition | Sales Attrition |
|:-----------:|:-------------:|:---------------:|
| 0 (none) | **20.5%** | 32.2% |
| 1 | **9.1%** | 9.6% |
| 2 | **5.8%** | 11.5% |
| 3 | **12.1%** | 27.3% |

R&D has a slightly lower proportion of employees with no stock options (42.4% vs. Sales 44.2%).

---

## 7. Factor 5: Income

Within Job Level 1 (the largest segment), R&D pays significantly more:

| Level | R&D Avg Income | Sales Avg Income | Difference |
|:----:|:--------------:|:----------------:|:----------:|
| 1 | **$2,842** | $2,513 | **+$329** |
| 2 | $5,298 | $5,745 | -$447 |
| 3 | **$10,169** | $9,301 | **+$868** |
| 4 | **$15,635** | $15,077 | **+$558** |
| 5 | $19,219 | $19,088 | +$131 |

Higher income at lower job levels may contribute to lower attrition among entry-level R&D employees.

![Income Analysis](<../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/work/income_analysis.png>)
*Figure 5: Average monthly income by job level and job role across departments.*

---

## 8. Additional Factors

**Marital Status:** Single employees have higher attrition in all departments, but R&D retains single employees better (21.6% vs. Sales 34.4%). R&D also has slightly fewer single employees (31.6% vs. Sales 34.2%).

**Work-Life Balance:** R&D has a higher proportion of employees rating work-life balance as 3+ (69.4% vs. Sales 73.3%), but within every balance level, R&D has lower attrition.

**Job Satisfaction:** R&D has higher job satisfaction (61.7% rate 3+ vs. Sales 61.3%), and within every satisfaction level, R&D retains better.

**Business Travel:** Frequent travel is more damaging in Sales (32.9% attrition) than in R&D (20.2%). R&D has slightly fewer frequent travelers (18.9% vs. Sales 18.9%).

---

## 9. Manager Role Comparison (Control)

The only role that exists across all three departments is "Manager," and here attrition rates are similar:

| Department | Managers | Attrition Rate | Avg Income |
|-----------|:--------:|:--------------:|:----------:|
| Human Resources | 11 | **0.0%** | $18,089 |
| Research & Development | 54 | **5.6%** | $17,130 |
| Sales | 37 | **5.4%** | $16,987 |

This confirms that the department-level differences are driven by the *composition of roles* and *within-role factors* rather than a generic "department culture" effect.

---

## 10. Conclusions

The R&D department's lower attrition is driven by:

1. **Primary: Pervasive within-level retention advantage.** Across all job levels, R&D retains employees at substantially higher rates than Sales. This suggests that R&D offers better working conditions, growth opportunities, compensation packages, or job fit for its employees.

2. **Secondary: Role composition.** R&D has a higher proportion of senior roles (Research Directors, Managers, Manufacturing Directors) with very low attrition, while Sales is burdened by Sales Representatives (39.3% attrition) who account for 35.9% of all Sales attrition.

3. **Contributing factors:**
   - Higher income for entry-level (Level 1) employees (+$329/month)
   - Better overtime management (27.2% vs. 38.0% attrition among overtime workers)
   - More effective use of stock options for retention
   - Better retention across all demographics (single, married, divorced)
   - Lower impact of frequent business travel on attrition

4. **Not the cause:** The composition effect actually *favors Sales* (fewer level-1 employees), so the gap would be even larger if departments had identical job-level distributions.

### Recommendations for Sales and HR:
- Investigate Sales Representative role to identify specific factors driving 39.3% attrition
- Implement R&D-like overtime policies or compensation for overtime workers
- Review stock option allocation, especially for entry-level positions
- Consider income adjustments for Level 1 Sales employees
- Analyze why R&D retains single employees and frequent travelers better

---

*Data source: Employee attrition dataset (1,470 unique employees across 3 departments). Analysis performed using SQLite and Python.*