WITH stu AS (
  SELECT *, "Have you ever had suicidal thoughts?" AS suicidal FROM sheet1 WHERE "Working professional or student" = 'Student'
)
SELECT 
  CASE 
    WHEN "Satisfaction with studies" <= 2 THEN 'Low (1-2)'
    WHEN "Satisfaction with studies" = 3 THEN 'Medium (3)'
    ELSE 'High (4-5)'
  END AS sat_group,
  COUNT(*) AS total,
  SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END) AS yes_n,
  ROUND(100.0*SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) AS yes_pct
FROM stu
GROUP BY sat_group
ORDER BY yes_pct DESC