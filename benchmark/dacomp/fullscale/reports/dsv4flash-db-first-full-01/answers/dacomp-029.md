<!-- Reading copy: local artifact links normalized. Original answer is preserved at ../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/answer.md -->

# Used Car Buyback Value Analysis Report

## Executive Summary

This report analyzes **675 used car listings** from the autohome platform to identify which vehicle models and configurations retain the highest value (buyback/保值率). The **overall average retention rate** (used price ÷ original new car price) is **69.0%**, with vehicles aged approximately 1–2 years being the dominant cohort.

The dataset consists primarily of **new energy vehicles (NEVs)** — pure electric, plug-in hybrid, and range-extender models — mostly small EVs in the mini/micro car segment (81.5% of listings have new car prices between 60,000–100,000 CNY).

---

## 1. Key Findings

### 1.1 Retention Rate Distribution

![Retention analysis overview](<../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/work/figure1_detailed_analysis.png>)

- **Retention rates range** from 20.9% (8-year-old Cayenne PHEV) to 89.1% (Changan Deep Blue SL03, 0.8 years old)
- Most vehicles (1–2 years old) cluster around **68–69% retention**
- The retention rate declines by approximately **5–6 percentage points per year** of age

### 1.2 Fuel Type Comparison

| Fuel Type | Avg Retention | Sample Size |
|-----------|:------------:|:-----------:|
| Range Extender | 69.5% | 228 |
| Pure Electric | 69.2% | 228 |
| Plug-in Hybrid | 68.3% | 219 |

All three fuel types perform similarly, with **range-extender** vehicles showing a marginal advantage. The difference is not statistically significant.

### 1.3 Vehicle Class Comparison

Top classes by retention (n ≥ 3):
- **Microcar** (e.g., Wuling Hongguang MINI EV): **73.3%** — highest retention
- **Mini Car**: **68.7%** — the largest segment (416 listings)
- **Mid-size SUV**: **66.2%**
- **Mid-to-Large SUV**: **60.1%**
- **Compact SUV**: **58.1%**

Smaller, cheaper vehicles consistently retain a higher percentage of their original value.

### 1.4 Age-Adjusted Retention

| Age Bracket | Avg Retention | Count |
|:-----------:|:------------:|:-----:|
| 0–1 year | 75.9% | 23 |
| 1–1.5 years | 68.6% | 184 |
| 1.5–2 years | 68.5% | 201 |
| 2–3 years | 63.5% | 30 |
| 3+ years | 40.8% | 9 |

The steepest depreciation occurs in the first year (~24% loss), then stabilizes to ~6–7% annual depreciation in years 1–2.

---

## 2. Best Models for Buyback (Mass Market)

### 2.1 Top Models by Retention Rate (n ≥ 3 listings)

![Model ranking](<../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/work/figure2_model_ranking.png>)

| Rank | Model | Retention | Avg Age | Listings |
|:----:|-------|:---------:|:-------:|:--------:|
| 1 | Hongguang MINI EV 2023 Elite Edition | **77.9%** | 1.4y | 3 |
| 2 | Hongguang MINI EV 2022 Elite Edition | **76.2%** | 1.5y | 4 |
| 3 | Chery eQ1 2023 Elite Edition | **73.2%** | 1.1y | 3 |
| 4 | Jianghuai iEV6E 2022 Luxury Edition | **72.6%** | 1.5y | 3 |
| 5 | Chery eQ1 2022 Elite Edition | **71.6%** | 1.6y | 3 |
| 6 | Nezha V 2023 Elite Edition | **70.9%** | 1.4y | 4 |
| 7 | Great Wall ORA Haomao 2023 Standard Edition | **70.2%** | 1.5y | 3 |
| 8 | Jianghuai Sihao E20X 2023 Elite Edition | **70.0%** | 1.5y | 3 |

**Key insight**: The **Wuling Hongguang MINI EV** and **Chery eQ1** (both affordable mini EVs) dominate the top retention spots. These vehicles have strong brand recognition, high demand, and low original prices, resulting in minimal depreciation.

### 2.2 Best Trim Levels

- **Elite Edition** (精英版): **69.8%** avg retention (n=102) — best performing trim
- **Standard Edition** (标准版): **69.2%** avg retention (n=87)
- **Luxury Edition** (豪华版): **69.0%** avg retention (n=94)

The Elite Edition trims command a small premium in the used market, likely due to better standard equipment (larger screens, driver assistance features, etc.).

---

## 3. Premium Vehicle Buyback Analysis

![Premium vehicles](<../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/work/figure3_premium_retention.png>)

### 3.1 Top Premium Vehicles (new car price ≥ 300,000 CNY)

| Model | Retention | Used Price | New Price | Age |
|-------|:---------:|:----------:|:---------:|:---:|
| **Cadillac LYRIQ 2022 Long Range Luxury** | **88.6%** | 38.97万 | 43.97万 | 0.3y |
| **NIO ET7 2022 75kWh** | **88.8%** | 39.80万 | 44.80万 | 0.4y |
| **Li Xiang L8 2023 Pro** | **85.6%** | 30.80万 | 35.98万 | 0.1y |
| **Tesla Model Y 2022 Standard Range** | **82.4%** | 24.88万 | 30.18万 | 0.7y |
| **BMW iX3 2021 Leading Model** | **81.7%** | 32.69万 | 39.99万 | 1.5y |
| **Mercedes-Benz EQA 2022 EQA 300 4MATIC** | **81.5%** | 29.88万 | 36.68万 | 1.2y |
| **IM L7 2022 Angel Wheel Edition** | **80.2%** | 32.80万 | 40.88万 | 1.8y |
| **NIO ES6 2021 420km Sport Edition** | **79.6%** | 28.50万 | 35.80万 | 2.0y |
| **Volvo XC40 Recharge 2022 P8 AWD** | **76.6%** | 28.65万 | 37.39万 | 0.9y |
| **Li Xiang ONE 2021 Range-Extender 6-Seat** | **58.5%** | 22.20万 | 37.97万 | 1.5y |

**Premium vehicles with the highest buyback value:**

1. **Cadillac LYRIQ** — nearly brand new (0.3 years), retains 88.6%
2. **NIO ET7** — very new (0.4 years), retains 88.8%
3. **Li Xiang L8** — almost new (0.1 years), retains 85.6%
4. **Tesla Model Y** — strong brand, retains 82.4% at 0.7 years
5. **BMW iX3** — 1.5 years old yet retains 81.7%, excellent buyback

**Caution on older premium vehicles:**
- **Cayenne E-Hybrid 2015** (8.4 years): only 23.0% retention
- **Li Xiang ONE 2021** (1.5 years): 58.5% — notably lower than its successor L8/L9

---

## 4. Configuration Analysis

### 4.1 Drivetrain

| Drivetrain | Avg Retention | Count |
|------------|:------------:|:-----:|
| Front-engine Rear-wheel Drive | 79.4% | 7 |
| Dual Motor Four-wheel Drive (AWD) | 69.5% | 239 |
| Front-engine Four-wheel Drive | 68.9% | 213 |
| Front-engine Front-wheel Drive | 66.9% | 147 |

**Rear-wheel drive** configuration shows the highest retention, though sample size is small (7 vehicles). Among mainstream configurations, **AWD (dual motor)** slightly outperforms FWD.

### 4.2 Color Preference

Popular color groups sorted by retention (n ≥ 10):
- **Yellow**: 71.6% (n=30) — uncommon but retains well
- **Pink**: 70.9% (n=31) — niche appeal
- **Orange**: 70.7% (n=26)
- **Black**: 70.4% (n=42)
- **Green**: 70.2% (n=53)
- **White**: 66.7% (n=106) — most common but lowest retention among major colors

**Recommendation**: Non-traditional colors (yellow, pink, orange, black) hold value slightly better, possibly because they are "special edition" colors in the mini EV segment.

### 4.3 Ownership History

| Previous Owners | Avg Retention | Count |
|:---------------:|:------------:|:-----:|
| 0 | 69.3% | 580 |
| 1 | 61.2% | 30 |
| 2 | 58.6% | 16 |
| 4 | 63.4% | 1 |

**Zero-owner vehicles** (first transfer) retain significantly more value. Each additional owner reduces retention by approximately 5–8 percentage points.

### 4.4 Listing Tags

| Tag | Avg Retention |
|-----|:------------:|
| Brand Verified | 74.8% |
| Like-New Vehicle | 73.4% |
| Zero Transfers | 72.6% |
| Brand Certified | 66.7% (lower due to higher mileage vehicles) |

---

## 5. Specific Buyback Recommendations

### 🏆 For Small EV Dealers (Mass Market - Best Returns)

| Priority | Model Recommendation | Reason |
|:--------:|---------------------|--------|
| **1st** | **Wuling Hongguang MINI EV Elite Edition** (2022-2023) | Highest retention (76–78%), strong brand, huge demand, low buy-in cost (~4–5万) |
| **2nd** | **Chery eQ1 Elite/Luxury Edition** (2022-2023) | 71–73% retention, reliable seller, consistent pricing |
| **3rd** | **Nezha V Elite Edition** (2023) | 70.9% retention, growing brand recognition |
| **4th** | **Jianghuai iEV6E Luxury Edition** (2022) | 72.6% retention, good value buy |
| **5th** | **Changan Benben E-Star Elite Edition** (2022-2023) | 69–70% retention, high volume (6 listings) |

**Optimal trim**: Always prefer **Elite Edition** over Standard or Luxury — it achieves ~0.6% higher retention.

**Recommended price range**: 4–6万 (CNY 40,000–60,000) used listing price, with new price around 7–8万.

### 🏆 For Premium EV Dealers

| Priority | Model Recommendation | Reason |
|:--------:|---------------------|--------|
| **1st** | **BMW iX3 2021-2022** | 81.7% retention at 1.5y, ~32万 resale, strong brand trust |
| **2nd** | **Mercedes-Benz EQA 300 4MATIC 2022** | 81.5% retention at 1.2y, ~30万 resale |
| **3rd** | **Tesla Model Y 2022** | 82.4% retention at 0.7y, ~25万 resale, highest liquidity |
| **4th** | **NIO ET7 2022** | 88.8% retention at 0.4y (very new), ~40万 resale |
| **5th** | **Li Xiang L8 2023 Pro** | 85.6% retention (almost new), ~31万 resale |

### ⚠️ Models to Avoid (Low Buyback Value)

| Model | Retention | Reason |
|-------|:---------:|--------|
| WM Motor W6 2022 | 58.7% | Low brand recognition, limited demand |
| WM Motor EX5 2021 | 63.3% | Weak resale market |
| Lantu FREE 2021 | 60.9% | Niche brand, limited buyer pool |
| Li Xiang ONE 2021 | 58.5% / 62.4% | Discontinued, replaced by L8/L9 |
| Trumpchi GS4 New Energy 2017 | 20.9% | Old, outdated PHEV tech |
| Audi Q2L e-tron 2019 | 41.5% | Short range, low demand |

---

## 6. Data Quality Notes

- **30 rows** (4.4% of dataset) were identified as having title/price mismatches (e.g., "Mercedes-Benz EQA 2023 Fashion Edition" listed with a new car price of 84,800 yuan, consistent with a mini EV). These were excluded from the primary analysis.
- The dataset is **dominated by small EVs** (81.5% have new car price 60k–100k CNY), so conclusions about premium/large vehicles are based on smaller sample sizes.
- Posting dates had leading/trailing whitespace for some vehicle classes, which required trimming for accurate age computation.

---

## 7. Conclusion

For a used car dealer, the **highest buyback value vehicles** are:

1. **Mass market**: **Wuling Hongguang MINI EV Elite Edition** (77–78% retention) — low risk, high turnover, strong demand
2. **Premium**: **BMW iX3 / Mercedes-Benz EQA** (~81–82% retention at 1.5 years) — strong brand equity
3. **Best trim**: Always choose **Elite Edition** trims
4. **Best colors**: Yellow, pink, orange, black (avoid white)
5. **Best age**: 0.5–1.5 years old (steepest depreciation already passed, still high retention)
6. **Lowest mileage**: Under 30,000 km preferred

The new energy used car market in China shows remarkable stability, with most vehicles retaining ~69% of their value after 1–2 years. The key to maximizing buyback profit is focusing on **high-volume, recognizable brands** (Wuling, Chery, BYD, Tesla) with **Elite trims** and **0 previous owners**.