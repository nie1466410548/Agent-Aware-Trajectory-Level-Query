# Why Is South China's Monthly Profit So Unstable? (2023 Root-Cause Analysis)

## 1. Scope, data and method
- Source: `sheet1`, 10,000,000 waybills, 2023‑01‑01 → 2023‑12‑31, 277 destinations coded `"Region-Province-City"`.
- **South China = the 73 destinations with prefix `South China-`**: 3,717,808 orders (37.2% of company volume) and 4,840.4M profit (37.4% of company profit).
- Accounting identities verified on the data: `Profit = Total Logistics Revenue − Total Logistics Cost`; `Revenue = List Price Revenue + Value‑Added Service Revenue − Discount`; `Cost = Freight + Warehousing + Other`.
- Volatility measured on the 12 monthly aggregates (CV = std/mean, min–max range, month‑over‑month deltas). All figures below were computed by hand from the SQL result sets — **no Python/figures were available in this environment**, so all statistics are manual calculations (CVs use the population formula on 12 points; expect ±rounding).

## 2. The instability, quantified
| Month | Orders | Revenue (M) | Cost (M) | Profit (M) | Δ MoM (M) |
|---|---|---|---|---|---|
| Jan | 313,974 | 441.8 | 29.4 | 412.4 | — |
| Feb | 280,544 | 375.2 | 25.8 | **349.4** | **−63.0 (−15.3%)** |
| Mar | 334,249 | 445.9 | 31.6 | 414.4 | +64.9 (+18.6%) |
| Apr | 303,560 | 403.0 | 28.1 | 374.9 | −39.4 (−9.5%) |
| May | 305,211 | 419.5 | 28.6 | 391.0 | +16.0 |
| Jun | 288,216 | 396.9 | 27.3 | 369.6 | −21.3 |
| Jul | 315,067 | 452.9 | 29.3 | 423.5 | +53.9 (+14.6%) |
| Aug | 330,416 | 456.4 | 31.9 | 424.5 | +1.0 |
| Sep | 302,465 | 449.2 | 27.7 | 421.5 | −3.0 |
| Oct | 319,456 | 448.6 | 30.0 | 418.6 | −2.9 |
| Nov | 295,879 | 435.3 | 27.6 | 407.7 | −11.0 |
| Dec | 328,771 | 463.2 | 30.5 | 432.7 | +25.0 |

Mean 403.4M, std ≈ 25M, **CV ≈ 6.2%**; range 349.4–432.7M (1.24×); mean absolute MoM change ≈ 27.3M (~6.8% of a typical month). Context: peer regions' profit CVs are East 7.4%, North 7.6%, Northeast 8.1%, Northwest 10.6%, Southwest 14.1% — South China is mid‑pack *relatively*, but its **absolute swings are the largest in the company** (the Feb −63M swing alone ≈ 2× Southwest's entire monthly profit) simply because it is the biggest region.

## 3. Costs are exonerated
- Total cost per order: 91.5–96.6 (**CV ≈ 1.8%**); cost is only 6.6–7.0% of revenue; **profit margin is locked at 92.9–93.8% every single month**.
- Freight/order 52.7–57.6, warehousing/order 27.2–28.3, other operating/order 10.7–11.3 — all flat. Value‑added service revenue (~25/order) and discounts (~10/order) are tiny and stable.
- ➜ Essentially **100% of the profit instability comes from the revenue side** (list‑price revenue), not from costs, services or discounting.

## 4. Revenue instability = volume × price
| Factor | Range (12 months) | CV |
|---|---|---|
| Orders | 280,544 – 334,249 | **5.3%** (main driver) |
| Units per order | 48.5 – 51.9 | ~2% (minor) |
| Avg unit price (revenue/qty) | 26.63 – 28.49 | ~±3.5% (amplifier) |
| Profit per order | 1,235 – 1,394 | ~4.5% |

Example — the February crash is a *combination*: orders −10.6% vs Jan **and** unit price −4.3% (weighted 27.83→26.63) ⇒ revenue −15.1%.

## 5. Cause 1 — Asynchronous product‑category cycles (dominant cause)
Monthly profit CV by product (South China):
| Product | Mean profit (M/mo) | CV | Signature swing |
|---|---|---|---|
| Kitchen Appliances | 50.6 | **20.5%** | Feb −52% vs Jan (69.8→33.3M): orders −34.5% **and** unit price −14.6% (30.55→26.09) |
| Office furniture | 7.1 | **40.9%** | Mar spike 2.8× (revenue 5.8→16.0M), then −61% in Apr |
| Bedroom Furniture | 48.0 | 15.4% | Oct +30.6% |
| Computer hardware | 46.9 | 14.9% | Jul +31.9% (orders +26%), Aug −37.6% |
| Bathroom supplies | 60.2 | 13.8% | Oct −33.7% |
| Home decor items | 53.8 | 12.3% | Feb −25.6% (price −16%) |
| Auto parts | 58.9 | 11.5% | Feb −16.4%, Mar→Apr −25.2% |
| Bedding set | 77.9 | 9.4% | The **stabilizer**: orders nearly flat (54.8–67.4K) |

Because the categories cycle **out of sync**, the total (CV 6.2%) is far steadier than any product — but when several fall together the total crashes:
- **Feb (−63.0M)**: Kitchen −36.5M + Home decor −17.0M + Auto −10.2M + Bedroom −7.5M, only +8.2M offset (Computer/Bedding/Office/Bathroom up).
- **Mar (+64.9M)**: Kitchen +22.5M, Auto +17.3M, Bathroom +12.8M, Bedroom +8.6M, Office +10.0M (spike), Bedding −12.2M.
- **Apr (−39.4M)**: Kitchen −20.5M, Bathroom −21.2M, Auto −17.4M, Office −9.4M vs Computer +11.2M, Bedroom +8.5M, Home decor +8.2M.
- **Jul (+53.9M)**: Computer +15.0M, Kitchen +13.6M, Auto +11.9M. **Aug**: Computer alone −23.2M. **Oct**: Bathroom −25.2M, Bedroom +15.1M.

## 6. Cause 2 — Geography: city concentration + misassigned "South China" label
- **Concentration**: top‑3 cities (Beihai 318.9K, Guangzhou 274.0K, Meizhou 180.8K orders) = 20.8% of volume; top‑12 = 48.8%. Beihai alone swings 22.4M (Apr) → 46.0M (Oct), incl. **Sep→Oct +74% (orders +117%)**; Guangzhou 22.7–41.2M (Oct→Nov +36% on **falling** orders — per‑order value 1,087→1,881); Meizhou Aug→Sep +120%, Sep→Oct −58%.
- **Data‑quality amplifier**: 39 of the 73 "South China" cities are actually in **Henan/Hubei/Hunan** (Central China) — ~888K orders (23.9% of volume, ~1,149M profit). This "central" group is far more volatile than the true GD/GX/Hainan core: **profit CV 12.0% vs 7.0%** (orders CV 10.0% vs 5.6%), and its cycle is **asynchronous** with the core:
  - Apr: central −22.8M vs core −16.6M (both fell; central deepened the dip);
  - May: central **+33.9M** while core **−17.8M** (masked a core slump);
  - Oct→Nov: central **−34.2M** while core +23.2M (created the Nov drop);
  - Feb is the only month both fell together (core −39.7M, central −23.3M).
  - Extremes: Anyang 3.6M→19.9M (5.5×), Zhengzhou 2.1M→14.8M→3.1M within 3 months, Yichang 0.07M→5.75M (87×); some city‑months are **negative** (Jingzhou Jan −45.2K, Luohe Jan −21.8K, Xinxiang Nov −27.9K).

## 7. Cause 3 — Seasonality (a systematic component)
The February trough is common to most regions (East −6.4%, North −12.3%, Northwest −13.6%, Southwest −22.2% vs their means; Chinese‑New‑Year effect) — but South China compounds it with its own Kitchen/price weakness, producing the company's largest single swing (−63M, +18.6% rebound in Mar).

## 8. Non‑causes checked
- **Cost components**: stable (§3). **Discounts/VAS**: negligible and flat.
- **Customer demographics**: gender and age bands move with the market, not independently (Female −16.1% and Male −14.5% in Feb, mirroring the total). Age 20–29 is the most volatile band (CV 11.0% vs 8.9% for 40–49) but is an amplifier, not a driver.
- **Single large orders**: impossible — monthly totals are built from ~280–334K waybills averaging ~1,270 profit each; swings are aggregate demand phenomena.

## 9. Conclusion — ranked causes of South China's profit instability
1. **Volatile product mix**: Kitchen Appliances (CV 20.5%, the single biggest contributor) plus Auto parts, Bathroom supplies, Computer hardware, Bedroom Furniture and Home decor swing ±25–50% month to month; the total crashes/rebounds when several categories move together (Feb, Mar, Apr, Jul).
2. **Unit‑price swings that amplify volume**: product‑level prices move ±5–16% between months (Kitchen −14.6% and Home decor −16% in Feb), so the same month gets hit by fewer orders *and* lower prices; units per order and per‑order costs are stable.
3. **Geographic structure**: heavy city concentration (top‑3 = 21% of orders, each city's profit swings ~2×), plus **39 Henan/Hubei/Hunan cities mislabeled as "South China" (24% of volume) whose asynchronous, higher‑volatility cycles (CV 12% vs 7%) distort the region's monthly totals** — including negative‑profit city‑months. The region label should be audited and this group forecast separately.
4. **Seasonality**: a systematic February (CNY) dip shared with other regions, magnified here by South China's size and Kitchen/price weakness.
5. **Small‑base noise**: Office furniture (1.7% of profit, CV 41%, 2.8× March spike) and micro‑cities add spikes that are visible in the total.
6. **Explicitly not causes**: logistics costs (stable ~7% of revenue, margin 92.9–93.8% every month), value‑added services, discounts, and customer gender/age mix.

Practical implication: stabilizing South China's monthly profit means (a) smoothing the Kitchen Appliances demand/price cycle, (b) enforcing price discipline in Kitchen/Home decor, (c) diversifying the Beihai/Guangzhou/Meizhou concentration, and (d) excluding or separately managing the misassigned Central‑China cities from the "South China" P&L.

## 10. Limitations
- This prototype provides SQL and report submission only — **no Python or chart generation**; all statistics (CVs, decompositions, factor math) were computed manually from query results and rounded to 0.1M.
- Volatility metrics use 12 monthly observations (population CV); no statistical significance tests or formal variance decomposition were possible.
- "South China" is taken as the region label present in the data; the misassignment of Central‑China cities is documented but not corrected in the aggregates. Causality is inferred from co‑movement of aggregates, not from causal models.
