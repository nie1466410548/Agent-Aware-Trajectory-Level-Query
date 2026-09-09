# Department Security Awareness Analysis Report

## Executive Summary

Based on comprehensive analysis of abnormal login data, account security indicators, login behaviors, and security event handling across four departments, **the Sales Department exhibits the weakest security awareness** and should be prioritized for security awareness guidance. The Technical Department and Marketing Department follow as secondary priorities, while the Finance Department demonstrates relatively stronger security awareness.

---

## Methodology

We analyzed security awareness weakness across departments using a composite index of 9 behavioral indicators:

| Indicator | What It Measures | Why It Matters |
|-----------|-----------------|----------------|
| **Anomaly Rate** | Anomalies per 100 users | Overall security incident density |
| **Remote Login Rate** | Remote login anomalies per 100 users | Potential credential sharing / phishing susceptibility |
| **Repeat Offender Rate** | % of users with ≥2 anomalies | Recidivism — failure to learn from incidents |
| **Failed Login Rate** | % of login attempts that failed | Password management issues |
| **No 2FA Rate** | % of logins without two-factor auth | Poor adoption of basic security hygiene |
| **Locked Account Rate** | % of accounts locked | Password-related security problems |
| **Unprocessed Log Rate** | % of system logs still unprocessed | Lack of incident response diligence |
| **High Severity Events** | High+Severe security events per 100 users | Exposure to serious threats |
| **Confirmed Anomaly Rate** | % of anomalies confirmed as real threats | Actual validated security incidents |

Each indicator was normalized to a 0–1 scale (higher = weaker awareness) and averaged into a composite weakness score.

---

## Results

### Overall Security Awareness Weakness Ranking

| Rank | Department | Composite Score | Priority |
|------|-----------|:--------------:|:--------:|
| **1** | **Sales Department** | **0.803** | **Highest Priority** |
| 2 | Technical Department | 0.474 | Medium Priority |
| 3 | Marketing Department | 0.469 | Medium Priority |
| 4 | Finance Department | 0.352 | Lowest Priority |

![Composite Weakness Score](security_awareness_weakness_score.png)

### Department Breakdown

#### 1. Sales Department — Weakest Security Awareness (Score: 0.803)

| Indicator | Value | Risk |
|-----------|:-----:|:----:|
| Repeat Offender Rate | **45.6%** | ⚠️ Very High |
| No 2FA Rate | **57.4%** | ⚠️ Very High |
| Locked Account Rate | **53.8%** | ⚠️ Very High |
| Unprocessed Log Rate | **41.0%** | ⚠️ Very High |
| Confirmed Anomaly Rate | **58.7%** | ⚠️ Very High |
| Anomaly Rate | 65.0 / 100 users | High |
| Remote Login Rate | 13.8 / 100 users | Moderate |
| Avg Password Attempts | 2.71 | Moderate |
| Off-Hours Anomalies | 31.7% | Moderate |

**Key Concerns:** The Sales Department leads in 5 out of 9 indicators. The extremely high repeat offender rate (45.6%) indicates that users who experience security incidents continue to have further incidents — a clear sign of weak security awareness and failure to adopt safer practices. The high locked account rate (53.8%) suggests widespread password management problems. Over half of users do not use two-factor authentication despite its availability.

#### 2. Technical Department (Score: 0.474)

| Indicator | Value | Risk |
|-----------|:-----:|:----:|
| High Severity Events per 100 users | **35.95** | ⚠️ Very High |
| Failed Login Rate | **54.2%** | ⚠️ Very High |
| No 2FA Rate | **57.0%** | ⚠️ Very High |
| Unprocessed Log Rate | 38.5% | High |
| Avg Anomaly Score | **51.07** | Highest |
| Remote Login Rate | 9.8 / 100 users | Low |

**Key Concerns:** Despite being the technical department, it has the highest rate of high-severity security events (35.95 per 100 users), the highest average anomaly score (51.07), and a very high rate of not using 2FA (57.0%). This suggests a disconnect between technical expertise and personal security practices.

#### 3. Marketing Department (Score: 0.469)

| Indicator | Value | Risk |
|-----------|:-----:|:----:|
| Remote Login Rate | **16.7 / 100 users** | ⚠️ Very High |
| Failed Login Rate | **54.6%** | ⚠️ Very High |
| Locked Account Rate | **52.6%** | ⚠️ Very High |
| Off-Hours Anomalies | **34.5%** | ⚠️ Very High |
| Anomaly Rate | 61.1 / 100 users | Moderate |

**Key Concerns:** The Marketing Department has the highest remote login anomaly rate (16.7 per 100 users), which may indicate exposure to phishing or unauthorized access. The highest off-hours anomaly rate (34.5%) and high failed login rate (54.6%) suggest credential hygiene issues.

#### 4. Finance Department (Score: 0.352)

| Indicator | Value | Risk |
|-----------|:-----:|:----:|
| Anomaly Rate | 65.5 / 100 users | High |
| High Severity Events | 31.55 / 100 users | High |
| Repeat Offender Rate | 34.6% | Moderate |
| Avg Password Attempts | **1.94** | ✅ Lowest |
| Unprocessed Log Rate | **24.8%** | ✅ Lowest |
| Confirmed Anomaly Rate | **38.2%** | ✅ Lowest |

**Key Concerns:** While the Finance Department has the highest raw anomaly rate per 100 users, its indicators of security awareness weakness are the lowest. The low confirmed anomaly rate (38.2%) suggests many anomalies are false positives or minor. The lowest unprocessed log rate (24.8%) shows better incident response diligence.

---

## Statistical Analysis

Statistical tests were performed to assess the significance of differences:

- **Kruskal-Wallis test on anomaly scores** across departments: H=3.42, p=0.33 — differences in anomaly score distributions are not statistically significant at α=0.05.
- **Chi-square test on risk level distribution** across departments: χ²=12.09, p=0.21 — not statistically significant.
- **Chi-square test on authentication status** across departments: χ²=1.03, p=0.80 — not statistically significant.
- **Chi-square test on 2FA status** across departments: χ²=2.60, p=0.46 — not statistically significant.

While individual indicators do not show statistically significant differences, the **pattern across multiple indicators** consistently points to the Sales Department as having the weakest security awareness. The composite score approach provides a practical prioritization framework for security awareness interventions.

---

## Visualizations

### 1. Security Awareness Weakness Composite Score
![Composite Score](security_awareness_weakness_score.png)

### 2. Department Radar Chart (Risk Profile)
![Radar Chart](department_security_radar.png)

### 3. Anomaly & Login Metrics Comparison
![Metrics Comparison](department_security_awareness_analysis.png)

---

## Recommendations

### Priority 1: Sales Department (Immediate Action Required)
- **Implement mandatory 2FA enrollment** — only 42.6% currently use 2FA
- **Conduct targeted security awareness training** focused on password hygiene and recognizing phishing attempts
- **Review and resolve locked accounts** — investigate why 53.8% of accounts are locked
- **Establish incident response protocols** to reduce the 41% unprocessed log rate
- **Monitor repeat offenders** — 45.6% of affected users are repeat offenders; implement personalized coaching

### Priority 2: Technical Department
- **Address the 2FA gap** — despite the technical nature of the department, 57% don't use 2FA
- **Investigate high-severity events** — 35.95 per 100 users is the highest rate
- **Improve log processing** — 38.5% unprocessed rate needs attention

### Priority 3: Marketing Department
- **Focus on remote login risks** — highest rate at 16.7 per 100 users; implement geo-fencing or VPN requirements
- **Address off-hours anomaly patterns** — 34.5% of anomalies occur during off-hours (0:00–6:00)
- **Reduce locked accounts** — 52.6% locked rate needs review

### Priority 4: Finance Department
- **Maintain current practices** while continuing to monitor
- **Investigate the high anomaly rate** — 65.5 per 100 users despite good awareness indicators; may indicate external targeting rather than internal weakness

---

## Limitations

1. **Statistical significance**: The differences between departments on individual metrics are not statistically significant at conventional thresholds. The composite ranking should be viewed as a prioritization tool rather than definitive proof of differences.
2. **Confounding factors**: Departments may face different external threat levels (e.g., Finance may be more targeted by external attackers), which could inflate raw anomaly counts without indicating weaker awareness.
3. **Data completeness**: The analysis relies on logged anomalies; some security incidents may go undetected.
4. **Equal weighting**: The composite index uses equal weights; a different weighting scheme could produce different rankings.
5. **Temporal factors**: Analysis does not account for changes over time; a department that has recently undergone training may show improved but older data.

---

## Conclusion

Based on the multi-indicator analysis of abnormal login data, account security, and incident handling, **the Sales Department demonstrates the weakest security awareness** and should be prioritized for security awareness strengthening. The department's high repeat offender rate, low 2FA adoption, high account lock rate, and poor incident log processing collectively indicate a systemic lack of security-conscious behavior. The Technical and Marketing Departments show moderate weakness, while the Finance Department exhibits relatively stronger security awareness practices.