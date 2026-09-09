SELECT 
  organization_size_category,
  performance_category,
  COUNT(*) n,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY organization_size_category), 1) AS pct
FROM workday__organization_overview
GROUP BY organization_size_category, performance_category
ORDER BY organization_size_category, performance_category