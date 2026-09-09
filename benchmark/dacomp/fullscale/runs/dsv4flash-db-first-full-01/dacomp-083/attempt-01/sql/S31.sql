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
  employee_risk_level,
  ROUND(AVG(work_conditions_score), 1) as avg_work_cond,
  ROUND(AVG(dept_turnover_rate), 3) as avg_turnover,
  ROUND(AVG(dept_management_ratio), 3) as avg_mgmt_ratio,
  ROUND(AVG(dept_health_score), 1) as avg_dept_health,
  ROUND(AVG(compensation_tier), 1) as avg_comp
FROM core
GROUP BY employee_risk_level