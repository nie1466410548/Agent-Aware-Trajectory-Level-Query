WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  is_low,
  ROUND(AVG("Logistics Value-Added Service Revenue"), 2) AS avg_vas,
  ROUND(AVG("Logistics Value-Added Service Revenue") / NULLIF(AVG("Total Logistics Revenue"), 0) * 100, 2) AS vas_pct_of_rev,
  COUNT(CASE WHEN "Logistics Value-Added Service Revenue" > 0 THEN 1 END) AS vas_orders,
  ROUND(100.0 * COUNT(CASE WHEN "Logistics Value-Added Service Revenue" > 0 THEN 1 END) / COUNT(*), 2) AS pct_vas_orders
FROM lm
GROUP BY is_low