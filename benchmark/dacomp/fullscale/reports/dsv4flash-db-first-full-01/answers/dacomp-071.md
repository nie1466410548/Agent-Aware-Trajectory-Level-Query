<!-- Reading copy: local artifact links normalized. Original answer is preserved at ../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/answer.md -->

# Hiring Funnel Bottleneck Analysis

## Objective
Identify hiring-funnel bottleneck stages where (a) **average time in stage > 25 days** and **attrition rate > 40%**, and (b) stages with an **efficiency index < 1.5** (defined as `pass_rate / avg_days * 100`), then provide improvement recommendations for stages with **≥ 100 samples**.

## Data & Methodology
- **Source**: `lever__opportunity_stage_history` — 8,019 stage-interval records for **3,000 candidates** across 10 stages (Application Review → Phone Screening → Technical Assessment → First Interview → Second Interview → Final Interview → Reference Check → Offer Discussion → Background Check → Hired, ordered by `stage_id` STAGE_01–STAGE_10).
- **Pass** at a stage = the candidate has a record at a *later* stage in the funnel (progression-based). **Attrition** at a stage = the stage is the candidate's furthest (terminal) stage (the Hired stage is a terminal-success outcome and is excluded from bottleneck classification).
- **avg_days** = mean `days_in_stage`; **attrition%** = attrited / entries; **efficiency index** = `pass_rate / avg_days * 100`.
- Progression was determined by stage order because `valid_from` timestamps in this dataset are not chronological.

## Stage-Level Results

| Stage | Entries | Avg Days | Pass % | Attrition % | Efficiency Index |
|---|---|---|---|---|---|
| Application Review | 3,000 | 5.9 | 65.4 | 34.6 | 11.05 |
| Phone Screening | 1,962 | 9.1 | 68.4 | 31.6 | 7.50 |
| **Technical Assessment** | **1,342** | **44.1** | **57.2** | **42.8** | **1.30** |
| First Interview | 768 | 16.1 | 59.9 | 40.1 | 3.72 |
| Second Interview | 460 | 19.6 | 48.7 | 51.3 | 2.49 |
| **Final Interview** | **224** | **42.3** | **37.1** | **62.9** | **0.88** |
| Reference Check | 83 | 63.5 | 89.2 | 10.8 | 1.40 |
| Offer Discussion | 74 | 38.5 | 74.3 | 25.7 | 1.93 |
| Background Check | 55 | 39.3 | 92.7 | 7.3 | 2.36 |
| Hired (terminal) | 51 | 49.9 | — | — | — |

## 1. Key Bottleneck Stages (avg days > 25 **AND** attrition > 40%)

Two stages meet both criteria and are confirmed bottlenecks:

### ⚠️ Technical Assessment — avg 44.1 days, attrition 42.8%
- Highest volume bottleneck (1,342 candidates; 42.8% never advance). Median dwell time 44 days; 25th–75th percentile spans 29–55 days (up to 123 days for some).
- **Attrition drivers** (574 terminal exits): *Failed technical assessment* 54.7%, *Technical skills insufficient* 34.5%, *Coding challenge failed* 8.9% → **~98% of losses are skills/assessment-related**.

### ⚠️ Final Interview — avg 42.3 days, attrition 62.9%
- Worst attrition in the funnel: only 37.1% of candidates advance. Median dwell 39 days; 25th–75th percentile 32–50 days.
- **Attrition drivers** (141 terminal exits): *Cultural fit concerns* 67.4%, *Interview performance below expectations* 24.8%, *Better candidate selected* 7.1%.

## 2. Efficiency Index Below 1.5 (with ≥ 100 samples)

| Stage | Samples | Avg Days | Attrition % | Efficiency Index |
|---|---|---|---|---|
| **Technical Assessment** | 1,342 | 44.1 | 42.8 | **1.30** |
| **Final Interview** | 224 | 42.3 | 62.9 | **0.88** |

Both bottleneck stages also have efficiency indexes below 1.5. (Reference Check also scores 1.40 and Hired 0.00, but each has < 100 samples and are excluded from recommendations per the task rule.)

## 3. Improvement Recommendations (based on ≥ 100-sample stage data)

### Technical Assessment (n = 1,342)
1. **Move skill screening earlier** — verify core technical/coding prerequisites during Phone Screening (avg 9 days) so unqualified candidates are rejected before the slow, ~44-day assessment stage.
2. **Sharpen job requirements** — publish explicit skill/experience criteria so candidates self-select; this is cheap and can reduce the ~49% team-level attrition seen for Marketing (49.2%) and Engineering (45.2%).
3. **Calibrate assessment difficulty** — 54.7% of exits are "Failed technical assessment"; review test calibration against the role level and retire questions with near-zero pass rates.
4. **Cap turnaround time** — enforce a hard SLA (e.g., ≤ 3 weeks) for assessment scheduling/grading; automate rubric-based grading and parallel-test windows to cut the 44-day dwell time.
5. **Offer practice materials** — reduce "unfamiliarity" failures (8.9% "Coding challenge failed") with sample tests.

### Final Interview (n = 224)
1. **Institutionalize structured, scorecard-based interviews** — 67.4% of dropouts are "Cultural fit concerns," which is highly subjective; use standard questions + scoring rubrics and require documented evidence.
2. **Clarify culture/fit expectations upstream** — communicate values and work-style expectations in postings and early interviews so candidates self-filter earlier (Data 77.3%, Marketing 69.4%, Sales 68.4% are the highest attrition teams).
3. **Train and calibrate interviewers** — reduce "Interview performance below expectations" (24.8%) noise by training hiring managers on consistent, bias-aware evaluation.
4. **Speed up final-round logistics** — compress the 42-day final-round cycle (schedule panel rounds in a single day, define decision SLAs) to shorten time-to-hire.
5. **Reduce competition-driven losses** — "Better candidate selected" (7.1%) suggests improving speed-to-decision so strong candidates aren't lost to competing offers.

## Additional Observations
- **Second Interview** (attrition 51.3%) narrowly misses the time criterion (19.6 days < 25) but is a high-attrition mid-funnel stage worth monitoring.
- **Reference Check** has the longest average dwell time (63.5 days) but low attrition (10.8%); it is a *time* bottleneck, not an attrition bottleneck.
- No strong team or application-source pattern explains the long dwell times (avg days are uniform at 39–46 days across teams), so the delay is process-wide, not team-specific.

## Limitations
- **Archive-reason field is partially unreliable**: 899 records (11.2%) carry a negative `archive_reason` (e.g., "Failed technical assessment") yet the candidate still appears at a later stage (763 of these at Technical Assessment). Pass/attrition were therefore computed from **stage progression** rather than the `archive_reason` text; the reason text was used only to describe *why* terminal dropouts occur.
- Stages with < 100 samples (Reference Check, Offer Discussion, Background Check, Hired) have less reliable rate estimates and were excluded from recommendation targets.
- `valid_from` timestamps are not chronological, so time-in-funnel was measured via the explicit `days_in_stage` column.

## Figures
- `stage_bottleneck_analysis.png` — per-stage avg days, attrition %, and efficiency index vs. thresholds.
- `funnel_visualization.png` — candidate funnel with bottleneck stages highlighted.
