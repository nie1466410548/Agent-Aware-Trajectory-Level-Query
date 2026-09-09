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
