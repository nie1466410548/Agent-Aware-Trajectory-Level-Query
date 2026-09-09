SELECT 
  CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END AS tenure_group,
  OverTime, COUNT(*) AS cnt,
  ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (PARTITION BY CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END),2) AS pct_in_group
FROM sheet1
GROUP BY tenure_group, OverTime
ORDER BY tenure_group, OverTime