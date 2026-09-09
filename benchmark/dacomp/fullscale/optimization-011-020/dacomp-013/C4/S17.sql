SELECT
  __g3 AS "Task Owner",
  __g2 AS "Task Type",
  SUM(__a0) AS "total_tasks",
  SUM(__a1) AS "completed_tasks"
FROM temp."reuse_013_c4"
GROUP BY
  __g3,
  __g2
ORDER BY
  __g3,
  __g2;
