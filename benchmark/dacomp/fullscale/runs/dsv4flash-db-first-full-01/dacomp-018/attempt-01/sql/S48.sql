
WITH cust AS (
  SELECT "Customer ID", "Customer Segment" AS segment, gender, age
  FROM customer_information GROUP BY "Customer ID"
),
cust_orders AS (
  SELECT "Customer ID", COUNT(*) AS orders, SUM(profit) AS profit, SUM(Sales) AS sales
  FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID"
),
cust_browse AS (
  SELECT "Customer ID", SUM(like) AS likes, SUM(share) AS shares, SUM("Add to Cart") AS carts,
         SUM("Browsing Time (minutes)") AS browse_time
  FROM product_browsing WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID"
)
SELECT c.gender, c.segment, o.orders, o.profit, o.sales, b.likes, b.shares, b.carts, b.browse_time
FROM cust c JOIN cust_orders o ON c."Customer ID"=o."Customer ID"
JOIN cust_browse b ON c."Customer ID"=b."Customer ID"
