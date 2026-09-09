import pandas as pd
import numpy as np

# Recompute with principled tie-breaker: within equal composite, more assigned-but-incomplete workload -> worse (lower)
df = pd.read_csv('/work/owner_metrics.csv')
for m in ['completion_rate','on_time_rate','quality_norm','priority_weighted_completion','hours_efficiency','rework_avoidance']:
    df[m] = df[m].fillna(0.0)
metrics = ['completion_rate','on_time_rate','quality_norm','priority_weighted_completion','hours_efficiency','rework_avoidance']
for m in metrics:
    df['p_' + m] = df.groupby('task_type')[m].transform(lambda s: s.rank(pct=True))
W = {'p_completion_rate':0.20,'p_on_time_rate':0.20,'p_quality_norm':0.15,
     'p_priority_weighted_completion':0.20,'p_hours_efficiency':0.15,'p_rework_avoidance':0.10}
df['composite'] = sum(df[k]*w for k,w in W.items())

# Tie-break: composite desc; then more tasks-without-completion = worse => total_tasks asc within tie
df_sorted = df.sort_values(['composite','total_tasks','completed_tasks'], ascending=[False, True, False]).reset_index(drop=True)

n = len(df_sorted)
n_ex = int(round(n*0.20)); n_ni = int(round(n*0.10)); n_gd = n - n_ex - n_ni
df_sorted['classification'] = 'Good'
df_sorted.loc[:n_ex-1,'classification'] = 'Excellent'
df_sorted.loc[n-n_ni:,'classification'] = 'Needs Improvement'

# Check boundary resolution
bd = df_sorted[(df_sorted['task_type']=='Testing') & (df_sorted['completed_tasks']==0)]
print("Testing 0-completed owners at boundary:")
print(bd[['Task Owner','total_tasks','composite','classification']].sort_values(['composite','total_tasks']).to_string())

# Correlation between avg_diff and completion_rate within each type
print("\nWithin-type corr(avg_diff, completion_rate):")
print(df.groupby('task_type')[['avg_diff','completion_rate']].corr().iloc[0::2,1].round(3).to_string())

print("\nCorr(avg_diff, on_time_rate):")
print(df[df['completed_tasks']>0].groupby('task_type')[['avg_diff','on_time_rate']].corr().iloc[0::2,1].round(3).to_string())

df_sorted.to_csv('/work/owner_classification_v3.csv', index=False)
print("\nSaved v3. Counts:", df_sorted['classification'].value_counts().to_dict())
