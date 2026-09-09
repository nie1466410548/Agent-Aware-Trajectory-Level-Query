SELECT
  MIN("Planned Work Hours") AS min_planned, MAX("Planned Work Hours") AS max_planned,
  AVG("Planned Work Hours") AS avg_planned,
  SUM(CASE WHEN "Actual Work Hours" = '-' OR "Actual Work Hours" = '' OR "Actual Work Hours" IS NULL THEN 1 ELSE 0 END) AS missing_actual_hours,
  SUM(CASE WHEN "Completion Quality Score" = '-' OR "Completion Quality Score" = '' OR "Completion Quality Score" IS NULL THEN 1 ELSE 0 END) AS missing_quality,
  SUM(CASE WHEN "Rework Count" = '-' OR "Rework Count" = '' OR "Rework Count" IS NULL THEN 1 ELSE 0 END) AS missing_rework
FROM sheet1