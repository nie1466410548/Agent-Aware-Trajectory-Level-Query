SELECT
  "Project Status",
  COUNT(*) as n,
  ROUND(AVG("Budget Amount" - "Actual Cost"), 2) as avg_dev,
  ROUND(AVG(("Budget Amount" - "Actual Cost")*100.0/"Budget Amount"), 2) as avg_dev_pct,
  ROUND(AVG("Customer Satisfaction"), 2) as avg_sat
FROM sheet1
GROUP BY "Project Status"
ORDER BY avg_dev DESC