<!-- Reading copy: local artifact links normalized. Original answer is preserved at ../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/answer.md -->

# Emergency Response Resource Allocation Effectiveness for Level 5 Disasters

## 1. Scope and Identification of Relevant Records

The `disaster_events` table contains 999 events; **202 are classified as "Level 5"** (the highest severity tier, ~20% of all events). Level 5 coverage spans all five disaster types: Flood (43), Earthquake (42), Tsunami (40), Hurricane (39), and Wildfire (38).

All 202 Level 5 events have complete 1:1 linked records in every resource dimension (confirmed by `COUNT(DISTINCT "Disaster Reference ID")` = 202 in `human_resources`, `operations1`, `financials1`, `supplies1`, `transportation1`, and `distribution_hubs` via the `Disaster Reference ID` / `Disaster Event Reference ID` columns). Level 5 events average **535,295 affected persons, 52,163 displaced, 2,409 injured, and 513 casualties**, with ~49% infrastructure damage and ~51% power outage (from the JSON `Impact Indicator`).

**Headline finding:** despite carrying the highest severity designation, Level 5 events receive essentially the *same* per-event resource envelope as lower-severity events while facing a larger affected population. Consequently, per-capita resource coverage is thinner and several operational-outcome anchors are worse for Level 5 than for the rest of the registry.

## 2. Human Resources Dimension (`human_resources` + `operations1`)

- **Staffing mix (documented staffing-ratio anchor):** average 258.3 total personnel per event, composed of medical 58.5 (**34% of staff**, vs 27.6% for non-Level 5), security 54.8 (33%), logistics 110.1 (**69%**), plus 541.2 volunteers (volunteer-to-staff ratio ≈ 3.2:1). The heavier medical weighting is a positive Level 5 anchor: **injured-per-medic = 54.5 vs 65.1 for non-Level 5**.
- **Readiness:** staff availability 85.1%; **37.6% of events report Critical PPE status** (vs 31.4% non-Level 5) and only **29.7% have Complete training** (vs 33.4% non-Level 5) — a negative anchor.
- **Operations (`operations1`):** `Resource Allocation Status` = Sufficient 74, Critical 65, Limited 63; `Supply Flow Status` = Stable 78, Disrupted 69, Strained 55; `Response Phase` spans Initial (59), Emergency (54), Reconstruction (51), Recovery (38); `Operation Status` = Planning 54, Active 54, Scaling Down 49, Completed 45. Emergency levels split across Black (51), Orange (63), Red (45), Yellow (43). Roughly **61% of Level 5 supply flows are non-stable** (Disrupted + Strained).

## 3. Financial Resources Dimension (`financials1`)

- Average budget allotment **$5,196,011** — statistically indistinguishable from non-Level 5 ($5,085,127) despite the larger impact footprint.
- **Funds utilization 50.2%** — identical to lower levels; the recorded `costbene(USD)` **cost-benefit anchor averages 493.1** (range 13.1–980.2), i.e., the documented ROI/benefit value per event.
- **Funding state:** only 64/202 Adequate; 66 Critical and 72 Limited (**68% of Level 5 events are not adequately funded**). Average resource gap $515,239 (~10% of budget) with donor commitments averaging $4.78M.
- **Cost structure (Fig. 3):** personnel costs dominate ($547,049), then transport ($524,621), operational ($488,103), storage ($255,483) — the mix is delivery/logistics-heavy as expected for Level 5 response.

## 4. Material Supplies Dimension (`supplies1` + `distribution_hubs`)

- **Inventory anchor (avg per event):** 527 generators, 49,667 L fuel, 50,304 medical units, 4,966 shelter units, 50,003 blankets, 502 tons food, 495,818 L water, 49,589 hygiene kits.
- **Coverage anchors:** 27.5 displaced per shelter unit; 2,307 affected per food ton; 0.115 injured per medical unit; 2.19 affected per liter of water.
- **Distribution hubs:** average capacity 4,803 tons at **50.5% utilization**; storage 49,262 m³ with 4,837 m³ available; cold storage 552 m³ at ~5 °C; **inventory accuracy 95.1%** (108/202 ≥ 95%) with turnover 2.62. Warehouse condition is mixed — Good 60, Excellent 52, but **Fair 45 and Poor 45** (44.6% below Good), undermining cold-chain and supply integrity at scale.

## 5. Transportation Dimension (`transportation1`)

- **Fleet anchor:** 106.8 vehicles/event (52.5 trucks, 4.9 helicopters, 9.8 ships); total transport volume 2,561 tons, daily throughput 252 tons across 26 distribution points.
- **Delivery-efficiency anchors:** average delivery time **35.6 hours**, **delivery success rate 85.8%** (range 70.1–99.9%). Deliveries are **On Track for only 31.7% of events** (64/202); **73 Delayed and 65 Suspended** (Fig. 2). **Route optimization is Required for 78 events** and only 67 are Optimized; **maintenance is Overdue for 131/202 (64.9%)**, with a 5.0% vehicle failure rate and 12.7 L/km fuel consumption.

## 6. How the Resource Mix Supports Operational Outcomes

- **Outcome anchors:** delivery success 85.8%, Distribution Equity Index **0.739** (the *lowest* of all severity tiers: L1 0.754, L2 0.755, L3 0.751, L4 0.758), affected-population feedback 3.06/5, report compliance 84.9%, data quality 3.0, stakeholder satisfaction 3.0, 26.5 partner organizations, and 51 security incidents per event.
- **Per-capita coverage is thinner for Level 5:** affected-per-staff = **3,253 vs 2,635** for non-Level 5; affected-per-$1k-budget = **0.273 vs 0.215**; affected-per-distribution-point = **28,852 vs 26,296**. In other words, Level 5 events are expected to serve *more* people with the same relative inputs.
- **Weak linkage between inputs and performance:** correlation analysis (Pearson/Spearman) between 17 resource indicators and delivery success for the 202 Level 5 events found **no statistically significant positive association** (all p > 0.05; best was inventory accuracy r = 0.133, p = 0.058). The only significant correlations were *negative*: hub utilization (r = −0.157, p = 0.026) and water supply (r = −0.207, p = 0.003) vs. beneficiary feedback — signs that over-utilized hubs and bulk stocking do not translate into better beneficiary-perceived outcomes.
- **Status triangulation (Fig. 1–2):** Critical allocation (65) pairs with Disrupted/Strained flows (23+25), Limited allocation (63) with Disrupted flows (20), and last-mile Suspended/Delayed (138/202) aligns with the 131 overdue-maintenance records — showing the transport/logistics bottleneck is the binding constraint on Level 5 outcomes, not the absolute size of the budget or inventory.

## 7. Conclusions

1. **Level 5 resource allocation is not severity-scaled.** Budget, staffing, supplies, and transport volume for Level 5 are statistically equivalent to lower severity levels, yet demand (affected population) is larger, driving weaker per-capita coverage (affected-per-staff +23%, affected-per-$1k +27%).
2. **Strength lies in medical staffing and inventory integrity.** Level 5 outperforms on medical-staff share (34%), injured-per-medic (54.5), inventory accuracy (95.1%), and comparable delivery success (85.8%) — the quantified performance expectations that are actually met.
3. **Weaknesses concentrate in logistics readiness:** 61% non-stable supply flows, 68% non-adequate funding, only 31.7% On-Track last-mile deliveries, 64.9% overdue maintenance, 37.6% Critical PPE, and the lowest distribution-equity index across all severity tiers (0.739).
4. **Allocation is not outcome-driven:** no significant input→outcome correlations indicate that marginal resources are not systematically steered toward the events where they would most improve delivery success or equity.

## 8. Limitations

- `costbene(USD)` is an index-like recorded field (13–980) without documented units; reported as the recorded cost-benefit anchor, not recomputed ROI.
- `operations1.Emergency Level` (Black/Orange/Red/Yellow) is a per-operation attribute independent of `Disaster Severity Level` (all severity levels contain all four), so it was not used as a severity proxy.
- Audit state for Level 5 shows Completed/Due/Overdue but no "Passed" values in the recorded field; compliance is therefore summarized as recorded categorical states.
- JSON payloads (Staffing, Inventory resources, Impact Indicator) were parsed with `json_extract`; analysis is SQL-aggregated with Python used only for correlation testing and figures.

![Resource intensity and HR/delivery metrics](<../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/work/fig1_resource_intensity.png>)
![Level 5 operational status distributions](<../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/work/fig2_operational_status.png>)
![Average cost breakdown for Level 5 events](<../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/work/fig3_cost_breakdown.png>)
![Operation duration by emergency level](<../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/work/fig4_emergency_duration.png>)
