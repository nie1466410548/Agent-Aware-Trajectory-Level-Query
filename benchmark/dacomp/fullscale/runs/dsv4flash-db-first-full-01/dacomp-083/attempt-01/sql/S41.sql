WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
core AS (
  SELECT * FROM emp 
  WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
)
SELECT 
  highest_management_level_reached,
  dept_performance_category,
  COUNT(*) as total_core,
  SUM(CASE WHEN employee_risk_level IN ('High','Medium') THEN 1 ELSE 0 END) as risk_core,
  ROUND(100.0 * SUM(CASE WHEN employee_risk_level IN ('High','Medium') THEN 1 ELSE 0 END) / COUNT(*), 1) as risk_pct,
  SUM(CASE WHEN retention_stability_score < 60 THEN 1 ELSE 0 END) as low_retention,
  ROUND(100.0 * SUM(CASE WHEN retention_stability_score < 60 THEN 1 ELSE 0 END) / COUNT(*), 1) as low_retention_pct,
  ROUND(AVG(overall_employee_score), 1) as avg_overall,
  ROUND(AVG(career_development_score), 1) as avg_career
FROM core
GROUP BY highest_management_level_reached, dept_performance_category
ORDER BY highest_management_level_reached, dept_performance_category