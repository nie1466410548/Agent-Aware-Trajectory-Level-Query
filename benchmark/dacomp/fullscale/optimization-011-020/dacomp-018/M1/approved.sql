-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_018_m1" AS
SELECT "Customer ID", "Customer Segment", gender, age, "Education Level", "Marital Status", Region, Country, City FROM customer_information GROUP BY "Customer ID";
CREATE INDEX temp."reuse_018_m1_customer" ON "reuse_018_m1"("Customer ID");

-- S19
WITH cust AS (
  SELECT
    "Customer ID",
    "Customer Segment",
    "gender",
    "age",
    "Education Level",
    "Marital Status",
    "Region",
    "Country",
    "City"
  FROM temp."reuse_018_m1"
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
    "Customer ID",
    "Customer Segment",
    "gender",
    "age",
    "Education Level",
    "Marital Status",
    "Region",
    "Country",
    "City"
  FROM temp."reuse_018_m1"
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
    "Customer ID",
    "Customer Segment",
    "gender",
    "age",
    "Education Level",
    "Marital Status",
    "Region",
    "Country",
    "City"
  FROM temp."reuse_018_m1"
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
    "Customer ID",
    "Customer Segment",
    "gender",
    "age",
    "Education Level",
    "Marital Status",
    "Region",
    "Country",
    "City"
  FROM temp."reuse_018_m1"
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
    "Customer ID",
    "Customer Segment",
    "gender",
    "age",
    "Education Level",
    "Marital Status",
    "Region",
    "Country",
    "City"
  FROM temp."reuse_018_m1"
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
    "Customer ID",
    "Customer Segment",
    "gender",
    "age",
    "Education Level",
    "Marital Status",
    "Region",
    "Country",
    "City"
  FROM temp."reuse_018_m1"
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

-- S37
WITH cust AS (
  SELECT
    "Customer ID",
    "gender",
    "Customer Segment"
  FROM temp."reuse_018_m1"
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

-- S42
WITH cust AS (
  SELECT
    "Customer ID",
    "gender"
  FROM temp."reuse_018_m1"
)
SELECT
  c.gender AS "gender",
  o."Shipping Method" AS "Shipping Method",
  COUNT(*) AS "orders",
  SUM(o.profit) AS "profit"
FROM order_information AS o
JOIN cust AS c
  ON o."Customer ID" = c."Customer ID"
WHERE
  o."Product Category" = 'Fashion'
GROUP BY
  c.gender,
  o."Shipping Method"
ORDER BY
  c.gender,
  orders DESC;

-- S43
WITH cust AS (
  SELECT
    "Customer ID",
    "gender"
  FROM temp."reuse_018_m1"
)
SELECT
  c.gender AS "gender",
  STRFTIME('%Y', o."Order Date") AS "year",
  STRFTIME('%m', o."Order Date") AS "month",
  COUNT(*) AS "orders",
  SUM(o.profit) AS "profit"
FROM order_information AS o
JOIN cust AS c
  ON o."Customer ID" = c."Customer ID"
WHERE
  o."Product Category" = 'Fashion'
GROUP BY
  c.gender,
  year,
  month
ORDER BY
  year,
  month,
  c.gender;

-- S45
WITH cust AS (
  SELECT
    "Customer ID",
    "gender"
  FROM temp."reuse_018_m1"
)
SELECT
  c.gender AS "gender",
  STRFTIME('%Y-%m', o."Order Date") AS "ym",
  COUNT(*) AS "orders",
  SUM(o.profit) AS "profit"
FROM order_information AS o
JOIN cust AS c
  ON o."Customer ID" = c."Customer ID"
WHERE
  o."Product Category" = 'Fashion'
GROUP BY
  c.gender,
  ym
ORDER BY
  ym,
  c.gender;

-- S49
WITH cust AS (
  SELECT
    "Customer ID",
    "gender"
  FROM temp."reuse_018_m1"
)
SELECT
  c.gender AS "gender",
  STRFTIME('%Y-%m', o."Order Date") AS "ym",
  SUM(o.profit) AS "profit",
  COUNT(*) AS "orders"
FROM order_information AS o
JOIN cust AS c
  ON o."Customer ID" = c."Customer ID"
WHERE
  o."Product Category" = 'Fashion'
GROUP BY
  c.gender,
  ym;

-- S50
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

-- S51
WITH cust AS (
  SELECT
    "Customer ID",
    "gender"
  FROM temp."reuse_018_m1"
)
SELECT
  c.gender AS "gender",
  o."Order Priority" AS "Order Priority",
  COUNT(*) AS "orders",
  SUM(o.profit) AS "profit",
  SUM(o.profit) / COUNT(*) AS "avg_profit_per_order"
FROM order_information AS o
JOIN cust AS c
  ON o."Customer ID" = c."Customer ID"
WHERE
  o."Product Category" = 'Fashion'
GROUP BY
  c.gender,
  o."Order Priority"
ORDER BY
  c.gender,
  orders DESC;

-- S52
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
  SUM(o.profit) AS "profit"
FROM order_information AS o
JOIN cust AS c
  ON o."Customer ID" = c."Customer ID"
WHERE
  o."Product Category" = 'Fashion'
GROUP BY
  o."Product",
  c.gender;

-- S53
WITH cust AS (
  SELECT
    "Customer ID",
    "gender"
  FROM temp."reuse_018_m1"
)
SELECT
  c.gender AS "gender",
  STRFTIME('%m', o."Order Date") AS "month_num",
  o."Month" AS "month_name",
  COUNT(*) AS "orders",
  SUM(o.profit) AS "profit"
FROM order_information AS o
JOIN cust AS c
  ON o."Customer ID" = c."Customer ID"
WHERE
  o."Product Category" = 'Fashion'
GROUP BY
  c.gender,
  month_num,
  month_name
ORDER BY
  month_num,
  c.gender;

-- S54
WITH cust AS (
  SELECT
    "Customer ID",
    "gender"
  FROM temp."reuse_018_m1"
)
SELECT
  c.gender AS "gender",
  CAST(o.Discount AS REAL) AS "discount",
  COUNT(*) AS "orders",
  SUM(o.profit) AS "profit",
  AVG(o.profit) AS "avg_profit"
FROM order_information AS o
JOIN cust AS c
  ON o."Customer ID" = c."Customer ID"
WHERE
  o."Product Category" = 'Fashion'
GROUP BY
  c.gender,
  discount
ORDER BY
  c.gender,
  discount;

-- S55
WITH cust AS (
  SELECT
    "Customer ID",
    "gender"
  FROM temp."reuse_018_m1"
)
SELECT
  c.gender AS "gender",
  STRFTIME('%m', o."Order Date") AS "mm",
  SUM(o.profit) AS "profit",
  COUNT(*) AS "orders"
FROM order_information AS o
JOIN cust AS c
  ON o."Customer ID" = c."Customer ID"
WHERE
  o."Product Category" = 'Fashion'
GROUP BY
  c.gender,
  mm;

-- S57
WITH cust AS (
  SELECT
    "Customer ID",
    "gender"
  FROM temp."reuse_018_m1"
)
SELECT
  c.gender AS "gender",
  CAST(o.Discount AS REAL) AS "discount",
  COUNT(*) AS "orders",
  SUM(o.profit) AS "profit",
  AVG(o.profit) AS "avg_profit",
  SUM(o.Sales) AS "sales"
FROM order_information AS o
JOIN cust AS c
  ON o."Customer ID" = c."Customer ID"
WHERE
  o."Product Category" = 'Fashion'
GROUP BY
  c.gender,
  discount
ORDER BY
  c.gender,
  discount;

DROP TABLE temp."reuse_018_m1";
