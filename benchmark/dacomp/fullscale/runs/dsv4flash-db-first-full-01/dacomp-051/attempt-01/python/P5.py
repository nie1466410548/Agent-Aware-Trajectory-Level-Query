import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Per-user analysis: capability vs assignment fit
result = db.query("""
SELECT CAST(t.assignee_user_id AS TEXT) AS user_id, u.user_name,
  u.avg_close_time_assigned_days,
  u.number_of_open_tasks,
  u.number_of_tasks_completed,
  COUNT(*) AS n_tasks,
  SUM(CASE WHEN t.is_completed=1 THEN 1 ELSE 0 END) AS n_completed,
  ROUND(AVG(t.complexity_score),2) AS avg_complexity,
  ROUND(AVG(t.urgency_score),2) AS avg_urgency,
  ROUND(AVG(t.hours_assigned_to_completion),1) AS avg_atc,
  ROUND(AVG(t.avg_daily_activity_rate),3) AS avg_activity_rate,
  SUM(CASE WHEN t.delay_days>0 THEN 1 ELSE 0 END) AS n_delayed
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT)=u.user_id
WHERE t.is_valid_record=1
GROUP BY t.assignee_user_id
""")
per_user = db.frame(result)
print(f"Users with matched tasks: {len(per_user)}")

# Correlation between user speed and complexity of assigned tasks
corr_c, p_c = stats.pearsonr(per_user['avg_close_time_assigned_days'], per_user['avg_complexity'])
print(f"Correlation: user_avg_close_time vs avg_complexity_of_assigned_tasks: r={corr_c:.3f}, p={p_c:.4f}")

corr_u, p_u = stats.pearsonr(per_user['avg_close_time_assigned_days'], per_user['avg_urgency'])
print(f"Correlation: user_avg_close_time vs avg_urgency_of_assigned_tasks: r={corr_u:.3f}, p={p_u:.4f}")

# Workload correlation
corr_w, p_w = stats.pearsonr(per_user['avg_close_time_assigned_days'], per_user['n_tasks'])
print(f"Correlation: user_avg_close_time vs number_of_assigned_tasks: r={corr_w:.3f}, p={p_w:.4f}")

# Segmentation: slow users by complexity bucket of tasks they handle
slow_users = per_user[per_user['avg_close_time_assigned_days'] > 12.2541]
print(f"\nSlow users with tasks: {len(slow_users)}")
print("\nSlow user complexity profile of handled tasks:")
print(slow_users['avg_complexity'].describe())

# Does the complexity of tasks a slow user handles relate to their speed?
high_complex_slow = slow_users[slow_users['avg_complexity']>=3.5]
low_complex_slow = slow_users[slow_users['avg_complexity']<3.0]
print(f"\nSlow users handling high-complexity tasks (>=3.5): n={len(high_complex_slow)}, mean close time={high_complex_slow['avg_close_time_assigned_days'].mean():.2f}")
print(f"Slow users handling low-complexity tasks (<3.0): n={len(low_complex_slow)}, mean close time={low_complex_slow['avg_close_time_assigned_days'].mean():.2f}")

# Figure: user speed vs task complexity scatter
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

axes[0].scatter(per_user['avg_complexity'], per_user['avg_close_time_assigned_days'], alpha=0.5, s=per_user['n_tasks']*3)
axes[0].set_xlabel('Avg Complexity of Assigned Tasks'); axes[0].set_ylabel('User Avg Close Time (days)')
axes[0].set_title('User Speed vs Complexity of Assigned Tasks')
axes[0].axhline(12.2541, color='r', linestyle='--', label='1.5x overall avg')
axes[0].legend()

axes[1].scatter(per_user['n_tasks'], per_user['avg_close_time_assigned_days'], alpha=0.5)
axes[1].set_xlabel('Number of Assigned Tasks'); axes[1].set_ylabel('User Avg Close Time (days)')
axes[1].set_title('User Speed vs Task Load')
axes[1].axhline(12.2541, color='r', linestyle='--', label='1.5x overall avg')
axes[1].legend()

axes[2].scatter(per_user['avg_activity_rate'], per_user['avg_close_time_assigned_days'], alpha=0.5)
axes[2].set_xlabel('Avg Daily Activity Rate on Tasks'); axes[2].set_ylabel('User Avg Close Time (days)')
axes[2].set_title('User Speed vs Task Activity')
axes[2].axhline(12.2541, color='r', linestyle='--', label='1.5x overall avg')
axes[2].legend()

plt.tight_layout()
plt.savefig('/work/capability_fit.png', dpi=100)
print("Saved capability_fit.png")

# Also examine slow user concentration in teams vs completion rate
result = db.query("""
SELECT t.team_id,
  COUNT(*) AS total_tasks,
  ROUND(100.0*SUM(CASE WHEN t.is_completed=1 THEN 1 ELSE 0 END)/COUNT(*),2) AS completion_rate,
  COUNT(DISTINCT CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN t.assignee_user_id END) AS n_slow_users
FROM asana__task_lifecycle_analysis t
LEFT JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT)=u.user_id
WHERE t.is_valid_record=1
GROUP BY t.team_id
""")
team2 = db.frame(result)
# Check distribution of slow users across teams
print("\nSlow user concentration across teams:")
print(team2['n_slow_users'].describe())