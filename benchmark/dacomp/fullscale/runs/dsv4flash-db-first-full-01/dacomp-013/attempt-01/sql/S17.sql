SELECT
  "Task Owner",
  "Task Type",
  COUNT(*) AS total_tasks,
  SUM(CASE WHEN "Task Status" = 'Completed' THEN 1 ELSE 0 END) AS completed_tasks
FROM sheet1
GROUP BY "Task Owner", "Task Type"
ORDER BY "Task Owner", "Task Type"