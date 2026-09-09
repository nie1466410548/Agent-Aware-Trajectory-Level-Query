WITH base AS (
  SELECT "Customer ID",
         MAX("Order Date") AS last_order,
         COUNT(DISTINCT "Order ID") AS frequency,
         SUM(profit) AS monetary_profit,
         SUM(Sales) AS monetary_sales,
         COUNT(*) AS n_rows,
         SUM("Quantity" * 1.0) AS total_qty
  FROM order_information
  WHERE "Product Category" = 'Home & Furniture'
  GROUP BY "Customer ID"
)
SELECT "Customer ID", last_order, frequency, ROUND(monetary_profit,1) AS m_profit,
       monetary_sales, n_rows, ROUND(total_qty,1) AS total_qty,
       ROUND((julianday('2024-12-31') - julianday(last_order)),0) AS recency_days
FROM base
ORDER BY recency_days ASC
LIMIT 15