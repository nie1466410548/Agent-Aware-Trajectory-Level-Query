# Multi-Dimensional Vendor Resilience Assessment Framework

## Executive Summary

This report presents a comprehensive vendor resilience assessment for **91 key vendors** identified by spend concentration ratio >15% or strategic importance (Mission Critical / High Strategic Value). The analysis integrates four core resilience dimensions, a dynamic risk warning mechanism for 12-18 month supply disruption, personalized improvement plans, and quantitative ROI analysis of improvement strategies.

**Key Findings:**
- **Total portfolio exposure**: $44.0M across 91 key vendors
- **31 vendors (34%)** flagged as high disruption risk (probability ≥60%)
- **1 vendor (Industrial Components Group)** rated RED ALERT (79% disruption probability, $7.4M spend)
- **Financial resilience** is the weakest dimension (mean 71.4/100, but high-spend vendors score much lower)
- Financial Restructuring (S1) yields the highest ROI (782% portfolio-wide), followed by Contract Restructuring (297%)
- **Southwest region** concentrates 40.6% of total spend, creating geographic risk concentration

---

## 1. Multi-Dimensional Resilience Assessment Framework

### 1.1 Dimension Definitions

| Dimension | Components | Weighting |
|---|---|---|
| **Financial Resilience** | Avg Payment Delay (lower better), Overdue Payment % (lower better), Financial Health Score (higher better) | 30% / 35% / 35% |
| **Operational Resilience** | Quality Score, Cybersecurity Score, Innovation Capability Score | 35% / 35% / 30% |
| **Market Resilience** | Market Volatility Index (lower better), Alternative Suppliers Count (higher better), Price Volatility Coefficient (lower better), Switching Cost (lower better) | 30% / 30% / 20% / 20% |
| **Strategic Resilience** | Geographic Diversity, Contract Expiry Days, Environmental Rating, Relationship Stability, Transaction Recency, Relationship Duration | 20% / 20% / 15% / 15% / 15% / 15% |

### 1.2 Score Distribution

| Dimension | Mean | Std Dev | Min | Max |
|---|---|---|---|---|
| **Financial Resilience** | 71.4 | 22.1 | 6.0 | 98.4 |
| **Operational Resilience** | 50.8 | 12.9 | 17.2 | 80.1 |
| **Market Resilience** | 57.6 | 10.5 | 36.9 | 83.4 |
| **Strategic Resilience** | 48.6 | 8.4 | 36.9 | 85.9 |
| **Overall Resilience** | 57.1 | 7.3 | 32.4 | 71.7 |

**Classification**: 1 High Resilience, 81 Medium Resilience, 9 Low Resilience.

### 1.3 Visualizations

#### Figure 1: Multi-Dimensional Resilience Heatmap (Top 15 by Spend)
![Resilience Heatmap](figure1_resilience_heatmap.png)

The heatmap reveals that high-spend vendors consistently score poorly on Financial Resilience (red cells), while Operational and Market dimensions show more variation. Industrial Components Group ($7.4M) is the weakest overall.

#### Figure 2: Resilience Radar - Top 5 Strategic Vendors
![Resilience Radar](figure2_resilience_radar.png)

The radar chart shows the stark contrast between Operational/Innovation strengths (Precision Electronics scores 97 on cybersecurity) and Financial weaknesses across all top vendors.

#### Figure 3: Score Distribution Across Dimensions
![Score Distributions](figure3_score_distributions.png)

Financial Resilience is bimodal with a cluster of high and low scores. Operational and Strategic show more normal distributions. Market Resilience is relatively compressed.

#### Figure 4: Resilience by Vendor Category
![Category Resilience](figure4_category_resilience.png)

Construction & Engineering leads in Strategic Resilience but lags in Operational. Manufacturing & Industrial shows the weakest financial scores. General Suppliers (low-spend) have high Financial but low Operational resilience.

#### Figure 5: Spend vs. Resilience
![Spend vs Resilience](figure5_spend_vs_resilience.png)

A strong negative correlation (-0.690) exists between vendor spend and overall resilience. High-spend vendors are systematically less resilient, creating a "too big to fail, too risky to ignore" paradox.

---

## 2. Dynamic Risk Warning Mechanism (12-18 Month Horizon)

### 2.1 Risk Indicator Framework

The disruption probability integrates 8 weighted indicators:

| Risk Indicator | Weight | Description |
|---|---|---|
| Financial Distress Risk | 20% | Inverse of financial health, payment delays, overdue % |
| Dependency Risk | 15% | Critical/High dependency levels |
| Activity Risk | 15% | Dormant/Inactive status |
| Contract Expiry Risk | 12% | Contracts expiring within 12-18 months |
| Operational Weakness Risk | 12% | Low quality/cyber/innovation scores |
| Market Risk | 12% | High volatility, few alternatives, high price volatility |
| Concentration Risk | 9% | High spend concentration ratio |
| Inactivity Risk | 5% | Days since last transaction |

### 2.2 Warning Levels

| Warning Level | Threshold | Vendors | Total Spend |
|---|---|---|---|
| 🔴 RED ALERT (≥75) | 79+ | 1 | $7.4M |
| 🟠 AMBER (60-74) | 60-74 | 30 | $27.3M |
| 🟡 YELLOW (45-59) | 45-59 | 58 | $9.1M |
| 🟢 GREEN (<45) | <45 | 2 | $0.2M |

#### Figure 6: Disruption Risk Distribution
![Disruption Risk](figure6_disruption_risk.png)

The distribution shows a right-skewed pattern with most vendors in the 45-65 range. The bubble chart confirms that high-spend vendors cluster in the high-risk/low-resilience quadrant.

### 2.3 High-Risk Scenarios

**RED ALERT - Industrial Components Group** (79% disruption probability, $7.4M spend):
- Financial Resilience score: 10/100 (worst in portfolio)
- 35.7% overdue payment rate, 41.8 days avg payment delay
- Critical dependency, Unstable relationship, Inactive status
- 92 days since last transaction
- **Risk**: Immediate supply disruption highly probable

**AMBER - Key High-Risk Vendors (Spend > $1M):**

| Vendor | Spend | Prob | Key Weakness |
|---|---|---|---|
| Central Supply Systems | $2.7M | 74% | Operational (17) |
| Advanced Materials Group | $4.8M | 72% | Financial (26) |
| Precision Electronics Corp | $7.2M | 71% | Financial (6) |
| Vendor_NET71245 | $3.0M | 70% | Financial (31) |
| Strategic Manufacturing Corp | $2.5M | 68% | Financial (21) |
| Global Steel & Materials Corp | $1.3M | 63% | Financial (28) |
| Energy Solutions Consortium | $2.7M | 63% | Financial (30) |
| Prime Logistics Solutions | $3.3M | 60% | Financial (8) |

#### Figure 10: Risk Quadrant
![Risk Quadrant](figure10_risk_quadrant.png)

#### Figure 11: Risk Indicator Breakdown (Top 5)
![Risk Indicator Breakdown](figure11_risk_indicators.png)

---

## 3. Personalized Resilience Improvement Paths

### 3.1 Improvement Plans for Key High-Risk Vendors

**Industrial Components Group** ($7.4M, 79% disruption probability):
- **Priority 1 - Financial**: Negotiate early-payment discounts; establish dynamic payment terms; implement weekly AP monitoring; reduce credit limit
- **Priority 2 - Operational**: Conduct quality/cybersecurity audit; co-develop innovation roadmap; enforce SLA penalties
- **Contingency**: IMMEDIATE ACTION - Freeze new orders, activate alternative suppliers, initiate urgent contract renegotiation, establish 30-day emergency inventory buffer

**Precision Electronics Corp** ($7.2M, 71% disruption probability):
- **Priority 1 - Financial**: Immediate payment plan restructuring; reduce credit exposure
- **Priority 2 - Market**: Qualify 2+ alternative suppliers; hedge price volatility
- **Contingency**: SHORT-TERM - Begin alternative supplier qualification, reduce dependency, monitor daily

**Advanced Materials Group** ($4.8M, 72% disruption probability):
- **Priority 1 - Financial**: Renegotiate payment terms; weekly monitoring
- **Priority 2 - Operational**: Quality improvement program; cybersecurity audit
- **Contingency**: SHORT-TERM - Qualify backup suppliers, reduce single-source dependency

**Central Supply Systems** ($2.7M, 74% disruption probability):
- **Priority 1 - Operational**: Quality/cybersecurity audit; SLA enforcement
- **Priority 2 - Financial**: Early-payment discounts; dynamic payment terms
- **Contingency**: SHORT-TERM - Contract renegotiation, weekly risk monitoring

### 3.2 Contingency Plans by Risk Tier

- **RED ALERT (≥75)**: Immediate freeze on new orders, activate alternatives, executive escalation, daily monitoring, 30-day emergency inventory
- **AMBER (65-74)**: 30-60 day action plan - qualify backup suppliers, reduce dependency, renegotiate terms, weekly monitoring
- **YELLOW (60-64)**: Elevated monitoring - formalize alternative shortlist, quarterly reviews, maintain communication

---

## 4. Quantitative ROI Analysis of Resilience Strategies

### 4.1 Strategy Definitions

| Strategy | Cost Rate (% of Spend) | Expected Prob Reduction | Focus Dimension |
|---|---|---|---|
| **S1: Financial Restructuring** | 0.5% | 25% | Financial |
| **S2: Supplier Diversification** | 2.5% | 35% | Market |
| **S3: Cybersecurity & Quality Upgrade** | 1.5% | 20% | Operational |
| **S4: Contract Restructuring** | 0.8% | 18% | Strategic |
| **S5: Geographic Diversification** | 3.0% | 30% | Strategic |
| **S6: Joint Innovation Program** | 1.2% | 15% | Operational |
| **S7: ESG Compliance Program** | 0.4% | 8% | Strategic |
| **S8: Inventory Buffer & VMI** | 2.0% | 40% | Financial |

### 4.2 Portfolio-Wide ROI (3-Year Horizon)

| Strategy | Annual Cost | Annual Benefit | Net Benefit (3yr) | ROI | Positive ROI Vendors |
|---|---|---|---|---|---|
| **S1: Financial Restructuring** | $220K | $1.94M | $5.16M | **782%** | 91/91 |
| **S4: Contract Restructuring** | $352K | $1.40M | $3.14M | **297%** | 91/91 |
| **S8: Inventory Buffer & VMI** | $881K | $3.11M | $6.68M | **253%** | 91/91 |
| **S7: ESG Compliance Program** | $176K | $621K | $1.34M | **253%** | 91/91 |
| **S2: Supplier Diversification** | $1.10M | $2.72M | $4.85M | **147%** | 90/91 |
| **S3: Cybersecurity & Quality** | $660K | $1.55M | $2.68M | **135%** | 89/91 |
| **S6: Joint Innovation** | $528K | $1.16M | $1.91M | **120%** | 89/91 |
| **S5: Geographic Diversification** | $1.32M | $2.33M | $3.03M | **76%** | 65/91 |

#### Figure 7: ROI Comparison
![ROI Strategies](figure7_roi_strategies.png)

#### Figure 9: Refined ROI
![Refined ROI](figure9_refined_roi.png)

#### Figure 12: ROI Sensitivity Analysis
![ROI Sensitivity](figure12_roi_sensitivity.png)

The sensitivity analysis shows that even at modest probability reductions (15-20%), both S1 and S2 deliver positive ROI. The breakeven point for S2 (Supplier Diversification) is at ~10% probability reduction.

#### Figure 13: Strategy Cost-Benefit Trade-off
![Strategy Trade-off](figure13_strategy_tradeoff.png)

### 4.3 Optimal Strategy by Vendor

For **all 91 vendors**, S1 (Financial Restructuring) is the optimal first-priority strategy due to its low cost (0.5% of spend) and high impact. However, for a comprehensive risk management approach, a **layered strategy** is recommended:

| Vendor Tier | Primary Strategy | Secondary Strategy |
|---|---|---|
| RED ALERT (1 vendor) | S1: Financial Restructuring | S2: Supplier Diversification |
| AMBER, high-spend (8 vendors) | S1: Financial Restructuring | S4: Contract Restructuring |
| YELLOW (58 vendors) | S1: Financial Restructuring | S7: ESG Compliance |
| GREEN (2 vendors) | S4: Contract Restructuring | S7: ESG Compliance |

---

## 5. Portfolio Optimization Recommendations

### 5.1 Geographic Risk Concentration

| Region | Vendors | Total Spend | % of Portfolio |
|---|---|---|---|
| **Southwest** | 31 | $17.9M | **40.6%** |
| **Northeast** | 21 | $11.1M | 25.2% |
| **West Coast** | 11 | $8.4M | 19.2% |
| Central US | 12 | $2.7M | 6.1% |
| Southeast | 15 | $2.7M | 6.0% |
| Global | 1 | $1.3M | 2.9% |

**Recommendation**: Reduce Southwest concentration through geographic diversification (S5, ROI 76%). Target 25% max per region.

### 5.2 Category-Level Risk

| Category | Spend | Avg Delay | Avg Overdue | Avg Fin Health | Priority |
|---|---|---|---|---|---|
| **Manufacturing & Industrial** | $15.5M | 42.5d | 33.5% | 47.8 | CRITICAL |
| **Technology & Electronics** | $7.2M | 47.6d | 38.1% | 43.0 | CRITICAL |
| **Raw Materials & Components** | $6.0M | 39.3d | 30.1% | 58.0 | HIGH |
| **Logistics & Supply Chain** | $7.3M | 35.8d | 27.9% | 51.3 | HIGH |

### 5.3 Contract Expiry Risk

79 of 91 vendors (87%) have **Strategic Partnership** contracts. Contracts show a cluster of expiries in **2025 Q1** (Feb: 11 vendors, Jan: 9 vendors, Mar: 8 vendors), creating a renewal bottleneck.

**Recommendation**: Initiate contract renewal negotiations 6 months before expiry (by Q3 2024 for Q1 2025 expiries). Prioritize the 11 vendors with Feb 2025 expiries.

### 5.4 Phased Implementation Roadmap

| Phase | Timeline | Actions | Cost Estimate | Expected Benefit |
|---|---|---|---|---|
| **Phase 1 - Emergency** | Months 1-3 | Financial restructuring for RED/AMBER vendors (9 vendors) | $220K | 25% reduction in disruption probability |
| **Phase 2 - Stabilization** | Months 3-6 | Contract restructuring for all 91 vendors | $352K | 18% further risk reduction |
| **Phase 3 - Diversification** | Months 6-12 | Supplier diversification for high-risk categories | $1.1M | 35% risk reduction for covered vendors |
| **Phase 4 - Optimization** | Months 12-18 | Geographic diversification, ESG, innovation programs | $1.3M | Portfolio optimization |
| **Total 18-Month Investment** | | | **~$3.0M** | **Expected 3-year benefit: ~$15.8M** |

---

## 6. Limitations

1. **Synthetic data effects**: 77 vendors (85%) have synthetic names ("Vendor_NETxxxxx") with minimal spend (<$1K) but 100% concentration ratios, likely representing edge-case test data. Their inclusion may skew portfolio-level metrics.
2. **Analysis date variance**: The `analysis_date` ranges from 2024-01-01 to 2025-09-20, meaning the "12-18 month" risk window is not uniform across all vendors.
3. **ROI model simplifications**: Cost rates and probability reductions are estimates based on industry benchmarks. Actual ROI depends on implementation effectiveness and vendor cooperation.
4. **Single-snapshot data**: The database represents a single point-in-time assessment. A time-series approach would improve trend detection.
5. **No external validation**: The disruption probability model is internally consistent but has not been validated against actual disruption events.

---

## 7. Conclusion

The multi-dimensional resilience assessment reveals a clear pattern: **high-spend vendors are systematically less resilient**, particularly in financial health. The concentrated geographic exposure (40.6% in Southwest) and clustered contract expiries (Q1 2025) create additional systemic risk.

**Priority actions for senior management:**
1. **Immediate**: Implement Financial Restructuring (S1) for the 9 high-spend AMBER/RED vendors - ROI 782%, 3-year net benefit $5.2M
2. **Short-term**: Initiate Contract Restructuring (S4) across all key vendors before Q1 2025 expiry cluster
3. **Medium-term**: Deploy Supplier Diversification (S2) for Manufacturing & Industrial and Technology & Electronics categories
4. **Ongoing**: Establish quarterly risk monitoring with dynamic re-scoring of the 4-dimensional framework

The total 18-month investment of ~$3.0M is projected to yield **$15.8M in risk reduction benefits** over 3 years, representing a **5.3x return** on resilience investment.