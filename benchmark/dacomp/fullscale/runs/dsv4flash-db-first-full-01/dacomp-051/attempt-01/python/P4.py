import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

result = db.query("""
SELECT t.*,
  CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END AS cohort
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE t.is_valid_record=1
""")
df = db.frame(result)

# Categorical comparisons
fig, axes = plt.subplots(2, 3, figsize=(16, 10))

for i, col in enumerate(['current_lifecycle_stage', 'activity_level', 'anomaly_patterns', 'success_patterns', 'relative_performance_vs_project', 'task_status_category']):
    ax = axes[i//3, i%3]
    # normalize to percentages
    ct = pd.crosstab(df['cohort'], df[col], normalize='index')*100
    ct.T.plot(kind='bar', ax=ax, alpha=0.7)
    ax.set_title(f'{col} (by cohort, %)')
    ax.set_ylabel('%')
    ax.set_xlabel('')
    ax.tick_params(axis='x', rotation=45)
    ax.legend(title='Cohort')

plt.tight_layout()
plt.savefig('/work/cohort_categorical.png', dpi=100)
print("Saved cohort_categorical.png")

# Chi-square tests for each categorical
for col in ['current_lifecycle_stage', 'activity_level', 'anomaly_patterns', 'success_patterns', 'relative_performance_vs_project', 'task_status_category']:
    ct = pd.crosstab(df['cohort'], df[col])
    chi2, p, dof, _ = stats.chi2_contingency(ct)
    print(f"{col}: Chi2={chi2:.2f}, p={p:.4f}")

# Key numeric feature comparison (t-test)
print("\n=== Numeric feature comparisons (Welch t-test) ===")
num_cols = ['health_score', 'response_time_days', 'delay_days', 'activity_score', 'hours_to_assignment',
            'hours_assigned_to_completion', 'total_lifecycle_hours', 'total_story_events', 'unique_action_types',
            'days_with_activity', 'avg_daily_activity_rate', 'lifecycle_health_score']
for col in num_cols:
    slow = df[df['cohort']=='SLOW'][col].dropna()
    fast = df[df['cohort']=='FAST'][col].dropna()
    t_stat, p = stats.ttest_ind(slow, fast, equal_var=False)
    print(f"{col}: SLOW={slow.mean():.2f} vs FAST={fast.mean():.2f} | t={t_stat:.2f}, p={p:.4f}")

# Focus: comparison of delay metrics on completed tasks
comp = df[df['is_completed']==1]
print("\n=== Completed tasks only: delay_days ===")
print(comp.groupby('cohort')['delay_days'].agg(['mean', 'median', 'count']))

# Check task status categories
print("\n=== Task status category distribution ===")
print(pd.crosstab(df['cohort'], df['task_status_category'], normalize='index')*100)