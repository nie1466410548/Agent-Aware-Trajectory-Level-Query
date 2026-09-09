# Mental Health and Academic Performance: Trend Shape, Robustness, and Moderation

## Data and Methods
The dataset `sheet1` contains **1,000 students** with no missing values in any column except `Parents' education level` (89 missing; coded as a separate "Missing" category in regressions). `Mental health score` is an integer 1–10 (mean 5.36, SD 2.87); `Exam score` ranges 18.4–100 (mean 69.6, SD 16.9). All regression and hypothesis-testing procedures were run in Python (scipy/numpy) because SQLite cannot perform OLS, t/F tests, or delta-R² tests; SQL was used for all filtering, grouping, and descriptive aggregation.

---

## Question 1 — Overall relationship between `Mental health score` and `Exam score`

**Result: The relationship is positive, monotonic, and well approximated by a straight line; no statistically reliable inflection point exists, though the raw group means show a mild visual steepening near the middle of the scale.**

Evidence:

1. **Correlation (statistical association).** Pearson *r* = 0.326 (p = 3.6×10⁻²⁶); Spearman *ρ* = 0.329 (p = 1.2×10⁻²⁶); Kendall *τ* = 0.233 (p = 7.3×10⁻²⁶). All three agree the association is moderate, positive, and overwhelmingly significant.
2. **Monotonicity.** Group means rise almost monotonically from 63.2 (`Mental health score` = 1) to 78.1 (= 10). Only 1 of 9 adjacent steps is non-increasing (a trivial −0.21 drop between scores 1→2). The near-equality of Pearson and Spearman coefficients confirms the trend is essentially rank-preserving (monotonic) rather than driven by outliers.
3. **Linearity / inflection tests.** OLS gives `Exam score = 59.32 + 1.92 × Mental health score`, R² = 0.106. Adding a quadratic term does **not** improve fit (F = 0.79, p = 0.375); a cubic term is only borderline (F = 3.55, p = 0.060, ΔR² = 0.004). Segmented (piecewise-linear) regressions at knots 4.5–6.5 find no significant slope change (largest t = 1.32, p = 0.186; knot 5.5 slope change p = 0.395). The largest group-mean jump occurs between scores 5 and 6 (+3.79 points), suggesting a mild steepening in the middle of the scale, but statistically the linear model captures the trend adequately — the curvature terms add < 0.4% explained variance.
4. **Effect size.** Each 1-point increase in `Mental health score` is associated with **+1.92 exam points** (95% CI ≈ [1.57, 2.27]); a 5-point increase (1→6) corresponds to ≈ 9.6 points, about 0.57 SD of `Exam score`.

**Conclusion for Q1:** The trend is *monotonically increasing and approximately linear* (not flat, not U-shaped). Any inflection at `Mental health score` ≈ 5–6 is visually suggestive but not statistically supported.

![Trend shape: scatter, group means, linear and cubic fits](work/fig1_trend.png)

---

## Question 2 — Marginal effect of `Mental health score` after controlling for learning-habit and lifestyle factors

**Result: `Mental health score` retains a large, highly significant marginal effect on `Exam score` after all controls. The coefficient is only modestly attenuated (1.92 → 1.83), and it is by far the strongest predictor after `Daily study time`.**

Model (OLS, n = 1,000, k = 15, R² = 0.8545, adj. R² = 0.8524), controlling for `Daily study time`, `Social media usage time`, `Attendance rate`, `Sleep duration`, `Exercise frequency`, `Diet quality` (dummies vs. Fair), `Part-time job` (vs. No), `Internet quality` (vs. Average), and `Parents' education level` (vs. High School, incl. Missing category):

| Parameter | Coef | SE | t | p | 95% CI |
|---|---|---|---|---|---|
| **`Mental health score`** | **1.834** | **0.073** | **25.24** | **< 1×10⁻¹⁵** | **[1.692, 1.977]** |
| `Daily study time` | 9.490 | 0.141 | 67.07 | < 1e-15 | [9.212, 9.767] |
| `Social media usage time` | −1.635 | 0.153 | −10.69 | < 1e-15 | [−1.935, −1.335] |
| `Attendance rate` | −0.000 | 0.018 | −0.02 | 0.986 | [−0.036, 0.035] |
| `Sleep duration` | 1.807 | 0.168 | 10.77 | < 1e-15 | [1.478, 2.136] |
| `Exercise frequency` | 1.454 | 0.102 | 14.31 | < 1e-15 | [1.254, 1.653] |
| `Diet quality` = Good | −0.989 | 0.459 | −2.16 | 0.031 | [−1.889, −0.089] |
| `Diet quality` = Poor | −0.221 | 0.573 | −0.39 | 0.700 | [−1.344, 0.903] |
| `Part-time job` = Yes | 0.161 | 0.501 | 0.32 | 0.747 | [−0.821, 1.144] |
| `Internet quality` = Good/Poor | −0.683 / 0.185 | — | −1.51 / 0.30 | 0.131 / 0.761 | — |
| `Parents' education` (Bachelor/Master/Missing) | −0.371 / −1.030 / −0.646 | — | — | 0.441 / 0.088 / 0.400 | — |

**Inferential quantities for `Mental health score`:**
- **Coefficient (marginal effect): 1.834 exam points per 1-point MH increase**, controlling for all covariates.
- **95% CI:** [1.692, 1.977] (classical); HC1 heteroskedasticity-robust [1.690, 1.978] — t = 24.96 robust, p < 1×10⁻¹⁵.
- **Delta-R² = 0.0941:** `Mental health score` explains **9.4 additional percentage points** of `Exam score` variance above the controls (controls-only R² = 0.7604 → full R² = 0.8545). Partial R² for MH = 0.393; **partial F(1,985) = 637.2, p < 1×10⁻¹⁵**.
- **Standardized β = 0.311** (medium-to-large by conventional benchmarks), second only to `Daily study time` (β ≈ 0.85).
- **Stability across specifications:** crude b = 1.919 → controlled b = 1.834 → fully saturated (adding `Age`, `Gender`, `Extracurricular activity participation`) b = 1.833. Attenuation is only ~4.5%, indicating little confounding from the measured habits/lifestyle factors.
- **Diagnostics:** all VIFs < 1.3 (no multicollinearity); residuals approximately normal (slight departure, p = 0.01 on Shapiro test, acceptable at n = 1,000).

**Conclusion for Q2:** Yes — after controlling for the specified learning-habit and lifestyle variables, `Mental health score` maintains a statistically significant marginal effect of **+1.83 exam points per unit (p < 1e-15)**, contributing ΔR² = 0.094 beyond controls. This is a robust, policy-relevant effect, not an artifact of confounded covariates.

---

## Question 3 — Variables that interact with `Mental health score` to amplify or dampen its effect

**Result: Two significant moderators emerge — `Attendance rate` amplifies the MH→Exam effect, and `Social media usage time` dampens it. No other habit, lifestyle, or demographic variable interacts significantly.**

Interaction terms were added one at a time to the full control model; significance was judged on the interaction coefficient, its partial F-test, and ΔR²:

| Interaction (× `Mental health score`) | b_int | SE | t | p | ΔR² | Effect |
|---|---|---|---|---|---|---|
| **`Attendance rate`** | **+0.0318** | 0.0060 | 5.29 | **1.49×10⁻⁷** | 0.0040 | **Amplifies** |
| **`Social media usage time`** | **−0.1433** | 0.0513 | −2.79 | **0.0054** | 0.0011 | **Dampens** |
| `Daily study time` | −0.003 | 0.050 | 0.956 | — | 0.0000 | none |
| `Sleep duration` | 0.047 | 0.060 | 0.433 | — | 0.0001 | none |
| `Exercise frequency` | −0.053 | 0.036 | 0.138 | — | 0.0003 | none |
| `Diet quality` (Good / Poor) | −0.023 / −0.292 | — | 0.878 / 0.117 | — | ≤ 0.0004 | none |
| `Part-time job` | −0.110 | 0.170 | 0.518 | — | 0.0001 | none |
| `Internet quality` (Good / Poor) | 0.124 / −0.048 | — | 0.393 / 0.804 | — | ≤ 0.0001 | none |
| `Parents' education level` (Bachelor / Master / Missing) | 0.138 / 0.313 / −0.334 | — | 0.357 / 0.117 / 0.205 | — | ≤ 0.0004 | none |
| `Age`, `Gender`, `Extracurricular activity participation` | ≤ 0.062 | — | ≥ 0.36 | — | ≤ 0.0001 | none |

**Quantified moderation (marginal MH slope d`Exam score`/d`Mental health score`, other covariates at means):**

- **`Attendance rate` (amplifier):** MH slope = 1.11 at 60% attendance → 2.09 at 83% → 2.38 at 100% attendance. Across the observed attendance range (≈60→100%), the MH effect grows by **≈1.27 exam points per MH unit** — i.e., a 10-point attendance increase raises the MH payoff by ≈0.32 exam points per unit.
- **`Social media usage time` (dampener):** MH slope = 2.21 at 0 h → 1.83 at 2.6 h → 1.49 at 5 h → 1.06 at 8 h. Across 0→8 h of daily social media, the MH effect shrinks by **≈1.15 exam points per MH unit**.

![Significant interactions: MH × Attendance (amplifier) and MH × Social media (dampener)](work/fig2_interactions.png)

**Mechanistic and policy implications:**
1. **`Attendance rate` as an engagement amplifier.** Good mental health and school engagement appear *complementary*: students who attend regularly convert good mental health into exam performance more effectively. Mechanistically, regular attendance proxies for consistent exposure to instruction, structured routine, and social support — resources that allow well-being to translate into learning. Policy implication: mental-health interventions will have the **largest academic returns among engaged, regularly attending students**; conversely, supporting attendance (e.g., reducing absenteeism) raises the ROI of mental-health programs.
2. **`Social media usage time` as a dampener.** Heavy social-media use erodes the academic benefit of good mental health — mentally healthy students who spend many hours on social media see a much smaller exam payoff. Mechanism: screen time displaces study/rest, fragments attention, and may substitute for the deep engagement that converts well-being into achievement. Policy implication: screen-time limits or digital-wellbeing programs are a lever to **realize the academic benefits of mental health**, especially for otherwise high-MH students.
3. **Non-findings are informative.** Habit variables like `Daily study time`, `Sleep duration`, and `Exercise frequency` add large *main effects* on `Exam score` but do **not** change the *slope* of MH→Exam; i.e., they shift the whole achievement distribution rather than conditioning the value of mental health. Demographics (`Age`, `Gender`) and family background (`Parents' education level`) also do not moderate the MH effect.

---

## Limitations
- Observational cross-sectional data: coefficients are associational, not causal; unmeasured confounders may remain.
- `Parents' education level` has 89 missing values; handled via an explicit "Missing" dummy rather than imputation.
- The MH→Exam trend is strongly linear; the middle-of-scale inflection (scores 5–6) is visually present but not statistically significant with n = 1,000.
- Interaction ΔR² values are small (0.001–0.004); they are statistically robust (partial-F p ≤ 0.005) but modest in magnitude, so moderation effects are meaningful at the extremes of the moderators rather than at typical values.
- Exam scores are capped at 100; mild residual non-normality (Shapiro p = 0.01) exists, but HC1-robust SEs confirm the inferences.

## Key Takeaways
1. `Mental health score` → `Exam score` is **positive, monotonic, and approximately linear** (r = 0.326; +1.92 points per MH unit), with no statistically supported inflection.
2. After full controls, the marginal effect remains **+1.834 (95% CI [1.692, 1.977], p < 1e-15; ΔR² = 0.094, partial F = 637)** — robust to heteroskedasticity and model specification.
3. **`Attendance rate` amplifies** (interaction +0.032, p = 1.5×10⁻⁷) and **`Social media usage time` dampens** (interaction −0.143, p = 0.005) the mental-health payoff on exam performance — pointing to engagement support and screen-time management as the two highest-leverage complements to mental-health policy.
