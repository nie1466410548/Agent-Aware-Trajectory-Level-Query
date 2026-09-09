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
