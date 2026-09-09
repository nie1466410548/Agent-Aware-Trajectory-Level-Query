SELECT
  "Task Type",
  ROUND(AVG(1.0*completed/total),3) AS avg_completion_rate,
  ROUND(AVG(CASE WHEN completed>0 THEN on_time/completed END),3) AS avg_on_time_rate,
  ROUND(AVG(CASE WHEN completed>0 THEN quality_sum/completed END),3) AS avg_quality
FROM (
  SELECT "Task Owner", "Task Type", COUNT(*) AS total,
    SUM(CASE WHEN "Task Status"='Completed' THEN 1 ELSE 0 END) AS completed,
    SUM(CASE WHEN "Task Status"='Completed' AND "Actual Completion Time" != '-' AND "Planned Deadline" != '-'
              AND julianday("Actual Completion Time") <= julianday("Planned Deadline") THEN 1 ELSE 0 END) AS on_time,
    SUM(CASE WHEN "Task Status"='Completed' AND "Completion Quality Score" != '-'
         THEN CAST("Completion Quality Score" AS REAL) ELSE 0 END) AS quality_sum
  FROM sheet1
  GROUP BY "Task Owner", "Task Type"
)
GROUP BY "Task Type"
ORDER BY "Task Type"