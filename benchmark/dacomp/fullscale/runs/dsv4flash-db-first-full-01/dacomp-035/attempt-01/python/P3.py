import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dept_order = ['Technical Department', 'Sales Department', 'Finance Department', 'Marketing Department']
dept_labels = ['Technical', 'Sales', 'Finance', 'Marketing']

# Re-fetch data with clean queries
dept_users = db.frame(db.query("SELECT Department, COUNT(*) AS user_count FROM user_information_table GROUP BY Department"))
dept_users = dept_users.set_index('Department').reindex(dept_order)

anomaly_counts = db.frame(db.query("""
SELECT u.Department AS dept, COUNT(*) AS anomaly_count
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department
""")).set_index('dept').reindex(dept_order)

risk_dist = db.frame(db.query("""
SELECT u.Department AS dept, a."Risk Level" AS rl, COUNT(*) AS cnt
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department, a."Risk Level"
"""))
risk_pivot = risk_dist.pivot_table(index='dept', columns='rl', values='cnt', aggfunc='sum').fillna(0).reindex(dept_order)
risk_pivot['hs'] = risk_pivot.get('High', 0) + risk_pivot.get('Severe', 0)
risk_pivot['total'] = risk_pivot.sum(axis=1)
risk_pivot['pct_hs'] = risk_pivot['hs'] / risk_pivot['total'] * 100

login_metrics = db.frame(db.query("""
SELECT u.Department AS dept,
  COUNT(*) AS total_logins,
  SUM(CASE WHEN l."Authentication Status" = 'Failure' THEN 1 ELSE 0 END) AS failed_logins,
  SUM(CASE WHEN l."Two-Factor Authentication Status" = 'Not Enabled' THEN 1 ELSE 0 END) AS no_2fa_logins
FROM login_records_table l
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department
""")).set_index('dept').reindex(dept_order)
login_metrics['failed_rate'] = login_metrics['failed_logins'] / login_metrics['total_logins'] * 100
login_metrics['no_2fa_rate'] = login_metrics['no_2fa_logins'] / login_metrics['total_logins'] * 100

repeat_data = db.frame(db.query("""
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
repeat_data['repeat_rate'] = repeat_data['repeat_users'] / repeat_data['total_users_with_anomalies'] * 100

acct_metrics = db.frame(db.query("""
SELECT u.Department AS dept,
  AVG(ua."Password Attempt Count") AS avg_pw,
  SUM(CASE WHEN ua."Account Lock Status" = 'Locked' THEN 1 ELSE 0 END) AS locked,
  COUNT(*) AS acct_count
FROM user_account_table ua
JOIN user_information_table u ON ua."User ID" = u."User ID"
GROUP BY u.Department
""")).set_index('dept').reindex(dept_order)
acct_metrics['locked_rate'] = acct_metrics['locked'] / acct_metrics['acct_count'] * 100

score_data = db.frame(db.query("""
SELECT u.Department AS dept, AVG(a."Anomaly Score") AS avg_score
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department
""")).set_index('dept').reindex(dept_order)

events_data = db.frame(db.query("""
SELECT u.Department AS dept, COUNT(*) AS event_count
FROM security_events_table se
JOIN login_records_table l ON se."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department
""")).set_index('dept').reindex(dept_order)

# Build normalized metrics (0-1 scale)
def norm(series):
    return (series - series.min()) / (series.max() - series.min() + 0.001)

anomaly_rate = anomaly_counts['anomaly_count'] / dept_users['user_count']
failed_rate = login_metrics['failed_rate'] / 100
no_2fa = login_metrics['no_2fa_rate'] / 100
repeat_rate = repeat_data['repeat_rate'] / 100
locked_rate = acct_metrics['locked_rate'] / 100
pct_hs = risk_pivot['pct_hs'] / 100
avg_score = score_data['avg_score']
events_per_user = events_data['event_count'] / dept_users['user_count']

categories = ['Anomaly Rate', 'Repeat Offenders', 'Failed Logins', 'No 2FA',
              'Locked Accounts', 'High/Severe', 'Avg Score', 'Security Events']
N = len(categories)
angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
angles += angles[:1]

values = {
    'Technical Department': [norm(anomaly_rate)['Technical Department'], norm(repeat_rate)['Technical Department'],
                             norm(failed_rate)['Technical Department'], norm(no_2fa)['Technical Department'],
                             norm(locked_rate)['Technical Department'], norm(pct_hs)['Technical Department'],
                             norm(avg_score)['Technical Department'], norm(events_per_user)['Technical Department']],
    'Sales Department': [norm(anomaly_rate)['Sales Department'], norm(repeat_rate)['Sales Department'],
                         norm(failed_rate)['Sales Department'], norm(no_2fa)['Sales Department'],
                         norm(locked_rate)['Sales Department'], norm(pct_hs)['Sales Department'],
                         norm(avg_score)['Sales Department'], norm(events_per_user)['Sales Department']],
    'Finance Department': [norm(anomaly_rate)['Finance Department'], norm(repeat_rate)['Finance Department'],
                           norm(failed_rate)['Finance Department'], norm(no_2fa)['Finance Department'],
                           norm(locked_rate)['Finance Department'], norm(pct_hs)['Finance Department'],
                           norm(avg_score)['Finance Department'], norm(events_per_user)['Finance Department']],
    'Marketing Department': [norm(anomaly_rate)['Marketing Department'], norm(repeat_rate)['Marketing Department'],
                             norm(failed_rate)['Marketing Department'], norm(no_2fa)['Marketing Department'],
                             norm(locked_rate)['Marketing Department'], norm(pct_hs)['Marketing Department'],
                             norm(avg_score)['Marketing Department'], norm(events_per_user)['Marketing Department']]
}

fig2, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
dept_colors = {'Technical Department': '#E74C3C', 'Sales Department': '#F39C12',
               'Finance Department': '#3498DB', 'Marketing Department': '#2ECC71'}

for dept in dept_order:
    vals = values[dept] + values[dept][:1]
    ax.plot(angles, vals, 'o-', linewidth=2, label=dept_labels[dept_order.index(dept)], color=dept_colors[dept])
    ax.fill(angles, vals, alpha=0.1, color=dept_colors[dept])

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=10)
ax.set_ylim(0, 1.1)
ax.set_title('Security Awareness Risk Profile by Department', fontsize=14, fontweight='bold', pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
plt.tight_layout()
plt.savefig('/work/department_security_radar.png', dpi=150, bbox_inches='tight')
plt.close()
print("Radar chart saved to /work/department_security_radar.png")
print("All visualizations ready.")