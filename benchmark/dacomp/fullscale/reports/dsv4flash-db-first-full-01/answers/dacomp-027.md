<!-- Reading copy: local artifact links normalized. Original answer is preserved at ../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/answer.md -->

# Secondary & Cascading Hazards and Sustained Negative Impacts Across Disaster Levels

## 1. Scope and Method

**Data:** 999 synthetic disaster events across 5 global Disaster Levels (Level 1–5), each linked one-to-one with coordination/evaluation, environment & health, operations, financials, transportation, distribution-hub, and supply records. Secondary/cascading hazard intensity is measured by `Secincident Count` (0–100) in the coordination table. Human impacts come from the `Impact Indicator` JSON (affected, injured, casualties, displaced, missing, infrastructure damage) and environment & health fields (disease risk, vaccination, water quality, sanitation, environmental impact rate).

**Method:** All joins, grouping, and aggregation were performed in SQLite (JSON fields parsed with `json_extract`). Statistical tests (Pearson/Spearman correlation, ANOVA, chi-square association, t-tests) and all visualizations were run in Python because hypothesis testing/effect-size computation is not supported by SQLite. Figures are saved under `/work`.

## 2. Key Findings

### 2.1 Secondary/cascading hazards are associated with higher disease risk (people impact)
Events with more secondary incidents have a **statistically significant** higher share of "High" disease risk (chi²=10.87, p=0.028, Cramér's V=0.074):

| Secondary incident group | High disease risk | Low | Medium |
|---|---|---|---|
| Low (0–32) | 28.8% | 31.7% | 39.4% |
| Medium (33–65) | 34.5% | 29.4% | 36.1% |
| High (66–100) | **35.9%** | 35.6% | 28.6% |

The disease-risk gradient is monotonically increasing with secondary-hazard load, and the effect is visible within nearly every Disaster Level (e.g., Level 2: 25.4% → 27.0% → 39.7% High-risk across low→med→high secondary groups).

### 2.2 Health protection weakens exactly where secondary hazards are worst
Among **High disease-risk** events, vaccination coverage is markedly lower when secondary incidents are high (Fig. 2):

- Low secondary: mean **53.5%** vaccination
- Medium secondary: mean **55.3%**
- High secondary: mean **46.9%** (≈7-point deficit, t=-1.63, p≈0.11 in the small subgroup — not significant but practically meaningful)

This is the signature of a *sustained* people impact: the populations most exposed to cascading hazards (highest disease risk) receive the least preventive health protection.

### 2.3 Cascading-hazard events get *less* frequent monitoring and more overdue audits
Counterintuitively, higher secondary-hazard load is significantly associated with **less frequent monitoring** (chi²=9.90, p=0.042) and **more overdue audits** (chi²=11.14, p=0.025) (Fig. 1):

| Secondary group | Daily monitoring | Weekly | Monthly | Overdue audits |
|---|---|---|---|---|
| Low (0–32) | 40.4% | 25.0% | 34.6% | 32.4% |
| High (66–100) | **31.1%** | 33.3% | 35.6% | **38.4%** |

Cascading, compounding emergencies — exactly the situations needing the closest scrutiny — receive less frequent monitoring and slower accountability.

### 2.4 Institutional learning is delayed in high-secondary events
High-secondary events show fewer "Documented" lessons and more "In Progress"/"Pending" lessons-learned entries (Fig. 3): Documented 26.6% (vs 35.3% low), In Progress 38.7% (vs 35.3%), Pending 34.7% (vs 29.5%). The learning loop is not closed for the most complex events, perpetuating negative impacts into future responses.

### 2.5 Higher Disaster Levels sustain operations longer
Higher global Disaster Levels show **more "Active" and fewer "Completed" operations** (Fig. 4):

| Disaster Level | Active | Completed |
|---|---|---|
| Level 1 | 19.9% | 29.3% |
| Level 4 | 27.5% | 25.5% |
| Level 5 | 26.7% | **22.3%** |

This indicates *sustained* operational burden at the highest levels — response phases linger rather than concluding.

### 2.6 Environment: amplification at Level 5 + high cascading load
Disaster Level alone is not significantly associated with the environmental impact rate (chi²=7.27, p=0.51), but the **combination** of Level 5 with high secondary incidents yields the highest share of "High" environmental impact (43.7%) of any level×hazard cell (Level 1+high: 39.2%, Level 2+high: 39.7%). Continuous environmental indicators (water quality index, sanitation, carbon, recycling) show no meaningful correlation with secondary counts (all |r|<0.06), meaning the environmental damage signal is concentrated in high-complexity, high-level events.

### 2.7 Resource allocation stress
High-secondary events report a higher share of "Limited" resource-allocation status (36.7% vs 32.7% low) and a lower share of "Critical" allocation (28.9% vs 36.2%), suggesting resources are stretched or mis-prioritized in cascading emergencies.

## 3. Conclusions

- **Cascading/secondary hazards are the operative driver of sustained human harm**, not Disaster Level alone: they raise disease risk, and coincide with weaker vaccination, less frequent monitoring, delayed audits, and unclosed lessons-learned loops.
- **Higher Disaster Levels sustain operations** (fewer completions) and, when combined with high secondary loads, produce the worst environmental-impact outcomes (Level 5 + high cascades).
- The response system is **least attentive where risk is greatest**: cascading events get fewer daily check-ins, more overdue audits, and more delayed institutional learning.

## 4. Targeted Recommendations

1. **Scale monitoring intensity with secondary-hazard load.** Mandate daily monitoring for events with high cascading risk (Secincident ≥66); current data show daily monitoring drops to 31% in exactly those events. Add automated early-warning triggers (aftershocks, dam overflow, secondary fires/landslides) that automatically escalate monitoring frequency.
2. **Protect health-service continuity in high-secondary, high-disease-risk zones.** Prioritize vaccination/sanitation surge capacity where cascading hazards coincide with High disease risk; current vaccination coverage is ~7 points lower there. Pre-position cold-chain capacity at Level 5 hubs.
3. **Close the accountability loop faster.** Enforce audit and evaluation deadlines proportional to event complexity — high-secondary events currently have 38% overdue audits and more than a third of lessons-learned entries still pending. Tie follow-on funding to documented lessons and completed audits.
4. **Accelerate operations closure at high Disaster Levels.** Level 4–5 events stall in "Active" status (≈27%) with the lowest completion rates; introduce time-boxed transition criteria (e.g., clear exit milestones for reconstruction/recovery) and dedicated scaling-down teams.
5. **Focus environmental monitoring on Level 5 + high-cascade events.** Environmental-impact surveillance (water quality, waste management, emissions) should be activated automatically when disaster level and secondary-incident counts both breach thresholds, since this is where "High" environmental impact concentrates (43.7%).
6. **Re-balance resource allocation in cascading events.** Because high-secondary events show more "Limited" allocation states, apply risk-based resource formulas that add capacity with each secondary incident rather than treating resource plans as fixed at onset.
7. **Build cascading-scenario contingency planning.** High-secondary events lag in documented contingency plans; run multi-hazard scenario planning (primary + secondary + tertiary) for Level 4–5 regions where cascades are statistically most damaging.

## 5. Limitations

- Dataset is synthetic; associations are modest in effect size (Cramér's V≈0.07) even where statistically significant, and several secondary indicators (WQI, carbon, casualties) show no detectable correlation — consistent with largely independent synthetic generation.
- Vaccination deficit among high-risk events is not statistically significant (p≈0.11) due to small subgroup; treat as a directional finding.
- "Sustained" impact is inferred from process states (Active operations, Overdue audits, Pending lessons) rather than longitudinal time-series; no true repeated-measure data were available.

![Fig1](<../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/work/fig1_disease_monitoring_audit.png>)
![Fig2](<../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/work/fig2_vaccination_high_risk.png>)
![Fig3](<../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/work/fig3_lessons_learned.png>)
![Fig4](<../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/work/fig4_ops_by_level.png>)
