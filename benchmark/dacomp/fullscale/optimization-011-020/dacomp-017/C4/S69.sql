SELECT
  "Customer ID" AS "Customer ID",
  SUM(profit) AS "profit",
  SUM(Sales) AS "sales"
FROM temp."reuse_017_c4" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
GROUP BY
  "Customer ID";
