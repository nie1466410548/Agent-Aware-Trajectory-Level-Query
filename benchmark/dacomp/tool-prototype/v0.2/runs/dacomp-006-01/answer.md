# Why Monthly Total Profit in South China Is Unstable

## 1. Summary
In 2023, South China's monthly total profit ranged from **¥683.0k (Feb)** to **¥839.1k (Dec)**, with a mean of **¥794.3k**, a standard deviation of **¥46.7k**, and a coefficient of variation (CV) of **5.9%** — a spread of ~¥156k (≈20% of the mean) between the best and worst months. The instability is **not** caused by costs, discounts, or pricing. It is caused by **fluctuation in sales volume (quantity shipped)**, which is driven by three aspects: (1) erratic volume swings in specific product categories, (2) geographically concentrated demand (Guangdong + Guangxi ≈ 63% of profit), and (3) a strong seasonal dip in February that hits nearly every segment simultaneously.

## 2. Data and Method
- Single flat table (`sheet1`), 7,359 South-China rows in 2023-01-01..2023-12-31, 106 destination cities in 11 province-level areas, 8 product categories.
- Verified internally consistent: **Profit = Total Logistics Revenue − Total Logistics Cost for all 7,359 rows** (0 mismatches). No single-order outliers (per-order profit min −¥138, max ¥4,813; only 257 rows / 3.5% have non-positive profit, all small losses).
- No Python/figures available in this prototype, so all analysis is from SQL aggregations; charts/visualizations are a limitation.

## 3. Aspect 1 — Sales volume (the dominant lever)
Profit per unit is nearly constant across all months and all products (**¥24.7–¥27.0 per unit**). Therefore:

- Monthly profit tracks monthly quantity almost 1:1. Monthly quantity ranged from **27,454 (Feb)** to **33,496 (Aug)** (CV ≈ 6–7%), which matches the profit CV of 5.9%.
- Revenue is profit + small costs: costs are only ~6.4% of revenue, so profit volatility ≈ revenue/volume volatility.
- The dips are volume dips, not margin or price dips.

## 4. Aspect 2 — Product mix volatility
Monthly profit CV by product (descending):

| Product | Avg monthly profit | Std | CV | Min–Max |
|---|---|---|---|---|
| Office furniture | ¥13.5k | ¥5.1k | 37.5% | 6.7k–28.0k |
| **Kitchen Appliances** | **¥102.8k** | **¥18.3k** | **17.8%** | **73.6k–142.4k** |
| Bedroom Furniture | ¥94.9k | ¥14.3k | 15.1% | 63.9k–123.5k |
| Computer hardware | ¥91.7k | ¥13.6k | 14.9% | 72.0k–118.7k |
| Bathroom supplies | ¥117.5k | ¥15.0k | 12.7% | 96.8k–148.5k |
| Auto parts | ¥117.5k | ¥14.3k | 12.2% | 97.2k–143.5k |
| Home decor items | ¥105.1k | ¥12.4k | 11.8% | 85.6k–125.6k |
| Bedding set | ¥151.2k | ¥13.4k | 8.9% | 130.1k–174.3k |

- **Kitchen Appliances is the single most destabilizing category in absolute terms** (largest CV among the big categories; swings of ~¥70k between months). It alone accounted for **−¥66.6k of the February drop** and **−¥33.0k of the April drop**.
- **Home decor items** contributed **−¥25.4k** to the June drop; **Auto parts** −¥28.1k (Feb) and −¥30.7k (Apr); **Bedroom Furniture** −¥21.5k (Feb); **Bathroom supplies** −¥33.0k (Apr).
- **Bedding set**, the largest category, is the most stable of the majors (CV 8.9%) but still swings ±¥30–40k, adding noise.
- Office furniture is highly unstable relative to itself (CV 37.5%) but too small (avg ¥13.5k) to matter much for the total.

## 5. Aspect 3 — Geographic concentration
Province-level monthly profit:

| Province | Avg monthly profit | CV | Min–Max |
|---|---|---|---|
| Guangdong | ¥314.4k (~40% of total) | 8.5% | 264.7k–352.3k |
| Guangxi | ¥189.9k | 9.3% | 151.7k–215.0k |
| Henan | ¥86.3k | 16.6% | 60.4k–105.8k |
| Hainan | ¥57.2k | 20.0% | 44.0k–81.9k |
| Hubei | ¥47.8k | 22.9% | 33.0k–71.1k |
| Hunan | ¥40.6k | 19.2% | 25.4k–55.9k |
| Sichuan | ¥17.1k | 35.3% | 7.9k–27.6k |
| Guizhou | ¥15.9k | 34.0% | 8.7k–26.0k |
| Chongqing | ¥10.4k | 34.2% | 5.4k–15.5k |
| Yunnan | ¥9.4k | 38.1% | 2.1k–14.6k |
| Tibet | ¥5.3k | 54.4% | 0.9k–11.5k |

- **Guangdong alone contributes ~40% of South-China profit and has absolute swings of ~¥88k** (June low vs August high), the largest single geographic contributor to instability. Within Guangdong, **Guangzhou dominates** (~¥48k–75k/month), so Guangzhou demand swings move the whole region.
- Guangxi adds swings of ~¥63k; Henan ~¥45k; Hainan/Hubei/Hunan ~¥30–40k each.
- Small provinces (Tibet, Yunnan, Chongqing, Sichuan, Guizhou) have very high relative volatility (CV 34–54%) but small absolute impact — they add noise, not the main instability.

## 6. Aspect 4 — Customer segments
- **Gender:** Female segment is larger (avg ~¥422k vs ~¥369k male). Male is more volatile relatively: it jumped +¥102k in July and dropped −¥62k in February; Female dropped −¥79k in February. Both genders' swings align in the same months, reinforcing the total instability.
- **Age:** All age bands fluctuate in the same pattern; the 40–49 and 50–59 bands are the largest profit contributors, while 20–29 and 60–69 show proportionally larger swings. Demographics amplify, but do not originate, the instability.

## 7. Aspect 5 — Seasonality (February structural dip)
- February is the clear low month (−¥141k vs January, −¥123k vs March) — consistent with a Chinese New Year slowdown. The drop is **broad-based**: nearly every product (Kitchen Appliances −66.6k, Auto parts −28.1k, Home decor −25.2k, Bedroom Furniture −21.5k), every province, both genders, and all age groups fall together.
- The other dips (April −54.2k, June −55.2k) are **compositional**: they occur because volatile categories (Kitchen Appliances, Home decor, Bathroom, Auto parts) slump while others only partially offset (e.g., in April Computer hardware +30.6k and Home decor +22.7k partly offset Bathroom/Kitchen/Auto/Office declines).

## 8. Minor aspects (rule out)
- **Costs:** Freight is the largest cost component (~58% of total cost), followed by warehousing (~29%) and other operating costs (~12%), but total cost is only ~6.4% of revenue. Monthly cost changes (±¥3–8k) are an order of magnitude too small to drive ±¥100k profit swings.
- **Pricing/discounts:** Discounts are only ~0.7% of list-price revenue and are stable month-to-month; unit price is flat (~¥26/unit). Pricing policy is not a cause.
- **Promotional spikes:** Daily profit peaks are mild (max ~¥44k/day vs average ~¥26.5k/day); no single day or event dominates a month, so the instability is broad-based volume movement rather than isolated campaign spikes.

## 9. Conclusion — which aspects cause the instability
1. **Sales volume fluctuation is the underlying driver** (profit per unit is constant); everything else is secondary.
2. **Product mix**: Kitchen Appliances (and secondarily Home decor, Auto parts, Bedroom Furniture) are the most volatile large categories and account for the largest share of month-to-month swings.
3. **Geographic concentration**: Guangdong (esp. Guangzhou) and Guangxi together drive most of the absolute movement because they generate ~63% of profit; smaller provinces add high relative but low absolute noise.
4. **Seasonality**: the February dip is systemic (affects all segments) and is the single largest swing; the April and June dips are driven by simultaneous slumps in the volatile product categories.
5. Costs, discounts, and pricing are **not** material causes.

**Recommendation direction:** stabilizing profit requires smoothing volume — most impact would come from demand management/promotions for Kitchen Appliances and Home decor, and from monitoring Guangdong/Guangxi (especially Guangzhou) order intake; the February seasonal trough should be planned for rather than treated as an anomaly.
