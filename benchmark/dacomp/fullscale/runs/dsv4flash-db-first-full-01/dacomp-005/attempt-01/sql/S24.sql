WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  ROUND("Freight Cost", -1) AS freight_bucket,
  is_low,
  COUNT(*) AS n,
  ROUND(AVG("Sales Quantity"), 2) AS avg_qty,
  ROUND(AVG("Total Logistics Revenue"), 2) AS avg_rev,
  ROUND(AVG("Profit"), 2) AS avg_profit
FROM lm
GROUP BY freight_bucket, is_low
ORDER BY freight_bucket, is_low
LIMIT 30