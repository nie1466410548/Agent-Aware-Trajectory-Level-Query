# Why Is South China's Monthly Total Profit Unstable?

**Data:** 1,000,000 waybills, Jan–Dec 2023; South China = rows with `Destination` starting "South China-" → **371,782 orders**, total profit **¥483.97M**.
**Method:** Because Python/plots are unavailable, all statistics were computed in SQL. Instability was decomposed with an exact covariance identity: since profit is the sum of mutually exclusive parts, `Var(total) = Σ Cov(part_m, total_m)`, so each aspect's share of monthly profit variance (shares sum to 100%) could be measured. Variance uses the population convention (÷12 months).

## 1. The monthly pattern

| Stat | Value |
|---|---|
| Mean monthly profit | ¥40.33M |
| Min / Max | ¥34.93M (Feb) / ¥43.28M (Dec) |
| Std dev | ¥2.50M → **CV ≈ 6.2%** |
| Range | ¥8.35M ≈ 20.7% of mean |

Clear trough months: **Feb (−13%), Jun (−8%), Apr (−7%)**; peak: **Dec (+7%)**. Profit = Total Revenue − Total Cost, and the identity was verified: Revenue = List Price + Value-Added Services − Discount; Cost = Freight + Warehousing + Other.

## 2. Findings — what causes the instability

**(a) It is a revenue problem, not a cost problem.** Decomposing monthly profit variance by P&L line: **list-price revenue +104.5%**, VAS revenue +1.2%, discount −0.4%, freight cost **−3.3%**, warehousing −1.4%, other operating cost −0.6%. All three cost lines (and discounts) move *with* revenue and therefore **dampen** the swings — total cost stays in a narrow ¥2.58M–3.19M band while revenue swings ¥37.5M–46.3M. Nothing on the cost side is destabilizing profit.

**(b) The revenue swings are a volume phenomenon, not a pricing one.** Splitting profit = quantity × unit profit: **volume contributes 78.0%** of the variance, unit economics 23.8% (interaction −1.7%). CV of monthly quantity ≈ 5.5% (1.39M–1.70M units) and of order count ≈ 8.7% (28,053–33,426 orders), versus only ≈ 3.0% for profit per unit (¥24.9–26.9). Unit margins are steady; **the number of shipments per month is what moves**.

**(c) Product mix — three products drive ~62% of the volatility.**
| Product | Profit share | Variance contribution |
|---|---|---|
| Kitchen Appliances | 12.6% | **26.7%** |
| Auto parts | 14.6% | **18.8%** |
| Bedroom Furniture | 11.9% | **16.7%** |
| Bathroom supplies | 14.9% | 12.7% |
| Bedding set | 19.3% | 11.2% |
| Home decor / Computer hardware / Office furniture | 26.7% | 13.9% |

Kitchen Appliances swings hardest: ¥6.97M (Jan) → ¥3.33M (Feb, −52% vs Jan), alone explaining ~57% of the Jan→Feb regional drop. The largest product, Bedding set, is disproportionately stable.

**(d) Geographic concentration — a few mid-sized cities, not the big hub.** Top contributors: **Foshan 13.3%** of variance with only 3.2% of profit, **Beihai 12.6%** (8.3% share), **Meizhou 9.7%** (4.6%), Haikou 8.0%, Yangjiang 7.2%, Wuzhou 7.0%… The top-12 cities account for 86% of all variance. Guangzhou — the largest city (~7.3% of profit) — is *not* in the top 12: the big base is stable, while smaller cities whipsaw. Foshan is extreme: its monthly profit runs ¥0.30M (May, only 439 orders vs ~950 typical) to ¥2.21M (Oct) — **CV ≈ 38%** — and its Apr–Jun collapse coincides exactly with the region's trough months.

**(e) Customer mix amplifies it.** The **50-59 age band contributes 37.3%** of variance with only 24.3% of profit (1.5× over-index); 30-39 and 40-49 are neutral; 60-69 is counter-cyclical (−0.7%, a mild stabilizer). By gender, **male customers contribute 67.7%** of variance with 47.0% of profit.

**(f) Not outliers.** Loss-making orders total only −¥0.56M (0.12% of profit; 12,870 of 371,782 orders); per-order profit spans just −¥138 to +¥4,813 (avg ¥1,302). The instability is in aggregate volume, not a few extreme waybills.

## 3. Context

Relative to its size, South China is actually the **most stable** region in 2023 (CV 6.2% vs Southwest 14.1%, Northwest 10.5%, Northeast 8.0%, North China 7.6%, East China 7.4%). Its instability *feels* severe because it is the largest region — its ¥8.35M absolute monthly range dwarfs every other region — so the swings above dominate company-level volatility.

## 4. Conclusion & recommendations

**Root cause:** South China's monthly profit is unstable because **order/shipment volume fluctuates** (≈78% of variance), concentrated in **three products** (Kitchen Appliances, Auto parts, Bedroom Furniture ≈ 62%), a **handful of volatile mid-sized cities** (Foshan, Beihai, Meizhou ≈ 36%; top-12 ≈ 86%), and the **50-59 male customer segment**, while unit margins and all cost lines are stable and even cushion the swings. Data also flags a hygiene issue: the "South China" prefix contains Hubei/Henan/Hunan cities, so the regional label is inconsistent.

1. Investigate Foshan's Apr–Jun collapse (May: −76% vs its mean) — a fulfillment/route disruption is more plausible than demand seasonality.
2. Smooth demand for Kitchen Appliances / Auto parts / Bedroom Furniture (Feb & Apr–Jun promotions, inventory pre-builds); grow the stable Bedding set base.
3. Reduce geographic concentration risk; diversify volume beyond volatile mid-tier cities.
4. Focus retention on the 50-59 male segment; the 60-69 band behaves counter-cyclically and stabilizes revenue.
5. Costs need no intervention — they already act as a natural stabilizer.

**Limitations:** No Python/figure generation was available; all statistics (means, variances, covariance-share decompositions, CVs) were computed directly in SQL from the retrieved monthly aggregates, and charts cannot be embedded. Only 12 monthly observations underlie the variance estimates, and the analysis is descriptive — it quantifies which aspects move profit, but cannot prove causal mechanisms (e.g., why Foshan collapsed in May).