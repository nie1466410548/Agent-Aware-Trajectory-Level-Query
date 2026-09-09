WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1)
SELECT 
  SUM(is_work_shift_required) as shift_required,
  SUM(is_union_eligible) as union_eligible,
  ROUND(100.0 * SUM(is_work_shift_required) / COUNT(*), 1) as shift_required_pct,
  ROUND(100.0 * SUM(is_union_eligible) / COUNT(*), 1) as union_eligible_pct
FROM emp
WHERE retention_stability_score < 60 AND overall_employee_score > 80