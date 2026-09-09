WITH cust AS (
  SELECT
    "Customer ID",
    gender,
    age
  FROM customer_information
  GROUP BY
    "Customer ID"
), cust_orders AS (
  SELECT
    *
  FROM temp."reuse_018_c5"
)
SELECT
  c.gender AS "gender",
  c.age AS "age",
  co.profit AS "profit"
FROM cust AS c
JOIN cust_orders AS co
  ON c."Customer ID" = co."Customer ID";
