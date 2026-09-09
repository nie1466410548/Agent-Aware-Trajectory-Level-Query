WITH cust AS (
  SELECT
    "Customer ID",
    "gender"
  FROM temp."reuse_018_m1"
)
SELECT
  o."Product" AS "Product",
  c.gender AS "gender",
  COUNT(*) AS "orders",
  SUM(o.profit) AS "profit",
  SUM(o.Sales) AS "sales",
  SUM(o.profit) / COUNT(*) AS "profit_per_order",
  SUM(o.Sales) / COUNT(*) AS "sales_per_order"
FROM order_information AS o
JOIN cust AS c
  ON o."Customer ID" = c."Customer ID"
WHERE
  o."Product Category" = 'Fashion'
GROUP BY
  o."Product",
  c.gender
ORDER BY
  o."Product",
  c.gender;
