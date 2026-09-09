WITH cust AS (
  SELECT
    *
  FROM temp."reuse_018_c6"
)
SELECT
  c.gender AS "gender",
  STRFTIME('%m', o."Order Date") AS "mm",
  SUM(o.profit) AS "profit",
  COUNT(*) AS "orders"
FROM order_information AS o
JOIN cust AS c
  ON o."Customer ID" = c."Customer ID"
WHERE
  o."Product Category" = 'Fashion'
GROUP BY
  c.gender,
  mm;
