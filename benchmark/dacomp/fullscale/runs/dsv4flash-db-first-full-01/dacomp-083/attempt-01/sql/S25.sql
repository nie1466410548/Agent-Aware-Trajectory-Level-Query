WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
core AS (
  SELECT * FROM emp 
  WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
)
SELECT ethnicity_codes, COUNT(*) as cnt, ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM core), 1) as pct
FROM core
GROUP BY ethnicity_codes
ORDER BY cnt DESC