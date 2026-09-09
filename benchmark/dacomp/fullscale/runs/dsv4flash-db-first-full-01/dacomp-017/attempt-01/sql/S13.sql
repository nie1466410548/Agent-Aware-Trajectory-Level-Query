SELECT "Product Category", substr("Order Date",1,4) AS yr,
  SUM(CASE WHEN "Discount"='xxx' OR "Quantity"='abc' OR "Quantity" IS NULL THEN 1 ELSE 0 END) AS bad_rows,
  COUNT(*) AS n
FROM order_information GROUP BY "Product Category", yr
ORDER BY "Product Category", yr