<!-- Reading copy: local artifact links normalized. Original answer is preserved at ../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/answer.md -->

# Weak-Point Analysis of 2024 Login–Authentication Method Combinations & Recommendations

## 1. Scope and Method

**Dataset.** 487 login records in the database, of which **177 occurred in 2024**, joined to 150 anomalous logins (85% of 2024 logins had ≥1 anomaly), security events, system logs and IP data. The four login methods in 2024 were **Password Login, Scan Code Login, Fingerprint authentication, SMS verification code**, each paired with one of three 2FA channels: **SMS, Email, APP verification code** (12 combinations total).

**Weakness definition.** Each Login×2FA combination was scored on a normalized composite of: authentication failure count, anomaly count, average anomaly score, security-event count, summed risk score, and High/Severe events, with anomalies and security events weighted highest (see `/work/weakness_breakdown.png`).

## 2. Overall 2024 Landscape

| Login Method | Logins | Failure Rate | Anomalies |
|---|---|---|---|
| Scan Code Login | 46 | 45.7% | 37 |
| SMS verification code | 45 | 53.3% | 37 |
| Password Login | 44 | 54.5% | 36 |
| Fingerprint authentication | 42 | 54.8% | 40 |

- Failure rates are similar (~45–55%) across methods; **the decisive weak-point signal is not raw failure rate but anomaly density, security-event severity and risk score**. 
- Dominant anomaly types in 2024: **Device anomaly, Frequent login, Multiple IPs in short time, Remote Login**. Dominant security events: **Malicious Attack, Unauthorized Access, Unauthorized Operation, Data leakage** (many at High/Severe severity).
- The 2FA channel SMS stands out negatively: 58.5% failure rate vs 49.1% (Email) and 47.3% (APP verification code).

## 3. Weakest Combinations (2024)

Ranked by composite weakness score (`/work/ranking.png`, `/work/weakness_heatmap.png`):

| Rank | Login + 2FA | Logins | Failures | Anomalies | Events | High/Severe | Risk Sum | Weakness |
|---|---|---|---|---|---|---|---|---|
| 1 (worst) | **SMS verification code + Email** | 18 | 10 | 16 | 16 | 9 | **916** | 0.83 |
| 2 | **Fingerprint authentication + SMS** | 14 | **11 (78.6%)** | 14 | 14 | **9** | 648 | 0.72 |
| 3 | **Password Login + SMS** | 22 | 14 (63.6%) | **19** | 12 | 3 | 569 | 0.64 |
| 4 | **Scan Code Login + APP verification code** | 20 | 10 | 17 | 12 | 5 | 574 | 0.61 |

Key observations:
- **SMS verification code + Email** is the single weakest combination: the highest security-event count (16) and the highest total risk score (916) of all 12 combos, with 56% of its High/Severe events.
- **Fingerprint authentication + SMS** has the **highest authentication failure rate (78.6%)** and the most Severe events (7); its anomaly indicators are spread across device (6.9), network (6.1) and behavior (6.5) — a broad attack surface (`/work/anomaly_composition.png`).
- **Password Login + SMS** produces the most anomalies (19) of any combo, driven by frequent-login and multi-IP anomalies, plus the most ERROR system logs (9).

## 4. Strongest Combinations (Lower Weakness)

| Rank | Login + 2FA | Logins | Anomalies | Events | High/Severe | Risk Sum | Weakness |
|---|---|---|---|---|---|---|---|
| 1 (best) | **Scan Code Login + Email** | 11 | 7 | 5 | **1** | **194** | 0.12 |
| 2 | **Password Login + APP verification code** | 10 | 7 | 7 | 5 | 388 | 0.21 |
| 3 | **Fingerprint authentication + APP verification code** | 12 | 12 | 8 | 4 | 417 | 0.29 |
| 4 | **SMS verification code + APP verification code** | 13 | 10 | 8 | 5 | 405 | 0.29 |

## 5. Effect of Enabling 2FA (`/work/2fa_status_effect.png`)

Total 2024 risk for **2FA "Not Enabled"** logins was 3,260 vs 2,584 when enabled (62% higher). The benefit is method-dependent:
- **Fingerprint authentication:** enabling 2FA cuts risk per login from 41.9 → 34.3 (anomalies 26 → 14).
- **Scan Code Login:** enabling 2FA cuts risk per login from 29.6 → **19.1** (the best risk-per-login overall).
- **Password Login:** small benefit (risk per login 29.4 → 33.4; enabling shows slightly more anomalies, but SMS pairing is the real problem).
- **SMS verification code:** enabling 2FA *increases* observed risk (34.2 → 41.8) — consistent with SMS being a weak second channel that adds little protection.

## 6. Supporting Evidence from the Authentication Catalog

The `authentication_methods_table` (692 configuration records) shows **SMS verification code has the lowest average security level (2.8)** among the channel types, while **Fingerprint recognition and Dynamic Token have the highest (3.3)**; Email verification code is at 3.2. This corroborates the observed operational weakness of SMS as a second factor.

## 7. Recommendations

1. **Adopt "APP verification code" as the standard 2FA channel.** Across all four login methods it delivers the lowest failure rate (47.3%) and is present in three of the four strongest combinations; it corresponds to the high-security *Dynamic Token* class in the authentication catalog.
2. **Phase out SMS as a second factor.** SMS pairs fill the three weakest combinations, has the highest failure rate (58.5%), the lowest catalog security level (2.8), and the highest per-combo Severe-event counts.
3. **Retire the three worst combos first:** *SMS verification code + Email*, *Fingerprint authentication + SMS*, *Password Login + SMS*.
4. **Preferred forward combinations (adopt subsequently):**
   - **Scan Code Login + APP verification code** (already the most-used scan-code pairing; keep with 2FA enabled),
   - **Password Login + APP verification code** (recommended upgrade from Password + SMS),
   - **Fingerprint authentication + APP verification code** (recommended upgrade from Fingerprint + SMS/Email).
5. **Force-enable 2FA** for Fingerprint authentication and Scan Code Login, where enabling demonstrably reduces anomalies and risk-per-login, and apply account lockout/tamper policies from the catalog (SMS already has the strictest attempts/lockout, but its security weakness outweighs this).

## Limitations

- Only 177 login records exist for 2024; per-combination samples are small (10–22), so rankings are indicative rather than statistically powered. 
- "APP verification code" is mapped to the catalog's Dynamic Token class by similarity; the catalog contains no literal APP-verification-code row.
- Failure rates are near-uniform by construction, so the analysis leans on anomaly/security-event signals; confirmation status of anomalies (Pending vs Confirmed) was not used to filter, which may slightly inflate weak-point counts.
- Cross-year comparison (2022–2023) was not required for the task and is not included.

**Figures:** `/work/weakness_heatmap.png`, `/work/weakness_breakdown.png`, `/work/severity_distribution.png`, `/work/anomaly_composition.png`, `/work/2fa_status_effect.png`, `/work/ranking.png`
