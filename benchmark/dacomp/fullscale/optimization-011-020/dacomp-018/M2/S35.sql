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
