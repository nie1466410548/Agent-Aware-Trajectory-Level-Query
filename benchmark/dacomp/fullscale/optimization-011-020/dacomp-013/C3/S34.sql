WITH t AS (
  SELECT
    *
  FROM temp."reuse_013_c3"
)
SELECT
  "Task Owner" AS "Task Owner",
  MAX("Task Type") AS "task_type",
  COUNT(*) AS "total_tasks",
  SUM(completed) AS "completed_tasks",
  1.0 * SUM(completed) / COUNT(*) AS "completion_rate",
  1.0 * SUM(on_time) / NULLIF(SUM(completed), 0) AS "on_time_rate",
  AVG(quality) / 10.0 AS "quality_norm",
  1.0 * SUM(
    CASE
      WHEN "Priority" = 'Urgent'
      THEN 4
      WHEN "Priority" = 'High'
      THEN 3
      WHEN "Priority" = 'Medium'
      THEN 2
      WHEN "Priority" = 'Low'
      THEN 1
    END * completed
  ) / NULLIF(
    SUM(
      CASE
        WHEN "Priority" = 'Urgent'
        THEN 4
        WHEN "Priority" = 'High'
        THEN 3
        WHEN "Priority" = 'Medium'
        THEN 2
        WHEN "Priority" = 'Low'
        THEN 1
      END
    ),
    0
  ) AS "priority_weighted_completion",
  AVG(eff) AS "hours_efficiency",
  AVG(CASE WHEN NOT rework IS NULL THEN 1 - rework / 3.0 END) AS "rework_avoidance",
  SUM(CASE WHEN "Priority" IN ('Urgent', 'High') THEN 1 ELSE 0 END) AS "hp_total",
  SUM(CASE WHEN "Priority" IN ('Urgent', 'High') AND completed = 1 THEN 1 ELSE 0 END) AS "hp_completed",
  SUM(CASE WHEN "Priority" IN ('Urgent', 'High') AND on_time = 1 THEN 1 ELSE 0 END) AS "hp_on_time",
  ROUND(AVG("Task Difficulty Coefficient"), 3) AS "avg_diff"
FROM t
GROUP BY
  "Task Owner";
