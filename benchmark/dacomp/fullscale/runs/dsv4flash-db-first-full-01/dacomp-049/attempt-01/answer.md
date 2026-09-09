# Competitiveness Evaluation — PICC Life Insurance After-sales Department Establishment Manager (Xiamen)

**Prepared for:** HR, insurance industry · **Method:** horizontal (cross-position) comparison within the insurance industry · **Data source:** Xiamen recruitment postings database (5,004 records)

## 1. Executive summary

Compared against 16 comparable insurance-industry postings in Xiamen (China Life, Ping An Life, Taiping Life/Property, Sunshine Property, Dajia Property, Junlong Life) and against the full Xiamen market, the PICC Life **After-sales Department Establishment Manager** (¥30,000–50,000/month, base ¥24,000–30,000 + commission) is an **extreme pay outlier** — its midpoint (¥40,000) exceeds the peer median (¥6,500) by **6.2×** and sits above **~99.6% of all Xiamen job postings**. The main competitive weaknesses are structural: the statutory welfare package (“three insurances + housing fund”, no paid annual leave/performance bonus listed) is *thinner* than the near-universal “five social insurances + housing fund” among peers, and the combined experience-plus-income screening bar (≥3 yrs same industry or ≥1 yr supervisor **and** personal after-tax income >¥50,000/yr) is stricter than most peer ads.

| Dimension | Target position | Insurance peers (n=16) | Assessment |
|---|---|---|---|
| Salary range | 30,000–50,000 (mid 40,000) | median mid 6,500; max 15,000 | **Strong strength** (~6.2× peer median) |
| Education | Associate degree or above | 9/16 Bachelor+, 4/16 College+, 2/16 no limit | **Slight strength** (more lenient, larger pool) |
| Experience | ≥3 yrs same industry OR ≥1 yr supervisor + income gate | 8/16 no limit; 5/16 >1 yr; 2/16 ≥3 yrs | **Weakness** (stricter screen) |
| Age | 25–50 | 10/16 unspecified; most ≤45 | **Neutral/strength** (broad window) |
| Gender / Language | None | none / 2 female-pref | Parity |
| Benefits | 9 listed items + 三险一金 | 五险一金 11/16, paid leave 9/16, bonus 8/16 | **Mixed** (flexibility strong; statutory welfare thin) |
| Company type | State-owned (PICC) | 7/16 SOE, 5/16 listed | Aligned with largest peer cluster |
| Working hours | Mon–Fri, flexible afternoons, no overtime | standard 8-hr; only 3/16 flexible | **Strength** |

## 2. Methodology and comparison set

The target posting itself is not stored in the database (it is the company's own vacancy being benchmarked). The peer set = **16 genuine insurance-industry positions** in the database (companies whose industry field contains insurance *and* that are actual insurers; noise rows — e.g., real-estate agencies, pharmaceutical, ICT companies whose Industry cell was contaminated with benefit text — were excluded). Peer companies: China Life (5), Taiping Property/Life (4), Sunshine Property (3), Dajia Property (2), Ping An Life (2).

Salary strings were parsed to numeric ranges with regex in Python (SQLite has no regex engine); statistics were computed on the midpoint of the headline range. Four figures were produced:

- `fig1_salary_comparison.png` — salary bars of all 16 peers vs the target
- `fig2_education.png` — education-requirement distribution among peers
- `fig3_benefits.png` — benefit-package coverage (red = offered by target)
- `fig4_market_context.png` — full Xiamen salary distribution vs target range

## 3. Compensation competitiveness

**Peer salary landscape (12 of 16 peers disclosed salary):** median midpoint ¥6,500, mean ¥8,104, P25 ¥6,000, P75 ¥8,875, max ¥15,000. The two highest peers (Ping An Insurance Agent and Sunshine Telemarketing credit specialist, both ¥10,000–20,000) are **commission-driven agent roles with thin base pay** (Ping An base ¥5,000–10,000; Sunshine base ¥1,500–3,000), not guaranteed managerial salary. The closest management comparator, Sunshine **Branch Manager**, discloses no salary.

**Target vs peers:** target floor ¥30,000 = **4.6×** the peer median midpoint (¥6,500); target ceiling ¥50,000 = **3.3×** the highest peer ceiling (¥15,000). The guaranteed base alone (¥24,000–30,000) exceeds every peer's entire headline range. The only listed peer with comparable *uncapped* upside is Ping An's agent program (annual ¥650,000 claim in year one), but its base is far lower.

**Market context (n=4,119 postings with salary):** median ¥6,500, P90 ¥12,500, P95 ¥15,000, max ¥75,000. Only **0.83%** of all Xiamen postings reach a midpoint ≥¥30,000 and **0.36%** ≥¥40,000. The target's midpoint (¥40,000) is above **99.6%** of the entire market — a powerful recruiting magnet, but it also signals a "top-sales-hire" premium consistent with the income-gate and commission structure.

## 4. Benefits-system comparison

Target lists: commercial insurance, business trip allowance, holiday benefits, professional training, flexible working hours, employee travel, overseas opportunities, **no overtime, no probation period**; plus in the description **three insurances and one housing fund**, full company-resource support, and **four promotion opportunities per year**.

**Peer coverage of standard benefits** (see `fig3_benefits.png`):
- Commercial insurance — 12/16 → target ✓
- Five social insurances + housing fund (五险一金) — **11/16** → target only offers 三险一金 ⚠ **gap**
- Paid annual leave — **9/16** → not explicitly listed ⚠ **gap**
- Performance bonus — **8/16** → not explicitly listed ⚠ **gap**
- Communication allowance (7/16), meal allowance (6/16), transportation allowance (3/16) → not listed ⚠
- Professional training (6/16), holiday benefits (6/16), regular medical check-up (6/16) → ✓ / partial
- Employee travel (5/16), flexible working hours (3/16) → ✓ (flexibility is a differentiator; only 3 peers offer it)
- Year-end bonus (2/16), overtime pay (1/16) → target advertises "no overtime", a rare positive

**Verdict:** the target's *peripheral* welfare (flexibility, travel, training, no probation/overtime) is **above industry practice**, but its *statutory* package (三险一金) and absence of listed paid annual leave and performance/communication/meal allowances place it **below the 五险一金 standard** that 69% of peers advertise. This is the single most likely benefit-level objection from candidates and a clear remediation target.

## 5. Job-requirement competitiveness

- **Education** (`fig2_education.png`): 9/16 peers require Bachelor's+; the target's **Associate-degree floor** is more lenient than 56% of peers, widening the eligible pool — a mild advantage for fillability, though it may signal lower credential rigor than peer management roles.
- **Experience**: only 3/16 peers demand ≥3 yrs; the target's rule (≥3 yrs same industry OR ≥1 yr as supervisor) is **stricter than most**, and the additional hard screen of **personal after-tax income >¥50,000 in the past year** (≈¥4,167+/month net) is **unique among peers** — effectively targeting already-successful sales producers. This narrows the candidate pool and should be weighed against the 2-position headcount.
- **Age**: 25–50 is broader (upper bound 50 vs peers' 25–45 typical, one 22–50) — accommodates experienced, mid/late-career managers; aligns with the "establishment manager" maturity needed.
- **Gender/language**: none required — parity with peers (2 peer ads preferred female; none require foreign languages).
- **Employment type/location**: full-time; Xiamen (Haicang, Jimei, Xiang'an) with the same multi-district coverage as peer roles; working hours (Mon–Fri, free afternoons) are more flexible than the standard 8-hour day.

## 6. Competitive strengths & weaknesses

**Strengths (leverage in outreach):**
1. Pay leadership — guaranteed base ¥24,000–30,000 + commission vs peer median ¥6,500 (see `fig1_salary_comparison.png`, `fig4_market_context.png`).
2. State-owned platform (PICC brand), full company-resource support, 4 promotion opportunities/year.
3. Rare quality-of-work perks: no overtime, no probation period, flexible afternoons, overseas opportunities, business-trip allowance.
4. Broad age (25–50) and Associate-degree floor enlarge the accessible talent pool.
5. Commission upside keeps pay market-competitive at the very top of the Xiamen distribution.

**Weaknesses / risks:**
1. Statutory welfare below industry standard (三险一金 vs 五险一金; no paid annual leave/performance bonus/meal-communication-transport allowances advertised) — likely candidate objections.
2. Dual high screen (3-yr same-industry or 1-yr supervisory **plus** >¥50k after-tax income) may bottleneck the pipeline for only 2 openings.
3. Extremely high pay for a state-owned establishment role may attract candidates expecting agency-style uncapped commission; the guaranteed-base figure should be verified against the pay band to avoid expectation mismatch.
4. Pay position (~99th percentile) is hard to defend if performance targets are not met — risk of "high sticker, low realized" reputation.

## 7. Recommendations

1. **Upgrade the statutory package** to 五险一金 and explicitly add paid annual leave (+ performance bonus) in the ad; this closes the largest welfare gap at low incremental cost and matches 9–11 of 16 peers.
2. **Lead with the guaranteed base** in job ads and interview scripts (base alone ¥24k–30k ≈ 4× peer median) to differentiate from Ping An/China Life agent roles whose base is ¥1.5k–10k.
3. **Reconsider or clarify the income gate** (>¥50k after-tax prior year): keep it only if it demonstrably improves retention of top producers; otherwise relax to internal-promotion criteria.
4. **Communicate the four-promotion-per-year cadence and full resource support** — no peer quantifies promotion frequency, making this a distinctive selling point.
5. **Benchmark quarterly**: re-run this salary parse against the peer set; monitor whether any peer introduces a management role above ¥20k, which would narrow the pay premium.
6. Retain flexible-hours/no-overtime/no-probation framing as differentiators that compensate for the thinner statutory benefits.

## 8. Limitations

- The target posting is not in the database; analysis compares it to a manually curated subset (16 genuine insurance positions; 27 database rows mention insurance, the rest are contaminated/non-insurer rows).
- 4/16 peers did not disclose salary; peer statistics reflect the 12 disclosed postings.
- Salary parsing uses the headline range; commission-heavy peers (Ping An, Sunshine) can pay above their advertised range, so the true top-of-market gap may be slightly narrower than reported.
- Benefit comparisons are keyword-based on ad text; unlisted items (e.g., statutory leave) may still exist in practice, and wording variants can cause under- or over-counting.
- Data is a single-platform, Xiamen-only snapshot; results should not be generalized to other cities or channels.
