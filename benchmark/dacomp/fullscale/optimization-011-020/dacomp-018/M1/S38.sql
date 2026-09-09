WITH cust AS (
  SELECT
    "Customer ID",
    "gender",
    "Customer Segment"
  FROM temp."reuse_018_m1"
), cust_orders AS (
  SELECT
    "Customer ID",
    SUM(profit) AS profit,
    SUM(Sales) AS sales,
    COUNT(*) AS orders
  FROM order_information
  WHERE
    "Product Category" = 'Fashion'
  GROUP BY
    "Customer ID"
)
SELECT
  o."Product" AS "Product",
  c.gender AS "gender",
  COUNT(*) AS "orders",
  SUM(o.profit) AS "profit",
  SUM(o.profit) / COUNT(*) AS "profit_per_order"
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
  profit DESC;
