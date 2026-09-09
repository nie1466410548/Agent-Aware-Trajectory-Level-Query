WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY organization_size_category ORDER BY organization_health_score DESC) rn,
    COUNT(*) OVER (PARTITION BY organization_size_category) n
  FROM workday__organization_overview
)
SELECT organization_size_category, organization_id, organization_name, current_active_employees,
  organization_health_score, performance_category, management_ratio, avg_employee_performance_score,
  position_fill_rate, annual_turnover_rate, organization_type, staffing_model, organization_maturity_level,
  unique_organization_roles, total_promotions_in_organization
FROM ranked
WHERE rn <= CEIL(n*0.1)
ORDER BY organization_size_category, rn