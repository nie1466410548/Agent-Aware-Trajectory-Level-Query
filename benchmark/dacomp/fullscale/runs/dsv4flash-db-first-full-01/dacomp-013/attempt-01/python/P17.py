import pandas as pd
import numpy as np

df = pd.read_csv('/work/class_K10.csv')

# Overall stats
print("=== FINAL CLASSIFICATION SUMMARY (K=10) ===")
print("Counts:", df['classification'].value_counts().to_dict())
print("\nBy Task Type:")
print(pd.crosstab(df['task_type'], df['classification']))

print("\nClass mean raw metrics:")
print(df.groupby('classification')[['completion_rate','on_time_rate','quality_norm','priority_weighted_completion','hours_efficiency','rework_avoidance','composite']].mean().round(3))

# High-priority stats per class
df['hp_completion_rate'] = df['hp_completed']/df['hp_total'].replace(0,np.nan)
print("\nHigh-priority completion rate by class:")
print(df.groupby('classification').apply(lambda g: g['hp_completed'].sum()/g['hp_total'].sum()).round(3))

# Boundary values
for cls in ['Excellent','Good','Needs Improvement']:
    sub = df[df['classification']==cls]
    print(f"\n{cls}: composite range [{sub['composite'].min():.4f}, {sub['composite'].max():.4f}], "
          f"completed_tasks mean {sub['completed_tasks'].mean():.2f}, total_tasks mean {sub['total_tasks'].mean():.2f}")

# Check boundaries clean
ex_min = df[df['classification']=='Excellent']['composite'].min()
gd_max = df[df['classification']=='Good']['composite'].max()
gd_min = df[df['classification']=='Good']['composite'].min()
ni_max = df[df['classification']=='Needs Improvement']['composite'].max()
print(f"\nBoundary Excellent|Good: {ex_min:.4f} vs {gd_max:.4f}")
print(f"Boundary Good|Needs: {gd_min:.4f} vs {ni_max:.4f}")

# Top Excellent
print("\nTop 12 Excellent:")
print(df[df['classification']=='Excellent'].sort_values('composite',ascending=False)[['Task Owner','task_type','total_tasks','completed_tasks','completion_rate','on_time_rate','quality_norm','composite']].head(12).to_string())

# Bottom Needs
print("\nBottom 12 Needs Improvement:")
print(df[df['classification']=='Needs Improvement'].sort_values('composite',ascending=True)[['Task Owner','task_type','total_tasks','completed_tasks','completion_rate','composite']].head(12).to_string())