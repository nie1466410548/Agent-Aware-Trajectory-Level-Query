SELECT 
  "Project Type",
  COUNT(*) as count,
  ROUND(AVG("Budget Amount" - "Actual Cost"), 2) as avg_cost_deviation,
  ROUND(AVG("Budget Amount"), 2) as avg_budget,
  ROUND(AVG("Actual Cost"), 2) as avg_actual_cost,
  ROUND(MIN("Budget Amount" - "Actual Cost"), 2) as min_deviation,
  ROUND(MAX("Budget Amount" - "Actual Cost"), 2) as max_deviation,
  ROUND(AVG("Team Size"), 1) as avg_team_size,
  ROUND(AVG("Customer Satisfaction"), 2) as avg_customer_satisfaction
FROM sheet1
GROUP BY "Project Type"
ORDER BY avg_cost_deviation DESC