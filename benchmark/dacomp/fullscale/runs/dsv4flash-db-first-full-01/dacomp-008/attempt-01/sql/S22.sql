SELECT
  "Risk Level",
  "Project Status",
  COUNT(*) as n,
  ROUND(AVG("Budget Amount" - "Actual Cost"), 2) as avg_dev
FROM sheet1
WHERE "Project Status" = 'Completed'
GROUP BY "Risk Level"
ORDER BY avg_dev DESC