WITH cust AS (
  SELECT
    "Customer ID",
    gender,
    age,
    "Customer Segment"
  FROM customer_information
  GROUP BY
    "Customer ID"
), cust_orders AS (
  SELECT
    "Customer ID",
    "orders",
    "sales",
    "profit"
  FROM temp."reuse_018_m2"
)
SELECT
  c.gender AS "gender",
  CASE WHEN c.age < 35 THEN 'under35' ELSE '35plus' END AS "age_group",
  COUNT(*) AS "customers",
  SUM(co.profit) AS "profit",
  SUM(co.profit) / COUNT(*) AS "profit_per_customer",
  SUM(co.orders) / COUNT(*) AS "orders_per_customer"
FROM cust AS c
JOIN cust_orders AS co
  ON c."Customer ID" = co."Customer ID"
GROUP BY
  c.gender,
  age_group
ORDER BY
  profit_per_customer DESC;
