SELECT "Consigned Product" AS product,
  strftime('%Y-%m', "Date") AS month,
  COUNT(*) AS orders,
  ROUND(SUM("Profit"),2) AS profit,
  SUM(CASE WHEN "Profit" < 0 THEN 1 ELSE 0 END) AS neg_orders,
  ROUND(SUM(CASE WHEN "Profit" < 0 THEN "Profit" ELSE 0 END),2) AS neg_profit_sum
FROM sheet1
WHERE "Destination" LIKE 'South China%'
GROUP BY product, month
ORDER BY product, month