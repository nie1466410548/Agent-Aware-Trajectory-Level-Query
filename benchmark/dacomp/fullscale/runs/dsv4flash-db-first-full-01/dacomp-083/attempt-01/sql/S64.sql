
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
  CASE WHEN highest_management_level_reached = 0 THEN 'IC (L0)'
       WHEN highest_management_level_reached = 1 THEN 'Team Lead (L1)'
       WHEN highest_management_level_reached = 2 THEN 'Manager (L2)'
       ELSE 'Sr Mgmt (L3+)' END as mgmt_tier,
  dept_performance_category,
  COUNT(*) as n_core,
  SUM(CASE WHEN employee_risk_level IN ('High','Medium') THEN 1 ELSE 0 END) as n_at_risk,
  ROUND(100.0 * SUM(CASE WHEN employee_risk_level IN ('High','Medium') THEN 1 ELSE 0 END) / COUNT(*), 1) as at_risk_pct
FROM core
GROUP BY mgmt_tier, dept_performance_category
