import pandas as pd
import numpy as np
from scipy import stats

# Fetch anomaly data with department for statistical testing
anomaly_full = db.frame(db.query("""
SELECT u.Department AS dept, a."Anomaly Score" AS score, a."Risk Level" AS risk,
       a."Device Anomaly Indicators" AS dev, a."Network Anomaly Indicators" AS net,
       a."Behavior Anomaly Indicators" AS beh
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
"""))

# Kruskal-Wallis test on anomaly scores across departments
groups = [anomaly_full.loc[anomaly_full['dept'] == d, 'score'].values for d in anomaly_full['dept'].unique()]
h, p = stats.kruskal(*groups)
print(f"Kruskal-Wallis test on Anomaly Score across departments: H={h:.3f}, p={p:.4f}")

# Kruskal-Wallis on each anomaly indicator
for col in ['dev', 'net', 'beh']:
    groups = [anomaly_full.loc[anomaly_full['dept'] == d, col].values for d in anomaly_full['dept'].unique()]
    h, p = stats.kruskal(*groups)
    print(f"Kruskal-Wallis on {col}: H={h:.3f}, p={p:.4f}")

# Chi-square test on risk level distribution by department
ct = pd.crosstab(anomaly_full['dept'], anomaly_full['risk'])
chi2, p, dof, expected = stats.chi2_contingency(ct)
print(f"\nChi-square test on Risk Level x Department: chi2={chi2:.3f}, p={p:.4f}, dof={dof}")
print("Contingency table:")
print(ct)

# Per-department means of indicators
print("\nPer-department anomaly indicator means:")
print(anomaly_full.groupby('dept')[['score', 'dev', 'net', 'beh']].mean().round(3))

# Check login duration as potential proxy
login_data = db.frame(db.query("""
SELECT u.Department AS dept, l."Login Duration" AS dur, l."Authentication Status" AS auth
FROM login_records_table l
JOIN user_information_table u ON l."User ID" = u."User ID"
"""))
print("\nLogin durations by department:")
print(login_data.groupby('dept')['dur'].describe().round(1))

# Check failed login rate significance with chi-square
ct2 = pd.crosstab(login_data['dept'], login_data['auth'])
chi2b, pb, _, _ = stats.chi2_contingency(ct2)
print(f"\nChi-square on Authentication Status x Department: chi2={chi2b:.3f}, p={pb:.4f}")

# Check 2FA chi-square
login2fa = db.frame(db.query("""
SELECT u.Department AS dept, l."Two-Factor Authentication Status" AS tfa
FROM login_records_table l
JOIN user_information_table u ON l."User ID" = u."User ID"
"""))
ct3 = pd.crosstab(login2fa['dept'], login2fa['tfa'])
chi2c, pc, _, _ = stats.chi2_contingency(ct3)
print(f"Chi-square on 2FA Status x Department: chi2={chi2c:.3f}, p={pc:.4f}")
print(ct3)