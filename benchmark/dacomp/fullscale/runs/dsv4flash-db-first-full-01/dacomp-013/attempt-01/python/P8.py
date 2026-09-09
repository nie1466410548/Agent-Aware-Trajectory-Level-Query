import pandas as pd
import numpy as np

df = pd.read_csv('/work/owner_classification_v2.csv')

# Examine all owners at composite 0.1133 boundary
bd = df[abs(df['composite']-0.1133)<0.0002][['Task Owner','task_type','total_tasks','completed_tasks','composite','classification']]
print("Boundary (composite ~0.1133) rows:")
print(bd.sort_values(['classification','total_tasks'], ascending=[True,False]).to_string())

# Also check 0.158 group
g = df[abs(df['composite']-0.1581)<0.0002]
print("\n0.158 group count:", len(g), "classifications:", g['classification'].value_counts().to_dict())