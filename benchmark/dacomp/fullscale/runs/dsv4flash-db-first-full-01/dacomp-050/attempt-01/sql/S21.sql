WITH stu AS (
  SELECT *, "Have you ever had suicidal thoughts?" AS suicidal FROM sheet1 WHERE "Working professional or student" = 'Student'
)
SELECT 
  CASE 
    WHEN "Work/study hours" <= 6 THEN '≤6 hrs'
    WHEN "Work/study hours" <= 8 THEN '7-8 hrs'
    ELSE '9+ hrs'
  END AS hrs_group,
  COUNT(*) AS total,
  SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END) AS yes_n,
  ROUND(100.0*SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) AS yes_pct
FROM stu
GROUP BY hrs_group
ORDER BY yes_pct DESC