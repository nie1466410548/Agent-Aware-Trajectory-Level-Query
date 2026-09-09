WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  strftime('%Y-%m', "Date") AS month,
  SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) AS low_margin_count,
  SUM(CASE WHEN is_low = 0 THEN 1 ELSE 0 END) AS normal_count,
  ROUND(100.0 * SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) / NULLIF(SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) + SUM(CASE WHEN is_low = 0 THEN 1 ELSE 0 END), 0), 2) AS low_margin_pct
FROM lm
GROUP BY month
ORDER BY month