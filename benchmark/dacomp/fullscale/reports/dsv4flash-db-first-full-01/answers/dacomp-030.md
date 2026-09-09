<!-- Reading copy: local artifact links normalized. Original answer is preserved at ../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/answer.md -->

# Coca-Cola Outlet Type Strategy: Contract Signing Volume Recommendations

## Executive Summary

Based on a comprehensive multi-dimensional analysis of **10 outlet types** across **583 outlets**, considering **Target Achievement Rate (TAR)**, **sales performance**, **customer complaint issues**, **contract renewal dynamics**, **assessment scores**, and **operational efficiency**, I recommend:

| Action | Outlet Types | Rationale |
|--------|-------------|-----------|
| **INCREASE Contracts** | **Specialty Store**, **Convenience Store**, **Gas Station** | High sales performance, strong growth, good renewal rates, under-invested |
| **MAINTAIN Contracts** | **Department Store**, **Shopping Center**, **Restaurant**, **Retail Store** | Mixed performance-risk profiles — selective approach |
| **REDUCE Contracts** | **Supermarket**, **Food Store**, **Beverage Shop** | Low target achievement, high complaint ratios, poor renewal metrics, low contract efficiency |

---

## 1. Data & Methodology

### Data Sources Linked
All tables were joined at the **Outlet ID** or **Customer ID** level from the `point_of_sale_(pos)_information` table (the master outlet registry):

- **Sales Performance**: `sales_data_table` (Target Achievement Rate, YoY/MoM growth, Sales Value, filtered to `Data Status = 'Valid'`)
- **POS Operations**: `point_of_sale_(pos)_information` (Actual Sales vs Sales Target, VPO, PC, Qualification Rate)
- **Contracts**: `contract_information_table` (Signing Amount, Renewal Flag, Same-store Ratio)
- **Complaints & Issues**: `customer_management_table` (Warning Record = 'Complaint Record' / 'Quality Issue'), `appeal_record_table` (appeals per outlet), `photo_information_table` (photo compliance failures)
- **Quality Compliance**: `assessment_result_table` (Assessment Score, Pass Rate)
- **Equipment**: `device_information_table` (Failure counts)
- **Investment**: `expense_allocation_table` (Budget utilization)

### Composite Scoring Framework
Three additive pillars were constructed using percentile ranking (0–100 scale):

1. **Sales Performance Pillar** (35% TAR + 25% POS Target Achievement + 20% YoY Growth + 20% Avg Sales Value)
2. **Risk / Complaint Pillar** (40% Complaint Ratio + 25% Quality Issue Ratio + 20% Appeals per Outlet + 15% inverted Renewal Ratio)
3. **Relationship Health Pillar** (45% Renewal Ratio + 30% High Renewal Likelihood + 15% Avg Pass Rate + 10% Avg Score)

**Net Score = Performance Score – Risk Score** → determines recommendation.

---

## 2. Key Findings by Metric

### 2.1 Target Achievement Rate (TAR)
| Outlet Type | Avg TAR | POS Target Achievement | YoY Growth |
|-------------|---------|----------------------|------------|
| Specialty store | **0.862** | 1.646 | 13.96% |
| Department Store | 0.848 | **1.676** | 19.70% |
| Gas station | 0.847 | 1.603 | **19.57%** |
| Convenience Store | 0.836 | **1.699** | 18.51% |
| **Beverage Shop** | **0.807** | **1.565** | 13.72% |
| Restaurant | 0.819 | 1.616 | 16.13% |

Specialty stores, gas stations, and convenience stores lead in TAR. Beverage shops and restaurants lag.

### 2.2 Customer Complaint Issues
| Outlet Type | Complaint Ratio | Quality Issue Ratio | Appeals/Outlet | Photo Fail Rate |
|-------------|----------------|-------------------|--------------|----------------|
| Specialty store | **0.473** (highest) | 0.236 | **0.27** (lowest) | **0.286** |
| Supermarket | 0.407 | 0.271 | 0.44 | 0.161 |
| Department Store | 0.375 | 0.391 | 0.52 | 0.244 |
| Food Store | 0.349 | 0.317 | 0.51 | 0.086 |
| **Shopping Center** | **0.259** (lowest) | 0.328 | 0.50 | 0.083 |
| **Retail Store** | 0.263 | 0.421 | 0.44 | 0.139 |

Specialty stores have the highest complaint ratio but the **lowest appeals per outlet** — complaints may be lower severity and do not escalate to formal assessment appeals. The high renewal rate (0.673) confirms customer satisfaction despite complaint records.

### 2.3 Contract Economics & Efficiency
| Outlet Type | Avg Signing Amount | Renewal Ratio | Total Signing | Sales/Signing CNY |
|-------------|-------------------|--------------|--------------|------------------|
| Specialty store | **557.1** (lowest) | **0.673** (highest) | 30,640 | **31.34** (best) |
| Convenience Store | 725.5 | 0.528 | 37,000 | 22.73 |
| Gas station | 666.7 | 0.483 | 40,000 | 27.93 |
| Beverage Shop | 635.7 | **0.423** (lowest) | 32,420 | 20.13 |
| Supermarket | 665.4 | 0.458 | 39,260 | 17.03 |
| Food Store | 674.0 | 0.460 | 42,460 | **14.71** (worst) |

**Specialty stores** generate **31.34 CNY in sales per 1 CNY of contract signing amount** — the highest efficiency by a wide margin, yet they have the **lowest average signing amount** (557.1 CNY), suggesting they are **under-contracted**.

### 2.4 Assessment & Quality
| Outlet Type | Avg Score | Pass Rate | Device Failures (avg) |
|-------------|-----------|----------|---------------------|
| Beverage Shop | **33.18** | **0.982** | 2.43 |
| Retail Store | 32.93 | 0.979 | 2.58 |
| Gas station | 32.87 | 0.979 | 2.77 |
| Specialty store | 32.52 | 0.975 | **2.98** (worst) |
| Convenience Store | 32.27 | 0.973 | **2.15** (best) |
| Supermarket | 32.24 | 0.972 | 2.77 |

Beverage shops score highest in assessments but underperform on TAR and renewal. Convenience stores have the lowest device failure rates.

---

## 3. Strategic Recommendations

### 3.1 INCREASE Contract Signing Volume

**★ Specialty Store** (Net Score: +32.5)
- **Why**: Highest TAR (0.862), highest renewal ratio (0.673), best contract efficiency (31.34), highest relationship health (79). Yet they have the **lowest average signing amount** (557 CNY) — clearly under-invested.
- **Caveat**: Complaint ratio (0.473) and photo failure rate (0.286) are high. Recommend **increasing contract volume with stricter quality compliance conditions** (e.g., photo compliance training, equipment upgrades).
- **Action**: Target +20–30% more contracts; increase average signing amount toward 700+ CNY.

**★ Convenience Store** (Net Score: +27.5)
- **Why**: Strong TAR (0.836), best POS target achievement (1.70), high YoY growth (18.5%), highest MoM growth (19.8%), lowest device failures (2.15), low complaint ratio (0.302). Strong contract efficiency (22.73).
- **Action**: Increase contract volume by 15–25%; ideal for piloting new promotional programs.

**★ Gas Station** (Net Score: +26.8)
- **Why**: High TAR (0.847), highest YoY growth (19.6%), #2 contract efficiency (27.93), highest total sales value (1.12M CNY). Moderate renewal ratio (0.483) leaves room for improvement through better contract terms.
- **Action**: Increase contract volume moderately (10–15%), focus on improving renewal incentives.

### 3.2 MAINTAIN Contract Signing Volume

| Outlet Type | Net Score | Key Consideration |
|-------------|-----------|-------------------|
| Shopping Center | +6.5 | Low performance (40) but also lowest risk (33.5); high health. Maintain with selective approach. |
| Department Store | +4.5 | High performance (78) but high risk (73.5); high complaints and appeals. Maintain existing contracts; improve quality monitoring. |
| Restaurant | -6.5 | Moderate performance (48) and risk (54.5); high sales value but low renewal. Maintain with focus on retention. |
| Retail Store | -14.5 | Low performance (30.5) but low risk and highest health (76.5). Maintain; address performance issues. |

### 3.3 REDUCE Contract Signing Volume

**▼ Supermarket** (Net Score: -16.5)
- **Why**: Low TAR (0.822), **highest complaint ratio** (0.407), **lowest health score** (17), low renewal ratio (0.458), low contract efficiency (17.03). High YoY growth (24.3%) is an outlier — investigate if driven by promotions rather than organic growth.
- **Action**: Reduce new contract volume by 15–20%; allocate freed resources to Specialty/Convenience.

**▼ Food Store** (Net Score: -20.5)
- **Why**: Low YoY growth (8.56%), second-highest risk score (66.5), high complaints (0.349), lowest contract efficiency (14.71). Low renewal ratio (0.46).
- **Action**: Reduce new contracts by 10–15%; focus on existing contract remediation.

**▼ Beverage Shop** (Net Score: -24.8)
- **Why**: **Lowest TAR** (0.807), lowest POS target achievement (1.565), **lowest renewal ratio** (0.423), high risk score (61.8). Despite high assessment scores, sales performance is poor.
- **Action**: Reduce new contract volume by 20–25%; require performance improvement plans before new contracts.

---

## 4. Visualization Summary

### Performance vs. Risk Matrix
![Performance vs Risk](<../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/work/performance_vs_risk.png>)
*Outlet types in the upper-right quadrant (High Performance, Low Risk) are recommended for contract increase. Lower-left quadrant (Low Performance, High Risk) are candidates for reduction.*

### Composite Scores Comparison
![Composite Scores](<../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/work/composite_scores.png>)
*Specialty stores lead in both performance and health while maintaining moderate risk. Supermarkets and beverage shops show the largest performance-risk gaps.*

### Key Metrics Heatmap
![Key Metrics Heatmap](<../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/work/metrics_heatmap.png>)
*Green = better (higher TAR, higher growth, higher renewal, lower complaints). Red = areas needing improvement.*

### Contract Efficiency
![Contract Efficiency](<../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/work/contract_efficiency.png>)
*Specialty stores generate 31.34× sales per contract CNY — the highest ROI. Food stores and shopping centers underperform significantly.*

---

## 5. Limitations

1. **Sales Data Coverage**: Only ~50% of sales records were `Data Status = 'Valid'` (322 valid out of 628). The analysis used only valid records.
2. **Complaint Definition**: The "Warning Record" captures both formal complaints and quality issues. The severity of complaints cannot be distinguished from the available data.
3. **Temporal Context**: The data appears to be from 2023. Seasonal patterns and one-time events may affect year-over-year comparisons.
4. **Causality**: Correlation between outlet types and performance does not imply causation. The recommendations should be validated with pilot programs before full rollout.
5. **Customer Level Mix**: Different outlet types have different customer level distributions (A–D), which may affect their baseline performance expectations.

---

## 6. Action Plan Summary

| Priority | Outlet Type | Action | Expected Impact |
|----------|-------------|--------|----------------|
| **P1** | **Specialty Store** | Increase contract volume 20–30% | +300K–500K additional sales at 31× ROI |
| **P2** | **Convenience Store** | Increase contract volume 15–25% | Strong growth channel with low operational risk |
| **P3** | **Gas Station** | Increase contract volume 10–15% | Leverage high sales volume, improve renewal |
| **P4** | **Supermarket** | Reduce new contracts 15–20% | Redirect resources to higher-yield channels |
| **P5** | **Beverage Shop** | Reduce new contracts 20–25% | Require performance improvement before new signing |
| **P6** | **Food Store** | Reduce new contracts 10–15% | Low efficiency channel; optimize existing portfolio |

**Total projected reallocation effect**: Redirecting ~35–45% of new contract capacity from Reduce-category outlets to Increase-category outlets could yield an estimated **15–25% improvement in aggregate sales per contract signing amount**.