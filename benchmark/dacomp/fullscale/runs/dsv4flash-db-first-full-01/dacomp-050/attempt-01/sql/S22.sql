WITH stu AS (
  SELECT *, "Have you ever had suicidal thoughts?" AS suicidal FROM sheet1 WHERE "Working professional or student" = 'Student'
)
SELECT 
  CASE 
    WHEN "Cumulative GPA (CGPA)" < 6 THEN 'CGPA < 6'
    WHEN "Cumulative GPA (CGPA)" < 7.5 THEN 'CGPA 6-7.49'
    WHEN "Cumulative GPA (CGPA)" < 8.5 THEN 'CGPA 7.5-8.49'
    ELSE 'CGPA ≥ 8.5'
  END AS cgpa_group,
  COUNT(*) AS total,
  SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END) AS yes_n,
  ROUND(100.0*SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) AS yes_pct
FROM stu
GROUP BY cgpa_group
ORDER BY yes_pct DESC