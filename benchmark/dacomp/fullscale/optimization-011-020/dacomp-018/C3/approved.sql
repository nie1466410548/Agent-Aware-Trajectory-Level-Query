-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_018_c3" AS
SELECT "Customer ID", COUNT(*) AS orders, SUM(profit) AS profit, SUM(Sales) AS sales FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID";

-- S34
WITH cust AS (
  SELECT
    "Customer ID",
    "Customer Segment",
    gender,
    age,
    "Education Level",
    "Marital Status",
    Region,
    Country
  FROM customer_information
  GROUP BY
    "Customer ID"
), cust_orders AS (
  SELECT
    *
  FROM temp."reuse_018_c3"
), ranked AS (
  SELECT
    c.*,
    co.profit,
    co.orders,
    co.sales,
    NTILE(10) OVER (ORDER BY co.profit DESC) AS decile
  FROM cust AS c
  JOIN cust_orders AS co
    ON c."Customer ID" = co."Customer ID"
)
SELECT
  gender AS "gender",
  "Customer Segment" AS "Customer Segment",
  COUNT(*) AS "customers",
  SUM(profit) AS "profit",
  SUM(profit) / COUNT(*) AS "avg_profit"
FROM ranked
WHERE
  decile = 1
GROUP BY
  gender,
  "Customer Segment"
ORDER BY
  avg_profit DESC;

-- S35
WITH cust_orders AS (
  SELECT
    *
  FROM temp."reuse_018_c3"
)
SELECT
  COUNT(*) AS "top10_customers",
  SUM(profit) AS "top10_profit",
  SUM(profit) * 100.0 / (
    SELECT
      SUM(profit)
    FROM cust_orders
  ) AS "pct_of_total_profit"
FROM (
  SELECT
    "Customer ID",
    profit
  FROM cust_orders
  ORDER BY
    profit DESC
  LIMIT 80
);

-- S46
WITH cust AS (
  SELECT
    "Customer ID",
    gender,
    "Customer Segment",
    age,
    "Education Level",
    "Marital Status",
    Region
  FROM customer_information
  GROUP BY
    "Customer ID"
), cust_orders AS (
  SELECT
    *
  FROM temp."reuse_018_c3"
)
SELECT
  c.gender AS "gender",
  c."Customer Segment" AS "Customer Segment",
  c.Region AS "Region",
  COUNT(*) AS "customers",
  SUM(co.profit) AS "profit",
  SUM(co.profit) / COUNT(*) AS "profit_per_customer"
FROM cust AS c
JOIN cust_orders AS co
  ON c."Customer ID" = co."Customer ID"
GROUP BY
  c.gender,
  c."Customer Segment",
  c.Region
ORDER BY
  profit_per_customer DESC
LIMIT 20;

-- S47
WITH cust_orders AS (
  SELECT
    *
  FROM temp."reuse_018_c3"
)
SELECT
  CASE
    WHEN orders <= 20
    THEN '1-20'
    WHEN orders <= 40
    THEN '21-40'
    WHEN orders <= 60
    THEN '41-60'
    ELSE '60+'
  END AS "order_freq_group",
  COUNT(*) AS "customers",
  SUM(profit) AS "profit",
  SUM(profit) / COUNT(*) AS "profit_per_customer"
FROM cust_orders
GROUP BY
  order_freq_group
ORDER BY
  profit_per_customer DESC;

-- S58
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
    *
  FROM temp."reuse_018_c3"
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

DROP TABLE temp."reuse_018_c3";
