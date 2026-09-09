WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY organization_size_category ORDER BY organization_health_score DESC) rn,
    COUNT(*) OVER (PARTITION BY organization_size_category) n
  FROM workday__organization_overview
)
SELECT organization_size_category, 
  CASE WHEN rn <= CEIL(n*0.1) THEN 'Top10%' ELSE 'Rest' END AS grp,
  COUNT(*) n,
  ROUND(AVG(organization_health_score),1) avg_health,
  ROUND(AVG(management_ratio),3) avg_mr,
  ROUND(AVG(avg_employee_performance_score),3) avg_perf,
  ROUND(AVG(position_fill_rate),3) avg_fill,
  ROUND(AVG(annual_turnover_rate),3) avg_turnover,
  ROUND(AVG(avg_career_development_score),3) avg_dev,
  ROUND(AVG(avg_retention_stability_score),3) avg_ret,
  ROUND(AVG(avg_current_tenure_years),2) avg_tenure,
  ROUND(AVG(organization_age_years),2) avg_age
FROM ranked
GROUP BY organization_size_category, grp
ORDER BY organization_size_category, grp