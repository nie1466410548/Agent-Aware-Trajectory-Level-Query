SELECT 
  "Project Type",
  "Priority",
  COUNT(*) as count,
  ROUND(AVG("Budget Amount" - "Actual Cost"), 2) as avg_cost_deviation
FROM sheet1
GROUP BY "Project Type", "Priority"
ORDER BY "Project Type", "Priority"