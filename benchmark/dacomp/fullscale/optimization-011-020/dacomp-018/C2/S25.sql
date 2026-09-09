WITH cust AS (
  SELECT
    "Customer ID",
    Region,
    Country,
    City
  FROM customer_information
  GROUP BY
    "Customer ID"
), cust_orders AS (
  SELECT
    *
  FROM temp."reuse_018_c2"
)
SELECT
  c.Country AS "Country",
  COUNT(*) AS "customers",
  SUM(co.orders) AS "orders",
  SUM(co.profit) AS "profit",
  SUM(co.profit) / COUNT(*) AS "profit_per_customer"
FROM cust AS c
JOIN cust_orders AS co
  ON c."Customer ID" = co."Customer ID"
GROUP BY
  c.Country
ORDER BY
  profit DESC;
