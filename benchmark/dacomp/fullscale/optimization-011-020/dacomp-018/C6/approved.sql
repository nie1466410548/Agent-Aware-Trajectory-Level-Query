-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_018_c6" AS
SELECT "Customer ID", gender FROM customer_information GROUP BY "Customer ID";

-- S42
WITH cust AS (
  SELECT
    *
  FROM temp."reuse_018_c6"
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
    *
  FROM temp."reuse_018_c6"
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
    *
  FROM temp."reuse_018_c6"
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
    *
  FROM temp."reuse_018_c6"
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
    *
  FROM temp."reuse_018_c6"
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
    *
  FROM temp."reuse_018_c6"
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
    *
  FROM temp."reuse_018_c6"
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
    *
  FROM temp."reuse_018_c6"
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
    *
  FROM temp."reuse_018_c6"
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
    *
  FROM temp."reuse_018_c6"
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
    *
  FROM temp."reuse_018_c6"
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

DROP TABLE temp."reuse_018_c6";
