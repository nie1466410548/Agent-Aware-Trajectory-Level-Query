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
