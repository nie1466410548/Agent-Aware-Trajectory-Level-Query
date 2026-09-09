SELECT
  "Project Type",
  "Project Status",
  COUNT(*) as n,
  ROUND(AVG("Budget Amount" - "Actual Cost"), 2) as avg_dev,
  ROUND(AVG(("Budget Amount" - "Actual Cost") * 100.0 / "Budget Amount"), 2) as avg_dev_pct
FROM sheet1
GROUP BY "Project Type", "Project Status"
ORDER BY "Project Type", "Project Status"