
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
core AS (
  SELECT * FROM emp 
  WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
)
SELECT career_phase, employee_maturity_segment, 
       COUNT(*) as total,
       SUM(CASE WHEN employee_risk_level = 'High' THEN 1 ELSE 0 END) as high_risk,
       SUM(CASE WHEN employee_risk_level = 'Medium' THEN 1 ELSE 0 END) as med_risk,
       SUM(CASE WHEN employee_risk_level = 'Low' THEN 1 ELSE 0 END) as low_risk
FROM core
GROUP BY career_phase, employee_maturity_segment
ORDER BY career_phase, employee_maturity_segment
