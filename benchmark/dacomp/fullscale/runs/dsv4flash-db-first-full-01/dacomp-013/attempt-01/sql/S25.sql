SELECT "Task Type", COUNT(DISTINCT "Task Owner") AS owner_count
FROM sheet1
GROUP BY "Task Type"
ORDER BY "Task Type"