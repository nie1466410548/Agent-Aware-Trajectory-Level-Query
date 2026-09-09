SELECT 
  organization_size_category,
  COUNT(*) n_orgs,
  AVG(organization_health_score) avg_health,
  MIN(organization_health_score) min_health,
  MAX(organization_health_score) max_health,
  AVG(management_ratio) avg_mgmt_ratio,
  MIN(management_ratio) min_mgmt_ratio,
  MAX(management_ratio) max_mgmt_ratio,
  AVG(avg_employee_performance_score) avg_perf_score,
  AVG(position_fill_rate) avg_fill_rate,
  AVG(annual_turnover_rate) avg_turnover,
  AVG(current_active_employees) avg_emp_count
FROM workday__organization_overview
GROUP BY organization_size_category
ORDER BY 
  CASE organization_size_category
    WHEN 'Small (0-30)' THEN 1
    WHEN 'Medium (30-120)' THEN 2
    WHEN 'Large (120-300)' THEN 3
    WHEN 'Extra Large (300+)' THEN 4
  END