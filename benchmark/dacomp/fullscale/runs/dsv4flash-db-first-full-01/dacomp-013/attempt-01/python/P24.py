import pandas as pd
import numpy as np

# Get avg_diff per owner for the report
sql = """
SELECT "Task Owner", ROUND(AVG("Task Difficulty Coefficient"),3) AS avg_diff
FROM sheet1 GROUP BY "Task Owner"
"""
diff_df = db.frame(db.query(sql))

df = pd.read_csv('/work/final_classification.csv')
df = df.merge(diff_df, on='Task Owner', how='left')

# Check diff by class
print("Avg difficulty by class:")
print(df.groupby('classification')['avg_diff'].mean().round(3))

# Check diff by type
print("\nAvg difficulty by type:")
print(df.groupby('task_type')['avg_diff'].mean().round(3))

# Correlation between avg_diff and composite within type
print("\nCorr(avg_diff, composite) by type:")
for t in ['Design','Development','Document','Testing']:
    sub = df[df['task_type']==t]
    c = sub['avg_diff'].corr(sub['composite'])
    print(f"  {t}: {c:.3f}")

# Summary table for report
print("\n\n=== REPORT TABLE DATA ===")
summary = df.groupby('classification').agg({
    'Task Owner': 'count',
    'total_tasks': 'mean',
    'completed_tasks': 'mean',
    'completion_rate': 'mean',
    'on_time_rate': 'mean',
    'quality_norm': 'mean',
    'priority_weighted_completion': 'mean',
    'hours_efficiency': 'mean',
    'rework_avoidance': 'mean',
    'composite': 'mean',
    'avg_diff': 'mean',
}).round(3)
summary.columns = ['Count','Avg Total Tasks','Avg Completed','Completion Rate','On-Time Rate','Quality (0-1)','Priority-Weighted Completion','Hours Efficiency','Rework Avoidance','Composite','Avg Difficulty']
print(summary.to_string())

# By type
print("\n\n=== BY TYPE TABLE ===")
type_summary = df.groupby('task_type').agg({
    'Task Owner': 'count',
    'total_tasks': 'mean',
    'completed_tasks': 'mean',
    'completion_rate': 'mean',
    'avg_diff': 'mean',
}).round(3)
print(type_summary.to_string())