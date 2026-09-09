SELECT "Product Category", substr("Order Date",1,4) AS yr,
  SUM(CASE WHEN profit<0 THEN 1 ELSE 0 END) AS neg_rows,
  COUNT(*) AS n,
  SUM(CASE WHEN profit<0 THEN profit ELSE 0 END) AS neg_profit
FROM order_information GROUP BY "Product Category", yr
ORDER BY "Product Category", yr