-- Same task, same SQLite connection, immutable main database.
-- Successful data SQL only; original failed attempts are not replayed.
-- Offline selection; source queries and metadata remain in manifest.json.

-- S3
SELECT COUNT(*) AS total_orders, COUNT(DISTINCT "Customer ID") AS customers, COUNT(DISTINCT "Product Category") AS categories FROM order_information;

-- S4
SELECT "Product Category", COUNT(*) AS orders, COUNT(DISTINCT "Customer ID") AS customers, SUM(Sales) AS total_sales, SUM(profit) AS total_profit, AVG(profit) AS avg_profit_per_order FROM order_information GROUP BY "Product Category" ORDER BY total_profit DESC;

-- S5
SELECT COUNT(*) AS total_customers FROM customer_information;

-- S6
SELECT COUNT(*) AS total_browsing FROM product_browsing;

-- S7
SELECT * FROM customer_information LIMIT 5;

-- S8
SELECT * FROM order_information WHERE "Product Category" = 'Fashion' LIMIT 5;

-- S9
SELECT * FROM product_browsing WHERE "Product Category" = 'Fashion' LIMIT 5;

-- S10
SELECT c."Customer Segment", COUNT(o."Order ID") AS orders, COUNT(DISTINCT o."Customer ID") AS customers, SUM(o.Sales) AS sales, SUM(o.profit) AS profit, AVG(o.profit) AS avg_profit, SUM(o.profit)/COUNT(DISTINCT o."Customer ID") AS profit_per_customer
FROM order_information o JOIN customer_information c ON o."Customer ID" = c."Customer ID"
WHERE o."Product Category" = 'Fashion'
GROUP BY c."Customer Segment" ORDER BY profit DESC;

-- S11
SELECT c.gender, COUNT(o."Order ID") AS orders, COUNT(DISTINCT o."Customer ID") AS customers, SUM(o.profit) AS profit, AVG(o.profit) AS avg_profit, SUM(o.profit)/COUNT(DISTINCT o."Customer ID") AS profit_per_customer
FROM order_information o JOIN customer_information c ON o."Customer ID" = c."Customer ID"
WHERE o."Product Category" = 'Fashion'
GROUP BY c.gender ORDER BY profit DESC;

-- S12
SELECT COUNT(*) AS total_fashion_customers, COUNT(DISTINCT "Customer ID") AS distinct_fashion_customers FROM order_information WHERE "Product Category" = 'Fashion';

-- S13
SELECT COUNT(*) FROM customer_information;

-- S14
SELECT COUNT(DISTINCT "Customer ID") FROM customer_information;

-- S15
SELECT "Customer ID", COUNT(*) AS cnt FROM customer_information GROUP BY "Customer ID" ORDER BY cnt DESC LIMIT 10;

-- S16
SELECT "Customer Segment", COUNT(*) FROM (SELECT DISTINCT "Customer ID", "Customer Segment" FROM customer_information) GROUP BY "Customer Segment";

-- S17
SELECT COUNT(*) AS inconsistent_segments FROM (SELECT "Customer ID", COUNT(DISTINCT "Customer Segment") AS seg_cnt FROM customer_information GROUP BY "Customer ID" HAVING seg_cnt > 1);

-- S18
SELECT COUNT(*) AS inconsistent_gender FROM (SELECT "Customer ID", COUNT(DISTINCT gender) AS g_cnt FROM customer_information GROUP BY "Customer ID" HAVING g_cnt > 1);

-- BUILD M1 before S19
CREATE TEMP TABLE "reuse_018_m1" AS
SELECT "Customer ID", "Customer Segment", gender, age, "Education Level", "Marital Status", Region, Country, City FROM customer_information GROUP BY "Customer ID";

-- BUILD INDEX M1 before S19
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

-- BUILD M2 before S25
CREATE TEMP TABLE "reuse_018_m2" AS
SELECT "Customer ID", COUNT(*) AS orders, SUM(Sales) AS sales, SUM(profit) AS profit FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID";

-- BUILD INDEX M2 before S25
CREATE INDEX temp."reuse_018_m2_customer" ON "reuse_018_m2"("Customer ID");

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

-- S26
SELECT "Product", COUNT(*) AS orders, SUM(Sales) AS sales, SUM(profit) AS profit, AVG(profit) AS avg_profit_per_order
FROM order_information WHERE "Product Category" = 'Fashion'
GROUP BY "Product" ORDER BY profit DESC;

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

-- S29
SELECT "Customer ID", COUNT(*) AS rows_cnt, SUM("Browsing Time (minutes)") AS total_browse, SUM(like) AS likes, SUM(share) AS shares, SUM("Add to Cart") AS carts
FROM product_browsing WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID" ORDER BY rows_cnt DESC LIMIT 10;

-- S30
SELECT COUNT(*) AS rows_cnt, COUNT(DISTINCT "Customer ID") AS customers FROM product_browsing WHERE "Product Category" = 'Fashion';

-- S31
SELECT "Product", COUNT(*) AS browsed, SUM(like) AS likes, SUM(share) AS shares, SUM("Add to Cart") AS carts, AVG("Browsing Time (minutes)") AS avg_browse
FROM product_browsing WHERE "Product Category" = 'Fashion' GROUP BY "Product" ORDER BY browsed DESC;

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

-- S33
WITH cust_orders AS (
  SELECT "Customer ID", COUNT(*) AS orders, SUM(profit) AS profit
  FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID"
),
cust_browse AS (
  SELECT "Customer ID", SUM(like) AS likes, SUM(share) AS shares, SUM("Add to Cart") AS carts, SUM("Browsing Time (minutes)") AS browse_time
  FROM product_browsing WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID"
)
SELECT CASE WHEN b.carts*1.0/o.orders >= 0.5 THEN 'high_cart_rate' ELSE 'low_cart_rate' END AS cart_rate_group,
  COUNT(*) AS customers, SUM(o.profit) AS profit, SUM(o.profit)/COUNT(*) AS profit_per_customer
FROM cust_orders o JOIN cust_browse b ON o."Customer ID"=b."Customer ID"
GROUP BY cart_rate_group ORDER BY profit_per_customer DESC;

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

-- S36
WITH cust_orders AS (
  SELECT "Customer ID", COUNT(*) AS orders, SUM(profit) AS profit
  FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID"
),
ranked AS (
  SELECT profit, NTILE(5) OVER (ORDER BY profit DESC) AS quintile
  FROM cust_orders
)
SELECT quintile, COUNT(*) AS customers, SUM(profit) AS profit, SUM(profit)*100.0/(SELECT SUM(profit) FROM cust_orders) AS pct_of_profit
FROM ranked GROUP BY quintile ORDER BY quintile;

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

-- S40
SELECT c.gender,
  AVG(CAST(o.Discount AS REAL)) AS avg_discount,
  SUM(CASE WHEN CAST(o.Discount AS REAL) > 0 THEN 1 ELSE 0 END)*100.0/COUNT(*) AS pct_discounted,
  AVG(CAST(o."Shipping Cost" AS REAL)) AS avg_shipping_cost,
  o."Shipping Method", COUNT(*) AS orders
FROM order_information o JOIN customer_information c ON o."Customer ID"=c."Customer ID"
WHERE o."Product Category" = 'Fashion'
GROUP BY c.gender, o."Shipping Method"
ORDER BY c.gender, orders DESC;

-- S41
SELECT DISTINCT "Shipping Method" FROM order_information;

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

-- S44
SELECT DISTINCT strftime('%Y-%m', "Order Date") AS ym FROM order_information WHERE "Product Category" = 'Fashion' ORDER BY ym;

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

DROP TABLE temp."reuse_018_m1";
DROP TABLE temp."reuse_018_m2";
