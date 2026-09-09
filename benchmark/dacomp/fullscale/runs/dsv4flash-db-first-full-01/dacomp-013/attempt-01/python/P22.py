import pandas as pd
import numpy as np

df = pd.read_csv('/work/final_classification.csv')

# Additional stats for report
print("=== OVERALL ===")
print(f"Total Task Owners: {len(df)}")
print(f"Task Types: {df['task_type'].value_counts().to_dict()}")

print("\n=== CLASSIFICATION DETAILS ===")
for cls in ['Excellent','Good','Needs Improvement']:
    sub = df[df['classification']==cls]
    print(f"\n--- {cls} (n={len(sub)}) ---")
    print(f"  By type: {sub['task_type'].value_counts().to_dict()}")
    print(f"  Avg total tasks: {sub['total_tasks'].mean():.2f}")
    print(f"  Avg completed tasks: {sub['completed_tasks'].mean():.2f}")
    print(f"  Avg completion rate: {sub['completion_rate'].mean():.3f}")
    print(f"  Avg on-time rate: {sub['on_time_rate'].mean():.3f}")
    print(f"  Avg quality (0-1): {sub['quality_norm'].mean():.3f}")
    print(f"  Avg priority-weighted completion: {sub['priority_weighted_completion'].mean():.3f}")
    print(f"  Avg hours efficiency: {sub['hours_efficiency'].mean():.3f}")
    print(f"  Avg rework avoidance: {sub['rework_avoidance'].mean():.3f}")
    print(f"  HP completion rate: {sub['hp_completed'].sum()}/{sub['hp_total'].sum()} = {sub['hp_completed'].sum()/sub['hp_total'].sum():.3f}")

print("\n=== COMPOSITE RANGES ===")
for cls in ['Excellent','Good','Needs Improvement']:
    sub = df[df['classification']==cls]
    print(f"  {cls}: [{sub['composite'].min():.4f}, {sub['composite'].max():.4f}]")

# Check how many owners are near boundary
print("\n=== BOUNDARY CHECK ===")
print(f"Excellent min composite: {df[df['classification']=='Excellent']['composite'].min():.4f}")
print(f"Good max composite: {df[df['classification']=='Good']['composite'].max():.4f}")
print(f"Good min composite: {df[df['classification']=='Good']['composite'].min():.4f}")
print(f"Needs max composite: {df[df['classification']=='Needs Improvement']['composite'].max():.4f}")

# Distinct count of owners per type who have zero completed tasks
print("\n=== ZERO COMPLETED OWNERS BY TYPE ===")
print(df[df['completed_tasks']==0].groupby('task_type').size().to_dict())

# Check correlation between avg difficulty and composite within type
print("\n=== CORR(avg_diff, composite) BY TYPE ===")
# We need avg_diff per owner - not in this df. Let me check.
# Actually, let me compute from the original full metrics
print("(avg_diff not in final df, skip)")