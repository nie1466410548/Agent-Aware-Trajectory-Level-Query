WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
  WHERE "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1)
)
SELECT 
  "Destination",
  COUNT(*) AS n,
  ROUND(AVG("Freight Cost" / NULLIF("Sales Quantity",0)), 2) AS avg_freight_per_unit,
  ROUND(AVG("Total Logistics Cost" / NULLIF("Sales Quantity",0)), 2) AS avg_cost_per_unit,
  ROUND(AVG("Total Logistics Revenue" / NULLIF("Sales Quantity",0)), 2) AS avg_rev_per_unit,
  ROUND(SUM("Profit"), 2) AS total_profit_loss
FROM lm
GROUP BY "Destination"
ORDER BY total_profit_loss ASC
LIMIT 10