WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  is_low,
  MIN("Sales Quantity") AS min_qty,
  ROUND(AVG("Sales Quantity"),2) AS avg_qty,
  MAX("Sales Quantity") AS max_qty,
  COUNT(CASE WHEN "Sales Quantity" <= 6 THEN 1 END) AS qty_le_6,
  ROUND(100.0 * COUNT(CASE WHEN "Sales Quantity" <= 6 THEN 1 END) / COUNT(*), 2) AS pct_qty_le_6
FROM lm
GROUP BY is_low