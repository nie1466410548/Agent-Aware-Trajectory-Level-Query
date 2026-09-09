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
GROUP BY cart_rate_group ORDER BY profit_per_customer DESC