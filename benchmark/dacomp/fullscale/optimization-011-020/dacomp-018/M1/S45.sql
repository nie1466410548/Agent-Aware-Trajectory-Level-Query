WITH cust AS (
  SELECT
    "Customer ID",
    "gender"
  FROM temp."reuse_018_m1"
)
SELECT
  c.gender AS "gender",
  STRFTIME('%Y-%m', o."Order Date") AS "ym",
  COUNT(*) AS "orders",
  SUM(o.profit) AS "profit"
FROM order_information AS o
JOIN cust AS c
  ON o."Customer ID" = c."Customer ID"
WHERE
  o."Product Category" = 'Fashion'
GROUP BY
  c.gender,
  ym
ORDER BY
  ym,
  c.gender;
