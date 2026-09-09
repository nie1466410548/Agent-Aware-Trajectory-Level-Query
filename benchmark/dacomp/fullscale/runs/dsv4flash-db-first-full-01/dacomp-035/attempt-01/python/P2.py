import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Re-fetch the data using db.query for visualization
# Department user counts
dept_users = db.frame(db.query("SELECT Department, COUNT(*) AS user_count FROM user_information_table GROUP BY Department"))

# Key metrics for visualization
# 1. Anomaly count per department
anomaly_counts = db.frame(db.query("""
SELECT u.Department, COUNT(*) AS anomaly_count
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department
ORDER BY anomaly_count DESC
"""))

# 2. Risk level distribution
risk_dist = db.frame(db.query("""
SELECT u.Department, a."Risk Level", COUNT(*) AS cnt
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department, a."Risk Level"
ORDER BY u.Department, a."Risk Level"
"""))

# 3. Anomaly types
type_dist = db.frame(db.query("""
SELECT u.Department, a."Anomaly Type", COUNT(*) AS cnt
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department, a."Anomaly Type"
ORDER BY u.Department, a."Anomaly Type"
"""))

# 4. Login metrics per department
login_metrics = db.frame(db.query("""
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

# 5. Repeat offenders
repeat_data = db.frame(db.query("""
SELECT 
  u.Department,
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
"""))

# 6. Account data
acct_metrics = db.frame(db.query("""
SELECT 
  u.Department,
  AVG(ua."Password Attempt Count") AS avg_password_attempts,
  SUM(CASE WHEN ua."Account Lock Status" = 'Locked' THEN 1 ELSE 0 END) AS locked_accounts,
  COUNT(*) AS account_count
FROM user_account_table ua
JOIN user_information_table u ON ua."User ID" = u."User ID"
GROUP BY u.Department
"""))

# Set up the figure
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle('Department Security Awareness Analysis', fontsize=16, fontweight='bold')

# Color scheme
colors = ['#E74C3C', '#F39C12', '#3498DB', '#2ECC71']
dept_order = ['Technical Department', 'Sales Department', 'Finance Department', 'Marketing Department']
dept_labels = ['Technical', 'Sales', 'Finance', 'Marketing']

# Chart 1: Anomalies per 100 users
ax1 = axes[0, 0]
merged = anomaly_counts.merge(dept_users, on='Department')
merged['anomaly_per_100'] = merged['anomaly_count'] / merged['user_count'] * 100
merged = merged.set_index('Department').reindex(dept_order)
bars = ax1.bar(dept_labels, merged['anomaly_per_100'], color=colors)
ax1.set_title('Anomalies per 100 Users', fontsize=13)
ax1.set_ylabel('Count')
ax1.set_ylim(0, merged['anomaly_per_100'].max() * 1.2)
for bar, val in zip(bars, merged['anomaly_per_100']):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f'{val:.1f}', ha='center', fontweight='bold')

# Chart 2: High/Severe anomaly percentage
ax2 = axes[0, 1]
risk_pivot = risk_dist.pivot_table(index='Department', columns='Risk Level', values='cnt', aggfunc='sum').fillna(0)
risk_pivot = risk_pivot.reindex(dept_order)
risk_pivot['high_severe'] = risk_pivot.get('High', 0) + risk_pivot.get('Severe', 0)
risk_pivot['total'] = risk_pivot.sum(axis=1)
risk_pivot['pct_high_severe'] = risk_pivot['high_severe'] / risk_pivot['total'] * 100
bars = ax2.bar(dept_labels, risk_pivot['pct_high_severe'], color=colors)
ax2.set_title('% High/Severe Risk Anomalies', fontsize=13)
ax2.set_ylabel('Percentage (%)')
ax2.set_ylim(0, 80)
for bar, val in zip(bars, risk_pivot['pct_high_severe']):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{val:.1f}%', ha='center', fontweight='bold')

# Chart 3: Failed login & No 2FA rates
ax3 = axes[0, 2]
login_metrics['failed_rate'] = login_metrics['failed_logins'] / login_metrics['total_logins'] * 100
login_metrics['no_2fa_rate'] = login_metrics['no_2fa_logins'] / login_metrics['total_logins'] * 100
login_metrics = login_metrics.set_index('Department').reindex(dept_order)

x = np.arange(len(dept_labels))
width = 0.35
bars1 = ax3.bar(x - width/2, login_metrics['failed_rate'], width, label='Failed Login %', color='#E74C3C')
bars2 = ax3.bar(x + width/2, login_metrics['no_2fa_rate'], width, label='No 2FA %', color='#F39C12')
ax3.set_title('Login Security Indicators', fontsize=13)
ax3.set_ylabel('Percentage (%)')
ax3.set_xticks(x)
ax3.set_xticklabels(dept_labels)
ax3.legend()
ax3.set_ylim(0, 75)
for bar in bars1:
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{bar.get_height():.1f}%', ha='center', fontsize=9)
for bar in bars2:
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{bar.get_height():.1f}%', ha='center', fontsize=9)

# Chart 4: Repeat offender rate
ax4 = axes[1, 0]
repeat_data['repeat_rate'] = repeat_data['repeat_users'] / repeat_data['total_users_with_anomalies'] * 100
repeat_data = repeat_data.set_index('Department').reindex(dept_order)
bars = ax4.bar(dept_labels, repeat_data['repeat_rate'], color=colors)
ax4.set_title('Repeat Offender Rate\n(% of Users with Multiple Anomalies)', fontsize=13)
ax4.set_ylabel('Percentage (%)')
ax4.set_ylim(0, 60)
for bar, val in zip(bars, repeat_data['repeat_rate']):
    ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{val:.1f}%', ha='center', fontweight='bold')

# Chart 5: Locked accounts & Password attempts
ax5 = axes[1, 1]
acct_metrics['locked_rate'] = acct_metrics['locked_accounts'] / acct_metrics['account_count'] * 100
acct_metrics = acct_metrics.set_index('Department').reindex(dept_order)

# Twin axis
color1 = '#E74C3C'
color2 = '#3498DB'
bars5 = ax5.bar(x - width/2, acct_metrics['locked_rate'], width, label='Locked Account %', color=color1)
ax5.set_ylabel('Locked Account %', color=color1)
ax5.set_xticks(x)
ax5.set_xticklabels(dept_labels)
ax5.set_ylim(0, 70)
ax5_2 = ax5.twinx()
bars5_2 = ax5_2.bar(x + width/2, acct_metrics['avg_password_attempts'], width, label='Avg Password Attempts', color=color2)
ax5_2.set_ylabel('Avg Password Attempts', color=color2)
ax5_2.set_ylim(0, 4)
ax5.set_title('Account Security Indicators', fontsize=13)
for bar in bars5:
    ax5.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{bar.get_height():.1f}%', ha='center', fontsize=9)
for bar in bars5_2:
    ax5_2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, f'{bar.get_height():.2f}', ha='center', fontsize=9)

# Chart 6: Anomaly type distribution (stacked bar)
ax6 = axes[1, 2]
type_pivot = type_dist.pivot_table(index='Department', columns='Anomaly Type', values='cnt', aggfunc='sum').fillna(0)
type_pivot = type_pivot.reindex(dept_order)
type_pivot_pct = type_pivot.div(type_pivot.sum(axis=1), axis=0) * 100
type_pivot_pct.plot(kind='bar', stacked=True, ax=ax6, colormap='Set2')
ax6.set_title('Anomaly Type Distribution by Department', fontsize=13)
ax6.set_ylabel('Percentage (%)')
ax6.set_xticklabels(dept_labels, rotation=0)
ax6.legend(loc='upper right', fontsize=9)

plt.tight_layout()
plt.savefig('/work/department_security_awareness_analysis.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved figure to /work/department_security_awareness_analysis.png")

# Create a radar chart
fig2, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
categories = ['Anomaly Rate', 'Repeat Offenders', 'Failed Logins', 'No 2FA', 
              'Locked Accounts', 'High/Severe Anomalies', 'Avg Anomaly Score', 'Security Events']
N = len(categories)

# Normalize values for radar chart
# Anomaly rate per user
merged2 = anomaly_counts.merge(dept_users, on='Department')
merged2['anomaly_per_user'] = merged2['anomaly_count'] / merged2['user_count']
anomaly_rate = merged2.set_index('Department').reindex(dept_order)['anomaly_per_user'].values
anomaly_rate_norm = (anomaly_rate - anomaly_rate.min()) / (anomaly_rate.max() - anomaly_rate.min() + 0.001)

# Repeat rate
rr = repeat_data.set_index('Department').reindex(dept_order)['repeat_rate'].values / 100
rr_norm = (rr - rr.min()) / (rr.max() - rr.min() + 0.001)

# Failed login rate
flr = login_metrics['failed_rate'].values / 100
flr_norm = (flr - flr.min()) / (flr.max() - flr.min() + 0.001)

# No 2FA rate
n2fa = login_metrics['no_2fa_rate'].values / 100
n2fa_norm = (n2fa - n2fa.min()) / (n2fa.max() - n2fa.min() + 0.001)

# Locked rate
lr = acct_metrics['locked_rate'].values / 100
lr_norm = (lr - lr.min()) / (lr.max() - lr.min() + 0.001)

# High/Severe %
hs = risk_pivot['pct_high_severe'].values / 100
hs_norm = (hs - hs.min()) / (hs.max() - hs.min() + 0.001)

# Avg anomaly score (from earlier query)
score_data = db.frame(db.query("""
SELECT u.Department, ROUND(AVG(a."Anomaly Score"), 2) AS avg_score
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department
"""))
scores = score_data.set_index('Department').reindex(dept_order)['avg_score'].values
scores_norm = (scores - scores.min()) / (scores.max() - scores.min() + 0.001)

# Events per user
events_data = db.frame(db.query("""
SELECT u.Department, COUNT(*) AS event_count
FROM security_events_table se
JOIN login_records_table l ON se."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department
"""))
ev = events_data.set_index('Department').reindex(dept_order)['event_count'].values / dept_users.set_index('Department').reindex(dept_order)['user_count'].values
ev_norm = (ev - ev.min()) / (ev.max() - ev.min() + 0.001)

# Build radar data
values = {
    'Technical Department': [anomaly_rate_norm[0], rr_norm[0], flr_norm[0], n2fa_norm[0], lr_norm[0], hs_norm[0], scores_norm[0], ev_norm[0]],
    'Sales Department': [anomaly_rate_norm[1], rr_norm[1], flr_norm[1], n2fa_norm[1], lr_norm[1], hs_norm[1], scores_norm[1], ev_norm[1]],
    'Finance Department': [anomaly_rate_norm[2], rr_norm[2], flr_norm[2], n2fa_norm[2], lr_norm[2], hs_norm[2], scores_norm[2], ev_norm[2]],
    'Marketing Department': [anomaly_rate_norm[3], rr_norm[3], flr_norm[3], n2fa_norm[3], lr_norm[3], hs_norm[3], scores_norm[3], ev_norm[3]]
}

angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
angles += angles[:1]

dept_colors = {'Technical Department': '#E74C3C', 'Sales Department': '#F39C12', 
               'Finance Department': '#3498DB', 'Marketing Department': '#2ECC71'}

for dept in dept_order:
    vals = values[dept] + values[dept][:1]
    ax.plot(angles, vals, 'o-', linewidth=2, label=dept_labels[dept_order.index(dept)], color=dept_colors[dept])
    ax.fill(angles, vals, alpha=0.1, color=dept_colors[dept])

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=10)
ax.set_ylim(0, 1.1)
ax.set_title('Security Awareness Risk Profile (Radar Chart)', fontsize=14, fontweight='bold', pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
plt.tight_layout()
plt.savefig('/work/department_security_radar.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved radar chart to /work/department_security_radar.png")

print("\nAll visualizations saved successfully.")