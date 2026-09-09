import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats

# Comprehensive summary figure
result = db.query("""
SELECT t.*,
  CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END AS cohort
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE t.is_valid_record=1
""")
df = db.frame(result)

fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# 1. Avg daily activity rate
df.boxplot(column='avg_daily_activity_rate', by='cohort', ax=axes[0,0])
axes[0,0].set_title('Avg Daily Activity Rate\n(p=0.0016, d=-0.168)')
axes[0,0].set_ylabel('Activity Rate')

# 2. Unique action types
df.boxplot(column='unique_action_types', by='cohort', ax=axes[0,1])
axes[0,1].set_title('Unique Action Types\n(p=0.0058, d=-0.151)')
axes[0,1].set_ylabel('Action Types')

# 3. Lifecycle health score
df.boxplot(column='lifecycle_health_score', by='cohort', ax=axes[0,2])
axes[0,2].set_title('Lifecycle Health Score\n(p=0.0223, d=-0.124)')
axes[0,2].set_ylabel('Health Score')

# 4. Task status category
ct = pd.crosstab(df['cohort'], df['task_status_category'], normalize='index')*100
ct.plot(kind='bar', ax=axes[1,0], alpha=0.7)
axes[1,0].set_title('Task Status Distribution')
axes[1,0].set_ylabel('% of Cohort')
axes[1,0].set_xlabel('')
axes[1,0].legend(title='Status')

# 5. Completion rate by activity level (slow cohort only)
slow = df[df['cohort']=='SLOW']
al = slow.groupby('activity_level').agg(n=('task_id','count'), comp_rate=('is_completed','mean'))
al['comp_rate'] = al['comp_rate']*100
al = al.sort_values('comp_rate', ascending=False)
axes[1,1].bar(al.index, al['comp_rate'], color='skyblue', alpha=0.7)
axes[1,1].set_title('SLOW Cohort: Completion Rate\nby Activity Level')
axes[1,1].set_ylabel('Completion Rate (%)')
axes[1,1].tick_params(axis='x', rotation=45)

# 6. Collaboration effect
collab_means = df.groupby(df['success_patterns']=='high_collaboration')['hours_assigned_to_completion'].mean()
axes[1,2].bar(['Non-Collaborative', 'High Collaboration'], collab_means.values, color=['coral', 'green'], alpha=0.7)
axes[1,2].set_title('High Collaboration Effect\non Completion Time')
axes[1,2].set_ylabel('Avg Hours to Completion')

plt.suptitle('Root Cause Analysis: Key Drivers of Delivery Inefficiency', fontsize=14)
plt.tight_layout()
plt.savefig('/work/root_causes.png', dpi=100)
print("Saved root_causes.png")

# Summary stats for report
print("=== KEY STATISTICS FOR REPORT ===")
print(f"Total users: 1000")
print(f"Users exceeding 1.5x avg: 191 (19.1%)")
print(f"Overall avg close time: 8.17 days")
print(f"Threshold: 12.25 days")
print(f"Slow cohort range: 12.25 - 35.40 days")
print(f"Slow cohort avg: {df[df['cohort']=='SLOW']['hours_assigned_to_completion'].mean():.1f} hours")
print(f"Fast cohort avg: {df[df['cohort']=='FAST']['hours_assigned_to_completion'].mean():.1f} hours")
print(f"Overall completion rate: 38.9%")
print(f"Worst team completion rate: 23.7%")
print(f"Best team completion rate: 55.4%")
print(f"High-collab ATC: {df[df['success_patterns']=='high_collaboration']['hours_assigned_to_completion'].mean():.1f}h")
print(f"Non-collab ATC: {df[df['success_patterns']!='high_collaboration']['hours_assigned_to_completion'].mean():.1f}h")

# Underperforming teams summary
result2 = db.query("""
SELECT team_id, COUNT(*) AS total_tasks,
SUM(CASE WHEN is_completed=1 THEN 1 ELSE 0 END) AS completed_tasks,
ROUND(100.0*SUM(CASE WHEN is_completed=1 THEN 1 ELSE 0 END)/COUNT(*),2) AS completion_rate,
ROUND(AVG(project_health_score),2) AS avg_project_health,
ROUND(AVG(hours_assigned_to_completion),1) AS avg_hours_atc
FROM asana__task_lifecycle_analysis
WHERE is_valid_record=1
GROUP BY team_id
HAVING total_tasks >= 50
ORDER BY completion_rate ASC
LIMIT 10
""")
team_df = db.frame(result2)
print("\n=== Bottom 10 teams (by completion rate, >=50 tasks) ===")
print(team_df.to_string())