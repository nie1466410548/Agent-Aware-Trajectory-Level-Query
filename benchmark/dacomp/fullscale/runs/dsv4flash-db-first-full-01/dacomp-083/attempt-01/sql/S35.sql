WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1)
SELECT 
  'All employees' as grp,
  COUNT(*) as n,
  ROUND(100.0 * SUM(is_work_shift_required) / COUNT(*), 1) as shift_pct,
  ROUND(100.0 * SUM(is_union_eligible) / COUNT(*), 1) as union_pct,
  ROUND(AVG(retention_stability_score), 1) as avg_retention,
  ROUND(AVG(overall_employee_score), 1) as avg_overall
FROM emp
UNION ALL
SELECT 
  'High-value attrition risk',
  COUNT(*),
  ROUND(100.0 * SUM(is_work_shift_required) / COUNT(*), 1),
  ROUND(100.0 * SUM(is_union_eligible) / COUNT(*), 1),
  ROUND(AVG(retention_stability_score), 1),
  ROUND(AVG(overall_employee_score), 1)
FROM emp
WHERE retention_stability_score < 60 AND overall_employee_score > 80