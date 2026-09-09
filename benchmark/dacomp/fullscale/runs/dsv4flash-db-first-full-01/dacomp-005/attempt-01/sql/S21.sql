WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  is_low,
  ROUND(AVG("Freight Cost" / NULLIF("Sales Quantity",0)), 3) AS freight_per_unit,
  ROUND(AVG("Warehousing Cost" / NULLIF("Sales Quantity",0)), 3) AS warehousing_per_unit,
  ROUND(AVG("Other Operating Costs" / NULLIF("Sales Quantity",0)), 3) AS other_per_unit,
  ROUND(AVG("Total Logistics Cost" / NULLIF("Sales Quantity",0)), 3) AS total_cost_per_unit,
  ROUND(AVG("Total Logistics Revenue" / NULLIF("Sales Quantity",0)), 3) AS rev_per_unit,
  ROUND(AVG("Logistics Unit Price"), 3) AS unit_price
FROM lm
GROUP BY is_low