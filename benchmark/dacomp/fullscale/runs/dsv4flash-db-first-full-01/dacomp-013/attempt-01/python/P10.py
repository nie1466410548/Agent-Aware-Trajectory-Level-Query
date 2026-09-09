import pandas as pd
import numpy as np

df = pd.read_csv('/work/owner_classification_v3.csv')

# Summary stats by class
class_stats = df.groupby('classification').agg({
    'completion_rate': ['mean','std','min','max'],
    'on_time_rate': ['mean','std','min','max'],
    'quality_norm': ['mean','std'],
    'priority_weighted_completion': ['mean','std'],
    'hours_efficiency': ['mean','std'],
    'rework_avoidance': ['mean','std'],
    'composite': ['mean','std','min','max'],
    'total_tasks': ['mean','sum'],
    'completed_tasks': ['mean','sum'],
    'hp_completed': ['sum'],
    'hp_total': ['sum'],
})
print("Class summary:")
print(class_stats.round(4))

# Show top 10 Excellent
print("\nTop 10 Excellent owners:")
ex = df[df['classification']=='Excellent'].sort_values('composite', ascending=False)
print(ex[['Task Owner','task_type','total_tasks','completed_tasks','completion_rate','on_time_rate','quality_norm','composite','avg_diff']].head(10).to_string())

# Show bottom 10 Good (near boundary)
print("\nBottom 10 Good owners:")
gd = df[df['classification']=='Good'].sort_values('composite', ascending=True)
print(gd[['Task Owner','task_type','total_tasks','completed_tasks','completion_rate','composite']].head(10).to_string())

# Show all Needs Improvement
print("\nAll Needs Improvement owners:")
ni = df[df['classification']=='Needs Improvement'].sort_values('composite', ascending=True)
print(ni[['Task Owner','task_type','total_tasks','completed_tasks','completion_rate','composite']].to_string())