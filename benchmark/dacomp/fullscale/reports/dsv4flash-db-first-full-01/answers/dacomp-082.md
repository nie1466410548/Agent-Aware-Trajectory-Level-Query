<!-- Reading copy: local artifact links normalized. Original answer is preserved at ../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/answer.md -->

# Channel Effectiveness & ROI Reallocation Analysis

## Executive Summary

Traditional channel evaluation based solely on `completion_rate` and `efficiency_score` fails to capture (1) *which project categories* each channel serves well, and (2) *the quality of the user base* each channel reaches. This analysis integrates three data sources — `qualtrics__channel_performance` (channel metrics), `qualtrics__survey` (project-type / category response mix), and `qualtrics__contact` (user lifecycle value, LTV) — to build a composite ROI model and a data-driven budget reallocation plan.

**Headline recommendation:** shift budget from **mobile** (−8.2 pts) and **email** (−4.7 pts) into **SMS** (+12.0 pts), hold **web** near-flat, and cap **social** at a minimum experimental floor. The optimized portfolio is forecast to increase completed responses by **≈ +3.3%** (from 1,653 to ≈1,708) with no additional spend, while concentrating investment on channels that reach higher-lifecycle-value users.

---

## 1. Channel Performance Baseline

![Channel profile](<../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/work/fig_final_1_channel_profile.png>)

| Channel | Tier | Completion Rate | Efficiency Score | Current Share | User LTV Factor | Category Robustness |
|---|---|---|---|---|---|---|
| email | Tier 1 – Premium | 50.5% (rank 2) | **73.0 (rank 1)** | 35% | 1.04 | 0.96 |
| sms | Tier 1 – Premium | **52.3% (rank 1)** | 60.1 (rank 3) | 25% | **1.17** | 0.91 |
| web | Tier 2 – Standard | 41.3% | 63.7 (rank 2) | 22% | 0.98 | **0.96** |
| mobile | Tier 2 – Standard | **31.6% (rank 5)** | 46.6 (rank 4) | 18% | **0.61** | 0.96 |
| social | Tier 3 – Experimental | 43.7% | 41.9 (rank 5) | 8% | 1.11 | **0.09** |

Key observations:
- **Email** is the most efficient channel (top efficiency score) and delivers consistent completion across all categories, but its marginal return per budget point is lower than SMS.
- **SMS** posts the highest completion rate, reaches the **highest-LTV users** (LTV factor 1.17), and has the highest yield (≈22.1 completed responses per 1% budget share vs 17.4 for email).
- **Mobile** is the weakest link: lowest completion, lowest efficiency, and reaches the lowest-value users (LTV factor 0.61) — a strong case for downsizing.
- **Social** reaches decent users but is extremely inconsistent across categories (robustness 0.09), confirming its experimental status.

---

## 2. Performance by Project Category (feedback / research / evaluation)

![Category analysis](<../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/work/fig_final_2_category.png>)

Completion rate by channel × project_category (derived from `qualtrics__survey`):

| Channel | Evaluation | Feedback | Research | Dominant category mix |
|---|---|---|---|---|
| email | 57.8% | 60.7% | **63.9%** | Research (60.7% of email responses) |
| sms | **52.7%** | 42.5% | 49.1% | Evaluation (52.8%) |
| web | 41.0% | 37.9% | 37.8% | Feedback (50.8%) |
| mobile | 41.0% | 37.9% | 37.8% | Feedback (50.8%) |
| social | 16.7% | **1.2%** | 4.2% | Evaluation (50.7%) |

**Channel–category fit findings:**
- **Email** is the category-agnostic workhorse — highest completion in *research* (63.9%) and strong in *feedback* (60.7%) and *evaluation* (57.8%). It should anchor research/feedback programs.
- **SMS** is the clear winner for **evaluation** projects (52.7% completion; 52.8% of its volume is evaluation), but its completion drops to 42.5% on feedback surveys — a category-level weakness worth monitoring.
- **Web/Mobile** serve the **feedback** category (50.8% of their combined volume) at a moderate ~38–41% completion rate.
- **Social** is structurally unsuited for formal research/feedback (1.2–4.2% completion), which justifies keeping it at a minimal experimental allocation.

---

## 3. User Lifecycle Value & Cohort Analysis

![Cohorts](<../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/work/fig_final_3_cohorts.png>)

![Contact analysis](<../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/work/fig_final_6_contact.png>)

From the 4,000 contacts in `qualtrics__contact` (14,076 total completed surveys):

**Value is highly concentrated.** The top lifecycle-value quartile (Q4) contributes **81.2% of total LTV**; the bottom quartile contributes ~0%.

| Cohort | All Users | Email-Reached | SMS-Reached |
|---|---|---|---|
| Q1 (bottom) | 0.0% | 0.0% | 0.0% |
| Q2 | 0.5% | 1.0% | 3.0% |
| Q3 | 18.3% | 19.1% | 20.9% |
| **Q4 (top)** | **81.2%** | **79.9%** | **76.1%** |

**Channel reach quality:**
- **SMS-reached users** have higher average LTV (4.12 completed surveys) than email-reached users (3.66) and the all-user average (3.52).
- **Multi-channel users (email + SMS)** are 4.2× more valuable (avg LTV 4.23) than single-channel users (0.14–0.15) — 82.7% of contacts engage with both channels.
- **Per-contact funnel** (contact table): SMS outperforms email at every stage — open rate 66.7% vs 64.6%, start rate 43.2% vs 36.6%, completion rate 15.2% vs 11.6%. SMS is therefore more effective at *converting* reach into completed responses.

**Implication:** budget should be shifted toward channels that (a) reach high-LTV cohorts and (b) drive completion — both point to SMS.

---

## 4. Channel ROI Model & Optimal Investment Ratios

**Model construction.** Each channel is scored on four normalized dimensions:
1. **Efficiency** (efficiency_score) — cost-effectiveness of the channel.
2. **Completion** (completion_rate).
3. **User lifecycle value** — average LTV of users reached via the channel (contact table), relative to the all-user baseline; progress-rate proxy for web/mobile.
4. **Category robustness** — 1 − CV of completion rates across evaluation/feedback/research (survey table), penalizing channels that collapse in some categories (social).

The composite score is blended with **yield** (completed responses per 1% budget share) to avoid allocating to metrics alone, then normalized to an investment ratio with tier-based floors (min 5% for Standard tiers, 3% for Experimental).

**Sensitivity check** across 5 weighting scenarios (balanced, efficiency-, user-value-, completion-weighted, and pure-yield) produced a consistent allocation (SMS 36–40%, email 29–31%, web 18–21%, mobile 9–11%, social 3%), confirming the plan is robust to model specification.

![Reallocation](<../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/work/fig_final_4_reallocation.png>)

### Recommended investment ratio (current → optimal)

| Channel | Current Budget | **Optimal Investment Ratio** | Δ (points) | Rationale |
|---|---|---|---|---|
| sms | 25.0% | **37.0%** | **+12.0** | Highest yield & completion; reaches highest-LTV users; best for evaluation |
| email | 35.0% | **30.3%** | −4.7 | Most efficient & consistent, but lower marginal yield; still the anchor channel |
| web | 22.0% | **20.0%** | −2.0 | Moderate, stable performer in feedback; slight trim |
| mobile | 18.0% | **9.8%** | −8.2 | Weakest completion, efficiency, and user value |
| social | 8.0% | **3.0%** | −5.0 | Held at experimental floor; poor category completion |
| **Total** | 100% | 100% | — | — |

---

## 5. Forecast of Expected Returns

![Forecast](<../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/work/fig_final_5_forecast.png>)

Using per-channel yield (completed responses per 1% of budget) held constant at the reallocated shares:

| Channel | Current Completed | Forecast Completed | Change |
|---|---|---|---|
| email | 610 | 528 | −82 |
| sms | 552 | **817** | **+265** |
| web | 280 | 255 | −26 |
| mobile | 171 | 93 | −78 |
| social | 40 | 15 | −25 |
| **Portfolio** | **1,653** | **≈1,708** | **+55 (+3.3%)** |

- **Portfolio-level uplift:** +3.3% completed responses at constant spend — i.e., the reallocation captures incremental value purely by re-weighting the mix.
- SMS alone is expected to generate +265 additional completed responses, more than offsetting reductions from lower-yield channels.
- In the conservative case that applies diminishing returns (20% log decay on yield for increased shares), the plan is still approximately break-even on volume while improving user-value mix — the downside is bounded.

---

## 6. Actionable Recommendations

1. **Shift ~12 pts into SMS** — the highest-ROI channel by completion, per-contact funnel, and user LTV. Prioritize SMS for **evaluation** programs (52.8% natural fit, 52.7% completion).
2. **Keep email as the strategic anchor (≈30%)** — its category-consistency (57–64% everywhere) makes it the default for **research** and **feedback**; cut only the low-marginal-yield portion.
3. **Hold web at ~20%** for feedback delivery; it is a stable, moderate-cost channel.
4. **Cut mobile from 18% → ~10%** and re-evaluate: lowest completion (31.6%), efficiency, and user value across all channels.
5. **Cap social at 3%** experimental spend; its near-zero feedback/research completion (1.2%/4.2%) does not justify current 8%.
6. **Invest in multi-channel engagement** (email + SMS): users on both channels are 4.2× more valuable — cross-channel activation is a higher-leverage lever than any single-channel spend.
7. **Protect the Q4 cohort** (81% of LTV) with retention targeting; lifetime-value concentration means churn in the top quartile would outweigh any channel-level gain.

---

## 7. Limitations

- **No explicit cost data** exists in the schema; budget share is proxied by `market_share`, and cost is implicitly captured via `efficiency_score` and response yield. Actual media/unit costs would refine absolute ROI figures.
- **Contact-level data is available only for email and SMS**; web/mobile/social LTV factors were proxied from survey progress/performance rather than measured directly.
- **Channel identity mapping** is approximate: the survey table records email/SMS/social-media/uncategorized response counts, and the `web`+`mobile` channels were mapped to the survey "uncategorized" bucket for category-level completion.
- The forecast assumes per-point yield is stable; a diminishing-returns variant was tested and remains roughly break-even, bounding downside risk.
- Figures referenced are saved under `work/` in the workspace.
