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
  organization_type,
  organization_sub_type,
  COUNT(*) as total_core,
  ROUND(100.0 * SUM(CASE WHEN employee_risk_level IN ('High','Medium') THEN 1 ELSE 0 END) / COUNT(*), 1) as risk_pct,
  ROUND(AVG(highest_management_level_reached), 2) as avg_mgmt_level,
  ROUND(AVG(retention_stability_score), 1) as avg_retention,
  ROUND(AVG(overall_employee_score), 1) as avg_overall
FROM core
GROUP BY organization_type, organization_sub_type
HAVING COUNT(*) >= 20
ORDER BY risk_pct DESC