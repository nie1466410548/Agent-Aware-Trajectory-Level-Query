SELECT 
  CASE WHEN current_active_employees < 30 THEN 'Small (<30)'
       WHEN current_active_employees BETWEEN 30 AND 120 THEN 'Medium (30-120)'
       WHEN current_active_employees BETWEEN 121 AND 300 THEN 'Large (120-300)'
       ELSE 'Extra Large (>300)' END AS my_tier,
  organization_size_category AS existing_tier,
  COUNT(*) n
FROM workday__organization_overview
GROUP BY my_tier, existing_tier
ORDER BY my_tier