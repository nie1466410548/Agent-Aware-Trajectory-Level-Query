WITH cust AS (
  SELECT
    "Customer ID",
    "Customer Segment",
    gender,
    age,
    Region,
    Country
  FROM customer_information
  GROUP BY
    "Customer ID"
), cust_orders AS (
  SELECT
    *
  FROM temp."reuse_018_c2"
)
SELECT
  c.gender AS "gender",
  c."Customer Segment" AS "Customer Segment",
  COUNT(*) AS "customers",
  SUM(co.orders) AS "orders",
  SUM(co.profit) AS "profit",
  SUM(co.profit) / COUNT(*) AS "profit_per_customer",
  SUM(co.orders) / COUNT(*) AS "orders_per_customer"
FROM cust AS c
JOIN cust_orders AS co
  ON c."Customer ID" = co."Customer ID"
GROUP BY
  c.gender,
  c."Customer Segment"
ORDER BY
  profit_per_customer DESC;
