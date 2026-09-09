SELECT DISTINCT
  STRFTIME('%Y-%m', "Order Date") AS "ym"
FROM temp."reuse_018_c8" AS order_information
WHERE
  "Product Category" = 'Fashion'
ORDER BY
  ym;
