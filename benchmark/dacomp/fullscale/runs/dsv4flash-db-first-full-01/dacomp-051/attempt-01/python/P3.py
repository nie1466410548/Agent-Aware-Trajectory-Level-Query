import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Time trends by cohort
result = db.query("""
SELECT strftime('%Y-%m', t.created_at) AS month,
  CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END AS cohort,
  COUNT(*) AS n_tasks,
  SUM(CASE WHEN t.is_completed=1 THEN 1 ELSE 0 END) AS n_completed,
  ROUND(AVG(t.hours_assigned_to_completion),1) AS avg_atc,
  ROUND(AVG(t.avg_daily_activity_rate),3) AS avg_daily_activity
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE t.is_valid_record=1 AND t.created_at IS NOT NULL
GROUP BY month, cohort
ORDER BY month
""")
time_df = db.frame(result)
print(time_df)

# Also overall monthly completion rate
result2 = db.query("""
SELECT strftime('%Y-%m', created_at) AS month, COUNT(*) AS n_tasks,
SUM(CASE WHEN is_completed=1 THEN 1 ELSE 0 END) AS n_completed,
ROUND(100.0*SUM(CASE WHEN is_completed=1 THEN 1 ELSE 0 END)/COUNT(*),1) AS comp_rate
FROM asana__task_lifecycle_analysis
WHERE is_valid_record=1 AND created_at IS NOT NULL
GROUP BY month ORDER BY month
""")
all_time = db.frame(result2)
print("\nAll-time monthly:")
print(all_time)

fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# Plot completion rate by month
for cohort in ['FAST', 'SLOW']:
    d = time_df[time_df['cohort']==cohort]
    axes[0].plot(d['month'], 100.0*d['n_completed']/d['n_tasks'], marker='o', label=cohort)
axes[0].plot(all_time['month'], all_time['comp_rate'], marker='s', label='ALL', linestyle='--', alpha=0.7)
axes[0].set_xlabel('Month'); axes[0].set_ylabel('Completion Rate (%)')
axes[0].set_title('Monthly Completion Rate by Cohort')
axes[0].legend(); axes[0].tick_params(axis='x', rotation=45)

# Avg assigned-to-completion hours by month
for cohort in ['FAST', 'SLOW']:
    d = time_df[time_df['cohort']==cohort]
    axes[1].plot(d['month'], d['avg_atc'], marker='o', label=cohort)
axes[1].set_xlabel('Month'); axes[1].set_ylabel('Avg Hours Assigned→Completion')
axes[1].set_title('Monthly Avg Hours to Completion')
axes[1].legend(); axes[1].tick_params(axis='x', rotation=45)

# Task volume by month
for cohort in ['FAST', 'SLOW']:
    d = time_df[time_df['cohort']==cohort]
    axes[2].bar(d['month'], d['n_tasks'], label=cohort, alpha=0.6)
axes[2].set_xlabel('Month'); axes[2].set_ylabel('Tasks Created')
axes[2].set_title('Monthly Task Volume')
axes[2].legend(); axes[2].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('/work/time_trends.png', dpi=100)
print("Saved time_trends.png")

# Workload vs speed correlation
result3 = db.query("""
SELECT u.user_id, u.user_name, u.avg_close_time_assigned_days,
  u.number_of_open_tasks, u.number_of_tasks_completed,
  ts.n_tasks AS tasks_in_table,
  ts.n_completed AS completed_in_table
FROM asana__user u
LEFT JOIN (
  SELECT CAST(assignee_user_id AS TEXT) AS user_id, COUNT(*) AS n_tasks,
    SUM(CASE WHEN is_completed=1 THEN 1 ELSE 0 END) AS n_completed
  FROM asana__task_lifecycle_analysis
  WHERE is_valid_record=1
  GROUP BY assignee_user_id
) ts ON u.user_id = ts.user_id
""")
user_df = db.frame(result3)
print(f"\nUsers with task data: {user_df['tasks_in_table'].notna().sum()}")

# Correlation: avg_close_time vs open tasks
sub = user_df.dropna(subset=['tasks_in_table'])
corr, p = stats.pearsonr(sub['avg_close_time_assigned_days'], sub['tasks_in_table'])
print(f"Correlation: avg_close_time vs n_tasks_in_table: r={corr:.3f}, p={p:.4f}")
corr2, p2 = stats.pearsonr(sub['avg_close_time_assigned_days'], sub['number_of_open_tasks'])
print(f"Correlation: avg_close_time vs number_of_open_tasks: r={corr2:.3f}, p={p2:.4f}")

# Check high open-task users
high_open = user_df.nlargest(15, 'number_of_open_tasks')
print("\nTop 15 users by open tasks:")
print(high_open[['user_name', 'avg_close_time_assigned_days', 'number_of_open_tasks', 'number_of_tasks_completed', 'tasks_in_table']].to_string())