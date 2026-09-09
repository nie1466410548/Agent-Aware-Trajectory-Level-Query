WITH ranked AS (
  SELECT organization_id, organization_name, organization_size_category,
    current_active_employees, organization_health_score, performance_category,
    management_ratio, avg_employee_performance_score, position_fill_rate, annual_turnover_rate,
    avg_career_development_score, avg_retention_stability_score,
    ROW_NUMBER() OVER (PARTITION BY organization_size_category ORDER BY organization_health_score DESC) rn,
    COUNT(*) OVER (PARTITION BY organization_size_category) n
  FROM workday__organization_overview
)
SELECT organization_size_category, n AS tier_n, CEIL(n*0.1) AS top_k, rn,
  organization_id, organization_name, current_active_employees, organization_health_score,
  performance_category, management_ratio, avg_employee_performance_score, position_fill_rate, annual_turnover_rate
FROM ranked
WHERE rn <= CEIL(n*0.1)
ORDER BY organization_size_category, rn