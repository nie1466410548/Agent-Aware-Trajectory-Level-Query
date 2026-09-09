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
