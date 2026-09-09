WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1)
SELECT 
  'All Employees' as grp,
  ROUND(100.0 * SUM(CASE WHEN employee_risk_level = 'High' THEN 1 ELSE 0 END) / COUNT(*), 1) as high_risk_pct,
  ROUND(100.0 * SUM(CASE WHEN employee_risk_level = 'Medium' THEN 1 ELSE 0 END) / COUNT(*), 1) as med_risk_pct,
  ROUND(100.0 * SUM(CASE WHEN employee_risk_level = 'Low' THEN 1 ELSE 0 END) / COUNT(*), 1) as low_risk_pct,
  SUM(CASE WHEN retention_stability_score < 60 AND overall_employee_score > 80 THEN 1 ELSE 0 END) as high_value_attrition_risk
FROM emp
UNION ALL
SELECT 
  'Core Employees',
  ROUND(100.0 * SUM(CASE WHEN employee_risk_level = 'High' THEN 1 ELSE 0 END) / COUNT(*), 1),
  ROUND(100.0 * SUM(CASE WHEN employee_risk_level = 'Medium' THEN 1 ELSE 0 END) / COUNT(*), 1),
  ROUND(100.0 * SUM(CASE WHEN employee_risk_level = 'Low' THEN 1 ELSE 0 END) / COUNT(*), 1),
  SUM(CASE WHEN retention_stability_score < 60 AND overall_employee_score > 80 THEN 1 ELSE 0 END)
FROM emp
WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939