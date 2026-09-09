WITH t AS (
  SELECT
    "Task Owner",
    "Task Type",
    "Task Status",
    "Priority",
    "Task Difficulty Coefficient",
    CASE WHEN "Task Status" = 'Completed' THEN 1 ELSE 0 END AS completed,
    CASE WHEN "Priority" = 'Urgent' THEN 4 WHEN "Priority" = 'High' THEN 3
         WHEN "Priority" = 'Medium' THEN 2 WHEN "Priority" = 'Low' THEN 1 END AS pw,
    CASE WHEN "Task Status" = 'Completed' AND "Actual Completion Time" != '-'
              AND "Planned Deadline" != '-'
              AND julianday("Actual Completion Time") <= julianday("Planned Deadline")
         THEN 1 ELSE 0 END AS on_time,
    CASE WHEN "Task Status" = 'Completed' AND "Actual Completion Time" != '-'
              AND "Planned Deadline" != '-'
         THEN julianday("Actual Completion Time") - julianday("Planned Deadline") END AS late_days,
    CASE WHEN "Task Status" = 'Completed' AND "Completion Quality Score" != '-'
         THEN CAST("Completion Quality Score" AS REAL) END AS quality,
    CASE WHEN "Task Status" = 'Completed' AND "Actual Work Hours" != '-'
              AND "Planned Work Hours" > 0
         THEN MIN(("Planned Work Hours" * 1.0) / CAST("Actual Work Hours" AS REAL), 1.5) END AS eff,
    CASE WHEN "Task Status" = 'Completed' AND "Rework Count" != '-'
         THEN CAST("Rework Count" AS INTEGER) END AS rework
  FROM sheet1
)
SELECT
  "Task Owner",
  MAX("Task Type") AS task_type,
  COUNT(*) AS total_tasks,
  SUM(completed) AS completed_tasks,
  ROUND(1.0 * SUM(completed) / COUNT(*), 4) AS completion_rate,
  ROUND(1.0 * SUM(on_time) / NULLIF(SUM(completed),0), 4) AS on_time_rate,
  ROUND(AVG(quality), 4) AS avg_quality,
  ROUND(1.0 * SUM(pw * completed) / NULLIF(SUM(pw), 0), 4) AS priority_weighted_completion,
  ROUND(AVG(eff), 4) AS hours_efficiency,
  ROUND(AVG(CASE WHEN rework IS NOT NULL THEN 1 - rework / 3.0 END), 4) AS rework_avoidance,
  ROUND(AVG(late_days), 3) AS avg_late_days,
  ROUND(AVG("Task Difficulty Coefficient"), 3) AS avg_diff
FROM t
GROUP BY "Task Owner"
ORDER BY "Task Owner"