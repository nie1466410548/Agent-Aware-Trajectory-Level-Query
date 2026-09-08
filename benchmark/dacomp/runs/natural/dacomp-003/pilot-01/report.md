# Industrial Water Consumption Share vs. Economic Development in China (2000–2018)

**Data.** Provincial water-use records (`sheet1`) joined with provincial economic indicators (`economic_indicator_data`) on year and region code. 515 observations: the China national total (2000–2018, 19 years) plus 31 provinces/municipalities/autonomous regions (2003–2018, 16 years each, no missing values). The *industrial water share* is computed as Industrial Water Consumption ÷ Total Water Consumption (×100%). Per-capita GDP (yuan/person) proxies the level of economic development.

## 1. China overall: an inverted-U (Kuznets/EKC-type) relationship, not a simple linear one

Over 2000–2018, China's per-capita GDP grew ~4.9× (7,316 → 35,911 yuan). The industrial share of total water use traced a clear **inverted-U** against this growth (Fig. 1, Fig. 2):

- **Rising phase (2000–2007):** share climbed from 20.7% to a **peak of 24.1% in 2007**. Within this phase the share and GDP per capita are almost perfectly correlated (Spearman ρ = **+0.976**, p < 0.001).
- **Declining phase (2007–2018):** share fell steadily back to 21.0%. Spearman ρ = **−0.944** (p < 0.001) over this phase.
- Absolute industrial water use peaked later, in **2011 (146.2 billion m³)**, and declined to 126.2 billion m³ by 2018 — i.e., "decoupling" of industrial water use from GDP began even in absolute terms around 2011.

Because the two phases cancel out, a naive whole-period correlation is weak and insignificant (Pearson r = −0.15, p = 0.55; Spearman ρ = +0.11, p = 0.66). The correct reading is therefore a **two-stage, inverted-U path**: at lower income levels industrialization pushes industry's share of water up; after a turning point (~12,800 yuan per-capita GDP, 2007), efficiency gains, structural upgrading, and water-saving policy (the share decline coincides with China's "most stringent water resources management" era) push it back down while the economy keeps growing.

## 2. Cross-sectional view: richer provinces have *higher* industrial water shares

Cutting the data the other way — across the 31 provinces within each year — yields a **consistently positive** relationship: Spearman ρ between per-capita GDP and industrial water share ranges from **+0.49 to +0.63 (all p ≤ 0.005)** in every year 2003–2018 (pooled ρ = +0.31, p = 3×10⁻¹², n = 496; Fig. 3). More developed provinces/municipalities (e.g., Shanghai, ~60–66%; Jiangsu, ~36–43%; Chongqing, ~38–43%) devote a much larger share of water to industry than poor, agriculture-dominated regions (Tibet 1.3–4.7%, Xinjiang ~2%). This cross-sectional positive gradient reflects **economic structure** (share of industry in GDP) rather than a time trend — and it coexists with the within-region dynamics below.

## 3. Provincial breakdown: the relationship differs sharply by region

Computing the within-region time-series correlation (Spearman, 2003–2018, n = 16 each) between per-capita GDP and industrial water share gives a wide spread from −0.98 to +0.82 (Fig. 4, Fig. 5):

- **Strong negative (12 regions — "decoupling"):** Beijing (−0.98), Heilongjiang (−0.97), Gansu (−0.87), Shanxi (−0.82), Shanghai (−0.77), Qinghai (−0.77), Guangdong (−0.76), Sichuan (−0.69), Liaoning (−0.69), Chongqing (−0.57), Hebei (−0.52), Hubei (−0.51); all p < 0.05. This group is dominated by the most developed economies (Beijing's share fell 21.7%→8.4% while per-capita GDP rose ~3.8×; Guangdong 28.5%→23.6%) plus some northeast/old industrial bases. These regions sit on the **downward branch** of the inverted-U.
- **Strong positive (7 regions — still industrializing):** Xinjiang (+0.82), Ningxia (+0.80), Tibet (+0.75), Hunan (+0.71), Shandong (+0.58), Guangxi (+0.57), Jiangsu (+0.51); all p < 0.05. Mostly lower-income western regions where industrialization is still raising industry's water share (Tibet 1.3%→4.7%, Guangxi 13.3%→16.5%) — the **upward branch** of the inverted-U. Jiangsu is a notable exception: already rich but still rising (36.0%→43.1%), reflecting its heavy, water-intensive manufacturing base.
- **Weak/insignificant (12 regions):** e.g., Zhejiang, Tianjin, Fujian, Henan, Inner Mongolia (|ρ| < 0.5 or p ≥ 0.05) — many of these are near the turning point, showing flat or mildly hump-shaped paths (e.g., Tianjin's share hovered ~19–24% with no trend).

So the national inverted-U is an aggregation of regions at **different stages**: developed coastal municipalities and maturing industrial provinces have moved past the turning point (negative relation), while less-developed western regions remain on the rising limb (positive relation). This is consistent with a regional environmental-Kuznets interpretation: the sign of the GDP–industrial-water-share relationship depends on a region's development stage, not on development level alone.

## Key figures

| Finding | Value |
|---|---|
| China share 2000 → peak → 2018 | 20.7% → 24.1% (2007) → 21.0% |
| Spearman ρ, rising phase (2000–07) | +0.976 (p < 0.001) |
| Spearman ρ, declining phase (2007–18) | −0.944 (p < 0.001) |
| Whole-period naive correlation | r = −0.15, p = 0.55 (n.s.) |
| Cross-sectional ρ (each year 2003–18) | +0.49 to +0.63 (all p ≤ 0.005) |
| Regions with strong negative ρ | 12 (e.g., Beijing −0.98, Shanghai −0.77) |
| Regions with strong positive ρ | 7 (e.g., Xinjiang +0.82, Jiangsu +0.51) |

## Charts

- `fig1_china_overall.png` — China: industrial water share vs. per-capita GDP over time.
- `fig2_china_scatter.png` — China: inverted-U trajectory of share against per-capita GDP (year-colored).
- `fig3_cross_section.png` — Provincial cross-sections, 2003 and 2018 (positive within-year gradient).
- `fig4_region_corrs.png` — Bar chart of within-region Spearman correlations (2003–2018); * = p < 0.05.
- `fig5_trajectories.png` — Representative provincial trajectories in (GDP, share) space.

## Limitations

- The dataset covers only 2000–2018 (provinces from 2003); the turning-point dating (2007) is based on 19 annual points and could shift with more data.
- "Industrial share of water use" is driven by both economic structure and water-use efficiency; without sectoral GDP shares or water-intensity data, the mechanism (structure vs. efficiency vs. policy) cannot be separated.
- Per-capita GDP is in nominal yuan (no deflation available in the dataset), so comparisons are about development level rather than real income.
- Correlations are bivariate and do not control for urbanization, fixed-asset investment, or water-resource endowment; the cross-sectional positive gradient partly reflects differing industrial structures and agricultural water demand across provinces.
- National totals were taken from the provided "China" row rather than re-aggregated from provinces.
