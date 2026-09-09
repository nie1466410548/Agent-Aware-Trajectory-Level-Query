import pandas as pd
import numpy as np

df = pd.read_csv('/work/owner_metrics.csv')
n = len(df)
print(f"Total owners: {n}")

# Sort by composite descending
df_sorted = df.sort_values('composite', ascending=False).reset_index(drop=True)

# Assign labels: top 20% Excellent, next 70% Good, bottom 10% Needs Improvement
n_excellent = int(round(n * 0.20))
n_needs = int(round(n * 0.10))
n_good = n - n_excellent - n_needs
print(f"Target: Excellent={n_excellent} ({n_excellent/n*100:.1f}%), Good={n_good} ({n_good/n*100:.1f}%), Needs Improvement={n_needs} ({n_needs/n*100:.1f}%)")

df_sorted['classification'] = 'Good'
df_sorted.loc[:n_excellent-1, 'classification'] = 'Excellent'
df_sorted.loc[n - n_needs:, 'classification'] = 'Needs Improvement'

# Adjust for exact split if needed
print(df_sorted['classification'].value_counts())

# Check distribution by type within each class
print("\nClassification by Task Type:")
print(pd.crosstab(df_sorted['task_type'], df_sorted['classification']))

# Check characteristics of each class
class_means = df_sorted.groupby('classification')[['completion_rate','on_time_rate','quality_norm','priority_weighted_completion','hours_efficiency','rework_avoidance','composite']].mean()
print("\nClass means:")
print(class_means)

# Also compute high-priority completion rate
df_sorted['hp_completion_rate'] = df_sorted['hp_completed'] / df_sorted['hp_total'].replace(0, np.nan)
print("\nHigh-priority completion rate by class:")
print(df_sorted.groupby('classification')['hp_completion_rate'].mean())

# Save final results
df_sorted.to_csv('/work/owner_classification.csv', index=False)
print("\nSaved classification results.")