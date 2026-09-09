-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_018_c5" AS
SELECT "Customer ID", SUM(profit) AS profit FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID";

-- S37
WITH cust AS (
  SELECT
    "Customer ID",
    gender,
    "Customer Segment"
  FROM customer_information
  GROUP BY
    "Customer ID"
), cust_orders AS (
  SELECT
    *
  FROM temp."reuse_018_c5"
)
SELECT
  c.gender AS "gender",
  COUNT(*) AS "customers",
  COUNT(*) * 100.0 / 795 AS "pct_of_customers",
  SUM(co.profit) AS "profit",
  SUM(co.profit) * 100.0 / (
    SELECT
      SUM(profit)
    FROM cust_orders
  ) AS "pct_of_profit",
  SUM(co.profit) / COUNT(*) AS "profit_per_customer"
FROM cust AS c
JOIN cust_orders AS co
  ON c."Customer ID" = co."Customer ID"
GROUP BY
  c.gender;

-- S56
WITH cust AS (
  SELECT
    "Customer ID",
    gender,
    age
  FROM customer_information
  GROUP BY
    "Customer ID"
), cust_orders AS (
  SELECT
    *
  FROM temp."reuse_018_c5"
)
SELECT
  c.gender AS "gender",
  c.age AS "age",
  co.profit AS "profit"
FROM cust AS c
JOIN cust_orders AS co
  ON c."Customer ID" = co."Customer ID";

DROP TABLE temp."reuse_018_c5";
