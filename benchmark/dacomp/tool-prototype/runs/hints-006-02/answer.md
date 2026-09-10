# Why Is South China's Monthly Total Profit Unstable?

## 1. Data and Scope
- Source: `sheet1`, year 2023 (1 Jan – 31 Dec), 18,250 rows company-wide; 6,785 rows ship to destinations starting with "South China" (Guangdong, Guangxi, Hainan, Henan, Hubei, Hunan).
- All computations are monthly aggregates for South China only.
- **Limitation:** the environment provides SQL only (no Python/figures), and SQLite lacks a built-in `STDDEV` (CVs below were computed manually as σ = √(E[x²] − E[x]²)); no charts could be produced.

## 2. The Instability in Numbers
Monthly total profit (RMB): Feb **637,736** (min) → Mar 756,201 → Apr 684,254 → Jun 674,620 → Dec **789,694** (max).
Mean ≈ 736,146; σ ≈ 45,646; **CV ≈ 6.2%**; max–min spread ≈ 152,000 (~21% of mean). Troughs: February, June, April.

## 3. Root Cause #1 – Volume swings, NOT unit economics
Unit economics are rock-stable; the instability is a volume story:

| Metric (monthly) | CV |
|---|---|
| Profit per unit | **2.97%** |
| Profit per order | **3.78%** |
| Total profit | 6.20% |
| Sales quantity | **5.53%** |
| Order count | **5.23%** |
| Total revenue | 6.10% |
| Total logistics cost | 6.05% |

- Profit per unit hovers at ~25–27 across all 12 months; discounts per unit (~0.20), cost per unit (~1.87) and freight/warehousing per unit are nearly constant.
- Low-profit months are exactly the low-volume months: Feb (25,432 units / 512 orders), Jun (26,628 / 526), Apr (27,028 / 554); high-profit months are high-volume: Aug (30,983 / 603), Mar (30,395 / 610), Dec (29,586 / 600).
- Since profit ≈ 26 × quantity with a stable margin, monthly profit inherits the volatility of shipment volume. Cost-side components (CV ≈ 5–7%) move in lockstep with revenue and do not add extra variance.

## 4. Root Cause #2 – Province mix: small provinces are far more volatile
| Province | Share of SC profit | Monthly CV |
|---|---|---|
| Guangdong | 37.7% | 8.5% |
| Guangxi | 22.8% | 9.4% |
| Henan | 10.4% | **16.6%** |
| Hainan | 6.9% | **20.0%** |
| Hubei | 5.7% | **22.9%** |
| Hunan | 4.9% | **19.2%** |

- The four smaller provinces are 2–3× more volatile than Guangdong/Guangxi (e.g., Hainan 43,977–81,926; Hubei 33,017–71,084; Hunan 25,374–55,948).
- Decomposing the **February crash** (−114,974 vs Jan): Henan −40,427, Guangxi −35,141, Hainan −17,435, Guangdong −19,883, Hubei −1,901, Hunan −187 — a broad-based collapse, consistent with a Spring-Festival slowdown, with Henan and Guangxi the largest contributors.
- The **April dip** is driven by Henan (−32,688), Guangxi (−32,471) and Hainan (−29,309) — Guangdong actually rose.
- The **June dip** is driven by Guangdong (−23,052), Hubei (−21,929) and Henan (−13,210).

## 5. Root Cause #3 – Product mix: several large, volatile categories
| Product | Share of SC profit | Monthly CV |
|---|---|---|
| Office furniture | 1.6% | **40.9%** |
| Kitchen Appliances | 11.1% | **20.5%** |
| Bedroom Furniture | 10.5% | **15.4%** |
| Computer hardware | 10.3% | **14.9%** |
| Bathroom supplies | 13.2% | 13.8% |
| Home decor items | 11.8% | 12.3% |
| Auto parts | 12.9% | 11.5% |
| Bedding set | 17.1% | 9.4% |

- Kitchen Appliances (CV 20.5%, ~11% of profit) is the largest volatile category — e.g., it swings between ~60,725 and ~127,375 per month; Bedroom Furniture and Computer hardware (CV ~15%, ~10% each) add further swings.
- Office furniture is extremely erratic (CV 41%) but so small (1.6%) that its absolute impact is minor — it mostly adds noise.

## 6. Root Cause #4 – Customer-segment volatility
- **Age:** 60–69 has CV 21.8% (small share, 6.6%); 50–59 CV 12.6%; 30–39 CV 11.6%; 20–29 CV 10.9%; only 40–49 (22.2% share) is stable at CV 8.8%.
- **Gender:** male customers CV 10.6% vs female CV 6.1% — male-driven demand fluctuates more.

## 7. Conclusions / Key Aspects Causing the Instability
1. **Volume, not pricing or cost**: unit profit, unit cost, discounts and margin are stable; monthly profit moves almost 1:1 with monthly sales quantity/order count (CV ≈ 5.5%). Any demand fluctuation translates directly into profit swings.
2. **February seasonal trough** (likely Spring Festival): all six provinces drop simultaneously, producing the year's minimum (−12.6% vs the annual mean).
3. **Province mix**: the smaller provinces (Hainan, Hubei, Hunan, Henan — CV 16–23%) are inherently much more volatile than Guangdong/Guangxi, and their individual swings dominate the dips of Feb, Apr and Jun.
4. **Product mix**: Kitchen Appliances, Bedroom Furniture and Computer hardware (together ~32% of profit) are the volatile large categories; Office furniture is the most volatile but negligible in size.
5. **Demographics**: older (60–69) and male customers bring proportionally more variance to demand.

**Recommendation direction:** stabilize shipment volume planning for volatile provinces/products (e.g., promotion/booking smoothing for Henan, Guangxi, Hainan; Kitchen Appliances, Bedroom Furniture, Computer hardware) and manage February seasonality explicitly; unit economics need no correction since they are already stable.