WITH cust AS (
  SELECT "Customer ID", "Customer Segment", gender, age
  FROM customer_information GROUP BY "Customer ID"
),
cust_orders AS (
  SELECT "Customer ID", COUNT(*) AS orders, SUM(profit) AS profit, SUM(Sales) AS sales
  FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID"
),
cust_browse AS (
  SELECT "Customer ID", SUM(like) AS likes, SUM(share) AS shares, SUM("Add to Cart") AS carts, SUM("Browsing Time (minutes)") AS browse_time
  FROM product_browsing WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID"
)
SELECT c.gender, c."Customer Segment",
  AVG(b.carts*1.0/o.orders) AS carts_per_order,
  AVG(b.likes*1.0/o.orders) AS likes_per_order,
  AVG(b.shares*1.0/o.orders) AS shares_per_order,
  AVG(b.browse_time/o.orders) AS browse_min_per_order,
  SUM(o.profit)/COUNT(*) AS profit_per_customer
FROM cust c JOIN cust_orders o ON c."Customer ID"=o."Customer ID" JOIN cust_browse b ON c."Customer ID"=b."Customer ID"
GROUP BY c.gender, c."Customer Segment" ORDER BY profit_per_customer DESC