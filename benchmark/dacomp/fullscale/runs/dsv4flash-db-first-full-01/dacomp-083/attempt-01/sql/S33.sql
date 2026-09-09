WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1)
SELECT 
  employee_value_segment,
  COUNT(*) as cnt,
  ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM emp WHERE retention_stability_score < 60 AND overall_employee_score > 80), 1) as pct
FROM emp
WHERE retention_stability_score < 60 AND overall_employee_score > 80
GROUP BY employee_value_segment
ORDER BY cnt DESC