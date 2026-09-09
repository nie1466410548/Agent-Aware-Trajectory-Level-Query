WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  "Sales Quantity",
  is_low,
  COUNT(*) AS n,
  ROUND(AVG("Total Logistics Revenue"), 2) AS avg_rev,
  ROUND(AVG("Total Logistics Cost"), 2) AS avg_cost,
  ROUND(AVG("Profit"), 2) AS avg_profit,
  ROUND(AVG("Profit Margin"), 4) AS avg_pm
FROM lm
GROUP BY "Sales Quantity", is_low
ORDER BY "Sales Quantity", is_low
LIMIT 30