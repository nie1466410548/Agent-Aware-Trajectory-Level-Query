WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  "Logistics Value-Added Service Revenue",
  is_low,
  COUNT(*) AS n,
  ROUND(AVG("Total Logistics Revenue"), 2) AS avg_rev,
  ROUND(AVG("Profit"), 2) AS avg_profit
FROM lm
GROUP BY "Logistics Value-Added Service Revenue", is_low
ORDER BY "Logistics Value-Added Service Revenue", is_low
LIMIT 30