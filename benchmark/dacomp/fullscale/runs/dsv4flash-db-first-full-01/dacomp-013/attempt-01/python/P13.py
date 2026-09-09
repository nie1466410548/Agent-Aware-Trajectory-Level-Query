import pandas as pd
import numpy as np

df = pd.read_csv('/work/owner_classification_v3.csv')

# High-volume owners (>=5 total tasks): classification breakdown
hv = df[df['total_tasks']>=5]
print("Owners with >=5 total tasks: ", len(hv))
print(hv[['Task Owner','task_type','total_tasks','completed_tasks','completion_rate','on_time_rate','composite','classification']].sort_values('composite',ascending=False).to_string())

# Owners with >=3 completed tasks
mc = df[df['completed_tasks']>=3]
print("\nOwners with >=3 completed tasks:", len(mc))
print("Their classification:")
print(mc['classification'].value_counts())