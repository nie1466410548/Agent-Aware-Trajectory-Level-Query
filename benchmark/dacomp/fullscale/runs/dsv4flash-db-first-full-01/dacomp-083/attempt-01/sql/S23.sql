WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
core AS (
  SELECT * FROM emp 
  WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
)
SELECT 
  'Age' as feature,
  ROUND(AVG(age), 1) as avg_val,
  MIN(age) as min_val,
  MAX(age) as max_val,
  ROUND(AVG(age) - STDDEV(age), 1) as low_std,
  ROUND(AVG(age) + STDDEV(age), 1) as high_std
FROM core
UNION ALL
SELECT 
  'Tenure_years' as feature,
  ROUND(AVG(tenure_years), 2) as avg_val,
  ROUND(MIN(tenure_years), 2) as min_val,
  ROUND(MAX(tenure_years), 2) as max_val,
  ROUND(AVG(tenure_years) - STDDEV(tenure_years), 2) as low_std,
  ROUND(AVG(tenure_years) + STDDEV(tenure_years), 2) as high_std
FROM core
UNION ALL
SELECT 
  'Total_positions_held' as feature,
  ROUND(AVG(total_positions_held), 2) as avg_val,
  MIN(total_positions_held) as min_val,
  MAX(total_positions_held) as max_val,
  ROUND(AVG(total_positions_held) - STDDEV(total_positions_held), 2) as low_std,
  ROUND(AVG(total_positions_held) + STDDEV(total_positions_held), 2) as high_std
FROM core
UNION ALL
SELECT 
  'Total_promotions' as feature,
  ROUND(AVG(total_promotions), 2) as avg_val,
  MIN(total_promotions) as min_val,
  MAX(total_promotions) as max_val,
  ROUND(AVG(total_promotions) - STDDEV(total_promotions), 2) as low_std,
  ROUND(AVG(total_promotions) + STDDEV(total_promotions), 2) as high_std
FROM core
UNION ALL
SELECT 
  'Lateral_moves' as feature,
  ROUND(AVG(lateral_moves), 2) as avg_val,
  MIN(lateral_moves) as min_val,
  MAX(lateral_moves) as max_val,
  ROUND(AVG(lateral_moves) - STDDEV(lateral_moves), 2) as low_std,
  ROUND(AVG(lateral_moves) + STDDEV(lateral_moves), 2) as high_std
FROM core
UNION ALL
SELECT 
  'Management_positions_held' as feature,
  ROUND(AVG(management_positions_held), 2) as avg_val,
  MIN(management_positions_held) as min_val,
  MAX(management_positions_held) as max_val,
  ROUND(AVG(management_positions_held) - STDDEV(management_positions_held), 2) as low_std,
  ROUND(AVG(management_positions_held) + STDDEV(management_positions_held), 2) as high_std
FROM core