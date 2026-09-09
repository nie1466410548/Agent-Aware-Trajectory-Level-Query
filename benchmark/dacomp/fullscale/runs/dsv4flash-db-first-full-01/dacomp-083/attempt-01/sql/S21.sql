WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
ordered AS (
  SELECT career_development_score, ROW_NUMBER() OVER (ORDER BY career_development_score) as rn, COUNT(*) OVER () as total
  FROM emp
)
SELECT career_development_score as median_career FROM ordered WHERE rn = (total + 1) / 2