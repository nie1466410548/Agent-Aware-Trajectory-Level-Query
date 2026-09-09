import pandas as pd
import numpy as np

df = pd.read_csv('/work/owner_metrics_v2.csv')

def run_plan(K, save_name):
    d = df.copy()
    metric_defs = {
        'completion_rate': ('total_tasks', None),
        'on_time_rate': ('timed_completed', 0.0),
        'quality_norm': ('scored_completed', 0.0),
        'priority_weighted_completion': ('total_tasks', None),
        'hours_efficiency': ('eff_completed', 0.0),
        'rework_avoidance': ('rework_completed', 0.0),
    }
    type_means = d.groupby('task_type')[list(metric_defs.keys())].transform('mean')
    for m, (ncol, fill) in metric_defs.items():
        raw = d[m].fillna(0.0)
        n = d[ncol]
        prior = type_means[m]
        d['shrunk_' + m] = (n * raw + K * prior) / (n + K)
    metrics = ['completion_rate','on_time_rate','quality_norm','priority_weighted_completion','hours_efficiency','rework_avoidance']
    for m in metrics:
        d['p_' + m] = d.groupby('task_type')['shrunk_' + m].transform(lambda s: s.rank(pct=True))
    W = {'p_completion_rate':0.20,'p_on_time_rate':0.15,'p_quality_norm':0.15,
         'p_priority_weighted_completion':0.20,'p_hours_efficiency':0.15,'p_rework_avoidance':0.15}
    d['composite'] = sum(d[k]*w for k,w in W.items())
    ds = d.sort_values(['composite','total_tasks','completed_tasks'], ascending=[False, True, False]).reset_index(drop=True)
    n = len(ds)
    n_ex = int(round(n*0.20)); n_ni = int(round(n*0.10)); n_gd = n - n_ex - n_ni
    ds['classification'] = 'Good'
    ds.loc[:n_ex-1,'classification'] = 'Excellent'
    ds.loc[n-n_ni:,'classification'] = 'Needs Improvement'
    ds.to_csv(save_name, index=False)
    return ds

for K in [5, 10, 15]:
    ds = run_plan(K, f'/work/class_K{K}.csv')
    ex = ds[ds['classification']=='Excellent']
    hv = ds[ds['total_tasks']>=5]
    print(f"K={K}: Excellent n={len(ex)}, 1-task in Excellent={ex[ex['total_tasks']==1].shape[0]}, "
          f"1-completed in Excellent={ex[ex['completed_tasks']==1].shape[0]}")
    print(f"   High-volume(>=5) Excellent: {hv[hv['classification']=='Excellent'].shape[0]}/{len(hv)}")
    print(f"   By type Excellent: {ex['task_type'].value_counts().to_dict()}")
    print(f"   By type Needs: {ds[ds['classification']=='Needs Improvement']['task_type'].value_counts().to_dict()}")
    print()