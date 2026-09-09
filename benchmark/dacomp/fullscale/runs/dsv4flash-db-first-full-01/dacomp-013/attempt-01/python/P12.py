import pandas as pd
import numpy as np

df = pd.read_csv('/work/owner_classification_v3.csv')

# Excellent group: completed task distribution
ex = df[df['classification']=='Excellent']
print("Excellent: completed_tasks distribution")
print(ex['completed_tasks'].value_counts().sort_index())

print("\nExcellent: total_tasks distribution")
print(ex['total_tasks'].value_counts().sort_index())

print("\nExcellent: task_type distribution")
print(ex['task_type'].value_counts())

# Good group: how many with 0 completed?
gd = df[df['classification']=='Good']
print(f"\nGood with 0 completed: {gd[gd['completed_tasks']==0].shape[0]} out of {gd.shape[0]}")
print(f"Good with 0 completed by type:")
print(gd[gd['completed_tasks']==0].groupby('task_type')['Task Owner'].count().to_dict())

# Needs Improvement: all have 0 completed, confirmed
ni = df[df['classification']=='Needs Improvement']
print(f"\nNeeds Improvement with >0 completed: {ni[ni['completed_tasks']>0].shape[0]}")

# Check overall distribution of completed tasks by type
print("\n\nCompleted tasks per owner by type:")
print(df.groupby('task_type')['completed_tasks'].describe().round(1))

# Check HP completion rate details
print("\nHP completion rate by region:")
print(df.groupby('classification')['hp_completed'].sum())
print(df.groupby('classification')['hp_total'].sum())
print("HP completion rate:")
print((df.groupby('classification')['hp_completed'].sum() / df.groupby('classification')['hp_total'].sum()).round(3))

# Count of 'on time' tasks per class
print("\nOn-time rate mean by class:")
print(df.groupby('classification')['on_time_rate'].mean().round(3))

# Quality mean by class
print("\nQuality mean by class:")
print(df.groupby('classification')['quality_norm'].mean().round(3))

# Efficiency mean by class  
print("\nHours efficiency mean by class:")
print(df.groupby('classification')['hours_efficiency'].mean().round(3))