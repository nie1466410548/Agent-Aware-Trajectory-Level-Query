SELECT 
  organization_size_category,
  CASE WHEN management_ratio < 0.15 THEN 'A: <0.15'
       WHEN management_ratio < 0.18 THEN 'B: 0.15-0.18'
       WHEN management_ratio < 0.21 THEN 'C: 0.18-0.21'
       WHEN management_ratio < 0.25 THEN 'D: 0.21-0.25'
       ELSE 'E: >=0.25' END AS mr_bin,
  COUNT(*) n,
  ROUND(AVG(organization_health_score),2) avg_health,
  ROUND(AVG(avg_employee_performance_score),3) avg_perf,
  ROUND(AVG(position_fill_rate),3) avg_fill,
  ROUND(AVG(annual_turnover_rate),3) avg_turnover
FROM workday__organization_overview
GROUP BY organization_size_category, mr_bin
ORDER BY organization_size_category, mr_bin