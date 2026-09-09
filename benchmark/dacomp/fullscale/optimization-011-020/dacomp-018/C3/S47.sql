WITH cust_orders AS (
  SELECT
    *
  FROM temp."reuse_018_c3"
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
