import pandas as pd
import numpy as np

df = pd.read_csv('/work/owner_metrics.csv')

# Fill missing
for m in ['completion_rate','on_time_rate','quality_norm','priority_weighted_completion','hours_efficiency','rework_avoidance']:
    df[m] = df[m].fillna(0.0)

# Compute within-type percentile ranks
metrics = ['completion_rate','on_time_rate','quality_norm','priority_weighted_completion','hours_efficiency','rework_avoidance']
for m in metrics:
    df['p_' + m] = df.groupby('task_type')[m].transform(lambda s: s.rank(pct=True))

# Composite
W = {'p_completion_rate':0.20,'p_on_time_rate':0.20,'p_quality_norm':0.15,
     'p_priority_weighted_completion':0.20,'p_hours_efficiency':0.15,'p_rework_avoidance':0.10}
df['composite'] = sum(df[k]*w for k,w in W.items())

# Sort with tie-breaker: composite desc, then completed_tasks asc, then total_tasks desc
# After composite, owners with fewer completed AND more assigned tasks rank lower
df_sorted = df.sort_values(
    ['composite','completed_tasks','total_tasks'],
    ascending=[False, True, False]
).reset_index(drop=True)

n = len(df_sorted)
n_excellent = int(round(n * 0.20))
n_needs = int(round(n * 0.10))
n_good = n - n_excellent - n_needs

df_sorted['classification'] = 'Good'
df_sorted.loc[:n_excellent-1, 'classification'] = 'Excellent'
df_sorted.loc[n - n_needs:, 'classification'] = 'Needs Improvement'

print("Classification counts:")
print(df_sorted['classification'].value_counts())
print(f"\nBy type:")
print(pd.crosstab(df_sorted['task_type'], df_sorted['classification']))

# Verify boundary
print(f"\nExcellent lowest composite: {df_sorted[df_sorted['classification']=='Excellent']['composite'].min():.4f}")
print(f"Good highest composite: {df_sorted[df_sorted['classification']=='Good']['composite'].max():.4f}")
print(f"Good lowest composite: {df_sorted[df_sorted['classification']=='Good']['composite'].min():.4f}")
print(f"Needs highest composite: {df_sorted[df_sorted['classification']=='Needs Improvement']['composite'].max():.4f}")

# Check boundary rows
print("\nBoundary rows (Good/Needs):")
print(df_sorted.loc[n_good-5:n_good+5, ['Task Owner','task_type','total_tasks','completed_tasks','composite','classification']].to_string())

# Verify no 0-completed in Excellent
print("\nExcellent owners with 0 completed:")
print(df_sorted[(df_sorted['classification']=='Excellent') & (df_sorted['completed_tasks']==0)].shape[0])

# Check HP completion rate by class
df_sorted['hp_completion_rate'] = df_sorted['hp_completed'] / df_sorted['hp_total'].replace(0, np.nan)
print("\nHP completion rate by class:")
print(df_sorted.groupby('classification')['hp_completion_rate'].mean())

# Save
df_sorted.to_csv('/work/owner_classification_v2.csv', index=False)
print("\nSaved v2.")