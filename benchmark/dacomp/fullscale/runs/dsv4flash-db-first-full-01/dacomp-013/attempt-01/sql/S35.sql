
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
    CASE WHEN "Task Status" = 'Completed' THEN 1 ELSE 0 END AS is_comp
  FROM sheet1
)
SELECT
  "Task Owner", MAX("Task Type") AS task_type,
  COUNT(*) AS total_tasks,
  SUM(completed) AS completed_tasks,
  SUM(CASE WHEN "Task Status" = 'Completed' AND "Actual Completion Time" != '-'
              AND "Planned Deadline" != '-' THEN 1 ELSE 0 END) AS timed_completed,
  SUM(CASE WHEN "Task Status" = 'Completed' AND "Completion Quality Score" != '-' THEN 1 ELSE 0 END) AS scored_completed,
  SUM(CASE WHEN "Task Status" = 'Completed' AND "Actual Work Hours" != '-' AND "Planned Work Hours" > 0 THEN 1 ELSE 0 END) AS eff_completed,
  SUM(CASE WHEN "Task Status" = 'Completed' AND "Rework Count" != '-' THEN 1 ELSE 0 END) AS rework_completed,
  1.0*SUM(completed)/COUNT(*) AS completion_rate,
  1.0*SUM(on_time)/NULLIF(SUM(completed),0) AS on_time_rate,
  AVG(quality)/10.0 AS quality_norm,
  1.0*SUM(CASE WHEN "Priority"='Urgent' THEN 4 WHEN "Priority"='High' THEN 3
         WHEN "Priority"='Medium' THEN 2 WHEN "Priority"='Low' THEN 1 END * completed)
    /NULLIF(SUM(CASE WHEN "Priority"='Urgent' THEN 4 WHEN "Priority"='High' THEN 3
         WHEN "Priority"='Medium' THEN 2 WHEN "Priority"='Low' THEN 1 END),0) AS priority_weighted_completion,
  AVG(eff) AS hours_efficiency,
  AVG(CASE WHEN rework IS NOT NULL THEN 1 - rework/3.0 END) AS rework_avoidance
FROM t
GROUP BY "Task Owner"
