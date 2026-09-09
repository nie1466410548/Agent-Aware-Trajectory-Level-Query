WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  "Consigned Product",
  ROUND(AVG(CASE WHEN is_low = 1 THEN "Freight Cost" / NULLIF("Sales Quantity", 0) END), 2) AS lm_freight_per_unit,
  ROUND(AVG(CASE WHEN is_low = 0 THEN "Freight Cost" / NULLIF("Sales Quantity", 0) END), 2) AS normal_freight_per_unit,
  ROUND(AVG(CASE WHEN is_low = 1 THEN "Total Logistics Cost" / NULLIF("Sales Quantity", 0) END), 2) AS lm_cost_per_unit,
  ROUND(AVG(CASE WHEN is_low = 0 THEN "Total Logistics Cost" / NULLIF("Sales Quantity", 0) END), 2) AS normal_cost_per_unit,
  ROUND(AVG(CASE WHEN is_low = 1 THEN "Total Logistics Revenue" / NULLIF("Sales Quantity", 0) END), 2) AS lm_rev_per_unit,
  ROUND(AVG(CASE WHEN is_low = 0 THEN "Total Logistics Revenue" / NULLIF("Sales Quantity", 0) END), 2) AS normal_rev_per_unit
FROM lm
GROUP BY "Consigned Product"
ORDER BY lm_cost_per_unit DESC