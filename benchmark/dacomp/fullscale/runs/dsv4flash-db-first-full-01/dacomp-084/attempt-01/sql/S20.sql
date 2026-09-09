SELECT organization_size_category, MIN(management_ratio) mn, MAX(management_ratio) mx,
  ROUND(AVG(management_ratio),3) avg_mr
FROM workday__organization_overview
GROUP BY organization_size_category