SELECT
  "Task Type",
  COUNT(*) AS cnt,
  AVG(CAST("Completion Quality Score" AS REAL)) AS avg_quality,
  AVG("Task Difficulty Coefficient") AS avg_diff,
  AVG(CAST("Actual Work Hours" AS REAL)) AS avg_actual_hours,
  AVG("Planned Work Hours") AS avg_planned_hours,
  AVG(CAST("Actual Work Hours" AS REAL) * 1.0 / "Planned Work Hours") AS avg_hours_ratio,
  AVG(CAST("Rework Count" AS INTEGER)) AS avg_rework
FROM sheet1
WHERE "Task Status" = 'Completed'
  AND "Completion Quality Score" != '-'
  AND "Actual Work Hours" != '-'
  AND "Rework Count" != '-'
GROUP BY "Task Type"
ORDER BY "Task Type"