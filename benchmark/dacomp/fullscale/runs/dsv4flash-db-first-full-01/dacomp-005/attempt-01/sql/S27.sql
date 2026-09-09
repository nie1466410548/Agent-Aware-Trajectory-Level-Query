WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  SUBSTR("Destination", 1, INSTR("Destination", '-') - 1) AS region,
  SUBSTR("Destination", INSTR("Destination", '-') + 1, INSTR(SUBSTR("Destination", INSTR("Destination", '-') + 1), '-') - 1) AS province,
  is_low,
  COUNT(*) AS n,
  ROUND(AVG("Freight Cost"), 2) AS avg_freight,
  ROUND(AVG("Sales Quantity"), 2) AS avg_qty,
  ROUND(AVG("Freight Cost" / NULLIF("Sales Quantity", 0)), 2) AS freight_per_unit
FROM lm
WHERE is_low = 1
GROUP BY region, province
ORDER BY avg_freight DESC
LIMIT 15