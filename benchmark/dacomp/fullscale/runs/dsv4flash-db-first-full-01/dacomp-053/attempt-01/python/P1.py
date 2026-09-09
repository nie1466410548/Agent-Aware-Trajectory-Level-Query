
import pandas as pd
import numpy as np

res = db.query("""
SELECT overall_health_score, roi_efficiency_ratio, completion_percentage, quality_percentage,
       risk_percentage, efficiency_score, time_management_score, collaboration_score,
       complexity_factor, elapsed_days, planned_duration_days, unique_assignees,
       total_tasks, completion_rate_per_day
FROM asana__project_analytics
""")
df = db.frame(res)
df['elapsed_ratio'] = df['elapsed_days'] / df['planned_duration_days']
df['tasks_per_day'] = df['total_tasks'] / df['planned_duration_days']

cols = ['completion_percentage','quality_percentage','risk_percentage','efficiency_score',
        'time_management_score','collaboration_score','complexity_factor','elapsed_ratio',
        'unique_assignees','completion_rate_per_day']
corr = df[['roi_efficiency_ratio','overall_health_score'] + cols].corr()
print("Correlation with ROI:")
print(corr['roi_efficiency_ratio'].round(3).to_string())
print("\nCorrelation with Health Score:")
print(corr['overall_health_score'].round(3).to_string())
