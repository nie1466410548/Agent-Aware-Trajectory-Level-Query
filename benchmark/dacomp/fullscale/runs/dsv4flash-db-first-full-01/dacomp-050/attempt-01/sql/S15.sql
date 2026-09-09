WITH stu AS (
  SELECT *, "Have you ever had suicidal thoughts?" AS suicidal FROM sheet1 WHERE "Working professional or student" = 'Student'
)
SELECT 
  CASE WHEN "Dietary habits" IN ('Healthy','Moderate','Unhealthy') THEN "Dietary habits" ELSE 'Other/Unknown' END AS diet_group,
  COUNT(*) AS total,
  SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END) AS yes_n,
  ROUND(100.0*SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) AS yes_pct
FROM stu
GROUP BY diet_group
ORDER BY yes_pct DESC