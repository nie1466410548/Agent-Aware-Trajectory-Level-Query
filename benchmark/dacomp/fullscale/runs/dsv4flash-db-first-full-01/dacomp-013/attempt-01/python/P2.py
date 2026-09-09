
import pandas as pd
import numpy as np

# Re-fetch from results if not already in scope (db.frame returned df)
# Fill missing sub-metrics with 0 (no completed output -> worst standing)
metrics = ['completion_rate','on_time_rate','quality_norm','priority_weighted_completion','hours_efficiency','rework_avoidance']
for m in metrics:
    df[m] = df[m].fillna(0.0)

# Within-task-type percentile ranks (0..1), higher = better
def pct_rank(group):
    return group.rank(pct=True)

for m in metrics:
    df['p_' + m] = df.groupby('task_type')[m].transform(lambda s: s.rank(pct=True))

# Weighted composite (weights sum to 1.0)
W = {
    'p_completion_rate': 0.20,
    'p_on_time_rate': 0.20,
    'p_quality_norm': 0.15,
    'p_priority_weighted_completion': 0.20,
    'p_hours_efficiency': 0.15,
    'p_rework_avoidance': 0.10,
}
df['composite'] = sum(df[k] * w for k, w in W.items())

print(df[['Task Owner','task_type','total_tasks','completed_tasks','composite']].describe())

# Check type balance of composite
print("\nComposite by type:")
print(df.groupby('task_type')['composite'].agg(['count','mean','std']))
