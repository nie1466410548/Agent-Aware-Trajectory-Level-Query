WITH stu AS (
  SELECT * FROM sheet1 WHERE "Working professional or student" = 'Student'
    AND "Dietary habits" IN ('Healthy','Moderate','Unhealthy') AND "Sleep duration" IS NOT NULL
)
SELECT 
  ROUND(100.0*SUM(CASE WHEN "Academic stress" >= 4 AND "Financial stress" >= 4 THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_high_both,
  ROUND(100.0*SUM(CASE WHEN ("Academic stress" >= 4 OR "Financial stress" >= 4) AND "Dietary habits"='Unhealthy' AND "Sleep duration"='Less than 5 hours' THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_full_risk
FROM stu