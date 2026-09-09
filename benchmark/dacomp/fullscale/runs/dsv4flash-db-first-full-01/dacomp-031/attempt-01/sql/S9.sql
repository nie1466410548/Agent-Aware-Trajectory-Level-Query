SELECT 
  CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END AS tenure_group,
  Department,
  COUNT(*) AS cnt,
  ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (PARTITION BY CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END), 2) AS pct
FROM sheet1
GROUP BY tenure_group, Department
ORDER BY tenure_group, cnt DESC