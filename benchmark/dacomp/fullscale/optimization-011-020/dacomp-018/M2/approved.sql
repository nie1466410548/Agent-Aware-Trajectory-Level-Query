-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_018_m2" AS
SELECT "Customer ID", COUNT(*) AS orders, SUM(Sales) AS sales, SUM(profit) AS profit FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID";
CREATE INDEX temp."reuse_018_m2_customer" ON "reuse_018_m2"("Customer ID");

-- S20
WITH cust AS (
  SELECT
    "Customer ID",
    "Customer Segment",
    gender,
    age,
    "Education Level",
    "Marital Status",
    Region,
    Country,
    City
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
    gender,
    age,
    "Education Level",
    "Marital Status",
    Region,
    Country,
    City
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
    gender,
    age,
    "Education Level",
    "Marital Status",
    Region,
    Country,
    City
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
    gender,
    age,
    "Education Level",
    "Marital Status",
    Region,
    Country,
    City
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
    gender,
    age,
    "Education Level",
    "Marital Status",
    Region,
    Country,
    City
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

-- S25
WITH cust AS (
  SELECT
    "Customer ID",
    Region,
    Country,
    City
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
  c.Country AS "Country",
  COUNT(*) AS "customers",
  SUM(co.orders) AS "orders",
  SUM(co.profit) AS "profit",
  SUM(co.profit) / COUNT(*) AS "profit_per_customer"
FROM cust AS c
JOIN cust_orders AS co
  ON c."Customer ID" = co."Customer ID"
GROUP BY
  c.Country
ORDER BY
  profit DESC;

-- S27
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
    "Customer ID",
    "orders",
    "sales",
    "profit"
  FROM temp."reuse_018_m2"
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

-- S28
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

-- S32
WITH cust AS (
  SELECT
    "Customer ID",
    "Customer Segment",
    gender,
    age
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
), cust_browse AS (
  SELECT
    "Customer ID",
    SUM("like") AS likes,
    SUM(share) AS shares,
    SUM("Add to Cart") AS carts,
    SUM("Browsing Time (minutes)") AS browse_time
  FROM product_browsing
  WHERE
    "Product Category" = 'Fashion'
  GROUP BY
    "Customer ID"
)
SELECT
  c.gender AS "gender",
  c."Customer Segment" AS "Customer Segment",
  AVG(b.carts * 1.0 / o.orders) AS "carts_per_order",
  AVG(b.likes * 1.0 / o.orders) AS "likes_per_order",
  AVG(b.shares * 1.0 / o.orders) AS "shares_per_order",
  AVG(b.browse_time / o.orders) AS "browse_min_per_order",
  SUM(o.profit) / COUNT(*) AS "profit_per_customer"
FROM cust AS c
JOIN cust_orders AS o
  ON c."Customer ID" = o."Customer ID"
JOIN cust_browse AS b
  ON c."Customer ID" = b."Customer ID"
GROUP BY
  c.gender,
  c."Customer Segment"
ORDER BY
  profit_per_customer DESC;

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
    "Customer ID",
    "orders",
    "profit",
    "sales"
  FROM temp."reuse_018_m2"
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
    "Customer ID",
    "orders",
    "profit",
    "sales"
  FROM temp."reuse_018_m2"
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
    "Customer ID",
    "profit"
  FROM temp."reuse_018_m2"
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
    "Customer ID",
    "orders",
    "profit",
    "sales"
  FROM temp."reuse_018_m2"
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

-- S48
WITH cust AS (
  SELECT
    "Customer ID",
    "Customer Segment" AS segment,
    gender,
    age
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
), cust_browse AS (
  SELECT
    "Customer ID",
    SUM("like") AS likes,
    SUM(share) AS shares,
    SUM("Add to Cart") AS carts,
    SUM("Browsing Time (minutes)") AS browse_time
  FROM product_browsing
  WHERE
    "Product Category" = 'Fashion'
  GROUP BY
    "Customer ID"
)
SELECT
  c.gender AS "gender",
  c.segment AS "segment",
  o.orders AS "orders",
  o.profit AS "profit",
  o.sales AS "sales",
  b.likes AS "likes",
  b.shares AS "shares",
  b.carts AS "carts",
  b.browse_time AS "browse_time"
FROM cust AS c
JOIN cust_orders AS o
  ON c."Customer ID" = o."Customer ID"
JOIN cust_browse AS b
  ON c."Customer ID" = b."Customer ID";

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
    "Customer ID",
    "profit"
  FROM temp."reuse_018_m2"
)
SELECT
  c.gender AS "gender",
  c.age AS "age",
  co.profit AS "profit"
FROM cust AS c
JOIN cust_orders AS co
  ON c."Customer ID" = co."Customer ID";

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

DROP TABLE temp."reuse_018_m2";
