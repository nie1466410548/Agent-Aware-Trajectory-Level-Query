WITH cust AS (
  SELECT
    *
  FROM temp."reuse_018_c6"
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
