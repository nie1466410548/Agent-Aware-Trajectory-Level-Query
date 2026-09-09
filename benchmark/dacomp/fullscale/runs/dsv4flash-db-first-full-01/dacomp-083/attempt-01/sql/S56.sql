
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
core AS (
  SELECT * FROM emp 
  WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
)
SELECT highest_management_level_reached, dept_performance_category, 
       COUNT(*) as total,
       SUM(CASE WHEN employee_risk_level IN ('High','Medium') THEN 1 ELSE 0 END) as at_risk,
       SUM(CASE WHEN retention_stability_score < 60 THEN 1 ELSE 0 END) as low_retention
FROM core
GROUP BY highest_management_level_reached, dept_performance_category
ORDER BY highest_management_level_reached, dept_performance_category
