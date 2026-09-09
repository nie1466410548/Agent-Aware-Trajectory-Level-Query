import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Team-level analysis
result = db.query("""
SELECT t.team_id,
  COUNT(*) AS total_tasks,
  SUM(CASE WHEN t.is_completed=1 THEN 1 ELSE 0 END) AS completed_tasks,
  ROUND(100.0*SUM(CASE WHEN t.is_completed=1 THEN 1 ELSE 0 END)/COUNT(*),2) AS completion_rate,
  ROUND(AVG(t.project_health_score),2) AS avg_project_health,
  ROUND(AVG(t.hours_assigned_to_completion),1) AS avg_hours_atc,
  ROUND(AVG(t.complexity_score),2) AS avg_complexity,
  ROUND(AVG(t.urgency_score),2) AS avg_urgency,
  COUNT(DISTINCT t.assignee_user_id) AS n_users,
  COUNT(DISTINCT CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN t.assignee_user_id END) AS n_slow_users,
  ROUND(100.0*COUNT(DISTINCT CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN t.assignee_user_id END)/NULLIF(COUNT(DISTINCT t.assignee_user_id),0),2) AS slow_user_pct
FROM asana__task_lifecycle_analysis t
LEFT JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT)=u.user_id
WHERE t.is_valid_record=1
GROUP BY t.team_id
ORDER BY completion_rate ASC
""")
team_df = db.frame(result)
print(f"Teams: {len(team_df)}")
print(team_df.head(10))

# Correlation between slow_user_pct and completion_rate
corr, p_val = stats.pearsonr(team_df['slow_user_pct'], team_df['completion_rate'])
print(f"\nCorrelation: slow_user_pct vs completion_rate: r={corr:.3f}, p={p_val:.4f}")

corr2, p_val2 = stats.pearsonr(team_df['slow_user_pct'], team_df['avg_hours_atc'])
print(f"Correlation: slow_user_pct vs avg_hours_atc: r={corr2:.3f}, p={p_val2:.4f}")

corr3, p_val3 = stats.pearsonr(team_df['slow_user_pct'], team_df['avg_project_health'])
print(f"Correlation: slow_user_pct vs avg_project_health: r={corr3:.3f}, p={p_val3:.4f}")

# Visualize
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

axes[0,0].scatter(team_df['slow_user_pct'], team_df['completion_rate'], alpha=0.7)
axes[0,0].set_xlabel('Slow User % in Team')
axes[0,0].set_ylabel('Task Completion Rate (%)')
axes[0,0].set_title(f'Team Completion Rate vs Slow User % (r={corr:.3f})')
# Add regression line
m, b = np.polyfit(team_df['slow_user_pct'], team_df['completion_rate'], 1)
axes[0,0].plot(team_df['slow_user_pct'], m*team_df['slow_user_pct']+b, 'r--', alpha=0.5)

axes[0,1].scatter(team_df['slow_user_pct'], team_df['avg_hours_atc'], alpha=0.7)
axes[0,1].set_xlabel('Slow User % in Team')
axes[0,1].set_ylabel('Avg Hours to Completion')
axes[0,1].set_title(f'Avg Hours vs Slow User % (r={corr2:.3f})')
m2, b2 = np.polyfit(team_df['slow_user_pct'], team_df['avg_hours_atc'], 1)
axes[0,1].plot(team_df['slow_user_pct'], m2*team_df['slow_user_pct']+b2, 'r--', alpha=0.5)

axes[1,0].scatter(team_df['avg_complexity'], team_df['completion_rate'], alpha=0.7, c=team_df['slow_user_pct'], cmap='coolwarm')
axes[1,0].set_xlabel('Avg Task Complexity')
axes[1,0].set_ylabel('Task Completion Rate (%)')
axes[1,0].set_title('Completion Rate vs Complexity (color=Slow User %)')
cbar = plt.colorbar(axes[1,0].collections[0], ax=axes[1,0])
cbar.set_label('Slow User %')

axes[1,1].scatter(team_df['avg_project_health'], team_df['completion_rate'], alpha=0.7, c=team_df['slow_user_pct'], cmap='coolwarm')
axes[1,1].set_xlabel('Avg Project Health Score')
axes[1,1].set_ylabel('Task Completion Rate (%)')
axes[1,1].set_title('Completion Rate vs Project Health (color=Slow User %)')
cbar2 = plt.colorbar(axes[1,1].collections[0], ax=axes[1,1])
cbar2.set_label('Slow User %')

plt.tight_layout()
plt.savefig('/work/team_analysis.png', dpi=100)
print("Saved team_analysis.png")

# Identify underperforming teams
underperforming = team_df[team_df['completion_rate'] < 30].copy()
print(f"\nUnderperforming teams (completion_rate < 30%): {len(underperforming)}")
print(underperforming[['team_id', 'total_tasks', 'completion_rate', 'avg_project_health', 'avg_hours_atc', 'slow_user_pct']].to_string())

# Top performing teams
top_teams = team_df[team_df['completion_rate'] > 45].copy()
print(f"\nTop performing teams (completion_rate > 45%): {len(top_teams)}")
print(top_teams[['team_id', 'total_tasks', 'completion_rate', 'avg_project_health', 'avg_hours_atc', 'slow_user_pct']].to_string())