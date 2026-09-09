SELECT
  CASE
    WHEN completed = 0 THEN '0 completed'
    WHEN completed = 1 THEN '1 completed'
    WHEN completed BETWEEN 2 AND 4 THEN '2-4 completed'
    ELSE '5+ completed'
  END AS bucket,
  COUNT(*) AS owner_count
FROM (
  SELECT "Task Owner",
    SUM(CASE WHEN "Task Status" = 'Completed' THEN 1 ELSE 0 END) AS completed,
    COUNT(*) AS total
  FROM sheet1
  GROUP BY "Task Owner"
)
GROUP BY bucket
ORDER BY MIN(completed)