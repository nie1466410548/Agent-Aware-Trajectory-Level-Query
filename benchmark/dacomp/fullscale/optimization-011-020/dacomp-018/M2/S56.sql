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
    "Customer ID",
    "profit"
  FROM temp."reuse_018_m2"
)
SELECT
  c.gender AS "gender",
  c.age AS "age",
  co.profit AS "profit"
FROM cust AS c
JOIN cust_orders AS co
  ON c."Customer ID" = co."Customer ID";
