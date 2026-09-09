SELECT 
  SUM(CASE WHEN avg_career_development_score > 0 THEN 1 ELSE 0 END) n_dev,
  SUM(CASE WHEN avg_retention_stability_score > 0 THEN 1 ELSE 0 END) n_ret,
  SUM(CASE WHEN avg_current_tenure_years > 0 THEN 1 ELSE 0 END) n_tenure,
  SUM(CASE WHEN high_value_stable_employees > 0 THEN 1 ELSE 0 END) n_hvs,
  SUM(CASE WHEN management_role_employees > 0 THEN 1 ELSE 0 END) n_mgmt,
  SUM(CASE WHEN high_risk_employee_percentage > 0 THEN 1 ELSE 0 END) n_hrp,
  SUM(CASE WHEN total_promotions_in_organization > 0 THEN 1 ELSE 0 END) n_prom,
  SUM(CASE WHEN avg_employee_age > 0 THEN 1 ELSE 0 END) n_age
FROM workday__organization_overview