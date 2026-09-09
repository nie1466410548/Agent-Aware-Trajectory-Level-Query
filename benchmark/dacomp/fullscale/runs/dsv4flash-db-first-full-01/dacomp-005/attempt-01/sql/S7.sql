SELECT 
  COUNT(*) AS total_orders,
  COUNT(CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 END) AS low_margin_orders,
  ROUND(100.0 * COUNT(CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 END) / COUNT(*), 2) AS low_margin_pct
FROM sheet1