SELECT 
  CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END AS tenure_group,
  SalarySlab, COUNT(*) AS cnt,
  ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (PARTITION BY CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END),2) AS pct_in_group
FROM sheet1
GROUP BY tenure_group, SalarySlab
ORDER BY tenure_group, cnt DESC