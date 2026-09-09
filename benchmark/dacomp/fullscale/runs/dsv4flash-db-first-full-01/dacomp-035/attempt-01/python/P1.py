import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Get all the data needed
# 1. Department user counts
dept_users = db.frame(db.query("SELECT Department, COUNT(*) AS user_count FROM user_information_table GROUP BY Department"))

# 2. Anomaly data per department
anomaly_dept = db.frame(db.query("""
SELECT 
  u.Department,
  COUNT(*) AS anomaly_count,
  COUNT(DISTINCT l."User ID") AS users_with_anomalies,
  ROUND(AVG(a."Anomaly Score"), 2) AS avg_anomaly_score,
  ROUND(AVG(a."Device Anomaly Indicators"), 2) AS avg_device_indicator,
  ROUND(AVG(a."Network Anomaly Indicators"), 2) AS avg_network_indicator,
  ROUND(AVG(a."Behavior Anomaly Indicators"), 2) AS avg_behavior_indicator,
  ROUND(100.0 * SUM(CASE WHEN a."Risk Level" IN ('High', 'Severe') THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_high_severe,
  ROUND(100.0 * SUM(CASE WHEN a."Confirmation Status" = 'Confirmed' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_confirmed
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department
"""))

# 3. Repeat offenders
repeat = db.frame(db.query("""
SELECT 
  u.Department,
  COUNT(DISTINCT CASE WHEN ua.anomaly_count >= 2 THEN u."User ID" ELSE NULL END) AS repeat_users,
  SUM(CASE WHEN ua.anomaly_count >= 2 THEN ua.anomaly_count ELSE 0 END) AS repeat_anomalies
FROM (
  SELECT l."User ID", COUNT(*) AS anomaly_count
  FROM abnormal_logins_table a
  JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
  GROUP BY l."User ID"
) ua
JOIN user_information_table u ON ua."User ID" = u."User ID"
GROUP BY u.Department
"""))

# 4. Login data
login_dept = db.frame(db.query("""
SELECT 
  u.Department,
  COUNT(*) AS total_logins,
  SUM(CASE WHEN l."Authentication Status" = 'Failure' THEN 1 ELSE 0 END) AS failed_logins,
  SUM(CASE WHEN l."Two-Factor Authentication Status" = 'Not Enabled' THEN 1 ELSE 0 END) AS no_2fa_logins,
  COUNT(DISTINCT l."User ID") AS active_users
FROM login_records_table l
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department
"""))

# 5. Account data
acct_dept = db.frame(db.query("""
SELECT 
  u.Department,
  AVG(ua."Password Attempt Count") AS avg_password_attempts,
  SUM(CASE WHEN ua."Account Lock Status" = 'Locked' THEN 1 ELSE 0 END) AS locked_accounts,
  COUNT(*) AS account_count
FROM user_account_table ua
JOIN user_information_table u ON ua."User ID" = u."User ID"
GROUP BY u.Department
"""))

# 6. Security events
events_dept = db.frame(db.query("""
SELECT 
  u.Department,
  COUNT(*) AS total_events,
  SUM(CASE WHEN se."Severity" IN ('High', 'Severe') THEN 1 ELSE 0 END) AS high_sev_events,
  AVG(se."Risk Score") AS avg_risk_score
FROM security_events_table se
JOIN login_records_table l ON se."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department
"""))

# Merge all data
dept = dept_users.copy()
dept = dept.merge(anomaly_dept, on='Department', how='left')
dept = dept.merge(repeat, on='Department', how='left')
dept = dept.merge(login_dept, on='Department', how='left')
dept = dept.merge(acct_dept, on='Department', how='left')
dept = dept.merge(events_dept, on='Department', how='left')

# Compute normalized metrics
# 1. Anomaly rate per user
dept['anomaly_per_user'] = dept['anomaly_count'] / dept['user_count']

# 2. Repeat offender rate
dept['repeat_user_rate'] = dept['repeat_users'] / dept['users_with_anomalies']

# 3. Failed login rate
dept['failed_login_rate'] = dept['failed_logins'] / dept['total_logins']

# 4. No 2FA rate
dept['no_2fa_rate'] = dept['no_2fa_logins'] / dept['total_logins']

# 5. Locked account rate
dept['locked_account_rate'] = dept['locked_accounts'] / dept['account_count']

# 6. Security events per user
dept['events_per_user'] = dept['total_events'] / dept['user_count']

# 7. High severity events per user
dept['high_events_per_user'] = dept['high_sev_events'] / dept['user_count']

# 8. Average anomaly score (higher is worse)
# Already have avg_anomaly_score

# 9. High+severe anomaly percentage
# Already have pct_high_severe

# Normalize each metric to 0-1 scale (higher = weaker security awareness)
metrics = ['anomaly_per_user', 'repeat_user_rate', 'failed_login_rate', 'no_2fa_rate',
           'locked_account_rate', 'events_per_user', 'high_events_per_user',
           'avg_anomaly_score', 'pct_high_severe']

for m in metrics:
    min_val = dept[m].min()
    max_val = dept[m].max()
    if max_val > min_val:
        dept[f'{m}_norm'] = (dept[m] - min_val) / (max_val - min_val)
    else:
        dept[f'{m}_norm'] = 0.5

# Composite score (equal weight)
norm_cols = [f'{m}_norm' for m in metrics]
dept['composite_risk_score'] = dept[norm_cols].mean(axis=1)

# Rank
dept = dept.sort_values('composite_risk_score', ascending=False)
dept['rank'] = range(1, len(dept) + 1)

print("=== COMPREHENSIVE SECURITY AWARENESS RISK ANALYSIS ===")
print()
for _, row in dept.iterrows():
    print(f"Department: {row['Department']}")
    print(f"  Rank: {row['rank']}")
    print(f"  Composite Risk Score: {row['composite_risk_score']:.3f}")
    print(f"  Users: {row['user_count']}")
    print(f"  Anomaly count: {row['anomaly_count']}")
    print(f"  Anomalies per user: {row['anomaly_per_user']:.3f}")
    print(f"  Users with anomalies: {row['users_with_anomalies']}")
    print(f"  Repeat offender rate: {row['repeat_user_rate']:.3f}")
    print(f"  Avg anomaly score: {row['avg_anomaly_score']}")
    print(f"  % High/Severe anomalies: {row['pct_high_severe']}%")
    print(f"  % Confirmed anomalies: {row['pct_confirmed']}%")
    print(f"  Failed login rate: {row['failed_login_rate']:.3f}")
    print(f"  No 2FA rate: {row['no_2fa_rate']:.3f}")
    print(f"  Avg password attempts: {row['avg_password_attempts']:.3f}")
    print(f"  Locked account rate: {row['locked_account_rate']:.3f}")
    print(f"  Security events per user: {row['events_per_user']:.3f}")
    print(f"  High severity events per user: {row['high_events_per_user']:.3f}")
    print()

# Print detailed metrics
print("=== NORMALIZED METRICS ===")
for _, row in dept.iterrows():
    print(f"\n{row['Department']}:")
    for m in metrics:
        print(f"  {m}: {row[m]:.3f} (normalized: {row[f'{m}_norm']:.3f})")

print("\n\n=== SUMMARY ===")
print(dept[['Department', 'rank', 'composite_risk_score', 'anomaly_per_user', 'repeat_user_rate', 
           'failed_login_rate', 'no_2fa_rate', 'locked_account_rate', 'pct_high_severe']].to_string(index=False))