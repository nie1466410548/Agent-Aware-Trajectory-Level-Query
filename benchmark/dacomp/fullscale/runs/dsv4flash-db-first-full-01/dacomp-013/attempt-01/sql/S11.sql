SELECT "Task Type", "Task Status", COUNT(*) AS cnt
FROM sheet1 GROUP BY "Task Type", "Task Status" ORDER BY "Task Type", "Task Status"