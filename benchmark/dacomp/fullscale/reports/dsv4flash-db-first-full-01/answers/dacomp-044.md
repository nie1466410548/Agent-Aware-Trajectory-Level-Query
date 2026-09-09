<!-- Reading copy: local artifact links normalized. Original answer is preserved at ../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/answer.md -->

# Health Education Campaign Formats & Locations for Students with Long-Term Effectiveness and Behavioral Improvement

## 1. Objective and Data Scope

The task asks which health education campaign **formats** (Poster/Video/Lecture) and **locations** (School/Hospital/Community) for **students** deliver **long-term effectiveness** and **behavioral improvement**. The `health_education` table contains 400 campaigns, of which **75 (18.8%) explicitly target students** (`Population Covered = 'Student'`). Each campaign is rated (Weak/Average/Significant) on:

- **Behavioral Change Assessment** → proxy for behavioral improvement
- **Effectiveness Tracking** → proxy for long-term, sustained effectiveness
- **Effectiveness Assessment** → overall effectiveness rating

A campaign was classified as delivering both outcomes when **Behavioral Change Assessment = Significant AND Effectiveness Tracking = Significant** (7 of 75 student campaigns, 9.3%). An alternative definition using `Effectiveness Assessment` yielded similar conclusions (12.0%).

## 2. Student Campaign Landscape

| Format | Campaigns | Location | Campaigns |
|--------|-----------|----------|-----------|
| Lecture | 37 | School | 29 |
| Video | 25 | Community | 26 |
| Poster | 13 | Hospital | 20 |

Overall student outcome rates: 24/75 (32.0%) achieved significant behavioral change; 26/75 (34.7%) achieved significant effectiveness tracking; 7/75 (9.3%) achieved both.

## 3. Formats Capable of Delivering Both Long-Term Effectiveness and Behavioral Improvement

| Format | n | Both Significant | Rate |
|--------|---|------------------|------|
| **Poster** | 13 | 3 | **23.1%** |
| Video | 25 | 2 | 8.0% |
| Lecture | 37 | 2 | 5.4% |

**Poster campaigns show the highest rate** of combined behavioral change + long-term tracking (23.1%, 3× the rate of the other formats), despite being the least-used format for students.

## 4. Locations Capable of Delivering Both Outcomes

| Location | n | Both Significant | Rate |
|----------|---|------------------|------|
| **Community** | 26 | 4 | **15.4%** |
| School | 29 | 2 | 6.9% |
| Hospital | 20 | 1 | 5.0% |

**Community-based delivery yields the highest rate** of combined long-term effectiveness and behavioral improvement (15.4%), followed by school and hospital settings.

## 5. Best Format × Location Combinations

| Rank | Format @ Location | n | Behavioral Change | Tracking | Both | Both Rate |
|------|-------------------|---|-------------------|----------|------|-----------|
| 1 | **Poster @ Community** | 6 | 50.0% | 66.7% | 2 | **33.3%** |
| 2 | Poster @ Hospital | 2 | 50.0% | 50.0% | 1 | 50.0%* |
| 3 | **Video @ School** | 16 | 37.5% | 43.8% | 2 | **12.5%** |
| 4 | **Lecture @ Community** | 17 | 29.4% | 29.4% | 2 | **11.8%** |

*Poster @ Hospital has a 50% rate but only 2 campaigns (unreliable estimate).

**Most robust performers** (balancing rate and sample volume):
1. **Poster @ Community** – highest combined success rate (33.3%) with the top tracking rate (66.7%) and behavioral change rate (50.0%);
2. **Video @ School** – the highest-volume Video segment (n=16) with 12.5% combined success, 37.5% behavioral change and 43.8% tracking;
3. **Lecture @ Community** – highest overall Effectiveness Assessment (47.1%) among high-volume combos.

![Student effectiveness heatmaps](<../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/work/student_effectiveness_heatmap.png>)

![Student campaign effectiveness by format & location](<../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/work/student_detailed_bar.png>)

![Student campaign bubble chart](<../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/work/student_bubble_chart.png>)

## 6. Content and Supporting Factors

- **Treatment-oriented content** dominated the combined-success campaigns (5 of 7, 71.4%), suggesting prevention/treatment messages delivered via posters in community settings and videos in schools are most effective.
- Combined-success campaigns had **significantly higher knowledge-assessment scores** (mean 89.1% vs. 80.7%, Welch t-test p = 0.043), i.e., stronger knowledge gain accompanies behavioral improvement and sustained tracking.
- Awareness rates, distribution quantities, campaign frequency (~4–5 times/month), and new-media views were comparable between successful and unsuccessful campaigns (all p > 0.25).

## 7. Comparison with Non-Student Populations

Non-student campaigns achieve combined success at a higher overall rate (46/325 = 14.2%) than student campaigns (7/75 = 9.3%). Notably, for non-students **Lecture is the top-performing format** (≈19–20% combined success), whereas for students **Poster** takes the lead — indicating that format effectiveness is audience-specific.

## 8. Recommendations

For student-targeted health education designed to deliver **long-term effectiveness and behavioral improvement**:
- **Use Poster campaigns, delivered in Community settings**, as the primary strategy (33.3% combined success; 66.7% long-term tracking; 50% behavioral change).
- **Supplement with Video campaigns in School settings** for reach and scale (12.5% combined success, 43.8% tracking among the largest student video segment).
- **Prefer treatment-related messaging** and reinforce with high-quality knowledge-assessment materials, which were significantly associated with combined success.

## 9. Limitations

- Small cell sizes (e.g., Poster @ Hospital n=2, Video @ Community n=3) make rate-based rankings in those cells statistically fragile; chi-square tests found no significant association between format/location and outcomes (all p > 0.37).
- Outcomes rely on categorical self-reported ratings (Weak/Average/Significant) rather than measured long-term behavioral data.
- The database does not link these campaigns to individual student cases (basic_medical_record), so campaign-level aggregation on `Population Covered = 'Student'` is the only available linkage.
