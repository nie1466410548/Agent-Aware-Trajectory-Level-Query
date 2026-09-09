# Industrial Water Consumption Share and Economic Development in China (2000–2018)

## Executive Summary

The relationship between China's industrial water consumption share and per capita GDP is **not a simple linear function**. At the national aggregate level, it follows a **rise-then-fall (inverted-U)** pattern, while across provinces there is a **Simpson's paradox**: richer provinces have higher industrial water shares cross-sectionally, but within each province the share typically declines as the economy grows. Provincial trajectories diverge depending on the stage of industrialization.

---

## 1. National-Level Relationship

### 1.1 Data Overview

| Metric | Value |
|---|---|
| Time span | 2000–2018 (19 years) |
| National per capita GDP range | 7,316 → 35,911 yuan/person |
| Industrial water consumption share range | 20.5% → 24.1% → 21.0% |

### 1.2 The Inverted-U Pattern

![National time series and scatter](work/fig_national.png)

The national industrial water share rose from **20.7% in 2000** to a peak of **24.1% in 2007**, plateaued around 24% through 2011, and then declined steadily back to **21.0% by 2018** — all while per capita GDP grew monotonically by nearly 5×.

| Period | Phase | Pearson r (GDP vs share) | p-value | Interpretation |
|---|---|---|---|---|
| 2000–2007 | Rising | **+0.959** | 0.0002 | Strong positive correlation: share rises with GDP |
| 2008–2018 | Declining | **−0.956** | <0.0001 | Strong negative correlation: share falls as GDP rises |
| 2000–2018 (full) | Non-monotonic | −0.147 | 0.549 | Linear fit is meaningless; inverted-U fits better (R² = 0.38) |

The overall linear correlation is weak (Pearson r = −0.147, p = 0.55; Spearman ρ = 0.107, p = 0.66) because the relationship is **non-monotonic**. This is consistent with an **environmental Kuznets curve** for industrial water use: at early development stages, industrial expansion drives water share up; after a turning point, structural change toward services and water-saving technology drives it down.

---

## 2. Province-Level Relationship

### 2.1 Dramatic Heterogeneity

![Province trajectories](work/fig_trajectories.png)

The 31 provinces/municipalities/autonomous regions show striking divergence in the direction of their industrial water share trends:

**Strongly declining provinces** (10 with p < 0.05):  
Heilongjiang (−0.97), Guangdong (−0.93), Sichuan (−0.91), Shanghai (−0.90), Beijing (−0.89), Gansu (−0.83), Liaoning (−0.81), Shanxi (−0.78), Hebei (−0.74), Chongqing (−0.74)

**Strongly rising provinces** (5 with p < 0.05):  
Ningxia (+0.75), Xinjiang (+0.74), Tibet (+0.70), Shandong (+0.67), Jiangsu (+0.61)

**No significant trend** (16 provinces):  
Anhui, Fujian, Guangxi, Guizhou, Hainan, Henan, Hubei, Hunan, Inner Mongolia, Jiangxi, Shaanxi, Tianjin, Yunnan, Zhejiang, Qinghai, Jilin

### 2.2 Temporal Change (2003–2018)

![Province change scatter](work/fig_province_changes.png)

- **20 provinces** reduced their industrial water share between 2003 and 2018
- **11 provinces** increased their share
- Largest declines: Heilongjiang (−15.6 pp), Beijing (−13.3 pp), Sichuan (−10.3 pp)
- Largest increases: Jiangsu (+7.2 pp), Hunan (+6.2 pp), Tibet (+3.4 pp), Guangxi (+3.2 pp)

### 2.3 Structural Convergence Pattern

![Convergence figure](work/fig_convergence.png)

Provinces that started with a **higher industrial water share in 2003** tend to have **more negative Pearson correlations** between GDP and share (r = −0.43, p = 0.016). This suggests convergence: high-share provinces (old industrial bases, municipalities) are de-industrializing, while low-share provinces (western regions) are still industrializing.

### 2.4 The Simpson's Paradox: Within vs Between

![Within-province and between-province scatters](work/fig_within_province.png)
![Between-province scatter](work/fig_between_province.png)

| Decomposition | Pearson r | p-value | Interpretation |
|---|---|---|---|
| **Within-province** (temporal, demeaned) | **−0.373** | <0.0001 | On average, as a province develops, its industrial water share falls |
| **Between-province** (cross-sectional means) | **+0.614** | 0.0002 | Richer provinces average higher industrial water shares |
| Pooled (confounded) | +0.322 | <0.0001 | Positive but misleading due to level differences |

This is a classic **Simpson's paradox**: the cross-sectional relationship (between provinces) is positive, while the within-province temporal relationship is negative. The pooled correlation is a weighted average that can be misleading.

### 2.5 Cross-Sectional Relationship Over Time

| Year | Cross-sectional r (GDP vs share) | p-value |
|---|---|---|
| 2003 | **+0.686** | <0.0001 |
| 2018 | **+0.581** | 0.0006 |

The positive cross-sectional relationship weakened between 2003 and 2018, consistent with the convergence hypothesis: provinces are moving toward each other in industrial water structure.

---

## 3. Why the Relationship Differs by Province

The divergence reflects **different stages of the industrial development cycle**:

1. **Early-industrializing provinces** (Xinjiang, Tibet, Ningxia, Guangxi, Hunan, Jiangsu, Shandong): Their industrial water share is still rising as new industries are established. These provinces had very low initial shares (1.7%–6% in Xinjiang, Tibet, Ningxia) and are now increasing.

2. **Mature/post-industrial provinces** (Shanghai, Beijing, Heilongjiang, Liaoning, Chongqing, Guangdong): These provinces reached peak industrial water share earlier and are now de-industrializing. Shanghai's share fell from 66% to 55%, Beijing's from 22% to 8%.

3. **Agricultural bases** (Heilongjiang, Jilin, Henan, Shaanxi): These provinces maintained moderate-to-low industrial shares and are now reducing them through agricultural restructuring and water-saving policies.

---

## 4. Key Conclusions

1. **At the national level**, the relationship is **non-monotonic (inverted-U)** — rising with GDP in the early 2000s, peaking around 2007–2011, then declining. A simple linear correlation is not meaningful.

2. **At the provincial level**, the relationship differs dramatically: **negative** for already-industrialized provinces that are de-industrializing, **positive** for developing provinces that are still industrializing.

3. **A Simpson's paradox operates**: cross-sectionally richer provinces have higher industrial water shares, but temporally each province's share tends to fall as it grows richer.

4. **Convergence is occurring**: provinces with initially high industrial shares are declining faster, while those with low shares are rising, suggesting a gradual narrowing of provincial differences.

---

## 5. Limitations

- The dataset covers 2000–2018, which may not capture the full inverted-U turning point for all provinces.
- Province-level data aggregates mask intra-provincial heterogeneity (e.g., urban vs. rural).
- Causality cannot be inferred from the observed correlations.
- The analysis uses total industrial water consumption relative to total water consumption; absolute water use efficiency metrics (water use per unit of industrial output) are not examined.
- Data for provinces starts in 2003, missing the 2000–2002 period available for the national aggregate.