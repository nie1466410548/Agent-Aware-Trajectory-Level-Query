# Analysis of the Relationship Between Industrial Water Consumption Share and Economic Development in China

## 1. Overview

This analysis uses data from 2000–2018 (national level) and 2003–2018 (provincial/municipal level) to examine the relationship between the **share of Industrial Water Consumption** (Industrial Water Consumption / Total Water Consumption) and **economic development level** (per capita GDP). The dataset covers China as a whole and 31 provinces, municipalities, and autonomous regions.

---

## 2. Overall China-Level Relationship

For China as a whole, the data show a clear **inverted-U shaped (Environmental Kuznets Curve) relationship**:

| Year | Industrial Water Share (%) | Per Capita GDP (yuan) |
|------|---------------------------|----------------------|
| 2000 | 20.72 | 7,316 |
| 2001 | 20.51 | 8,185 |
| 2002 | 20.78 | 8,847 |
| 2003 | 22.13 | 9,895 |
| 2004 | 22.15 | 11,000 |
| 2005 | 22.82 | 11,735 |
| 2006 | 23.19 | 12,419 |
| 2007 | **24.11** (peak) | 12,828 |
| 2008 | 23.64 | 13,873 |
| 2009 | 23.32 | 15,174 |
| 2010 | 24.03 | 17,079 |
| 2011 | 23.94 | 18,960 |
| 2012 | 23.18 | 20,542 |
| 2013 | 22.74 | 22,319 |
| 2014 | 22.25 | 25,670 |
| 2015 | 21.87 | 29,581 |
| 2016 | 21.65 | 31,402 |
| 2017 | 21.13 | 34,959 |
| 2018 | 20.97 | 35,911 |

**Key pattern:** As China's per capita GDP rose from 7,316 yuan to 35,911 yuan, the industrial water share first increased from ~20.7% (2000) to a peak of ~24.1% (2007), then declined to ~21.0% (2018). This suggests that after reaching a certain development threshold (around 13,000–17,000 yuan per capita GDP), economic growth began to decouple from industrial water use—likely due to structural transformation toward services, improved water efficiency, and stricter environmental regulations.

---

## 3. Provincial/Municipal Breakdown

When disaggregated by province, the relationship is **highly heterogeneous**. Provinces fall into three broad categories based on the correlation between their industrial water share and per capita GDP over time:

### 3.1 Positive Correlation (Share Rises with GDP)

These provinces are in the **rising phase** of the inverted-U curve:

| Province | Correlation (share vs GDP) | Share 2003 (%) | Share 2018 (%) | Change (pp) | Avg GDP (yuan) |
|----------|---------------------------|----------------|----------------|-------------|----------------|
| Ningxia | +0.75 | 5.47 | 6.50 | +1.03 | 13,626 |
| Xinjiang | +0.74 | 1.65 | 2.30 | +0.65 | 11,602 |
| Tibet | +0.70 | 1.35 | 4.73 | +3.38 | 14,741 |
| Shandong | +0.67 | 14.41 | 15.28 | +0.87 | 26,432 |
| Jiangsu | +0.61 | 35.95 | 43.11 | +7.16 | 34,849 |
| Hunan | +0.49 | 21.45 | 27.66 | +6.21 | 23,767 |
| Guangxi | +0.44 | 13.30 | 16.54 | +3.24 | 14,341 |
| Yunnan | +0.26 | 11.90 | 13.49 | +1.59 | 12,333 |
| Inner Mongolia | +0.10 | 6.05 | 8.28 | +2.23 | 17,608 |
| Henan | +0.06 | 21.27 | 21.48 | +0.21 | 17,515 |

These provinces include **less-developed western regions** (Ningxia, Xinjiang, Tibet, Guangxi, Yunnan, Inner Mongolia) still in the early-industrialization phase, as well as some **industrializing provinces** (Jiangsu, Shandong, Hunan) where industrial water use continued growing alongside economic expansion.

### 3.2 Weak/Negative Correlation (Share Stable or Declining)

| Province | Correlation (share vs GDP) | Share 2003 (%) | Share 2018 (%) | Change (pp) | Avg GDP (yuan) |
|----------|---------------------------|----------------|----------------|-------------|----------------|
| Fujian | -0.05 | 32.87 | 33.23 | +0.36 | 26,981 |
| Tianjin | -0.12 | 23.67 | 19.01 | -4.66 | 29,020 |
| Shaanxi | -0.13 | 17.35 | 15.47 | -1.88 | 20,956 |
| Anhui | -0.20 | 35.33 | 31.84 | -3.49 | 19,939 |
| Jiangxi | -0.26 | 27.07 | 23.44 | -3.63 | 22,596 |

These provinces show mixed patterns—some with very small changes, some already in a declining phase.

### 3.3 Strongly Negative Correlation (Share Declines with GDP)

These provinces are in the **declining phase** of the inverted-U curve:

| Province | Correlation (share vs GDP) | Share 2003 (%) | Share 2018 (%) | Change (pp) | Avg GDP (yuan) |
|----------|---------------------------|----------------|----------------|-------------|----------------|
| Zhejiang | -0.42 | 26.84 | 25.32 | -1.52 | 30,925 |
| Guizhou | -0.45 | 28.18 | 23.60 | -4.58 | 11,458 |
| Hubei | -0.45 | 32.94 | 29.44 | -3.50 | 25,433 |
| Hainan | -0.51 | 8.77 | 6.43 | -2.34 | 20,304 |
| Jilin | -0.61 | 21.37 | 13.97 | -7.40 | 16,338 |
| Qinghai | -0.66 | 14.31 | 9.58 | -4.73 | 12,121 |
| Chongqing | -0.74 | 42.58 | 37.69 | -4.89 | 29,825 |
| Hebei | -0.74 | 13.13 | 10.47 | -2.66 | 17,746 |
| Shanxi | -0.78 | 25.14 | 18.84 | -6.30 | 12,519 |
| Liaoning | -0.81 | 17.07 | 14.35 | -2.72 | 29,469 |
| Gansu | -0.83 | 13.39 | 8.19 | -5.20 | 10,686 |
| Beijing | -0.89 | 21.71 | 8.40 | -13.31 | 33,942 |
| Shanghai | -0.90 | 66.24 | 59.57 | -6.67 | 39,315 |
| Sichuan | -0.91 | 26.71 | 16.40 | -10.31 | 23,282 |
| Guangdong | -0.93 | 28.49 | 23.62 | -4.87 | 38,103 |
| Heilongjiang | -0.97 | 21.36 | 5.76 | -15.60 | 24,270 |

### 3.4 Peak Year Analysis

The year when each province reached its maximum industrial water share also varies widely:

| Peak Period | Provinces |
|-------------|-----------|
| **Early (2003–2006)** | Beijing (2004), Tianjin (2003), Shanxi (2006), Gansu (2003), Heilongjiang (2003), Jiangxi (2003), Shaanxi (2003), Qinghai (2007) |
| **Mid (2007–2010)** | Shanghai (2007), Guangdong (2007), Anhui (2007), Fujian (2010), Hubei (2010), Jilin (2010), Liaoning (2010), Sichuan (2008), Hainan (2008), Chongqing (2009) |
| **Late (2011–2014)** | Zhejiang (2011), Guangxi (2011), Xinjiang (2011), Guizhou (2012), Henan (2012), Hunan (2012), Tibet (2012), Yunnan (2012), Hebei (2013), Inner Mongolia (2013), Ningxia (2014) |
| **Still rising (2018)** | Jiangsu (2018), Shandong (2018) |

---

## 4. Summary of Key Findings

### 4.1 Overall Relationship
For China as a whole, the relationship between industrial water share and economic development is **inverted-U shaped**. Industrial water share rose from ~20.7% (2000) to a peak of ~24.1% (2007) as per capita GDP grew from ~7,300 to ~12,800 yuan, then declined to ~21.0% (2018) as GDP reached ~35,900 yuan. This suggests a **decoupling effect** at higher development levels driven by industrial upgrading, water conservation, and environmental policy.

### 4.2 Provincial Differences
The relationship differs substantially across provinces:

1. **Stage of development matters:** Less-developed western provinces (Tibet, Ningxia, Xinjiang, Guangxi, Yunnan) are still in the **rising phase**—their industrial water share increases as GDP grows. More developed provinces (Beijing, Shanghai, Guangdong, Zhejiang, Tianjin) have already passed the peak and show **declining shares**.

2. **Industrial structure matters:** Provinces with heavy industrial bases (Jiangsu, Shandong) continue to see rising industrial water shares even at relatively high GDP levels, suggesting their industrial structure remains water-intensive. In contrast, provincial-level municipalities (Beijing, Shanghai, Tianjin) have transformed toward service economies, sharply reducing industrial water use.

3. **Rate of decline varies dramatically:** Beijing's share fell from 21.7% to 8.4% (a 13.3 percentage point drop), while Heilongjiang's fell from 21.4% to 5.8% (15.6 pp). Meanwhile, Jiangsu's share rose from 36.0% to 43.1% (7.2 pp increase).

4. **Cross-sectional pattern also shifted:** In 2003, richer provinces generally had higher industrial water shares. By 2018, this cross-sectional relationship had weakened—some high-GDP provinces (Shanghai, Jiangsu) still had high shares, while others (Beijing, Guangdong) had reduced substantially.

### 4.3 Limitations
- This analysis is based on SQL queries only; no figures or statistical regression modeling were generated.
- The provincial data span 2003–2018, while national data go back to 2000. Earlier years for provinces could provide a more complete picture.
- The relationship is descriptive (correlations and trends) rather than causal. Factors such as industrial structure, water pricing, technology adoption, and environmental regulations likely mediate the relationship.
- The "share" uses total water consumption as the denominator, which includes agricultural, domestic, and ecological water—changes in those sectors also affect the share metric.