WITH stu AS (
  SELECT * FROM sheet1 WHERE "Working professional or student" = 'Student'
    AND "Dietary habits" IN ('Healthy','Moderate','Unhealthy') AND "Sleep duration" IS NOT NULL
)
SELECT 
  ROUND(100.0*SUM(CASE WHEN "Academic stress" >= 4 THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_high_acad,
  ROUND(100.0*SUM(CASE WHEN "Financial stress" >= 4 THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_high_fin,
  ROUND(100.0*SUM(CASE WHEN "Dietary habits"='Unhealthy' THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_unhealthy_diet,
  ROUND(100.0*SUM(CASE WHEN "Sleep duration"='Less than 5 hours' THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_short_sleep,
  COUNT(*) AS n
FROM stu