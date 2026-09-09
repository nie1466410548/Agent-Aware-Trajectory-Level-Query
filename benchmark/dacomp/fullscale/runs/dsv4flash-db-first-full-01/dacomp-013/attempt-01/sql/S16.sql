SELECT
  "Priority",
  COUNT(*) AS cnt,
  AVG(CAST("Completion Quality Score" AS REAL)) AS avg_quality,
  AVG("Task Difficulty Coefficient") AS avg_diff
FROM sheet1
WHERE "Task Status" = 'Completed'
  AND "Completion Quality Score" != '-'
GROUP BY "Priority"
ORDER BY "Priority"