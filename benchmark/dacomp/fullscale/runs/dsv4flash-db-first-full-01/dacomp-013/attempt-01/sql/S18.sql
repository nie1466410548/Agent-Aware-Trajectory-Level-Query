SELECT "Task ID", "Planned Deadline", "Actual Completion Time"
FROM sheet1
WHERE "Task Status" = 'Completed'
ORDER BY "Task ID"
LIMIT 30