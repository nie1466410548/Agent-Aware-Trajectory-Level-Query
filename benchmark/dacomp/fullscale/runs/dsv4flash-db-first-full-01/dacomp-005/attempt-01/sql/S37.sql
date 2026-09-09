WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
  WHERE "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1)
)
SELECT 
  "Consigned Product",
  "Sales Quantity",
  COUNT(*) AS n,
  ROUND(AVG("Discount Amount" / NULLIF("List Price Revenue",0) * 100), 2) AS avg_disc_rate,
  ROUND(AVG("Total Logistics Cost" / NULLIF("Sales Quantity",0)), 2) AS avg_cost_per_unit,
  ROUND(AVG("Total Logistics Revenue" / NULLIF("Sales Quantity",0)), 2) AS avg_rev_per_unit,
  ROUND(AVG("Profit"), 2) AS avg_profit
FROM lm
GROUP BY "Consigned Product", "Sales Quantity"
HAVING n >= 5
ORDER BY "Consigned Product", "Sales Quantity"