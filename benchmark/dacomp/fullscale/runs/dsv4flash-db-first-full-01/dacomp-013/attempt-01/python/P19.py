import pandas as pd
import numpy as np

df = pd.read_csv('/work/owner_full_metrics.csv')

# Apply K=10 shrinkage plan
K = 10.0
metric_defs = {
    'completion_rate': ('total_tasks', None),
    'on_time_rate': ('timed_completed', 0.0),
    'quality_norm': ('scored_completed', 0.0),
    'priority_weighted_completion': ('total_tasks', None),
    'hours_efficiency': ('eff_completed', 0.0),
    'rework_avoidance': ('rework_completed', 0.0),
}
type_means = df.groupby('task_type')[list(metric_defs.keys())].transform('mean')
for m, (ncol, fill) in metric_defs.items():
    raw = df[m].fillna(0.0)
    n = df[ncol]
    prior = type_means[m]
    df['shrunk_' + m] = (n * raw + K * prior) / (n + K)

metrics = ['completion_rate','on_time_rate','quality_norm','priority_weighted_completion','hours_efficiency','rework_avoidance']
for m in metrics:
    df['p_' + m] = df.groupby('task_type')['shrunk_' + m].transform(lambda s: s.rank(pct=True))

W = {'p_completion_rate':0.20,'p_on_time_rate':0.15,'p_quality_norm':0.15,
     'p_priority_weighted_completion':0.20,'p_hours_efficiency':0.15,'p_rework_avoidance':0.15}
df['composite'] = sum(df[k]*w for k,w in W.items())

ds = df.sort_values(['composite','total_tasks','completed_tasks'], ascending=[False, True, False]).reset_index(drop=True)
n = len(ds)
n_ex = int(round(n*0.20)); n_ni = int(round(n*0.10)); n_gd = n - n_ex - n_ni
ds['classification'] = 'Good'
ds.loc[:n_ex-1,'classification'] = 'Excellent'
ds.loc[n-n_ni:,'classification'] = 'Needs Improvement'

print("Counts:", ds['classification'].value_counts().to_dict())
print("\nBy Type:")
print(pd.crosstab(ds['task_type'], ds['classification']))

print("\nClass means (raw metrics):")
print(ds.groupby('classification')[['completion_rate','on_time_rate','quality_norm','priority_weighted_completion','hours_efficiency','rework_avoidance','composite']].mean().round(3))

print("\nHigh-priority completion rate by class:")
print(ds.groupby('classification').apply(lambda g: g['hp_completed'].sum()/g['hp_total'].sum()).round(3))

print("\nClass composite ranges:")
for cls in ['Excellent','Good','Needs Improvement']:
    sub = ds[ds['classification']==cls]
    print(f"  {cls}: [{sub['composite'].min():.4f}, {sub['composite'].max():.4f}] n={len(sub)} completed_mean={sub['completed_tasks'].mean():.2f}")

# Save final
ds.to_csv('/work/final_classification.csv', index=False)
print("\nSaved final_classification.csv")