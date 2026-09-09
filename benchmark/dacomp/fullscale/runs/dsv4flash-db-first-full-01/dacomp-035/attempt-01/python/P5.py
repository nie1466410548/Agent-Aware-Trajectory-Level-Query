import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dept_order = ['Sales Department', 'Marketing Department', 'Technical Department', 'Finance Department']
dept_labels = ['Sales', 'Marketing', 'Technical', 'Finance']
colors = ['#F39C12', '#2ECC71', '#E74C3C', '#3498DB']

# Fetch all needed data
dept_users = db.frame(db.query("SELECT Department, COUNT(*) AS user_count FROM user_information_table GROUP BY Department"))
dept_users = dept_users.set_index('Department').reindex(dept_order)

# 1. Anomaly data
anomaly_count = db.frame(db.query("""
SELECT u.Department AS dept, COUNT(*) AS cnt
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department
""")).set_index('dept').reindex(dept_order)

# 2. Remote login count
remote = db.frame(db.query("""
SELECT u.Department AS dept, COUNT(*) AS remote_cnt
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
WHERE a."Anomaly Type" = 'Remote Login'
GROUP BY u.Department
""")).set_index('dept').reindex(dept_order).fillna(0)

# 3. Repeat offenders
repeat = db.frame(db.query("""
SELECT u.Department AS dept,
  COUNT(DISTINCT CASE WHEN ua.anomaly_count >= 2 THEN u."User ID" ELSE NULL END) AS repeat_users,
  COUNT(DISTINCT u."User ID") AS total_users_with_anomalies
FROM (
  SELECT l."User ID", COUNT(*) AS anomaly_count
  FROM abnormal_logins_table a
  JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
  GROUP BY l."User ID"
) ua
JOIN user_information_table u ON ua."User ID" = u."User ID"
GROUP BY u.Department
""")).set_index('dept').reindex(dept_order)

# 4. Login metrics
login = db.frame(db.query("""
SELECT u.Department AS dept,
  COUNT(*) AS total_logins,
  SUM(CASE WHEN l."Authentication Status" = 'Failure' THEN 1 ELSE 0 END) AS failed,
  SUM(CASE WHEN l."Two-Factor Authentication Status" = 'Not Enabled' THEN 1 ELSE 0 END) AS no_2fa
FROM login_records_table l
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department
""")).set_index('dept').reindex(dept_order)

# 5. Account metrics
acct = db.frame(db.query("""
SELECT u.Department AS dept,
  AVG(ua."Password Attempt Count") AS avg_pw_attempts,
  SUM(CASE WHEN ua."Account Lock Status" = 'Locked' THEN 1 ELSE 0 END) AS locked,
  COUNT(*) AS acct_count
FROM user_account_table ua
JOIN user_information_table u ON ua."User ID" = u."User ID"
GROUP BY u.Department
""")).set_index('dept').reindex(dept_order)

# 6. System logs handling - unprocessed
logs = db.frame(db.query("""
SELECT u.Department AS dept,
  COUNT(*) AS total_logs,
  SUM(CASE WHEN sl."Handling Status" = 'Unprocessed' THEN 1 ELSE 0 END) AS unprocessed
FROM system_logs_table sl
JOIN login_records_table l ON sl."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department
""")).set_index('dept').reindex(dept_order)

# 7. Security events (high severity)
events = db.frame(db.query("""
SELECT u.Department AS dept,
  COUNT(*) AS total_events,
  SUM(CASE WHEN se."Severity" IN ('High', 'Severe') THEN 1 ELSE 0 END) AS high_events
FROM security_events_table se
JOIN login_records_table l ON se."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department
""")).set_index('dept').reindex(dept_order)

# 8. Confirmed anomaly rate
confirmed = db.frame(db.query("""
SELECT u.Department AS dept,
  SUM(CASE WHEN a."Confirmation Status" = 'Confirmed' THEN 1 ELSE 0 END) AS confirmed_cnt,
  COUNT(*) AS total_anomalies
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department
""")).set_index('dept').reindex(dept_order)

# Compute composite metrics
df = pd.DataFrame(index=dept_order)
df['user_count'] = dept_users['user_count']

# Anomaly rate per 100 users
df['anomaly_per_100'] = anomaly_count['cnt'] / df['user_count'] * 100

# Remote login rate per 100 users
df['remote_per_100'] = remote['remote_cnt'] / df['user_count'] * 100

# Repeat offender rate
df['repeat_rate'] = repeat['repeat_users'] / repeat['total_users_with_anomalies'] * 100

# Failed login rate
df['failed_rate'] = login['failed'] / login['total_logins'] * 100

# No 2FA rate
df['no_2fa_rate'] = login['no_2fa'] / login['total_logins'] * 100

# Locked account rate
df['locked_rate'] = acct['locked'] / acct['acct_count'] * 100

# Unprocessed log rate
df['unprocessed_rate'] = logs['unprocessed'] / logs['total_logs'] * 100

# High severity events per 100 users
df['high_events_per_100'] = events['high_events'] / df['user_count'] * 100

# Confirmed anomaly rate (confirmed = real threats, higher = more actual incidents)
df['confirmed_rate'] = confirmed['confirmed_cnt'] / confirmed['total_anomalies'] * 100

# Normalize each metric (0-1, higher = weaker awareness)
# For confirmed_rate, more confirmed anomalies = more real incidents = weaker awareness
# For unprocessed_rate, more unprocessed = less responsiveness = weaker awareness

metrics = ['anomaly_per_100', 'remote_per_100', 'repeat_rate', 'failed_rate', 
           'no_2fa_rate', 'locked_rate', 'unprocessed_rate', 'high_events_per_100', 'confirmed_rate']

for m in metrics:
    mn, mx = df[m].min(), df[m].max()
    df[f'{m}_norm'] = (df[m] - mn) / (mx - mn) if mx > mn else 0.5

# Composite score (equal weight)
norm_cols = [f'{m}_norm' for m in metrics]
df['composite'] = df[norm_cols].mean(axis=1)
df = df.sort_values('composite', ascending=False)
df['rank'] = range(1, len(df) + 1)

print("=== FOCUSED SECURITY AWARENESS WEAKNESS ANALYSIS ===")
print("Higher composite score = weaker security awareness = higher priority for guidance")
print()
for dept in df.index:
    print(f"Rank {df.loc[dept, 'rank']:.0f}: {dept}")
    print(f"  Composite Weakness Score: {df.loc[dept, 'composite']:.3f}")
    for m in metrics:
        print(f"    {m}: {df.loc[dept, m]:.2f} (norm: {df.loc[dept, f'{m}_norm']:.3f})")
    print()

print("=== SUMMARY ===")
print(df[['rank', 'composite'] + metrics].round(2).to_string())

# Create visualization
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# Bar chart of composite scores
ax1 = axes[0]
bars = ax1.bar(df.index, df['composite'], color=colors)
ax1.set_title('Security Awareness Weakness Composite Score\n(Higher = Weaker = Higher Priority)', fontsize=13, fontweight='bold')
ax1.set_ylabel('Composite Weakness Score')
ax1.set_ylim(0, 1.0)
for bar, val in zip(bars, df['composite']):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, f'{val:.3f}', 
             ha='center', fontweight='bold', fontsize=12)
ax1.set_xticklabels(df.index, rotation=0, fontsize=10)

# Heatmap of normalized metrics
ax2 = axes[1]
heatmap_data = df[norm_cols].T
heatmap_data.index = [m.replace('_', ' ').title() for m in metrics]
im = ax2.imshow(heatmap_data.values, cmap='RdYlGn_r', aspect='auto', vmin=0, vmax=1)
ax2.set_xticks(range(len(df.index)))
ax2.set_xticklabels(df.index, rotation=0, fontsize=10)
ax2.set_yticks(range(len(metrics)))
ax2.set_yticklabels(heatmap_data.index, fontsize=9)
ax2.set_title('Normalized Risk Indicators by Department\n(Darker Red = Weaker Awareness)', fontsize=13, fontweight='bold')
fig.colorbar(im, ax=ax2, shrink=0.8, label='Normalized Risk (0=Low, 1=High)')

# Add text annotations
for i in range(len(metrics)):
    for j in range(len(df.index)):
        val = heatmap_data.iloc[i, j]
        color = 'white' if val > 0.6 else 'black'
        ax2.text(j, i, f'{val:.2f}', ha='center', va='center', fontsize=9, color=color)

plt.tight_layout()
plt.savefig('/work/security_awareness_weakness_score.png', dpi=150, bbox_inches='tight')
plt.close()
print("\nSaved figure to /work/security_awareness_weakness_score.png")