SELECT
  "Task Status",
  ROUND(AVG("Task Difficulty Coefficient"),3) AS avg_diff,
  ROUND(AVG("Planned Work Hours"),1) AS avg_planned
FROM sheet1
GROUP BY "Task Status"
ORDER BY "Task Status"