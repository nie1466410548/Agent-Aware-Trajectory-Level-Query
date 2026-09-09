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
  compensation_tier,
  COUNT(*) as total_core,
  SUM(CASE WHEN employee_risk_level = 'High' THEN 1 ELSE 0 END) as high_risk,
  ROUND(100.0 * SUM(CASE WHEN employee_risk_level = 'High' THEN 1 ELSE 0 END) / COUNT(*), 1) as high_risk_pct,
  ROUND(AVG(work_conditions_score), 1) as avg_work_cond,
  ROUND(AVG(dept_turnover_rate), 3) as avg_turnover,
  ROUND(AVG(dept_management_ratio), 3) as avg_mgmt_ratio,
  ROUND(AVG(dept_health_score), 1) as avg_dept_health
FROM core
GROUP BY compensation_tier
ORDER BY high_risk_pct DESC