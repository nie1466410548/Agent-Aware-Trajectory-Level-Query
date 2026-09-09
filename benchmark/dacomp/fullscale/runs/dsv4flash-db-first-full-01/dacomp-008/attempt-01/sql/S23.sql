SELECT
  "Project Type",
  "Risk Level",
  COUNT(*) as n,
  ROUND(AVG("Budget Amount" - "Actual Cost"), 2) as avg_dev,
  ROUND(AVG(("Budget Amount" - "Actual Cost")*100.0/"Budget Amount"), 2) as avg_dev_pct
FROM sheet1
WHERE "Project Status" = 'Completed'
GROUP BY "Project Type", "Risk Level"
ORDER BY "Project Type", "Risk Level"