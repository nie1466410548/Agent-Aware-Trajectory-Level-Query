WITH base AS (
  SELECT "Customer ID",
         MAX("Order Date") AS last_order,
         COUNT(DISTINCT "Order ID") AS frequency,
         SUM(profit) AS monetary_profit,
         SUM(Sales) AS monetary_sales,
         COUNT(*) AS n_rows,
         SUM(CAST("Quantity" AS REAL)) AS total_qty
  FROM order_information
  WHERE "Product Category" = 'Home & Furniture'
    AND "Quantity" != 'abc'
    AND "Quantity" IS NOT NULL
  GROUP BY "Customer ID"
)
SELECT "Customer ID",
       ROUND((julianday('2024-12-31') - julianday(last_order)),0) AS recency,
       frequency,
       ROUND(monetary_profit, 1) AS monetary,
       ROUND(monetary_sales, 0) AS sales,
       ROUND(total_qty, 1) AS total_qty
FROM base
ORDER BY "Customer ID"