WITH cust AS (
  SELECT
    "Customer ID",
    "Customer Segment",
    gender,
    age,
    "Education Level",
    "Marital Status",
    Region,
    Country
  FROM customer_information
  GROUP BY
    "Customer ID"
), cust_orders AS (
  SELECT
    "Customer ID",
    "orders",
    "profit",
    "sales"
  FROM temp."reuse_018_m2"
), ranked AS (
  SELECT
    c.*,
    co.profit,
    co.orders,
    co.sales,
    NTILE(10) OVER (ORDER BY co.profit DESC) AS decile
  FROM cust AS c
  JOIN cust_orders AS co
    ON c."Customer ID" = co."Customer ID"
)
SELECT
  gender AS "gender",
  "Customer Segment" AS "Customer Segment",
  COUNT(*) AS "customers",
  SUM(profit) AS "profit",
  SUM(profit) / COUNT(*) AS "avg_profit"
FROM ranked
WHERE
  decile = 1
GROUP BY
  gender,
  "Customer Segment"
ORDER BY
  avg_profit DESC;
