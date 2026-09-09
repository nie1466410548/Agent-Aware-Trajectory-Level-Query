
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
core AS (
  SELECT * FROM emp 
  WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
)
SELECT age, tenure_years, total_positions_held, total_promotions, lateral_moves, management_positions_held, 
       overall_employee_score, career_development_score, retention_stability_score,
       marital_status, ethnicity_codes, career_phase, employee_maturity_segment,
       employee_risk_level, compensation_tier, work_conditions_score, dept_turnover_rate,
       dept_health_score, dept_management_ratio, organization_type, organization_sub_type,
       dept_performance_category, highest_management_level_reached,
       is_work_shift_required, is_union_eligible, employee_value_segment
FROM core
