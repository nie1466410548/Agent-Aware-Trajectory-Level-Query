import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats

result = db.query("""
SELECT t.*,
  CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END AS cohort
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE t.is_valid_record=1
""")
df = db.frame(result)

# Simple linear regression for each predictor vs log(ATC)
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

dfr = df[df['hours_assigned_to_completion'].notna() & (df['hours_assigned_to_completion']>0)].copy()
dfr['log_atc'] = np.log(dfr['hours_assigned_to_completion'])
dfr['is_slow'] = (dfr['cohort']=='SLOW').astype(int)

predictors = ['is_slow', 'complexity_score', 'urgency_score', 'project_health_score',
              'hours_to_assignment', 'avg_daily_activity_rate', 'unique_action_types', 'total_story_events']
dfr = dfr[predictors + ['log_atc']].dropna()
X = dfr[predictors].values
y = dfr['log_atc'].values

# Standardize
scaler = StandardScaler()
Xs = scaler.fit_transform(X)
lr = LinearRegression().fit(Xs, y)
print("=== Standardized regression coefficients (importance) ===")
for name, coef in zip(predictors, lr.coef_):
    print(f"  {name}: {coef:+.4f}")
print(f"R² = {lr.score(Xs, y):.4f}")

# Feature gap analysis completed
print("\n=== Feature gap SLOW vs FAST (Cohen's d) ===")
features = ['complexity_score', 'urgency_score', 'project_health_score', 'activity_score',
            'hours_to_assignment', 'hours_assigned_to_completion', 'total_lifecycle_hours',
            'total_story_events', 'unique_action_types', 'days_with_activity',
            'avg_daily_activity_rate', 'lifecycle_health_score', 'delay_days', 'response_time_days']
for f in features:
    slow = df[df['cohort']=='SLOW'][f].dropna()
    fast = df[df['cohort']=='FAST'][f].dropna()
    pooled_std = np.sqrt((slow.std()**2 + fast.std()**2)/2)
    cohen_d = (slow.mean()-fast.mean())/pooled_std if pooled_std>0 else np.nan
    print(f"{f}: diff={slow.mean()-fast.mean():+.3f}, d={cohen_d:+.3f}")

# Compare completed vs non-completed for slow cohort
slow_df = df[df['cohort']=='SLOW']
comp = slow_df[slow_df['is_completed']==1]
open_ = slow_df[slow_df['is_completed']==0]
print("\n=== SLOW cohort: Completed vs Open feature comparison ===")
for f in ['complexity_score', 'urgency_score', 'project_health_score', 'avg_daily_activity_rate', 
          'lifecycle_health_score', 'total_story_events', 'hours_assigned_to_completion']:
    c = comp[f].dropna()
    o = open_[f].dropna()
    if len(c)>0 and len(o)>0:
        t, p = stats.ttest_ind(c, o, equal_var=False)
        print(f"{f}: completed={c.mean():.2f}, open={o.mean():.2f}, p={p:.4f}")

# Collaboration: high_collaboration pattern effect
print("\n=== High-collaboration tasks: ATC hours ===")
collab = df[df['success_patterns']=='high_collaboration']
noncollab = df[df['success_patterns']!='high_collaboration']
print(f"High-collaboration: n={len(collab)}, mean ATC={collab['hours_assigned_to_completion'].mean():.1f}h")
print(f"Other: n={len(noncollab)}, mean ATC={noncollab['hours_assigned_to_completion'].mean():.1f}h")

# Completion rate by success pattern
print("\nCompletion rate by success_patterns:")
sp = df.groupby('success_patterns').agg(n=('task_id','count'), comp_rate=('is_completed','mean'))
sp['comp_rate'] = sp['comp_rate']*100
print(sp.sort_values('comp_rate', ascending=False).to_string())

# Avg health by completion
print("\n=== Project health by completion status ===")
print(df.groupby('is_completed')['project_health_score'].agg(['mean','median','count']))

# Activity level vs completion rate
print("\n=== Activity level vs completion rate ===")
al = df.groupby('activity_level').agg(n=('task_id','count'), comp_rate=('is_completed','mean'))
al['comp_rate'] = al['comp_rate']*100
print(al.sort_values('comp_rate', ascending=False).to_string())

# Final visualization: key drivers
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Boxplot: avg_daily_activity_rate by cohort
df.boxplot(column='avg_daily_activity_rate', by='cohort', ax=axes[0])
axes[0].set_title('Avg Daily Activity Rate by Cohort')
axes[0].set_ylabel('Activity Rate')

# Boxplot: unique_action_types by cohort
df.boxplot(column='unique_action_types', by='cohort', ax=axes[1])
axes[1].set_title('Unique Action Types by Cohort')
axes[1].set_ylabel('Action Types')

plt.suptitle('')
plt.tight_layout()
plt.savefig('/work/key_drivers.png', dpi=100)
print("Saved key_drivers.png")