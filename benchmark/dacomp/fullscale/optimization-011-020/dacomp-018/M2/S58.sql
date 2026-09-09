WITH cust AS (
  SELECT
    "Customer ID",
    "Customer Segment",
    gender,
    age,
    "Education Level",
    "Marital Status",
    Region
  FROM customer_information
  GROUP BY
    "Customer ID"
), cust_orders AS (
  SELECT
    "Customer ID",
    "orders",
    "profit",
    "sales"
  FROM temp."reuse_018_m2"
)
SELECT
  c.gender AS "gender",
  c."Customer Segment" AS "Customer Segment",
  c.Region AS "Region",
  c."Marital Status" AS "Marital Status",
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
  c."Customer Segment",
  c.Region,
  c."Marital Status"
ORDER BY
  profit_per_customer DESC
LIMIT 15;
