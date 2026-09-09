import pandas as pd
import numpy as np

df = pd.read_csv('/work/owner_classification.csv')

# Check owners with 0 completed tasks - how many and their classification
print("Owners with 0 completed tasks:")
print(df[df['completed_tasks']==0][['Task Owner','task_type','total_tasks','completion_rate','composite','classification']])

# Check: are there any Needs Improvement with >0 completed tasks?
print("\nNeeds Improvement with >0 completed tasks:")
print(df[(df['classification']=='Needs Improvement') & (df['completed_tasks']>0)][['Task Owner','task_type','completed_tasks','total_tasks','composite']])

# Check boundary between Excellent and Good
excellent_last = df[df['classification']=='Excellent']['composite'].min()
good_first = df[df['classification']=='Good']['composite'].max()
print(f"\nExcellent lowest composite: {excellent_last:.4f}")
print(f"Good highest composite: {good_first:.4f}")

# Check boundary between Good and Needs Improvement
good_last = df[df['classification']=='Good']['composite'].min()
needs_first = df[df['classification']=='Needs Improvement']['composite'].max()
print(f"\nGood lowest composite: {good_last:.4f}")
print(f"Needs Improvement highest composite: {needs_first:.4f}")

# Check 0 completed by type
print("\n0 completed owners by type:")
print(df[df['completed_tasks']==0].groupby('task_type').size())

# Check all 0-completed owners - are they all Needs Improvement?
print("\nClassification of 0-completed owners:")
print(df[df['completed_tasks']==0]['classification'].value_counts())