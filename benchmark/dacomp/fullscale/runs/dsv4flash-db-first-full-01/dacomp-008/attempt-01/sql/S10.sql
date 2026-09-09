SELECT 
  "Risk Level",
  COUNT(*) as count,
  ROUND(AVG("Budget Amount" - "Actual Cost"), 2) as avg_cost_deviation,
  ROUND(AVG("Budget Amount"), 2) as avg_budget,
  ROUND(AVG("Actual Cost"), 2) as avg_actual_cost,
  ROUND(MIN("Budget Amount" - "Actual Cost"), 2) as min_deviation,
  ROUND(MAX("Budget Amount" - "Actual Cost"), 2) as max_deviation
FROM sheet1
GROUP BY "Risk Level"
ORDER BY avg_cost_deviation DESC