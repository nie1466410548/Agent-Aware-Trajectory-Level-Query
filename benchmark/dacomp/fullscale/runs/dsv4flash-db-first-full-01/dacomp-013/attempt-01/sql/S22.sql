SELECT
  CASE
    WHEN task_cnt <= 2 THEN '1-2'
    WHEN task_cnt <= 5 THEN '3-5'
    WHEN task_cnt <= 10 THEN '6-10'
    ELSE '11+'
  END AS owner_task_bucket,
  COUNT(*) AS owner_count
FROM (
  SELECT "Task Owner", SUM(CASE WHEN "Task Status" = 'Completed' THEN 1 ELSE 0 END) AS task_cnt
  FROM sheet1
  GROUP BY "Task Owner"
)
GROUP BY owner_task_bucket
ORDER BY MIN(task_cnt)