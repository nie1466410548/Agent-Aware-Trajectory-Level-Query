SELECT yr, "Product", "Discount", COUNT(*) AS n, SUM(Sales) AS sales
FROM (
  SELECT substr("Order Date",1,4) AS yr, "Product", "Discount", Sales
  FROM order_information
  WHERE "Product Category" = 'Home & Furniture'
) t
GROUP BY yr, "Product", "Discount"
ORDER BY yr, "Product", "Discount"