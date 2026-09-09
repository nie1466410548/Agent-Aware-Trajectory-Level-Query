SELECT 
  ROUND(("Budget Amount" - "Actual Cost") / NULLIF("Budget Amount", 0) * 100, 1) as deviation_pct,
  "Budget Amount" - "Actual Cost" as deviation,
  "Project Type", "Risk Level", "Team Size", "Customer Satisfaction", "Project Status"
FROM sheet1
ORDER BY deviation DESC
LIMIT 15