WITH cust AS (
  SELECT
    *
  FROM temp."reuse_018_c6"
)
SELECT
  o."Product" AS "Product",
  c.gender AS "gender",
  COUNT(*) AS "orders",
  SUM(o.profit) AS "profit"
FROM order_information AS o
JOIN cust AS c
  ON o."Customer ID" = c."Customer ID"
WHERE
  o."Product Category" = 'Fashion'
GROUP BY
  o."Product",
  c.gender;
