import pandas as pd
import numpy as np

df = pd.read_csv('/work/owner_metrics_v2.csv')

# Define raw metrics and their sample-size columns
metric_defs = {
    'completion_rate': ('total_tasks', None),            # n = total_tasks
    'on_time_rate': ('timed_completed', 0.0),            # n = timed_completed
    'quality_norm': ('scored_completed', 0.0),
    'priority_weighted_completion': ('total_tasks', None),
    'hours_efficiency': ('eff_completed', 0.0),
    'rework_avoidance': ('rework_completed', 0.0),
}

# Type means of raw metrics (for shrinkage prior)
type_means = df.groupby('task_type')[list(metric_defs.keys())].transform('mean')

K = 5.0  # credibility constant
for m, (ncol, fill) in metric_defs.items():
    raw = df[m].fillna(0.0)
    n = df[ncol]
    prior = type_means[m]
    df['shrunk_' + m] = (n * raw + K * prior) / (n + K)

# Within-type percentile ranks of shrunk metrics
metrics = ['completion_rate','on_time_rate','quality_norm','priority_weighted_completion','hours_efficiency','rework_avoidance']
for m in metrics:
    df['p_' + m] = df.groupby('task_type')['shrunk_' + m].transform(lambda s: s.rank(pct=True))

# Composite weights
W = {'p_completion_rate':0.20,'p_on_time_rate':0.15,'p_quality_norm':0.15,
     'p_priority_weighted_completion':0.20,'p_hours_efficiency':0.15,'p_rework_avoidance':0.15}
df['composite'] = sum(df[k]*w for k,w in W.items())

# Classification with tie-breaker
df_sorted = df.sort_values(['composite','total_tasks','completed_tasks'], ascending=[False, True, False]).reset_index(drop=True)
n = len(df_sorted)
n_ex = int(round(n*0.20)); n_ni = int(round(n*0.10)); n_gd = n - n_ex - n_ni
df_sorted['classification'] = 'Good'
df_sorted.loc[:n_ex-1,'classification'] = 'Excellent'
df_sorted.loc[n-n_ni:,'classification'] = 'Needs Improvement'

print("Classification counts:", df_sorted['classification'].value_counts().to_dict())
print("\nBy type:")
print(pd.crosstab(df_sorted['task_type'], df_sorted['classification']))

# Check Excellent completed_tasks distribution now
ex = df_sorted[df_sorted['classification']=='Excellent']
print("\nExcellent completed_tasks distribution:")
print(ex['completed_tasks'].value_counts().sort_index())
print("\nExcellent total_tasks distribution:")
print(ex['total_tasks'].value_counts().sort_index())

# High-volume owners now
hv = df_sorted[df_sorted['total_tasks']>=5]
print("\nHigh-volume owners classification:")
print(hv['classification'].value_counts())

# Show top excellent
print("\nTop 10 Excellent:")
print(ex.sort_values('composite',ascending=False)[['Task Owner','task_type','total_tasks','completed_tasks','completion_rate','composite']].head(10).to_string())

# Boundary
print(f"\nExcellent min composite: {df_sorted[df_sorted['classification']=='Excellent']['composite'].min():.4f}")
print(f"Good max composite: {df_sorted[df_sorted['classification']=='Good']['composite'].max():.4f}")
print(f"Needs max composite: {df_sorted[df_sorted['classification']=='Needs Improvement']['composite'].max():.4f}")

df_sorted.to_csv('/work/owner_classification_final.csv', index=False)
print("\nSaved final.")