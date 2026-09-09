WITH stu AS (
  SELECT *, "Have you ever had suicidal thoughts?" AS suicidal FROM sheet1 WHERE "Working professional or student" = 'Student'
)
SELECT 
  "Sleep duration",
  COUNT(*) AS total,
  SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END) AS yes_n,
  ROUND(100.0*SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) AS yes_pct
FROM stu
GROUP BY "Sleep duration"
ORDER BY yes_pct DESC