WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1)
SELECT 
  'All Employees' as grp,
  COUNT(*) as n,
  ROUND(AVG(age), 1) as avg_age,
  ROUND(AVG(tenure_years), 2) as avg_tenure,
  ROUND(AVG(overall_employee_score), 1) as avg_overall,
  ROUND(AVG(career_development_score), 1) as avg_career,
  ROUND(AVG(retention_stability_score), 1) as avg_retention,
  ROUND(AVG(total_positions_held), 2) as avg_positions,
  ROUND(AVG(total_promotions), 2) as avg_promotions,
  ROUND(AVG(lateral_moves), 2) as avg_lateral,
  ROUND(AVG(management_positions_held), 2) as avg_mgmt
FROM emp
UNION ALL
SELECT 
  'Core Employees',
  COUNT(*),
  ROUND(AVG(age), 1),
  ROUND(AVG(tenure_years), 2),
  ROUND(AVG(overall_employee_score), 1),
  ROUND(AVG(career_development_score), 1),
  ROUND(AVG(retention_stability_score), 1),
  ROUND(AVG(total_positions_held), 2),
  ROUND(AVG(total_promotions), 2),
  ROUND(AVG(lateral_moves), 2),
  ROUND(AVG(management_positions_held), 2)
FROM emp
WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939