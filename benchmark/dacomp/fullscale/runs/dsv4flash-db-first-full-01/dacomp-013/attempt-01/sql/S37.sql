
SELECT "Task Owner", ROUND(AVG("Task Difficulty Coefficient"),3) AS avg_diff
FROM sheet1 GROUP BY "Task Owner"
