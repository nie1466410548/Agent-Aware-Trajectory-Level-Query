
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1)
SELECT age, tenure_years, overall_employee_score, career_development_score, retention_stability_score,
       employee_risk_level, total_positions_held, total_promotions, lateral_moves, management_positions_held
FROM emp
