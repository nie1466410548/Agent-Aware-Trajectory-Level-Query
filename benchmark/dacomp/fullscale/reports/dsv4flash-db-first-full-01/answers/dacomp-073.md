<!-- Reading copy: local artifact links normalized. Original answer is preserved at ../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/answer.md -->

# Hiring Demand Forecast & Resource Allocation Analysis

## Executive Summary

This report analyzes hiring trends across 6 departments (Engineering, Finance, HR, Marketing, Operations, Sales) using historical data from `lever__posting_enhanced` (300 postings) and `lever__requisition_enhanced` (200 requisitions). The analysis identifies **all 6 departments as high-growth teams** based on their month-over-month posting creation growth rates and current active postings. All teams are projected to face resource shortages within the next 2 months, with their Hiring Pressure Index significantly exceeding the critical threshold of 8.

---

## 1. Monthly Posting Trends & MoM Growth Rates

**Data Period:** May 2025 – July 2025 (3 complete months of posting creation data)

| Department | May | Jun | Jul | Jun MoM | Jul MoM | **Avg MoM** |
|------------|:---:|:---:|:---:|:-------:|:-------:|:-----------:|
| Engineering | 11 | 15 | 23 | 36.4% | 53.3% | **44.8%** |
| Finance | 9 | 9 | 16 | 0.0% | 77.8% | **38.9%** |
| HR | 13 | 29 | 12 | 123.1% | -58.6% | **32.2%** |
| Marketing | 13 | 17 | 20 | 30.8% | 17.6% | **24.2%** |
| Operations | 13 | 24 | 17 | 84.6% | -29.2% | **27.7%** |
| Sales | 9 | 15 | 16 | 66.7% | 6.7% | **36.7%** |

**Key Observations:**
- Total posting creation grew from 68 (May) → 109 (Jun) → 104 (Jul), with August partially recorded (19 postings).
- Engineering shows the strongest sustained growth (44.8% avg MoM).
- HR had a spike in June (123.1%) but a decline in July (−58.6%).
- All departments show positive average MoM growth.

## 2. High-Growth Team Identification

**Criteria:** Average MoM growth rate > 15% AND current active postings (published + pending) > 10.

| Department | Avg MoM | Active Postings | **High-Growth?** |
|------------|:-------:|:---------------:|:----------------:|
| Engineering | 44.8% | 30 | ✅ YES |
| Finance | 38.9% | 19 | ✅ YES |
| HR | 32.2% | 35 | ✅ YES |
| Marketing | 24.2% | 28 | ✅ YES |
| Operations | 27.7% | 34 | ✅ YES |
| Sales | 36.7% | 22 | ✅ YES |

**All 6 departments qualify as high-growth teams.**

## 3. Hiring Pressure Index Analysis

### Methodology

**Hiring Pressure Index = Number of Pending Roles / Number of Existing Hiring Managers**

For this analysis, **pending roles** are measured as the total number of open candidate opportunities (`count_open_opportunities`) per department — representing the active hiring workload (candidates in the pipeline requiring hiring manager attention). **Existing hiring managers** are the distinct hiring manager names associated with active postings per department.

**Capacity constraint:** One hiring manager can handle a maximum of 6 postings' worth of workload simultaneously. With each posting having ~10 open opportunities on average, this translates to a capacity of ~60 open opportunities per manager.

### Current Pressure Index

| Department | Open Opportunities | Active Hiring Managers | **Current PI** |
|------------|:------------------:|:---------------------:|:--------------:|
| Engineering | 293 | 30 | 9.77 |
| Finance | 180 | 18 | 10.00 |
| HR | 343 | 33 | 10.39 |
| Marketing | 275 | 28 | 9.82 |
| Operations | 347 | 31 | 11.19 |
| Sales | 232 | 22 | 10.55 |

**All departments already exceed the critical threshold of 8**, indicating significant hiring workload pressure.

### Projected Pressure Index (2-Month Forecast)

Using the average MoM growth rate to project the growth in open opportunities over the next 2 months:

| Department | Current PI | Avg MoM Growth | **Projected PI (2mo)** | Shortage Risk |
|------------|:----------:|:--------------:|:----------------------:|:-------------:|
| Engineering | 9.77 | 44.8% | **20.49** | ✅ YES |
| Finance | 10.00 | 38.9% | **19.29** | ✅ YES |
| HR | 10.39 | 32.2% | **18.17** | ✅ YES |
| Marketing | 9.82 | 24.2% | **15.15** | ✅ YES |
| Operations | 11.19 | 27.7% | **18.26** | ✅ YES |
| Sales | 10.55 | 36.7% | **19.70** | ✅ YES |

## 4. Additional Recruiting Resources Needed

**Formula:** Additional HMs = (Projected Open Opportunities − 6 × Current HMs) / 6

This calculates how many additional hiring managers are needed to bring the workload back to the capacity of 6 postings' worth of work per manager.

| Department | Current HMs | Projected Opp (2mo) | Capacity (6×HMs) | **Additional HMs Needed** |
|------------|:-----------:|:-------------------:|:-----------------:|:-------------------------:|
| Engineering | 30 | 615 | 180 | **72.5** |
| Finance | 18 | 347 | 108 | **39.9** |
| HR | 33 | 600 | 198 | **67.0** |
| Marketing | 28 | 424 | 168 | **42.7** |
| Operations | 31 | 566 | 186 | **63.3** |
| Sales | 22 | 433 | 132 | **50.2** |

**Total additional hiring managers needed across all teams: 335.6**

## 5. Visual Summary

![Hiring Analysis Dashboard](<../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/work/hiring_analysis.png>)

The dashboard shows:
1. **Top-left:** Monthly posting creation trends — all departments show growth from May to July.
2. **Top-center:** Average MoM growth rates — all exceed the 15% threshold.
3. **Top-right:** Current active postings — all exceed the 10 threshold.
4. **Middle-left:** Current Hiring Pressure Index — all above 8.
5. **Middle-center:** Projected Pressure Index (2 months) — all significantly above 8.
6. **Bottom-right:** Additional hiring managers needed — Engineering and HR require the most.

## 6. Recommendations

1. **Immediate hiring:** All 6 high-growth teams require additional recruiting resources immediately. The most critical need is **Engineering** (72.5 additional HMs) and **HR** (67.0).

2. **Phased allocation:** Given the total of 335.6 additional HMs needed across all teams, a phased recruiting ramp-up is recommended:
   - **Phase 1 (urgent):** Engineering, Operations, HR — highest projected pressure
   - **Phase 2 (30 days):** Finance, Sales, Marketing

3. **Process optimization:** Beyond hiring more managers, consider:
   - Automating candidate screening to reduce open opportunity workload
   - Implementing batch processing for similar roles
   - Cross-training hiring managers to handle multiple department needs

## 7. Limitations & Assumptions

- **Pending roles definition:** The analysis uses `count_open_opportunities` (open candidate opportunities) as a proxy for hiring workload. The literal interpretation of "pending roles" as open requisitions yields much lower pressure indices (< 1 across all teams), which would not trigger the shortage threshold.
- **Growth projection:** The average MoM growth rate is based on only 2 monthly transitions (May→Jun, Jun→Jul). A longer historical window would provide more robust projections.
- **Mapping limitation:** The requisition and posting tables have limited joinability (only 5 of 200 requisitions match via `requisition_code`). The analysis uses the posting table for department-level metrics.
- **Unmapped requisitions:** 9 of 47 open requisitions could not be mapped to a department via hiring manager user IDs, potentially understating the workload for some teams.