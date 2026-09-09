SELECT "Priority", "Task Status", COUNT(*) AS cnt
FROM sheet1 GROUP BY "Priority", "Task Status"
ORDER BY "Priority", "Task Status"