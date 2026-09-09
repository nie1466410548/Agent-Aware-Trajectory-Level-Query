WITH stu AS (
  SELECT *, "Have you ever had suicidal thoughts?" AS suicidal FROM sheet1 WHERE "Working professional or student" = 'Student'
  AND "Dietary habits" IN ('Healthy','Moderate','Unhealthy')
)
SELECT 
  "Dietary habits",
  CASE WHEN "Sleep duration" = 'Less than 5 hours' THEN 'Sleep<5h' ELSE 'Sleep>=5h' END AS sleep_cat,
  COUNT(*) AS total,
  SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END) AS yes_n,
  ROUND(100.0*SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) AS yes_pct
FROM stu
GROUP BY "Dietary habits", sleep_cat
ORDER BY yes_pct DESC