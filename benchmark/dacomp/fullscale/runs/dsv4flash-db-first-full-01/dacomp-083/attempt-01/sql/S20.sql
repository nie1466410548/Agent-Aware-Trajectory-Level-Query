WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
)
SELECT career_development_score FROM ranked WHERE rn = 1 ORDER BY career_development_score LIMIT 1 OFFSET (SELECT COUNT(*)/2 FROM ranked WHERE rn = 1)