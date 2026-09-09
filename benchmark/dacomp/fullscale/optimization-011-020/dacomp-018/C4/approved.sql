-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_018_c4" AS
SELECT "Customer ID", gender, "Customer Segment" FROM customer_information GROUP BY "Customer ID";

-- S37
WITH cust AS (
  SELECT
    *
  FROM temp."reuse_018_c4"
), cust_orders AS (
  SELECT
    "Customer ID",
    SUM(profit) AS profit
  FROM order_information
  WHERE
    "Product Category" = 'Fashion'
  GROUP BY
    "Customer ID"
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

-- S38
WITH cust AS (
  SELECT
    *
  FROM temp."reuse_018_c4"
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

DROP TABLE temp."reuse_018_c4";
