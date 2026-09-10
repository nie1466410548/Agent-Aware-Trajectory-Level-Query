# Why is the monthly total profit in "South China" unstable? — Data Analysis Report

## Scope & data
- Data: `sheet1`, 18,250 orders in 2023 (Jan–Dec). Rows classified as South China (Destination LIKE `South China%`): 6,785 orders, ~8.83M total profit.
- **Data caveat**: the "South China" label in the dataset actually includes **non-South-China provinces**: Guangdong (2,873 orders), Guangxi (1,765), **Henan (797), Hubei (428), Hunan (396)**. Henan/Hubei/Hunan are geographically central China but are tagged "South China-…" in the data. These small, erratic segments are themselves a source of noise (see §4).

## 1. The instability in numbers
Monthly total profit (2023, all "South China" rows):

| Month | Profit | Month | Profit |
|---|---|---|---|
| Jan | 752,710 | Jul | 772,966 |
| Feb | **637,737** | Aug | 774,760 |
| Mar | 756,201 | Sep | 769,287 |
| Apr | 684,254 | Oct | 763,990 |
| May | 713,489 | Nov | 744,050 |
| Jun | 674,620 | Dec | **789,694** |

- Range: 637,737 (Feb) → 789,694 (Dec), a swing of **151,957 (23.8% of the trough month)**.
- Mean 736,146, std 45,646, **CV = 6.2%**. Trough months: **Feb, Jun, Apr**; peak months: Dec, Aug, Jul, Sep, Oct (H2 > H1).

## 2. The instability is driven by sales VOLUME, not pricing or margins
Decomposition of monthly series (CV = std/mean):

| Metric | Mean | Std | CV |
|---|---|---|---|
| Profit | 736,146 | 45,646 | 6.2% |
| Total Logistics Revenue | 789,017 | 48,092 | 6.1% |
| Total Logistics Cost | 52,870 | 3,200 | 6.1% |
| Sales Quantity | 28,336 | 1,568 | 5.5% |
| **Number of orders** | **565** | **30** | **5.2%** |

Per-order / per-unit economics are **stable** (CV only 2.5–3.6%):
- Revenue/order: 1,328–1,485 (CV ~3.6%); quantity/order: 48–51 (CV ~2.6%)
- Revenue/unit: 26.8–28.7 (CV ~2.5%); **profit/unit: 24.9–26.9 (CV ~2.7%)**
- Weighted profit margin (profit/revenue) is rock-steady at **92.9–93.8%**
- Discount rate stable (~0.68–0.76% of list price); VAS revenue rate stable (~1.6–2.0%)

**Conclusion: monthly profit moves almost 1:1 with order volume (CV 6.2% vs 5.2%); the per-unit price/margin structure does not fluctuate. The "instability" is essentially demand/order-volume volatility, with a clear seasonal shape (February trough, likely Chinese New Year; Aug–Dec high season).**

Costs are NOT the driver: total cost is only ~6.7% of revenue, and cost components track volume (Freight CV 6.7%, Warehousing 5.6%, Other 5.6%). Profit is therefore almost pure revenue pass-through.

## 3. Product-mix is a major amplifier (which products cause it)
Monthly profit std/CV by product (South China):

| Product | Avg monthly profit | Std | CV | Feb plunge (vs Jan) |
|---|---|---|---|---|
| Kitchen Appliances | 92,395 | **18,941** | **20.5%** | **−66,650** |
| Bathroom supplies | 109,846 | 15,169 | 13.8% | +2,170 |
| Bedroom Furniture | 87,611 | 13,488 | 15.4% | −13,661 |
| Bedding set | 142,198 | 13,322 | 9.4% | +4,281 |
| Computer hardware | 85,548 | 12,753 | 14.9% | +5,473 |
| Auto parts | 107,479 | 12,397 | 11.5% | −18,662 |
| Home decor items | 98,138 | 12,033 | 12.3% | −31,007 |
| Office furniture | 12,932 | 5,286 | 40.9% | +3,081 |

- **Kitchen Appliances is the single biggest destabilizer**: highest absolute monthly swing (std 18,941; range 60,725→127,375 = 66,650). Its February collapse (−66,650) alone explains **58%** of the total Feb profit drop (−114,973).
- **Home decor (−31,007), Auto parts (−18,662) and Bedroom Furniture (−13,661)** together explain another ~55% of the Feb decline (offset partly by Bedding/Computer/Bathroom/Office gains).
- **Office furniture** is the most volatile in relative terms (CV 40.9%) but small in size, so it adds noise without moving the total much.
- **Bedding set** is the largest profit contributor but has the lowest CV (9.4%) — it acts as a stabilizer.

## 4. Geography: small/erratic regions + mislabeled provinces add noise
Monthly-profit CV by province within the "South China" filter:

| Province | Avg monthly profit | Std | CV | Share of total profit |
|---|---|---|---|---|
| Guangdong | 314,374 | 26,780 | 8.5% | 43% |
| Guangxi | 189,873 | 17,748 | 9.3% | 26% |
| Hainan | 57,174 | 11,423 | 20.0% | 8% |
| **Henan (not South China)** | 86,285 | 14,335 | 16.6% | 12% |
| **Hubei (not South China)** | 47,843 | 10,954 | 22.9% | 6% |
| **Hunan (not South China)** | 40,599 | 7,802 | 19.2% | 6% |

- The **large core (Guangdong + Guangxi, 69% of profit)** has moderate CV (8.5–9.3%) and moves together with the seasonal volume pattern.
- The **smaller segments (Hainan, and the mislabeled Henan/Hubei/Hunan)** have CVs of 17–23%, i.e., ~2–3× more volatile than the core. In the Feb slump, Henan (−40,427) and Guangxi (−35,140) were the two biggest regional contributors, followed by Guangdong (−19,883) and Hainan (−17,435).
- At city level, several small cities are extremely erratic: Guangxi-Wuzhou CV 65.7%, Henan-Zhengzhou CV 68.4%, Guangdong-Qingyuan CV 42.8%, Guangdong-Yangjiang CV 45.8%, Guangdong-Foshan CV 38.3%, Henan-Anyang CV 37.5%.

## 5. Outliers in per-order margin (data-quality noise, not a profit driver)
A few abnormal orders (e.g., negative or near-zero revenue with positive cost: `DML202310312062` revenue −0.53 / cost 134.78 → margin 25,530%; `DML202308252842` revenue 2.01 / cost 134.27 → margin −6,580%) inflate the *average* per-order margin metric (Oct avg 122.6%, Aug avg 69.3%) but have negligible effect on total profit (weighted margin stays ~93%). They do distort margin-based monitoring.

## Bottom line: which aspects cause the instability?
1. **Order/volume seasonality (primary)**: total profit swings with order count (CV 5.2%) and quantity (5.5%); Feb trough (holiday) vs Aug–Dec peak explains most of the 152K range. Pricing, discounts, VAS and cost structure are all stable and are *not* the cause.
2. **Product mix (amplifier)**: Kitchen Appliances is the top volatility contributor (CV 20.5%, std 18,941; −66,650 in Feb = 58% of the Feb drop), followed by Home decor, Auto parts, Bedroom Furniture and high-CV Office furniture; Bedding set is the stabilizer.
3. **Geography mix (amplifier)**: small regions — especially the mislabeled Henan/Hubei/Hunan and small cities like Wuzhou, Zhengzhou, Qingyuan, Yangjiang, Foshan — have CVs of 17–69% and add disproportionate noise to the monthly total.
4. **Minor**: extreme per-order margin outliers distort margin KPIs (though not total profit), and total cost (only ~7% of revenue) is not a driver.

## Limitations
- No Python/figure generation available in this prototype; all conclusions are from SQL aggregations (no charts).
- Profit-margin analysis is affected by a handful of anomalous orders (negative/near-zero revenue).
- The "South China" classification in the data includes Henan/Hubei/Hunan; results reflect the dataset's own labeling.
