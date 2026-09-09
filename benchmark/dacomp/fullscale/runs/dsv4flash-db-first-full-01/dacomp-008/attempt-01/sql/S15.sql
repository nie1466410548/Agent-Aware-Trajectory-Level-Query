SELECT
  "Risk Level",
  ROUND(AVG("Budget Amount" - "Actual Cost"), 2) as mean_dev,
  ROUND(SQRT(MAX(0, AVG(("Budget Amount" - "Actual Cost") * ("Budget Amount" - "Actual Cost")) - AVG("Budget Amount" - "Actual Cost") * AVG("Budget Amount" - "Actual Cost"))), 2) as stddev_dev,
  ROUND(AVG("Budget Amount"), 2) as avg_budget,
  ROUND(AVG("Actual Cost"), 2) as avg_actual
FROM sheet1
GROUP BY "Risk Level"