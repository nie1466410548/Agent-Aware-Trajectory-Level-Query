
import pandas as pd
import numpy as np

sql = """
WITH t AS (
  SELECT
    "Task Owner", "Task Type", "Task Status", "Priority",
    CASE WHEN "Task Status" = 'Completed' THEN 1 ELSE 0 END AS completed,
    CASE WHEN "Task Status" = 'Completed' AND "Actual Completion Time" != '-'
              AND "Planned Deadline" != '-'
              AND julianday("Actual Completion Time") <= julianday("Planned Deadline")
         THEN 1 ELSE 0 END AS on_time,
    CASE WHEN "Task Status" = 'Completed' AND "Completion Quality Score" != '-'
         THEN CAST("Completion Quality Score" AS REAL) END AS quality,
    CASE WHEN "Task Status" = 'Completed' AND "Actual Work Hours" != '-'
              AND "Planned Work Hours" > 0
         THEN MIN(("Planned Work Hours" * 1.0) / CAST("Actual Work Hours" AS REAL), 1.5) END AS eff,
    CASE WHEN "Task Status" = 'Completed' AND "Rework Count" != '-'
         THEN CAST("Rework Count" AS INTEGER) END AS rework,
    "Task Difficulty Coefficient"
  FROM sheet1
)
SELECT
  "Task Owner",
  MAX("Task Type") AS task_type,
  COUNT(*) AS total_tasks,
  SUM(completed) AS completed_tasks,
  1.0*SUM(completed)/COUNT(*) AS completion_rate,
  1.0*SUM(on_time)/NULLIF(SUM(completed),0) AS on_time_rate,
  AVG(quality)/10.0 AS quality_norm,
  1.0*SUM(CASE WHEN "Priority"='Urgent' THEN 4 WHEN "Priority"='High' THEN 3
         WHEN "Priority"='Medium' THEN 2 WHEN "Priority"='Low' THEN 1 END * completed)
    /NULLIF(SUM(CASE WHEN "Priority"='Urgent' THEN 4 WHEN "Priority"='High' THEN 3
         WHEN "Priority"='Medium' THEN 2 WHEN "Priority"='Low' THEN 1 END),0) AS priority_weighted_completion,
  AVG(eff) AS hours_efficiency,
  AVG(CASE WHEN rework IS NOT NULL THEN 1 - rework/3.0 END) AS rework_avoidance,
  SUM(CASE WHEN "Priority" IN ('Urgent','High') THEN 1 ELSE 0 END) AS hp_total,
  SUM(CASE WHEN "Priority" IN ('Urgent','High') AND completed=1 THEN 1 ELSE 0 END) AS hp_completed,
  SUM(CASE WHEN "Priority" IN ('Urgent','High') AND on_time=1 THEN 1 ELSE 0 END) AS hp_on_time,
  ROUND(AVG("Task Difficulty Coefficient"),3) AS avg_diff
FROM t
GROUP BY "Task Owner"
"""
df = db.frame(db.query(sql))
for m in ['completion_rate','on_time_rate','quality_norm','priority_weighted_completion','hours_efficiency','rework_avoidance']:
    df[m] = df[m].fillna(0.0)

metrics = ['completion_rate','on_time_rate','quality_norm','priority_weighted_completion','hours_efficiency','rework_avoidance']
for m in metrics:
    df['p_' + m] = df.groupby('task_type')[m].transform(lambda s: s.rank(pct=True))

W = {'p_completion_rate':0.20,'p_on_time_rate':0.20,'p_quality_norm':0.15,
     'p_priority_weighted_completion':0.20,'p_hours_efficiency':0.15,'p_rework_avoidance':0.10}
df['composite'] = sum(df['p_'+m]*w for m,w in W.items() if ('p_'+m) in df.columns)
df['composite'] = sum(df[k]*w for k,w in W.items())

print(df[['completion_rate','on_time_rate','quality_norm','priority_weighted_completion','hours_efficiency','rework_avoidance','composite']].describe())
print("\nComposite by type:")
print(df.groupby('task_type')['composite'].agg(['count','mean','std']))

# Save for reuse
df.to_csv('/work/owner_metrics.csv', index=False)
print("\nsaved", df.shape)
