WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
core AS (
  SELECT * FROM emp 
  WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
)
SELECT employee_id, age, tenure_years, marital_status, ethnicity_codes, total_positions_held, total_promotions, lateral_moves, management_positions_held, career_phase, employee_maturity_segment, compensation_tier, work_conditions_score, dept_turnover_rate, dept_health_score, organization_type, organization_sub_type, retention_stability_score, overall_employee_score, career_development_score
FROM core
WHERE employee_risk_level = 'High'
ORDER BY retention_stability_score