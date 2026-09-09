WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  is_low,
  ROUND(AVG("Discount Amount"), 2) AS avg_discount_abs,
  ROUND(AVG("Discount Amount" / NULLIF("List Price Revenue", 0) * 100), 2) AS avg_discount_rate_pct,
  COUNT(CASE WHEN "Discount Amount" > 0 THEN 1 END) AS orders_with_discount,
  ROUND(100.0 * COUNT(CASE WHEN "Discount Amount" > 0 THEN 1 END) / COUNT(*), 2) AS pct_with_discount
FROM lm
GROUP BY is_low