<!-- Reading copy: local artifact links normalized. Original answer is preserved at ../../../runs/dsv4flash-db-first-full-01/dacomp-016/attempt-01/answer.md -->

# Surface-to-Groundwater Ratio Trend for China (2005–2018) and Its Relationship with Urbanization

## 1. Data Sources and Validation

The analysis uses two tables from the supplied database:

- **`sheet1`**: Contains `Surface Water Supply (100 million m³)` and `Groundwater Supply (100 million m³)` for China and 31 provinces, 2000–2018.
- **`economic_indicator_data`**: Contains `Urbanization rate (%)` and other economic indicators for the same regions and years.

The "China" row in `sheet1` is verified to be the sum of the 31 province rows (e.g., for 2018: sum of provincial surface = 4952.8, China = 4952.7; sum of provincial groundwater = 976.2, China = 976.4; differences are within rounding). The 14-year span 2005–2018 has complete data for both tables.

The `Urbanization rate (%)` for the China row (23.1%–42.1%) is consistently lower than the simple average of the 31 provincial urbanization rates (36.2%–52.3%); this is noted as a dataset characteristic but does not affect the relational analysis within the dataset.

## 2. Surface-to-Groundwater Ratio: Full-Span Trend

The ratio is computed as:

$$\text{Surface-to-Groundwater Ratio} = \frac{\text{Surface Water Supply (100 million m³)}}{\text{Groundwater Supply (100 million m³)}}$$

| Year | Surface Supply | Groundwater Supply | **Ratio** | YoY Change |
|------|---------------|-------------------|-----------|------------|
| 2005 | 4572.19 | 1038.83 | **4.401** | — |
| 2006 | 4706.80 | 1065.52 | **4.417** | +0.016 |
| 2007 | 4723.90 | 1069.06 | **4.419** | +0.001 |
| 2008 | 4796.42 | 1084.79 | **4.422** | +0.003 |
| 2009 | 4839.47 | 1094.52 | **4.422** | ≈0 |
| 2010 | 4881.57 | 1107.31 | **4.408** | −0.013 |
| 2011 | 4953.30 | 1109.10 | **4.466** | +0.058 |
| 2012 | 4963.02 | 1134.22 | **4.376** | −0.090 |
| 2013 | 5007.29 | 1126.22 | **4.446** | +0.070 |
| 2014 | 4920.46 | 1116.94 | **4.405** | −0.041 |
| 2015 | 4971.50 | 1069.20 | **4.650** | **+0.244** |
| 2016 | 4912.40 | 1057.00 | **4.647** | −0.002 |
| 2017 | 4945.50 | 1016.70 | **4.864** | +0.217 |
| 2018 | 4952.70 | 976.40 | **5.072** | +0.208 |

**Overall conclusion: The ratio is increasing.** From 4.401 in 2005 to 5.072 in 2018, a relative increase of **15.3%**. The linear trend yields a slope of **+0.038 per year** (Pearson r = 0.76, p = 0.0016, statistically significant at α = 0.01).

### 2.1 Sub-Period Patterns

The trend is not uniform. Three distinct sub-periods emerge:

| Sub-period | Mean Ratio | Range | Linear Slope | r | Interpretation |
|-----------|-----------|-------|-------------|---|---------------|
| **2005–2010** | 4.415 | [4.401, 4.422] | +0.0015/yr | 0.34 | **Stable**; ratio hovers near 4.41–4.42 |
| **2011–2014** | 4.423 | [4.376, 4.466] | −0.011/yr | −0.36 | **Volatile, no net trend**; dips to series low (4.376 in 2012) and rebounds |
| **2015–2018** | 4.809 | [4.647, 5.072] | **+0.149/yr** | **0.94** | **Strong acceleration**; ratio rises 0.43 points in four years |

The 2005–2014 period as a whole is essentially flat (slope +0.0009/yr, r = 0.11), meaning the entire increase is concentrated in the final four years.

### 2.2 Inflection Points

1. **2012 trough (lowest ratio: 4.376).** Groundwater peaked at 1134.22 in 2012 while surface was near its pre-2015 plateau, creating the lowest ratio in the series.
2. **2014→2015 jump (largest YoY increase: +0.244).** Groundwater began declining sharply (1116.9 → 1069.2, a drop of 47.7) while surface water remained stable, triggering the first major ratio increase.
3. **2018 peak (5.072, highest in series).** Groundwater fell to 976.4 — its lowest level — while surface water held near 4953, pushing the ratio above 5.0 for the first time.

## 3. Component Analysis: What Drives the Ratio?

The ratio increases when surface water rises *or* groundwater falls. The data show:

- **Surface Water Supply** increased from 4572.2 (2005) to 4952.7 (2018), a **+8.3%** rise, with a steady upward trajectory through 2013 followed by a plateau.
- **Groundwater Supply** peaked at 1134.2 (2012), then declined every year from 2013 onward, reaching 976.4 (2018) — a **−13.9%** drop from the peak and a **−6.0%** drop from 2005.

The ratio increase is therefore **driven predominantly by the decline in groundwater supply**, especially after 2012. Surface water contributed modestly through its earlier rise, but the post-2014 acceleration of the ratio coincides with the sustained groundwater drawdown.

![Surface and Groundwater Supply Trends](<../../../runs/dsv4flash-db-first-full-01/dacomp-016/attempt-01/work/figure3_components.png>)

## 4. Relationship with Urbanization Rate

### 4.1 Co-Trend at the Macro Level

The `Urbanization rate (%)` for China rises from 23.12% (2005) to 42.08% (2018), a gain of **18.96 percentage points** (linear trend: +1.20 pp/yr, r = 0.91).

![Dual-Axis Time Series: Ratio vs Urbanization Rate](<../../../runs/dsv4flash-db-first-full-01/dacomp-016/attempt-01/work/figure1_dual_axis.png>)

**Pearson correlation between the ratio and urbanization: r = 0.73 (p = 0.003).**  
**Spearman rank correlation: r = 0.68 (p = 0.007).**

Both are statistically significant, indicating a strong positive monotonic association over the full 14-year span.

### 4.2 Regression Quantification

Linear regression of the ratio on urbanization yields:

$$\text{Ratio} = 3.62 + 0.0276 \times \text{Urbanization Rate (%)}$$

**R² = 0.53** — urbanization level alone explains 53% of the variance in the ratio across these 14 years.

![Scatter Plot with Regression Line](<../../../runs/dsv4flash-db-first-full-01/dacomp-016/attempt-01/work/figure2_scatter.png>)

### 4.3 Component-Level Correlations

| Variable | Correlation with Urbanization | p-value |
|----------|------------------------------|---------|
| Surface Water Supply | **+0.70** | 0.005 |
| Groundwater Supply | −0.33 | 0.244 |

Surface water supply is significantly and positively correlated with urbanization, while groundwater supply shows a weak negative correlation that is not statistically significant. This suggests that urbanization is associated with increased surface water supply (possibly through expanded reservoir and diversion infrastructure) but not directly correlated with groundwater extraction levels.

### 4.4 Sub-Period and First-Difference Analysis

Within each sub-period, the correlation between the ratio and urbanization is not statistically significant (p > 0.35 for all three sub-periods). The first-difference (year-over-year change) correlation is also negligible (r = −0.10, p = 0.74).

This indicates that the relationship is **driven by long-term directional co-movement rather than synchronous year-to-year fluctuations**. The ratio and urbanization both trend upward over the study period, but their annual changes do not track each other tightly.

### 4.5 Interpretive Argument

Urbanization is associated with:

1. **Increased surface water supply** (r = 0.70). As urban populations grow, governments invest in surface-water infrastructure (reservoirs, inter-basin transfers) to meet rising demand, which supports the numerator of the ratio.
2. **A delayed indirect effect on groundwater.** Groundwater extraction rose through 2012 to meet growing demand, but then declined as surface supplies expanded and policies likely restricted groundwater over-extraction (a common response to aquifer depletion in fast-urbanizing regions). The decline in groundwater after 2012 — the primary driver of the ratio increase — reflects a structural shift away from groundwater reliance that coincides with the later stages of rapid urbanization.

Thus, the positive ratio–urbanization correlation reflects two parallel processes: surface water expansion to serve urbanizing areas, and a subsequent reduction in groundwater dependence as surface-water infrastructure matures and groundwater conservation policies take effect. The notable acceleration of the ratio after 2014 (slope +0.149/yr vs. near-zero before) aligns with the period when urbanization in the dataset exceeded 37% and groundwater began its sustained decline.

## 5. Summary of Key Findings

| Metric | Value |
|--------|-------|
| Overall ratio change (2005→2018) | 4.401 → 5.072 (+15.3%) |
| Full-period linear slope | +0.038/yr (r = 0.76, p = 0.002) |
| Pre-2015 slope (2005–2014) | +0.001/yr (essentially flat) |
| Post-2014 slope (2015–2018) | +0.149/yr (strong acceleration) |
| Groundwater change (peak 2012 → 2018) | −13.9% from peak |
| Pearson r (ratio vs urbanization) | 0.73 (p = 0.003) |
| Regression R² (ratio ~ urbanization) | 0.53 |
| Surface supply vs urbanization r | 0.70 (p = 0.005) |

**Conclusion:** The surface-to-groundwater ratio for China increased steadily over 2005–2018, with a pronounced inflection in 2014–2015 that marked a shift from a stable plateau to rapid growth. The primary driver was the sustained decline in groundwater supply after 2012, while surface water supply grew modestly. Urbanization rate is positively correlated with the ratio (r = 0.73), mainly through its association with expanded surface water supply; the relationship is a long-term co-trend rather than a year-to-year coupling.

## 6. Limitations

- The `Urbanization rate (%)` for the China row in the dataset (23.1%–42.1%) is substantially lower than commonly reported national figures (≈43%–60% for the same period) and is also lower than the simple average of provincial urbanization rates. This suggests the dataset uses a different definition or aggregation method; all conclusions are based on within-dataset relationships only.
- The analysis is observational; correlation does not imply causation. The relationship between urbanization and water-supply composition is likely mediated by policy, infrastructure investment, and regulatory changes not captured in the dataset.
- With only 14 annual observations, sub-period correlations have limited statistical power.