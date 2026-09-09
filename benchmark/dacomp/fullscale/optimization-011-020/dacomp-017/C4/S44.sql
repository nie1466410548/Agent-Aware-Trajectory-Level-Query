SELECT
  COUNT(DISTINCT "Order ID") AS "n_orders"
FROM temp."reuse_017_c4" AS order_information
WHERE
  "Product Category" = 'Home & Furniture';
