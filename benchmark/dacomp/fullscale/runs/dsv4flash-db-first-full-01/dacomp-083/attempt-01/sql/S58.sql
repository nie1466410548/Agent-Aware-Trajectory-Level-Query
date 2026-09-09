WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1)
SELECT 
  ethnicity_codes,
  COUNT(*) as total,
  SUM(CASE WHEN overall_employee_score > 75 AND career_development_score > 78.57581219355939 THEN 1 ELSE 0 END) as core,
  ROUND(100.0 * SUM(CASE WHEN overall_employee_score > 75 AND career_development_score > 78.57581219355939 THEN 1 ELSE 0 END) / COUNT(*), 1) as core_rate_pct
FROM emp
GROUP BY ethnicity_codes
ORDER BY core_rate_pct DESC