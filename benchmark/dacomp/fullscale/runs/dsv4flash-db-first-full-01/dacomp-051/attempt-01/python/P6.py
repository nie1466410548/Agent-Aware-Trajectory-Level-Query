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

# Key driver analysis: what distinguishes slow-user tasks
print("=== Feature gap SLOW vs FAST (mean, effect size) ===")
features = ['complexity_score', 'urgency_score', 'project_health_score', 'activity_score',
            'hours_to_assignment', 'hours_assigned_to_completion', 'total_lifecycle_hours',
            'total_story_events', 'unique_action_types', 'days_with_activity',
            'avg_daily_activity_rate', 'lifecycle_health_score', 'delay_days', 'response_time_days']
for f in features:
    slow = df[df['cohort']=='SLOW'][f].dropna()
    fast = df[df['cohort']=='FAST'][f].dropna()
    pooled_std = np.sqrt((slow.std()**2 + fast.std()**2)/2)
    cohen_d = (slow.mean()-fast.mean())/pooled_std if pooled_std>0 else np.nan
    print(f"{f}: diff={slow.mean()-fast.mean():+.3f}, Cohen's d={cohen_d:+.3f}")

# Regression: log(hours_assigned_to_completion) on features
import statsmodels.api as sm
dfr = df[df['hours_assigned_to_completion'].notna() & (df['hours_assigned_to_completion']>0)].copy()
dfr['log_atc'] = np.log(dfr['hours_assigned_to_completion'])
dfr['is_slow'] = (dfr['cohort']=='SLOW').astype(int)
X = dfr[['is_slow', 'complexity_score', 'urgency_score', 'project_health_score',
         'hours_to_assignment', 'avg_daily_activity_rate', 'unique_action_types', 'total_story_events']].dropna()
y = dfr.loc[X.index, 'log_atc']
Xc = sm.add_constant(X)
model = sm.OLS(y, Xc).fit()
print("\n=== OLS regression on log(hours assigned->completion) ===")
print(model.summary().tables[1])

# Feature importance via standardized coefficients
from sklearn.preprocessing import StandardScaler
Xs = StandardScaler().fit_transform(X)
model2 = sm.OLS(y, sm.add_constant(Xs)).fit()
print("Standardized coefficients (importance):")
for name, coef, p in zip(X.columns, model2.params[1:], model2.pvalues[1:]):
    print(f"  {name}: {coef:+.3f} (p={p:.4f})")

# Completed vs open task comparison for slow cohort
slow_df = df[df['cohort']=='SLOW']
comp = slow_df[slow_df['is_completed']==1]
open_ = slow_df[slow_df['is_completed']==0]
print("\n=== SLOW cohort: Completed vs Open tasks ===")
for f in ['complexity_score', 'urgency_score', 'project_health_score', 'avg_daily_activity_rate', 'lifecycle_health_score', 'total_story_events']:
    if comp[f].notna().sum()>0 and open_[f].notna().sum()>0:
        t, p = stats.ttest_ind(comp[f].dropna(), open_[f].dropna(), equal_var=False)
        print(f"{f}: completed={comp[f].mean():.2f}, open={open_[f].mean():.2f}, p={p:.4f}")

# Collaboration: high_collaboration pattern effect
print("\n=== High-collaboration tasks: ATC hours ===")
collab = df[df['success_patterns']=='high_collaboration']
print(f"High-collaboration tasks: n={len(collab)}, mean ATC hours={collab['hours_assigned_to_completion'].mean():.1f}")
noncollab = df[df['success_patterns']!='high_collaboration']
print(f"Other tasks: n={len(noncollab)}, mean ATC hours={noncollab['hours_assigned_to_completion'].mean():.1f}")

# completion rate by success pattern
print("\nCompletion rate by success_patterns (top 5):")
sp = df.groupby('success_patterns').agg(n=('task_id','count'), comp_rate=('is_completed','mean'))
sp['comp_rate'] = sp['comp_rate']*100
print(sp.sort_values('comp_rate', ascending=False).head(6))

# Average health by completion
print("\n=== Project health vs completion ===")
print(df.groupby('is_completed')['project_health_score'].agg(['mean','median','count']))