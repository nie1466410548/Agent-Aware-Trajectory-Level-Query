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
  MAX(age) as max_val
FROM core
UNION ALL
SELECT 
  'Tenure_years',
  ROUND(AVG(tenure_years), 2),
  ROUND(MIN(tenure_years), 2),
  ROUND(MAX(tenure_years), 2)
FROM core
UNION ALL
SELECT 
  'Total_positions_held',
  ROUND(AVG(total_positions_held), 2),
  MIN(total_positions_held),
  MAX(total_positions_held)
FROM core
UNION ALL
SELECT 
  'Total_promotions',
  ROUND(AVG(total_promotions), 2),
  MIN(total_promotions),
  MAX(total_promotions)
FROM core
UNION ALL
SELECT 
  'Lateral_moves',
  ROUND(AVG(lateral_moves), 2),
  MIN(lateral_moves),
  MAX(lateral_moves)
FROM core
UNION ALL
SELECT 
  'Management_positions_held',
  ROUND(AVG(management_positions_held), 2),
  MIN(management_positions_held),
  MAX(management_positions_held)
FROM core