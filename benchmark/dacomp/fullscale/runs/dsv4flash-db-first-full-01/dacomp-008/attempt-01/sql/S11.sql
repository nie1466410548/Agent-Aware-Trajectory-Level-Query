SELECT 
  "Project Status",
  COUNT(*) as count,
  ROUND(AVG("Budget Amount" - "Actual Cost"), 2) as avg_cost_deviation,
  ROUND(AVG("Budget Amount"), 2) as avg_budget,  
  ROUND(AVG("Actual Cost"), 2) as avg_actual_cost
FROM sheet1
GROUP BY "Project Status"
ORDER BY avg_cost_deviation DESC