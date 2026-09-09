WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  "Destination",
  COUNT(*) AS total,
  SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) AS low_cnt,
  ROUND(100.0 * SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS low_pct,
  ROUND(AVG("Sales Quantity"), 2) AS avg_qty,
  ROUND(AVG("Discount Amount" / NULLIF("List Price Revenue",0) * 100), 2) AS avg_disc_rate
FROM lm
GROUP BY "Destination"
HAVING total >= 30
ORDER BY low_pct DESC
LIMIT 20