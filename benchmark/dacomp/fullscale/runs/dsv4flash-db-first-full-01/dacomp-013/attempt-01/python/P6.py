import pandas as pd
import numpy as np

df = pd.read_csv('/work/owner_classification.csv')
df_sorted = df.sort_values(['composite','completed_tasks'], ascending=[False, True]).reset_index(drop=True)

# Examine owners near the Good/Needs boundary (composite <= 0.16)
print("Owners with composite <= 0.16 (bottom region):")
cols = ['Task Owner','task_type','total_tasks','completed_tasks','completion_rate','composite','classification']
print(df_sorted[df_sorted['composite']<=0.16][cols].to_string())

# How many at composite == 0.1133?
boundary_val = 0.1133
print("\nCount at composite 0.1133:", (df_sorted['composite']==boundary_val).sum())