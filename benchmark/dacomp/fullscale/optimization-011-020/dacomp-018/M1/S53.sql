WITH cust AS (
  SELECT
    "Customer ID",
    "gender"
  FROM temp."reuse_018_m1"
)
SELECT
  c.gender AS "gender",
  STRFTIME('%m', o."Order Date") AS "month_num",
  o."Month" AS "month_name",
  COUNT(*) AS "orders",
  SUM(o.profit) AS "profit"
FROM order_information AS o
JOIN cust AS c
  ON o."Customer ID" = c."Customer ID"
WHERE
  o."Product Category" = 'Fashion'
GROUP BY
  c.gender,
  month_num,
  month_name
ORDER BY
  month_num,
  c.gender;
