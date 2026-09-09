-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_018_c1" AS
SELECT "Customer ID", "Customer Segment", gender, age, "Education Level", "Marital Status", Region, Country, City FROM customer_information GROUP BY "Customer ID";

-- S19
WITH cust AS (
  SELECT
    *
  FROM temp."reuse_018_c1"
), cust_orders AS (
  SELECT
    "Customer ID",
    COUNT(*) AS orders,
    COUNT(DISTINCT "Order ID") AS order_ids,
    SUM(Sales) AS sales,
    SUM(profit) AS profit,
    SUM(CASE WHEN NOT Discount IS NULL AND CAST(Discount AS REAL) > 0 THEN 1 ELSE 0 END) AS discounted_orders
  FROM order_information
  WHERE
    "Product Category" = 'Fashion'
  GROUP BY
    "Customer ID"
)
SELECT
  c."Customer Segment" AS "Customer Segment",
  COUNT(*) AS "customers",
  SUM(co.orders) AS "fashion_orders",
  SUM(co.sales) AS "sales",
  SUM(co.profit) AS "profit",
  SUM(co.profit) / COUNT(*) AS "profit_per_customer",
  SUM(co.orders) / COUNT(*) AS "orders_per_customer",
  AVG(co.profit / co.orders) AS "avg_profit_per_order"
FROM cust AS c
JOIN cust_orders AS co
  ON c."Customer ID" = co."Customer ID"
GROUP BY
  c."Customer Segment"
ORDER BY
  profit DESC;

-- S20
WITH cust AS (
  SELECT
    *
  FROM temp."reuse_018_c1"
), cust_orders AS (
  SELECT
    "Customer ID",
    COUNT(*) AS orders,
    SUM(Sales) AS sales,
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
  SUM(co.orders) AS "fashion_orders",
  SUM(co.sales) AS "sales",
  SUM(co.profit) AS "profit",
  SUM(co.profit) / COUNT(*) AS "profit_per_customer",
  SUM(co.orders) / COUNT(*) AS "orders_per_customer",
  AVG(co.profit / co.orders) AS "avg_profit_per_order"
FROM cust AS c
JOIN cust_orders AS co
  ON c."Customer ID" = co."Customer ID"
GROUP BY
  c.gender
ORDER BY
  profit DESC;

-- S21
WITH cust AS (
  SELECT
    *
  FROM temp."reuse_018_c1"
), cust_orders AS (
  SELECT
    "Customer ID",
    COUNT(*) AS orders,
    SUM(Sales) AS sales,
    SUM(profit) AS profit
  FROM order_information
  WHERE
    "Product Category" = 'Fashion'
  GROUP BY
    "Customer ID"
), agebuckets AS (
  SELECT
    "Customer ID",
    CASE
      WHEN age < 25
      THEN '18-24'
      WHEN age < 35
      THEN '25-34'
      WHEN age < 45
      THEN '35-44'
      WHEN age < 55
      THEN '45-54'
      WHEN age < 65
      THEN '55-64'
      ELSE '65+'
    END AS age_group
  FROM cust
)
SELECT
  b.age_group AS "age_group",
  COUNT(*) AS "customers",
  SUM(co.orders) AS "orders",
  SUM(co.profit) AS "profit",
  SUM(co.profit) / COUNT(*) AS "profit_per_customer",
  SUM(co.orders) / COUNT(*) AS "orders_per_customer",
  AVG(co.profit / co.orders) AS "avg_profit_per_order"
FROM agebuckets AS b
JOIN cust_orders AS co
  ON b."Customer ID" = co."Customer ID"
GROUP BY
  b.age_group
ORDER BY
  profit_per_customer DESC;

-- S22
WITH cust AS (
  SELECT
    *
  FROM temp."reuse_018_c1"
), cust_orders AS (
  SELECT
    "Customer ID",
    COUNT(*) AS orders,
    SUM(Sales) AS sales,
    SUM(profit) AS profit
  FROM order_information
  WHERE
    "Product Category" = 'Fashion'
  GROUP BY
    "Customer ID"
)
SELECT
  c."Education Level" AS "Education Level",
  COUNT(*) AS "customers",
  SUM(co.orders) AS "orders",
  SUM(co.profit) AS "profit",
  SUM(co.profit) / COUNT(*) AS "profit_per_customer",
  SUM(co.orders) / COUNT(*) AS "orders_per_customer",
  AVG(co.profit / co.orders) AS "avg_profit_per_order"
FROM cust AS c
JOIN cust_orders AS co
  ON c."Customer ID" = co."Customer ID"
GROUP BY
  c."Education Level"
ORDER BY
  profit DESC;

-- S23
WITH cust AS (
  SELECT
    *
  FROM temp."reuse_018_c1"
), cust_orders AS (
  SELECT
    "Customer ID",
    COUNT(*) AS orders,
    SUM(Sales) AS sales,
    SUM(profit) AS profit
  FROM order_information
  WHERE
    "Product Category" = 'Fashion'
  GROUP BY
    "Customer ID"
)
SELECT
  c."Marital Status" AS "Marital Status",
  COUNT(*) AS "customers",
  SUM(co.orders) AS "orders",
  SUM(co.profit) AS "profit",
  SUM(co.profit) / COUNT(*) AS "profit_per_customer",
  SUM(co.orders) / COUNT(*) AS "orders_per_customer",
  AVG(co.profit / co.orders) AS "avg_profit_per_order"
FROM cust AS c
JOIN cust_orders AS co
  ON c."Customer ID" = co."Customer ID"
GROUP BY
  c."Marital Status"
ORDER BY
  profit DESC;

-- S24
WITH cust AS (
  SELECT
    *
  FROM temp."reuse_018_c1"
), cust_orders AS (
  SELECT
    "Customer ID",
    COUNT(*) AS orders,
    SUM(Sales) AS sales,
    SUM(profit) AS profit
  FROM order_information
  WHERE
    "Product Category" = 'Fashion'
  GROUP BY
    "Customer ID"
)
SELECT
  c.Region AS "Region",
  COUNT(*) AS "customers",
  SUM(co.orders) AS "orders",
  SUM(co.profit) AS "profit",
  SUM(co.profit) / COUNT(*) AS "profit_per_customer",
  SUM(co.orders) / COUNT(*) AS "orders_per_customer"
FROM cust AS c
JOIN cust_orders AS co
  ON c."Customer ID" = co."Customer ID"
GROUP BY
  c.Region
ORDER BY
  profit DESC;

DROP TABLE temp."reuse_018_c1";
