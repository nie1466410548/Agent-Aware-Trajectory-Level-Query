SELECT 
  "Project Type",
  "Risk Level",
  COUNT(*) as count,
  ROUND(AVG("Budget Amount" - "Actual Cost"), 2) as avg_cost_deviation,
  ROUND(AVG("Team Size"), 1) as avg_team_size,
  ROUND(AVG("Customer Satisfaction"), 2) as avg_satisfaction
FROM sheet1
GROUP BY "Project Type", "Risk Level"
ORDER BY "Project Type", "Risk Level"