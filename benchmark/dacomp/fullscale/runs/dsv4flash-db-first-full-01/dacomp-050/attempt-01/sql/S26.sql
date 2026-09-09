SELECT 
  CASE WHEN Age < 20 THEN '<20' WHEN Age <= 24 THEN '20-24' WHEN Age <= 29 THEN '25-29' ELSE '30+' END AS age_group,
  COUNT(*) AS total,
  SUM(CASE WHEN "Have you ever had suicidal thoughts?"='Yes' THEN 1 ELSE 0 END) AS yes_n,
  ROUND(100.0*SUM(CASE WHEN "Have you ever had suicidal thoughts?"='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) AS yes_pct
FROM sheet1 
WHERE "Working professional or student" = 'Student'
GROUP BY age_group
ORDER BY age_group