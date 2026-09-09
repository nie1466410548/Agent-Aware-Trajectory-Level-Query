<!-- Reading copy: local artifact links normalized. Original answer is preserved at ../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/answer.md -->

# Loss-Making Item Analysis: Procurement Reduction Recommendations

## Overview

The supermarket plans to set procurement quantities on **2023-07-01** based on the sales volume of **2023-06-30**. To avoid loss-making sales, we analyzed previous years' summer data (Jul–Aug 2020, Jun–Aug 2021, Jun–Aug 2022) to identify items that are clearly sold below effective cost. A sale is defined as loss-making when:

> **Unit selling price < Wholesale price / (1 − Loss Rate%)**

The loss rate accounts for product spoilage/waste, making the effective cost per sellable kg higher than the raw wholesale price.

---

## Key Findings

### Items sold on 2023-06-30 (the procurement basis)

A total of **39 items** were sold on 2023-06-30. Of these, **34 had sufficient historical summer data** (sales records with matching wholesale prices and loss rates) for the analysis.

**Two items stand out as clearly loss-making:**

| Item Code | Item Name | 2023-06-30 Volume (kg) | 2022 Summer Avg Profit (yuan/kg) | 2022 Summer % Loss Sales | 2022 Summer Total Profit (yuan) | Loss Rate |
|-----------|-----------|----------------------|-------------------------------|-------------------------|-------------------------------|-----------|
| 102900005118824 | **Gao Gua (1)** | 3.78 | **−0.080** | **47.9%** | **−18.09** | 29.25% |
| 102900011032732 | **Gao Gua (2)** | 0.51 | **0.018** | **23.9%** | **−10.97** | 9.43% |

These are the **only two items** among the 34 analyzed that had a **negative total profit** in the most recent summer (2022). Gao Gua (2) is also the **only item** with a negative total profit across **all previous summers combined** (−10.97 yuan).

### Monthly breakdown in 2022 summer

| Item | 2022-06 Avg Profit | 2022-07 Avg Profit | 2022-08 Avg Profit |
|------|-------------------|-------------------|-------------------|
| Gao Gua (1) | +2.95 (0% loss) | **−1.04 (67.1% loss)** | **−4.61 (100% loss)** |
| Gao Gua (2) | no sales | +9.38 (only 10 sales) | **−0.16 (24.3% loss)** |

Both items become **deeply loss-making in July–August**, exactly when the 2023-07-01 procurement is happening.

### Direct evidence on 2023-06-30

| Item | Sales | Avg Selling Price | Effective Cost | % Loss Sales |
|------|-------|-----------------|---------------|-------------|
| Gao Gua (1) | 11 sales, 3.78 kg | 10.91 yuan/kg | 16.49 yuan/kg | **100%** |
| Gao Gua (2) | 2 sales, 0.51 kg | 14.40 yuan/kg | 15.12 yuan/kg | **50%** |

On the procurement basis date itself, **all** Gao Gua (1) sales were loss-making, and half of Gao Gua (2) sales were loss-making.

---

## Visual Evidence

### Figure 1: 2022 Summer Profitability – All Items To Be Procured

![2022 summer profitability](<../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/work/work/summer_profitability_2022.png>)

The bar chart shows the average profit per kg in 2022 summer (Jun–Aug) for all items sold on 2023-06-30. Only two items (red bars) have zero or negative average profit.

### Figure 2: Selling Price vs. Effective Cost for Gao Gua Items

![Price vs cost](<../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/work/work/gaogua_price_vs_cost.png>)

The chart shows the gap between average selling price (green) and effective cost (red) widening in July–August 2022, making sales increasingly loss-making.

---

## Conclusion

Based on previous years' summer data, the following items **clearly need their procurement quantities reduced** on 2023-07-01:

### 1. Gao Gua (1) — Item Code: **102900005118824**
- **Negative average profit** (−0.08 yuan/kg) in 2022 summer
- **47.9% of sales** were loss-making in 2022 summer
- **Negative total profit** in 2022 summer (−18.09 yuan)
- **100% loss-making** on 2023-06-30 (all 11 sales below cost)
- **High loss rate** of 29.25% compounds the issue

### 2. Gao Gua (2) — Item Code: **102900011032732**
- **Near-zero average profit** (0.018 yuan/kg) in 2022 summer
- **23.9% of sales** were loss-making in 2022 summer
- **Negative total profit** across all previous summers combined (−10.97 yuan) — the only item with this distinction
- **50% loss-making** on 2023-06-30

### Supplementary Note

**Honghu Lotus Root Shoots** (102900051000944) showed a large expected loss on 2023-06-30 (−22.25 yuan) due to deep discounting (8 of 14 sales at 13 yuan vs. effective cost of 23.70 yuan). However, its historical summer data (2022) was profitable (avg +5.54 yuan/kg, 0% loss), so it does not meet the "clearly loss-making based on previous years' summer data" criterion. The supermarket may wish to investigate its discounting policy separately.

---

## Limitations

- **5 items** sold on 2023-06-30 (Wild Pink Lotus Root, Cordyceps militaris, Hypsizygus combo, Malabar Spinach portion, Seafood Mushroom) had no previous summer sales records and could not be assessed.
- The analysis uses the last available wholesale price (June 2023) for the direct calculation; the actual 2023-07-01 wholesale price may differ.
- The loss rate is applied uniformly; in practice, spoilage may vary by season.