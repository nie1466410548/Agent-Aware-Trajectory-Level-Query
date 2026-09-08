# Low-Margin Order Analysis — sheet1 (2023 logistics orders)

## 1. Definition and scale of the problem

- Dataset: **18,250 orders** in `sheet1`, covering `Date` 2023-01-01 to 2023-12-31.
- `Profit Margin` equals `Profit` / `Total Logistics Revenue` (verified row-by-row). Dataset average `Profit Margin` = **0.7953**, so the low-margin threshold (50% of the average) is **0.3976**.
- **Low-margin orders: 1,243 (6.81% of all orders).**
- These orders generate only **0.48% of total `Total Logistics Revenue`** (122,160 of 25,329,355) and their aggregate `Profit` is **−7,374.06**, i.e. the segment as a whole is *net loss-making*. 646 of the 1,243 low-margin orders (52%) have negative `Profit`, with a combined loss of **−27,592.21**.
- Normal orders (17,007) average a `Profit` of +1,389.20; only 4 of them are loss-making.

## 2. Salient characteristics of low-margin orders

### 2.1 Small `Sales Quantity` is the dominant driver

Per-order `Total Logistics Cost` is essentially **independent of `Sales Quantity`** (Spearman correlation ≈ −0.006): the average cost is ~93 per order in every quantity band. Revenue, by contrast, scales with quantity. The result is a collapse in cost per unit and margin as quantity falls:

| `Sales Quantity` band | Orders | Low-margin rate | Avg `Profit Margin` | Avg `Total Logistics Revenue` | Avg `Total Logistics Cost` | Cost per unit |
|---|---|---|---|---|---|---|
| 1–5 | 905 | **78.2%** | −0.41 | 95 | 93 | 43.70 |
| 6–10 | 936 | 31.8% | 0.40 | 230 | 95 | 12.36 |
| 11–15 | 918 | 10.9% | 0.67 | 381 | 93 | 7.25 |
| 16–20 | 878 | 8.4% | 0.73 | 496 | 95 | 5.30 |
| 21–25 | 910 | 4.2% | 0.80 | 652 | 94 | 4.10 |
| 26–30 | 962 | 1.9% | 0.84 | 802 | 93 | 3.31 |
| 31–35 | 927 | 0.65% | 0.86 | 923 | 93 | 2.81 |
| 36–50 | 2,809 | 0.04% | 0.89 | 1,194 | 95 | 2.22 |
| 51–99 | 9,005 | 0.00% | 0.93 | 2,073 | 94 | 1.30 |

- **80.9% of low-margin orders have `Sales Quantity` ≤ 10; 99.8% have `Sales Quantity` ≤ 32.** Above quantity 33 the low-margin rate is effectively zero.
- Average low-margin order: `Sales Quantity` 6.7 vs 53.2 for normal orders; average `Total Logistics Revenue` 98.3 vs 1,482.2, while average `Total Logistics Cost` is actually *higher* (104.2 vs 93.0).

### 2.2 Aggressive discounting compounds the problem

- Median discount rate (`Discount Amount` / `List Price Revenue`): **11.9% for low-margin orders vs 0.74% for normal orders**. 78.8% of low-margin orders have a discount rate above 5%, vs only 4.5% of normal orders.
- The low-margin rate rises monotonically with discount depth: ≤2% discount → 0.7% low-margin; 5–10% → 29.2%; 10–20% → 73.9%; 20–50% → **97.0%**; >50% → **100%** (avg margin −2.99).
- Note: the average absolute `Discount Amount` is nearly identical (10.1 vs 10.0); it is only devastating on small-basket orders where it erases a large share of a small `List Price Revenue`.

### 2.3 Cost components: same structure, slightly higher level

- Average per-order costs, low-margin vs normal: `Freight Cost` 63.3 vs 54.4; `Warehousing Cost` 29.7 vs 27.5; `Other Operating Costs` 11.2 vs 11.0; `Total Logistics Cost` 104.2 vs 93.0.
- The cost *mix* is essentially identical (Freight ≈ 60%, Warehousing ≈ 29%, Other ≈ 11–12% in both groups), so low margins are **not** caused by a different cost structure — they are caused by spreading an order-level cost of ~93–104 over a tiny revenue base (see cost_components.png).
- `Logistics Value-Added Service Revenue` is almost flat per order (23.7 low vs 25.0 normal), so it makes up **33% of revenue** on low-margin orders vs 3.3% on normal orders — value-added services are currently the main thing keeping small orders from being even worse.

### 2.4 Geography, demographics, product and time are NOT differentiators

- Region-level low-margin rates are tightly clustered (6.6%–7.1% across the six regions in `Destination`); the highest city rate (Northwest-Gansu Province-Jiuquan, 26.7%) rests on only 30 orders and is consistent with small-sample noise.
- `Customer Gender` × `Age Range` cells range only from 5.4% to 8.1% low-margin; average `Customer Age` is 42.3 (low) vs 42.0 (normal).
- `Consigned Product` low-margin rates span just 5.1%–7.1% across all eight categories, with near-identical average quantities — no product effect.
- Monthly low-margin rate is stable (5.8%–8.3%), with a mild improvement toward year-end (Dec 5.8% vs Mar 8.3%); no structural time trend (see low_margin_overview.png).

## 3. Data-backed remedies

### 3.1 Cost control (beating down expense)

1. **Enforce a minimum order quantity / order consolidation for small orders.** Because `Total Logistics Cost` (~93–104 per order) does not fall with quantity, the fix is volume per shipment, not cost engineering per se. Simulation: if every low-margin order were consolidated to `Sales Quantity` = 20 at its observed per-unit revenue, the segment would move from −7,374 to **+454,425 in aggregate `Profit`**, with 97.2% of orders profitable. Median quantity needed to reach the 0.3976 threshold margin is only **10 units** (vs the current median of 5); to reach the dataset-average margin it is **28 units**.
2. **Attack `Freight Cost`, the largest component (~60% of cost in both groups).** Low-margin orders carry an average `Freight Cost` of 63.3 — 16% above the normal-order average of 54.4 — despite being much smaller shipments. Route consolidation, batching small orders by `Destination`/postal code, and renegotiating per-shipment (rather than per-unit) carrier rates directly target this. A uniform **20% cost reduction** on low-margin orders flips the segment from −7,374 to **+18,533** and makes 62.1% of them profitable on its own.
3. **Introduce a small-order surcharge or handling fee** calibrated to the observed cost floor: any order whose `Total Logistics Revenue` is below ~173 (the average revenue needed to cover average cost at the 0.3976 threshold margin) should either pay a surcharge covering the gap to `Total Logistics Cost` or be bundled.

### 3.2 Revenue / profit uplift (efficiency and effectiveness)

1. **Cap and target discounts.** Discounting above 10% of `List Price Revenue` is almost perfectly associated with low margins (73.9%→100% low-margin rate) while delivering orders that average 3.9–7.9 units. Remove discretionary discounts on baskets below ~20 units and cap discount rates at 5%. Simulation: simply removing the `Discount Amount` from low-margin orders moves the segment from −7,374 to **+5,234** (560 orders would still be loss-making, which is why discount control must be paired with the quantity fix).
2. **Protect and expand `Logistics Value-Added Service Revenue` on small orders.** VAS revenue is the one revenue line that does not shrink with quantity (~24–25 per order) and already represents 33% of small-order revenue. Bundling VAS (insurance, packaging, priority handling) into every sub-20-unit order is pure margin uplift at zero additional `Freight Cost`.
3. **Steer customers to larger baskets** (volume-tiered pricing, free-shipping thresholds set at `Sales Quantity` ≥ 20, bundle offers across the eight `Consigned Product` categories). The quantity-band table shows the margin curve steepens exactly in the 5–25 range, so even modest basket-size increases move orders out of the danger zone.
4. **No demographic, geographic or seasonal targeting is warranted**: `Age Range`, `Customer Gender`, `Destination` region, `Consigned Product` and month all show flat low-margin rates, so remedies should be applied uniformly to the small-order/high-discount mechanics rather than to customer segments.

## 4. Limitations

- `Profit Margin` values exceed 1.0 for some orders (max 255.3), indicating occasional revenue-side anomalies (e.g., near-zero or inconsistent cost/revenue recording); the average-based threshold is sensitive to this, but results were cross-checked against quantity bands and are robust.
- The consolidation simulations assume per-unit revenue stays constant when orders are merged and that costs are truly order-level fixed — the data (cost independent of quantity, Spearman ≈ −0.006) supports this, but real capacity/pick costs may scale partially with units.
- `Destination` has 277 distinct values, so city-level rates are noisy; only region-level geography was judged reliable.
- The dataset covers a single year (2023); the mild year-end improvement cannot be confirmed as a durable trend.
- `Postal Code`, `Waybill Number` and `Consignee` were not analytically used (identifiers/high-cardinality fields with no margin signal expected).

## Figures

- `low_margin_overview.png` — low-margin rate vs `Sales Quantity`; discount-rate distributions; revenue-vs-cost scatter with threshold line; monthly low-margin rate.
- `cost_components.png` — average `Freight Cost`, `Warehousing Cost`, `Other Operating Costs` per order, low-margin vs normal.
