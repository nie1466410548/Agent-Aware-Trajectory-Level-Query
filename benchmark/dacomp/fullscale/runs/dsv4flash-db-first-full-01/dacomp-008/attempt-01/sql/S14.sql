SELECT
  "Project Type",
  COUNT(*) as count,
  ROUND(AVG("Budget Amount" - "Actual Cost"), 2) as mean_dev,
  ROUND(AVG(("Budget Amount" - "Actual Cost") * ("Budget Amount" - "Actual Cost")) - AVG("Budget Amount" - "Actual Cost") * AVG("Budget Amount" - "Actual Cost"), 2) as variance_dev,
  ROUND(SQRT(MAX(0, AVG(("Budget Amount" - "Actual Cost") * ("Budget Amount" - "Actual Cost")) - AVG("Budget Amount" - "Actual Cost") * AVG("Budget Amount" - "Actual Cost"))), 2) as stddev_dev
FROM sheet1
GROUP BY "Project Type"