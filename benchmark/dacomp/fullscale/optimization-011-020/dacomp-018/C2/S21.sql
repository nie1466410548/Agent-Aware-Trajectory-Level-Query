WITH cust AS (
  SELECT
    "Customer ID",
    "Customer Segment",
    gender,
    age,
    "Education Level",
    "Marital Status",
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
), agebuckets AS (
  SELECT
    "Customer ID",
    CASE
      WHEN age < 25
      THEN '18-24'
      WHEN age < 35
      THEN '25-34'
      WHEN age < 45
      THEN '35-44'
      WHEN age < 55
      THEN '45-54'
      WHEN age < 65
      THEN '55-64'
      ELSE '65+'
    END AS age_group
  FROM cust
)
SELECT
  b.age_group AS "age_group",
  COUNT(*) AS "customers",
  SUM(co.orders) AS "orders",
  SUM(co.profit) AS "profit",
  SUM(co.profit) / COUNT(*) AS "profit_per_customer",
  SUM(co.orders) / COUNT(*) AS "orders_per_customer",
  AVG(co.profit / co.orders) AS "avg_profit_per_order"
FROM agebuckets AS b
JOIN cust_orders AS co
  ON b."Customer ID" = co."Customer ID"
GROUP BY
  b.age_group
ORDER BY
  profit_per_customer DESC;
