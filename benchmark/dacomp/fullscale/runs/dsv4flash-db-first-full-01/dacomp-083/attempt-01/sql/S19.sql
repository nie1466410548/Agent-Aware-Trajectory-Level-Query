WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
)
SELECT 
  COUNT(*) as n,
  AVG(career_development_score) as avg_career,
  MIN(career_development_score) as min_career,
  MAX(career_development_score) as max_career,
  AVG(overall_employee_score) as avg_overall,
  MIN(overall_employee_score) as min_overall,
  MAX(overall_employee_score) as max_overall
FROM ranked WHERE rn = 1