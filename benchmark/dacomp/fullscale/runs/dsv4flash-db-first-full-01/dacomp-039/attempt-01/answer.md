# 2024 Levels: Churn Rate & Level Rating across Difficulty × Level Type

## Data Scope
- **3,142 levels launched in 2024** (out of a full dataset spanning 2021–2025). The 2024 cohort is the game's largest content release year (vs ~390 in 2022 and ~580 in 2023).
- Difficulty levels present: Easy, Normal, Hard, Hell. Level types present: Exploration, Parkour, Puzzle, Battle, BOSS.
- All combinations are **not** produced equally: Easy/Normal have **zero BOSS** levels; Hard/Hell have **zero Exploration** levels. Hell is overwhelmingly BOSS (660 of 702 Hell levels, 94%).

## Headline Pattern: Difficulty is the Dominant Driver
Both metrics move almost entirely with Difficulty Level:

| Difficulty | Levels | Avg Churn Rate | Avg Level Rating | Avg Clear Rate | Avg Retries | Avg Players |
|---|---|---|---|---|---|---|
| Easy | 806 | **0.039** | **4.46** | 0.89 | 1.3 | 24,719 |
| Normal | 819 | 0.123 | 3.82 | 0.67 | 3.0 | 15,363 |
| Hard | 815 | 0.284 | 3.01 | 0.33 | 8.3 | 8,526 |
| Hell | 702 | **0.591** | **1.87** | 0.10 | 23.4 | 2,366 |

- Churn increases monotonically (+8.4pp, +16.1pp, +30.7pp per difficulty step); Rating falls monotonically.
- **Difficulty alone explains ~85.6% of Churn variance and ~85.5% of Rating variance** (linear-model R²). Adding Level Type raises Churn R² only to 0.8574 — Level Type contributes almost nothing beyond difficulty.
- Pairwise differences between difficulty bands are massive (Cohen's d = 2.5–2.65, all p < 1e-50).
- **This pattern is stable across years** (2022–2024 marginal difficulty averages are nearly identical), so the 2024 structure is not an anomaly.

## Level Type Effects Within a Difficulty Band
Type only matters *within* a difficulty band, and even then effects are small:

| Difficulty | Lowest-churn type | Highest-churn type | Spread |
|---|---|---|---|
| Easy | Exploration (0.027) | Battle (0.047) | 0.020 |
| Normal | Parkour (0.111) | Battle (0.138) | 0.027 |
| Hard | Parkour (0.270) | BOSS (0.305) | 0.035 |
| Hell | Battle (0.512) | BOSS (0.595) | 0.083 |

- **Battle is the consistent under-performer**: at Easy, Normal, and Hard it has the highest (or near-highest) churn and lowest rating within its band (e.g., Normal+Battle 0.138 vs band 0.123).
- **BOSS levels look worst overall (churn 0.58, rating 1.92) but that is a difficulty artifact** — BOSS only exists in Hard/Hell. Within Hard, BOSS (0.305) is only marginally above Battle (0.286) and Puzzle (0.278), and within-Hard type differences are not statistically significant (Parkour vs Puzzle p=0.37; Battle vs BOSS p=0.15).
- The largest true type effect in 2024 is **Hell+Battle: churn 0.512 vs the Hell band average 0.591 (−0.079) and rating +0.49 above band** — but it rests on only 22 levels vs 660 Hell BOSS levels, so treat cautiously.
- Exploration, where it exists (Easy/Normal), is the best-performing type (lowest churn, highest rating) yet is nearly absent in 2024 (16 levels total).

## Churn and Rating Are Two Sides of the Same Coin
Correlations on 2024 levels (SQLite has no CORR; computed in Python):
- Churn ↔ Rating: **r = −0.934**
- Churn ↔ Clear Rate: r = −0.910; Churn ↔ Retry Count: r = +0.867
- Churn ↔ Level Completion Rate: r = **−0.985** (Completion Rate ≈ 1 − Churn; sum averages 0.986) — a nearly perfect inverse proxy usable for early detection.
- Longer average clear time ⇒ higher churn (r = 0.62); higher participation ⇒ lower churn (r = −0.56) and higher rating (r = 0.62).
- Reward Value does **not** compensate for churn: overall r = +0.37 with churn (within Hard, r = 0.39). Bigger rewards co-occur with, rather than offset, higher churn.

## Optimization Recommendations
1. **Fix the Hell bottleneck first.** Hell levels churn ~59% of an already-small audience (avg 2,366 players) while scoring 1.87 — the steepest rating loss (−1.13 vs Hard) for the smallest pool. Because Hell is 94% BOSS, the primary lever is rebalancing Hell BOSS design (checkpoint frequency, telegraphing, damage curves) rather than adding new types.
2. **Use Level Type as a secondary tuning knob, not a primary one.** Since difficulty dominates, plan content against the difficulty bands (Easy≈4%/Normal≈12%/Hard≈28%/Hell≈59% churn) and use type only to nudge within a band: prefer **Parkour/Puzzle** for the least-churn hard content, and **Battle** when you must accept higher churn.
3. **Avoid or redesign Battle levels at Easy/Normal/Hard** — they consistently sit at the top of their band's churn and bottom of its rating, yet Battle is one of the most-produced types (550 Hard + 176 Normal + 75 Easy in 2024).
4. **Reconsider the BOSS/Exploration asymmetry.** BOSS is only built for the hardest tiers and Exploration only for the easiest. Exploration's excellent metrics (Easy 0.027 churn / 4.63 rating) suggest it is an under-used, player-friendly format that could absorb some content volume shifted out of high-churn Battle.
5. **Use Level Completion Rate as an early-warning KPI** (r = −0.985 with churn). Any level whose completion rate lags its difficulty band by >1.5 IQR should be flagged before full rollout. 2024 outlier counts by band: Easy 13, Normal 14, Hard 20, Hell 0.
6. **Don't use bigger rewards to fix churn** — reward value is positively (not negatively) correlated with churn. Instead, reduce friction: lower clear-time/retry burdens (both strongly associated with churn) and improve discoverability/participation (higher participation tracks with lower churn and higher ratings).
7. **Monitor the Normal→Hard gap.** It is the second-steepest jump (+16pp churn, −0.81 rating). Smoothing this ramp (e.g., more Normal-Hard bridging content) could keep mid-skill players from churning out.

## Figures
- `work/heatmaps_2024.png` — Churn, Rating, and level-count heatmaps across Difficulty × Level Type
- `work/difficulty_tradeoff.png` — Marginal churn vs rating trade-off by difficulty
- `work/scatter_churn_rating.png` — Level-level churn vs rating scatter by difficulty (r = −0.93)
- `work/scatter_combo_summary.png` — Bubble summary of all 16 combinations (size = level count)
- `work/bar_churn.png`, `work/bar_rating.png` — Grouped bars by difficulty and type
- `work/violin_churn.png` — Churn distribution by difficulty

## Limitations
- Level Type contributes little after controlling for difficulty, so conclusions about types rest mainly on within-band spreads; several band-type cells have very small sample sizes (Hell Parkour n=9, Hell Puzzle n=11, Easy/Normal Exploration n≈8) and should be read as indicative only.
- The dataset is highly unbalanced (660 Hell-BOSS vs 7 Normal-Exploration), so ANOVA-style sums of squares are non-additive; I therefore used linear-model R² decomposition instead.
- No causal inference: this is observational correlational data; recommendations are pattern-based hypotheses for A/B testing. Monthly churn in 2024 also fluctuates (peak ~0.31 in May, low ~0.16 in February), which may reflect campaign/event effects not captured by level attributes.
