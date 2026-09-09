import pandas as pd
import numpy as np

df = pd.read_csv('/work/final_classification.csv')

print("Needs Improvement completed_tasks distribution:")
ni = df[df['classification']=='Needs Improvement']
print(ni['completed_tasks'].value_counts().sort_index())
print("\nNeeds Improvement total_tasks distribution:")
print(ni['total_tasks'].value_counts().sort_index())

print("\nSample of Needs Improvement owners:")
print(ni[['Task Owner','task_type','total_tasks','completed_tasks','completion_rate','on_time_rate','priority_weighted_completion','composite']].sort_values('composite').head(15).to_string())

print("\nGood with 0 completed:", df[(df['classification']=='Good')&(df['completed_tasks']==0)].shape[0])
print("Needs with 0 completed:", df[(df['classification']=='Needs Improvement')&(df['completed_tasks']==0)].shape[0])
print("Needs with >=1 completed:", df[(df['classification']=='Needs Improvement')&(df['completed_tasks']>=1)].shape[0])