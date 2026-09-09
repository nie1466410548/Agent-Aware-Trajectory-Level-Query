SELECT 
  COUNT(*) total,
  SUM(CASE WHEN span_of_control IS NOT NULL THEN 1 ELSE 0 END) n_span,
  SUM(CASE WHEN talent_density_ratio IS NOT NULL THEN 1 ELSE 0 END) n_tdr,
  SUM(CASE WHEN high_value_retention_rate IS NOT NULL THEN 1 ELSE 0 END) n_hvrr,
  SUM(CASE WHEN talent_flight_risk_rate IS NOT NULL THEN 1 ELSE 0 END) n_tfrr,
  SUM(CASE WHEN high_achiever_percentage IS NOT NULL THEN 1 ELSE 0 END) n_hap,
  SUM(CASE WHEN avg_employee_satisfaction_proxy IS NOT NULL THEN 1 ELSE 0 END) n_sat
FROM workday__organization_performance