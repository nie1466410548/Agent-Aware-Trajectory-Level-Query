SELECT
  "Task Type",
  ROUND(AVG("Task Difficulty Coefficient"),3) AS avg_diff,
  ROUND(AVG("Planned Work Hours"),1) AS avg_planned,
  ROUND(AVG(CASE WHEN "Task Status"='Completed' THEN CAST("Actual Work Hours" AS REAL) END),1) AS avg_actual,
  ROUND(AVG(CASE WHEN "Task Status"='Completed' THEN CAST("Completion Quality Score" AS REAL) END),2) AS avg_quality
FROM sheet1
GROUP BY "Task Type"
ORDER BY "Task Type"