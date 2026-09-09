SELECT
  "Task Owner",
  COUNT(*) AS total_tasks,
  SUM(CASE WHEN "Task Status" = 'Completed' THEN 1 ELSE 0 END) AS completed_tasks,
  SUM(CASE WHEN "Task Status" = 'In Progress' THEN 1 ELSE 0 END) AS in_progress,
  SUM(CASE WHEN "Task Status" = 'Not Started' THEN 1 ELSE 0 END) AS not_started,
  SUM(CASE WHEN "Task Status" = 'Paused' THEN 1 ELSE 0 END) AS paused
FROM sheet1
GROUP BY "Task Owner"
HAVING total_tasks >= 3
ORDER BY completed_tasks DESC
LIMIT 30